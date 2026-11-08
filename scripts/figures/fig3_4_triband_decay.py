"""
Figure 3.4: Tri-Band Continuous Harmonic Temporal Decay Comparison
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    fig, ax = plt.subplots(figsize=(7.2, 2.85), dpi=300)
    dt = np.linspace(0.01, 72.0, 500) # hours

    # Section 3.3.2 Decay Rates: lambda_b in {0.80, 0.05, 0.01}
    decay_fast = np.exp(-0.80 * dt)
    decay_slow = np.exp(-0.01 * dt)

    # C-STGB Tri-band harmonic attention weight
    w_burst = np.exp(-0.80 * dt)
    w_diurnal = np.exp(-0.05 * dt) * (0.6 + 0.4 * np.cos(2 * np.pi * dt / 24.0))
    w_macro = np.exp(-0.01 * dt)
    w_triband = 0.45 * w_burst + 0.35 * w_diurnal + 0.20 * w_macro
    w_triband = np.clip(w_triband, 0.0, 1.0)

    ax.plot(dt, decay_fast, label=r"Monolithic Fast Decay ($\lambda_1 = 0.80$)", color="#94a3b8", lw=1.5, ls="--")
    ax.plot(dt, decay_slow, label=r"Monolithic Slow Decay ($\lambda_3 = 0.01$)", color="#64748b", lw=1.5, ls=":")
    ax.plot(dt, w_triband, label=r"C-STGB Tri-Band Harmonic Attention $w(\Delta t)$ (Ours)", color="#047857", lw=2.2)

    # Vertical Harmonic Resonance Lines (bounded below legend to prevent collision)
    ax.plot([24.0, 24.0], [0, 0.85], color="#1e40af", linestyle="-.", alpha=0.7, lw=1.1)
    ax.text(24.4, 0.65, "24h Diurnal\nResonance", fontsize=7.2, color="#1e40af", fontweight="bold")

    ax.plot([48.0, 48.0], [0, 0.55], color="#1e40af", linestyle="-.", alpha=0.7, lw=1.1)
    ax.text(48.4, 0.35, "48h Harmonic\nResonance", fontsize=7.2, color="#1e40af", fontweight="bold")

    ax.set_xlabel(r"Elapsed Inter-Event Time $\Delta t$ (Hours)", fontsize=9.0, fontweight="bold")
    ax.set_ylabel(r"Attention Weight $w(\Delta t)$", fontsize=9.0, fontweight="bold")
    ax.set_xlim([0, 80])
    ax.set_ylim([0, 1.15])
    ax.grid(True, linestyle=":", alpha=0.5)
    
    # Legend in upper right, well clear of harmonic markers
    ax.legend(loc="upper right", framealpha=0.96, fontsize=7.6, edgecolor="#cbd5e1")
    ax.set_title(r"Multi-Scale Tri-Band Continuous Harmonic Decay vs. Monolithic Exponential Baselines",
                 fontweight="bold", fontsize=9.5, pad=10)
    plt.tight_layout()

    save_figure(fig, "fig_triband_decay_comparison", pad_inches=0.15)
    plt.close(fig)

if __name__ == "__main__":
    generate()
