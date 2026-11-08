"""
Figure 7.16: Fast-Path vs Full Streaming Latency Comparison
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Sharp rectangular geometry, proper mathtext, strict 4-color palette, readable fonts (>=7.2pt).
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_REVIEW, COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=300)

    modes = ["Fast-Path\n(LRU Cache Hit)", "Full Streaming\n(Deep Spatio-Temp.)", "Tier-1 Banking\nSLA Threshold"]
    lat_vals = [0.45, 2.10, 10.00]
    p99_vals = [0.82, 3.67, 10.00]
    colors_lat = [COLOR_SAFE, COLOR_INGEST, COLOR_RISK]

    bars = ax.bar(modes, lat_vals, color=colors_lat, edgecolor=COLOR_DARK, lw=0.8, width=0.52, alpha=0.92)

    # P99 error bars on first two
    ax.errorbar([0, 1], [0.45, 2.10], yerr=[[0, 0], [0.82 - 0.45, 3.67 - 2.10]],
                fmt='none', ecolor=COLOR_DARK, capsize=4.0, lw=1.4)

    ax.text(0, 0.82 + 0.45, "0.45 ms\n(P99: 0.82 ms)", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=COLOR_SAFE)
    ax.text(1, 3.67 + 0.45, "2.10 ms\n(P99: 3.67 ms)", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=COLOR_INGEST)
    ax.text(2, 10.00 + 0.45, "10.00 ms\n(Max Upper Bound)", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=COLOR_RISK)

    ax.axhline(10.00, color=COLOR_RISK, linestyle=":", lw=1.2, alpha=0.7)
    ax.set_ylabel("Transaction Scoring Latency (ms)", fontsize=8.8, fontweight="bold")
    ax.set_ylim([0, 13.8])
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.set_title("Streaming Transaction Latency vs. Regulatory Banking SLA", fontweight="bold", fontsize=9.6, pad=8)

    plt.tight_layout()
    save_figure(fig, "fig_fastpath_latency_comparison", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
