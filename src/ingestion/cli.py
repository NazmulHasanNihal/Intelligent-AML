#!/usr/bin/env python
"""
Layer 1 CLI — run the ingestion engine from anywhere with one command.

Examples
--------
  # Ingest every configured dataset (Kaggle: paths already mounted; local: set DATA_DIR)
  python -m src.ingestion.cli --all

  # Ingest just one dataset from a local folder
  python -m src.ingestion.cli --dataset paysim1 --path /data/paysim

  # Ingest a single CSV into a graph with explicit typing
  python -m src.ingestion.cli --csv txns.csv --name mydata \
        --src-col sender --dst-col receiver --label-col is_fraud \
        --src-type Account --dst-type Institution

The engine is dependency-light (polars + duckdb + pyarrow) and imports instantly
(DuckDB spins up lazily on first use). Output lands in data/outputs/graph_data/.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Intelligent AML — Layer 1 ingestion CLI")
    ap.add_argument("--all", action="store_true", help="Run the full configured pipeline (run_all_datasets)")
    ap.add_argument("--dataset", help="Name of a configured dataset to ingest")
    ap.add_argument("--path", help="Local path (folder or file) for --dataset / --csv")
    ap.add_argument("--csv", help="A single CSV/TSV file to ingest as a graph")
    ap.add_argument("--name", help="Output dataset name (for --csv)")
    ap.add_argument("--src-col", default=None, help="Source/node column")
    ap.add_argument("--dst-col", default=None, help="Destination/node column")
    ap.add_argument("--label-col", default=None, help="Label column")
    ap.add_argument("--ts-col", default=None, help="Timestamp column (normalized to ts)")
    ap.add_argument("--src-type", default="Account", help="Source node type")
    ap.add_argument("--dst-type", default="Account", help="Destination node type")
    ap.add_argument("--edge-type", default="Transaction", help="Edge type")
    ap.add_argument("--no-split", action="store_true", help="Skip train/val/test split")
    return ap


def main(argv=None):
    args = _build_parser().parse_args(argv)
    from src.ingestion import pipeline as P

    if args.all:
        P.run_all_datasets()
        if not args.no_split:
            P.split_all_datasets()
        P.write_run_manifest(P.OUTPUT_DIR)
        print("\n✅ Layer 1 complete. Output:", P.OUTPUT_DIR)
        return

    if args.csv:
        name = args.name or Path(args.csv).stem
        path = Path(args.csv)
        print(f"📥 Ingesting {path} -> {name}")
        # Build a minimal DATASETS entry so the universal engine handles it.
        P.DATASETS[name] = path
        hints = {}
        if args.src_col: hints["src_hints"] = [args.src_col]
        if args.dst_col: hints["dst_hints"] = [args.dst_col]
        if args.label_col: hints["label_hints"] = [args.label_col]
        P.ingest_transaction_csv(
            name, path, src_node_type=args.src_type, dst_node_type=args.dst_type,
            edge_type_name=args.edge_type, **hints)
        if not args.no_split:
            P.split_dataset(name, strategy="temporal")
        P.write_run_manifest(P.OUTPUT_DIR)
        print("✅ Done. Output:", P.OUTPUT_DIR / name)
        return

    if args.dataset:
        target = args.path or P.DATASETS.get(args.dataset)
        if target is None:
            print(f"❌ No path for dataset '{args.dataset}'. Pass --path or add it to DATASETS.")
            sys.exit(1)
        P.ingest_transaction_csv(args.dataset, Path(target),
                                 src_node_type=args.src_type, dst_node_type=args.dst_type,
                                 edge_type_name=args.edge_type)
        if not args.no_split:
            P.split_dataset(args.dataset, strategy="temporal")
        print("✅ Done.")
        return

    _build_parser().print_help()


if __name__ == "__main__":
    main()
