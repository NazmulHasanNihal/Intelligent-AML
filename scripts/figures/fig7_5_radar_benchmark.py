"""
Figure 7.5: 14-Dataset Multi-Criteria Radar Benchmark
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Perfect geometric alignment, no label clipping or radial collision.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    categories = [
        'PR-AUC (Mean)', 
        'Illicit F1 (Elliptic)', 
        'Recall (Catch Rate)', 
        'Imbalance Robustness', 
        'Camouflage Retention', 
        'Banking SLA Compl.'
    ]
    N = len(categories)
    
    # 6 axes evenly spaced; start at top (pi/2) going clockwise
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.0, 5.2), subplot_kw=dict(polar=True), dpi=300)
    
    # Set top at 12 o'clock and direction clockwise
    ax.set_theta_offset(np.pi / 2.0)
    ax.set_theta_direction(-1)

    cstgb_vals = [93.1, 91.4, 90.1, 98.5, 96.8, 100.0]
    cstgb_vals += cstgb_vals[:1]

    xgb_vals = [88.5, 88.4, 85.2, 72.0, 60.5, 98.0]
    xgb_vals += xgb_vals[:1]

    care_vals = [68.0, 64.5, 58.0, 68.0, 84.5, 24.1]
    care_vals += care_vals[:1]

    hgt_vals = [76.4, 48.2, 55.0, 52.0, 48.2, 45.0]
    hgt_vals += hgt_vals[:1]

    # Plot filled polygon for C-STGB
    ax.plot(angles, cstgb_vals, color=COLOR_SAFE, linewidth=2.4, label='C-STGB (Ours)', zorder=4)
    ax.fill(angles, cstgb_vals, color=COLOR_SAFE, alpha=0.20, zorder=3)

    # Plot baseline lines
    ax.plot(angles, xgb_vals, color=COLOR_INGEST, linewidth=1.7, linestyle='-', label='XGBoost Baseline', zorder=4)
    ax.plot(angles, care_vals, color=COLOR_RISK, linewidth=1.5, linestyle='--', label='CARE-GNN', zorder=4)
    ax.plot(angles, hgt_vals, color=COLOR_GNN, linewidth=1.5, linestyle='-.', label='Vanilla HGT', zorder=4)

    # Grid and limits
    ax.set_ylim(0, 105)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=6.8, color='#64748b')
    # Position radial labels between axes (e.g. 30 degrees) with clean white background pill
    ax.set_rlabel_position(30)
    for t in ax.get_yticklabels():
        t.set_bbox(dict(boxstyle="round,pad=0.15", fc="#ffffff", ec="#cbd5e1", lw=0.5, alpha=0.9))
        t.set_zorder(6)

    # Configure X ticks and labels with explicit alignment
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])  # Clear default labels to place manually with exact alignment

    # Place each category label with perfect horizontal & vertical alignment and padding
    alignments = [
        ('center', 'bottom', 113.0),   # 0: Top (PR-AUC)
        ('left',   'center', 110.0),   # 1: Top-Right (Illicit F1)
        ('left',   'top',    110.0),   # 2: Bottom-Right (Recall)
        ('center', 'top',    113.0),   # 3: Bottom (Imbalance Robustness)
        ('right',  'top',    110.0),   # 4: Bottom-Left (Camouflage Retention)
        ('right',  'center', 110.0),   # 5: Top-Left (Banking SLA Compl.)
    ]

    for angle, cat, (ha, va, r_pos) in zip(angles[:-1], categories, alignments):
        ax.text(
            angle, r_pos, cat,
            ha=ha, va=va,
            fontsize=7.8, fontweight='bold', color='#1e293b',
            zorder=7
        )

    # Subtle circular grid styling
    ax.grid(color='#cbd5e1', linestyle='--', linewidth=0.7, alpha=0.8)
    ax.spines['polar'].set_color('#94a3b8')
    ax.spines['polar'].set_linewidth(0.8)

    ax.set_title("14-Dataset Multi-Criteria Radar Benchmark", fontweight="bold", fontsize=9.6, y=1.14)
    ax.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, -0.22),
        framealpha=0.95,
        edgecolor=COLOR_BORDER,
        fontsize=7.4,
        ncol=2
    )

    plt.subplots_adjust(top=0.86, bottom=0.18, left=0.12, right=0.88)
    save_figure(fig, "fig7_multi_dataset_radar", pad_inches=0.10)
    save_figure(fig, "fig7_5_radar_benchmark", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
