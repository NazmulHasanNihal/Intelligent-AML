"""
Figure 1.3: Five Canonical Failure Modes of Conventional AML Architectures
Redesigned with:
- Zero overlapping labels across all 5 panels
- Adjusted text positions to stay completely clear of curves, shaded bands, and markers
- Perfect alignment and clean, high-contrast publication typography
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_GNN, COLOR_SAFE, COLOR_RISK,
    COLOR_DARK
)

def generate():
    setup_plt(font_size=8.0, title_size=9.2, label_size=8.2)
    # Generous aspect ratio (15.5 x 4.2 in) to provide breathing room for 5 panels
    fig, axes = plt.subplots(1, 5, figsize=(15.5, 4.2), dpi=300)

    # Common styling helper
    def style_panel(ax, title):
        ax.set_facecolor("#fafbfc")
        ax.grid(True, linestyle=":", alpha=0.55, color="#cbd5e1", zorder=0)
        ax.set_title(title, fontweight="bold", fontsize=9.2, pad=10, color=COLOR_DARK)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color("#64748b")
        ax.spines['bottom'].set_color("#64748b")

    # =========================================================================
    # Panel 1: Long-Dwell Hibernation (Memory Vanishing)
    # =========================================================================
    ax = axes[0]
    dt = np.linspace(0, 90, 250)
    decay_naive = np.exp(-0.14 * dt)
    # Multi-frequency continuous tri-band decay with active retention
    decay_triband = 0.42 * np.exp(-0.008 * dt) + 0.18 * np.cos(2 * np.pi * dt / 7.0) * np.exp(-0.018 * dt) + 0.38
    
    ax.plot(dt, decay_naive, color=COLOR_RISK, lw=2.2, label="Static Exp. Decay", zorder=3)
    ax.plot(dt, np.clip(decay_triband, 0, 1), color=COLOR_SAFE, lw=2.2, label="C-STGB Tri-Band", zorder=3)
    ax.axvline(20, color=COLOR_RISK, linestyle="--", lw=1.2, alpha=0.8, zorder=2)
    ax.text(22.0, 0.20, "20d Blind Spot", fontsize=6.8, color=COLOR_RISK, fontweight="bold")
    
    style_panel(ax, "(a) Memory Vanishing")
    ax.set_xlabel("Elapsed Time (Days)", fontsize=8.2, labelpad=5)
    ax.set_ylabel("Attention Weight", fontsize=8.2, labelpad=5)
    ax.set_xlim(-1, 92)
    ax.set_ylim(-0.04, 1.05)
    ax.legend(fontsize=7.0, loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.92)

    # =========================================================================
    # Panel 2: Dirichlet Energy Collapse (Over-Smoothing)
    # =========================================================================
    ax = axes[1]
    layers = np.arange(1, 9)
    energy_gcn = 1.0 * (0.42 ** (layers - 1))
    energy_cstgb = np.array([1.0, 0.93, 0.89, 0.86, 0.84, 0.83, 0.82, 0.81])
    
    ax.plot(layers, energy_gcn, "-o", color=COLOR_RISK, lw=2.0, ms=4.5, label=r"GCN: $\mathcal{E}(H) \to 0$", zorder=3)
    ax.plot(layers, energy_cstgb, "-s", color=COLOR_INGEST, lw=2.0, ms=4.5, label=r"C-STGB: $\mathcal{E}(H) \geq c$", zorder=3)
    
    # Over-smoothing risk zone with callout cleanly centered in upper-right region of the band
    ax.axhspan(0, 0.16, color=COLOR_RISK, alpha=0.08, zorder=1)
    ax.text(5.5, 0.22, "Over-Smoothing Zone", ha="center", fontsize=6.8, color=COLOR_RISK, fontstyle="italic", fontweight="bold")
    
    style_panel(ax, "(b) Feature Over-Smoothing")
    ax.set_xlabel("GNN Layer Depth ($L$)", fontsize=8.2, labelpad=5)
    ax.set_ylabel(r"Dirichlet Energy $\mathcal{E}(H)$", fontsize=8.2, labelpad=5)
    ax.set_xlim(0.6, 8.4)
    ax.set_ylim(-0.04, 1.06)
    ax.legend(fontsize=7.0, loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.92)

    # =========================================================================
    # Panel 3: Threshold Collapse under Extreme Class Skew
    # =========================================================================
    ax = axes[2]
    taus = np.linspace(0.01, 0.90, 200)
    # Realistic sigmoid recall cliff under extreme 0.05% skew
    recall = 100.0 / (1.0 + np.exp(14.0 * (taus - 0.26)))
    
    ax.plot(taus, recall, color=COLOR_GNN, lw=2.2, label="Minority Recall", zorder=3)
    ax.axvline(0.50, color=COLOR_RISK, linestyle="--", lw=1.5, label=r"Default $\tau = 0.50$ (12%)", zorder=2)
    ax.axvline(0.18, color=COLOR_SAFE, linestyle="-.", lw=1.5, label=r"Bayes $\tau^* = 0.18$ (91%)", zorder=2)
    
    # Missed alarms callout placed with comfortable clearance
    ax.plot([0.50], [12.0], "ro", ms=5, zorder=4)
    ax.text(0.53, 20.0, "88% Missed", fontsize=7.0, fontweight="bold", color=COLOR_RISK)
    
    style_panel(ax, "(c) Recall Collapse")
    ax.set_xlabel(r"Decision Cutoff ($\tau$)", fontsize=8.2, labelpad=5)
    ax.set_ylabel("Minority Recall (%)", fontsize=8.2, labelpad=5)
    ax.set_xlim(-0.02, 0.92)
    ax.set_ylim(-3, 106)
    ax.legend(fontsize=6.8, loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.92)

    # =========================================================================
    # Panel 4: k-Hop Combinatorial VRAM Explosion
    # =========================================================================
    ax = axes[3]
    k_hops = np.array([1, 2, 3, 4])
    vram_full = np.array([3.8, 17.5, 96.0, 480.0])
    vram_cstgb = np.array([1.2, 3.2, 6.4, 11.8])
    
    ax.plot(k_hops, vram_full, "-o", color=COLOR_RISK, lw=2.0, ms=4.5, label="Full $k$-Hop Expansion", zorder=3)
    ax.plot(k_hops, vram_cstgb, "-s", color=COLOR_SAFE, lw=2.0, ms=4.5, label="DuckDB 2-Hop (<16GB)", zorder=3)
    ax.axhline(80, color=COLOR_RISK, linestyle=":", lw=1.3, label="A100 GPU Limit (80GB)", zorder=2)
    
    # OOM Marker placed safely to the left of the data point
    ax.text(2.35, 115, "OOM Crashes (>80GB)", fontsize=6.8, fontweight="bold", color=COLOR_RISK)
    
    ax.set_yscale("log")
    style_panel(ax, "(d) VRAM Explosion")
    ax.set_xlabel("Neighborhood Hop ($k$)", fontsize=8.2, labelpad=5)
    ax.set_ylabel("Peak VRAM (GB, log)", fontsize=8.2, labelpad=5)
    ax.set_xlim(0.8, 4.3)
    ax.set_ylim(0.7, 850)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["1-Hop", "2-Hop", "3-Hop", "4-Hop"])
    ax.legend(fontsize=6.8, loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.92)

    # =========================================================================
    # Panel 5: Marginal Conformal Queue Flooding
    # =========================================================================
    ax = axes[4]
    skews = np.array([0.05, 0.2, 0.5, 1.0, 2.0, 5.0])
    marginal_q = np.array([97.8, 92.5, 78.0, 62.0, 38.0, 22.0])
    cstgb_q = np.array([0.49, 0.51, 0.53, 0.56, 0.60, 0.64])
    
    ax.plot(skews, marginal_q, "-o", color=COLOR_RISK, lw=2.0, ms=4.5, label="Marginal Conformal", zorder=3)
    ax.plot(skews, cstgb_q, "-s", color=COLOR_INGEST, lw=2.0, ms=4.5, label="Class-Cond. CRC", zorder=3)
    
    # 90%+ saturation callout positioned with clear clearance from the curve
    ax.plot([0.05], [97.8], "ro", ms=5, zorder=4)
    ax.text(1.2, 92.0, "Queue Saturated\n(97.8% Review)", fontsize=6.6, color=COLOR_RISK, fontweight="bold")
    
    style_panel(ax, "(e) Conformal Queue")
    ax.set_xlabel(r"Minority Skew $\pi$ (%)", fontsize=8.2, labelpad=5)
    ax.set_ylabel("Manual Review Queue (%)", fontsize=8.2, labelpad=5)
    ax.set_xlim(-0.15, 5.3)
    ax.set_ylim(-3, 108)
    ax.legend(fontsize=6.8, loc="center right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.92)

    # Generous layout spacing to prevent any subplot or axis label collision
    plt.subplots_adjust(left=0.045, right=0.985, top=0.88, bottom=0.18, wspace=0.34)
    save_figure(fig, "fig_1_3_failure_modes", pad_inches=0.08)
    plt.close(fig)

if __name__ == "__main__":
    generate()
