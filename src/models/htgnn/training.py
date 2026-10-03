"""
training.py — Temporal Contrastive Pre-Training, Supervised Learning, and Latent Extraction.
"""
import os
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, *args, **kwargs):
        return iterable

from .profiles import get_dataset_profile
from .model import BurstAwareHGT, FocalLoss, EWC
from .builder import build_hetero_data, get_neighbor_loader

def train_temporal_contrastive_pretraining(model, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, num_epochs=5, temperature=0.1):
    """
    Multi-Scale Self-Supervised Temporal Contrastive Pretraining (InfoNCE):
    Learns invariant spatiotemporal node representations across fast bursts and long-term dormancy.
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    model.train()
    
    # Sub-sample large graphs for memory safety
    total_nodes = sum(x.shape[0] for x in x_dict.values())
    if total_nodes > 250_000:
        sample_ratio = min(1.0, 200_000.0 / max(1, total_nodes))
        sub_x_dict = {}
        sub_edge_index = {}
        sub_delta_t = {}
        sub_burst = {}
        node_sub_limits = {}
        
        for nt, x in x_dict.items():
            n_sub = max(100, int(x.shape[0] * sample_ratio))
            sub_x_dict[nt] = x[:n_sub]
            node_sub_limits[nt] = n_sub
            
        for rel, edge_index in edge_index_dict.items():
            src_nt, _, dst_nt = rel
            max_s = node_sub_limits.get(src_nt, 0)
            max_d = node_sub_limits.get(dst_nt, 0)
            if edge_index.numel() > 0:
                e_mask = (edge_index[0] < max_s) & (edge_index[1] < max_d)
                sub_edge_index[rel] = edge_index[:, e_mask]
                sub_delta_t[rel] = delta_t_dict[rel][e_mask] if rel in delta_t_dict else torch.zeros(0)
                sub_burst[rel] = burst_score_dict[rel][e_mask] if rel in burst_score_dict else torch.zeros(0)
            else:
                sub_edge_index[rel] = edge_index
                sub_delta_t[rel] = delta_t_dict.get(rel, torch.zeros(0))
                sub_burst[rel] = burst_score_dict.get(rel, torch.zeros(0))
        use_x = sub_x_dict
        use_edge = sub_edge_index
        use_dt = sub_delta_t
        use_burst = sub_burst
    else:
        use_x = x_dict
        use_edge = edge_index_dict
        use_dt = delta_t_dict
        use_burst = burst_score_dict

    print("  [Pipeline] [1/5] Multi-Scale Contrastive Pretraining (InfoNCE)...")
    pretrain_bar = tqdm(range(1, num_epochs + 1), desc="  [Pretrain] InfoNCE", unit="ep", dynamic_ncols=True, leave=False)
    for epoch in pretrain_bar:
        optimizer.zero_grad()
        
        # View 1: Multi-scale log-temporal masking + 10% feature dropout
        delta_t_v1 = {rel: dt * torch.exp(0.20 * torch.randn_like(dt)) for rel, dt in use_dt.items()}
        x_dict_v1 = {nt: F.dropout(x, p=0.10, training=True) for nt, x in use_x.items()}
        z_v1 = model.get_embeddings(x_dict_v1, use_edge, delta_t_v1, use_burst)
        
        # View 2: Counter-jitter log-temporal scaling + 10% feature dropout
        delta_t_v2 = {rel: dt * torch.exp(-0.20 * torch.randn_like(dt)) for rel, dt in use_dt.items()}
        x_dict_v2 = {nt: F.dropout(x, p=0.10, training=True) for nt, x in use_x.items()}
        z_v2 = model.get_embeddings(x_dict_v2, use_edge, delta_t_v2, use_burst)
        
        device = next(model.parameters()).device
        total_contrastive_loss = torch.tensor(0.0, device=device)
        for nt in z_v1:
            if z_v1[nt].shape[0] < 2:
                continue
            h1 = F.normalize(z_v1[nt], p=2, dim=-1)
            h2 = F.normalize(z_v2[nt], p=2, dim=-1)
            
            # Subsample for memory efficiency
            if h1.shape[0] > 2000:
                idx = torch.randperm(h1.shape[0], device=h1.device)[:2000]
                h1 = h1[idx]
                h2 = h2[idx]
                
            sim_matrix = torch.mm(h1, h2.t()) / temperature
            labels = torch.arange(h1.shape[0], device=h1.device)
            loss_nt = F.cross_entropy(sim_matrix, labels)
            total_contrastive_loss = total_contrastive_loss + loss_nt
            
        total_contrastive_loss.backward()
        optimizer.step()
        pretrain_bar.set_postfix({"Loss": f"{total_contrastive_loss.item():.4f}"})
    print(f"    -> InfoNCE Pretrain Completed ({num_epochs} epochs) | Final Loss: {total_contrastive_loss.item():.4f}")


def train_htgnn(dataset_name, num_epochs=50, learning_rate=0.001, prev_ewc=None, ewc_lambda=100.0, preloaded_data=None, *args, **kwargs):
    """
    Train HT-GNN using 3-way chronological split protocol (Temporal Validation).
    Evaluates predictive capacity under Concept Drift with Early Stopping & Checkpoint Recovery.
    """
    import copy
    print(f"\n{'='*70}")
    print(f" Burst-Aware HT-GNN Training (Temporal Splitting): {dataset_name}")
    print(f"{'='*70}")

    if preloaded_data is None:
        preloaded_data = kwargs.get("preloaded_data", None)

    if preloaded_data is not None:
        data = preloaded_data
    else:
        data = build_hetero_data(dataset_name)
    
    # Confirm label presence on the node type containing labels and populated nodes
    target_node = None
    for nt in data.node_types:
        if hasattr(data[nt], "y") and data[nt].y is not None and data[nt].y.numel() > 0:
            if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
                target_node = nt
                break
            
    if target_node is None:
        for nt in data.node_types:
            if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
                target_node = nt
                break
        if target_node is None:
            target_node = data.node_types[0]
        
    has_labels = target_node in data.node_types and hasattr(data[target_node], "y") and data[target_node].y is not None
    
    if not has_labels:
        print(f"  [ERROR] Training aborted: Target node type '{target_node}' does not have label attributes.")
        return None, None

    # Chronological 3-Way Split Protocol: 60% Train / 10% Validation / 30% Test
    num_target_nodes_orig = data[target_node].x.shape[0]
    train_split_idx = int(num_target_nodes_orig * 0.60)
    val_split_idx = int(num_target_nodes_orig * 0.70)
    train_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    train_mask_nodes[:train_split_idx] = True
    
    val_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    val_mask_nodes[train_split_idx:val_split_idx] = True
    
    test_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    test_mask_nodes[val_split_idx:num_target_nodes_orig] = True
    
    # Stratification safeguard if test slice lacks positive representation (Upgrade I)
    y_target = data[target_node].y
    total_positives = int((y_target == 1).sum().item())
    test_positives = int((y_target[test_mask_nodes] == 1).sum().item())
    
    if test_positives < 2 and total_positives >= 5:
        print(f"  [Temporal Split] Pure index partition yielded {test_positives} test positives. Applying temporal-stratified partition...")
        pos_indices = torch.where(y_target == 1)[0]
        neg_indices = torch.where(y_target == 0)[0]
        unl_indices = torch.where(y_target < 0)[0]
        
        n_pos = len(pos_indices)
        n_neg = len(neg_indices)
        n_unl = len(unl_indices)
        
        train_pos = pos_indices[:int(n_pos * 0.60)]
        val_pos = pos_indices[int(n_pos * 0.60):int(n_pos * 0.70)]
        test_pos = pos_indices[int(n_pos * 0.70):]
        
        train_neg = neg_indices[:int(n_neg * 0.60)]
        val_neg = neg_indices[int(n_neg * 0.60):int(n_neg * 0.70)]
        test_neg = neg_indices[int(n_neg * 0.70):]
        
        train_unl = unl_indices[:int(n_unl * 0.60)]
        val_unl = unl_indices[int(n_unl * 0.60):int(n_unl * 0.70)]
        test_unl = unl_indices[int(n_unl * 0.70):]
        
        train_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        train_mask_nodes[torch.cat([train_pos, train_neg, train_unl])] = True
        
        val_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        val_mask_nodes[torch.cat([val_pos, val_neg, val_unl])] = True
        
        test_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        test_mask_nodes[torch.cat([test_pos, test_neg, test_unl])] = True
    
    train_mask_nodes_augmented = train_mask_nodes

    # Identify metadata
    metadata = data.metadata()
    in_channels_dict = {nt: data[nt].x.shape[1] for nt in metadata[0]}
    
    # Compute inverse class frequencies for balancing alpha in FocalLoss
    y_train_valid = y_target[train_mask_nodes]
    y_train_clean = y_train_valid[y_train_valid >= 0]
    if y_train_clean.numel() > 0:
        counts = torch.bincount(y_train_clean)
        alpha = 1.0 / (counts.float() + 1e-6)
        alpha = alpha / alpha.sum()
    else:
        alpha = torch.tensor([0.5, 0.5])
        
    num_total_nodes = sum(data[nt].num_nodes for nt in data.node_types if hasattr(data[nt], "num_nodes") and data[nt].num_nodes is not None)
    
    # Dataset-Adaptive Hyperparameter Profiles
    profile = get_dataset_profile(dataset_name)
    effective_gnn_layers = profile["gnn_layers"]
    effective_hidden = profile["hidden"]
    effective_lr = profile["lr"]
    effective_focal_beta = profile["focal_beta"]
    effective_smote_ratio = profile["smote_ratio"]
    effective_xgb_n = profile["xgb_n"]
    effective_xgb_depth = profile["xgb_depth"]
    
    # Override hidden, layer depth and epoch schedule for massive graphs
    patience = 10
    effective_epochs = num_epochs
    effective_patience = patience
    min_epochs_early_stop = 10
    if num_total_nodes > 5_000_000:
        effective_hidden = min(effective_hidden, 32)
        effective_gnn_layers = min(effective_gnn_layers, 3)
        effective_epochs = min(num_epochs, 6)
        effective_patience = 2
        min_epochs_early_stop = 3
    elif num_total_nodes > 2_000_000:
        effective_hidden = min(effective_hidden, 48)
        effective_gnn_layers = min(effective_gnn_layers, 4)
        effective_epochs = min(num_epochs, 10)
        effective_patience = 3
        min_epochs_early_stop = 5
    elif num_total_nodes > 500_000:
        effective_hidden = min(effective_hidden, 64)
    
    print(f"  [Profile] Dataset '{dataset_name}' -> GNN Layers={effective_gnn_layers}, Hidden={effective_hidden}, LR={effective_lr}, beta={effective_focal_beta}, SMOTE={effective_smote_ratio}, Epochs={effective_epochs}")
    
    model = BurstAwareHGT(
        in_channels_dict=in_channels_dict,
        hidden_channels=effective_hidden,
        num_layers=effective_gnn_layers,
        metadata=metadata,
        dropout=DROPOUT,
        jk_mode="cat" if effective_gnn_layers >= 4 else None
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=effective_lr, weight_decay=0.0001)
    from torch.optim.lr_scheduler import OneCycleLR, CosineAnnealingLR
    try:
        scheduler = OneCycleLR(optimizer, max_lr=max(1e-3, effective_lr * 2.5), total_steps=max(2, effective_epochs), pct_start=0.15, anneal_strategy="cos")
    except Exception:
        scheduler = CosineAnnealingLR(optimizer, T_max=effective_epochs, eta_min=1e-5)
    
    try:
        from .focal_tversky_loss import CostSensitiveFocalTverskyLoss
        from .soft_f1_loss import CompositeAMLObjective
        base_criterion = CostSensitiveFocalTverskyLoss(alpha=max(0.10, 1.0 - effective_focal_beta), beta=effective_focal_beta, gamma=1.33, adaptive_imbalance=True)
        criterion = CompositeAMLObjective(base_criterion, soft_f1_weight=0.60, supcon_weight=0.10)
    except Exception:
        criterion = FocalLoss(alpha=alpha, gamma=2.0, label_smoothing=0.05)

    all_ts_tensors = []
    for rel in metadata[1]:
        if rel in data:
            if hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0:
                all_ts_tensors.append(data[rel].ts.float().flatten())
            elif hasattr(data[rel], "delta_t") and data[rel].delta_t is not None and data[rel].delta_t.numel() > 0:
                all_ts_tensors.append(data[rel].delta_t.float().flatten())
            
    if all_ts_tensors:
        cat_ts = torch.cat(all_ts_tensors)
        ts_train_thresh = float(torch.quantile(cat_ts, 0.60).item())
        ts_val_thresh = float(torch.quantile(cat_ts, 0.70).item())
        del cat_ts, all_ts_tensors
    else:
        ts_train_thresh, ts_val_thresh = 0.0, 0.0

    # Build mask dictionaries for 3-way temporal split using absolute timestamps (Upgrade D)
    train_edge_index, train_delta_t, train_burst_score = {}, {}, {}
    val_edge_index, val_delta_t, val_burst_score = {}, {}, {}
    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index
            delta_t = data[rel].delta_t
            burst_score = data[rel].burst_score
            rel_ts = data[rel].ts if (hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0) else delta_t
            
            t_mask = rel_ts <= ts_train_thresh
            v_mask = (rel_ts > ts_train_thresh) & (rel_ts <= ts_val_thresh)
            te_mask = rel_ts > ts_val_thresh
            
            train_edge_index[rel] = edge_index[:, t_mask]
            train_delta_t[rel] = delta_t[t_mask]
            train_burst_score[rel] = burst_score[t_mask]
            
            val_edge_index[rel] = edge_index[:, t_mask | v_mask]
            val_delta_t[rel] = delta_t[t_mask | v_mask]
            val_burst_score[rel] = burst_score[t_mask | v_mask]
            
            test_edge_index[rel] = edge_index[:, te_mask]
            test_delta_t[rel] = delta_t[te_mask]
            test_burst_score[rel] = burst_score[te_mask]

    # Move model and graph tensors to CUDA accelerator if available
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    use_cuda = (device.type == 'cuda')
    if use_cuda:
        try:
            torch.backends.cudnn.benchmark = True
            torch.cuda.empty_cache()
            model = model.to(device)
            x_dict = {nt: data[nt].x.to(device) for nt in metadata[0]}
            train_edge_index = {rel: train_edge_index[rel].to(device) for rel in train_edge_index}
            train_delta_t = {rel: train_delta_t[rel].to(device) for rel in train_delta_t}
            train_burst_score = {rel: train_burst_score[rel].to(device) for rel in train_burst_score}
            val_edge_index = {rel: val_edge_index[rel].to(device) for rel in val_edge_index}
            val_delta_t = {rel: val_delta_t[rel].to(device) for rel in val_delta_t}
            val_burst_score = {rel: val_burst_score[rel].to(device) for rel in val_burst_score}
            test_edge_index = {rel: test_edge_index[rel].to(device) for rel in test_edge_index}
            test_delta_t = {rel: test_delta_t[rel].to(device) for rel in test_delta_t}
            test_burst_score = {rel: test_burst_score[rel].to(device) for rel in test_burst_score}
            y_target = y_target.to(device)
            train_mask_nodes_augmented = train_mask_nodes_augmented.to(device)
            val_mask_nodes = val_mask_nodes.to(device)
            test_mask_nodes = test_mask_nodes.to(device)
            if hasattr(criterion, 'to'):
                criterion = criterion.to(device)
        except (torch.cuda.OutOfMemoryError, RuntimeError) as oom:
            print(f"  [Memory Guard] Graph memory exceeded GPU VRAM, falling back to CPU: {oom}")
            device = torch.device('cpu')
            model = model.to(device)
            torch.cuda.empty_cache()
            x_dict = {nt: data[nt].x for nt in metadata[0]}
    else:
        x_dict = {nt: data[nt].x for nt in metadata[0]}

    # Step 1: Self-Supervised Temporal Contrastive Pretraining (Pruned 2-Epoch Cosine Anneal)
    train_temporal_contrastive_pretraining(model, x_dict, train_edge_index, train_delta_t, train_burst_score, num_epochs=2)

    # Maintain device placement for x_dict after pretraining
    x_dict = {nt: data[nt].x.to(device) for nt in metadata[0]}

    # Model Training Loop with Mixed Precision & Memory Optimizations
    best_val_loss = float('inf')
    best_val_score = -1e9
    patience = effective_patience
    patience_counter = 0
    best_model_weights = copy.deepcopy(model.state_dict())
    
    # Initialize modern device-aware AMP scaler
    device_type = 'cuda' if torch.cuda.is_available() else 'cpu'
    from contextlib import nullcontext
    if device_type == 'cuda':
        try:
            from torch.amp import autocast as modern_autocast, GradScaler as ModernScaler
            autocast_ctx = modern_autocast(device_type='cuda')
            scaler = ModernScaler('cuda')
        except Exception:
            from torch.cuda.amp import autocast as legacy_autocast, GradScaler as LegacyScaler
            autocast_ctx = legacy_autocast()
            scaler = LegacyScaler()
    else:
        autocast_ctx = nullcontext()
        class DummyScaler:
            def scale(self, l): return l
            def unscale_(self, opt): pass
            def step(self, opt): opt.step()
            def update(self): pass
            def get_scale(self): return 1.0
        scaler = DummyScaler()
    
    # Check memory bounds
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    model.train()
    gnn_pbar = tqdm(range(1, effective_epochs + 1), desc=f"  [Pipeline] [2/5] HT-GNN Epochs", unit="ep", dynamic_ncols=True, leave=False)
    for epoch in gnn_pbar:
        model.train()
        optimizer.zero_grad(set_to_none=True)
        
        # Step curriculum loss (Upgrade F)
        if hasattr(criterion, "step_curriculum"):
            criterion.step_curriculum(epoch, effective_epochs)
        
        with autocast_ctx:
            # EXTRACT EMBEDDINGS FIRST (Latent Manifold-Constrained SMOTE)
            z_dict = model.get_embeddings(x_dict, train_edge_index, train_delta_t, train_burst_score)
            z_target = z_dict[target_node]
            
            # Identify minority train nodes for SMOTE
            valid_train_mask = train_mask_nodes_augmented & (y_target >= 0)
            minority_idx = torch.where(valid_train_mask & (y_target == 1))[0]
            
            synthetic_logits = []
            synthetic_y = []
            # Latent-Space GraphSMOTE Augmentation Engine
            if len(minority_idx) >= 2:
                graph_smote_engine = LatentGraphSMOTE(hidden_dim=effective_hidden, k_neighbors=min(5, len(minority_idx)-1), oversample_ratio=effective_smote_ratio)
                z_target_aug, y_target_aug, _ = graph_smote_engine.synthesize_latent_nodes(
                    z_target[minority_idx], y_target[minority_idx]
                )
                num_syn = z_target_aug.shape[0] - len(minority_idx)
                if num_syn > 0:
                    synthetic_logits = model.out_proj[target_node](z_target_aug[len(minority_idx):])
                    synthetic_y = torch.ones(num_syn, dtype=y_target.dtype, device=y_target.device)
            
            # Normal forward pass for real nodes
            out_dict = {}
            for nt in z_dict:
                if z_dict[nt].shape[0] > 0:
                    out_dict[nt] = model.out_proj[nt](z_dict[nt])
                else:
                    out_dict[nt] = torch.zeros(0, 2, device=z_dict[nt].device)
                    
            logits = out_dict[target_node]
            valid_mask = (y_target >= 0) & train_mask_nodes_augmented
            
            # Stratified Minority Oversampling in GNN Training Batches
            pos_batch_idx = torch.where(valid_mask & (y_target == 1))[0]
            neg_batch_idx = torch.where(valid_mask & (y_target == 0))[0]
            
            if len(pos_batch_idx) >= 2 and len(neg_batch_idx) >= 2:
                # Subsample negatives if pool > 80,000 to keep backward pass ultra fast and VRAM minimal
                if len(neg_batch_idx) > 80_000:
                    sub_neg_perm = torch.randperm(len(neg_batch_idx), device=neg_batch_idx.device)[:80_000]
                    use_neg_idx = neg_batch_idx[sub_neg_perm]
                else:
                    use_neg_idx = neg_batch_idx
                    
                desired_pos = max(len(pos_batch_idx), min(int(effective_smote_ratio * len(use_neg_idx)), 40_000))
                if desired_pos > len(pos_batch_idx):
                    oversample_idx = pos_batch_idx[torch.randint(0, len(pos_batch_idx), (desired_pos - len(pos_batch_idx),), device=pos_batch_idx.device)]
                    batch_idx = torch.cat([pos_batch_idx, oversample_idx, use_neg_idx])
                else:
                    batch_idx = torch.cat([pos_batch_idx, use_neg_idx])
                batch_idx = batch_idx[torch.randperm(len(batch_idx), device=batch_idx.device)]
                logits_valid = logits[batch_idx]
                y_target_valid = y_target[batch_idx]
                z_target_valid = z_target[batch_idx]
            else:
                logits_valid = logits[valid_mask]
                y_target_valid = y_target[valid_mask]
                z_target_valid = z_target[valid_mask]
            
            # Combine real and synthetic for loss calculation
            if len(synthetic_logits) > 0:
                logits_valid = torch.cat([logits_valid, synthetic_logits], dim=0)
                y_target_valid = torch.cat([y_target_valid, synthetic_y], dim=0)
                if 'z_target_aug' in locals() and z_target_aug is not None:
                    z_target_valid = torch.cat([z_target_valid, z_target_aug[len(minority_idx):]], dim=0)
            
            # EWC continual learning parameter penalty
            ewc_penalty = 0.0
            if prev_ewc is not None:
                ewc_penalty = prev_ewc.penalty(model)
                
            if len(y_target_valid) > 0:
                try:
                    loss = criterion(logits_valid, y_target_valid, embeddings=z_target_valid) + ewc_lambda * ewc_penalty
                except TypeError:
                    loss = criterion(logits_valid, y_target_valid) + ewc_lambda * ewc_penalty
            else:
                loss = torch.tensor(ewc_lambda * ewc_penalty, requires_grad=True, device=logits.device)
            
        scaler.scale(loss).backward()
        try:
            scaler.unscale_(optimizer)
        except Exception:
            pass
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()
        
        if torch.cuda.is_available() and num_total_nodes > 1000000:
            torch.cuda.empty_cache()
        
        # Validation monitoring every 2 epochs (Upgrade T)
        if epoch % 2 == 0:
            model.eval()
            with torch.no_grad():
                with autocast_ctx:
                    val_out = model(x_dict, val_edge_index, val_delta_t, val_burst_score)
                    val_logits = val_out[target_node][val_mask_nodes]
                
                val_y = y_target[val_mask_nodes]
                val_valid = val_y >= 0
                if val_valid.sum() > 0:
                    val_loss = F.cross_entropy(val_logits[val_valid].float(), val_y[val_valid]).item()
                    val_probs = F.softmax(val_logits[val_valid].float(), dim=1)[:, 1].cpu().numpy()
                    val_targets = val_y[val_valid].cpu().numpy()
                    
                    if len(np.unique(val_targets)) > 1:
                        from sklearn.metrics import average_precision_score
                        val_prauc = float(average_precision_score(val_targets, val_probs))
                        val_score = val_prauc - 0.1 * val_loss
                    else:
                        val_score = -val_loss
                        
                    if val_score > best_val_score:
                        best_val_score = val_score
                        best_val_loss = val_loss
                        patience_counter = 0
                        best_model_weights = copy.deepcopy(model.state_dict())
                    else:
                        patience_counter += 1
                        if patience_counter >= effective_patience and epoch > min_epochs_early_stop:
                            print(f"  [Early Stopping] Triggered at Epoch {epoch} with Best Val Score {best_val_score:.4f} (Loss: {best_val_loss:.4f})", flush=True)
                            gnn_pbar.close()
                            break
        
        if len(y_target_valid) > 0:
            pred = logits_valid.argmax(dim=1)
            acc = (pred == y_target_valid).float().mean().item()
        else:
            acc = 0.0
        gnn_pbar.set_postfix({"Loss": f"{loss.item():.4f}", "Acc": f"{acc:.4f}", "ValScore": f"{best_val_score:.4f}"})
        
        print_freq = 1 if (num_total_nodes > 1_000_000 or effective_epochs <= 10) else (5 if effective_epochs <= 20 else 10)
        if epoch % print_freq == 0 or epoch == 1 or epoch == effective_epochs:
            print(f"    [Training] Epoch {epoch:2d}/{effective_epochs} | Loss: {loss.item():.4f} | Train Acc: {acc:.4f}", flush=True)

    # Restore best checkpoint
    model.load_state_dict(best_model_weights)

    # Temporal Streaming Evaluation & Standalone Dynamic Threshold Calibration
    model.eval()
    with torch.no_grad():
        with autocast_ctx:
            test_out_dict = model(x_dict, test_edge_index, test_delta_t, test_burst_score)
            val_out_dict = model(x_dict, val_edge_index, val_delta_t, val_burst_score)
            
        logits = test_out_dict[target_node]
        risk_scores = F.softmax(logits, dim=1)[:, 1]
        
        val_logits = val_out_dict[target_node]
        val_probs = F.softmax(val_logits[val_mask_nodes], dim=1)[:, 1].cpu().numpy()
        val_y = y_target[val_mask_nodes]
        val_y_np = val_y.detach().cpu().numpy() if hasattr(val_y, "cpu") else np.asarray(val_y)
        # Dynamic Threshold Calibration for Standalone GNN (Balanced F1-Score & FPR bounded)
        try:
            from .threshold_optimizer import OptimalThresholdCalibrator
            opt_cal = OptimalThresholdCalibrator(target_metric="pareto_95", max_allowed_fpr=0.05)
            optimal_standalone_tau = opt_cal.fit(val_y_np, val_probs)
        except Exception:
            calibrator = DynamicThresholdCalibrator(beta=1.0)
            optimal_standalone_tau = calibrator.calibrate(val_probs, val_y_np)
        
        valid_mask = y_target >= 0
        logits_valid = logits[valid_mask]
        y_target_valid = y_target[valid_mask]
        test_scores = risk_scores[valid_mask].cpu().numpy()
        test_y = y_target_valid.cpu().numpy()
        
        standalone_preds = (test_scores >= optimal_standalone_tau).astype(int)
        test_pos = (test_y == 1)
        test_rec = np.sum((standalone_preds == 1) & test_pos) / max(1, np.sum(test_pos))
        test_prec = np.sum((standalone_preds == 1) & test_pos) / max(1, np.sum(standalone_preds == 1))
        test_f1 = 2 * (test_prec * test_rec) / (test_prec + test_rec + 1e-6)
        
        if len(y_target_valid) > 0:
            preds = logits_valid.argmax(dim=1)
            test_acc = (preds == y_target_valid).float().mean().item()
        else:
            test_acc = 0.0
        
        print(f"  Inference Evaluation:")
        print(f"    Target Node '{target_node}' Accuracy: {test_acc:.4f}")
        print(f"    Standalone GNN Calibrated Metrics (tau* = {optimal_standalone_tau:.3f}):")
        print(f"      Recall: {test_rec*100:.2f}% | Precision: {test_prec*100:.2f}% | F1-Score: {test_f1*100:.2f}%")
        print(f"    Risk Score range: [{risk_scores.min().item():.4f}, {risk_scores.max().item():.4f}]")
        print(f"    Alerts triggered (Risk >= tau*): {(risk_scores >= optimal_standalone_tau).sum().item()}")

    # Save base HGT model weights
    model_dir = Path("data/outputs/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_dir / "htgnn_model.pt")
    print(f"  [Checkpoint] Base GNN weights saved to {model_dir / 'htgnn_model.pt'}")

    # Fit Unified C-STGB Master Algorithm
    print("  [Pipeline] Training Unified C-STGB (Conformal Spatio-Temporal GraphBoost) Classifier...")
    cstgb_model = CSTGBClassifier(model, target_node=target_node, hidden_channels=effective_hidden, alpha=0.10)
    
    # Pass train mask, val mask, and test mask
    eval_test_mask = test_mask_nodes
    
    cstgb_model.fit(
        x_dict, train_edge_index, train_delta_t, train_burst_score,
        y_target, train_mask_nodes_augmented, val_mask=val_mask_nodes, test_mask=eval_test_mask
    )
    cstgb_model.save(model_dir)
    
    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, eval_test_mask)
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cstgb_model, test_probs


def extract_ego_neighborhood_embeddings(embeddings_dict, edge_index_dict, target_node):
    """
    Multi-Moment Higher-Order Subnetwork Ego-Pooling with Cold-Start & Super-Node Protection
    (Memory-Optimized with In-Place Buffers & Active Cache Eviction):
    1. 1st Moment (Mean): Average neighborhood risk
    2. Anomaly Contrast: z_u - mean(N(u))
    3. 2nd Central Moment (Dispersion): std(N(u))
    4. Extreme High-Risk Counterparty (Max Pool): max(N(u))
    5. Baseline Counterparty (Min Pool): min(N(u))
    6. 95th Percentile Counterparty (p95 Pool): Protects super-nodes from variance dilution
    7. Cold-Start Prior Indicator: Binary flag + Global Centroid substitution when d_u == 0
    """
    import gc
    z_target = embeddings_dict[target_node]
    num_nodes, emb_dim = z_target.shape
    device = z_target.device
    
    neighbor_sum = torch.zeros((num_nodes, emb_dim), dtype=torch.float32, device=device)
    neighbor_sq_sum = torch.zeros((num_nodes, emb_dim), dtype=torch.float32, device=device)
    neighbor_max = torch.full((num_nodes, emb_dim), -float('inf'), dtype=torch.float32, device=device)
    neighbor_min = torch.full((num_nodes, emb_dim), float('inf'), dtype=torch.float32, device=device)
    neighbor_counts = torch.zeros(num_nodes, dtype=torch.float32, device=device)
    
    for rel, edge_index in edge_index_dict.items():
        if edge_index is None or edge_index.numel() == 0:
            continue
        src_type, _, dst_type = rel
        src_emb = embeddings_dict[src_type]
        dst_emb = embeddings_dict[dst_type]
        
        if src_type == target_node and edge_index.shape[1] > 0:
            src_idx = edge_index[0]
            dst_idx = edge_index[1]
            valid = src_idx < num_nodes
            s_val = src_idx[valid]
            d_emb = dst_emb[dst_idx[valid]]
            
            neighbor_sum.index_add_(0, s_val, d_emb)
            neighbor_sq_sum.index_add_(0, s_val, d_emb ** 2)
            neighbor_counts.index_add_(0, s_val, torch.ones_like(s_val, dtype=torch.float32))
            neighbor_max.scatter_reduce_(0, s_val.unsqueeze(-1).expand_as(d_emb), d_emb, reduce='amax', include_self=True)
            neighbor_min.scatter_reduce_(0, s_val.unsqueeze(-1).expand_as(d_emb), d_emb, reduce='amin', include_self=True)
            
        if dst_type == target_node and edge_index.shape[1] > 0:
            src_idx = edge_index[0]
            dst_idx = edge_index[1]
            valid = dst_idx < num_nodes
            d_val = dst_idx[valid]
            s_emb = src_emb[src_idx[valid]]
            
            neighbor_sum.index_add_(0, d_val, s_emb)
            neighbor_sq_sum.index_add_(0, d_val, s_emb ** 2)
            neighbor_counts.index_add_(0, d_val, torch.ones_like(d_val, dtype=torch.float32))
            neighbor_max.scatter_reduce_(0, d_val.unsqueeze(-1).expand_as(s_emb), s_emb, reduce='amax', include_self=True)
            neighbor_min.scatter_reduce_(0, d_val.unsqueeze(-1).expand_as(s_emb), s_emb, reduce='amin', include_self=True)
            
    has_neighbors = neighbor_counts > 0
    cold_start_flag = np.ascontiguousarray((~has_neighbors).float().unsqueeze(-1).cpu().numpy(), dtype=np.float32)
    
    # Global Population Centroid for Cold-Start Prior Fallback
    global_centroid = z_target.mean(dim=0, keepdim=True)
    
    ego_mean = z_target.clone()
    ego_mean[has_neighbors] = neighbor_sum[has_neighbors] / neighbor_counts[has_neighbors].unsqueeze(-1)
    ego_mean[~has_neighbors] = global_centroid.expand((~has_neighbors).sum(), emb_dim)
    
    ego_contrast = z_target - ego_mean
    
    # 2nd Central Moment (Dispersion)
    ego_std = torch.zeros_like(z_target)
    mean_sq = ego_mean[has_neighbors] ** 2
    sq_mean = neighbor_sq_sum[has_neighbors] / neighbor_counts[has_neighbors].unsqueeze(-1)
    ego_std[has_neighbors] = torch.sqrt(torch.clamp(sq_mean - mean_sq, min=0.0) + 1e-6)
    
    # Release square sum buffer immediately
    del neighbor_sq_sum
    
    # Max and Min Counterparty embeddings
    ego_max = z_target.clone()
    ego_max[has_neighbors] = neighbor_max[has_neighbors]
    ego_min = z_target.clone()
    ego_min[has_neighbors] = neighbor_min[has_neighbors]
    
    # Release min/max accumulation buffers
    del neighbor_sum, neighbor_max, neighbor_min, neighbor_counts
    
    # Exact Asymptotic 95th Percentile Quantile Estimator (Gaussian/GEV quantile)
    # q_0.95 = mu + 1.64485 * sigma
    ego_p95 = ego_mean + 1.64485 * ego_std
    
    # Convert to contiguous float32 numpy arrays and release PyTorch GPU/CPU memory
    out_mean = np.ascontiguousarray(ego_mean.detach().cpu().numpy(), dtype=np.float32)
    out_contrast = np.ascontiguousarray(ego_contrast.detach().cpu().numpy(), dtype=np.float32)
    out_std = np.ascontiguousarray(ego_std.detach().cpu().numpy(), dtype=np.float32)
    out_max = np.ascontiguousarray(ego_max.detach().cpu().numpy(), dtype=np.float32)
    out_min = np.ascontiguousarray(ego_min.detach().cpu().numpy(), dtype=np.float32)
    out_p95 = np.ascontiguousarray(ego_p95.detach().cpu().numpy(), dtype=np.float32)
    
    del ego_mean, ego_contrast, ego_std, ego_max, ego_min, ego_p95
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return (
        out_mean,
        out_contrast,
        out_std,
        out_max,
        out_min,
        out_p95,
        cold_start_flag
    )


