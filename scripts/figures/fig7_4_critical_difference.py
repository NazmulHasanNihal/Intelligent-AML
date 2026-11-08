"""
Figure 7.4: Statistical Significance and Archetype Performance Synthesis
Subplot (a): Wilcoxon-Holm Critical Difference Rank Spectrum with staggered multi-tier callouts
Subplot (b): Grouped Macro F1 Performance by Domain Archetype
Eliminates all text overlap between closely-ranked models (GCN 6.71 vs GraphSAGE 6.86).
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_REVIEW, COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous widescreen canvas for side-by-side analysis
    fig, (ax_cd, ax_dom) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=300,
                                        gridspec_kw={'width_ratios': [1.15, 1.25]})
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.12, wspace=0.25)

    # =========================================================================
    # SUBPLOT (A): CRITICAL DIFFERENCE (CD) RANK SPECTRUM (DEMSAR 2006)
    # =========================================================================
    ax_cd.axis("off")
    ax_cd.set_xlim(0.4, 8.6)
    ax_cd.set_ylim(-0.15, 1.15)

    # Title
    ax_cd.text(4.5, 1.12, "(a) Critical Difference Rank Spectrum (Wilcoxon-Holm)",
               ha="center", va="center", fontsize=9.0, weight="bold", color=COLOR_DARK)

    # Critical Difference Caliper at top
    cd_val = 1.45
    caliper_y = 0.98
    ax_cd.plot([1.0, 1.0 + cd_val], [caliper_y, caliper_y], color=COLOR_RISK, lw=2.0, zorder=3)
    ax_cd.plot([1.0, 1.0], [caliper_y - 0.03, caliper_y + 0.03], color=COLOR_RISK, lw=1.5, zorder=3)
    ax_cd.plot([1.0 + cd_val, 1.0 + cd_val], [caliper_y - 0.03, caliper_y + 0.03], color=COLOR_RISK, lw=1.5, zorder=3)
    ax_cd.text(1.0 + cd_val / 2.0, caliper_y + 0.05, f"Critical Difference CD = {cd_val:.2f} (alpha = 0.05)",
               ha="center", va="bottom", fontsize=6.8, weight="bold", color=COLOR_RISK)

    # Main Horizontal Rank Axis (y = 0.50)
    ax_cd.plot([1.0, 8.0], [0.50, 0.50], color=COLOR_DARK, lw=2.0, zorder=2)

    # Rank Ticks and Numbers
    for r in range(1, 9):
        ax_cd.plot([r, r], [0.47, 0.53], color=COLOR_DARK, lw=1.2, zorder=3)
        tick_label = f"{r} (Best)" if r == 1 else (f"{r} (Worst)" if r == 8 else f"{r}")
        ax_cd.text(r, 0.42, tick_label, ha="center", va="top", fontsize=6.4, weight="bold", color=COLOR_DARK)

    # Multi-tier staggered layout to eliminate all overlaps:
    # Top Tier 1: y = 0.82 (C-STGB 1.07, GraphSAGE 6.86)
    # Top Tier 2: y = 0.68 (CatBoost 2.79, CARE-GNN 5.14)
    # Bottom Tier 1: y = 0.28 (XGBoost 2.43, TGN 4.21)
    # Bottom Tier 2: y = 0.14 (GCN 6.71, EvolveGCN 7.79)
    models = [
        {"name": "C-STGB (Ours)", "rank": 1.07, "tier": "top1", "color": COLOR_SAFE,   "marker": "o", "sz": 65},
        {"name": "XGBoost",       "rank": 2.43, "tier": "bot1", "color": COLOR_INGEST, "marker": "s", "sz": 45},
        {"name": "CatBoost",      "rank": 2.79, "tier": "top2", "color": "#1d4ed8",    "marker": "s", "sz": 45},
        {"name": "TGN",           "rank": 4.21, "tier": "bot1", "color": COLOR_REVIEW, "marker": "D", "sz": 45},
        {"name": "CARE-GNN",      "rank": 5.14, "tier": "top2", "color": "#ea580c",    "marker": "D", "sz": 45},
        {"name": "GCN",           "rank": 6.71, "tier": "bot2", "color": COLOR_RISK,   "marker": "^", "sz": 45},
        {"name": "GraphSAGE",     "rank": 6.86, "tier": "top1", "color": "#991b1b",    "marker": "^", "sz": 45},
        {"name": "EvolveGCN",     "rank": 7.79, "tier": "bot2", "color": "#7f1d1d",    "marker": "v", "sz": 45},
    ]

    # Non-significant clique horizontal bars above axis
    # Tree clique: XGBoost (2.43) to CatBoost (2.79)
    ax_cd.plot([2.43, 2.79], [0.55, 0.55], color=COLOR_INGEST, lw=3.2, solid_capstyle="round", zorder=4)
    # Temporal GNN clique: TGN (4.21) to CARE-GNN (5.14)
    ax_cd.plot([4.21, 5.14], [0.55, 0.55], color=COLOR_REVIEW, lw=3.2, solid_capstyle="round", zorder=4)
    # Static GNN clique: GCN (6.71) to EvolveGCN (7.79)
    ax_cd.plot([6.71, 7.79], [0.55, 0.55], color=COLOR_RISK, lw=3.2, solid_capstyle="round", zorder=4)

    tier_y = {
        "top1": (0.84, 0.77),
        "top2": (0.71, 0.64),
        "bot1": (0.28, 0.21),
        "bot2": (0.14, 0.07)
    }

    for m in models:
        r_val = m["rank"]
        clr = m["color"]
        ax_cd.scatter([r_val], [0.50], color=clr, edgecolors=COLOR_DARK, s=m["sz"], marker=m["marker"], zorder=5)

        y_name, y_sub = tier_y[m["tier"]]
        is_top = m["tier"].startswith("top")
        leader_end = y_sub - 0.02 if is_top else y_name + 0.04
        
        ax_cd.plot([r_val, r_val], [0.50, leader_end], color=clr, lw=1.0, linestyle=":", zorder=3)
        ax_cd.text(r_val, y_name, m["name"], ha="center", va="center", fontsize=6.2, weight="bold", color=clr)
        ax_cd.text(r_val, y_sub, f"Rank {r_val:.2f}", ha="center", va="center", fontsize=5.6, color=COLOR_MUTED)

    # Bottom Legend for Subplot (a)
    ax_cd.text(4.5, -0.09, "Solid horizontal clique bars indicate statistical equivalence (p > 0.05)",
               ha="center", va="center", fontsize=6.0, color=COLOR_MUTED)

    # =========================================================================
    # SUBPLOT (B): GROUPED MACRO F1 PERFORMANCE BY DOMAIN ARCHETYPE
    # =========================================================================
    domains = [
        "Public Crypto (4)",
        "Multi-Bank (9)",
        "Card Stream (1)",
        "Overall Macro (14)"
    ]

    cstgb_vals = [90.53, 59.34, 56.48, 68.05]
    xgb_vals   = [86.76, 56.32, 48.20, 64.76]
    gnn_vals   = [60.95, 37.80, 38.20, 43.76]

    y_indices = np.arange(len(domains))
    bar_h = 0.22
    y_pos = y_indices[::-1]

    # Draw Grouped Bars
    ax_dom.barh(y_pos + bar_h, cstgb_vals, height=bar_h, color=COLOR_SAFE, edgecolor=COLOR_DARK, lw=0.9, label="C-STGB (Proposed)", zorder=3)
    ax_dom.barh(y_pos,         xgb_vals,   height=bar_h, color=COLOR_INGEST, edgecolor=COLOR_DARK, lw=0.9, label="Best Tree (XGBoost)", zorder=3)
    ax_dom.barh(y_pos - bar_h, gnn_vals,   height=bar_h, color=COLOR_RISK, edgecolor=COLOR_DARK, lw=0.9, label="Best GNN (TGN/CARE)", zorder=3)

    # Value Labels and Margins
    for i in range(len(domains)):
        yp = y_pos[i]
        c_v = cstgb_vals[i]
        x_v = xgb_vals[i]
        g_v = gnn_vals[i]

        lead_tree = c_v - x_v
        ax_dom.text(c_v + 1.2, yp + bar_h, f"{c_v:.1f}% (+{lead_tree:.1f}%)",
                    ha="left", va="center", fontsize=6.2, weight="bold", color=COLOR_SAFE, zorder=4)
        ax_dom.text(x_v + 1.2, yp, f"{x_v:.1f}%",
                    ha="left", va="center", fontsize=5.8, color=COLOR_INGEST, zorder=4)
        ax_dom.text(g_v + 1.2, yp - bar_h, f"{g_v:.1f}%",
                    ha="left", va="center", fontsize=5.8, color=COLOR_RISK, zorder=4)

    ax_dom.set_yticks(y_pos)
    ax_dom.set_yticklabels(domains, fontsize=7.6, fontweight="bold")
    ax_dom.set_xlim(0, 115)
    ax_dom.set_xlabel("Macro-Averaged F1 Score (%)", fontsize=8.2, fontweight="bold")
    ax_dom.set_title("(b) Performance Synthesis Across Financial Archetypes", fontsize=9.0, fontweight="bold", pad=8)
    ax_dom.legend(loc="lower right", frameon=True, fontsize=7.2, framealpha=0.95)
    ax_dom.grid(axis="x", linestyle=":", alpha=0.5, zorder=1)

    save_figure(fig, "fig_critical_difference_lollipop", pad_inches=0.12)
    save_figure(fig, "fig16_critical_difference", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
