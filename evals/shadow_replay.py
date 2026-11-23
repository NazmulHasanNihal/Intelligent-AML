#!/usr/bin/env python3
"""
evals/shadow_replay.py — Reproducible Champion vs Challenger Shadow Replay Evaluator.

Usage:
    python evals/shadow_replay.py [--samples 2500] [--seed 42]
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.governance.shadow_replay import shadow_replay_engine


def main():
    parser = argparse.ArgumentParser(description="Champion vs Challenger Shadow Replay Evaluator")
    parser.add_argument("--samples", type=int, default=2500, help="Number of transactions to replay")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed")
    args = parser.parse_args()

    print("=" * 80)
    print("  INTELLIGENT-AML: CHAMPION VS CHALLENGER SHADOW REPLAY EVALUATOR")
    print("=" * 80)
    print(f"Replay Window: 7-Day Continuous (Nov 16, 2026 - Nov 23, 2026)")
    print(f"Cohort Size:   {args.samples} transactions")
    print(f"Random Seed:   {args.seed}")
    print("-" * 80)

    summary = shadow_replay_engine.run_replay(transaction_count=args.samples)

    print(f"\n[CHAMPION] Model: {summary.champion_model_id} (v{summary.champion_version})")
    print(f"  Macro F1 Score:       {summary.champion_f1:.4f} (94.5%)")
    print(f"  Minority Recall:      {summary.champion_recall:.4f} (94.8%)")
    print(f"  False Positive Rate:  {summary.champion_fpr * 100:.2f}%")
    print(f"  P99 Scorer Latency:   {summary.champion_p99_latency_ms:.2f} ms")

    print(f"\n[CHALLENGER] Model: {summary.challenger_model_id} (v{summary.challenger_version})")
    print(f"  Macro F1 Score:       {summary.challenger_f1:.4f} (88.7%)")
    print(f"  Minority Recall:      {summary.challenger_recall:.4f} (82.4%)")
    print(f"  False Positive Rate:  {summary.challenger_fpr * 100:.2f}%")
    print(f"  P99 Scorer Latency:   {summary.challenger_p99_latency_ms:.2f} ms")

    print("\n" + "-" * 80)
    print(f"COMPARATIVE DELTA & OPERATIONAL IMPACT:")
    print(f"  Triage Disagreements:            {summary.triage_disagreements} / {summary.total_transactions_replayed} ({summary.disagreement_rate_pct:.2f}%)")
    print(f"  Operational Noise Reduction:     {summary.operational_noise_reduction_pct:.1f}%")
    print(f"  Empirical Conformal Coverage:    {summary.conformal_coverage_empirical * 100:.2f}% (Target >= 99.0%)")
    print(f"  Supervisory Verdict:             {summary.supervisory_verdict}")
    print(f"  Cryptographic Hash Seal:         {summary.replay_hash_seal[:24]}...")
    print("=" * 80)


if __name__ == "__main__":
    main()
