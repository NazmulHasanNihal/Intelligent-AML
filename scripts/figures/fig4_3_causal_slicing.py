"""
Figure 4.3: Time-Causal 2-Hop Ego-Graph Extraction Window
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    fig, ax = plt.subplots(figsize=(10.0, 3.4), dpi=300)

    # Timeline zones
    ax.add_patch(patches.Rectangle((0, 0.3), 2.0, 0.4, facecolor="#E2E8F0", edgecolor="black"))
    ax.add_patch(patches.Rectangle((2.0, 0.3), 5.5, 0.4, facecolor="#DCFCE7", edgecolor="#15803D", linewidth=2))
    ax.add_patch(patches.Rectangle((7.5, 0.3), 2.5, 0.4, facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2, hatch="//"))

    ax.axvline(7.5, color="#DC2626", linewidth=2.5)
    ax.text(7.5, 0.82, r"Evaluation Timestamp $t_{\mathrm{eval}}$ (Strict Causal Barrier)",
            color="#DC2626", fontweight="bold", ha="center", fontsize=9.5)

    ax.text(1.0, 0.5, "Archived History\n(> 90 Days Ago)", ha="center", va="center", fontsize=8.5, color="#475569")
    ax.text(4.75, 0.5, r"Active 2-Hop Causal Ego-Graph Window ($t_{\mathrm{eval}} - 90\mathrm{d} \leq t_e \leq t_{\mathrm{eval}}$)"
            "\nDuckDB Composite B-Tree Scan: 0.18 ms | Zero Lookahead",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color="#166534")
    ax.text(8.75, 0.5, r"Forbidden Future ($t_e > t_{\mathrm{eval}}$)" "\nBlocked by SQL Contract\n(0.0% Leakage)",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color="#991B1B")

    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0.1, 1.0)
    ax.axis("off")
    ax.set_title("Vectorized Time-Causal Ego-Graph Extraction & Zero-Lookahead Invariant (Listing C.2)", fontsize=10.5, fontweight="bold")
    plt.tight_layout()
    save_figure(fig, "fig_4_3_causal_slicing", pad_inches=0.12)
    plt.close()

# ==============================================================================
# 5. Figure 5.6: ACI Martingale Drift Convergence
# ==============================================================================


if __name__ == "__main__":
    generate()
