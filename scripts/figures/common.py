"""
scripts/figures/common.py
Universal publication-grade configuration, styling, and multi-directory export handler
for all thesis figures in C-STGB dissertation.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Ensure standard UTF-8 stream handling on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Master Strict 4-Color Palette (Publication Standard)
COLOR_INGEST = "#1E40AF"        # Blue: Ingestion / Data Processing
COLOR_INGEST_LIGHT = "#DBEAFE"
COLOR_INGEST_BG = "#EFF6FF"

COLOR_GNN = "#0F766E"           # Teal: Neural Network / GNN Core
COLOR_GNN_PURPLE = "#6D28D9"    # Deep Purple accent for embeddings
COLOR_GNN_LIGHT = "#CCFBF1"
COLOR_GNN_BG = "#F0FDFA"

COLOR_SAFE = "#15803D"          # Green: Safe / Cleared (Straight-Through STP)
COLOR_SAFE_LIGHT = "#DCFCE7"
COLOR_SAFE_BG = "#F0FDF4"

COLOR_RISK = "#B91C1C"          # Red: High-Risk / Quarantine / Auto-SAR
COLOR_RISK_LIGHT = "#FEE2E2"
COLOR_RISK_BG = "#FEF2F2"

COLOR_REVIEW = "#C2410C"        # Orange: Human Review Desk / Tier 2 Triage
COLOR_REVIEW_LIGHT = "#FFEDD5"
COLOR_REVIEW_BG = "#FFFBEB"

COLOR_DARK = "#0F172A"          # Slate 900: Primary labels and borders
COLOR_MUTED = "#64748B"         # Slate 500: Secondary text / subtitles
COLOR_BORDER = "#94A3B8"        # Slate 400: Neutral card/box outlines

TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "reports" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
]

def setup_plt(font_size=8.5, title_size=9.8, label_size=9.0):
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica', 'Liberation Sans'],
        'font.size': font_size,
        'axes.labelsize': label_size,
        'axes.titlesize': title_size,
        'xtick.labelsize': font_size - 1.0,
        'ytick.labelsize': font_size - 1.0,
        'legend.fontsize': font_size - 1.0,
        'figure.titlesize': title_size + 1.0,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'mathtext.fontset': 'stix',
        'axes.linewidth': 0.8,
        'grid.linewidth': 0.5,
        'grid.linestyle': ':',
        'grid.alpha': 0.6,
    })

def save_figure(fig, basename, pad_inches=0.10):
    """
    Saves figure in both .pdf and .png format across all 5 figure repositories.
    """
    saved_paths = []
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in [".pdf", ".png"]:
            out_path = d / f"{basename}{ext}"
            fig.savefig(out_path, bbox_inches="tight", pad_inches=pad_inches, dpi=300)
            saved_paths.append(out_path)
    print(f"Successfully saved {basename}.pdf & .png across {len(TARGET_DIRS)} directories.")
    return saved_paths

