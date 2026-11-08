"""
Figure 5.6: Algorithmic Fairness and Non-Discrimination Audit
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    groups = ["Customer Age Tier", "Geographic Region", "Account Tenure", "Retail vs. SME Entity"]
    dp_c_stgb = [0.009, 0.012, 0.007, 0.010]
    eo_c_stgb = [0.006, 0.008, 0.005, 0.007]
    dp_uncal  = [0.068, 0.084, 0.052, 0.071]

    y = np.arange(len(groups))
    h = 0.25

    fig, ax = plt.subplots(figsize=(8.8, 3.8), dpi=300)
    ax.barh(y + h, dp_uncal,  h, label=r"Uncalibrated GNN ($\Delta_{\mathrm{DP}}$)", color="#94A3B8", edgecolor="black")
    ax.barh(y,     dp_c_stgb, h, label=r"C-STGB Class-Cond. CRC ($\Delta_{\mathrm{DP}} \leq 0.012$)", color="#2563EB", edgecolor="black")
    ax.barh(y - h, eo_c_stgb, h, label=r"C-STGB Class-Cond. CRC ($\Delta_{\mathrm{EO}} \leq 0.008$)", color="#15803D", edgecolor="black")

    ax.axvline(0.050, color="#DC2626", linestyle="--", linewidth=2.0, label=r"Statutory Fair-Lending Ceiling ($\epsilon_{\mathrm{fair}} = 0.050$)")
    ax.set_yticks(y)
    ax.set_yticklabels(groups, fontsize=8.5, fontweight="bold")
    ax.set_xlim(0, 0.10)
    ax.set_xlabel("Absolute Disparity Score", fontsize=9.5, fontweight="bold")
    ax.set_title("Algorithmic Fairness & Non-Discrimination Audit (ECOA / Fair Lending Compliance)", fontsize=10.5, fontweight="bold")
    ax.legend(loc="lower right", frameon=True, fontsize=8.0)
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    plt.tight_layout()
    save_figure(fig, "fig_5_7_fairness_audit", pad_inches=0.12)
    plt.close()

# ==============================================================================
# 7. Figure 6.5: SHA-256 Merkle Audit Tree & WORM Verification
# ==============================================================================


if __name__ == "__main__":
    generate()
