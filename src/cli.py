#!/usr/bin/env python
"""
Intelligent-AML Master CLI.
Provides a unified developer command-line interface for running benchmarks,
simulations, test suites, figure generation, and ingestion.

Usage:
    intelligent-aml [command] [options]
    python -m src.cli [command] [options]
"""

from __future__ import annotations

import argparse
import os
import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def cmd_test(args):
    """Run the test suite."""
    print("🧪 Running Intelligent-AML Test Suite...")
    cmd = [sys.executable, "-m", "pytest", "tests/"]
    if args.verbose:
        cmd.append("-v")
    if args.filter:
        cmd.extend(["-k", args.filter])
    sys.exit(subprocess.call(cmd, cwd=REPO_ROOT))


def cmd_demo(args):
    """Run the enterprise streaming AML production simulation."""
    print("🏛️ Running Enterprise AML Production Simulation...")
    from scripts.run_enterprise_aml_demo import run_enterprise_simulation
    run_enterprise_simulation()


def cmd_benchmark(args):
    """Run the master comparative benchmark or standalone GNN improvement."""
    if args.standalone:
        print("📈 Running Standalone GNN Improvement Benchmark...")
        import benchmark_standalone_gnn_improvement
        benchmark_standalone_gnn_improvement.main()
    else:
        print("📊 Running Comprehensive Multi-Dataset Benchmark...")
        import run_before_after_comparison
        run_before_after_comparison.main()


def cmd_figures(args):
    """Generate 300 DPI publication figures (PDF and PNG)."""
    print("🎨 Generating 300 DPI Publication Vector Figures...")
    import generate_publication_figures
    generate_publication_figures.main()


def cmd_scorecard(args):
    """Print the 13-dataset master literature scorecard."""
    print("📋 Displaying 13-Dataset Literature Benchmark Scorecard...")
    import print_all_datasets_report
    print_all_datasets_report.main()


def cmd_ingest(args):
    """Run the DuckDB/Polars ingestion engine."""
    from src.ingestion.cli import main as ingest_main
    ingest_args = []
    if args.all:
        ingest_args.append("--all")
    if args.dataset:
        ingest_args.extend(["--dataset", args.dataset])
    if args.csv:
        ingest_args.extend(["--csv", args.csv])
    ingest_main(ingest_args)


def cmd_dashboard(args):
    """Launch the interactive Streamlit enterprise compliance dashboard."""
    print("🌐 Launching Intelligent-AML Enterprise Compliance Dashboard (Streamlit)...")
    dashboard_path = os.path.join(REPO_ROOT, "scripts", "dashboard.py")
    cmd = [sys.executable, "-m", "streamlit", "run", dashboard_path]
    if args.port:
        cmd.extend(["--server.port", str(args.port)])
    sys.exit(subprocess.call(cmd, cwd=REPO_ROOT))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intelligent-aml",
        description="🏛️ Intelligent-AML: Conformal Spatio-Temporal GraphBoost Platform"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # test command
    p_test = subparsers.add_parser("test", help="Run automated test suite (102+ tests)")
    p_test.add_argument("-v", "--verbose", action="store_true", help="Verbose test output")
    p_test.add_argument("-k", "--filter", default=None, help="Filter test names by keyword")
    p_test.set_defaults(func=cmd_test)

    # dashboard command
    p_dash = subparsers.add_parser("dashboard", help="Launch interactive Streamlit enterprise compliance dashboard")
    p_dash.add_argument("-p", "--port", type=int, default=8501, help="Port to bind dashboard server (default: 8501)")
    p_dash.set_defaults(func=cmd_dashboard)

    # demo command
    p_demo = subparsers.add_parser("demo", help="Run live enterprise streaming AML simulation")
    p_demo.set_defaults(func=cmd_demo)

    # benchmark command
    p_bench = subparsers.add_parser("benchmark", help="Run model benchmarking suite")
    p_bench.add_argument("--standalone", action="store_true", help="Run standalone GNN improvement benchmark")
    p_bench.set_defaults(func=cmd_benchmark)

    # figures command
    p_fig = subparsers.add_parser("figures", help="Generate publication-ready 300 DPI figures")
    p_fig.set_defaults(func=cmd_figures)

    # scorecard command
    p_card = subparsers.add_parser("scorecard", help="Display 13-dataset performance scorecard")
    p_card.set_defaults(func=cmd_scorecard)

    # ingest command
    p_ingest = subparsers.add_parser("ingest", help="Run DuckDB/Polars data ingestion engine")
    p_ingest.add_argument("--all", action="store_true", help="Ingest all configured datasets")
    p_ingest.add_argument("--dataset", help="Specific dataset to ingest")
    p_ingest.add_argument("--csv", help="Single CSV to ingest")
    p_ingest.set_defaults(func=cmd_ingest)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

