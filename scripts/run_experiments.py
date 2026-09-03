"""
Phase 2 Experiments: Proposed C-STGB vs. Literature & Graph Baselines.
Evaluates:
1. Tabular Baseline: XGBoost Classifier
2. Topological Baseline: Network Features + Logistic Regression
3. Homogeneous GCN Baseline: Kipf & Welling (2017) / Weber et al. (2019)
4. GraphSAGE Baseline: Hamilton et al. (2017) Inductive Graph Convolution
5. Graph Attention Network (GAT) Baseline: Velickovic et al. (2018)
6. Graph Isomorphism Network (GIN) Baseline: Xu et al. (2019) / Custom Edge GIN (2025)
7. EvolveGCN Baseline: Pareja et al. (2020) Dynamic Recurrent Graph Network
8. Spatiotemporal GCN-GRU Baseline: Chronological Feature Sequence Model
9. PROPOSED: C-STGB (Conformal Spatio-Temporal GraphBoost Classifier)
"""

import os
import sys
import time
import json
import tracemalloc
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.models.htgnn import build_hetero_data, BurstAwareHGT, train_htgnn, CSTGBClassifier
from src.utils.conformal import ConformalFilter

from sklearn.metrics import f1_score, precision_score, recall_score, precision_recall_curve, auc, fbeta_score, roc_curve
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


class HomogeneousGCN(nn.Module):
    """3-layer Homogeneous GCN Conv baseline from Weber et al. (2019)."""
    def __init__(self, in_channels, hidden_channels, out_channels=2, num_layers=3):
        super().__init__()
        from torch_geometric.nn import GCNConv
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(in_channels, hidden_channels))
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
        self.convs.append(GCNConv(hidden_channels, out_channels))
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        return self.convs[-1](x, edge_index)


class GraphSAGEBaseline(nn.Module):
    """3-layer Inductive GraphSAGE baseline from Hamilton et al. (2017)."""
    def __init__(self, in_channels, hidden_channels, out_channels=2, num_layers=3):
        super().__init__()
        from torch_geometric.nn import SAGEConv
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_channels, hidden_channels, aggr="mean"))
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_channels, hidden_channels, aggr="mean"))
        self.convs.append(SAGEConv(hidden_channels, out_channels, aggr="mean"))
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        return self.convs[-1](x, edge_index)


class GINBaseline(nn.Module):
    """3-layer Graph Isomorphism Network (GIN) from Xu et al. (2019) / Custom Edge GIN (2025)."""
    def __init__(self, in_channels, hidden_channels, out_channels=2):
        super().__init__()
        from torch_geometric.nn import GINConv
        mlp1 = nn.Sequential(
            nn.Linear(in_channels, hidden_channels),
            nn.BatchNorm1d(hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        mlp2 = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.BatchNorm1d(hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        self.conv1 = GINConv(mlp1, train_eps=True)
        self.conv2 = GINConv(mlp2, train_eps=True)
        self.out_proj = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index):
        h = F.relu(self.conv1(x, edge_index))
        h = self.dropout(h)
        h = F.relu(self.conv2(h, edge_index))
        h = self.dropout(h)
        return self.out_proj(h)


class EvolveGCNBaseline(nn.Module):
    """EvolveGCN Dynamic Graph baseline from Pareja et al. (2020)."""
    def __init__(self, in_channels, hidden_channels, out_channels=2):
        super().__init__()
        from torch_geometric.nn import GCNConv
        self.gcn1 = GCNConv(in_channels, hidden_channels)
        self.gcn2 = GCNConv(hidden_channels, hidden_channels)
        self.gru = nn.GRUCell(hidden_channels, hidden_channels)
        self.out_proj = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index, h_prev=None):
        h = F.relu(self.gcn1(x, edge_index))
        h = self.dropout(h)
        h = F.relu(self.gcn2(h, edge_index))
        if h_prev is not None:
            h = self.gru(h, h_prev)
        return self.out_proj(h), h


class GCNGRUBaseline(nn.Module):
    """Spatiotemporal GCN-GRU Sequence baseline."""
    def __init__(self, in_channels, hidden_channels, out_channels=2):
        super().__init__()
        from torch_geometric.nn import GCNConv
        self.spatial_encoder = GCNConv(in_channels, hidden_channels)
        self.temporal_proj = nn.Linear(2, hidden_channels) # delta_t + burst_score
        self.gru_cell = nn.GRUCell(hidden_channels, hidden_channels)
        self.classifier = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x, edge_index, delta_t, burst_score):
        h_spatial = F.relu(self.spatial_encoder(x, edge_index))
        h_spatial = self.dropout(h_spatial)
        
        # Combine temporal embeddings
        t_feats = torch.stack([delta_t, burst_score], dim=-1)
        h_temporal = F.relu(self.temporal_proj(t_feats))
        
        h_fused = self.gru_cell(h_spatial, h_temporal)
        out = self.classifier(h_fused)
        return out


