"""
Figure 2.2: 1-WL Graph Isomorphism Failure vs C-STGB Invariant Disambiguation
Standalone publication script for C-STGB monograph.
Human-designed, practically intuitive diagram showing why standard GNNs miss smurfing and how C-STGB catches it.
Bounded geometry with strict padding ensuring zero text goes outside boundaries.
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

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.5), dpi=300)

    for ax in axes:
        ax.axis("off")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)

    # =========================================================================
    # LEFT PANEL: THE 1-WL GRAPH ISOMORPHISM FAILURE (Standard GNNs)
    # =========================================================================
    ax0 = axes[0]
    ax0.add_patch(patches.Rectangle((0.00, 0.00), 1.00, 1.00, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))
    
    # Header banner
    ax0.add_patch(patches.Rectangle((0.00, 0.92), 1.00, 0.08, facecolor="#fef2f2", edgecolor="#fca5a5", lw=0.8))
    ax0.text(0.50, 0.960, "Conventional GNNs: Blind to Physical Flow Dynamics",
             ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_RISK)

    # Sub-case 1: Retail Merchant (Left side of Left Panel)
    ax0.add_patch(patches.Rectangle((0.04, 0.36), 0.43, 0.53, facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1.0))
    ax0.text(0.255, 0.855, "Account A: Retail Store", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_INGEST)
    ax0.text(0.255, 0.818, "Coffee Shop / Grocery Merchant", ha="center", va="center", fontsize=6.2, color=COLOR_MUTED)

    # Central merchant node
    ax0.add_patch(patches.Circle((0.27, 0.62), 0.060, facecolor="#e0f2fe", edgecolor=COLOR_INGEST, lw=1.4))
    ax0.text(0.27, 0.62, "Retail\nStore", ha="center", va="center", fontsize=6.6, fontweight="bold", color=COLOR_INGEST)

    # 4 Customer deposit arrows (Safely padded from left edge 0.04)
    y_deposits = [0.73, 0.66, 0.58, 0.51]
    for yd in y_deposits:
        ax0.annotate("", xy=(0.21, yd), xytext=(0.10, yd),
                     arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#64748b", mutation_scale=9))
        ax0.text(0.09, yd, "$15", ha="right", va="center", fontsize=5.8, color="#64748b")
    ax0.text(0.255, 0.40, "Graph Degree: 4 Inbound Edges", ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_DARK)

    # Sub-case 2: Smurfing Mule (Right side of Left Panel)
    ax0.add_patch(patches.Rectangle((0.53, 0.36), 0.43, 0.53, facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.0))
    ax0.text(0.745, 0.855, "Account B: Smurfing Mule", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_RISK)
    ax0.text(0.745, 0.818, "Criminal Layering Conduit", ha="center", va="center", fontsize=6.2, color=COLOR_MUTED)

    # Central mule node
    ax0.add_patch(patches.Circle((0.76, 0.62), 0.060, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.4))
    ax0.text(0.76, 0.62, "Mule\nConduit", ha="center", va="center", fontsize=6.6, fontweight="bold", color=COLOR_RISK)

    # 4 Smurf deposit arrows (Safely padded from 0.53 edge)
    for yd in y_deposits:
        ax0.annotate("", xy=(0.70, yd), xytext=(0.59, yd),
                     arrowprops=dict(arrowstyle="-|>", lw=1.2, color=COLOR_RISK, mutation_scale=9))
        ax0.text(0.58, yd, "$9.8k", ha="right", va="center", fontsize=5.8, fontweight="bold", color=COLOR_RISK)
    ax0.text(0.745, 0.40, "Graph Degree: 4 Inbound Edges", ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_DARK)

    # Standard GNN Verdict Callout Box
    ax0.add_patch(patches.Rectangle((0.04, 0.04), 0.92, 0.28, facecolor="#fef2f2", edgecolor=COLOR_RISK, lw=1.2))
    ax0.text(0.50, 0.27, "1-WL GRAPH ISOMORPHISM BOTTLENECK",
             ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_RISK)
    ax0.text(0.50, 0.19, "• Standard GNNs (GCN, GAT, GraphSAGE) rely purely on degree and neighborhood topology.\n"
                         "• Degree(Retail Store) = 4 Inbound  ==  Degree(Smurfing Mule) = 4 Inbound.\n"
                         "• Verdict: 1-WL message-passing treats both accounts as STRUCTURALLY IDENTICAL!",
             ha="center", va="center", fontsize=6.6, color=COLOR_DARK, linespacing=1.25)
    ax0.text(0.50, 0.09, "RESULT: SEVERE FALSE NEGATIVE (Laundering Mule completely missed!)",
             ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_RISK)

    # =========================================================================
    # PANEL (B): HOW C-STGB PHYSICAL INVARIANTS INSTANTLY SOLVE IT
    # =========================================================================
    ax1 = axes[1]
    ax1.add_patch(patches.Rectangle((0.00, 0.00), 1.00, 1.00, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))
    
    # Header banner
    ax1.add_patch(patches.Rectangle((0.00, 0.92), 1.00, 0.08, facecolor="#f0fdf4", edgecolor="#86efac", lw=0.8))
    ax1.text(0.50, 0.960, "C-STGB Solution: Disambiguation via Mass-Flow Invariants",
             ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_SAFE)

    # Invariant Examination of Account A (Retail)
    ax1.add_patch(patches.Rectangle((0.04, 0.36), 0.43, 0.53, facecolor="#f0fdf4", edgecolor="#86efac", lw=1.0))
    ax1.text(0.255, 0.855, "Account A: Retail Store", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_SAFE)
    
    # Flow diagram for Retail (Safely inside [0.04, 0.47])
    ax1.annotate("", xy=(0.19, 0.68), xytext=(0.07, 0.68), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLOR_INGEST, mutation_scale=10))
    ax1.text(0.13, 0.72, "In: $60", ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=COLOR_INGEST)
    
    ax1.add_patch(patches.Rectangle((0.19, 0.58), 0.12, 0.20, facecolor="#dcfce7", edgecolor=COLOR_SAFE, lw=1.2))
    ax1.text(0.25, 0.68, "Absorbs\nFunds", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_SAFE)
    
    ax1.annotate("", xy=(0.43, 0.68), xytext=(0.31, 0.68), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#64748b", mutation_scale=9))
    ax1.text(0.37, 0.72, "Out: $5", ha="center", va="bottom", fontsize=6.0, color="#64748b")

    ax1.text(0.255, 0.50, "Capital Retention: 91.7%", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_SAFE)
    ax1.text(0.255, 0.43, "Flow Velocity: Low (Days)\nVerdict: Cleared Commercial", ha="center", va="center", fontsize=6.2, color=COLOR_DARK, linespacing=1.2)

    # Invariant Examination of Account B (Mule)
    ax1.add_patch(patches.Rectangle((0.53, 0.36), 0.43, 0.53, facecolor="#fff1f2", edgecolor="#fca5a5", lw=1.0))
    ax1.text(0.745, 0.855, "Account B: Smurfing Mule", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_RISK)
    
    # Flow diagram for Mule (Safely inside [0.53, 0.96])
    ax1.annotate("", xy=(0.68, 0.68), xytext=(0.56, 0.68), arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=11))
    ax1.text(0.62, 0.72, "In: $39.2k", ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=COLOR_RISK)
    
    ax1.add_patch(patches.Rectangle((0.68, 0.58), 0.12, 0.20, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.2))
    ax1.text(0.74, 0.68, "Zero\nRetain", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_RISK)
    
    ax1.annotate("", xy=(0.93, 0.68), xytext=(0.80, 0.68), arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=11))
    ax1.text(0.865, 0.72, "Out: $39.1k", ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=COLOR_RISK)

    ax1.text(0.745, 0.50, "Capital Retention: 0.25%", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_RISK)
    ax1.text(0.745, 0.43, "Flow Velocity: 12 min\nVerdict: Tier 1 Quarantine", ha="center", va="center", fontsize=6.2, color=COLOR_RISK, linespacing=1.2)

    # C-STGB Solution Callout Box
    ax1.add_patch(patches.Rectangle((0.04, 0.04), 0.92, 0.28, facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.2))
    ax1.text(0.50, 0.27, "C-STGB PHYSICAL MASS-FLOW INVARIANTS SUCCEED",
             ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_SAFE)
    ax1.text(0.50, 0.19, "• C-STGB looks beyond graph degree to track hydrodynamics and arrival timing.\n"
                         "• Mass-flow conservation reveals near-instant 99.7% pass-through velocity.\n"
                         "• 12-D Invariant vector breaks degree symmetry and unmasks the laundering chain!",
             ha="center", va="center", fontsize=6.6, color=COLOR_DARK, linespacing=1.25)
    ax1.text(0.50, 0.09, "RESULT: SUCCESSFUL DETECTION (100% Identification with Tier-1 Fast-Path Freeze)",
             ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_SAFE)

    save_figure(fig, "fig_2_3_1wl_failure_vs_invariants", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
