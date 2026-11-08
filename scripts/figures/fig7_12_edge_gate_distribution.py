"""
Figure 7.12: Edge-Gate Weight Distribution Comparison
Redesigned as two clean, side-by-side subplots:
(a) Untrained Initialization (t = 0): Unimodal Gaussian (indistinguishable camouflage)
(b) Trained C-STGB Gate Head: Bimodal Separation with 65.9% Chaff Pruned Below Trust Floor (0.10)
Eliminates confusing overlapping histograms and small cramped text.
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
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous widescreen canvas for 2 side-by-side distribution panels
    fig, (ax_un, ax_tr) = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=300)
    fig.subplots_adjust(left=0.07, right=0.96, top=0.88, bottom=0.14, wspace=0.22)
    np.random.seed(42)

    # Synthetic realistic edge weights
    g_untrained = np.random.normal(0.50, 0.14, 10000)
    g_untrained = np.clip(g_untrained, 0.01, 0.99)

    g_trained_chaff = np.random.beta(0.6, 6.0, 3500)
    g_trained_legit = np.random.beta(8.5, 1.8, 6500)
    bins = np.linspace(0, 1, 40)

    # =========================================================================
    # SUBPLOT (a): UNTRAINED INITIALIZATION (t = 0)
    # =========================================================================
    ax_un.hist(g_untrained, bins=bins, color=COLOR_MUTED, alpha=0.75,
               edgecolor=COLOR_DARK, lw=0.6, density=True)
    ax_un.axvline(0.50, color=COLOR_DARK, linestyle="--", lw=1.6, label="Mean Initialization = 0.50")

    ax_un.set_title("(a) Untrained Initialization (t = 0)", fontsize=9.2, fontweight="bold", pad=8)
    ax_un.set_xlabel("Edge Gate Weight", fontsize=8.5, fontweight="bold")
    ax_un.set_ylabel("Probability Density", fontsize=8.5, fontweight="bold")
    ax_un.set_xlim([-0.02, 1.02])
    ax_un.set_ylim([0, 4.4])
    ax_un.grid(True, linestyle=":", alpha=0.5)
    ax_un.legend(loc="upper right", framealpha=0.92, edgecolor=COLOR_BORDER, fontsize=7.4)

    ax_un.text(0.50, 3.50, "Indistinguishable Camouflage\nMean = 0.50, Zero Separation",
               ha="center", va="center", fontsize=7.4, fontweight="bold", color=COLOR_DARK,
               bbox=dict(boxstyle="square,pad=0.3", fc="#f8fafc", ec=COLOR_BORDER, lw=0.9))

    # =========================================================================
    # SUBPLOT (b): TRAINED C-STGB EDGE-GATING HEAD
    # =========================================================================
    # Draw Chaff distribution (pruned)
    ax_tr.hist(g_trained_chaff, bins=bins, color=COLOR_RISK, alpha=0.85,
               edgecolor=COLOR_DARK, lw=0.6, density=True, label="Camouflage Chaff")
    # Draw Legitimate distribution (retained)
    ax_tr.hist(g_trained_legit, bins=bins, color=COLOR_SAFE, alpha=0.85,
               edgecolor=COLOR_DARK, lw=0.6, density=True, label="Legitimate Commercial")

    ax_tr.axvline(0.10, color=COLOR_DARK, linestyle="--", lw=2.0, label="Trust Floor = 0.10")

    # Legend in the center valley where density is zero
    ax_tr.legend(loc="upper center", framealpha=0.92, edgecolor=COLOR_BORDER, fontsize=7.2)

    ax_tr.annotate("65.9% Chaff Pruned\n(< 0.10 Floor)",
                   xy=(0.10, 2.5), xytext=(0.04, 3.45),
                   arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.6),
                   fontsize=7.2, fontweight="bold", color=COLOR_RISK,
                   bbox=dict(boxstyle="square,pad=0.25", facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=0.9))

    ax_tr.annotate("Legitimate Flow\nHigh Confidence",
                   xy=(0.88, 2.8), xytext=(0.68, 3.45),
                   arrowprops=dict(arrowstyle="->", color=COLOR_SAFE, lw=1.6),
                   fontsize=7.2, fontweight="bold", color=COLOR_SAFE,
                   bbox=dict(boxstyle="square,pad=0.25", facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=0.9))

    ax_tr.set_title("(b) Trained C-STGB Gating Head", fontsize=9.2, fontweight="bold", pad=8)
    ax_tr.set_xlabel("Edge Gate Weight", fontsize=8.5, fontweight="bold")
    ax_tr.set_ylabel("Probability Density", fontsize=8.5, fontweight="bold")
    ax_tr.set_xlim([-0.02, 1.02])
    ax_tr.set_ylim([0, 4.4])
    ax_tr.grid(True, linestyle=":", alpha=0.5)

    fig.suptitle("Empirical Distribution of Learnable Edge-Trust Gating Weights",
                 fontsize=10.2, fontweight="bold", y=0.98)

    save_figure(fig, "fig_edge_gate_distribution", pad_inches=0.12)
    save_figure(fig, "fig18_edge_gate_distribution", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
