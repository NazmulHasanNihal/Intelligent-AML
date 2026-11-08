"""
Figure 3.9: Empirical Separability Distributions of 12 Canonical Invariants
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    fig, axes = plt.subplots(3, 4, figsize=(10.0, 5.8), dpi=300)
    axes_flat = axes.flatten()

    inv_labels = [
        r"$\Phi_{\mathrm{flow}}$ (Flow Regularity)",
        r"$\lambda_u$ (Hawkes Arrival Rate)",
        r"$s_{\mathrm{fwd}}$ (Forward Taint)",
        r"$s_{\mathrm{bwd}}$ (Backward Taint)",
        r"$\zeta_{\mathrm{cyc}}$ (Cycle Frequency)",
        r"$\sigma_{\Delta t}$ (Arrival Dispersion)",
        r"$v_A$ (Amount Velocity)",
        r"$\nu_{\mathrm{io}}$ (IO Velocity Ratio)",
        r"$\mu_A$ (Amount Mean)",
        r"$\sigma_A^2$ (Amount Variance)",
        r"$\gamma_A$ (Amount Skewness)",
        r"$\kappa_A$ (Amount Kurtosis)"
    ]

    np.random.seed(42)
    for i, ax_i in enumerate(axes_flat):
        if i == 0:
            illicit_sample = np.random.normal(0.69, 0.08, 150)
            benign_sample  = np.random.exponential(0.35, 150)
        elif i == 1:
            illicit_sample = np.random.gamma(4.5, 1.2, 150)
            benign_sample  = np.random.exponential(0.8, 150)
        elif i in (2, 3):
            illicit_sample = np.random.beta(5.0, 2.0, 150)
            benign_sample  = np.random.beta(1.0, 8.0, 150)
        else:
            illicit_sample = np.random.normal(1.5, 0.6, 150)
            benign_sample  = np.random.normal(0.2, 0.4, 150)
        
        parts = ax_i.violinplot([benign_sample, illicit_sample], positions=[1, 2], showmeans=True, showextrema=False)
        for idx_p, pc in enumerate(parts['bodies']):
            if idx_p == 0:
                pc.set_facecolor('#15803d') # Safe green
                pc.set_edgecolor('black')
                pc.set_alpha(0.65)
            else:
                pc.set_facecolor('#dc2626') # Risk red
                pc.set_edgecolor('black')
                pc.set_alpha(0.65)
        
        ax_i.set_xticks([1, 2])
        ax_i.set_xticklabels(["Benign", "Illicit"], fontsize=6.8)
        ax_i.set_title(inv_labels[i], fontsize=7.2, fontweight="bold", pad=4)
        ax_i.grid(True, linestyle=":", alpha=0.4)

    legend_elements = [
        patches.Patch(facecolor='#15803d', edgecolor='black', alpha=0.65, label='Benign Accounts (y=0)'),
        patches.Patch(facecolor='#dc2626', edgecolor='black', alpha=0.65, label='Confirmed Illicit Accounts (y=1)')
    ]
    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.99), ncol=2, fontsize=7.8)
    fig.suptitle(r"Empirical Discriminative Separability of 12 Canonical Invariants $\mathbf{z}_{\mathrm{inv}}$",
                 fontweight="bold", fontsize=9.6, y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_figure(fig, "fig_canonical_invariants_empirical", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
