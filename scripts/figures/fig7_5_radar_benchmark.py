"""
Figure 7.5: 14-Dataset Multi-Criteria Radar Benchmark
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
    categories = [
        'PR-AUC (Mean)', 
        'Illicit F1 (Elliptic)', 
        'Recall (Catch Rate)', 
        'Imbalance Robustness', 
        'Camouflage Retention', 
        'Banking SLA Compl.'
    ]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4.4, 4.8), subplot_kw=dict(polar=True), dpi=300)

    cstgb_vals = [93.1, 91.4, 90.1, 98.5, 96.8, 100.0]
    cstgb_vals += cstgb_vals[:1]

    xgb_vals = [88.5, 88.4, 85.2, 72.0, 60.5, 98.0]
    xgb_vals += xgb_vals[:1]

    care_vals = [68.0, 64.5, 58.0, 68.0, 84.5, 24.1]
    care_vals += care_vals[:1]

    hgt_vals = [76.4, 48.2, 55.0, 52.0, 48.2, 45.0]
    hgt_vals += hgt_vals[:1]

    ax.plot(angles, cstgb_vals, color=COLOR_SAFE, linewidth=2.4, label='C-STGB (Ours)')
    ax.fill(angles, cstgb_vals, color=COLOR_SAFE, alpha=0.22)

    ax.plot(angles, xgb_vals, color=COLOR_INGEST, linewidth=1.6, linestyle='-', label='XGBoost Baseline')
    ax.plot(angles, care_vals, color=COLOR_RISK, linewidth=1.5, linestyle='--', label='CARE-GNN')
    ax.plot(angles, hgt_vals, color=COLOR_GNN, linewidth=1.5, linestyle='-.', label='Vanilla HGT')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=7.6, fontweight="bold")
    ax.tick_params(pad=9)
    ax.set_ylim(0, 105)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=7.0, color='#64748b')
    ax.set_rlabel_position(35)
    ax.set_title("14-Dataset Multi-Criteria Radar Benchmark", fontweight="bold", fontsize=9.6, y=1.12)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.28), framealpha=0.94, edgecolor=COLOR_BORDER, fontsize=7.4, ncol=2)

    plt.subplots_adjust(top=0.86, bottom=0.22, left=0.10, right=0.90)
    save_figure(fig, "fig7_multi_dataset_radar", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
