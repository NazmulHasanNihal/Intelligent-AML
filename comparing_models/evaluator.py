"""
Evaluation Suite & Graph Projection Utilities for AML Model Comparison.
"""

import time
import tracemalloc
import numpy as np
import torch
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    precision_recall_curve, roc_curve, auc, fbeta_score, roc_auc_score
)


def evaluate_model_performance(y_true, y_probs, threshold=None):
    """Computes comprehensive evaluation metrics under class imbalance with adaptive threshold support."""
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
            "auc_pr": 0.0,
            "roc_auc": 0.0,
            "auc_roc": 0.0,
            "tpr_at_01fpr": 0.0,
            "optimal_threshold": 0.50
        }
        
    # Auto-calibrate optimal decision threshold if not explicitly specified
    if threshold is None or str(threshold).lower() in ("auto", "youden", "youden_j", "f1"):
        criterion = str(threshold).lower() if threshold is not None else "f1"
        best_score = -1e9
        best_tau = 0.50
        # Multi-resolution candidate search from 0.005 to 0.98 for extreme class imbalance (IBM AMLSim, PaySim)
        candidates = np.unique(np.concatenate([
            np.logspace(np.log10(0.005), np.log10(0.20), 50),
            np.linspace(0.20, 0.98, 50)
        ]))
        
        pos_mask = (y_true_clean == 1)
        neg_mask = (y_true_clean == 0)
        total_pos = float(pos_mask.sum())
        total_neg = float(neg_mask.sum())
        
        for tau in candidates:
            preds = (y_probs_clean >= tau).astype(int)
            if criterion in ("youden", "youden_j"):
                tp = float(preds[pos_mask].sum())
                fp = float(preds[neg_mask].sum())
                sens = tp / max(1.0, total_pos)
                spec = (total_neg - fp) / max(1.0, total_neg)
                score = sens + spec - 1.0
            else:
                score = f1_score(y_true_clean, preds, zero_division=0)
                
            if score > best_score:
                best_score = score
                best_tau = float(tau)
        threshold = best_tau
        
    y_pred = (y_probs_clean >= threshold).astype(int)
    
    acc = (y_pred == y_true_clean).mean()
    prec = precision_score(y_true_clean, y_pred, zero_division=0)
    rec = recall_score(y_true_clean, y_pred, zero_division=0)
    f1 = f1_score(y_true_clean, y_pred, zero_division=0)
    f2 = fbeta_score(y_true_clean, y_pred, beta=2.0, zero_division=0)
    
    precision_curve, recall_curve, _ = precision_recall_curve(y_true_clean, y_probs_clean)
    pr_auc = auc(recall_curve, precision_curve)
    
    try:
        roc_auc_val = roc_auc_score(y_true_clean, y_probs_clean)
    except Exception:
        roc_auc_val = 0.0
        
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
        "auc_pr": pr_auc,
        "roc_auc": roc_auc_val,
        "auc_roc": roc_auc_val,
        "tpr_at_01fpr": tpr_at_01fpr,
        "optimal_threshold": float(threshold)
    }


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


def to_homogeneous_projection(data):
    """Projects HeteroData to a single homogeneous tensor representation."""
    metadata = data.metadata()
    node_types = metadata[0]
    
    node_offsets = {}
    total_nodes = 0
    feature_list = []
    
    for nt in node_types:
        if hasattr(data[nt], "x") and data[nt].x is not None and data[nt].x.shape[0] > 0:
            x = data[nt].x
            node_offsets[nt] = total_nodes
            total_nodes += x.shape[0]
            feature_list.append(x)
        else:
            node_offsets[nt] = total_nodes
        
    if not feature_list:
        return torch.zeros((0, 16)), torch.zeros((2, 0), dtype=torch.long), node_offsets
        
    max_dim = max(x.shape[1] for x in feature_list)
    padded_features = []
    for x in feature_list:
        if x.shape[1] < max_dim:
            pad = torch.zeros(x.shape[0], max_dim - x.shape[1], device=x.device)
            padded_features.append(torch.cat([x, pad], dim=1))
        else:
            padded_features.append(x)
            
    x_homo = torch.cat(padded_features, dim=0)
    del padded_features, feature_list
    import gc
    gc.collect()
    x_homo = torch.nan_to_num(x_homo, nan=0.0, posinf=1.0, neginf=0.0)
    
    edge_index_list = []
    for relation in metadata[1]:
        if relation in data:
            src_type, _, dst_type = relation
            if src_type in node_offsets and dst_type in node_offsets:
                edges = data[relation].edge_index.clone()
                edges[0] += node_offsets[src_type]
                edges[1] += node_offsets[dst_type]
                edge_index_list.append(edges)
            
    if edge_index_list:
        edge_index_homo = torch.cat(edge_index_list, dim=1)
        del edge_index_list
        gc.collect()
    else:
        edge_index_homo = torch.zeros((2, 0), dtype=torch.long)
        
    return x_homo, edge_index_homo, node_offsets
