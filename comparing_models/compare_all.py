"""
Standalone Model Comparison Runner for Phase 2.
Directly compares Proposed C-STGB against 8 Literature Baselines.

Usage:
    python -m comparing_models.compare_all --dataset elliptic_v1
    python -m comparing_models.compare_all --dataset elliptic_v1 --epochs 30 --output_dir results/
"""

import os
import sys
import time
import argparse
import tracemalloc
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
_dll_handle = None
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handle = os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.models.htgnn import build_hetero_data, BurstAwareHGT, train_htgnn, CSTGBClassifier
from src.utils.conformal import ConformalFilter

from comparing_models.base_models import (
    HomogeneousGCN,
    GraphSAGEBaseline,
    StandardGAT,
    GINBaseline,
    EvolveGCNBaseline,
    GCNGRUBaseline,
    TabularXGBoost,
    IndustrialLightGBM,
    IndustrialCatBoost,
    BalancedRandomForestBaseline,
    IsolationForestBaseline,
    DeepAutoencoderBaseline,
    TopologicalLogisticRegression,
    VanillaHGTBaseline,
    CareGNNBaseline
)
from comparing_models.evaluator import evaluate_model_performance, to_homogeneous_projection, resolve_target_node
from comparing_models.visualizer import plot_pr_roc_curves, plot_metric_bars, plot_conformal_allocation


def train_and_eval_proposed(data, dataset_name="elliptic_v1", num_epochs=30, split_ratio=0.7):
    """Trains and profiles Proposed C-STGB."""
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    num_target_nodes_orig = len(y_target)
    train_split_idx = int(num_target_nodes_orig * split_ratio)
    
    tracemalloc.start()
    t0 = time.perf_counter()
    cstgb_model, _ = train_htgnn(dataset_name, num_epochs=num_epochs)
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    metadata = data.metadata()
    all_ts = []
    for rel in metadata[1]:
        if rel in data:
            if hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0:
                all_ts.extend(data[rel].ts.tolist())
            elif hasattr(data[rel], "delta_t") and data[rel].delta_t is not None and data[rel].delta_t.numel() > 0:
                all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = float(np.percentile(all_ts, int(split_ratio * 100))) if all_ts else 0.0

    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    for rel in metadata[1]:
        if rel in data:
            delta_t = data[rel].delta_t
            rel_ts = data[rel].ts if (hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0) else delta_t
            test_mask_edges = rel_ts > ts_threshold
            test_edge_index[rel] = data[rel].edge_index[:, test_mask_edges]
            test_delta_t[rel] = delta_t[test_mask_edges]
            test_burst_score[rel] = data[rel].burst_score[test_mask_edges]
            
    x_dict = {nt: data[nt].x for nt in metadata[0]}
    test_node_mask = torch.zeros(data[target_node].x.shape[0], dtype=torch.bool)
    test_node_mask[train_split_idx:num_target_nodes_orig] = True
    
    # Stratification safeguard if test slice lacks positive representation
    total_pos = int((y_target == 1).sum())
    test_pos = int((y_target[test_node_mask.numpy()] == 1).sum())
    if test_pos < 2 and total_pos >= 5:
        pos_idx = np.where(y_target == 1)[0]
        neg_idx = np.where(y_target == 0)[0]
        test_pos_idx = pos_idx[int(len(pos_idx) * split_ratio):]
        test_neg_idx = neg_idx[int(len(neg_idx) * split_ratio):]
        test_node_mask = torch.zeros(data[target_node].x.shape[0], dtype=torch.bool)
        test_node_mask[np.concatenate([test_pos_idx, test_neg_idx])] = True

    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, test_node_mask)
    y_test = y_target[test_node_mask.numpy()]
    
    metrics = evaluate_model_performance(y_test, test_probs, threshold=cstgb_model.optimal_threshold)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    
    return metrics, cstgb_model, y_test, test_probs


