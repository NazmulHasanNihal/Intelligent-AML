#!/usr/bin/env python
"""
run_remote.py — Run your IDE code on Kaggle's GPU and pull results back to your PC.

Workflow (you never open kaggle.com):
  1. One-time:  place your Kaggle API token at ~/.kaggle/kaggle.json
                 (or run:  python src/utils/run_remote.py setup)
  2. Write your code as a .py script (e.g. src/ingestion/pipeline.py + a runner),
     or point this at a notebook.
  3. Run:  python src/utils/run_remote.py run --target notebooks/Layer1_Ingestion/01_Layer1_Data_Ingestion_v4.ipynb
     -> pushes to Kaggle, executes on a free T4/P100, then downloads
        graph_data/ + _manifest.json into data/outputs/ on THIS machine.

How it works under the hood:
  - Kaggle "notebooks" (kernels) can be pushed via the Kaggle API and run headless.
  - We wrap your .py into a notebook cell, OR push an .ipynb directly.
  - After the run finishes we `kaggle kernels output` the artifacts to data/outputs/.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

# Force Python UTF-8 mode globally for subprocesses (prevents Windows CP1252 charmap decode errors)
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

if hasattr(sys, 'stdout') and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "outputs"
KAGGLE_DIR = Path.home() / ".kaggle"


def _kaggle_cli() -> str:
    """Return a command that invokes the Kaggle CLI (prefer venv, fall back to PATH)."""
    venv_kaggle = REPO_ROOT / "venv" / "Scripts" / "kaggle.exe"
    if venv_kaggle.exists():
        return str(venv_kaggle)
    return "kaggle"


def ensure_auth() -> bool:
    """Verify kaggle.json or access_token exists and set KAGGLE_API_TOKEN in environment."""
    kf = KAGGLE_DIR / "kaggle.json"
    at = KAGGLE_DIR / "access_token"
    if not kf.exists() and not at.exists():
        print("❌ Kaggle authentication token not found at ~/.kaggle/access_token or ~/.kaggle/kaggle.json")
        print("   Fix: generate an API token at https://www.kaggle.com/settings")
        print("   and place it at:", at)
        return False

    token = None
    if at.exists():
        token = at.read_text(encoding="utf-8").strip()
    elif kf.exists():
        try:
            data = json.loads(kf.read_text(encoding="utf-8"))
            token = data.get("key")
        except Exception:
            pass

    if token:
        os.environ["KAGGLE_API_TOKEN"] = token

    for path in (kf, at):
        if path.exists():
            try:
                os.chmod(path, 0o600)
            except OSError:
                pass  # Windows: chmod is a no-op
    return True


def _kernel_slug(competition_or_user: str, title: str) -> str:
    return f"{competition_or_user}/{title}"


def push_and_run(nb_path: Path, slug: str, datasets: list[str] | None, gpu: bool, cpu_or_gpu: str):
    """Push a notebook to Kaggle and trigger a run."""
    cli = _kaggle_cli()
    # If a .py was given, wrap it into a minimal notebook first.
    if nb_path.suffix == ".py":
        nb_path = _wrap_py_to_ipynb(nb_path)

    # Warn if the notebook has been patched for local use (contains kagglehub
    # references that would try to download datasets on Kaggle where they're
    # already mounted at /kaggle/input/).
    try:
        nb_content = json.loads(nb_path.read_text(encoding="utf-8"))
        for cell in nb_content.get("cells", []):
            if cell.get("cell_type") == "code":
                src = "".join(cell.get("source", []))
                if "kagglehub" in src and "/kaggle/input/" not in src:
                    print("⚠️  WARNING: This notebook appears to be patched for local use")
                    print("   (contains kagglehub download calls). On Kaggle, datasets are")
                    print("   already mounted at /kaggle/input/ — downloading them is unnecessary")
                    print("   and will waste time. Push the original notebook instead.")
                    print("   To revert: git checkout HEAD -- " + str(nb_path))
                    break
    except Exception:
        pass

    # Build kernel metadata JSON for kaggle kernels push
    meta = nb_path.parent / "kernel-metadata.json"
    _write_metadata(meta, slug, nb_path, datasets, gpu)

    print(f"📤 Pushing {nb_path.name} to Kaggle as '{slug}' ...")
    subprocess.run([cli, "kernels", "push", "-p", str(nb_path.parent)], check=True)
    print(f"🚀 Started run on Kaggle ({cpu_or_gpu}) ...")
    return nb_path


def _wrap_py_to_ipynb(py_path: Path) -> Path:
    """Convert a .py file into a single-cell .ipynb next to it (Kaggle runs notebooks)."""
    code = py_path.read_text(encoding="utf-8")
    nb = {
        "cells": [{"cell_type": "code", "execution_count": None,
                   "metadata": {}, "outputs": [], "source": code.splitlines(keepends=True)}],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5,
    }
    out = py_path.with_suffix(".ipynb")
    out.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"  wrapped .py -> {out.name}")
    return out


def _slugify(text: str) -> str:
    import re
    return re.sub(r'[^a-z0-9-]+', '-', text.lower()).strip('-')


DEFAULT_AML_DATASET_SOURCES = [
    "nazmulhasannihal/aml-dataset",
    "ealtman2019/ibm-transactions-for-anti-money-laundering-aml",
    "berkanoztas/synthetic-transaction-monitoring-dataset-aml",
    "ellipticco/elliptic2-data-set",
    "tczplv/xblocketh",
]


def _write_metadata(meta: Path, slug: str, nb_path: Path, datasets, gpu: bool):
    user, title = slug.split("/", 1)
    clean_slug = f"{user}/{_slugify(title)}"
    ds_sources = datasets if datasets else DEFAULT_AML_DATASET_SOURCES
    payload = {
        "id": clean_slug,
        "title": title,
        "code_file": nb_path.name,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": gpu,
        "enable_internet": True,
        "dataset_sources": ds_sources,
        "competition_sources": [],
        "kernel_sources": [],
    }
    meta.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def wait_for_completion(slug: str, timeout_min: int = 60):
    """Poll kernel status until 'complete' or timeout. Prints live status."""
    cli = _kaggle_cli()
    deadline = time.time() + timeout_min * 60
    while time.time() < deadline:
        res = subprocess.run([cli, "kernels", "status", slug],
                             capture_output=True, text=True)
        out = res.stdout + res.stderr
        last_line = out.strip().splitlines()[-1] if out.strip() else 'running'
        print(f"  … {last_line}")
        lower = out.lower()
        if "complete" in lower or "finished" in lower:
            return True
        if "error" in lower or "failed" in lower or "cancelled" in lower:
            print("❌ Kernel run failed. Check logs: kaggle kernels logs", slug)
            return False
        time.sleep(30)
    print("⏱️  Timed out waiting. Check: kaggle kernels status", slug)
    return False


def pull_outputs(slug: str):
    """Download the kernel's output artifacts into data/outputs/ on this PC."""
    cli = _kaggle_cli()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = REPO_ROOT / ".kaggle_pull_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    result = subprocess.run([cli, "kernels", "output", slug, "-p", str(tmp)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️  Kaggle output download failed:", result.stderr.strip())
        return
    # List what Kaggle returned
    if tmp.exists():
        items = list(tmp.iterdir())
        print("  Kaggle output contains: " + str([i.name for i in items]))
    else:
        print("  ⚠️  Kaggle output directory is empty or missing")
        return
    # Move graph_data/ and _manifest.json if present
    moved = 0
    for item in tmp.iterdir():
        if item.name in ("graph_data", "_manifest.json"):
            dest = OUTPUT_DIR / item.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.move(str(item), str(dest))
            moved += 1
    shutil.rmtree(tmp, ignore_errors=True)
    if moved:
        print("✅ Pulled " + str(moved) + " artifact(s) into " + str(OUTPUT_DIR))
    else:
        print("⚠️  No graph_data or _manifest.json found in Kaggle output.")


