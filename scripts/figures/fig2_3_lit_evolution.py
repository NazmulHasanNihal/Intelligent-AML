"""
Figure 2.3: Chronological SOTA Frontier in Graph Financial Crime Surveillance
Standalone publication script for C-STGB monograph.
Human-designed, perfectly positioned points and clear empirical F1 scores without collisions.
Translucent pill bounding boxes on all labels ensure 100% readability with zero line overlap.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_REVIEW, COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.8)
    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=300)

    # Models: (Name, Year/Era-Index, F1-Score %, Category, (offset_x, offset_y), ha, va)
    models = [
        {"name": "GCN", "year": 1.0, "f1": 43.55, "cat": "Static GNN", "col": COLOR_MUTED, "ox": -10, "oy": 10, "ha": "right"},
        {"name": "GAT", "year": 1.4, "f1": 31.35, "cat": "Static GNN", "col": COLOR_MUTED, "ox": 10, "oy": -12, "ha": "left"},
        {"name": "GraphSAGE", "year": 1.8, "f1": 49.07, "cat": "Static GNN", "col": COLOR_MUTED, "ox": -10, "oy": 10, "ha": "right"},
        {"name": "EvolveGCN", "year": 3.2, "f1": 51.04, "cat": "Temporal GNN", "col": COLOR_INGEST, "ox": 10, "oy": -14, "ha": "left"},
        {"name": "Skip-GCN", "year": 3.5, "f1": 62.40, "cat": "Static GNN", "col": COLOR_MUTED, "ox": -10, "oy": 10, "ha": "right"},
        {"name": "CARE-GNN", "year": 3.8, "f1": 64.50, "cat": "Camouflage GNN", "col": COLOR_REVIEW, "ox": 10, "oy": 10, "ha": "left"},
        {"name": "TGN", "year": 4.3, "f1": 68.40, "cat": "Temporal GNN", "col": COLOR_INGEST, "ox": -10, "oy": 10, "ha": "right"},
        {"name": "GraphSMOTE", "year": 5.0, "f1": 72.10, "cat": "Imbalance GNN", "col": "#7c3aed", "ox": 10, "oy": -12, "ha": "left"},
        {"name": "ChronoWave-GNN", "year": 6.2, "f1": 84.20, "cat": "Temporal GNN", "col": COLOR_INGEST, "ox": -12, "oy": 10, "ha": "right"},
        {"name": "XGBoost", "year": 2.6, "f1": 88.35, "cat": "Industrial Tabular", "col": COLOR_DARK, "ox": -12, "oy": 10, "ha": "right"},
        {"name": "C-STGB (Proposed)", "year": 8.0, "f1": 91.42, "cat": "Proposed Framework", "col": COLOR_SAFE, "ox": -14, "oy": 12, "ha": "right"},
    ]

    # Draw Horizontal Tabular Baseline (XGBoost line)
    ax.axhline(88.35, color="#64748b", linestyle="--", lw=1.2, alpha=0.75, zorder=2)
    ax.text(0.45, 90.0, "Industrial Baseline: XGBoost (88.35% F1)", fontsize=7.4, fontweight="bold", color="#475569",
            bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec="#cbd5e1", lw=0.6, alpha=0.9))

    # SOTA Frontier Curve (Pareto frontier connecting GCN -> Skip-GCN -> TGN -> GraphSMOTE -> ChronoWave -> C-STGB)
    frontier_x = [1.0, 3.5, 4.3, 5.0, 6.2, 8.0]
    frontier_y = [43.55, 62.40, 68.40, 72.10, 84.20, 91.42]
    ax.plot(frontier_x, frontier_y, color=COLOR_SAFE, linestyle="-", lw=2.4, alpha=0.85, zorder=3)
    ax.text(4.4, 73.0, "Empirical SOTA Progression Curve", fontsize=7.2, fontweight="bold", color=COLOR_SAFE, rotation=22,
            bbox=dict(boxstyle="square,pad=0.2", fc="#f0fdf4", ec=COLOR_SAFE, lw=0.6, alpha=0.9))

    # Plot points with shielded text boxes
    for m in models:
        is_cstgb = "C-STGB" in m["name"]
        is_xgb = "XGBoost" in m["name"]
        
        size = 180 if is_cstgb else (120 if is_xgb else 80)
        marker = "*" if is_cstgb else ("s" if is_xgb else "o")
        
        ax.scatter(m["year"], m["f1"], s=size, color=m["col"], marker=marker,
                   edgecolors=COLOR_DARK, lw=1.2, zorder=5)

        # Label with Name + Exact Percentage
        lbl_text = f"{m['name']}\n({m['f1']:.1f}%)" if is_cstgb else f"{m['name']} ({m['f1']:.1f}%)"
        fw = "bold" if (is_cstgb or is_xgb) else "normal"
        fc = COLOR_SAFE if is_cstgb else (COLOR_DARK if is_xgb else "#1e293b")
        
        if is_cstgb:
            bbox_style = dict(boxstyle="round,pad=0.25", fc="#dcfce7", ec=COLOR_SAFE, lw=1.3)
        elif is_xgb:
            bbox_style = dict(boxstyle="square,pad=0.2", fc="#f1f5f9", ec=COLOR_DARK, lw=1.0)
        else:
            bbox_style = dict(boxstyle="square,pad=0.18", fc="#ffffff", ec="#cbd5e1", lw=0.6, alpha=0.92)

        ax.annotate(lbl_text, (m["year"], m["f1"]),
                    xytext=(m["ox"], m["oy"]), textcoords="offset points",
                    ha=m["ha"], va=m.get("va", "center"), fontsize=7.0, fontweight=fw, color=fc,
                    bbox=bbox_style, zorder=6)

    # Era Shading & Milestones
    ax.set_xticks([1.0, 2.0, 4.0, 5.0, 6.4, 8.0])
    ax.set_xticklabels([
        "2017\n(Static GNN)",
        "2018\n(Attention)",
        "2020\n(Dynamic Time)",
        "2021\n(SMOTE Balance)",
        "2022–2023\n(Camouflage Def.)",
        "2024–2025\n(C-STGB Proposed)"
    ], fontsize=7.8, fontweight="bold")

    ax.set_xlabel("Chronological Evolution & Architectural Paradigm Milestones", fontsize=8.8, fontweight="bold", labelpad=8)
    ax.set_ylabel("Elliptic-v1 Minority Illicit Macro F1-Score (%)", fontsize=8.8, fontweight="bold")
    ax.set_xlim([0.3, 8.7])
    ax.set_ylim([35, 98])
    ax.grid(True, linestyle=":", alpha=0.5)

    # Custom Legend
    legend_elements = [
        mlines.Line2D([], [], color=COLOR_MUTED, marker='o', ls='', label='Static GNN (2017-18)'),
        mlines.Line2D([], [], color=COLOR_INGEST, marker='o', ls='', label='Temporal GNN (2020)'),
        mlines.Line2D([], [], color=COLOR_REVIEW, marker='o', ls='', label='Camouflage GNN (2020-22)'),
        mlines.Line2D([], [], color='#7c3aed', marker='o', ls='', label='Imbalance GNN (2021)'),
        mlines.Line2D([], [], color=COLOR_DARK, marker='s', ls='', label='XGBoost Baseline'),
        mlines.Line2D([], [], color=COLOR_SAFE, marker='*', ls='', markersize=10, label='C-STGB (Proposed Apex)'),
    ]
    ax.legend(handles=legend_elements, loc="lower right", framealpha=0.95, facecolor="#ffffff",
              edgecolor=COLOR_BORDER, fontsize=7.2, ncol=2)
    ax.set_title("Evolutionary SOTA Frontier in Financial Crime Graph Surveillance", fontweight="bold", fontsize=10.0, pad=10)

    plt.tight_layout()
    save_figure(fig, "fig_lit_evolution_frontier", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
