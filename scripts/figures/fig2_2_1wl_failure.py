"""
Figure 2.2: 1-WL Graph Isomorphism Failure vs C-STGB Invariant Disambiguation
Complete professional overhaul:
- Expanded canvas dimensions with generous margins
- Perfectly fitted text with zero overflow or border clipping
- Crisp account cards, flow diagrams, and physical conservation metrics
- Strict 4-color palette (Blue = Ingestion/Merchant, Red = Risk/Mule, Green = Safe/Defense)
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def build_left_panel(ax):
    """Left Panel: Conventional 1-WL Failure under Topological Isomorphism."""
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Master White Panel Box
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.0, zorder=1))

    # Header Banner
    ax.add_patch(patches.Rectangle((0, 93.2), 100, 6.8, facecolor="#fef2f2", edgecolor=COLOR_RISK, lw=1.0, zorder=2))
    ax.text(50, 96.6, "(a) CONVENTIONAL GNN FAILURE: 1-WL GRAPH ISOMORPHISM BOTTLENECK",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_RISK, zorder=3)

    # Sub-Card 1: Account A (Retail Merchant) - Left: x in [3.5, 48.0]
    ax.add_patch(patches.FancyBboxPatch(
        (3.5, 36.0), 44.5, 54.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1.1, zorder=2
    ))
    # Header inside Sub-Card 1
    ax.add_patch(patches.Rectangle((3.5, 83.5), 44.5, 6.5, facecolor="#e0f2fe", edgecolor="none", zorder=3))
    ax.text(25.75, 87.2, "ACCOUNT A: RETAIL STORE", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_INGEST, zorder=4)
    ax.text(25.75, 84.8, "Coffee Shop / Supermarket Merchant", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=4)

    # Central Merchant Node
    ax.add_patch(patches.Circle((29.0, 62.0), 7.0, facecolor="#e0f2fe", edgecolor=COLOR_INGEST, lw=1.4, zorder=4))
    ax.text(29.0, 63.2, "Retail", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_INGEST, zorder=5)
    ax.text(29.0, 60.6, "Store", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_INGEST, zorder=5)

    # 4 Customer Inbound Wires (Properly padded from left boundary x=3.5)
    y_in = [74.0, 66.0, 58.0, 50.0]
    amounts_a = ["$15.00", "$25.50", "$12.00", "$17.50"]
    for yi, amt in zip(y_in, amounts_a):
        ax.annotate("", xy=(21.5, yi), xytext=(8.0, yi),
                    arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#64748b", mutation_scale=9), zorder=4)
        ax.text(14.0, yi + 1.4, amt, ha="center", va="bottom", fontsize=5.6, color="#475569", zorder=5)

    # Degree metrics badge
    ax.add_patch(patches.FancyBboxPatch(
        (6.0, 38.5), 39.5, 7.5,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor="#ffffff", edgecolor="#cbd5e1", lw=0.9, zorder=4
    ))
    ax.text(25.75, 43.5, r"Topological In-Degree: $\mathrm{deg}_{\mathrm{in}} = 4$", ha="center", va="center", fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=5)
    ax.text(25.75, 40.5, r"1-WL Representation: $\{\{1, 1, 1, 1\}\}$", ha="center", va="center", fontsize=5.6, color="#64748b", zorder=5)

    # Sub-Card 2: Account B (Smurfing Mule) - Right: x in [52.0, 96.5]
    ax.add_patch(patches.FancyBboxPatch(
        (52.0, 36.0), 44.5, 54.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.1, zorder=2
    ))
    # Header inside Sub-Card 2
    ax.add_patch(patches.Rectangle((52.0, 83.5), 44.5, 6.5, facecolor="#fee2e2", edgecolor="none", zorder=3))
    ax.text(74.25, 87.2, "ACCOUNT B: SMURFING MULE", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_RISK, zorder=4)
    ax.text(74.25, 84.8, "Criminal Structuring / Conduit Mule", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=4)

    # Central Mule Node
    ax.add_patch(patches.Circle((77.5, 62.0), 7.0, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.4, zorder=4))
    ax.text(77.5, 63.2, "Mule", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_RISK, zorder=5)
    ax.text(77.5, 60.6, "Conduit", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_RISK, zorder=5)

    # 4 Criminal Inbound Wires (Properly padded from x=52.0)
    amounts_b = ["$9,850", "$9,800", "$9,900", "$9,750"]
    for yi, amt in zip(y_in, amounts_b):
        ax.annotate("", xy=(70.0, yi), xytext=(56.5, yi),
                    arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_RISK, mutation_scale=9), zorder=4)
        ax.text(62.5, yi + 1.4, amt, ha="center", va="bottom", fontsize=5.6, fontweight="bold", color=COLOR_RISK, zorder=5)

    # Degree metrics badge
    ax.add_patch(patches.FancyBboxPatch(
        (54.5, 38.5), 39.5, 7.5,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor="#ffffff", edgecolor="#fca5a5", lw=0.9, zorder=4
    ))
    ax.text(74.25, 43.5, r"Topological In-Degree: $\mathrm{deg}_{\mathrm{in}} = 4$", ha="center", va="center", fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=5)
    ax.text(74.25, 40.5, r"1-WL Representation: $\{\{1, 1, 1, 1\}\}$", ha="center", va="center", fontsize=5.6, color="#64748b", zorder=5)

    # Bottom Callout Box (Sized and padded with high precision)
    ax.add_patch(patches.FancyBboxPatch(
        (3.5, 3.5), 93.0, 29.5,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#fff1f2", edgecolor=COLOR_RISK, lw=1.2, zorder=2
    ))
    ax.text(50.0, 29.5, "1-WL GRAPH ISOMORPHISM BOTTLENECK: NON-INJECTIVE COLLAPSE",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_RISK, zorder=3)
    
    ax.text(6.0, 24.5, "> Standard GNNs (GCN, GAT, GraphSAGE) map both accounts to identical multiset representations.",
            fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(6.0, 20.5, r"> Spatial neighborhood aggregation ignores continuous transaction volume (\$15 vs \$9,800) and time intervals.",
            fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(6.0, 16.5, r"> Weisfeiler-Lehman color hashing assigns identical structural embeddings: $h(\mathrm{Retail}) = h(\mathrm{Mule})$.",
            fontsize=5.8, color="#1e293b", zorder=3)

    # Verdict Pill at bottom
    ax.add_patch(patches.FancyBboxPatch(
        (6.0, 6.0), 88.0, 6.5,
        boxstyle="round,pad=0.15,rounding_size=0.4",
        facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=0.8, zorder=3
    ))
    ax.text(50.0, 9.25, "CONVENTIONAL VERDICT: FALSE NEGATIVE (Laundering Ring Completely Missed, Recall < 12%)",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_RISK, zorder=4)


def build_right_panel(ax):
    """Right Panel: C-STGB Solution via 12-D Mass-Flow Invariants."""
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Master White Panel Box
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.0, zorder=1))

    # Header Banner
    ax.add_patch(patches.Rectangle((0, 93.2), 100, 6.8, facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.0, zorder=2))
    ax.text(50, 96.6, "(b) C-STGB SOLUTION: INVARIANT-GUIDED MASS-FLOW DISAMBIGUATION",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_SAFE, zorder=3)

    # Sub-Card 1: Account A (Retail Merchant Invariant Profile) - Left: x in [3.5, 48.0]
    ax.add_patch(patches.FancyBboxPatch(
        (3.5, 36.0), 44.5, 54.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f0fdf4", edgecolor="#86efac", lw=1.1, zorder=2
    ))
    # Header inside Sub-Card 1
    ax.add_patch(patches.Rectangle((3.5, 83.5), 44.5, 6.5, facecolor="#dcfce7", edgecolor="none", zorder=3))
    ax.text(25.75, 87.2, "ACCOUNT A: RETAIL STORE", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_SAFE, zorder=4)
    ax.text(25.75, 84.8, "Absorptive Commercial Capital Sink", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=4)

    # Flow graphic for Retail
    # Inflow pipe
    ax.annotate("", xy=(19.0, 68.0), xytext=(7.0, 68.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_INGEST, mutation_scale=10), zorder=4)
    ax.text(13.0, 70.4, "In: $70.00", ha="center", va="bottom", fontsize=5.8, fontweight="bold", color=COLOR_INGEST, zorder=5)

    # Storage Box (Absorbs Funds)
    ax.add_patch(patches.FancyBboxPatch(
        (19.0, 58.0), 13.5, 20.0,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor="#dcfce7", edgecolor=COLOR_SAFE, lw=1.2, zorder=4
    ))
    ax.text(25.75, 69.5, "Capital Sink", ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_SAFE, zorder=5)
    ax.text(25.75, 66.0, "Absorbs", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)
    ax.text(25.75, 63.0, "Consumer", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)
    ax.text(25.75, 60.0, "Revenue", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)

    # Outflow pipe
    ax.annotate("", xy=(44.5, 68.0), xytext=(32.5, 68.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#64748b", mutation_scale=9), zorder=4)
    ax.text(38.5, 70.4, "Out: $6.50", ha="center", va="bottom", fontsize=5.6, color="#64748b", zorder=5)

    # Invariant Metrics Box
    ax.add_patch(patches.FancyBboxPatch(
        (6.0, 38.5), 39.5, 16.0,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor="#ffffff", edgecolor="#86efac", lw=0.9, zorder=4
    ))
    ax.text(25.75, 51.5, "INVARIANT METRICS (ACCOUNT A):", ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_SAFE, zorder=5)
    ax.text(8.0, 47.5, r"> Net Capital Retention: $\Phi_{\mathrm{flow}} = 90.7\%$", fontsize=5.4, color="#1e293b", zorder=5)
    ax.text(8.0, 44.0, r"> Hawkes Burst Rate: $\lambda = 0.04\ /\ \mathrm{min}$ (Steady)", fontsize=5.4, color="#1e293b", zorder=5)
    ax.text(8.0, 40.5, "> Temporal Span: Distributed across 14 days", fontsize=5.4, color="#1e293b", zorder=5)

    # Sub-Card 2: Account B (Smurfing Mule Invariant Profile) - Right: x in [52.0, 96.5]
    ax.add_patch(patches.FancyBboxPatch(
        (52.0, 36.0), 44.5, 54.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.1, zorder=2
    ))
    # Header inside Sub-Card 2
    ax.add_patch(patches.Rectangle((52.0, 83.5), 44.5, 6.5, facecolor="#fee2e2", edgecolor="none", zorder=3))
    ax.text(74.25, 87.2, "ACCOUNT B: SMURFING MULE", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_RISK, zorder=4)
    ax.text(74.25, 84.8, "High-Velocity Pass-Through Conduit", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=4)

    # Flow graphic for Mule
    # Inflow pipe
    ax.annotate("", xy=(67.5, 68.0), xytext=(55.5, 68.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=10), zorder=4)
    ax.text(61.5, 70.4, "In: $39.3k", ha="center", va="bottom", fontsize=5.8, fontweight="bold", color=COLOR_RISK, zorder=5)

    # Conduit Box (Zero Retention)
    ax.add_patch(patches.FancyBboxPatch(
        (67.5, 58.0), 13.5, 20.0,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.2, zorder=4
    ))
    ax.text(74.25, 69.5, "Pass-Through", ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_RISK, zorder=5)
    ax.text(74.25, 66.0, "Zero Retain", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)
    ax.text(74.25, 63.0, "Rapid Wire", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)
    ax.text(74.25, 60.0, "Tunnel", ha="center", va="center", fontsize=5.6, color=COLOR_DARK, zorder=5)

    # Outflow pipe
    ax.annotate("", xy=(93.0, 68.0), xytext=(81.0, 68.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=10), zorder=4)
    ax.text(87.0, 70.4, "Out: $39.2k", ha="center", va="bottom", fontsize=5.8, fontweight="bold", color=COLOR_RISK, zorder=5)

    # Invariant Metrics Box
    ax.add_patch(patches.FancyBboxPatch(
        (54.5, 38.5), 39.5, 16.0,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor="#ffffff", edgecolor="#fca5a5", lw=0.9, zorder=4
    ))
    ax.text(74.25, 51.5, "INVARIANT METRICS (ACCOUNT B):", ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_RISK, zorder=5)
    ax.text(56.5, 47.5, r"> Net Capital Retention: $\Phi_{\mathrm{flow}} = 0.25\%$", fontsize=5.4, fontweight="bold", color=COLOR_RISK, zorder=5)
    ax.text(56.5, 44.0, r"> Hawkes Burst Rate: $\lambda = 74.2\ /\ \mathrm{hr}$ (Burst)", fontsize=5.4, fontweight="bold", color=COLOR_RISK, zorder=5)
    ax.text(56.5, 40.5, "> Temporal Span: Fully drained within 12 minutes", fontsize=5.4, fontweight="bold", color=COLOR_RISK, zorder=5)

    # Bottom Callout Box (Sized and padded with high precision)
    ax.add_patch(patches.FancyBboxPatch(
        (3.5, 3.5), 93.0, 29.5,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.2, zorder=2
    ))
    ax.text(50.0, 29.5, "C-STGB DISAMBIGUATION: PHYSICAL INVARIANTS ESTABLISH STRICT INJECTIVITY",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_SAFE, zorder=3)
    
    ax.text(6.0, 24.5, "> 12-D Physical Invariant vector incorporates Kirchhoff flow conservation law and self-exciting Hawkes arrival timing.",
            fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(6.0, 20.5, r"> Breaks topological symmetry: $\Delta\Phi_{\mathrm{flow}} = 90.45\ \mathrm{pp}$ separation cleanly discriminates commercial sink from conduit mule.",
            fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(6.0, 16.5, "> Continuous harmonic attention pinpoints 12-minute dwell delay, driving conformal triage to quarantine the wire instantly.",
            fontsize=5.8, color="#1e293b", zorder=3)

    # Verdict Pill at bottom
    ax.add_patch(patches.FancyBboxPatch(
        (6.0, 6.0), 88.0, 6.5,
        boxstyle="round,pad=0.15,rounding_size=0.4",
        facecolor="#dcfce7", edgecolor=COLOR_SAFE, lw=0.8, zorder=3
    ))
    ax.text(50.0, 9.25, "C-STGB VERDICT: TIER-1 INTERDICTION (100% Identification with Instant Real-Time Quarantine)",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_SAFE, zorder=4)


def generate():
    setup_plt(font_size=8.0, title_size=9.2, label_size=8.5)
    # Spacious 15.2 x 6.4 inch canvas with balanced margins
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 6.4), dpi=300)

    # Panel (a): Conventional 1-WL Failure
    build_left_panel(axes[0])

    # Panel (b): C-STGB Invariant Disambiguation
    build_right_panel(axes[1])

    plt.subplots_adjust(left=0.015, right=0.985, top=0.97, bottom=0.03, wspace=0.08)
    save_figure(fig, "fig_2_3_1wl_failure_vs_invariants", pad_inches=0.06)
    save_figure(fig, "fig2_2_1wl_failure", pad_inches=0.06)
    plt.close(fig)

if __name__ == "__main__":
    generate()
