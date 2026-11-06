"""
scripts/redesign_fig3_5_triband_spectrum.py
Publication-grade redesign of Figure 3.5:
- Top title given full vertical margin clearance (zero horizontal slice)
- Band 1 peaks fully unclipped (ylim upper bound set to 1.35)
- Band 2 wave labels placed comfortably above wave crests
- Exported with pad_inches=0.15 across all target directories
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 8.8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'stix',
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "reports" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
]

def generate_fig3_5():
    t = np.linspace(0, 168, 1000) # 7-day observation window (hours)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7.6, 5.0), sharex=True, dpi=300)

    # Band 1: Micro-burst (tau = 2.4 h)
    burst_signal = np.zeros_like(t)
    burst_centers = [12, 14, 15.5, 60, 61, 120]
    for bc in burst_centers:
        burst_signal += 1.05 * np.exp(-((t - bc) / 1.2)**2)
    burst_signal = np.clip(burst_signal, 0, 1.20)
    ax1.plot(t, burst_signal, color="#dc2626", lw=1.3)
    ax1.fill_between(t, 0, burst_signal, color="#fee2e2", alpha=0.65)
    ax1.set_ylabel(r"Band 1 ($\tau_1 = 2.4\,\mathrm{h}$)", fontsize=7.6, fontweight="bold", color="#991b1b")
    ax1.text(0.98, 0.80, "Micro-Burst Smurfing & Rapid Structuring Peaks", transform=ax1.transAxes,
             ha="right", va="center", fontsize=7.0, color="#991b1b", fontweight="bold")
    ax1.set_ylim(0, 1.35)
    ax1.grid(True, linestyle=":", alpha=0.5)

    # Band 2: Circadian / Diurnal (tau = 24 h)
    circadian_signal = 0.50 + 0.40 * np.sin(2 * np.pi * t / 24.0 - np.pi/2)
    ax2.plot(t, circadian_signal, color="#2563eb", lw=1.3)
    ax2.fill_between(t, 0, circadian_signal, color="#dbeafe", alpha=0.65)
    ax2.set_ylabel(r"Band 2 ($\tau_2 = 24\,\mathrm{h}$)", fontsize=7.6, fontweight="bold", color="#1d4ed8")
    ax2.text(0.98, 0.82, "Circadian Business Hours & Diurnal Banking Clearing", transform=ax2.transAxes,
             ha="right", va="center", fontsize=7.0, color="#1d4ed8", fontweight="bold")
    ax2.set_ylim(0, 1.25)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Band 3: Macro Dormancy (tau = 168 h / 90 Days)
    macro_signal = np.exp(-t / 168.0)
    ax3.plot(t, macro_signal, color="#7c3aed", lw=1.3)
    ax3.fill_between(t, 0, macro_signal, color="#f3e8ff", alpha=0.65)
    ax3.set_ylabel(r"Band 3 ($\tau_3 = 168\,\mathrm{h}$)", fontsize=7.6, fontweight="bold", color="#6d28d9")
    ax3.text(0.98, 0.80, "90-Day Dormant Hibernation Holding Chains", transform=ax3.transAxes,
             ha="right", va="center", fontsize=7.0, color="#6d28d9", fontweight="bold")
    ax3.set_ylim(0, 1.25)
    ax3.grid(True, linestyle=":", alpha=0.5)

    # Combined Kernel Response vs Standard Decay
    cstgb_unified = 0.35 * burst_signal + 0.35 * circadian_signal + 0.30 * macro_signal
    std_decay = np.exp(-t / 6.0)
    ax4.plot(t, cstgb_unified, color="#0f172a", lw=1.8, label="C-STGB Unified Tri-Band Attention Bank (Sustained Sensitivity)")
    ax4.plot(t, std_decay, color="#94a3b8", lw=1.4, linestyle="--", label=r"Conventional Single Decay (Vanishes after 12h: Hibernation Blindness)")
    ax4.set_ylabel(r"Kernel $\psi(\Delta t)$", fontsize=7.6, fontweight="bold")
    ax4.set_xlabel(r"Elapsed Time Window $\Delta t$ (Hours across 7-Day Observation Horizon)", fontsize=8.2, fontweight="bold")
    ax4.legend(fontsize=7.2, loc="upper right", framealpha=0.95, edgecolor="#cbd5e1")
    ax4.set_ylim(0, 1.25)
    ax4.grid(True, linestyle=":", alpha=0.5)

    fig.suptitle("C-STGB Tri-Band Harmonic Temporal Attention Spectrum: Bridging Microsecond Bursts & 90-Day Dormancy",
                 fontsize=9.2, fontweight="bold", y=0.98)
    fig.subplots_adjust(top=0.93, bottom=0.09, left=0.12, right=0.97, hspace=0.18)

    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in [".pdf", ".png"]:
            out_file = d / f"fig_triband_waveform_spectrum{ext}"
            fig.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
            print(f"Saved: {out_file}")

    plt.close()

if __name__ == "__main__":
    generate_fig3_5()

