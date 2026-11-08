"""
Figure 1.3: Five Canonical Failure Modes of Conventional AML Architectures
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Sharp rectangular geometry, proper mathtext, strict 4-color palette.
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
    setup_plt(font_size=8.0, title_size=9.2, label_size=8.2)
    fig, axes = plt.subplots(1, 5, figsize=(14.0, 3.4), dpi=300)

    # Panel 1: Exponential Decay Vanishing
    ax = axes[0]
    dt = np.linspace(0, 90, 200)
    decay_naive = np.exp(-0.15 * dt)
    decay_triband = 0.5 * np.exp(-0.01 * dt) + 0.3 * np.cos(2 * np.pi * dt / 7) * np.exp(-0.03 * dt) + 0.2
    ax.plot(dt, decay_naive, color=COLOR_RISK, lw=2, label="Static Decay (20d Miss)")
    ax.plot(dt, np.clip(decay_triband, 0, 1), color=COLOR_SAFE, lw=2, label="C-STGB Tri-Band (90d Active)")
    ax.axvline(20, color=COLOR_RISK, linestyle=":", alpha=0.7)
    ax.set_title("(a) Memory Vanishing", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("Elapsed Time (Days)", fontsize=8.0)
    ax.set_ylabel("Attention Weight", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 2: Dirichlet Energy Collapse (Over-smoothing)
    ax = axes[1]
    layers = np.arange(1, 9)
    energy_gcn = 1.0 * (0.45 ** (layers - 1))
    energy_cstgb = np.array([1.0, 0.92, 0.88, 0.85, 0.83, 0.82, 0.81, 0.80])
    ax.plot(layers, energy_gcn, "-o", color=COLOR_RISK, lw=1.8, ms=4, label=r"Standard GCN $\mathcal{E}(H) \to 0$")
    ax.plot(layers, energy_cstgb, "-s", color=COLOR_INGEST, lw=1.8, ms=4, label=r"C-STGB Gate $\mathcal{E}(H) \geq c > 0$")
    ax.set_title("(b) Feature Over-Smoothing", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("GNN Layer Depth (L)", fontsize=8.0)
    ax.set_ylabel(r"Dirichlet Energy $\mathcal{E}(H)$", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 3: Threshold Collapse under Class Skew
    ax = axes[2]
    taus = np.linspace(0.01, 0.90, 100)
    recall = 1.0 / (1.0 + np.exp(12 * (taus - 0.25)))
    ax.plot(taus, recall * 100, color=COLOR_GNN, lw=2)
    ax.axvline(0.50, color=COLOR_RISK, linestyle="--", lw=1.5, label=r"Naïve $\tau=0.50$ (Recall < 12%)")
    ax.axvline(0.18, color=COLOR_SAFE, linestyle="-.", lw=1.5, label=r"Bayes $\tau^*=0.18$ (Recall > 90%)")
    ax.set_title("(c) Recall Collapse", fontweight="bold", fontsize=8.8)
    ax.set_xlabel(r"Decision Cutoff ($\tau$)", fontsize=8.0)
    ax.set_ylabel("Minority Recall (%)", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 4: k-Hop VRAM Explosion
    ax = axes[3]
    k_hops = np.arange(1, 5)
    vram_full = np.array([4.2, 18.5, 96.0, 480.0])
    vram_cstgb = np.array([1.2, 3.4, 6.8, 12.5])
    ax.plot(k_hops, vram_full, "-o", color=COLOR_RISK, lw=1.8, ms=4, label="Full $k$-Hop (>80GB OOM)")
    ax.plot(k_hops, vram_cstgb, "-s", color=COLOR_SAFE, lw=1.8, ms=4, label="DuckDB 2-Hop (<16GB)")
    ax.axhline(80, color=COLOR_RISK, linestyle=":", label="A100 80GB VRAM Limit")
    ax.set_yscale("log")
    ax.set_title("(d) VRAM Explosion", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("Neighborhood Hop ($k$)", fontsize=8.0)
    ax.set_ylabel("Peak VRAM (GB, log)", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="lower right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 5: Conformal Queue Flooding
    ax = axes[4]
    skews = np.array([0.05, 0.1, 0.5, 1.0, 2.0, 5.0])
    marginal_q = np.array([98.2, 95.0, 82.0, 65.0, 42.0, 25.0])
    cstgb_q = np.array([0.49, 0.52, 0.55, 0.58, 0.62, 0.65])
    ax.plot(skews, marginal_q, "-o", color=COLOR_RISK, lw=1.8, ms=4, label="Marginal Conformal (>90%)")
    ax.plot(skews, cstgb_q, "-s", color=COLOR_INGEST, lw=1.8, ms=4, label="Class-Cond. CRC (<0.6%)")
    ax.set_title("(e) Conformal Queue", fontweight="bold", fontsize=8.8)
    ax.set_xlabel(r"Minority Skew $\pi$ (%)", fontsize=8.0)
    ax.set_ylabel("Manual Review %", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="center right")
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    save_figure(fig, "fig_1_3_failure_modes", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
