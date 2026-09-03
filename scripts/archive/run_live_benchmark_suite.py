"""
run_live_benchmark_suite.py — Live Post-Optimization Benchmark Runner.

Executes end-to-end benchmark comparisons across datasets and literature baselines,
measuring training time, inference latency, peak RAM, F1, precision, recall, and AUC.
Saves results incrementally dataset-by-dataset to prevent data loss.
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

if os.name == "nt":
    _torch_lib = ROOT / "venv" / "Lib" / "site-packages" / "torch" / "lib"
    if _torch_lib.exists():
        os.environ["PATH"] = str(_torch_lib) + ";" + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(str(_torch_lib))
            except Exception:
                pass

import pandas as pd
import numpy as np
import torch

from comparing_models.compare_all import run_comparison

# Datasets in order of priority: core benchmarks first
PRIORITY_DATASETS = [
    "elliptic_v1",
    "ibm_amlsim_hi_small",
    "ibm_amlsim_li_small",
    "saml_d",
    "paysim1",
    "elliptic_v2",
    "cc_transactions",
    "dgraphfin",
]


def run_live_benchmark(datasets=None, epochs=15, split_ratio=0.7,
                       output_csv="results/metrics/new_live_benchmark_results.csv",
                       output_dir="results/outputs/comparisons"):
    if datasets is None:
        datasets = PRIORITY_DATASETS
        
    out_csv_path = ROOT / output_csv
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    out_dir_path = ROOT / output_dir
    out_dir_path.mkdir(parents=True, exist_ok=True)

    print("=" * 90)
    print(f" LIVE POST-UPDATE AML BENCHMARK RUNNER")
    print(f" Datasets: {datasets}")
    print(f" Epochs: {epochs} | Split Ratio: {split_ratio} ({int(split_ratio*100)}/{int((1-split_ratio)*100)})")
    print(f" Results Target: {out_csv_path}")
    print("=" * 90)

    for idx, dset in enumerate(datasets, 1):
        print(f"\n{'='*80}")
        print(f" [{idx}/{len(datasets)}] BENCHMARKING DATASET: {dset.upper()}")
        print(f"{'='*80}")
        
        t0_dset = time.perf_counter()
        try:
            df_metrics = run_comparison(
                dataset_name=dset,
                num_epochs=epochs,
                split_ratio=split_ratio,
                output_dir=str(out_dir_path)
            )
            
            df_metrics["dataset"] = dset
            df_metrics["split_ratio"] = split_ratio
            df_metrics["epochs"] = epochs
            df_metrics["timestamp"] = datetime.now().isoformat()
            
            # Save or append immediately to prevent data loss
            if out_csv_path.exists():
                existing = pd.read_csv(out_csv_path)
                combined = pd.concat([existing, df_metrics], ignore_index=True)
                combined.to_csv(out_csv_path, index=False)
            else:
                df_metrics.to_csv(out_csv_path, index=False)
                
            elapsed = time.perf_counter() - t0_dset
            print(f"\n  [COMPLETED] {dset.upper()} in {elapsed:.1f}s — Results written to {out_csv_path.name}")
            
            # Print scorecard for Proposed C-STGB vs Baselines
            if "Proposed C-STGB" in df_metrics.index or "model" in df_metrics.columns:
                print("\n  Summary Scorecard:")
                display_cols = [c for c in ["f1_score", "precision", "recall", "pr_auc", "roc_auc", "training_time_sec", "peak_memory_mb"] if c in df_metrics.columns]
                print(df_metrics[display_cols].to_string())
                
        except Exception as e:
            print(f"  [ERROR] Benchmark failed for {dset}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 90)
    print(" ALL DATASET BENCHMARKS COMPLETED!")
    print(f" Final master results saved to: {out_csv_path}")
    print("=" * 90)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", type=str, default=None, help="Comma-separated dataset names")
    parser.add_argument("--epochs", type=int, default=15, help="Number of GNN training epochs")
    parser.add_argument("--split", type=float, default=0.7, help="Train split ratio (default: 0.7)")
    parser.add_argument("--output_csv", type=str, default="results/metrics/new_live_benchmark_results.csv")
    args = parser.parse_args()

    dset_list = [d.strip() for d in args.datasets.split(",")] if args.datasets else None
    run_live_benchmark(datasets=dset_list, epochs=args.epochs, split_ratio=args.split, output_csv=args.output_csv)
