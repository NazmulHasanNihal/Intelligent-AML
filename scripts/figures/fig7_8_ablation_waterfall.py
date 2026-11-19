"""
Figure 7.8: Stepwise Cumulative Architectural Ablation Progression on Elliptic-v1
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Sharp rectangular geometry, proper mathtext, strict 4-color palette, readable fonts (>=7.2pt).
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_REVIEW, COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=300)

    steps = [
        r"Base GCN (Bayes $\tau^*$)",
        r"+ 12-D Invariants",
        r"+ Hawkes Temporal",
        r"+ Edge Gate ($\hat{g}_{ij} \geq 0.10$)",
        r"+ GraphSMOTE",
        r"+ Adaptive Fusion",
        r"+ Bayes Risk Head",
        r"Full C-STGB"
    ]

    deltas = [26.40, 28.40, 13.70, 7.70, 9.92, 3.68, 1.62]

    bottoms = [0.0]
    heights = [deltas[0]]
    current = deltas[0]

    for d in deltas[1:]:
        bottoms.append(current)
        heights.append(d)
        current += d

    # Final summary bar
    bottoms.append(0.0)
    heights.append(current)

    # 4-color palette assignment
    colors_wf = [
        COLOR_MUTED,   # Base GCN
        COLOR_INGEST,  # +12-D Invariants (Blue)
        COLOR_GNN,     # +Hawkes Temporal (Teal)
        COLOR_INGEST,  # +Edge Gate (Blue)
        COLOR_REVIEW,  # +GraphSMOTE (Orange/Amber)
        COLOR_GNN,     # +Adaptive Fusion (Teal)
        COLOR_REVIEW,  # +Bayes Risk Head (Amber)
        COLOR_SAFE     # Full C-STGB (Green)
    ]

    x_pos = np.arange(len(steps))
    bars = ax.bar(x_pos, heights, bottom=bottoms, color=colors_wf, edgecolor=COLOR_DARK, lw=0.8, width=0.56)

    # Dotted guide lines
    for i in range(len(deltas) - 1):
        y_top = bottoms[i+1] + heights[i+1]
        ax.plot([x_pos[i+1] - 0.28, x_pos[i+2] + 0.28], [y_top, y_top], color=COLOR_MUTED, linestyle=":", lw=1.0)

    # Value annotations
    for i, (b, h) in enumerate(zip(bottoms, heights)):
        if i == 0:
            ax.text(x_pos[i], h + 1.8, f"{h:.2f}%", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=COLOR_DARK)
        elif i == len(steps) - 1:
            ax.text(x_pos[i], h + 1.8, f"{h:.2f}%\n(+65.02 pp)", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=COLOR_SAFE)
        else:
            ax.text(x_pos[i], b + h + 1.8, f"+{h:.2f}\n({b+h:.1f}%)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color=COLOR_DARK)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(steps, fontsize=7.4, rotation=32, ha="right", fontweight="bold")
    ax.set_ylabel("Elliptic-v1 Minority F1 Score (%)", fontsize=8.8, fontweight="bold")
    ax.set_ylim([0, 115])
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.set_title("Stepwise Cumulative Architectural Ablation Progression on Elliptic-v1",
                 fontweight="bold", fontsize=9.8, pad=9)

    plt.tight_layout()
    save_figure(fig, "fig_ablation_waterfall", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
