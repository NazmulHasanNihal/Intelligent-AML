#!/usr/bin/env python
"""
download_datasets.py
--------------------
Utility script to download benchmark AML datasets directly from Kaggle
into the Kaggle notebook environment or local data/raw/ directory.

Usage (local):
    python scripts/download_datasets.py --local

Usage (inside Kaggle):
    Datasets are attached via the Kaggle UI, this script is not needed.
"""
import argparse
import subprocess
import sys
from pathlib import Path


DATASETS = {
    "elliptic_bitcoin": "ellipticco/elliptic-data-set",
    "paysim":           "ealaxi/paysim1",
    "ibm_amlsim":       "ealtman2019/ibm-transactions-for-anti-money-laundering-aml",
}


def download(dataset_slug: str, output_dir: Path):
    """Download and unzip a Kaggle dataset."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "kaggle", "datasets", "download",
        "-d", dataset_slug,
        "-p", str(output_dir),
        "--unzip",
    ]
    print(f"Downloading {dataset_slug} → {output_dir}")
    subprocess.run(cmd, check=True)
    print("Done.\n")


def main():
    parser = argparse.ArgumentParser(description="Download AML benchmark datasets from Kaggle")
    parser.add_argument("--local", action="store_true", help="Download to local data/raw/ directory")
    parser.add_argument("--dataset", choices=list(DATASETS.keys()), default=None,
                        help="Download a specific dataset (default: all)")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    output = base / "data" / "raw" if args.local else Path("/kaggle/input")

    targets = {args.dataset: DATASETS[args.dataset]} if args.dataset else DATASETS

    for name, slug in targets.items():
        download(slug, output / name)

    print("All downloads complete.")


if __name__ == "__main__":
    main()