def evaluate_metrics(y_true, y_probs, threshold=0.70):
    """Computes comprehensive evaluation metrics under class imbalance."""
    valid_mask = y_true >= 0
    y_true_clean = y_true[valid_mask]
    y_probs_clean = y_probs[valid_mask]
    
    if len(y_true_clean) == 0 or len(np.unique(y_true_clean)) < 2:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "f2_score": 0.0,
            "pr_auc": 0.0,
            "tpr_at_01fpr": 0.0
        }
        
    y_pred = (y_probs_clean >= threshold).astype(int)
    
    acc = (y_pred == y_true_clean).mean()
    prec = precision_score(y_true_clean, y_pred, zero_division=0)
    rec = recall_score(y_true_clean, y_pred, zero_division=0)
    f1 = f1_score(y_true_clean, y_pred, zero_division=0)
    f2 = fbeta_score(y_true_clean, y_pred, beta=2.0, zero_division=0)
    
    # PR-AUC
    precision_curve, recall_curve, _ = precision_recall_curve(y_true_clean, y_probs_clean)
    pr_auc = auc(recall_curve, precision_curve)
    
    # TPR at 0.1% (0.001) False Positive Rate
    fpr, tpr, _ = roc_curve(y_true_clean, y_probs_clean)
    target_fpr = 0.001
    idx = np.where(fpr <= target_fpr)[0]
    tpr_at_01fpr = tpr[idx[-1]] if len(idx) > 0 else 0.0
    
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "f2_score": f2,
        "pr_auc": pr_auc,
        "tpr_at_01fpr": tpr_at_01fpr
    }


def to_homogeneous_projection(data):
    """Projects HeteroData to a single homogeneous tensor representation."""
    metadata = data.metadata()
    node_types = metadata[0]
    
    node_offsets = {}
    total_nodes = 0
    feature_list = []
    
    for nt in node_types:
        x = data[nt].x
        node_offsets[nt] = total_nodes
        total_nodes += x.shape[0]
        feature_list.append(x)
        
    max_dim = max(x.shape[1] for x in feature_list)
    padded_features = []
    for x in feature_list:
        if x.shape[1] < max_dim:
            pad = torch.zeros(x.shape[0], max_dim - x.shape[1], device=x.device)
            padded_features.append(torch.cat([x, pad], dim=1))
        else:
            padded_features.append(x)
            
    x_homo = torch.cat(padded_features, dim=0)
    
    edge_index_list = []
    for relation in metadata[1]:
        if relation in data:
            src_type, _, dst_type = relation
            edges = data[relation].edge_index.clone()
            edges[0] += node_offsets[src_type]
            edges[1] += node_offsets[dst_type]
            edge_index_list.append(edges)
            
    if edge_index_list:
        edge_index_homo = torch.cat(edge_index_list, dim=1)
    else:
        edge_index_homo = torch.zeros((2, 0), dtype=torch.long)
        
    return x_homo, edge_index_homo, node_offsets


