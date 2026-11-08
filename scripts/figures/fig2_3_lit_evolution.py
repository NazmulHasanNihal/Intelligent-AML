"""
Figure 2.3: 2D Financial Crime Graph Learning Evolution Frontier
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, ax = plt.subplots(figsize=(8.2, 4.8), dpi=300)

    # Baselines data
    models = [
        ("GCN", 15, 43.55, "#94a3b8", "Static"),
        ("GraphSAGE", 25, 48.20, "#94a3b8", "Static"),
        ("EvolveGCN", 35, 51.04, "#38bdf8", "Discrete Dynamic"),
        ("GAT", 30, 52.40, "#94a3b8", "Static Attn"),
        ("CARE-GNN", 40, 64.50, "#f59e0b", "Camouflage Filter"),
        ("TGN", 65, 68.40, "#3b82f6", "Continuous Dynamic"),
        ("TGAT", 60, 67.20, "#3b82f6", "Continuous Dynamic"),
        ("H2-IDE", 43, 74.00, "#f59e0b", "Heterophily"),
        ("CamFD", 51, 83.00, "#f59e0b", "Camouflage Contrast"),
        ("GraphSMOTE", 55, 78.40, "#a855f7", "Imbalance SMOTE"),
        ("XGBoost", 20, 88.35, "#64748b", "Tabular Baseline"),
        ("C-STGB (Ours)", 92, 91.42, "#dc2626", "Proposed Framework")
    ]

    for name, x, y, color, tag in models:
        s = 200 if "C-STGB" in name else (130 if "XGBoost" in name else 85)
        ax.scatter(x, y, s=s, color=color, edgecolor="black", lw=1.0, zorder=5)
        
        # Staggered offsets for zero collision
        ox, oy = 2.0, 1.5
        if name == "H2-IDE": ox, oy = -14.0, 2.0
        elif name == "CamFD": ox, oy = -14.0, 2.0
        elif name == "TGN": ox, oy = 2.0, -3.5
        elif name == "TGAT": ox, oy = -16.0, 1.5
        elif name == "C-STGB (Ours)": ox, oy = -40.0, 2.2
        elif name == "XGBoost": ox, oy = 2.5, -3.5
        
        fw = "bold" if "C-STGB" in name else "normal"
        ax.annotate(name, (x, y), xytext=(x + ox, y + oy), fontsize=7.2, fontweight=fw)

    # Evolution arrows
    ax.annotate("", xy=(33, 50), xytext=(20, 44), arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=1.2, ls="--"))
    ax.annotate("", xy=(62, 67), xytext=(38, 52), arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.2, ls="--"))
    ax.annotate("", xy=(88, 90), xytext=(68, 70), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.6))

    ax.set_xlabel(r"Spatio-Temporal Topological Expressiveness Rating $\longrightarrow$", fontsize=9.0, fontweight="bold")
    ax.set_ylabel(r"Elliptic-v1 Minority Illicit F1-Score (%) $\longrightarrow$", fontsize=9.0, fontweight="bold")
    ax.set_xlim([10, 100])
    ax.set_ylim([35, 96])
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_title("Evolutionary SOTA Frontier in Graph Financial Crime Surveillance", fontweight="bold", fontsize=10.0, pad=10)

    save_figure(fig, "fig_lit_evolution_frontier", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
