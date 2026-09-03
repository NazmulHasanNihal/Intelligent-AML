"""
Automated Multi-Tier AML Benchmark Pipeline Orchestrator.
Intelligent-AML (Phase 2 Master Benchmark Suite)

Automates the end-to-end sequential benchmarking of Proposed C-STGB against 12 literature
baselines across all financial graph datasets, splits, and epoch configurations locally.

Features:
- Structured Tier Progression: Tier 1 (Pending) -> Tier 2 -> Tier 3 -> Multi-Split Expansion
- Resumable: Checks existing runs in master CSV/JSON to prevent redundant computations
- Memory-Safe: Enforces garbage collection and torch VRAM clearing between runs
- Auto-Merging: Consolidates metrics into master CSV, master JSON, and markdown reports
- Local Data Sourcing: Loads directly from data/outputs/graph_data/

Usage:
    # 1. Check current status across all tiers:
    python scripts/run_automated_benchmark_pipeline.py --status

    # 2. Run pending Tier 1 & Tier 2 datasets (70/30 split, 10 epochs):
    python scripts/run_automated_benchmark_pipeline.py --tier tier1_2

    # 3. Run Tier 3 scale-up datasets:
    python scripts/run_automated_benchmark_pipeline.py --tier tier3

    # 4. Run Multi-Split Expansion (50/50, 80/20, 40/60 splits, 30 epochs):
    python scripts/run_automated_benchmark_pipeline.py --tier expansion

    # 5. Run complete end-to-end remaining suite:
    python scripts/run_automated_benchmark_pipeline.py --tier all
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if os.name == "nt":
    _torch_lib = ROOT / "venv" / "Lib" / "site-packages" / "torch" / "lib"
    if _torch_lib.exists():
        try:
            os.add_dll_directory(str(_torch_lib))
        except Exception:
            pass

# IMPORTANT: torch MUST be imported before numpy, pandas, polars on Windows
import torch

import gc
import time
import json
import argparse
from datetime import datetime
import numpy as np
import pandas as pd

# Import benchmark components
from scripts.run_master_benchmark import (
    run_benchmark_for_dataset,
    save_single_result,
    generate_live_markdown_report,
    MASTER_CSV,
    MASTER_JSON,
    REPORT_MD
)

# ─────────────────────────────────────────────────────────────────────────────
# TIER DEFINITIONS & WORKFLOW CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

TIER_1_DATASETS = [
    "ibm_amlsim_li_small",   # Completed
    "ibm_amlsim_hi_small",   # Completed
    "saml_d",                # Completed
    "mtgox_leaked"           # PENDING
]

TIER_2_DATASETS = [
    "paysim1",               # Pending
    "data_generator",        # Pending
    "dgraphfin",             # Pending
    "xblock_eth"             # Pending
]

TIER_3_DATASETS = [
    "ibm_amlsim_hi_medium",  # Pending (Scaled Banking)
    "ibm_amlsim_li_medium",  # Pending (Scaled Banking)
    "eth_phishing",          # Pending (Ethereum Smart Contracts)
    "cc_transactions",       # Pending (Credit Card)
    "paysim_extended"        # Pending (71M Ledger)
]

ALL_BENCHMARK_DATASETS = [
    "elliptic_v1",
    "elliptic_v2",
    "ibm_amlsim_li_small",
    "ibm_amlsim_hi_small",
    "saml_d",
    "mtgox_leaked",
    "paysim1",
    "data_generator",
    "dgraphfin",
    "xblock_eth",
    "ibm_amlsim_hi_medium",
    "ibm_amlsim_li_medium",
    "eth_phishing",
    "cc_transactions",
    "paysim_extended"
]

EXPANSION_SPLITS = [0.50, 0.80, 0.40]
STANDARD_SPLITS = [0.70]

# ─────────────────────────────────────────────────────────────────────────────
# STATUS AUDITING UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def get_completed_runs():
    """Returns a set of (dataset, model, split, epochs) tuples already executed."""
    if not MASTER_CSV.exists():
        return set()
    try:
        df = pd.read_csv(MASTER_CSV)
        if df.empty:
            return set()
        completed = set()
        for _, row in df.iterrows():
            key = (
                str(row.get("dataset", "")).strip(),
                str(row.get("model", "")).strip(),
                str(row.get("split", "")).strip(),
                int(row.get("epochs", 10))
            )
            completed.add(key)
        return completed
    except Exception:
        return set()


def display_pipeline_status():
    """Prints a structured scorecard of completed vs pending benchmark trials."""
    completed = get_completed_runs()
    
    print("\n" + "=" * 90)
    print(" INTELLIGENT-AML BENCHMARK PROGRESS STATUS SCORECARD")
    print("=" * 90)
    print(f" Master CSV: {MASTER_CSV}")
    print(f" Master JSON: {MASTER_JSON}")
    print(f" Total Executed Trials Recorded: {len(completed)}")
    print("-" * 90)

    def print_tier_status(tier_name, datasets, expected_models=13):
        print(f"\n[{tier_name.upper()}]")
        print(f"{'Dataset':<26} | {'70/30 (10ep)':<15} | {'50/50 (10ep)':<15} | {'80/20 (10ep)':<15} | {'40/60 (10ep)':<15} | {'Status'}")
        print("-" * 90)
        for ds in datasets:
            c_70 = sum(1 for k in completed if k[0] == ds and k[2] == "70_30")
            c_50 = sum(1 for k in completed if k[0] == ds and k[2] == "50_50")
            c_80 = sum(1 for k in completed if k[0] == ds and k[2] == "80_20" or (k[0] == ds and k[2] == "80_19"))
            c_40 = sum(1 for k in completed if k[0] == ds and k[2] == "40_60")
            
            status = "COMPLETED" if c_70 >= expected_models else ("IN PROGRESS" if c_70 > 0 else "PENDING")
            print(f"{ds:<26} | {c_70:>2}/{expected_models:<11} | {c_50:>2}/{expected_models:<11} | {c_80:>2}/{expected_models:<11} | {c_40:>2}/{expected_models:<11} | {status}")

    print_tier_status("Tier 1: Core Synthetic & Blockchain Baselines", TIER_1_DATASETS)
    print_tier_status("Tier 2: FinTech, P2P & Mobile Money", TIER_2_DATASETS)
    print_tier_status("Tier 3: Scaled Multi-Million Graph Topologies", TIER_3_DATASETS)
    print("=" * 90 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# SEQUENTIAL AUTOMATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def run_dataset_benchmark_safe(dataset_name, epochs_list, splits_list, resume=True):
    """
    Executes all required splits and epochs for a single dataset.
    Ensures complete dataset completion before returning.
    """
    print("\n" + "#" * 90)
    print(f" STARTING BENCHMARK FOR DATASET: {dataset_name.upper()}")
    print(f" Target Splits: {splits_list} | Target Epochs: {epochs_list} | Local Source: data/outputs/graph_data/{dataset_name}")
    print("#" * 90)

    dataset_path = ROOT / "data" / "outputs" / "graph_data" / dataset_name
    if not dataset_path.exists():
        print(f"  [ERROR] Dataset directory not found at: {dataset_path}")
        print(f"  Skipping {dataset_name}...")
        return False

    if resume:
        completed = get_completed_runs()
        all_done = True
        for sp in splits_list:
            split_name = f"{int(sp*100)}_{int((1-sp)*100)}"
            for ep in epochs_list:
                c_count = sum(1 for k in completed if k[0] == dataset_name and k[2] == split_name and k[3] == ep)
                if c_count < 13:
                    all_done = False
                    break
            if not all_done:
                break
        if all_done and len(completed) > 0:
            print(f"  [STAGE SKIPPED - ALL COMPLETE] All 13 baseline and C-STGB models already executed and saved for {dataset_name.upper()}.")
            return True

    t_start = time.perf_counter()
    try:
        run_benchmark_for_dataset(
            dataset_name=dataset_name,
            epochs_list=epochs_list,
            splits_list=splits_list,
            reset=False,
            reset_master=False
        )
        elapsed = time.perf_counter() - t_start
        print(f"\n  [SUCCESS] Dataset {dataset_name.upper()} completed in {elapsed/60.0:.2f} minutes.")
        return True
    except Exception as e:
        print(f"\n  [CRITICAL ERROR] Execution failed on dataset {dataset_name}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def execute_pipeline(tier="all", custom_datasets=None, custom_splits=None, custom_epochs=None, resume=True):
    """
    Orchestrates the multi-tier sequential benchmark execution.
    """
    epochs_default = [10]
    splits_default = [0.70]

    epochs = custom_epochs or epochs_default
    splits = custom_splits or splits_default

    queue = []

    if custom_datasets:
        queue = [(ds, epochs, splits) for ds in custom_datasets]
    elif tier == "tier1":
        # Pending Tier 1 dataset: mtgox_leaked
        queue = [(ds, epochs, splits) for ds in ["mtgox_leaked"]]
    elif tier == "tier1_2":
        # Pending Tier 1 + All Tier 2 datasets
        pending_tier1_2 = ["mtgox_leaked"] + TIER_2_DATASETS
        queue = [(ds, epochs, splits) for ds in pending_tier1_2]
    elif tier == "tier2":
        queue = [(ds, epochs, splits) for ds in TIER_2_DATASETS]
    elif tier == "tier3":
        queue = [(ds, epochs, splits) for ds in TIER_3_DATASETS]
    elif tier == "expansion":
        # Run 50/50, 80/20, 40/60 splits and 30-epoch runs across core datasets
        expansion_datasets = ["elliptic_v1", "elliptic_v2", "ibm_amlsim_hi_small", "ibm_amlsim_li_small", "saml_d", "mtgox_leaked", "paysim1"]
        queue = [(ds, [10, 30], EXPANSION_SPLITS) for ds in expansion_datasets]
    elif tier == "all":
        # 1. Pending Tier 1/2
        pending_t1_t2 = ["mtgox_leaked"] + TIER_2_DATASETS
        for ds in pending_t1_t2:
            queue.append((ds, [10], [0.70]))
        # 2. Tier 3 Scale-Up
        for ds in TIER_3_DATASETS:
            queue.append((ds, [10], [0.70]))
        # 3. Expansion Phase (Multi-split & 30-epoch)
        for ds in ALL_BENCHMARK_DATASETS:
            queue.append((ds, [30], [0.50, 0.80, 0.40]))
    else:
        print(f"Unknown tier specification: {tier}")
        return

    print("\n" + "=" * 90)
    print(" INTELLIGENT-AML AUTOMATED BENCHMARK ORCHESTRATION WORKFLOW")
    print("=" * 90)
    print(f" Execution Plan: {len(queue)} dataset-configuration stages queued.")
    for idx, (ds, ep, sp) in enumerate(queue, 1):
        print(f"  Stage {idx:02d}/{len(queue):02d}: Dataset='{ds}' | Splits={sp} | Epochs={ep}")
    print("=" * 90 + "\n")

    overall_start = time.perf_counter()
    successful_stages = 0

    for idx, (dataset_name, epoch_list, split_list) in enumerate(queue, 1):
        print(f"\n>>> [Stage {idx}/{len(queue)}] Processing Dataset {dataset_name.upper()} ({idx} of {len(queue)})")
        success = run_dataset_benchmark_safe(
            dataset_name=dataset_name,
            epochs_list=epoch_list,
            splits_list=split_list,
            resume=resume
        )
        if success:
            successful_stages += 1
            # Re-generate consolidated master markdown report after each stage
            generate_live_markdown_report(dataset_name)

    total_time = time.perf_counter() - overall_start
    print("\n" + "=" * 90)
    print(" BENCHMARK WORKFLOW EXECUTION COMPLETE")
    print(f" Successfully Finished: {successful_stages}/{len(queue)} stages")
    print(f" Total Wall-Clock Time: {total_time/3600.0:.2f} hours ({total_time/60.0:.1f} minutes)")
    print(f" Master Scorecard CSV:  {MASTER_CSV}")
    print(f" Master Scorecard JSON: {MASTER_JSON}")
    print(f" Consolidated Report:   {REPORT_MD}")
    print("=" * 90 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent-AML Automated Benchmark Pipeline Orchestrator"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check and display current benchmark completion scorecard across all tiers"
    )
    parser.add_argument(
        "--tier",
        type=str,
        choices=["tier1", "tier2", "tier1_2", "tier3", "expansion", "all"],
        default="tier1_2",
        help="Benchmark tier to execute: tier1, tier2, tier1_2 (pending T1+T2), tier3, expansion, or all"
    )
    parser.add_argument(
        "--datasets",
        type=str,
        default="",
        help="Optional comma-separated dataset names override (e.g. 'mtgox_leaked,paysim1')"
    )
    parser.add_argument(
        "--splits",
        type=str,
        default="",
        help="Optional comma-separated split ratios override (e.g. '0.70,0.50')"
    )
    parser.add_argument(
        "--epochs",
        type=str,
        default="",
        help="Optional comma-separated epochs override (e.g. '10,30')"
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Disable run deduplication check and force re-running existing configs"
    )

    args = parser.parse_args()

    if args.status:
        display_pipeline_status()
        return

    custom_datasets = [d.strip() for d in args.datasets.split(",") if d.strip()] if args.datasets else None
    custom_splits = [float(s.strip()) for s in args.splits.split(",") if s.strip()] if args.splits else None
    custom_epochs = [int(e.strip()) for e in args.epochs.split(",") if e.strip()] if args.epochs else None

    execute_pipeline(
        tier=args.tier,
        custom_datasets=custom_datasets,
        custom_splits=custom_splits,
        custom_epochs=custom_epochs,
        resume=not args.no_resume
    )


if __name__ == "__main__":
    main()