def resolve_target_node(data):
    """Identifies the node type containing supervision labels and valid nodes."""
    for nt in data.node_types:
        if hasattr(data[nt], "y") and data[nt].y is not None and data[nt].y.numel() > 0:
            if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
                return nt
    for nt in data.node_types:
        if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
            return nt
    return data.node_types[0]


def extract_topological_features(data, target_node="Account"):
    """Extracts degree and edge weight summaries for classical baseline models."""
    x = data[target_node].x
    num_nodes = x.shape[0]
    
    in_degree = torch.zeros(num_nodes, device=x.device)
    out_degree = torch.zeros(num_nodes, device=x.device)
    
    for rel in data.metadata()[1]:
        src_type, et, dst_type = rel
        if rel in data:
            edge_index = data[rel].edge_index
            if src_type == target_node:
                out_degree += torch.bincount(edge_index[0], minlength=num_nodes).float()
            if dst_type == target_node:
                in_degree += torch.bincount(edge_index[1], minlength=num_nodes).float()
                
    in_degree = in_degree.unsqueeze(-1)
    out_degree = out_degree.unsqueeze(-1)
    
    return torch.cat([x, in_degree, out_degree], dim=-1)


def compute_node_temporal_features(data, target_offset, num_target_nodes):
    """Aggregates edge delta_t and burst_score to node level."""
    target_node = resolve_target_node(data)
    node_delta_t = torch.zeros(num_target_nodes, device=data[target_node].x.device)
    node_burst_score = torch.zeros(num_target_nodes, device=data[target_node].x.device)
    node_counts = torch.zeros(num_target_nodes, device=data[target_node].x.device)
    
    for rel in data.metadata()[1]:
        src_type, _, dst_type = rel
        if rel in data and hasattr(data[rel], "delta_t"):
            edge_index = data[rel].edge_index
            delta_t = data[rel].delta_t
            burst_score = data[rel].burst_score
            
            if dst_type == target_node and edge_index.shape[1] > 0:
                dst_idx = edge_index[1]
                valid_mask = dst_idx < num_target_nodes
                dst_valid = dst_idx[valid_mask]
                
                node_delta_t.index_add_(0, dst_valid, delta_t[valid_mask])
                node_burst_score.index_add_(0, dst_valid, burst_score[valid_mask])
                node_counts.index_add_(0, dst_valid, torch.ones_like(dst_valid, dtype=torch.float))
                
    mask = node_counts > 0
    node_delta_t[mask] /= node_counts[mask]
    node_burst_score[mask] /= node_counts[mask]
    return node_delta_t, node_burst_score


def train_and_profile_cstgb(data, dataset_name="elliptic_v1", num_epochs=30):
    """Trains and profiles the proposed unified C-STGB master algorithm."""
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    num_target_nodes_orig = len(y_target)
    train_split_idx = int(num_target_nodes_orig * 0.7)
    
    tracemalloc.start()
    t0 = time.perf_counter()
    
    cstgb_model, _ = train_htgnn(dataset_name, num_epochs=num_epochs)
    
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    metadata = data.metadata()
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    for rel in metadata[1]:
        if rel in data:
            delta_t = data[rel].delta_t
            test_mask_edges = delta_t > ts_threshold
            test_edge_index[rel] = data[rel].edge_index[:, test_mask_edges]
            test_delta_t[rel] = delta_t[test_mask_edges]
            test_burst_score[rel] = data[rel].burst_score[test_mask_edges]
            
    x_dict = {nt: data[nt].x for nt in metadata[0]}
    test_node_mask = torch.zeros(data[target_node].x.shape[0], dtype=torch.bool)
    test_node_mask[train_split_idx:num_target_nodes_orig] = True
    
    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, test_node_mask)
    y_test = y_target[train_split_idx:num_target_nodes_orig]
    
    metrics = evaluate_metrics(y_test, test_probs, threshold=cstgb_model.optimal_threshold)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    
    return metrics, cstgb_model, y_test, test_probs


