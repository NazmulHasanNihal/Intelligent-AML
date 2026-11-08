"""
Figure 3.7: Gradient Magnitude Dynamics of Cost-Sensitive Focal Tversky Loss
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    p = np.linspace(0.001, 0.999, 500)
    beta_fn, beta_fp = 0.85, 0.15

    grad_illicit_c_stgb = beta_fn * p * (1 - p) / (p + beta_fn * (1 - p))**2
    grad_illicit_bce    = (1 - p) * 0.18
    grad_benign_c_stgb  = beta_fp * p * (1 - p) / ((1 - p) + beta_fp * p)**2

    fig, ax = plt.subplots(figsize=(8.8, 4.2), dpi=300)
    ax.plot(p, grad_illicit_c_stgb, color="#DC2626", linewidth=2.5,
            label=r"C-STGB Illicit Gradient ($y_i=1, \beta_{FN}=0.85$) — 5.67x Boost")
    ax.plot(p, grad_benign_c_stgb, color="#2563EB", linewidth=2.0, linestyle="--",
            label=r"C-STGB Benign Gradient ($y_i=0, \beta_{FP}=0.15$)")
    ax.plot(p, grad_illicit_bce, color="#64748B", linewidth=1.8, linestyle=":",
            label=r"Standard Cross-Entropy ($\tau=0.50$, Recall Collapse)")

    ax.axvline(0.18, color="#15803D", linestyle="-.", linewidth=1.5,
               label=r"Calibrated Bayes Threshold ($\tau^* = 0.18$)")
    ax.set_xlabel(r"Predicted Anomaly Probability $p_i = \sigma(z_i)$", fontsize=9.5, fontweight="bold")
    ax.set_ylabel(r"Gradient Magnitude $|\partial \mathcal{L}_{\mathrm{task}} / \partial z_i|$", fontsize=9.5, fontweight="bold")
    ax.set_title("Asymmetric Focal Tversky Gradient Dynamics (Eq. 3.29: 5.67x FN Penalty)", fontsize=10.5, fontweight="bold")
    ax.legend(loc="upper right", frameon=True, fontsize=8.0)
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    save_figure(fig, "fig_3_10_gradient_dynamics", pad_inches=0.12)
    plt.close()

# ==============================================================================
# 4. Figure 4.3: Zero-Lookahead Causal Slicing
# ==============================================================================


if __name__ == "__main__":
    generate()
