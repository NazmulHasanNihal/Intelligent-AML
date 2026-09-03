"""
run_sequential_benchmarks.py — Autonomous Sequential Multi-Dataset Benchmark Runner.

Executes end-to-end benchmark performance testing on non-elliptic datasets one by one,
saving real-time incremental scorecard CSVs, JSON checkpoints, and comparison charts after each dataset.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_dll_handle = None
_venv_torch_lib = Path(__file__).resolve().parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handle = os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import torch
import pandas as pd
import numpy as np

from comparing_models.compare_all import run_comparison

# Non-Elliptic Datasets for Comprehensive Master Evaluation
BENCHMARK_DATASETS = [
    "paysim_extended",
    "eth_phishing",
    "xblock_eth",
    "saml_d",
    "mtgox_leaked",
    "ibm_amlsim_hi_small",
    "ibm_amlsim_li_small",
    "ibm_amlsim_hi_medium",
    "ibm_amlsim_li_medium",
    "cc_transactions",
    "dgraphfin",
    "ulb_credit_card",
    "synthaml",
    "smart_ponzi",
    "paysim1"
]


def run_sequential_benchmarks(epochs=5, split_ratio=0.7,
                              output_dir="data/outputs/comparisons",
                              master_csv="results/metrics/sequential_benchmark_metrics.csv",
                              checkpoint_file="results/benchmarks/sequential_checkpoint.json"):
    out_dir = ROOT / output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    master_csv_path = ROOT / master_csv
    master_csv_path.parent.mkdir(parents=True, exist_ok=True)
    ckpt_path = ROOT / checkpoint_file
    ckpt_path.parent.mkdir(parents=True, exist_ok=True)

    # Load or initialize checkpoint
    if ckpt_path.exists():
        try:
            with open(ckpt_path, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {"completed": [], "failed": {}, "timings": {}}
    else:
        state = {"completed": [], "failed": {}, "timings": {}}

    print("=" * 95)
    print(" STARTING SEQUENTIAL MASTER AML BENCHMARK PERFORMANCE TESTING")
    print(f" Datasets to test: {len(BENCHMARK_DATASETS)} (Excluding elliptic_v1 & elliptic_v2)")
    print(f" Master Metrics CSV: {master_csv_path}")
    print(f" Checkpoint Tracker: {ckpt_path}")
    print("=" * 95)

    all_results = []
    if master_csv_path.exists():
        try:
            existing_df = pd.read_csv(master_csv_path)
            all_results.append(existing_df)
        except Exception:
            pass

    for idx, dset in enumerate(BENCHMARK_DATASETS, 1):
        print("\n" + "=" * 90)
        print(f" [{idx}/{len(BENCHMARK_DATASETS)}] RUNNING BENCHMARK EVALUATION: {dset.upper()}")
        print("=" * 90)

        # Availability Guard
        dset_dir = ROOT / "data" / "outputs" / "graph_data" / dset
        nodes_file = dset_dir / "nodes.parquet"
        if not nodes_file.exists():
            print(f"  [SKIPPED] Dataset {dset} is not yet ingested (nodes.parquet not found). Continuing...")
            state["failed"][dset] = "nodes.parquet not found"
            continue

        t0 = time.perf_counter()
        try:
            df_metrics = run_comparison(
                dataset_name=dset,
                num_epochs=epochs,
                split_ratio=split_ratio,
                output_dir=str(out_dir)
            )
            elapsed = time.perf_counter() - t0

            # Save state immediately
            if dset not in state["completed"]:
                state["completed"].append(dset)
            state["timings"][dset] = round(elapsed, 2)
            with open(ckpt_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)

            # Format and append to master CSV
            df_save = df_metrics.copy()
            df_save["dataset"] = dset
            df_save["model"] = df_save.index
            df_save["timestamp"] = datetime.now().isoformat()

            if master_csv_path.exists():
                try:
                    cur_master = pd.read_csv(master_csv_path)
                    cur_master = cur_master[cur_master["dataset"] != dset]
                    combined = pd.concat([cur_master, df_save], ignore_index=True)
                    combined.to_csv(master_csv_path, index=False)
                except Exception:
                    df_save.to_csv(master_csv_path, index=False)
            else:
                df_save.to_csv(master_csv_path, index=False)

            print(f"\n  [SUCCESS] Dataset {dset.upper()} completed in {elapsed:.1f}s!")
            print(f"  Scorecard for {dset.upper()}:")
            display_cols = [c for c in ["accuracy", "precision", "recall", "f1_score", "f2_score", "pr_auc", "tpr_at_01fpr"] if c in df_metrics.columns]
            print(df_metrics[display_cols].to_string())

        except Exception as e:
            elapsed = time.perf_counter() - t0
            print(f"\n  [ERROR] Dataset {dset} failed with: {e}")
            import traceback
            traceback.print_exc()
            state["failed"][dset] = str(e)
            with open(ckpt_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)

    print("\n" + "=" * 95)
    print(" ALL SEQUENTIAL BENCHMARK PERFORMANCE TESTS COMPLETE!")
    print(f" Master Consolidated Results: {master_csv_path}")
    print("=" * 95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sequential Benchmarks across Non-Elliptic Datasets")
    parser.add_argument("--epochs", type=int, default=5, help="GNN training epochs")
    parser.add_argument("--split", type=float, default=0.7, help="Train split ratio")
    parser.add_argument("--output_dir", type=str, default="data/outputs/comparisons")
    parser.add_argument("--master_csv", type=str, default="results/metrics/sequential_benchmark_metrics.csv")
    args = parser.parse_args()

    run_sequential_benchmarks(
        epochs=args.epochs,
        split_ratio=args.split,
        output_dir=args.output_dir,
        master_csv=args.master_csv
    )
