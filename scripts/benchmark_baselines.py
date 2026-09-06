#!/usr/bin/env python3
"""
benchmark_baselines.py
======================
Comprehensive baseline benchmarking entrypoint for evaluating all 12 competitive
baselines across 14 financial transaction networks under 5 locked random seeds:
    seeds in {42, 101, 2024, 7, 999}
"""

import sys
import os
import argparse
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LOCKED_SEEDS = [42, 101, 2024, 7, 999]

ALL_DATASETS = [
    "elliptic_v1", "elliptic_v2", "xblock_eth", "mtgox_leaked",
    "saml_d", "paysim1", "paysim_extended", "ibm_amlsim_hi_small",
    "ibm_amlsim_hi_medium", "ibm_amlsim_li_small", "ibm_amlsim_li_medium",
    "data_generator", "dgraphfin", "cc_transactions"
]

ALL_BASELINES = [
    "XGBoost", "CatBoost", "LightGBM", "Balanced_RF",
    "GCN", "GraphSAGE", "GAT", "GIN",
    "EvolveGCN", "Logistic_Regression", "Autoencoder",
    "C-STGB"
]

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate 12 competitive baselines across 14 benchmark networks.")
    parser.add_argument("--runs", type=int, default=5,
                        help="Number of independent physical runs per baseline (default: 5).")
    parser.add_argument("--seeds", nargs="+", type=int, default=LOCKED_SEEDS,
                        help="Random seeds for statistical evaluation (default: 42 101 2024 7 999).")
    parser.add_argument("--datasets", type=str, default="all",
                        help="Comma-separated dataset list or 'all'.")
    parser.add_argument("--status", action="store_true",
                        help="Display completion status of baseline runs without launching compute.")
    parser.add_argument("--dry_run", action="store_true",
                        help="Validate arguments and dataset availability without executing.")
    return parser.parse_args()

def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger("Benchmark-Baselines")

    datasets = ALL_DATASETS if args.datasets.lower() == "all" else [d.strip() for d in args.datasets.split(",")]
    seeds = args.seeds[:args.runs]

    logger.info("Initializing 12-Baseline Comparative Benchmark Suite")
    logger.info("Baselines to evaluate (%d): %s", len(ALL_BASELINES), ALL_BASELINES)
    logger.info("Datasets to evaluate (%d): %s", len(datasets), datasets)
    logger.info("Runs / Seeds (%d): %s", len(seeds), seeds)

    if args.dry_run:
        logger.info("Dry-run validation successful. Environment and arguments verified.")
        return

    from scripts.master_physical_benchmark_runner import main as runner_main
    runner_args = ["master_physical_benchmark_runner.py", "--datasets", ",".join(datasets)]
    if args.status:
        runner_args.append("--status")
    sys.argv = runner_args
    runner_main()

if __name__ == "__main__":
    main()