def train_and_profile_gat(data, num_epochs=30):
    """Standard GAT Baseline from Veličković et al. (2018)."""
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y
    in_channels_dict = {nt: data[nt].x.shape[1] for nt in metadata[0]}
    
    model = BurstAwareHGT(
        in_channels_dict=in_channels_dict,
        hidden_channels=128,
        num_layers=3,
        metadata=metadata,
        lambda_decay=0.0, # no temporal decay (standard GAT)
        beta_scale=0.0
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    train_edge_index, train_delta_t, train_burst_score = {}, {}, {}
    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    
    for rel in metadata[1]:
        if rel in data:
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            test_mask = ~train_mask
            
            train_edge_index[rel] = data[rel].edge_index[:, train_mask]
            train_delta_t[rel] = delta_t[train_mask]
            train_burst_score[rel] = data[rel].burst_score[train_mask]
            
            test_edge_index[rel] = data[rel].edge_index[:, test_mask]
            test_delta_t[rel] = delta_t[test_mask]
            test_burst_score[rel] = data[rel].burst_score[test_mask]
            
    x_dict = {nt: data[nt].x for nt in metadata[0]}
    
    tracemalloc.start()
    t0 = time.perf_counter()
    
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out_dict = model(x_dict, train_edge_index, train_delta_t, train_burst_score)
        logits = out_dict[target_node]
        valid_mask = y_target >= 0
        loss = criterion(logits[valid_mask], y_target[valid_mask])
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out_dict = model(x_dict, test_edge_index, test_delta_t, test_burst_score)
        logits = out_dict[target_node]
        probs = F.softmax(logits, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target.cpu().numpy(), probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_gcn(data, num_epochs=30):
    """Homogeneous GCN Baseline from Weber et al. (2019)."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    valid_edge_indices = []
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index.clone()
            edge_index[0] += offset_dict[rel[0]]
            edge_index[1] += offset_dict[rel[2]]
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            valid_edge_indices.append(edge_index[:, train_mask])
            
    train_edge_index = torch.cat(valid_edge_indices, dim=1) if valid_edge_indices else torch.zeros((2, 0), dtype=torch.long)
    model = HomogeneousGCN(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out = model(x_homo, train_edge_index)
        target_out = out[target_offset : target_offset + len(y_target)]
        train_mask = y_target >= 0
        loss = criterion(target_out[train_mask], torch.tensor(y_target[train_mask], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out = model(x_homo, edge_index_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target, probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_sage(data, num_epochs=30):
    """GraphSAGE Baseline from Hamilton et al. (2017)."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    valid_edge_indices = []
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index.clone()
            edge_index[0] += offset_dict[rel[0]]
            edge_index[1] += offset_dict[rel[2]]
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            valid_edge_indices.append(edge_index[:, train_mask])
            
    train_edge_index = torch.cat(valid_edge_indices, dim=1) if valid_edge_indices else torch.zeros((2, 0), dtype=torch.long)
    model = GraphSAGEBaseline(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out = model(x_homo, train_edge_index)
        target_out = out[target_offset : target_offset + len(y_target)]
        train_mask = y_target >= 0
        loss = criterion(target_out[train_mask], torch.tensor(y_target[train_mask], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out = model(x_homo, edge_index_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target, probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_gin(data, num_epochs=30):
    """Graph Isomorphism Network (GIN) from Xu et al. (2019) / Custom Edge GIN (2025)."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    valid_edge_indices = []
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index.clone()
            edge_index[0] += offset_dict[rel[0]]
            edge_index[1] += offset_dict[rel[2]]
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            valid_edge_indices.append(edge_index[:, train_mask])
            
    train_edge_index = torch.cat(valid_edge_indices, dim=1) if valid_edge_indices else torch.zeros((2, 0), dtype=torch.long)
    model = GINBaseline(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out = model(x_homo, train_edge_index)
        target_out = out[target_offset : target_offset + len(y_target)]
        train_mask = y_target >= 0
        loss = criterion(target_out[train_mask], torch.tensor(y_target[train_mask], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out = model(x_homo, edge_index_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target, probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_evolvegcn(data, num_epochs=30):
    """EvolveGCN Dynamic Graph baseline from Pareja et al. (2020)."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    valid_edge_indices = []
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index.clone()
            edge_index[0] += offset_dict[rel[0]]
            edge_index[1] += offset_dict[rel[2]]
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            valid_edge_indices.append(edge_index[:, train_mask])
            
    train_edge_index = torch.cat(valid_edge_indices, dim=1) if valid_edge_indices else torch.zeros((2, 0), dtype=torch.long)
    model = EvolveGCNBaseline(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    h_prev = None
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out, h_prev = model(x_homo, train_edge_index, h_prev.detach() if h_prev is not None else None)
        target_out = out[target_offset : target_offset + len(y_target)]
        train_mask = y_target >= 0
        loss = criterion(target_out[train_mask], torch.tensor(y_target[train_mask], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out, _ = model(x_homo, edge_index_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target, probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_gcngru(data, num_epochs=30):
    """Spatiotemporal GCN-GRU Sequence baseline."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    # Compute node level temporal features
    node_delta_t, node_burst_score = compute_node_temporal_features(data, target_offset, len(y_target))
    
    node_delta_t_homo = torch.zeros(x_homo.shape[0], device=x_homo.device)
    node_burst_score_homo = torch.zeros(x_homo.shape[0], device=x_homo.device)
    node_delta_t_homo[target_offset : target_offset + len(y_target)] = node_delta_t
    node_burst_score_homo[target_offset : target_offset + len(y_target)] = node_burst_score
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, 70) if all_ts else 0.0

    valid_edge_indices = []
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index.clone()
            edge_index[0] += offset_dict[rel[0]]
            edge_index[1] += offset_dict[rel[2]]
            delta_t = data[rel].delta_t
            train_mask = delta_t <= ts_threshold
            valid_edge_indices.append(edge_index[:, train_mask])
            
    train_edge_index = torch.cat(valid_edge_indices, dim=1) if valid_edge_indices else torch.zeros((2, 0), dtype=torch.long)
    model = GCNGRUBaseline(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out = model(x_homo, train_edge_index, node_delta_t_homo, node_burst_score_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        train_mask = y_target >= 0
        loss = criterion(target_out[train_mask], torch.tensor(y_target[train_mask], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out = model(x_homo, edge_index_homo, node_delta_t_homo, node_burst_score_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    metrics = evaluate_metrics(y_target, probs, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def train_and_profile_tabular(model_type, data):
    """Trains and profiles tabular and network feature baselines."""
    metadata = data.metadata()
    target_node = resolve_target_node(data)
    y = data[target_node].y.cpu().numpy()
    
    if model_type == "xgb":
        x = data[target_node].x.cpu().numpy()
    else:
        x = extract_topological_features(data, target_node).cpu().numpy()
        
    split_idx = int(len(x) * 0.7)
    x_train, x_test = x[:split_idx], x[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    train_mask = y_train >= 0
    test_mask = y_test >= 0
    
    x_train_l, y_train_l = x_train[train_mask], y_train[train_mask]
    x_test_l, y_test_l = x_test[test_mask], y_test[test_mask]
    
    tracemalloc.start()
    t0 = time.perf_counter()
    
    if model_type == "xgb":
        model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.08, random_state=42, n_jobs=-1)
        model.fit(x_train_l, y_train_l)
        probs = model.predict_proba(x_test_l)[:, 1]
    else:
        model = LogisticRegression(max_iter=200, random_state=42)
        model.fit(x_train_l, y_train_l)
        probs = model.predict_proba(x_test_l)[:, 1]
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    y_test_full = np.ones(len(y_test)) * -1
    y_test_full[test_mask] = y_test_l
    probs_full = np.zeros(len(y_test))
    probs_full[test_mask] = probs
    
    metrics = evaluate_metrics(y_test_full, probs_full, threshold=0.70)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics


def run_experiments():
    print("=" * 80)
    print(" Running Phase 2 Multi-Baseline Literature Benchmarking Suite")
    print("=" * 80)
    
    dataset_name = "elliptic_v1"
    print(f"Loading preprocessed dataset: {dataset_name} ...")
    data = build_hetero_data(dataset_name)
    
    # 1. Train Proposed Master Algorithm: C-STGB
    print("\n[1/9] Training Proposed Master Algorithm: C-STGB (Conformal Spatio-Temporal GraphBoost)...")
    cstgb, cstgb_model, y_test, cstgb_probs = train_and_profile_cstgb(data, num_epochs=30)
    
    # 2. Train Tabular XGBoost
    print("\n[2/9] Training Tabular Baseline (XGBoost)...")
    xgb = train_and_profile_tabular("xgb", data)
    
    # 3. Train Topological Logistic Regression
    print("\n[3/9] Training Topological Baseline (Network Features + Logistic Regression)...")
    topo_lr = train_and_profile_tabular("topo_lr", data)
    
    # 4. Train Homogeneous GCN Baseline (Weber et al. 2019)
    print("\n[4/9] Training Homogeneous GCN Baseline (Weber et al. 2019)...")
    gcn = train_and_profile_gcn(data)
    
    # 5. Train GraphSAGE Baseline (Hamilton et al. 2017)
    print("\n[5/9] Training GraphSAGE Baseline (Hamilton et al. 2017)...")
    sage = train_and_profile_sage(data)
    
    # 6. Train Standard GAT Baseline (Velickovic et al. 2018)
    print("\n[6/9] Training Standard GAT Baseline (Velickovic et al. 2018)...")
    gat = train_and_profile_gat(data)
    
    # 7. Train GIN Baseline (Xu et al. 2019 / Custom Edge GIN 2025)
    print("\n[7/9] Training GIN Baseline (Xu et al. 2019 / Edge GIN 2025)...")
    gin = train_and_profile_gin(data)
    
    # 8. Train EvolveGCN Baseline (Pareja et al. 2020)
    print("\n[8/9] Training EvolveGCN Dynamic Graph Baseline (Pareja et al. 2020)...")
    evolvegcn = train_and_profile_evolvegcn(data)
    
    # 9. Train GCN-GRU Spatiotemporal Sequence Baseline
    print("\n[9/9] Training GCN-GRU Spatiotemporal Sequence Baseline...")
    gcngru = train_and_profile_gcngru(data)
    
    # Evaluate Conformal Prediction Filter on C-STGB
    conformal = cstgb_model.conformal if cstgb_model.conformal is not None else ConformalFilter(alpha=0.10)
    n_cal = min(10000, len(y_test) // 3)
    test_probs_subset = cstgb_probs[n_cal:]
    
    if conformal.q is None:
        conformal.calibrate(cstgb_probs[:n_cal], y_test[:n_cal])
        
    prediction_sets = conformal.predict_set(test_probs_subset)
    total_test = len(prediction_sets)
    confident_licit = np.sum(prediction_sets == 0)
    confident_fraud = np.sum(prediction_sets == 1)
    uncertain_review = np.sum(prediction_sets == 2)
    
    # Save output report to artifacts
    report_content = f"""# System-Wide Comparative Benchmark Report: Proposed C-STGB vs. Literature Baselines

Evaluated on the **Elliptic v1** cryptocurrency transaction benchmark ($N = 203,769$ nodes, $E = 234,355$ edges) across a chronological temporal split (70% Historical Train, 30% Streaming Test) under **Calibrated Thresholding ($\\tau^* = {cstgb_model.optimal_threshold:.2f}$ for C-STGB, $\\tau = 0.70$ for Baselines)**.

---

## 1. Comprehensive Performance Comparison Matrix

| Evaluation Metric | Tabular (XGB) | Network + LR | Homogeneous GCN | GraphSAGE | Standard GAT | GIN (2019/2025) | EvolveGCN (2020) | GCN-GRU (2025) | **PROPOSED C-STGB** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Accuracy** | {xgb['accuracy']:.4f} | {topo_lr['accuracy']:.4f} | {gcn['accuracy']:.4f} | {sage['accuracy']:.4f} | {gat['accuracy']:.4f} | {gin['accuracy']:.4f} | {evolvegcn['accuracy']:.4f} | {gcngru['accuracy']:.4f} | **{cstgb['accuracy']:.4f}** |
| **Precision** | {xgb['precision']:.4f} | {topo_lr['precision']:.4f} | {gcn['precision']:.4f} | {sage['precision']:.4f} | {gat['precision']:.4f} | {gin['precision']:.4f} | {evolvegcn['precision']:.4f} | {gcngru['precision']:.4f} | **{cstgb['precision']:.4f}** |
| **Recall (Catch Rate)** | {xgb['recall']:.4f} | {topo_lr['recall']:.4f} | {gcn['recall']:.4f} | {sage['recall']:.4f} | {gat['recall']:.4f} | {gin['recall']:.4f} | {evolvegcn['recall']:.4f} | {gcngru['recall']:.4f} | **{cstgb['recall']:.4f}** |
| **F1-Score** | {xgb['f1_score']:.4f} | {topo_lr['f1_score']:.4f} | {gcn['f1_score']:.4f} | {sage['f1_score']:.4f} | {gat['f1_score']:.4f} | {gin['f1_score']:.4f} | {evolvegcn['f1_score']:.4f} | {gcngru['f1_score']:.4f} | **{cstgb['f1_score']:.4f}** |
| **F2-Score (Recall Focus)** | {xgb['f2_score']:.4f} | {topo_lr['f2_score']:.4f} | {gcn['f2_score']:.4f} | {sage['f2_score']:.4f} | {gat['f2_score']:.4f} | {gin['f2_score']:.4f} | {evolvegcn['f2_score']:.4f} | {gcngru['f2_score']:.4f} | **{cstgb['f2_score']:.4f}** |
| **PR-AUC** | {xgb['pr_auc']:.4f} | {topo_lr['pr_auc']:.4f} | {gcn['pr_auc']:.4f} | {sage['pr_auc']:.4f} | {gat['pr_auc']:.4f} | {gin['pr_auc']:.4f} | {evolvegcn['pr_auc']:.4f} | {gcngru['pr_auc']:.4f} | **{cstgb['pr_auc']:.4f}** |
| **TPR @ 0.1% FPR** | {xgb['tpr_at_01fpr']:.4f} | {topo_lr['tpr_at_01fpr']:.4f} | {gcn['tpr_at_01fpr']:.4f} | {sage['tpr_at_01fpr']:.4f} | {gat['tpr_at_01fpr']:.4f} | {gin['tpr_at_01fpr']:.4f} | {evolvegcn['tpr_at_01fpr']:.4f} | {gcngru['tpr_at_01fpr']:.4f} | **{cstgb['tpr_at_01fpr']:.4f}** |

---

## 2. Computational Efficiency & Overhead

| Efficiency Metric | Tabular (XGB) | Network + LR | Homogeneous GCN | GraphSAGE | Standard GAT | GIN | EvolveGCN | GCN-GRU | **PROPOSED C-STGB** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Training Duration** | {xgb['training_time_sec']:.2f} s | {topo_lr['training_time_sec']:.2f} s | {gcn['training_time_sec']:.2f} s | {sage['training_time_sec']:.2f} s | {gat['training_time_sec']:.2f} s | {gin['training_time_sec']:.2f} s | {evolvegcn['training_time_sec']:.2f} s | {gcngru['training_time_sec']:.2f} s | **{cstgb['training_time_sec']:.2f} s** |
| **Peak RAM Allocation** | {xgb['peak_memory_mb']:.2f} MB | {topo_lr['peak_memory_mb']:.2f} MB | {gcn['peak_memory_mb']:.2f} MB | {sage['peak_memory_mb']:.2f} MB | {gat['peak_memory_mb']:.2f} MB | {gin['peak_memory_mb']:.2f} MB | {evolvegcn['peak_memory_mb']:.2f} MB | {gcngru['peak_memory_mb']:.2f} MB | **{cstgb['peak_memory_mb']:.2f} MB** |

---

## 3. Conformal Risk Gate Performance (Confidence Level: {1.0 - conformal.alpha:.0%})

Inductive Conformal Prediction (ICP) filters borderline predictions, producing mathematically guaranteed prediction sets:

| Queue Category | Set Size | Percentage of Total Volume | Compliance Action |
| :--- | :---: | :---: | :--- |
| **Confident Licit** ($C = \\{{0\\}}$) | {confident_licit:,} | {confident_licit/total_test:.2%} | **Auto-Approve** (Instantly bypass gateway) |
| **Confident Fraud** ($C = \\{{1\\}}$) | {confident_fraud:,} | {confident_fraud/total_test:.2%} | **Auto-Flag Alert** (Submit SAR immediately) |
| **Uncertain / Review** ($C = \\{{0, 1\\}}$) | {uncertain_review:,} | {uncertain_review/total_test:.2%} | **Route to Compliance Queue** (Enhanced Due Diligence) |
"""
    
    artifact_dir = Path("C:/Users/Nazmul Hasan Nihal/.gemini/antigravity-ide/brain/f0dd4eb5-aa65-4ac1-8be9-be8776a6c3a7")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "comparative_metrics_report.md").write_text(report_content, encoding="utf-8")
    
    # Terminal Display
    print("\n" + "=" * 165)
    print(" SYSTEM-WIDE COMPARATIVE BENCHMARK REPORT: PROPOSED C-STGB vs. LITERATURE BASELINES (Threshold: 0.70)")
    print("=" * 165)
    header = f"{'Metric':<20} | {'Tabular (XGB)':<13} | {'Network + LR':<13} | {'Homo GCN':<13} | {'GraphSAGE':<13} | {'Base (GAT)':<13} | {'GIN (2025)':<13} | {'EvolveGCN':<13} | {'GCN-GRU':<13} | {'PROPOSED C-STGB':<17}"
    print(header)
    print("-" * 165)
    for k in ["accuracy", "precision", "recall", "f1_score", "f2_score", "pr_auc", "tpr_at_01fpr"]:
        print(f"{k.replace('_', ' ').capitalize():<20} | "
              f"{xgb[k]:13.4f} | "
              f"{topo_lr[k]:13.4f} | "
              f"{gcn[k]:13.4f} | "
              f"{sage[k]:13.4f} | "
              f"{gat[k]:13.4f} | "
              f"{gin[k]:13.4f} | "
              f"{evolvegcn[k]:13.4f} | "
              f"{gcngru[k]:13.4f} | "
              f"{cstgb[k]:17.4f}")
    print("-" * 165)
    print(f"[Conformal Risk Statistics (Total: {total_test:,} transactions)]")
    print(f"  Auto-Approve Rate (Confident Licit):    {confident_licit/total_test:.2%}")
    print(f"  Auto-Flag Alert Rate (Confident Fraud): {confident_fraud/total_test:.2%}")
    print(f"  Compliance Audit Queue Load:            {uncertain_review/total_test:.2%}")
    print("=" * 165)


if __name__ == "__main__":
    run_experiments()
