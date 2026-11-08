"""
Figure 9.3: Multi-Bank Blind Spot vs. Privacy-Preserving Federated Split-GNN
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(11.0, 5.2), dpi=300)

    # Top: Multi-Bank Blind Spot
    ax_top.set_xlim(0, 10)
    ax_top.set_ylim(0, 3)
    ax_top.axis("off")
    ax_top.set_title("(a) Multi-Bank Siloed Blind Spot: Cross-Institution Laundering Chains Truncated into 1-Hop Stubs",
                     fontsize=9.0, fontweight="bold", color="#991B1B")

    bg_top = patches.FancyBboxPatch((0.1, 0.1), 9.8, 2.7, boxstyle="round,pad=0.05", fc="#FEF2F2", ec="#FCA5A5", lw=1.0)
    ax_top.add_patch(bg_top)

    # Bank A Box
    b_a = patches.FancyBboxPatch((0.4, 0.3), 4.2, 2.2, boxstyle="round,pad=0.05", fc="#ffffff", ec="#DC2626", lw=1.2)
    ax_top.add_patch(b_a)
    ax_top.text(2.5, 2.25, "Financial Institution A (Siloed)", fontsize=8.0, fontweight="bold", color="#991B1B", ha="center")
    ax_top.text(2.5, 1.2, "Sees Outflow to External Account:\nOriginator -> External Wire\n(Laundering Chain Truncated - Blind)",
                fontsize=7.2, color="#7F1D1D", ha="center")

    # Bank B Box
    b_b = patches.FancyBboxPatch((5.4, 0.3), 4.2, 2.2, boxstyle="round,pad=0.05", fc="#ffffff", ec="#DC2626", lw=1.2)
    ax_top.add_patch(b_b)
    ax_top.text(7.5, 2.25, "Financial Institution B (Siloed)", fontsize=8.0, fontweight="bold", color="#991B1B", ha="center")
    ax_top.text(7.5, 1.2, "Sees Inflow from External Account:\nExternal Wire -> Mule Cashout\n(Looks like Isolated Benign Deposit)",
                fontsize=7.2, color="#7F1D1D", ha="center")

    ax_top.annotate("", xy=(5.4, 1.4), xytext=(4.6, 1.4), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.0, linestyle="--"))
    ax_top.text(5.0, 1.65, "BLIND SPOT", color="#DC2626", fontweight="bold", fontsize=7.0, ha="center")

    # Bottom: Federated Split-GNN Solution
    ax_bot.set_xlim(0, 10)
    ax_bot.set_ylim(0, 3)
    ax_bot.axis("off")
    ax_bot.set_title("(b) Privacy-Preserving Federated Split-GNN: 12-D Canonical Invariant Boundary Bridging",
                     fontsize=9.0, fontweight="bold", color="#15803D")

    bg_bot = patches.FancyBboxPatch((0.1, 0.1), 9.8, 2.7, boxstyle="round,pad=0.05", fc="#F0FDF4", ec="#86EFAC", lw=1.0)
    ax_bot.add_patch(bg_bot)

    # Bank A Local Client
    c_a = patches.FancyBboxPatch((0.4, 0.3), 3.0, 2.2, boxstyle="round,pad=0.05", fc="#ffffff", ec="#16A34A", lw=1.0)
    ax_bot.add_patch(c_a)
    ax_bot.text(1.9, 2.25, "Bank A Local Client", fontsize=7.5, fontweight="bold", color="#15803D", ha="center")
    ax_bot.text(1.9, 1.2, "Private PII & Raw Graphs Kept Local\nExtracts Universal 12-D Invariants:\nz_inv = [Phi_flow, lambda, v_A, ...]",
                fontsize=6.8, color="#166534", ha="center")

    # Central Split-GNN Arbiter
    s_c = patches.FancyBboxPatch((3.8, 0.3), 2.4, 2.2, boxstyle="round,pad=0.05", fc="#EFF6FF", ec="#2563EB", lw=1.2)
    ax_bot.add_patch(s_c)
    ax_bot.text(5.0, 2.25, "Federated Boundary Arbiter", fontsize=7.5, fontweight="bold", color="#1D4ED8", ha="center")
    ax_bot.text(5.0, 1.2, "Aggregates Boundary Activations\nh_bound without Raw Account PII\nComputes End-to-End CRC Risk",
                fontsize=6.8, color="#1E40AF", ha="center")

    # Bank B Local Client
    c_b = patches.FancyBboxPatch((6.6, 0.3), 3.0, 2.2, boxstyle="round,pad=0.05", fc="#ffffff", ec="#16A34A", lw=1.0)
    ax_bot.add_patch(c_b)
    ax_bot.text(8.1, 2.25, "Bank B Local Client", fontsize=7.5, fontweight="bold", color="#15803D", ha="center")
    ax_bot.text(8.1, 1.2, "Private PII & Raw Graphs Kept Local\nSynchronizes Boundary Embeddings\n100% GDPR / BSA Compliant",
                fontsize=6.8, color="#166534", ha="center")

    ax_bot.annotate("", xy=(3.8, 1.4), xytext=(3.4, 1.4), arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=1.5))
    ax_bot.annotate("", xy=(6.6, 1.4), xytext=(6.2, 1.4), arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=1.5))

    plt.tight_layout()
    save_figure(fig, "fig_9_3_multibank_split_gnn", pad_inches=0.12)
    plt.close()



if __name__ == "__main__":
    generate()
