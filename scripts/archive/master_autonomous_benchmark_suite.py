"""
master_autonomous_benchmark_suite.py — Master Autonomous Benchmark Suite with Resilient Checkpointing.

Executes comprehensive end-to-end benchmark comparisons across all 24 datasets and 14 literature baselines.
Features:
- Resilient JSON checkpointing: Resumes automatically from last completed dataset if interrupted.
- Real-time incremental CSV metric persistence.
- Captures 12+ granular performance metrics (Accuracy, Precision, Recall, F1, F2, PR-AUC, ROC-AUC, TPR@0.1%FPR, Optimal Tau, Time, Latency, Peak RAM).
- Fully autonomous execution with zero manual pauses.
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

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_dll_handle = None
if os.name == "nt":
    _torch_lib = ROOT / "venv" / "Lib" / "site-packages" / "torch" / "lib"
    if _torch_lib.exists():
        os.environ["PATH"] = str(_torch_lib) + ";" + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                _dll_handle = os.add_dll_directory(str(_torch_lib))
            except Exception:
                pass

import pandas as pd
import numpy as np
import torch

from comparing_models.compare_all import run_comparison

# Comprehensive 24-Dataset Catalog across 5 Archetypes
ALL_DATASETS = [
    # 1. Crypto & Blockchain Forensic Networks
    "elliptic_v1",
    "elliptic_v2",
    "eth_phishing",
    "eth_phishing_2nd",
    "xblock_eth",
    "mtgox_leaked",
    "smart_ponzi",
    
    # 2. Multi-Tier Banking & Inter-Bank Clearing
    "ibm_amlsim_hi_small",
    "ibm_amlsim_hi_small_accounts",
    "ibm_amlsim_hi_medium",
    "ibm_amlsim_hi_medium_accounts",
    "ibm_amlsim_li_small",
    "ibm_amlsim_li_small_accounts",
    "ibm_amlsim_li_medium",
    "ibm_amlsim_li_medium_accounts",
    "saml_d",
    "synthaml",
    
    # 3. High-Velocity Mobile Money
    "paysim1",
    "paysim_extended",
    
    # 4. FinTech Lending & Credit Card Fraud
    "dgraphfin",
    "cc_transactions",
    "ulb_credit_card",
    
    # 5. Synthetic Simulators & Enterprise Live Demos
    "data_generator",
    "live_demo",
]


class BenchmarkCheckpointManager:
    """Manages persistent JSON checkpointing and master CSV synchronization."""

    def __init__(self, checkpoint_file="results/benchmarks/autonomous_checkpoint.json",
                 master_csv="results/metrics/master_all_datasets_benchmark.csv"):
        self.checkpoint_path = ROOT / checkpoint_file
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        self.master_csv_path = ROOT / master_csv
        self.master_csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self):
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"  [Checkpoint] Warning reading checkpoint file, starting fresh: {e}")
        return {
            "started_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "completed_datasets": [],
            "failed_datasets": {},
            "dataset_timings": {}
        }

    def save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        temp_file = self.checkpoint_path.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
        temp_file.replace(self.checkpoint_path)

    def is_completed(self, dataset_name):
        return dataset_name in self.state.get("completed_datasets", [])

    def mark_completed(self, dataset_name, elapsed_sec, metrics_df):
        if dataset_name not in self.state["completed_datasets"]:
            self.state["completed_datasets"].append(dataset_name)
        self.state["dataset_timings"][dataset_name] = round(elapsed_sec, 2)
        self.save_state()

        # Incremental write to master CSV with deduplication
        metrics_df["dataset"] = dataset_name
        metrics_df["model"] = metrics_df.index
        metrics_df["timestamp"] = datetime.now().isoformat()

        if self.master_csv_path.exists():
            try:
                existing_df = pd.read_csv(self.master_csv_path)
                # Filter out previous runs for this dataset to avoid duplicate rows
                existing_df = existing_df[existing_df["dataset"] != dataset_name]
                combined_df = pd.concat([existing_df, metrics_df], ignore_index=True)
                combined_df.to_csv(self.master_csv_path, index=False)
            except Exception:
                metrics_df.to_csv(self.master_csv_path, index=False)
        else:
            metrics_df.to_csv(self.master_csv_path, index=False)

    def mark_failed(self, dataset_name, error_msg):
        self.state["failed_datasets"][dataset_name] = {
            "error": str(error_msg),
            "timestamp": datetime.now().isoformat()
        }
        self.save_state()


def run_master_autonomous_benchmarks(datasets=None, epochs=10, split_ratio=0.7,
                                     checkpoint_file="results/benchmarks/autonomous_checkpoint.json",
                                     master_csv="results/metrics/master_all_datasets_benchmark.csv",
                                     output_dir="data/outputs/comparisons"):
    if datasets is None:
        datasets = ALL_DATASETS

    mgr = BenchmarkCheckpointManager(checkpoint_file=checkpoint_file, master_csv=master_csv)
    out_dir_path = ROOT / output_dir
    out_dir_path.mkdir(parents=True, exist_ok=True)

    pending_datasets = [d for d in datasets if not mgr.is_completed(d)]
    completed_count = len(datasets) - len(pending_datasets)

    print("=" * 95)
    print(" MASTER AUTONOMOUS AML BENCHMARK SUITE (24 DATASETS x 14 MODELS)")
    print(f" Total Datasets: {len(datasets)} | Completed: {completed_count} | Pending: {len(pending_datasets)}")
    print(f" Checkpoint Tracker: {mgr.checkpoint_path}")
    print(f" Master Metrics CSV: {mgr.master_csv_path}")
    print(f" Settings: Epochs={epochs} | Split Ratio={split_ratio*100:.0f}/{(1-split_ratio)*100:.0f}")
    print("=" * 95)

    if not pending_datasets:
        print("\n [SUCCESS] All 24 datasets have already been completed!")
        return

    for idx, dset in enumerate(pending_datasets, 1):
        overall_idx = len(datasets) - len(pending_datasets) + idx
        print("\n" + "=" * 90)
        print(f" [{overall_idx}/{len(datasets)}] AUTONOMOUS BENCHMARK: {dset.upper()}")
        print("=" * 90)

        t0 = time.perf_counter()
        try:
            df_metrics = run_comparison(
                dataset_name=dset,
                num_epochs=epochs,
                split_ratio=split_ratio,
                output_dir=str(out_dir_path)
            )

            elapsed = time.perf_counter() - t0
            mgr.mark_completed(dset, elapsed, df_metrics)
            print(f"\n  [SUCCESS] Completed {dset.upper()} in {elapsed:.1f}s | Progress saved to Checkpoint & Master CSV.")

            # Display scorecard
            display_cols = [c for c in ["accuracy", "precision", "recall", "f1_score", "f2_score", "pr_auc", "training_time_sec"] if c in df_metrics.columns]
            print("\n  Scorecard Summary:")
            print(df_metrics[display_cols].to_string())

        except Exception as e:
            elapsed = time.perf_counter() - t0
            print(f"\n  [WARNING] Dataset {dset} encountered error: {e}")
            import traceback
            traceback.print_exc()
            mgr.mark_failed(dset, str(e))
            print(f"  [Auto-Resume] Checkpoint updated. Continuing autonomously to next dataset...")

    print("\n" + "=" * 95)
    print(" ALL 24 DATASET BENCHMARK RUNS COMPLETED!")
    print(f" Master Results File: {mgr.master_csv_path}")
    print("=" * 95)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master Autonomous 24-Dataset Benchmark Suite")
    parser.add_argument("--datasets", type=str, default=None, help="Optional subset of comma-separated datasets")
    parser.add_argument("--epochs", type=int, default=10, help="GNN training epochs (default: 10)")
    parser.add_argument("--split", type=float, default=0.7, help="Train split ratio (default: 0.7)")
    parser.add_argument("--checkpoint", type=str, default="results/benchmarks/autonomous_checkpoint.json")
    parser.add_argument("--master_csv", type=str, default="results/metrics/master_all_datasets_benchmark.csv")
    args = parser.parse_args()

    dset_list = [d.strip() for d in args.datasets.split(",")] if args.datasets else None
    run_master_autonomous_benchmarks(
        datasets=dset_list,
        epochs=args.epochs,
        split_ratio=args.split,
        checkpoint_file=args.checkpoint,
        master_csv=args.master_csv
    )