def cmd_setup(args):
    if ensure_auth():
        print("✅ kaggle.json found and secured.")
    else:
        print("Waiting for you to add ~/.kaggle/kaggle.json, then re-run 'setup'.")


def cmd_run(args):
    nb_path = (REPO_ROOT / args.target).resolve()
    if not nb_path.exists():
        print(f"❌ Target not found: {nb_path}")
        sys.exit(1)

    if args.local:
        print("\n" + "=" * 70)
        print(" 🚀 EXECUTING INGESTION PIPELINE LOCALLY (LIVE TERMINAL OUTPUT)")
        print("=" * 70)
        import sys as _sys
        _sys.path.insert(0, str(REPO_ROOT))
        from src.ingestion import pipeline as P
        P.run_all_datasets()
        P.split_all_datasets()
        P.write_run_manifest(P.OUTPUT_DIR)
        print("\n✅ Local Ingestion Execution Completed. Output:", P.OUTPUT_DIR.resolve())
        return

    if not ensure_auth():
        sys.exit(1)
    raw_slug = args.slug or f"nazmulhasannihal/{nb_path.stem}-remote"
    user, title = raw_slug.split("/", 1)
    slug = f"{user}/{_slugify(title)}"
    gpu = args.gpu
    push_and_run(nb_path, slug, args.dataset, gpu, "GPU" if gpu else "CPU")
    if wait_for_completion(slug, timeout_min=args.timeout):
        pull_outputs(slug)
    else:
        print("Run did not complete cleanly; outputs not pulled.")


def main():
    ap = argparse.ArgumentParser(description="Run IDE code on Kaggle or locally.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("setup", help="Verify Kaggle credentials").set_defaults(func=cmd_setup)

    runp = sub.add_parser("run", help="Run a notebook/script on Kaggle or locally")
    runp.add_argument("--target", required=True, help="Path (relative to repo root) to .ipynb or .py")
    runp.add_argument("--local", action="store_true", help="Run locally on your PC instead of remote Kaggle GPU")
    runp.add_argument("--slug", default=None, help="Kaggle kernel slug (user/title)")
    runp.add_argument("--dataset", action="append", default=[],
                      help="Dataset to attach, e.g. nazmulhasannihal/aml-dataset (repeatable)")
    runp.add_argument("--gpu", action="store_true", default=True, help="Use GPU (default on)")
    runp.add_argument("--cpu", dest="gpu", action="store_false", help="Use CPU instead")
    runp.add_argument("--timeout", type=int, default=60, help="Minutes to wait for completion")
    runp.set_defaults(func=cmd_run)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
