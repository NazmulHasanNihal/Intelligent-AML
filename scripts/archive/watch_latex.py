"""Continuous LaTeX Watcher, Linter, and Compiler for Intelligent-AML.

Watches IEEE_Research_Paper and University_CSE_Thesis for real-time
integrity checking, auto-compilation to PDF via Tectonic, and automated
Overleaf ZIP archive packaging.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils.latex_validator import LaTeXProjectValidator

TECTONIC_EXE = BASE_DIR / "tools" / "tectonic" / "tectonic.exe"

PROJECTS = {
    "IEEE_Research_Paper": {
        "name": "IEEE Transactions Research Paper",
        "dir": BASE_DIR / "IEEE_Research_Paper",
        "main": BASE_DIR / "IEEE_Research_Paper" / "main.tex",
        "zip": BASE_DIR / "IEEE_Research_Paper.zip",
        "pdf": BASE_DIR / "IEEE_Research_Paper" / "main.pdf",
    },
    "University_CSE_Thesis": {
        "name": "University CSE Thesis",
        "dir": BASE_DIR / "University_CSE_Thesis",
        "main": BASE_DIR / "University_CSE_Thesis" / "main.tex",
        "zip": BASE_DIR / "University_CSE_Thesis.zip",
        "pdf": BASE_DIR / "University_CSE_Thesis" / "main.pdf",
    },
}


def zip_directory(src_dir: Path, target_zip: Path):
    """Packages project directory into a clean, ready-to-upload Overleaf ZIP."""
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for file in files:
                # Exclude intermediate build files from zip
                if file.endswith(
                    (
                        ".aux",
                        ".log",
                        ".out",
                        ".toc",
                        ".bbl",
                        ".blg",
                        ".synctex.gz",
                    )
                ):
                    continue
                file_path = Path(root) / file
                rel_path = file_path.relative_to(src_dir)
                zf.write(file_path, arcname=str(rel_path))


def run_pipeline(project_key: str = None, compile_pdf: bool = True):
    """Runs verification, compilation, and packaging for one or all projects."""
    keys = [project_key] if project_key else list(PROJECTS.keys())
    print("\n" + "=" * 78)
    print("  ANTIGRAVITY IN-IDE CONTINUOUS LATEX COMPILER & AUDIT")
    print("=" * 78)

    all_clean = True

    for k in keys:
        cfg = PROJECTS[k]
        pdir = cfg["dir"]
        print(f"\n🔍 [AUDIT] Checking: {cfg['name']} ({k})")

        # 1. Real-time Lint & Semantic Integrity Audit
        validator = LaTeXProjectValidator(pdir)
        is_valid, errors, warnings = validator.validate()

        if not is_valid:
            all_clean = False
            print(f"❌ Syntax / Citation / Figure Errors Found in {k}:")
            for err in errors:
                print(f"   • [ERROR] {err}")
            for warn in warnings:
                print(f"   • [WARN] {warn}")
            print(f"⚠️ Skipping compilation for {k} until errors are resolved.")
            continue

        print(
            "   ✅ Integrity Audit Passed (0 syntax errors, 0 missing bibtex, 0 broken figures)"
        )

        # 2. Local Fast Compilation via Tectonic
        if compile_pdf and TECTONIC_EXE.exists():
            print(f"   ⚡ Compiling PDF using Tectonic -> {cfg['pdf'].name}...")
            start_t = time.time()
            res = subprocess.run(
                [
                    str(TECTONIC_EXE),
                    "--keep-intermediates",
                    str(cfg["main"]),
                    "--outdir",
                    str(pdir),
                ],
                capture_output=True,
                text=True,
            )
            elapsed = time.time() - start_t
            if res.returncode == 0:
                print(
                    f"   🎉 Build Success! PDF generated in {elapsed:.2f}s: {cfg['pdf']}"
                )
            else:
                print(f"   ⚠️ Compilation Warning/Error ({elapsed:.2f}s):")
                err_lines = [
                    l
                    for l in res.stderr.splitlines()
                    if "error" in l.lower() or "warning" in l.lower()
                ]
                for l in err_lines[:5]:
                    print(f"      {l}")

        # 3. Synchronize Overleaf ZIP package
        zip_directory(pdir, cfg["zip"])
        print(f"   📦 Updated Overleaf Bundle: {cfg['zip'].name}")

    print("\n" + "=" * 78)
    return all_clean


def get_file_mtimes():
    """Returns mapping of relative path to modification time."""
    mtimes = {}
    for k, cfg in PROJECTS.items():
        for f in cfg["dir"].rglob("*"):
            if f.suffix in [".tex", ".bib", ".sty", ".cls", ".png", ".pdf"]:
                mtimes[f] = f.stat().st_mtime
    return mtimes


def watch_loop(poll_interval: float = 1.0):
    """Continuously watches for file modifications and triggers pipeline."""
    print("🚀 [WATCH MODE] Antigravity IDE Continuous LaTeX Monitor Active.")
    print("📝 Watching .tex, .bib, and figures in:")
    for k, cfg in PROJECTS.items():
        print(f"   - {cfg['dir']}")
    print("\n💡 Save any file in your IDE to auto-audit, compile PDF, and sync Overleaf zip.\n")

    # Initial run
    run_pipeline(compile_pdf=True)

    last_mtimes = get_file_mtimes()

    try:
        while True:
            time.sleep(poll_interval)
            current_mtimes = get_file_mtimes()
            modified = []
            for f, mtime in current_mtimes.items():
                if f not in last_mtimes or mtime > last_mtimes[f]:
                    modified.append(f)

            if modified:
                print(f"\n🔄 Detected change in: {[f.name for f in modified]}")
                run_pipeline(compile_pdf=True)
                last_mtimes = current_mtimes
    except KeyboardInterrupt:
        print("\n⏹️ Stopped watching.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="In-IDE Continuous LaTeX Watcher & Compiler"
    )
    parser.add_argument(
        "--once", action="store_true", help="Run once and exit without watching"
    )
    parser.add_argument(
        "--project",
        choices=["IEEE_Research_Paper", "University_CSE_Thesis"],
        help="Specify single project",
    )
    args = parser.parse_args()

    if args.once:
        run_pipeline(project_key=args.project, compile_pdf=True)
    else:
        watch_loop()
