"""
Figure 3.3: 12-Dimensional Canonical Invariant Physical Toy-Model Schematic
Redesigned with:
- Physical hydrodynamic visual with equations extracted: Tank labeled "Inflow", pipe labeled "Outflow ≈ Inflow"
- Plain English labels across all 4 panels (no raw lambda_u, Phi_flow, or s_fwd/s_bwd clutter)
- Strict 4-color publication palette.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST_LIGHT,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_LIGHT,
    COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE_LIGHT,
    COLOR_RISK, COLOR_RISK_BG, COLOR_RISK_LIGHT,
    COLOR_REVIEW, COLOR_REVIEW_BG, COLOR_REVIEW_LIGHT,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    fig, axes = plt.subplots(2, 2, figsize=(10.0, 6.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # =========================================================================
    # Panel (a): Hydrodynamic Mass-Flow Balance
    # (Clean tank and pipe visual without equations)
    # =========================================================================
    ax_a = axes[0, 0]
    ax_a.set_facecolor('#ffffff')
    ax_a.set_title("(a) Hydrodynamic Mass-Flow Balance", 
                   fontsize=9.2, weight='bold', color=COLOR_DARK, pad=10)
    
    card_a = Rectangle((0.015, 0.02), 0.97, 0.96, fc="#ffffff", ec=COLOR_BORDER, lw=1.2, zorder=1)
    ax_a.add_patch(card_a)

    # Inflow Arrow & Tank
    ax_a.annotate("", xy=(0.28, 0.53), xytext=(0.05, 0.53),
                  arrowprops=dict(arrowstyle="simple,tail_width=3.5,head_width=9,head_length=8",
                                  facecolor=COLOR_INGEST, edgecolor="none"), zorder=4)
    ax_a.text(0.16, 0.65, "Inflow Tank\n(Capital Ingress)", ha="center", va="center",
              fontsize=7.6, weight="bold", color=COLOR_INGEST)

    # Main Pipe Conduit
    pipe_main = Rectangle((0.28, 0.38), 0.44, 0.30, fc=COLOR_INGEST_BG, ec=COLOR_INGEST, lw=1.6, zorder=2)
    ax_a.add_patch(pipe_main)

    # Intermediary Mule Node inside pipe
    ax_a.add_patch(patches.Circle((0.50, 0.53), 0.080, facecolor="#ffffff", edgecolor=COLOR_RISK, lw=1.6, zorder=3))
    ax_a.text(0.50, 0.54, "Conduit\nAccount", ha="center", va="center", fontsize=7.0, weight="bold", color=COLOR_RISK, zorder=4)

    # Outflow Arrow & Label
    ax_a.annotate("", xy=(0.95, 0.53), xytext=(0.72, 0.53),
                  arrowprops=dict(arrowstyle="simple,tail_width=3.5,head_width=9,head_length=8",
                                  facecolor=COLOR_INGEST, edgecolor="none"), zorder=4)
    ax_a.text(0.84, 0.65, "Outflow ≈ Inflow\n(Capital Egress)", ha="center", va="center",
              fontsize=7.6, weight="bold", color=COLOR_INGEST)

    # Status Callout Box
    status_box = Rectangle((0.06, 0.08), 0.88, 0.19, fc=COLOR_RISK_BG, ec=COLOR_RISK, lw=1.0, zorder=2)
    ax_a.add_patch(status_box)
    ax_a.text(0.50, 0.18, "Laundering Conduit: Rapid Flow Equivalence (Outflow ≈ Inflow)",
              ha="center", va="center", fontsize=7.2, weight="bold", color=COLOR_RISK)
    ax_a.text(0.50, 0.11, "Benign Merchant / Household: High Absorptive or Dispersive Capital Retention",
              ha="center", va="center", fontsize=6.6, color=COLOR_DARK)

    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1.05)
    ax_a.axis("off")

    # =========================================================================
    # Panel (b): Burst Arrival Dynamics
    # =========================================================================
    ax_b = axes[0, 1]
    ax_b.set_title("(b) Burst Arrival Dynamics (Smurfing vs Benign)",
                   fontsize=9.2, weight='bold', color=COLOR_DARK, pad=10)
    
    t_span = np.linspace(0, 48, 400)
    mu_base = 0.05
    smurf_times = [10.0, 10.4, 10.9, 11.3, 11.8, 12.2]
    alpha_s, beta_s = 1.2, 0.8
    intensity_smurf = np.full_like(t_span, mu_base)
    for st in smurf_times:
        mask = t_span >= st
        intensity_smurf[mask] += alpha_s * np.exp(-beta_s * (t_span[mask] - st))

    np.random.seed(42)
    poisson_times = np.sort(np.random.uniform(2, 46, 6))
    intensity_benign = np.full_like(t_span, mu_base)
    for pt in poisson_times:
        mask = t_span >= pt
        intensity_benign[mask] += 0.25 * np.exp(-1.5 * (t_span[mask] - pt))

    ax_b.plot(t_span, intensity_smurf, color=COLOR_RISK, lw=2.0, label="Coordinated Burst Cascade")
    ax_b.plot(t_span, intensity_benign, color=COLOR_MUTED, lw=1.2, linestyle="--", label="Benign Random Baseline")
    ax_b.vlines(smurf_times, 0, 0.35, color=COLOR_RISK, lw=1.2, alpha=0.7)
    
    ax_b.annotate("High-Frequency Arrival Spike\n(Smurfing Cluster)", xy=(11.5, 2.2), xytext=(17, 2.3),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.2),
                  fontsize=7.0, weight="bold", color=COLOR_RISK)

    ax_b.set_xlabel("Observation Window (Hours)", fontsize=8.0)
    ax_b.set_ylabel("Transaction Arrival Intensity", fontsize=8.0)
    ax_b.set_xlim(0, 48)
    ax_b.set_ylim(0, 2.8)
    ax_b.grid(True, linestyle=":", alpha=0.5)
    ax_b.legend(fontsize=6.8, loc="upper right")

    # =========================================================================
    # Panel (c): Causal Taint Reachability
    # =========================================================================
    ax_c = axes[1, 0]
    ax_c.set_facecolor('#ffffff')
    ax_c.set_title("(c) Bi-Directional Causal Taint Reachability",
                   fontsize=9.2, weight='bold', color=COLOR_DARK, pad=10)

    card_c = Rectangle((0.015, 0.02), 0.97, 0.96, fc="#ffffff", ec=COLOR_BORDER, lw=1.2, zorder=1)
    ax_c.add_patch(card_c)

    # 4 Nodes: Source -> Mule A, Mule B -> Cashout
    b_s0 = Rectangle((0.05, 0.38), 0.19, 0.32, fc=COLOR_RISK_BG, ec=COLOR_RISK, lw=1.2, zorder=2)
    b_m1 = Rectangle((0.39, 0.65), 0.22, 0.24, fc=COLOR_INGEST_BG, ec=COLOR_INGEST, lw=1.2, zorder=2)
    b_m2 = Rectangle((0.39, 0.20), 0.22, 0.24, fc=COLOR_INGEST_BG, ec=COLOR_INGEST, lw=1.2, zorder=2)
    b_c3 = Rectangle((0.76, 0.38), 0.19, 0.32, fc=COLOR_RISK_BG, ec=COLOR_RISK, lw=1.2, zorder=2)

    for b in [b_s0, b_m1, b_m2, b_c3]:
        ax_c.add_patch(b)

    ax_c.text(0.145, 0.58, "Sanctioned\nSource", ha="center", va="center", fontsize=7.2, weight="bold", color=COLOR_RISK)
    ax_c.text(0.145, 0.44, "100% Forward\nTaint Origin", ha="center", va="center", fontsize=6.2, color=COLOR_DARK)

    ax_c.text(0.50, 0.80, "Layering Conduit A", ha="center", va="center", fontsize=7.2, weight="bold", color=COLOR_INGEST)
    ax_c.text(0.50, 0.70, "Bi-Directional Conduit", ha="center", va="center", fontsize=6.2, color=COLOR_DARK)

    ax_c.text(0.50, 0.35, "Layering Conduit B", ha="center", va="center", fontsize=7.2, weight="bold", color=COLOR_INGEST)
    ax_c.text(0.50, 0.25, "Bi-Directional Conduit", ha="center", va="center", fontsize=6.2, color=COLOR_DARK)

    ax_c.text(0.855, 0.58, "High-Risk\nCashout Sink", ha="center", va="center", fontsize=7.2, weight="bold", color=COLOR_RISK)
    ax_c.text(0.855, 0.44, "100% Backward\nTaint Termination", ha="center", va="center", fontsize=6.2, color=COLOR_DARK)

    # Directional Arrows
    ax_c.annotate("", xy=(0.38, 0.75), xytext=(0.25, 0.55),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.6))
    ax_c.annotate("", xy=(0.38, 0.35), xytext=(0.25, 0.48),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.6))
    ax_c.annotate("", xy=(0.75, 0.55), xytext=(0.62, 0.75),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.6))
    ax_c.annotate("", xy=(0.75, 0.48), xytext=(0.62, 0.35),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.6))

    ax_c.text(0.50, 0.08, "Causal Invariant: Dual forward-backward reachability flags active money laundering pathways.",
              ha="center", va="center", fontsize=6.8, weight="bold", color=COLOR_DARK)

    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1.05)
    ax_c.axis("off")

    # =========================================================================
    # Panel (d): Comparative Invariant Signature
    # (Clean English labels on x-axis instead of raw math symbols)
    # =========================================================================
    ax_d = axes[1, 1]
    ax_d.set_title("(d) Normalized Invariant Signature Comparison",
                   fontsize=9.2, weight='bold', color=COLOR_DARK, pad=10)

    metric_labels = [
        "Flow\nBalance", "Burst\nIntensity", "Forward\nTaint",
        "Backward\nTaint", "Time\nVariance", "Capital\nVelocity", "Degree\nAsymmetry"
    ]
    illicit_prof = [0.95, 0.90, 0.85, 0.80, 0.88, 0.92, 0.78]
    benign_prof  = [0.15, 0.20, 0.10, 0.08, 0.25, 0.18, 0.12]

    x_m = np.arange(len(metric_labels))
    w = 0.35
    ax_d.bar(x_m - w/2, illicit_prof, width=w, color=COLOR_RISK, edgecolor="#991b1b", lw=1.0, label="Illicit Syndicate Pattern")
    ax_d.bar(x_m + w/2, benign_prof,  width=w, color=COLOR_INGEST, edgecolor="#1d4ed8", lw=1.0, label="Benign Commercial Pattern")
    ax_d.set_xticks(x_m)
    ax_d.set_xticklabels(metric_labels, fontsize=6.8)
    ax_d.set_ylabel("Normalized Invariant Score", fontsize=8.0)
    ax_d.set_ylim(0, 1.15)
    ax_d.grid(True, linestyle=":", alpha=0.5)
    ax_d.legend(fontsize=6.8, loc="upper right")

    plt.tight_layout()
    save_figure(fig, "fig_12d_toy_model_schematic", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
