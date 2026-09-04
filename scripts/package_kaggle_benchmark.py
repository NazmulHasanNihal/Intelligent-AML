#!/usr/bin/env python3
"""
package_kaggle_benchmark.py
===========================
Prepares and packages the Intelligent-AML benchmark payload for Kaggle.

Features:
1. Gathers the 13 canonical paper datasets from data/outputs/graph_data/.
2. Bundles the existing 77 checkpoints from results/benchmarks/ so Kaggle
   resumes seamlessly and does not duplicate work.
3. Packages core source code (src/, comparing_models/, scripts/, configs/).
4. Outputs a zip file: data/kaggle_benchmark_payload.zip
5. Optionally uploads the dataset directly to Kaggle via the Kaggle API.

Usage:
    python scripts/package_kaggle_benchmark.py
    python scripts/package_kaggle_benchmark.py --upload
"""

import sys
import os
import json
import zipfile
import shutil
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 16 Target Benchmark Datasets (All datasets in Paper Table 2 + Medium Imbalance Benchmarks)
TARGET_DATASETS = [
    "elliptic_v1",
    "elliptic_v2",
    "ibm_amlsim_hi_small",
    "ibm_amlsim_li_small",
    "ibm_amlsim_hi_medium",
    "ibm_amlsim_li_medium",
    "mtgox_leaked",
    "saml_d",
    "paysim1",
    "eth_phishing",
    "xblock_eth",
    "cc_transactions",
    "data_generator",
    "dgraphfin",
    "smart_ponzi",
    "synthaml"
]


def create_kaggle_dataset_metadata(dest_dir: Path, title: str = "Intelligent AML Benchmark Payload"):
    """Generates dataset-metadata.json required by Kaggle CLI."""
    meta = {
        "title": title,
        "id": "nazmulhasannihal/intelligent-aml-benchmark-data",
        "licenses": [{"name": "CC0-1.0"}]
    }
    with open(dest_dir / "dataset-metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def package_benchmark(upload: bool = False):
    print("=" * 80)
    print(" INTELLIGENT-AML: PACKAGING BENCHMARK PAYLOAD FOR KAGGLE")
    print("=" * 80)

    payload_dir = ROOT / "data" / "kaggle_payload"
    if payload_dir.exists():
        shutil.rmtree(payload_dir)
    payload_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy Benchmark Datasets (parquet files)
    print("\n[1/4] Copying 13 target graph datasets...")
    graph_data_src = ROOT / "data" / "outputs" / "graph_data"
    graph_data_dst = payload_dir / "graph_data"
    graph_data_dst.mkdir(parents=True, exist_ok=True)

    total_bytes = 0
    for ds in TARGET_DATASETS:
        src = graph_data_src / ds
        if not src.exists():
            print(f"  [Warning] Dataset '{ds}' not found in {graph_data_src}")
            continue
        dst = graph_data_dst / ds
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*.parquet"):
            shutil.copy2(f, dst / f.name)
            sz = f.stat().st_size
            total_bytes += sz
        print(f"  -> Included '{ds}'")

    print(f"  Total dataset size: {total_bytes / (1024 * 1024):.2f} MB")

    # 2. Copy Existing Checkpoints (77 completed model runs)
    print("\n[2/4] Bundling existing checkpoints (safe resumption guard)...")
    checkpoints_dst = payload_dir / "benchmarks"
    checkpoints_dst.mkdir(parents=True, exist_ok=True)

    benchmarks_src = ROOT / "results" / "benchmarks"
    ckpt_count = 0
    if benchmarks_src.exists():
        for ds in TARGET_DATASETS:
            ds_src = benchmarks_src / ds
            if ds_src.exists():
                ds_dst = checkpoints_dst / ds
                shutil.copytree(ds_src, ds_dst, dirs_exist_ok=True)
                for _ in ds_dst.rglob("*.json"):
                    ckpt_count += 1

    print(f"  Successfully bundled {ckpt_count} existing model checkpoints.")

    # 3. Copy Codebase (src, comparing_models, scripts, configs) for 100% self-contained execution
    print("\n[3/5] Bundling codebase (src, comparing_models, scripts, configs)...")
    code_dst = payload_dir / "code"
    for item in ["src", "comparing_models", "scripts", "configs", "notebooks"]:
        src_item = ROOT / item
        if src_item.exists():
            shutil.copytree(src_item, code_dst / item, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            print(f"  -> Included code module: {item}/")

    # 4. Create kaggle metadata
    create_kaggle_dataset_metadata(payload_dir)

    # 5. Create single archive for easy download/upload
    print("\n[4/5] Compressing into data/kaggle_benchmark_payload.zip...")
    zip_path = ROOT / "data" / "kaggle_benchmark_payload.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(payload_dir):
            for file in files:
                abs_f = Path(root) / file
                rel_f = abs_f.relative_to(payload_dir)
                zipf.write(abs_f, rel_f)

    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  Created: {zip_path} ({zip_size_mb:.2f} MB)")

    # 5. Optional Direct Kaggle Upload
    if upload:
        print("\n[4/4] Uploading dataset to Kaggle via Kaggle CLI...")
        try:
            import subprocess
            cmd = [sys.executable, "-m", "kaggle", "datasets", "create", "-p", str(payload_dir), "-u"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("  Dataset successfully created/updated on Kaggle!")
                print("  URL: https://www.kaggle.com/datasets/nazmulhasannihal/intelligent-aml-benchmark-data")
            else:
                print(f"  Kaggle CLI note: {result.stdout.strip()} {result.stderr.strip()}")
                print("  (You can also upload data/kaggle_benchmark_payload.zip manually via Kaggle Web UI)")
        except Exception as e:
            print(f"  Could not run automated upload: {e}")
    else:
        print("\n[4/4] To upload directly using Kaggle API:")
        print("  python scripts/package_kaggle_benchmark.py --upload")
        print("  Or upload 'data/kaggle_benchmark_payload.zip' directly to Kaggle Web UI.")

    print("\n" + "=" * 80)
    print(" PACKAGING COMPLETE! Ready for Kaggle execution.")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Intelligent-AML Benchmark for Kaggle")
    parser.add_argument("--upload", action="store_true", help="Upload dataset directly to Kaggle via Kaggle API")
    args = parser.parse_args()
    package_benchmark(upload=args.upload)
