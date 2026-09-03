"""
Multi-Dataset Phase 2 Benchmark Suite: Proposed C-STGB vs. 8 Literature Baselines.
Evaluates across all available ingested AML datasets in data/outputs/graph_data/.
"""

import os
import sys
import time
import json
import argparse
import tracemalloc
from pathlib import Path
import numpy as np
import polars as pl
import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.models.htgnn import build_hetero_data, train_htgnn, CSTGBClassifier
from src.utils.conformal import ConformalFilter

from scripts.run_experiments import (
    evaluate_metrics,
    resolve_target_node,
    train_and_profile_cstgb,
    train_and_profile_tabular,
    train_and_profile_gcn,
    train_and_profile_sage,
    train_and_profile_gat,
    train_and_profile_gin,
    train_and_profile_evolvegcn,
    train_and_profile_gcngru
)


def discover_available_datasets(graph_data_dir="data/outputs/graph_data"):
    """Discovers valid preprocessed datasets containing node and edge parquet files."""
    p = Path(graph_data_dir)
    if not p.exists():
        return []
    valid = []
    for d in sorted(p.iterdir()):
        if d.is_dir():
            nodes = list(d.glob("nodes*.parquet"))
            edges = list(d.glob("edges*.parquet"))
            if nodes and edges:
                valid.append(d.name)
    return valid


def run_benchmark_on_dataset(dataset_name, num_epochs=30):
    """Runs the 9-model comparative benchmarking on a specific dataset."""
    print("\n" + "=" * 80)
    print(f" BENCHMARKING DATASET: {dataset_name.upper()}")
    print("=" * 80)
    
    try:
        data = build_hetero_data(dataset_name)
    except Exception as e:
        print(f"  [ERROR] Failed to load {dataset_name}: {e}")
        return None

    target_node = resolve_target_node(data)
    y_target = data[target_node].y.cpu().numpy()
    valid_labels = y_target[y_target >= 0]
    
    if len(valid_labels) == 0 or len(np.unique(valid_labels)) < 2:
        print(f"  [SKIPPING] {dataset_name} lacks binary supervision labels (Unique labels: {np.unique(y_target)}).")
        return None

    results = {}
    
    # 1. Proposed C-STGB
    print(f"  [1/9] Training Proposed C-STGB on {dataset_name}...")
    try:
        cstgb, cstgb_model, y_test, cstgb_probs = train_and_profile_cstgb(data, dataset_name=dataset_name, num_epochs=num_epochs)
        results["C-STGB (Proposed)"] = cstgb
    except Exception as e:
        print(f"    [Warning] C-STGB error on {dataset_name}: {e}")
        results["C-STGB (Proposed)"] = {"f1_score": 0.0, "precision": 0.0, "recall": 0.0, "accuracy": 0.0, "f2_score": 0.0, "pr_auc": 0.0, "tpr_at_01fpr": 0.0, "training_time_sec": 0.0, "peak_memory_mb": 0.0}

    # 2. Tabular XGBoost
    print(f"  [2/9] Training Tabular XGBoost on {dataset_name}...")
    try:
        results["Tabular (XGB)"] = train_and_profile_tabular("xgb", data)
    except Exception as e:
        print(f"    [Warning] Tabular XGB error: {e}")

    # 3. Topological Logistic Regression
    print(f"  [3/9] Training Network + LR on {dataset_name}...")
    try:
        results["Network + LR"] = train_and_profile_tabular("topo_lr", data)
    except Exception as e:
        print(f"    [Warning] Network+LR error: {e}")

    # 4. Homogeneous GCN
    print(f"  [4/9] Training Homogeneous GCN on {dataset_name}...")
    try:
        results["Homogeneous GCN"] = train_and_profile_gcn(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] GCN error: {e}")

    # 5. GraphSAGE
    print(f"  [5/9] Training GraphSAGE on {dataset_name}...")
    try:
        results["GraphSAGE"] = train_and_profile_sage(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] GraphSAGE error: {e}")

    # 6. Standard GAT
    print(f"  [6/9] Training Standard GAT on {dataset_name}...")
    try:
        results["Standard GAT"] = train_and_profile_gat(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] GAT error: {e}")

    # 7. GIN
    print(f"  [7/9] Training GIN on {dataset_name}...")
    try:
        results["GIN (2025)"] = train_and_profile_gin(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] GIN error: {e}")

    # 8. EvolveGCN
    print(f"  [8/9] Training EvolveGCN on {dataset_name}...")
    try:
        results["EvolveGCN (2020)"] = train_and_profile_evolvegcn(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] EvolveGCN error: {e}")

    # 9. GCN-GRU
    print(f"  [9/9] Training GCN-GRU on {dataset_name}...")
    try:
        results["GCN-GRU"] = train_and_profile_gcngru(data, num_epochs=num_epochs)
    except Exception as e:
        print(f"    [Warning] GCN-GRU error: {e}")

    return results


