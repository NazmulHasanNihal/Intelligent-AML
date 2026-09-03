#!/usr/bin/env python3
"""
fetch_kaggle_results.py
=======================
Imports and merges completed benchmark results from Kaggle back into the local workspace.

Usage:
    # 1. Automatic fetch using Kaggle CLI (if kernel was run via Kaggle):
    python scripts/fetch_kaggle_results.py --kernel nazmulhasannihal/intelligent-aml-master-benchmark

    # 2. Manual import from a downloaded ZIP file:
    python scripts/fetch_kaggle_results.py --zip C:/Users/Nazmul/Downloads/intelligent_aml_benchmark_results.zip
"""

import sys
import os
import json
import shutil
import zipfile
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# Central Paths
BENCHMARKS_DIR = ROOT / "results" / "benchmarks"
METRICS_DIR = ROOT / "results" / "metrics"
MASTER_CSV = METRICS_DIR / "master_detailed_benchmark_results.csv"
MASTER_JSON = METRICS_DIR / "master_detailed_benchmark_results.json"
PROGRESS_MD = ROOT / "docs" / "Live_Physical_Benchmark_Progress.md"


def merge_checkpoints(src_dir: Path):
    """Merges all extracted checkpoints into local results/benchmarks."""
    imported_count = 0
    for ckpt_file in src_dir.rglob("*.json"):
        if "checkpoints" in ckpt_file.parts:
            # Reconstruct relative destination
            rel = ckpt_file.relative_to(src_dir)
            target = ROOT / "results" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ckpt_file, target)
            imported_count += 1
    return imported_count


def merge_master_csv(extracted_csv: Path):
    """Merges newly evaluated rows into the master benchmark CSV."""
    if not extracted_csv.exists():
        return 0
    try:
        new_df = pd.read_csv(extracted_csv)
        if MASTER_CSV.exists():
            existing_df = pd.read_csv(MASTER_CSV)
            # Combine and deduplicate based on dataset, model, split, epochs
            combined = pd.concat([existing_df, new_df], ignore_index=True)
            combined = combined.drop_duplicates(subset=["dataset", "model", "split", "epochs"], keep="last")
            combined.to_csv(MASTER_CSV, index=False)
            return len(combined) - len(existing_df)
        else:
            new_df.to_csv(MASTER_CSV, index=False)
            return len(new_df)
    except Exception as e:
        print(f"  [Warning] Error merging CSV: {e}")
        return 0


def update_progress_report():
    """Triggers the master progress report update."""
    try:
        from scripts.master_physical_benchmark_runner import update_live_progress_report
        update_live_progress_report()
        print(f"  Updated live progress scorecard: {PROGRESS_MD}")
    except Exception as e:
        print(f"  Could not update progress markdown: {e}")


def import_results(zip_path: str = None, kernel_name: str = None):
    print("=" * 80)
    print(" INTELLIGENT-AML: FETCH & IMPORT KAGGLE BENCHMARK RESULTS")
    print("=" * 80)

    temp_extract = ROOT / "data" / "_temp_kaggle_results"
    if temp_extract.exists():
        shutil.rmtree(temp_extract)
    temp_extract.mkdir(parents=True, exist_ok=True)

    target_zip = None

    # Option A: Automatic download from Kaggle CLI
    if kernel_name:
        print(f"\n[1/3] Downloading kernel output from Kaggle: {kernel_name}...")
        import subprocess
        cmd = [sys.executable, "-m", "kaggle", "kernels", "output", kernel_name, "-p", str(temp_extract)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  Error downloading from Kaggle: {res.stderr}")
            print("  Fallback: Download the results zip from the Kaggle webpage and run:")
            print(f"    python scripts/fetch_kaggle_results.py --zip path/to/results.zip")
            return
        zips = list(temp_extract.glob("*.zip"))
        if zips:
            target_zip = zips[0]
        else:
            target_zip = None

    # Option B: User-supplied ZIP file
    elif zip_path:
        target_zip = Path(zip_path)
        if not target_zip.exists():
            print(f"  Error: File not found: {zip_path}")
            return

    # Extract ZIP
    if target_zip and target_zip.exists():
        print(f"\n[2/3] Extracting {target_zip.name}...")
        with zipfile.ZipFile(target_zip, "r") as z:
            z.extractall(temp_extract)

    # Merge Checkpoints
    print("\n[3/4] Merging checkpoints into results/benchmarks/...")
    imported_ckpts = merge_checkpoints(temp_extract)
    print(f"  Successfully imported/updated {imported_ckpts} model checkpoints!")

    # Merge CSV
    for csv_file in temp_extract.rglob("*master_detailed_benchmark_results*.csv"):
        added_rows = merge_master_csv(csv_file)
        print(f"  Master CSV updated with {added_rows} new records.")
        break

    # Merge Tables & Figures
    print("\n[4/4] Synchronizing LaTeX tables and publication vector figures...")
    tables_src = temp_extract / "papers" / "IEEE_Research_Paper" / "tables"
    if tables_src.exists():
        dst_tab = ROOT / "papers" / "IEEE_Research_Paper" / "tables"
        dst_tab.mkdir(parents=True, exist_ok=True)
        shutil.copytree(tables_src, dst_tab, dirs_exist_ok=True)
        print("  Imported LaTeX tables into papers/IEEE_Research_Paper/tables/")

    figures_src = temp_extract / "papers" / "IEEE_Research_Paper" / "figures"
    if figures_src.exists():
        dst_fig = ROOT / "papers" / "IEEE_Research_Paper" / "figures"
        dst_fig.mkdir(parents=True, exist_ok=True)
        shutil.copytree(figures_src, dst_fig, dirs_exist_ok=True)
        # Also copy to Thesis
        dst_thesis = ROOT / "papers" / "University_CSE_Thesis" / "figures"
        if dst_thesis.exists():
            shutil.copytree(figures_src, dst_thesis, dirs_exist_ok=True)
        print("  Imported 300-DPI publication figures into IEEE and Thesis directories!")

    # Auto-generate latest updated tables from merged CSV
    try:
        from scripts.generate_paper_tables import generate_latex_tables
        generate_latex_tables()
    except Exception as e:
        pass

    # Clean up temp
    if temp_extract.exists():
        shutil.rmtree(temp_extract, ignore_errors=True)

    # Re-generate Live Progress Scorecard
    update_progress_report()

    print("\n" + "=" * 80)
    print(" ALL KAGGLE RESULTS & PAPER ARTIFACTS SUCCESSFULLY INTEGRATED!")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and import benchmark results from Kaggle")
    parser.add_argument("--zip", type=str, default=None, help="Path to downloaded results ZIP file")
    parser.add_argument("--kernel", type=str, default=None, help="Kaggle kernel identifier (e.g. nazmulhasannihal/intelligent-aml-master-benchmark)")
    args = parser.parse_args()

    if not args.zip and not args.kernel:
        # Check default download locations
        default_downloads = Path.home() / "Downloads"
        candidate_zips = list(default_downloads.glob("*intelligent_aml*benchmark*.zip")) + list(default_downloads.glob("*benchmark_results*.zip"))
        if candidate_zips:
            print(f"Found candidate results zip in Downloads: {candidate_zips[0]}")
            import_results(zip_path=str(candidate_zips[0]))
        else:
            parser.print_help()
            print("\nPlease provide either --zip <path_to_zip> or --kernel <kernel_slug>")
    else:
        import_results(zip_path=args.zip, kernel_name=args.kernel)
