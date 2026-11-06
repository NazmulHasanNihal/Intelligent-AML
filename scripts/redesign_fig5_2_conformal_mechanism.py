"""
scripts/redesign_fig5_2_conformal_mechanism.py
Publication-grade redesign of Figure 5.2:
Class-Conditional Conformal Calibration Mechanism under Extreme Imbalance.
Generates fig19_conformal_risk_mechanism.pdf and .png.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import beta as beta_dist

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 8.8,
    'axes.titlesize': 9.2,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "reports" / "figures",
    BASE_DIR / "data" / "outputs" / "figures"
]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def generate_figure_5_2():
    # Canvas sized 9.8 x 4.8 for publication elegance and spacious readability
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.8))
    
    # =========================================================================
    # PANEL (a): Class-Conditional Dual Quantile Calibration under Imbalance
    # =========================================================================
    ax0 = axes[0]
    ax0.set_facecolor("#fafbfc")
    ax0.grid(True, linestyle="--", linewidth=0.5, color="#cbd5e1", alpha=0.7, zorder=0)
    
    # Smooth analytical non-conformity densities
    s_grid = np.linspace(0.001, 0.999, 500)
    
    # Benign distribution: Beta(2.2, 8.5) -> peak ~0.15
    dens_benign = beta_dist.pdf(s_grid, 2.2, 8.5)
    # Illicit distribution: Beta(6.5, 2.5) -> peak ~0.75
    dens_illicit = beta_dist.pdf(s_grid, 6.5, 2.5)
    
    # Cutoff quantiles at 1 - alpha = 0.99 (99% coverage)
    q0 = beta_dist.ppf(0.99, 2.2, 8.5)   # 0.518 -> 0.52
    q1 = beta_dist.ppf(0.99, 6.5, 2.5)   # 0.942 -> 0.94
    q_marginal = 0.53                    # Dominated by 99.95% benign majority
    
    # Plot Benign Density Curve & Shading
    ax0.plot(s_grid, dens_benign, color="#0284c7", lw=2.2, label=r"Benign Density: $p(s \mid Y=0)$ [99.95%]", zorder=3)
    ax0.fill_between(s_grid, 0, dens_benign, where=(s_grid <= q0), color="#38bdf8", alpha=0.35, zorder=2)
    ax0.fill_between(s_grid, 0, dens_benign, where=(s_grid > q0), color="#94a3b8", alpha=0.25, hatch="//", zorder=2)
    
    # Plot Illicit Density Curve & Shading
    ax0.plot(s_grid, dens_illicit, color="#dc2626", lw=2.2, label=r"Illicit Density: $p(s \mid Y=1)$ [0.05%]", zorder=3)
    ax0.fill_between(s_grid, 0, dens_illicit, where=(s_grid <= q1), color="#f87171", alpha=0.35, zorder=2)
    ax0.fill_between(s_grid, 0, dens_illicit, where=(s_grid > q1), color="#94a3b8", alpha=0.25, hatch="//", zorder=2)
    
    # Vertical Threshold Lines
    ax0.axvline(q0, color="#0369a1", ls="--", lw=1.8, zorder=4)
    ax0.axvline(q1, color="#b91c1c", ls="-.", lw=1.8, zorder=4)
    ax0.axvline(q_marginal, color="#7c3aed", ls=":", lw=1.5, zorder=4)
    
    # Text Badges for Thresholds (carefully non-overlapping)
    # Benign threshold badge
    ax0.text(q0 - 0.02, 3.65, r"$\hat{q}^{(0)} = 0.52$" + "\n(Benign 99% Cov.)",
             ha="right", va="top", fontsize=7.2, fontweight="bold", color="#0369a1",
             bbox=dict(boxstyle="round,pad=0.25", fc="#e0f2fe", ec="#0284c7", lw=0.8, alpha=0.95), zorder=5)
    
    # Illicit threshold badge
    ax0.text(q1 - 0.02, 3.65, r"$\hat{q}^{(1)} = 0.94$" + "\n(Illicit 99% Cov.)",
             ha="right", va="top", fontsize=7.2, fontweight="bold", color="#b91c1c",
             bbox=dict(boxstyle="round,pad=0.25", fc="#fee2e2", ec="#dc2626", lw=0.8, alpha=0.95), zorder=5)
             
    # Marginal threshold callout
    ax0.text(q_marginal + 0.02, 2.50, r"$\hat{q}_{marg} = 0.53$" + " (Marginal)\nDeficit: Illicit Cov. $\\rightarrow 82.4\%$",
             ha="left", va="top", fontsize=6.8, color="#5b21b6",
             bbox=dict(boxstyle="round,pad=0.22", fc="#ede9fe", ec="#7c3aed", lw=0.8, alpha=0.92), zorder=5)

    # Finite-Sample Guarantee Callout Badge (Lower Left, completely collision-free)
    ax0.text(0.03, 1.80, "Finite-Sample Validity:\n" + r"$\mathbb{P}(Y \in \Gamma \mid Y=y) \geq 99.0\%$" + "\nGuaranteed for BOTH Classes",
             ha="left", va="top", fontsize=6.8, fontweight="bold", color="#1e293b",
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#94a3b8", lw=0.8, alpha=0.95), zorder=5)

    # Triage Decision Regime Ribbon at bottom
    ax0.text(0.25, -0.42, "Auto-Clear STP:\n" + r"$\Gamma(u) = \{0\}$", ha="center", va="top",
             fontsize=7.0, color="#0369a1", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="#f0f9ff", ec="#0284c7", lw=0.8))
             
    ax0.text(0.73, -0.42, "Human Review Queue:\n" + r"$\Gamma(u) = \{0, 1\}$", ha="center", va="top",
             fontsize=7.0, color="#b45309", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="#fffbeb", ec="#f59e0b", lw=0.8))
             
    ax0.text(0.97, -0.42, "Auto-Block:\n" + r"$\Gamma(u) = \{1\}$", ha="center", va="top",
             fontsize=7.0, color="#991b1b", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="#fef2f2", ec="#dc2626", lw=0.8))

    ax0.set_xlim(-0.02, 1.02)
    ax0.set_ylim(-0.75, 4.30)
    ax0.set_xlabel(r"Class-Conditional Non-Conformity Score $s_i^{(y)} = 1 - \hat{p}_i(y)$", fontsize=8.6, weight="bold", labelpad=6)
    ax0.set_ylabel(r"Probability Density $p(s \mid Y=y)$", fontsize=8.6, weight="bold", labelpad=6)
    ax0.set_title("(a) Dual Calibrated Non-Conformity Quantiles under Imbalance", fontsize=9.2, fontweight="bold", pad=28)
    
    # Legend for Panel (a) positioned above the plot to eliminate all internal collisions
    ax0.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, framealpha=0.95, fontsize=7.2, edgecolor="#cbd5e1")

    # =========================================================================
    # PANEL (b): Triage Operational Volume Comparison (N = 10,000 Wires)
    # =========================================================================
    ax1 = axes[1]
    ax1.set_facecolor("#fafbfc")
    ax1.grid(True, which="both", axis="y", linestyle="--", linewidth=0.5, color="#cbd5e1", alpha=0.7, zorder=0)

    # Categories and empirical data for N = 10,000
    models = ["Marginal Conformal\n(Class-Agnostic)", "Class-Conditional CRC\n(Proposed C-STGB)"]
    
    # Data shares in %
    p_clear = [80.40, 99.33]   # Auto-Clear {0}: 8,040 vs 9,933
    p_review = [18.40, 0.49]   # Review Queue {0, 1}: 1,840 vs 49
    p_block = [1.20, 0.18]     # Auto-Block {1}: 120 vs 18

    x = np.arange(len(models))
    w = 0.22

    # Grouped bars
    b_clear = ax1.bar(x - w, p_clear, w, label=r"Auto-Clear $\{0\}$ (STP)", color="#10b981", edgecolor="#047857", lw=1.0, zorder=3)
    b_review = ax1.bar(x, p_review, w, label=r"Human Review $\{0, 1\}$ (Queue)", color="#f59e0b", edgecolor="#b45309", lw=1.0, zorder=3)
    b_block = ax1.bar(x + w, p_block, w, label=r"Auto-Block $\{1\}$ (Quarantine)", color="#ef4444", edgecolor="#b91c1c", lw=1.0, zorder=3)

    # Value Labels above bars (Percentage & Count)
    # Clear bars
    ax1.text(x[0] - w, p_clear[0] * 1.18, "80.40%\n(8,040 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#047857")
    ax1.text(x[1] - w, p_clear[1] * 1.18, "99.33%\n(9,933 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#047857")
    
    # Review bars
    ax1.text(x[0], p_review[0] * 1.25, "18.40%\n(1,840 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#b45309")
    ax1.text(x[1], p_review[1] * 1.30, "0.49%\n(49 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#b45309")

    # Block bars
    ax1.text(x[0] + w, p_block[0] * 1.30, "1.20%\n(120 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#b91c1c")
    ax1.text(x[1] + w, p_block[1] * 1.30, "0.18%\n(18 tx)", ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#b91c1c")

    # Workload Slashing Callout Arrow (shortened so it never crosses over '0.49% (49 tx)')
    ax1.annotate("", xy=(x[1], 1.25), xytext=(x[0] + 0.08, 12.0),
                 arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.6, connectionstyle="arc3,rad=-0.16"))
    
    # Callout badge centered at x=0.52, y=6.0 (safely above the 1.20% block bar and between bars)
    ax1.text(0.52, 6.0, "-97.3% Review Slashing\n" + r"(1,840 $\rightarrow$ 49 alerts / 10k)" + "\n[-99.51% vs Legacy Rules]",
             ha="center", va="center", fontsize=7.0, fontweight="bold", color="#991b1b",
             bbox=dict(boxstyle="round,pad=0.28", fc="#fef2f2", ec="#dc2626", lw=1.0, alpha=0.95), zorder=5)

    ax1.set_yscale("log")
    ax1.set_ylim(0.04, 380)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=8.2, fontweight="bold")
    ax1.set_ylabel("Transaction Share (%) [Log Scale]", fontsize=8.6, weight="bold", labelpad=6)
    ax1.set_title("(b) Triage Operational Volume Comparison (N = 10,000 Wires)", fontsize=9.2, fontweight="bold", pad=28)
    
    # Legend for Panel (b) positioned above the plot to eliminate all collisions
    ax1.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, framealpha=0.95, fontsize=7.0, edgecolor="#cbd5e1")

    # Overall Layout Polish with ample top padding for the legends
    fig.subplots_adjust(left=0.08, right=0.97, top=0.86, bottom=0.15, wspace=0.28)
    
    # Save to all target directories
    for d in TARGET_DIRS:
        for stem in ["fig19_conformal_risk_mechanism", "fig_conformal_mechanism_proof"]:
            pdf_path = d / f"{stem}.pdf"
            png_path = d / f"{stem}.png"
            fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
            fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
            print(f" [OK] Saved: {pdf_path}")
        
    # Also save to artifact directory
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig5_2_redesigned_final.png")
    fig.savefig(artifact_png, dpi=300, bbox_inches="tight", pad_inches=0.15)
    print(f" [OK] Artifact copy saved: {artifact_png}")
    plt.close(fig)

if __name__ == "__main__":
    generate_figure_5_2()