def compile_multi_dataset_report(all_dataset_results, output_path="data/outputs/multi_dataset_benchmark_report.md"):
    """Compiles a cross-dataset benchmarking markdown report and CSV matrix."""
    lines = []
    lines.append("# Cross-Dataset Multi-Baseline Benchmark Report: C-STGB vs. Literature Models\n")
    lines.append(f"Evaluated across {len(all_dataset_results)} AML benchmarks with chronological splitting.\n")
    
    # Summary Table for F1-Scores across all datasets
    lines.append("## 1. Cross-Dataset F1-Score Performance Comparison\n")
    models = ["Tabular (XGB)", "Network + LR", "Homogeneous GCN", "GraphSAGE", "Standard GAT", "GIN (2025)", "EvolveGCN (2020)", "GCN-GRU", "C-STGB (Proposed)"]
    
    header = "| Dataset | " + " | ".join(models) + " |"
    separator = "| :--- | " + " | ".join([":---:"] * len(models)) + " |"
    lines.append(header)
    lines.append(separator)
    
    csv_rows = []
    
    for ds_name, ds_res in all_dataset_results.items():
        row_vals = []
        for m in models:
            if m in ds_res:
                score = ds_res[m].get("f1_score", 0.0)
                if m == "C-STGB (Proposed)":
                    row_vals.append(f"**{score:.4f}**")
                else:
                    row_vals.append(f"{score:.4f}")
            else:
                row_vals.append("N/A")
        lines.append(f"| **{ds_name}** | " + " | ".join(row_vals) + " |")
        
    lines.append("\n---\n")
    
    # Detailed tables per dataset
    lines.append("## 2. Granular Metrics per Dataset\n")
    for ds_name, ds_res in all_dataset_results.items():
        lines.append(f"### Dataset: `{ds_name}`\n")
        lines.append("| Metric | " + " | ".join(models) + " |")
        lines.append("| :--- | " + " | ".join([":---:"] * len(models)) + " |")
        
        for metric_key in ["accuracy", "precision", "recall", "f1_score", "f2_score", "pr_auc", "tpr_at_01fpr", "training_time_sec"]:
            m_label = metric_key.replace("_", " ").capitalize()
            row = [f"**{m_label}**"]
            for m in models:
                if m in ds_res:
                    val = ds_res[m].get(metric_key, 0.0)
                    if metric_key == "training_time_sec":
                        row.append(f"{val:.2f}s")
                    elif m == "C-STGB (Proposed)":
                        row.append(f"**{val:.4f}**")
                    else:
                        row.append(f"{val:.4f}")
                else:
                    row.append("N/A")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("\n")
        
    report_content = "\n".join(lines)
    
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(report_content, encoding="utf-8")
    
    # Also save to artifacts directory
    artifact_dir = Path("C:/Users/Nazmul Hasan Nihal/.gemini/antigravity-ide/brain/f0dd4eb5-aa65-4ac1-8be9-be8776a6c3a7")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "multi_dataset_benchmark_report.md").write_text(report_content, encoding="utf-8")
    
    print(f"\n[Report Exported] Cross-dataset summary written to {output_path} and artifacts.")


def main():
    parser = argparse.ArgumentParser(description="Multi-Dataset C-STGB Benchmark Suite")
    parser.add_argument("--datasets", nargs="+", default=["elliptic_v1", "paysim1", "saml_d"], help="Datasets to evaluate or 'all'")
    parser.add_argument("--epochs", type=int, default=30, help="Number of GNN training epochs")
    parser.add_argument("--output", type=str, default="data/outputs/multi_dataset_benchmark_report.md", help="Output report file path")
    args = parser.parse_args()

    available = discover_available_datasets()
    print(f"Discovered {len(available)} available graph dataset(s): {available}")

    target_datasets = available if "all" in args.datasets else [d for d in args.datasets if d in available]
    print(f"Targeting evaluation across {len(target_datasets)} dataset(s): {target_datasets}")

    all_results = {}
    for ds in target_datasets:
        res = run_benchmark_on_dataset(ds, num_epochs=args.epochs)
        if res is not None:
            all_results[ds] = res

    if all_results:
        compile_multi_dataset_report(all_results, output_path=args.output)
        print("\n" + "=" * 80)
        print(" MULTI-DATASET BENCHMARKING COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    main()
