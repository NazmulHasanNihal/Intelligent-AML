"""
scripts/figures/fig1_1_benign_vs_smurfing.py
Figure 1.1: Topological Contrast Between Legitimate Flows and Smurfing Structuring
Exports to all 5 thesis directories.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Shared styling and multi-directory export
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    # Widen canvas to 9.2 x 3.9 inches and increase wspace to 0.32 for clean separation
    fig, (ax_b, ax_m) = plt.subplots(1, 2, figsize=(9.2, 3.9), dpi=300, gridspec_kw={'wspace': 0.30})
    ax_b.axis('off')
    ax_m.axis('off')

    # ----------------------------------------------------
    # Left Panel: Benign Retail Merchant Star Graph
    # ----------------------------------------------------
    ax_b.set_xlim([-1.55, 1.50])
    ax_b.set_ylim([-1.60, 1.35])
    ax_b.set_title("(a) Benign Commercial Merchant Hub", fontweight="bold", fontsize=9.2, pad=12)

    # Merchant Node (widened square with crisp padding)
    circle_m = patches.Rectangle((-0.30, -0.30), 0.60, 0.60, facecolor="#1e40af", edgecolor="#0f172a", lw=1.2, zorder=5)
    ax_b.add_patch(circle_m)
    ax_b.text(0, 0, "Retail Hub\n(deg=85)", ha="center", va="center", fontsize=6.3, fontweight="bold", color="#ffffff", linespacing=1.1, zorder=6)

    # Customer Nodes
    n_cust = 12
    angles = np.linspace(0, 2*np.pi, n_cust, endpoint=False)
    radius = 1.05
    for i, theta in enumerate(angles):
        cx = radius * np.cos(theta)
        cy = radius * np.sin(theta)
        c_node = patches.Circle((cx, cy), 0.11, facecolor="#94a3b8", edgecolor="#334155", lw=0.9, zorder=5)
        ax_b.add_patch(c_node)
        ax_b.text(cx, cy, f"C{i+1}", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#0f172a", zorder=6)
        
        # Directed edge to merchant
        ax_b.annotate("", xy=(0.24*np.cos(theta), 0.24*np.sin(theta)),
                      xytext=(cx - 0.11*np.cos(theta), cy - 0.11*np.sin(theta)),
                      arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.1, shrinkA=2, shrinkB=2), zorder=3)

    # Panel (a) Invariant annotation (clean two-line box with ample margin)
    ax_b.text(0, -1.35, "Invariant: Absorptive Commercial Sink\nMean $42.50 | High In-Degree Fan-In",
              ha="center", va="center", fontsize=6.8, fontweight="bold", color="#1e3a8a", linespacing=1.2,
              bbox=dict(boxstyle="square,pad=0.35", facecolor="#eff6ff", edgecolor="#bfdbfe", lw=0.8))

    # ----------------------------------------------------
    # Right Panel: Adversarial Smurfing & Structuring Tree
    # ----------------------------------------------------
    ax_m.set_xlim([-1.55, 1.50])
    ax_m.set_ylim([-1.60, 1.35])
    ax_m.set_title("(b) Synthetic Smurfing & Mule Network", fontweight="bold", fontsize=9.2, pad=12)

    # Illicit Source
    src = patches.Rectangle((-1.25, -0.24), 0.46, 0.48, facecolor="#dc2626", edgecolor="#991b1b", lw=1.2, zorder=5)
    ax_m.add_patch(src)
    ax_m.text(-1.02, 0, "Illicit\nSource", ha="center", va="center", fontsize=6.5, fontweight="bold", color="#ffffff", linespacing=1.1, zorder=6)

    # Intermediate Mules
    mules_y = [0.75, 0.25, -0.25, -0.75]
    for i, my in enumerate(mules_y):
        mule = patches.Rectangle((-0.18, my - 0.18), 0.36, 0.36, facecolor="#ea580c", edgecolor="#9a3412", lw=1.1, zorder=5)
        ax_m.add_patch(mule)
        ax_m.text(0, my, f"Mule {i+1}", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#ffffff", zorder=6)
        
        # Edge from Source to Mule
        ax_m.annotate("", xy=(-0.18, my), xytext=(-0.79, 0),
                      arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.1, shrinkA=2, shrinkB=2), zorder=3)

    # Consolidation Layer
    con = patches.Rectangle((0.80, -0.24), 0.46, 0.48, facecolor="#7c3aed", edgecolor="#5b21b6", lw=1.2, zorder=5)
    ax_m.add_patch(con)
    ax_m.text(1.03, 0, "Exfil\nAccount", ha="center", va="center", fontsize=6.5, fontweight="bold", color="#ffffff", linespacing=1.1, zorder=6)

    for my in mules_y:
        ax_m.annotate("", xy=(0.80, 0), xytext=(0.18, my),
                      arrowprops=dict(arrowstyle="->", color="#ea580c", lw=1.1, shrinkA=2, shrinkB=2), zorder=3)

    # Panel (b) Invariant annotation (clean two-line box with ample margin)
    ax_m.text(0, -1.35, "Invariant: Strict Pass-Through Flow\nNear CTR ($9,850) | High-Velocity Mule Chain",
              ha="center", va="center", fontsize=6.8, fontweight="bold", color="#991b1b", linespacing=1.2,
              bbox=dict(boxstyle="square,pad=0.35", facecolor="#fef2f2", edgecolor="#fecaca", lw=0.8))

    save_figure(fig, "fig_benign_vs_smurfing_topology", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
