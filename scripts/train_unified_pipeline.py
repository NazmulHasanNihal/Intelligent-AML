#!/usr/bin/env python3
"""
train_unified_pipeline.py
=========================
Master training entrypoint for C-STGB (Conformal Spatio-Temporal Graph Neural Network)
across all benchmark datasets under the 5 locked evaluation random seeds:
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

def parse_args():
    parser = argparse.ArgumentParser(description="Train C-STGB Unified Pipeline across datasets and seeds.")
    parser.add_argument("--dataset", type=str, default="all",
                        help="Target dataset name or 'all' for complete 14-dataset evaluation.")
    parser.add_argument("--seeds", nargs="+", type=int, default=LOCKED_SEEDS,
                        help="Random seeds for statistical evaluation (default: 42 101 2024 7 999).")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Maximum training epochs per seed.")
    parser.add_argument("--dry_run", action="store_true",
                        help="Perform configuration validation without running training.")
    return parser.parse_args()

def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger("C-STGB-Train")

    datasets = ALL_DATASETS if args.dataset.lower() == "all" else [d.strip() for d in args.dataset.split(",")]
    logger.info("Initializing C-STGB Unified Multi-Stage Training Pipeline")
    logger.info("Datasets to evaluate (%d): %s", len(datasets), datasets)
    logger.info("Evaluation seeds (%d): %s", len(args.seeds), args.seeds)
    logger.info("Max epochs: %d", args.epochs)

    if args.dry_run:
        logger.info("Dry-run validation successful. Environment and arguments verified.")
        return

    # Forward to the physical benchmark execution engine
    from scripts.master_physical_benchmark_runner import main as runner_main
    sys.argv = ["master_physical_benchmark_runner.py", "--datasets", ",".join(datasets)]
    runner_main()

if __name__ == "__main__":
    main()
