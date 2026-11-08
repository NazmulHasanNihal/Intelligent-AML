"""
Figure 7.7: Stepwise Architectural Ablation across Three Benchmark Datasets
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    steps = [
        r"(1a) GCN Raw" "\n" r"($\tau=0.50$)",
        r"(1b) +Bayes $\tau^*$" "\n" r"(Cost Opt)",
        r"(2) +12-D Space" "\n" r"($\mathbf{z}_{\mathrm{inv}}$)",
        r"(3) +Tri-Band" "\n" r"($w(\Delta t)$)",
        r"(4) +Edge Gate" "\n" r"($\hat{g}_{ij} \geq 0.10$)",
        r"(5) +SMOTE" "\n" r"(Typology)",
        r"(6) +Fusion" "\n" r"($\mathbf{h}_u^*$)",
        r"(7) Full C-STGB" "\n" r"(End-to-End)"
    ]

    elliptic = [10.33, 26.40, 54.80, 68.50, 76.20, 86.12, 89.80, 91.42]
    samld    = [6.20,  18.50, 46.20, 61.40, 71.80, 81.50, 89.80, 93.68]
    amlsim   = [2.10,   6.80, 18.40, 26.50, 32.40, 39.80, 43.20, 46.85]

    x = np.arange(len(steps))
    w = 0.26

    fig, ax = plt.subplots(figsize=(11.5, 4.6), dpi=300)
    b1 = ax.bar(x - w, elliptic, w, label="Elliptic-v1 (Bitcoin UTXO)", color="#1E3A8A", edgecolor="black", linewidth=0.8, zorder=3)
    b2 = ax.bar(x,     samld,    w, label="SAML-D (15-Bank Rail)", color="#15803D", edgecolor="black", linewidth=0.8, zorder=3)
    b3 = ax.bar(x + w, amlsim,   w, label="IBM AMLSim HI (Multi-Bank)", color="#EA580C", edgecolor="black", linewidth=0.8, zorder=3)

    # Label each bar with staggered heights to eliminate any text overlap
    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#1E3A8A", rotation=90, zorder=4)

    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#15803D", rotation=90, zorder=4)

    for bar in b3:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#EA580C", rotation=90, zorder=4)

    ax.set_ylim(0, 115)
    ax.set_ylabel("Macro F1-Score (%)", fontsize=10.0, fontweight="bold")
    ax.set_title("Stepwise Architectural Ablation Progression across 3 Diverse Financial Archetypes", fontsize=11.5, fontweight="bold", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(steps, fontsize=8.5, fontweight="bold")
    ax.legend(loc="upper left", ncol=3, frameon=True, fontsize=9.0)
    ax.grid(axis="y", linestyle=":", alpha=0.5, zorder=1)
    plt.tight_layout()

    save_figure(fig, "fig3_ablation_component_study", pad_inches=0.15)
    save_figure(fig, "ablation_study", pad_inches=0.15)
    plt.close(fig)

if __name__ == "__main__":
    generate()
