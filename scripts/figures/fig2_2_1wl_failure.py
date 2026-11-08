"""
Figure 2.2: 1-WL Graph Isomorphism Bottleneck vs. 12-D Invariant Disambiguation
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=300)

    # Left: 1-WL Failure (Circular 6-Ring vs Two 3-Cycles)
    ax1.set_xlim(-0.2, 4.2)
    ax1.set_ylim(-0.2, 4.2)
    ax1.axis("off")
    ax1.set_title("Standard Spatial GNN (1-WL Bottleneck: Identical Multisets)", fontsize=9.2, fontweight="bold", color="#991B1B")

    card1 = patches.Rectangle((0, 0), 4.0, 4.0, facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=1.2)
    ax1.add_patch(card1)

    # Draw 6-cycle (wash ring)
    angles = np.linspace(0, 2 * np.pi, 7)[:-1]
    cx, cy, r = 1.3, 2.3, 0.85
    pts = [(cx + r * np.cos(a), cy + r * np.sin(a)) for a in angles]
    for i in range(6):
        ax1.plot([pts[i][0], pts[(i+1)%6][0]], [pts[i][1], pts[(i+1)%6][1]], color="#64748B", lw=2, zorder=2)
    for p in pts:
        ax1.scatter(p[0], p[1], s=140, color="#DC2626", edgecolor="black", zorder=3)
    ax1.text(cx, cy, "6-Node Wash Ring\nDegree Multiset: {{2,2}}", fontsize=7.2, fontweight="bold", ha="center", va="center")

    # Draw two disjoint 3-cycles
    pts_t1 = [(3.0, 3.1), (3.6, 3.1), (3.3, 3.6)]
    pts_t2 = [(3.0, 1.2), (3.6, 1.2), (3.3, 1.7)]
    for tri in [pts_t1, pts_t2]:
        for i in range(3):
            ax1.plot([tri[i][0], tri[(i+1)%3][0]], [tri[i][1], tri[(i+1)%3][1]], color="#64748B", lw=2, zorder=2)
        for p in tri:
            ax1.scatter(p[0], p[1], s=140, color="#2563EB", edgecolor="black", zorder=3)
    ax1.text(3.3, 2.45, "Disjoint 3-Cycles\nDegree Multiset: {{2,2}}", fontsize=7.2, fontweight="bold", ha="center", va="center")

    fail_badge = patches.Rectangle((0.15, 0.12), 3.7, 0.55, facecolor="#B91C1C", edgecolor="#991B1B", lw=0.8)
    ax1.add_patch(fail_badge)
    ax1.text(2.0, 0.395, "1-WL COLOR REFINEMENT FAILS: c(u) = c(v)\nCannot distinguish circular wash cycle from benign bipartite transfers!",
             color="white", fontsize=6.8, fontweight="bold", ha="center", va="center")

    # Right: C-STGB Disambiguation via 12-D Invariants
    ax2.set_xlim(-0.2, 4.2)
    ax2.set_ylim(-0.2, 4.2)
    ax2.axis("off")
    ax2.set_title("C-STGB Disambiguation: 12-D Universal Canonical Invariants", fontsize=9.2, fontweight="bold", color="#166534")

    card2 = patches.Rectangle((0, 0), 4.0, 4.0, facecolor="#F0FDF4", edgecolor="#86EFAC", lw=1.2)
    ax2.add_patch(card2)

    # Feature separator callouts
    separators = [
        ("Kirchhoff Mass-Flow Invariant", "Wash Ring: Strict Flow Conservation (Equal Inflow & Outflow)\nBenign Clusters: Absorptive Retail Sinks with Net Capital Retention", "#15803D"),
        ("Forward / Backward Causal Taint", "Wash Ring: High Bi-Directional Reachability (Closed Laundering Loop)\nBenign Clusters: Strictly Tree-like Unidirectional Flow", "#1D4ED8"),
        ("Hawkes Burst Timing Dispersion", "Wash Ring: Coordinated Rapid-Fire Bursts (<2.4h Intervals)\nBenign Clusters: Stochastic Human Inter-Arrival Times (>48h)", "#7C3AED"),
        ("Transmission Capital Velocity", "Wash Ring: High-Velocity Throughput (Immediate Mule Forwarding)\nBenign Clusters: Standard Holding Period (>14 Days Dormancy)", "#B45309")
    ]

    for idx, (title, desc, col) in enumerate(separators):
        y = 3.25 - idx * 0.76
        sbox = patches.Rectangle((0.2, y - 0.22), 3.6, 0.65, facecolor="#ffffff", edgecolor=col, lw=1.0)
        ax2.add_patch(sbox)
        ax2.text(0.35, y + 0.25, title, fontsize=7.5, fontweight="bold", color=col)
        ax2.text(0.35, y - 0.05, desc, fontsize=6.8, color="#1E293B")

    succ_badge = patches.Rectangle((0.15, 0.12), 3.7, 0.55, facecolor="#15803D", edgecolor="#166534", lw=0.8)
    ax2.add_patch(succ_badge)
    ax2.text(2.0, 0.395, "THEORETICALLY SEPARABLE: Injective Multiset Mapping\n12-D invariants strictly separate topologically isomorphic crime patterns!",
             color="white", fontsize=6.8, fontweight="bold", ha="center", va="center")

    plt.tight_layout()
    save_figure(fig, "fig_2_3_1wl_failure_vs_invariants", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
