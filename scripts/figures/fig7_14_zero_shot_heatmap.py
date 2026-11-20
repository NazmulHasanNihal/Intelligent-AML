"""
Figure 7.14: Zero-Shot Cross-Domain Generalization on Frozen Weights
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    print("13. GENERATING ZERO-SHOT CROSS-DOMAIN TRANSFER HEATMAP (Ch 7)")
    print("======================================================================")
    fig, ax = plt.subplots(figsize=(8.20, 3.40))
    
    pairs = [
        "Elliptic-v1 -> Elliptic-v2",
        "Elliptic-v1 -> SAML-D",
        "Elliptic-v1 -> PaySim Ext.",
        "PaySim Ext. -> IBM HI Med",
        "PaySim Ext. -> SAML-D",
        "DGraphFin -> Elliptic-v1",
        "SAML-D -> IBM HI Med",
        "XBlock-ETH -> DGraphFin"
    ]
    hgt_zs =    [21.40, 14.20, 16.80, 18.50, 22.10, 19.40, 15.20, 28.50]
    xgb_zs =    [64.20, 58.10, 61.40, 31.40, 56.80, 62.80, 28.60, 69.20]
    cstgb_zs =  [82.40, 76.80, 79.20, 41.80, 74.50, 80.60, 39.40, 85.10]
    target_f1 = [99.10, 93.68, 92.40, 46.85, 93.68, 91.42, 46.85, 94.62]
    
    x_p = np.arange(len(pairs))
    w_p = 0.20
    
    ax.bar(x_p - 1.5*w_p, hgt_zs, width=w_p, color="#b91c1c", edgecolor="black", lw=0.5, label="Vanilla HGT (eta=0)")
    ax.bar(x_p - 0.5*w_p, xgb_zs, width=w_p, color="#1e40af", edgecolor="black", lw=0.5, label="XGBoost (eta=0)")
    ax.bar(x_p + 0.5*w_p, cstgb_zs, width=w_p, color="#15803d", edgecolor="black", lw=0.6, label="C-STGB Zero-Shot (eta=0)")
    ax.bar(x_p + 1.5*w_p, target_f1, width=w_p, color="#94a3b8", edgecolor="black", lw=0.5, label="Target-Tuned Upper Bound")
    
    ax.set_ylabel("Minority F1 (%)", fontsize=8.5, fontweight="bold")
    ax.set_title("Frozen-Weight Zero-Shot Transfer Matrix across 8 Cross-Domain Source-Target Pairs", fontweight="bold", fontsize=9.2, pad=25)
    ax.set_xticks(x_p)
    ax.set_xticklabels(pairs, rotation=30, ha="right", fontsize=7.0, fontweight="bold")
    ax.set_ylim([0, 115])
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=4, fontsize=6.8, framealpha=0.95, edgecolor="#cbd5e1")
    
    for i in range(len(pairs)):
        ax.annotate(f"{cstgb_zs[i]:.1f}%", (x_p[i] + 0.5*w_p, cstgb_zs[i]), xytext=(0, 2), textcoords="offset points",
                    ha="center", va="bottom", fontsize=5.4, fontweight="bold", color="#15803d")
    
    plt.tight_layout()
    save_figure(fig, "fig_zero_shot_transfer_heatmap", pad_inches=0.12)
    save_figure(fig, "fig_transfer_matrix_heatmap", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
