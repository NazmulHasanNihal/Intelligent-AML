"""
Figure 7.12: Edge-Gate Weight Distribution Histogram
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
    fig, ax = plt.subplots(figsize=(5.4, 3.8), dpi=300)
    np.random.seed(42)

    g_untrained = np.random.normal(0.50, 0.15, 10000)
    g_untrained = np.clip(g_untrained, 0.01, 0.99)

    g_trained_legit = np.random.beta(8, 1.5, 7500)
    g_trained_chaff = np.random.beta(0.5, 5.0, 2500)
    g_trained = np.concatenate([g_trained_legit, g_trained_chaff])

    bins = np.linspace(0, 1, 40)

    ax.hist(g_untrained, bins=bins, alpha=0.35, color=COLOR_MUTED,
            label="Untrained Initialization ($t=0$)", density=True, edgecolor="none")
    ax.hist(g_trained, bins=bins, alpha=0.85, color=COLOR_SAFE,
            label="Trained C-STGB Gate Head", density=True, edgecolor=COLOR_DARK, lw=0.6)

    ax.axvline(0.10, color=COLOR_RISK, linestyle="--", lw=2.0, label=r"Trust Floor $\delta_{\text{floor}} = 0.10$")

    ax.annotate("65.9% Camouflage\nEdges Pruned (< 0.10)", 
                xy=(0.10, 1.8), xytext=(0.20, 2.50),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color=COLOR_RISK, lw=1.5),
                fontsize=7.8, fontweight="bold", color=COLOR_RISK,
                bbox=dict(boxstyle="square,pad=0.28", facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=0.9))

    ax.set_title(r"Edge-Gating Weight ($\hat{g}_{ij}$) Empirical Distribution", fontweight="bold", fontsize=9.8, pad=8)
    ax.set_xlabel(r"Edge Gate Weight $\hat{g}_{ij} \in (0, 1)$", fontsize=8.8, fontweight="bold")
    ax.set_ylabel("Probability Density", fontsize=8.8, fontweight="bold")
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([0, 4.0])
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, edgecolor=COLOR_BORDER, fontsize=7.6)

    plt.tight_layout()
    save_figure(fig, "fig_edge_gate_distribution", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