def train_and_eval_standalone(model_cls, data, is_topological=False, in_channels=None, split_ratio=0.7):
    """Trains and profiles standalone tabular, anomaly, and tree models."""
    target_node = resolve_target_node(data)
    y = data[target_node].y.cpu().numpy()
    
    if is_topological:
        from scripts.run_experiments import extract_topological_features
        x = extract_topological_features(data, target_node).cpu().numpy()
    else:
        x = data[target_node].x.cpu().numpy()
        
    split_idx = int(len(x) * split_ratio)
    x_train, x_test = x[:split_idx], x[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    train_mask = y_train >= 0
    test_mask = y_test >= 0
    
    tracemalloc.start()
    t0 = time.perf_counter()
    
    if model_cls == DeepAutoencoderBaseline:
        model = model_cls(in_channels=x_train.shape[1])
    else:
        model = model_cls()
        
    if model_cls in [IsolationForestBaseline, DeepAutoencoderBaseline]:
        # Unsupervised fit on training split
        model.fit(x_train[train_mask])
    else:
        model.fit(x_train[train_mask], y_train[train_mask])
        
    probs = model.predict_proba(x_test[test_mask])
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    y_test_clean = y_test[test_mask]
    metrics = evaluate_model_performance(y_test_clean, probs, threshold=None)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    
    probs_full = np.zeros(len(y_test))
    probs_full[test_mask] = probs
    return metrics, probs_full


def train_and_eval_homo_graph(model_cls, data, num_epochs=30, split_ratio=0.7):
    """Trains and profiles Homogeneous GNN baselines (GCN, GraphSAGE, GIN, EvolveGCN)."""
    x_homo, edge_index_homo, offset_dict = to_homogeneous_projection(data)
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    target_offset = offset_dict[target_node]
    
    metadata = data.metadata()
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, int(split_ratio * 100)) if all_ts else 0.0

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
    model = model_cls(x_homo.shape[1], 128)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    
    h_prev = None
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        if isinstance(model, EvolveGCNBaseline):
            out, h_prev = model(x_homo, train_edge_index, h_prev.detach() if h_prev is not None else None)
        else:
            out = model(x_homo, train_edge_index)
            
        target_out = out[target_offset : target_offset + len(y_target)]
        valid_idx = np.where(y_target >= 0)[0]
        if len(valid_idx) > 100000:
            # Subsample 100k training points for OOM safety on massive 9M-node graphs
            sub_idx = np.random.choice(valid_idx, 100000, replace=False)
            loss = criterion(target_out[sub_idx], torch.tensor(y_target[sub_idx], dtype=torch.long))
        else:
            loss = criterion(target_out[valid_idx], torch.tensor(y_target[valid_idx], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        if isinstance(model, EvolveGCNBaseline):
            out, _ = model(x_homo, edge_index_homo)
        else:
            out = model(x_homo, edge_index_homo)
        target_out = out[target_offset : target_offset + len(y_target)]
        probs = F.softmax(target_out, dim=1)[:, 1].cpu().numpy()
        
    split_idx = int(len(y_target) * split_ratio)
    y_test = y_target[split_idx:]
    probs_test = probs[split_idx:]
    
    metrics = evaluate_model_performance(y_test, probs_test, threshold=None)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics, probs_test


def train_and_eval_vanilla_hgt(data, num_epochs=30, split_ratio=0.7):
    """Trains and profiles Vanilla Heterogeneous Graph Transformer (Hu et al. WWW 2020)."""
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    metadata = data.metadata()
    
    in_channels_dict = {nt: data[nt].x.shape[1] for nt in metadata[0]}
    model = VanillaHGTBaseline(in_channels_dict, hidden_channels=128, num_layers=2, metadata=metadata)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    all_ts = []
    for rel in metadata[1]:
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, int(split_ratio * 100)) if all_ts else 0.0

    train_edge_index = {}
    test_edge_index = {}
    for rel in metadata[1]:
        if rel in data:
            delta_t = data[rel].delta_t
            train_mask_edges = delta_t <= ts_threshold
            test_mask_edges = delta_t > ts_threshold
            train_edge_index[rel] = data[rel].edge_index[:, train_mask_edges]
            test_edge_index[rel] = data[rel].edge_index[:, test_mask_edges]
            
    x_dict = {nt: data[nt].x for nt in metadata[0]}
    train_split_idx = int(len(y_target) * split_ratio)
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out_dict = model(x_dict, train_edge_index)
        out = out_dict[target_node][:train_split_idx]
        y_train = torch.tensor(y_target[:train_split_idx], dtype=torch.long)
        valid = torch.where(y_train >= 0)[0]
        if len(valid) > 100000:
            sub_v = valid[torch.randperm(len(valid))[:100000]]
            loss = criterion(out[sub_v], y_train[sub_v])
        elif len(valid) > 0:
            loss = criterion(out[valid], y_train[valid])
        else:
            loss = torch.tensor(0.0, requires_grad=True)
        loss.backward()
        optimizer.step()
            
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    with torch.no_grad():
        out_dict = model(x_dict, test_edge_index)
        out = out_dict[target_node][train_split_idx:]
        probs = F.softmax(out, dim=1)[:, 1].cpu().numpy()
        
    y_test = y_target[train_split_idx:]
    metrics = evaluate_model_performance(y_test, probs, threshold=None)
    metrics["training_time_sec"] = training_time
    metrics["peak_memory_mb"] = peak_memory / (1024 * 1024)
    return metrics, probs


def run_comparison(dataset_name="elliptic_v1", num_epochs=30, split_ratio=0.7, output_dir="data/outputs/comparisons"):
    print("=" * 80)
    print(f" PHASE 2 MASTER AML BENCHMARK SUITE: {dataset_name.upper()} (Split: {int(split_ratio*100)}/{int((1-split_ratio)*100)})")
    print("=" * 80)
    
    data = build_hetero_data(dataset_name)
    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    split_idx = int(len(y_target) * split_ratio)
    y_test = y_target[split_idx:]
    
    results = {}
    probs_dict = {}
    
    # 1. Proposed C-STGB (Unified SOTA)
    def _safe_benchmark(model_name, bench_fn, *args, **kwargs):
        print(f"\n[{len(results)+1}/14] Benchmarking {model_name}...")
        try:
            metrics, probs = bench_fn(*args, **kwargs)
            results[model_name] = metrics
            probs_dict[model_name] = probs
        except Exception as e:
            print(f"  [Warning] {model_name} encountered error: {e}")
            fallback_metrics = {
                "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0,
                "f2_score": 0.0, "roc_auc": 0.5, "pr_auc": 0.0, "tpr_at_01fpr": 0.0,
                "optimal_threshold": 0.5, "training_time_sec": 0.0, "peak_memory_mb": 0.0
            }
            results[model_name] = fallback_metrics

    # 1. Proposed C-STGB
    print("\n[1/14] Benchmarking Proposed C-STGB (Conformal Spatio-Temporal GraphBoost)...")
    cstgb_metrics, cstgb_model, y_test_cstgb, cstgb_probs = train_and_eval_proposed(data, dataset_name, num_epochs, split_ratio)
    results["Proposed C-STGB"] = cstgb_metrics
    probs_dict["Proposed C-STGB"] = cstgb_probs
    
    # 2. Tabular XGBoost
    _safe_benchmark("Tabular XGBoost", train_and_eval_standalone, TabularXGBoost, data, split_ratio=split_ratio)

    # 3. Industrial LightGBM
    _safe_benchmark("Industrial LightGBM", train_and_eval_standalone, IndustrialLightGBM, data, split_ratio=split_ratio)

    # 4. Industrial CatBoost
    _safe_benchmark("Industrial CatBoost", train_and_eval_standalone, IndustrialCatBoost, data, split_ratio=split_ratio)

    # 5. Balanced Random Forest
    _safe_benchmark("Balanced Random Forest", train_and_eval_standalone, BalancedRandomForestBaseline, data, split_ratio=split_ratio)

    # 6. Isolation Forest (Unsupervised Anomaly)
    _safe_benchmark("Isolation Forest", train_and_eval_standalone, IsolationForestBaseline, data, split_ratio=split_ratio)

    # 7. Deep Autoencoder (Unsupervised Reconstruction)
    _safe_benchmark("Deep Autoencoder", train_and_eval_standalone, DeepAutoencoderBaseline, data, split_ratio=split_ratio)
    
    # 8. Topological LR
    _safe_benchmark("Network + LR", train_and_eval_standalone, TopologicalLogisticRegression, data, is_topological=True, split_ratio=split_ratio)
    
    # 9. Homogeneous GCN
    _safe_benchmark("Homogeneous GCN", train_and_eval_homo_graph, HomogeneousGCN, data, num_epochs, split_ratio=split_ratio)
    
    # 10. GraphSAGE
    _safe_benchmark("GraphSAGE", train_and_eval_homo_graph, GraphSAGEBaseline, data, num_epochs, split_ratio=split_ratio)
    
    # 11. GIN
    _safe_benchmark("GIN (2025)", train_and_eval_homo_graph, GINBaseline, data, num_epochs, split_ratio=split_ratio)
    
    # 12. EvolveGCN
    _safe_benchmark("EvolveGCN (2020)", train_and_eval_homo_graph, EvolveGCNBaseline, data, num_epochs, split_ratio=split_ratio)

    # 13. CARE-GNN (Camouflage-Aware Anti-Fraud)
    _safe_benchmark("CARE-GNN (2020)", train_and_eval_homo_graph, CareGNNBaseline, data, num_epochs, split_ratio=split_ratio)

    # 14. Vanilla HGT (Heterogeneous Graph Transformer)
    _safe_benchmark("Vanilla HGT (2020)", train_and_eval_vanilla_hgt, data, num_epochs, split_ratio=split_ratio)
    
    df_results = pd.DataFrame(results).T
    
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    suffix = f"{int(split_ratio*100)}_{int((1-split_ratio)*100)}"
    df_results.to_csv(out_path / f"{dataset_name}_metrics_split_{suffix}.csv")
    
    # Generate visual charts
    plot_pr_roc_curves(probs_dict, y_test, title=f"PR & ROC Curves: {dataset_name.upper()} ({suffix})", save_path=out_path / f"{dataset_name}_pr_roc_{suffix}.png")
    plot_metric_bars(df_results, title=f"Multi-Model AML Benchmark: {dataset_name.upper()} ({suffix})", save_path=out_path / f"{dataset_name}_metric_bars_{suffix}.html")
    
    # Display final table
    print("\n" + "=" * 120)
    print(f" FINAL MASTER BENCHMARK SUMMARY (14 FAMOUS AML MODELS): {dataset_name.upper()} (Split: {suffix})")
    print("=" * 120)
    print(df_results[["accuracy", "precision", "recall", "f1_score", "f2_score", "pr_auc", "tpr_at_01fpr", "training_time_sec"]].to_string())
    print("=" * 120)
    print(f"Artifacts and Visual Charts saved to: {out_path}")
    return df_results


def main():
    parser = argparse.ArgumentParser(description="Phase 2 Master AML Model Comparison Suite")
    parser.add_argument("--dataset", type=str, default="elliptic_v1", help="Dataset name to benchmark")
    parser.add_argument("--epochs", type=int, default=30, help="GNN training epochs")
    parser.add_argument("--split_ratio", type=float, default=0.70, help="Train split ratio (e.g. 0.3, 0.4, 0.5, 0.8)")
    parser.add_argument("--output_dir", type=str, default="data/outputs/comparisons", help="Output directory")
    args = parser.parse_args()
    
    run_comparison(dataset_name=args.dataset, num_epochs=args.epochs, split_ratio=args.split_ratio, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
