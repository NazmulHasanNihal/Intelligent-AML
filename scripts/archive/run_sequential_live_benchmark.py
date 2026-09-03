import sys
import os
import re

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# IMPORTANT: torch MUST be imported before numpy, pandas, polars on Windows
import torch
import torch.nn as nn
import torch.nn.functional as F

import gc
import time
import json
import argparse
import tracemalloc
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.models.htgnn import build_hetero_data, BurstAwareHGT, train_htgnn, CSTGBClassifier
from src.utils.conformal import SoftMondrianConformalFilter
from comparing_models.base_models import (
    HomogeneousGCN,
    GraphSAGEBaseline,
    HomogeneousGAT,
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

RUNS_DIR = ROOT / "results" / "metrics" / "runs"
MASTER_CSV = ROOT / "results" / "metrics" / "master_detailed_benchmark_results.csv"
MASTER_JSON = ROOT / "results" / "metrics" / "master_detailed_benchmark_results.json"


def slugify(text):
    """Converts model name into a clean filename slug."""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)


def save_single_result(record, dataset_name):
    """
    Saves an individual run JSON file into results/metrics/runs/,
    and appends to both the dataset-specific master file and global master files.
    """
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Save Individual Run JSON
    model_slug = slugify(record["model"])
    ts_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    run_file = RUNS_DIR / f"{dataset_name}_{model_slug}_{record['split']}_{record['epochs']}ep_{ts_str}.json"
    with open(run_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
        
    # 2. Append to Dataset-Specific Master Files
    ds_csv = ROOT / "results" / "metrics" / f"{dataset_name}_master_benchmark.csv"
    ds_json = ROOT / "results" / "metrics" / f"{dataset_name}_master_benchmark.json"
    
    df_single = pd.DataFrame([record])
    if not ds_csv.exists():
        df_single.to_csv(ds_csv, index=False)
    else:
        df_single.to_csv(ds_csv, mode="a", header=False, index=False)
        
    ds_records = []
    if ds_json.exists():
        try:
            with open(ds_json, "r", encoding="utf-8") as f:
                ds_records = json.load(f)
        except Exception:
            ds_records = []
    ds_records.append(record)
    with open(ds_json, "w", encoding="utf-8") as f:
        json.dump(ds_records, f, indent=2)
        
    # 3. Append to Global Master Files
    MASTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not MASTER_CSV.exists():
        df_single.to_csv(MASTER_CSV, index=False)
    else:
        df_single.to_csv(MASTER_CSV, mode="a", header=False, index=False)
        
    global_records = []
    if MASTER_JSON.exists():
        try:
            with open(MASTER_JSON, "r", encoding="utf-8") as f:
                global_records = json.load(f)
        except Exception:
            global_records = []
    global_records.append(record)
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(global_records, f, indent=2)


def get_dataset_metadata(data, dataset_name):
    """Extracts summary statistics for the dataset."""
    metadata = data.metadata()
    node_types, edge_types = metadata
    
    total_nodes = sum(data[nt].num_nodes for nt in node_types if hasattr(data[nt], "num_nodes") and data[nt].num_nodes is not None)
    total_edges = 0
    for et in edge_types:
        try:
            if hasattr(data[et], "edge_index") and data[et].edge_index is not None:
                total_edges += int(data[et].edge_index.shape[1])
        except Exception:
            pass
            
    target_node = resolve_target_node(data)
    y = data[target_node].y.cpu().numpy()
    valid_mask = y >= 0
    pos_count = int(np.sum(y == 1))
    neg_count = int(np.sum(y == 0))
    illicit_pct = (pos_count / max(1, pos_count + neg_count)) * 100.0
    feat_dim = data[target_node].x.shape[1] if hasattr(data[target_node], "x") else 0
    
    return {
        "dataset": dataset_name,
        "target_node": target_node,
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "target_features": feat_dim,
        "licit_count": neg_count,
        "illicit_count": pos_count,
        "illicit_ratio_pct": round(illicit_pct, 4)
    }


def evaluate_proposed_cstgb(data, dataset_name, num_epochs=10, split_ratio=0.70):
    """Evaluates C-STGB model with memory tracking and latency profiling."""
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
        if rel in data and hasattr(data[rel], "delta_t"):
            all_ts.extend(data[rel].delta_t.tolist())
    ts_threshold = np.percentile(all_ts, int(split_ratio * 100)) if all_ts else 0.0

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
    
    t_lat0 = time.perf_counter()
    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, test_node_mask)
    inf_latency = (time.perf_counter() - t_lat0) / max(1, test_node_mask.sum().item()) * 1000.0
    
    y_test = y_target[train_split_idx:num_target_nodes_orig]
    metrics = evaluate_model_performance(y_test, test_probs, threshold=cstgb_model.optimal_threshold)
    metrics["training_time_sec"] = round(training_time, 2)
    metrics["inference_latency_ms"] = round(inf_latency, 4)
    metrics["peak_memory_mb"] = round(peak_memory / (1024 * 1024), 2)
    
    del cstgb_model, test_edge_index, test_delta_t, test_burst_score, x_dict
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    return metrics


