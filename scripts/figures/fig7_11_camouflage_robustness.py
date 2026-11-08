"""
Figure 7.11: Adversarial Camouflage Link Robustness
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

    noise_ratios = np.array([0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80])
    f1_cstgb     = np.array([91.42, 91.39, 91.31, 90.97, 90.41, 89.63, 88.20, 86.40, 84.20])
    f1_care      = np.array([64.50, 62.10, 58.40, 52.10, 46.50, 40.20, 35.10, 30.50, 26.20])
    f1_hgt       = np.array([48.20, 44.10, 39.80, 34.50, 28.70, 23.20, 18.10, 13.50,  9.80])
    f1_graphsage = np.array([49.07, 44.50, 38.20, 30.10, 22.40, 16.50, 11.20,  7.80,  4.80])
    f1_gcn       = np.array([43.55, 38.20, 31.40, 24.50, 18.20, 12.80,  8.40,  5.20,  3.10])

    ax.plot(noise_ratios * 100, f1_cstgb, label="C-STGB (Edge-Gated)", color=COLOR_SAFE, lw=2.4, marker="o", markersize=4.0)
    ax.plot(noise_ratios * 100, f1_care, label="CARE-GNN (RL Filter)", color=COLOR_INGEST, lw=1.6, marker="s", markersize=3.8, ls="--")
    ax.plot(noise_ratios * 100, f1_hgt, label="Vanilla HGT", color=COLOR_GNN, lw=1.5, marker="^", markersize=3.8, ls="-.")
    ax.plot(noise_ratios * 100, f1_graphsage, label="GraphSAGE", color=COLOR_MUTED, lw=1.5, marker="D", markersize=3.5, ls=":")
    ax.plot(noise_ratios * 100, f1_gcn, label="GCN (Weber 2019)", color=COLOR_RISK, lw=1.5, marker="x", markersize=4.0, ls=":")

    ax.set_title("Adversarial Camouflage Link Robustness", fontweight="bold", fontsize=9.8, pad=8)
    ax.set_xlabel("Injected Camouflage Link Ratio (%)", fontsize=8.8, fontweight="bold")
    ax.set_ylabel("Macro F1-Score (%)", fontsize=8.8, fontweight="bold")
    ax.set_xlim([-2, 82])
    ax.set_ylim([0, 105])
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="lower left", framealpha=0.92, edgecolor=COLOR_BORDER,
              fontsize=7.4, handlelength=1.2, handletextpad=0.30, borderpad=0.30)

    plt.tight_layout()
    save_figure(fig, "fig9_adversarial_camouflage_robustness", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
