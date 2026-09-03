"""
Universal Multi-Dataset Multi-Split Benchmark Runner for C-STGB.
Iterates across ALL ready graph datasets in data/outputs/graph_data/
and evaluates across all 4 split ratios (30/70, 40/60, 50/50, 80/20).

Usage:
    python scripts/benchmark_all_datasets.py --epochs 10
    python scripts/benchmark_all_datasets.py --datasets elliptic_v1,elliptic_v2,ibm_amlsim_hi_small --epochs 15
"""

import os
import sys
import time
import argparse
from pathlib import Path

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

import torch
import pandas as pd
import numpy as np

from comparing_models.compare_all import run_comparison

ALL_DATASETS = [
    "elliptic_v1",
    "elliptic_v2",
    "ibm_amlsim_hi_small",
    "ibm_amlsim_li_small",
    "ibm_amlsim_hi_medium",
    "ibm_amlsim_li_medium",
    "saml_d",
    "paysim1",
    "paysim_extended",
    "mtgox_leaked",
    "eth_phishing",
    "xblock_eth",
    "dgraphfin",
    "cc_transactions",
    "data_generator"
]

SPLIT_RATIOS = [0.30, 0.40, 0.50, 0.80]


def run_full_suite(datasets=None, epochs=10, splits=None, output_dir="data/outputs/comparisons"):
    if datasets is None:
        datasets = ALL_DATASETS
    if splits is None:
        splits = SPLIT_RATIOS

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    master_summary = []

    print("=" * 100)
    print(f" UNIVERSAL MULTI-DATASET AML BENCHMARK: {len(datasets)} DATASETS | {len(splits)} SPLITS")
    print("=" * 100)

    for d_idx, dataset_name in enumerate(datasets, 1):
        print(f"\n>>> [{d_idx}/{len(datasets)}] PROCESSING DATASET: {dataset_name.upper()}")
        for s_idx, split_ratio in enumerate(splits, 1):
            suffix = f"{int(split_ratio*100)}_{int((1-split_ratio)*100)}"
            print(f"  --> Split [{s_idx}/{len(splits)}]: {suffix}")
            
            try:
                df_metrics = run_comparison(
                    dataset_name=dataset_name,
                    num_epochs=epochs,
                    split_ratio=split_ratio,
                    output_dir=output_dir
                )
                df_metrics["dataset"] = dataset_name
                df_metrics["split_ratio"] = split_ratio
                df_metrics["split_name"] = suffix
                master_summary.append(df_metrics)
            except Exception as e:
                print(f"  [Error] Skipping {dataset_name} ({suffix}) due to: {e}")

    if master_summary:
        df_master = pd.concat(master_summary)
        df_master.to_csv(out_path / "master_multi_dataset_benchmark_results.csv")
        print("\n" + "=" * 100)
        print(" MASTER BENCHMARK RUN COMPLETE! Results saved to data/outputs/comparisons/master_multi_dataset_benchmark_results.csv")
        print("=" * 100)


def main():
    parser = argparse.ArgumentParser(description="Universal Multi-Dataset Multi-Split Benchmark Runner")
    parser.add_argument("--datasets", type=str, default="", help="Comma-separated dataset names (leave empty for all)")
    parser.add_argument("--epochs", type=int, default=10, help="GNN training epochs per trial")
    parser.add_argument("--splits", type=str, default="0.30,0.40,0.50,0.80", help="Comma-separated split ratios")
    parser.add_argument("--output_dir", type=str, default="data/outputs/comparisons", help="Output directory")
    args = parser.parse_args()

    datasets = [d.strip() for d in args.datasets.split(",") if d.strip()] if args.datasets else ALL_DATASETS
    splits = [float(s.strip()) for s in args.splits.split(",") if s.strip()]

    run_full_suite(datasets=datasets, epochs=args.epochs, splits=splits, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
