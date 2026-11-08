"""
Figure 2.1: Adversarial Camouflage Topology and Edge-Trust Filter Pruning
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 5.6), dpi=300)
    for ax in axes:
        ax.axis('off')
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)

    pos_syndicate = {
        'S0': np.array([-0.36,  0.42]),
        'M1': np.array([ 0.18,  0.48]),
        'M2': np.array([ 0.44,  0.04]),
        'L3': np.array([ 0.14, -0.38]),
        'C4': np.array([-0.36, -0.32]),
    }

    pos_merchants = {
        'H1': np.array([-0.95,  0.80]),
        'H2': np.array([ 0.95,  0.80]),
        'H3': np.array([ 0.95, -0.72]),
        'H4': np.array([-0.95, -0.72]),
    }

    np.random.seed(101)
    merchant_customers = {}
    for h_name, h_pos in pos_merchants.items():
        n_cust = 8
        angles = np.linspace(0, 2*np.pi, n_cust, endpoint=False) + np.random.uniform(-0.18, 0.18, n_cust)
        radii = np.random.uniform(0.18, 0.30, n_cust)
        cust_pos = [h_pos + np.array([r * np.cos(a), r * np.sin(a)]) for a, r in zip(angles, radii)]
        merchant_customers[h_name] = cust_pos

    chaff_pairs = [
        ('M1', 'H1'), ('M1', 'H2'), ('M1', 'H3'),
        ('M2', 'H2'), ('M2', 'H3'), ('M2', 'H1'),
        ('L3', 'H3'), ('L3', 'H4'), ('L3', 'H2'),
        ('S0', 'H1'), ('S0', 'H4'),
        ('C4', 'H4'), ('C4', 'H3'),
    ]
    syn_edges = [('S0', 'M1'), ('M1', 'M2'), ('M2', 'L3'), ('L3', 'C4'), ('C4', 'S0')]

    # Panel (a)
    ax0 = axes[0]
    ax0.set_title("(a) Raw Camouflaged Transaction Network\n(Spurious Chaff Edges Inducing Over-Smoothing)",
                  fontsize=8.8, fontweight="bold", color="#0f172a", pad=10)

    for h_name, h_pos in pos_merchants.items():
        for c_pos in merchant_customers[h_name]:
            ax0.plot([h_pos[0], c_pos[0]], [h_pos[1], c_pos[1]], color="#cbd5e1", lw=0.9, zorder=1)
            ax0.scatter(c_pos[0], c_pos[1], s=18, color="#94a3b8", edgecolors="#64748b", lw=0.5, zorder=2)

    for src, dst in chaff_pairs:
        p1 = pos_syndicate[src]
        p2 = pos_merchants[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=1.1, color="#f87171", ls="--", alpha=0.85))

    for src, dst in syn_edges:
        p1 = pos_syndicate[src]
        p2 = pos_syndicate[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=2.2, color="#dc2626"))

    for h_name, h_pos in pos_merchants.items():
        ax0.scatter(h_pos[0], h_pos[1], s=260, color="#0284c7", edgecolors="#0369a1", lw=1.5, zorder=4)
        ax0.text(h_pos[0], h_pos[1], h_name, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

    for s_name, s_pos in pos_syndicate.items():
        col = "#991b1b" if s_name in ['S0', 'C4'] else "#ea580c"
        ax0.scatter(s_pos[0], s_pos[1], s=220, color=col, edgecolors="#ffffff", lw=1.5, zorder=6)
        ax0.text(s_pos[0], s_pos[1], s_name, ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=7)

    ax0.add_patch(patches.Rectangle((-1.26, -1.28), 2.52, 0.22, fc="#fef2f2", ec="#ef4444", lw=1.0))
    ax0.text(0.0, -1.14, "Standard GNN Failure: Feature Over-Smoothing Collapse", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#991b1b")
    ax0.text(0.0, -1.22, r"Spurious Chaff dilutes Dirichlet Energy ($\mathcal{E} \to 0$); Laundering disguised as Benign Hub.", ha="center", va="center", fontsize=5.8, color="#7f1d1d")

    # Panel (b)
    ax1 = axes[1]
    ax1.set_title(r"(b) C-STGB Context-Aware Edge-Trust Gating ($\hat{g}_{ij} \geq 0.92$)" + "\n(65.9% Spurious Camouflage Chaff Pruned)",
                  fontsize=8.8, fontweight="bold", color="#0f172a", pad=10)

    for h_name, h_pos in pos_merchants.items():
        for c_pos in merchant_customers[h_name]:
            ax1.plot([h_pos[0], c_pos[0]], [h_pos[1], c_pos[1]], color="#cbd5e1", lw=0.9, zorder=1)
            ax1.scatter(c_pos[0], c_pos[1], s=18, color="#94a3b8", edgecolors="#64748b", lw=0.5, zorder=2)

    for src, dst in chaff_pairs:
        p1 = pos_syndicate[src]
        p2 = pos_merchants[dst]
        ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#e2e8f0", lw=0.8, ls=":", alpha=0.45, zorder=1)
        mid = 0.5 * (p1 + p2)
        ax1.text(mid[0], mid[1], "×", ha="center", va="center", fontsize=7.2, color="#ef4444", fontweight="bold", alpha=0.75)

    for src, dst in syn_edges:
        p1 = pos_syndicate[src]
        p2 = pos_syndicate[dst]
        ax1.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=2.6, color="#059669"))

    badge_positions = [
        (-0.09,  0.55),
        ( 0.42,  0.32),
        ( 0.38, -0.22),
        (-0.11, -0.46),
        (-0.48,  0.05),
    ]
    for bx, by in badge_positions:
        ax1.text(bx, by, r"$\hat{g} \approx 0.95$", ha="center", va="center", 
                 fontsize=5.2, fontweight="bold", color="#065f46",
                 bbox=dict(boxstyle="square,pad=0.18", fc="#dcfce7", ec="#16a34a", lw=0.6, alpha=0.95), zorder=8)

    for h_name, h_pos in pos_merchants.items():
        ax1.scatter(h_pos[0], h_pos[1], s=260, color="#0284c7", edgecolors="#0369a1", lw=1.5, zorder=4)
        ax1.text(h_pos[0], h_pos[1], h_name, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

    for s_name, s_pos in pos_syndicate.items():
        col = "#991b1b" if s_name in ['S0', 'C4'] else "#ea580c"
        ax1.scatter(s_pos[0], s_pos[1], s=240, color=col, edgecolors="#fde047", lw=2.0, zorder=6)
        ax1.text(s_pos[0], s_pos[1], s_name, ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=7)

    ax1.add_patch(patches.Rectangle((-1.26, -1.28), 2.52, 0.22, fc="#ecfdf5", ec="#10b981", lw=1.0))
    ax1.text(0.0, -1.14, "C-STGB Protection: Spectral Dirichlet Energy Preserved", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#065f46")
    ax1.text(0.0, -1.22, r"Edge Gate filters 65.9% Chaff ($\hat{g}_{ij} < 0.10$); True Wash Cycle Isolated ($\mathcal{E} > 0.75$).", ha="center", va="center", fontsize=5.8, color="#047857")

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Merchant Commercial Hubs (H1-H4)', markerfacecolor='#0284c7', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Laundering Syndicate (S0, M1-M2, L3, C4)', markerfacecolor='#dc2626', markeredgecolor='#fde047', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Benign Retail Customers', markerfacecolor='#94a3b8', markersize=5),
        plt.Line2D([0], [0], color='#dc2626', lw=2.0, label='Illicit Flow Conduit'),
        plt.Line2D([0], [0], color='#f87171', lw=1.2, linestyle='--', label=r'Adversarial Camouflage Chaff ($\hat{g}_{ij} < 0.10$)'),
        plt.Line2D([0], [0], color='#059669', lw=2.0, label=r'C-STGB Denoised Wash Cycle ($\hat{g}_{ij} \geq 0.92$)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.015),
               ncol=3, fontsize=6.6, framealpha=0.96, edgecolor='#cbd5e1')

    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.17, wspace=0.14)
    save_figure(fig, "fig21_adversarial_camouflage_topology", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