def evaluate_tabular_model(model_cls, data, split_ratio=0.70, is_topological=False):
    """Evaluates standalone tabular, tree, or anomaly models."""
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
        model = model_cls(in_channels=x_train.shape[1], epochs=15)
    else:
        model = model_cls()
        
    if model_cls in [IsolationForestBaseline, DeepAutoencoderBaseline]:
        model.fit(x_train[train_mask])
    else:
        model.fit(x_train[train_mask], y_train[train_mask])
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    t_lat0 = time.perf_counter()
    probs = model.predict_proba(x_test[test_mask])
    inf_latency = (time.perf_counter() - t_lat0) / max(1, len(probs)) * 1000.0
    
    y_test_clean = y_test[test_mask]
    thresh = 0.70 if model_cls not in [IsolationForestBaseline, DeepAutoencoderBaseline] else 0.50
    metrics = evaluate_model_performance(y_test_clean, probs, threshold=thresh)
    metrics["training_time_sec"] = round(training_time, 2)
    metrics["inference_latency_ms"] = round(inf_latency, 4)
    metrics["peak_memory_mb"] = round(peak_memory / (1024 * 1024), 2)
    
    del model, x_train, x_test, y_train, y_test
    gc.collect()
    return metrics


def evaluate_gnn_model(model_cls, data, num_epochs=10, split_ratio=0.70):
    """Evaluates homogeneous GNN baselines (GCN, GraphSAGE, GIN, EvolveGCN, GAT)."""
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
    hidden_dim = 64 if x_homo.shape[0] > 500000 else 128
    model = model_cls(x_homo.shape[1], hidden_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    tracemalloc.start()
    t0 = time.perf_counter()
    model.train()
    
    effective_epochs = min(5, num_epochs) if x_homo.shape[0] > 1000000 else num_epochs
    train_mask_full = np.where(y_target >= 0)[0]
    
    h_prev = None
    for epoch in range(1, effective_epochs + 1):
        optimizer.zero_grad()
        if isinstance(model, EvolveGCNBaseline):
            out, h_prev = model(x_homo, train_edge_index, h_prev.detach() if h_prev is not None else None)
        else:
            out = model(x_homo, train_edge_index)
            
        target_out = out[target_offset : target_offset + len(y_target)]
        
        # Subsampled loss for multi-million graphs
        if len(train_mask_full) > 50000:
            batch_idx = np.random.choice(train_mask_full, size=50000, replace=False)
        else:
            batch_idx = train_mask_full
            
        loss = criterion(target_out[batch_idx], torch.tensor(y_target[batch_idx], dtype=torch.long))
        loss.backward()
        optimizer.step()
        
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    t_lat0 = time.perf_counter()
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
    inf_latency = (time.perf_counter() - t_lat0) / max(1, len(probs_test)) * 1000.0
    
    metrics = evaluate_model_performance(y_test, probs_test, threshold=0.70)
    metrics["training_time_sec"] = round(training_time, 2)
    metrics["inference_latency_ms"] = round(inf_latency, 4)
    metrics["peak_memory_mb"] = round(peak_memory / (1024 * 1024), 2)
    
    del model, optimizer, criterion, x_homo, edge_index_homo, train_edge_index
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    return metrics


def evaluate_vanilla_hgt_model(data, num_epochs=10, split_ratio=0.70):
    """Evaluates Vanilla Heterogeneous Graph Transformer baseline (Hu et al. WWW 2020)."""
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
        valid = y_train >= 0
        if valid.sum() > 0:
            loss = criterion(out[valid], y_train[valid])
            loss.backward()
            optimizer.step()
            
    training_time = time.perf_counter() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    model.eval()
    t_lat0 = time.perf_counter()
    with torch.no_grad():
        out_dict = model(x_dict, test_edge_index)
        out = out_dict[target_node][train_split_idx:]
        probs = F.softmax(out, dim=1)[:, 1].cpu().numpy()
        
    y_test = y_target[train_split_idx:]
    inf_latency = (time.perf_counter() - t_lat0) / max(1, len(probs)) * 1000.0
    
    metrics = evaluate_model_performance(y_test, probs, threshold=0.70)
    metrics["training_time_sec"] = round(training_time, 2)
    metrics["inference_latency_ms"] = round(inf_latency, 4)
    metrics["peak_memory_mb"] = round(peak_memory / (1024 * 1024), 2)
    
    del model, optimizer, criterion, x_dict, train_edge_index, test_edge_index
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    return metrics


def run_benchmark_for_dataset(dataset_name, epochs_list=[10], splits_list=[0.70], clean_state=True):
    """
    Sequentially runs and logs every model for a single dataset across epochs and splits.
    """
    if clean_state:
        cache_file = ROOT / "data" / "cache" / f"{dataset_name}_temporal_features.parquet"
        if cache_file.exists():
            print(f"  [Clean State] Flushing pre-existing cache file: {cache_file}")
            try:
                cache_file.unlink()
            except Exception as e:
                print(f"  [Clean State] Warning: Could not delete cache: {e}")

    print("\n" + "=" * 95)
    print(f" [STARTING FRESH LIVE BENCHMARK] DATASET: {dataset_name.upper()}")
    print("=" * 95)
    
    data = build_hetero_data(dataset_name)
    ds_meta = get_dataset_metadata(data, dataset_name)
    
    print(f"  Dataset Characteristics:")
    print(f"    * Total Nodes:      {ds_meta['total_nodes']:,}")
    print(f"    * Total Edges:      {ds_meta['total_edges']:,}")
    print(f"    * Target Entity:    '{ds_meta['target_node']}' ({ds_meta['target_features']} features)")
    print(f"    * Class Skew:       {ds_meta['licit_count']:,} Licit / {ds_meta['illicit_count']:,} Illicit ({ds_meta['illicit_ratio_pct']}% Illicit)")
    print("-" * 95)
    
    models_to_run = [
        ("Proposed C-STGB", "cstgb", None),
        ("Tabular XGBoost", "tabular", TabularXGBoost),
        ("Industrial LightGBM", "tabular", IndustrialLightGBM),
        ("Industrial CatBoost", "tabular", IndustrialCatBoost),
        ("Balanced Random Forest", "tabular", BalancedRandomForestBaseline),
        ("Topological Logistic Reg", "tabular_topo", TopologicalLogisticRegression),
        ("Isolation Forest (Unsupervised)", "tabular", IsolationForestBaseline),
        ("Deep Autoencoder (Reconstruction)", "tabular", DeepAutoencoderBaseline),
        ("Homogeneous GCN", "gnn", HomogeneousGCN),
        ("Inductive GraphSAGE", "gnn", GraphSAGEBaseline),
        ("GIN (Graph Isomorphism)", "gnn", GINBaseline),
        ("EvolveGCN (Dynamic GNN)", "gnn", EvolveGCNBaseline),
        ("Homogeneous GAT", "gnn", HomogeneousGAT),
        ("CARE-GNN (Camouflage-Aware)", "gnn", CareGNNBaseline),
        ("Vanilla HGT (Hu et al. 2020)", "vanilla_hgt", VanillaHGTBaseline)
    ]
    
    dataset_records = []
    
    for split_ratio in splits_list:
        split_name = f"{int(split_ratio*100)}_{int((1-split_ratio)*100)}"
        
        for epochs in epochs_list:
            print(f"\n>>> Running Evaluation Suite: Split={split_name} | Epochs={epochs}")
            
            for m_idx, (model_name, m_type, m_cls) in enumerate(models_to_run, 1):
                print(f"  [{m_idx:02d}/{len(models_to_run):02d}] Running {model_name:<36} ... ", end="", flush=True)
                
                try:
                    t_start = time.perf_counter()
                    if m_type == "cstgb":
                        metrics = evaluate_proposed_cstgb(data, dataset_name, num_epochs=epochs, split_ratio=split_ratio)
                    elif m_type == "tabular":
                        metrics = evaluate_tabular_model(m_cls, data, split_ratio=split_ratio, is_topological=False)
                    elif m_type == "tabular_topo":
                        metrics = evaluate_tabular_model(m_cls, data, split_ratio=split_ratio, is_topological=True)
                    elif m_type == "gnn":
                        metrics = evaluate_gnn_model(m_cls, data, num_epochs=epochs, split_ratio=split_ratio)
                    elif m_type == "vanilla_hgt":
                        metrics = evaluate_vanilla_hgt_model(data, num_epochs=epochs, split_ratio=split_ratio)
                    else:
                        continue
                        
                    elapsed = time.perf_counter() - t_start
                    
                    # Assemble full record
                    record = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "dataset": dataset_name,
                        "model": model_name,
                        "split": split_name,
                        "split_ratio": split_ratio,
                        "epochs": epochs,
                        "total_nodes": ds_meta["total_nodes"],
                        "total_edges": ds_meta["total_edges"],
                        "illicit_pct": ds_meta["illicit_ratio_pct"],
                        "f1_score": round(metrics["f1_score"], 4),
                        "precision": round(metrics["precision"], 4),
                        "recall": round(metrics["recall"], 4),
                        "f2_score": round(metrics["f2_score"], 4),
                        "pr_auc": round(metrics["pr_auc"], 4),
                        "roc_auc": round(metrics["roc_auc"], 4),
                        "tpr_at_01fpr": round(metrics["tpr_at_01fpr"], 4),
                        "accuracy": round(metrics["accuracy"], 4),
                        "training_time_sec": metrics["training_time_sec"],
                        "inference_latency_ms": metrics["inference_latency_ms"],
                        "peak_memory_mb": metrics["peak_memory_mb"]
                    }
                    
                    save_single_result(record, dataset_name)
                    dataset_records.append(record)
                    print(f"DONE ({elapsed:.1f}s) -> F1: {metrics['f1_score']:.4f} | Prec: {metrics['precision']:.4f} | Rec: {metrics['recall']:.4f} | PR-AUC: {metrics['pr_auc']:.4f} | Lat: {metrics['inference_latency_ms']}ms")
                    
                except Exception as e:
                    print(f"FAILED: {e}")
                    import traceback
                    traceback.print_exc()
                    
                # Strict garbage collection after each model
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
    del data
    gc.collect()
    
    ds_csv = ROOT / "results" / "metrics" / f"{dataset_name}_master_benchmark.csv"
    print(f"\n[Completed Dataset: {dataset_name}] Master results saved to:")
    print(f"  * CSV:  {ds_csv}")
    print(f"  * JSON: {ROOT / 'results' / 'metrics' / f'{dataset_name}_master_benchmark.json'}")
    print(f"  * Runs: {RUNS_DIR}")
    
    # Print formatted summary table
    if dataset_records:
        df_summary = pd.DataFrame(dataset_records)
        print("\n" + "=" * 110)
        print(f" EMPIRICAL BENCHMARK SCORECARD: {dataset_name.upper()}")
        print("=" * 110)
        cols_to_print = ["model", "f1_score", "precision", "recall", "f2_score", "pr_auc", "roc_auc", "tpr_at_01fpr", "training_time_sec", "inference_latency_ms"]
        print(df_summary[cols_to_print].to_string(index=False))
        print("=" * 110)
        
    return dataset_records


def main():
    parser = argparse.ArgumentParser(description="Sequential Memory-Safe Live AML Benchmark Runner")
    parser.add_argument("--dataset", type=str, default="elliptic_v1", help="Dataset name to run (e.g. elliptic_v1, elliptic_v2, ibm_amlsim_hi_small, etc.)")
    parser.add_argument("--epochs", type=str, default="10", help="Comma-separated epochs list")
    parser.add_argument("--splits", type=str, default="0.70", help="Comma-separated split ratios list")
    parser.add_argument("--clean_state", action="store_true", default=True, help="Force flush existing cache")
    args = parser.parse_args()
    
    epochs_list = [int(e.strip()) for e in args.epochs.split(",") if e.strip()]
    splits_list = [float(s.strip()) for s in args.splits.split(",") if s.strip()]
    
    run_benchmark_for_dataset(args.dataset, epochs_list=epochs_list, splits_list=splits_list, clean_state=args.clean_state)


if __name__ == "__main__":
    main()
