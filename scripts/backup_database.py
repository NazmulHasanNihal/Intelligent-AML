#!/usr/bin/env python3
"""
scripts/backup_database.py
Institutional Backup Utility for Intelligent-AML Databases and WORM Checkpoints.
Creates a timestamped, compressed tarball with SHA-256 cryptographic manifest.
"""

import os
import sys
import time
import tarfile
import hashlib
from pathlib import Path

BACKUP_DIR = Path("results/backups")
DB_FILES = [
    Path("results/intelligent_aml.db"),
    Path("results/audit_ledger.db"),
    Path("results/metrics/conformal_calibration.json")
]
CHECKPOINT_DIR = Path("results/audit_checkpoints")


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def create_backup() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    archive_name = f"aml_backup_{timestamp}.tar.gz"
    archive_path = BACKUP_DIR / archive_name

    print(f"[*] Initializing Intelligent-AML Database Backup: {archive_name}")
    t0 = time.perf_counter()

    with tarfile.open(archive_path, "w:gz") as tar:
        for db in DB_FILES:
            if db.exists():
                tar.add(db, arcname=db.name)
                print(f"  + Added database file: {db}")

        if CHECKPOINT_DIR.exists():
            tar.add(CHECKPOINT_DIR, arcname="audit_checkpoints")
            print(f"  + Added WORM checkpoints directory: {CHECKPOINT_DIR}")

    elapsed = time.perf_counter() - t0
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    sha256 = compute_sha256(archive_path)

    # Write manifest
    manifest_path = archive_path.with_suffix(".tar.gz.manifest")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"Archive: {archive_name}\n")
        f.write(f"Timestamp: {timestamp} UTC\n")
        f.write(f"Size_MB: {size_mb:.4f}\n")
        f.write(f"Duration_sec: {elapsed:.3f}\n")
        f.write(f"SHA256: {sha256}\n")

    print(f"[✓] Backup Completed in {elapsed:.3f}s ({size_mb:.2f} MB)")
    print(f"    SHA-256: {sha256}")
    print(f"    Manifest: {manifest_path}")
    return archive_path


if __name__ == "__main__":
    create_backup()
