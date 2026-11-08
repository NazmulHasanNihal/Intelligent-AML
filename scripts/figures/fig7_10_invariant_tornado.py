"""
Figure 7.10: Factorial Importance Tornado Plot of the 12 Canonical Invariants
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
    inv_features = [
        r"Flow Regularity ($\tilde{\Phi}_{\text{flow}}$)",
        r"Hawkes Burst Intensity ($\lambda_u$)",
        r"Forward Causal Taint ($\mathbf{s}_{\text{fwd}}$)",
        r"Backward Causal Taint ($\mathbf{s}_{\text{bwd}}$)",
        r"Inter-Arrival Dispersion ($\sigma_{\Delta t}$)",
        r"Degree Asymmetry ($\Psi_{\text{asym}}$)",
        r"Amount Velocity ($v_A$)",
        r"In/Out Velocity Ratio ($\nu_{\text{io}}$)",
        r"Amount Mean ($\mu_A$)",
        r"Amount Variance ($\mathrm{Var}(A)$)",
        r"Amount Skewness ($\gamma_A$)",
        r"Amount Kurtosis ($\kappa_A$)"
    ]
    f1_drop_elliptic = [7.46, 2.30, 3.62, 2.52, 2.72, 2.92, 2.22, 1.62, 0.92, 1.32, 0.62, 0.52]
    f1_drop_amlsim   = [7.67, 3.97, 2.67, 2.37, 3.42, 3.27, 2.97, 1.87, 1.27, 1.57, 0.67, 0.57]

    fig, ax = plt.subplots(figsize=(8.8, 4.4), dpi=300)
    y_pos = np.arange(len(inv_features))[::-1]
    height = 0.35

    r1 = ax.barh(y_pos + height/2 + 0.02, f1_drop_elliptic, height,
                 label="Elliptic-v1 (Bitcoin UTXO)", color=COLOR_INGEST, edgecolor=COLOR_DARK, lw=0.7)
    r2 = ax.barh(y_pos - height/2 - 0.02, f1_drop_amlsim,   height,
                 label="IBM-AMLSim HI (Multi-Bank)", color=COLOR_RISK, edgecolor=COLOR_DARK, lw=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(inv_features, fontsize=7.8)
    ax.set_xlabel("F1 Degradation when Feature is Removed (Percentage Points, pp)", fontsize=8.8, fontweight="bold")
    ax.set_xlim([0, 9.5])
    ax.grid(True, axis="x", linestyle=":", alpha=0.5)
    ax.legend(loc="lower right", framealpha=0.92, edgecolor=COLOR_BORDER, fontsize=7.8)
    ax.set_title(r"Factorial Importance Tornado Plot of the 12 Canonical Invariants $\mathbf{z}_{\text{inv}}$",
                 fontweight="bold", fontsize=9.8, pad=8)

    for bar in r1:
        w = bar.get_width()
        ax.annotate(f"-{w:.2f}", (w, bar.get_y() + bar.get_height()/2), xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=6.8, color=COLOR_INGEST, fontweight="bold")
    for bar in r2:
        w = bar.get_width()
        ax.annotate(f"-{w:.2f}", (w, bar.get_y() + bar.get_height()/2), xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=6.8, color=COLOR_RISK, fontweight="bold")

    plt.tight_layout()
    save_figure(fig, "fig_invariant_importance_tornado", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
