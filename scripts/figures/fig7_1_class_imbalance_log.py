"""
Figure 7.1: Extreme Class Imbalance Distribution across 14 Financial Transaction Networks
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Sharp rectangular geometry, proper mathtext, strict 4-color palette, readable fonts (>=7.2pt).
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
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    datasets = [
        "Elliptic-v1", "Elliptic-v2", "XBlock-ETH", "MtGox",
        "SAML-D", "PaySim1", "PaySim Ext", "AMLSim HI-S", "AMLSim HI-M",
        "AMLSim LI-S", "AMLSim LI-M", "DataGen", "DGraphFin", "CreditCard"
    ]
    illicit_pct = [2.23, 0.85, 0.09, 1.82, 0.05, 0.13, 0.13, 0.23, 0.23, 0.75, 0.75, 1.50, 1.30, 0.17]

    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=300)
    x = np.arange(len(datasets))
    
    # 3 Archetype groups: Group A (Crypto: Blue), Group B (Banking/FinTech: Teal), Group C (Cards: Red)
    colors = [COLOR_INGEST if i < 4 else COLOR_GNN if i < 13 else COLOR_RISK for i in range(len(datasets))]

    bars = ax.bar(x, illicit_pct, color=colors, edgecolor=COLOR_DARK, lw=0.8, alpha=0.90, width=0.62)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=38, ha="right", fontsize=7.8, fontweight="bold")
    ax.set_ylabel(r"Illicit Ratio $\pi$ (%) [$\log_{10}$ scale]", fontsize=8.8, fontweight="bold")
    ax.set_ylim([0.02, 18.0])
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)

    for i, bar in enumerate(bars):
        h = bar.get_height()
        # Stagger vertical offset for adjacent bars with identical heights to prevent collisions
        y_offset = 12 if (i in [6, 8, 10, 12]) else 3
        ax.annotate(f"{h:.2f}%", (bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, y_offset), textcoords="offset points", ha="center", va="bottom",
                    fontsize=7.2, fontweight="bold", color=colors[i])

    legend_elements = [
        mlines.Line2D([], [], color=COLOR_INGEST, marker='s', ls='', label='Group A (Crypto / Blockchain)'),
        mlines.Line2D([], [], color=COLOR_GNN, marker='s', ls='', label='Group B (Banking / FinTech Rails)'),
        mlines.Line2D([], [], color=COLOR_RISK, marker='s', ls='', label='Group C (Credit Card Transactions)'),
    ]
    ax.legend(handles=legend_elements, loc="upper right", framealpha=0.95, edgecolor=COLOR_BORDER, fontsize=7.6, ncol=3)
    ax.set_title(r"Extreme Class Imbalance (Illicit Ratio $\pi$) across 14 Financial Transaction Networks",
                 fontweight="bold", fontsize=9.8, pad=9)
    plt.tight_layout()
    save_figure(fig, "fig_class_imbalance_log", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
