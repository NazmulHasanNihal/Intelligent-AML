"""
Figure 3.3: 12-Dimensional Canonical Invariant Physical Toy-Model Schematic
Standalone publication script for C-STGB monograph.
Redesigned with generous margins, zero overlapping text, horizontal signature bars, and clear physical intuition.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.2), dpi=300)
    plt.subplots_adjust(wspace=0.28, hspace=0.35, left=0.08, right=0.96, top=0.93, bottom=0.08)

    # =========================================================================
    # Panel (a): Hydrodynamic Mass-Flow Balance
    # =========================================================================
    ax_a = axes[0, 0]
    ax_a.axis("off")
    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1)
    ax_a.set_title("(a) Hydrodynamic Mass-Flow Balance", fontsize=9.2, fontweight="bold", color=COLOR_DARK, pad=8)
    
    # Outer frame
    ax_a.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))

    # Inflow Tank
    ax_a.add_patch(patches.Rectangle((0.05, 0.45), 0.22, 0.32, facecolor="#eff6ff", edgecolor=COLOR_INGEST, lw=1.3))
    ax_a.text(0.16, 0.65, "Inflow Tank", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_INGEST)
    ax_a.text(0.16, 0.53, "Capital Ingress\n($50,000)", ha="center", va="center", fontsize=6.6, color="#1e40af")

    # Inflow Arrow
    ax_a.annotate("", xy=(0.38, 0.61), xytext=(0.27, 0.61),
                  arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_INGEST, mutation_scale=12))

    # Central Conduit Pipe
    ax_a.add_patch(patches.Rectangle((0.38, 0.48), 0.24, 0.26, facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.2))
    ax_a.add_patch(patches.Circle((0.50, 0.61), 0.075, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.4))
    ax_a.text(0.50, 0.61, "Conduit\nMule", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_RISK)

    # Outflow Arrow
    ax_a.annotate("", xy=(0.73, 0.61), xytext=(0.62, 0.61),
                  arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=12))

    # Outflow Destination
    ax_a.add_patch(patches.Rectangle((0.73, 0.45), 0.22, 0.32, facecolor="#fef2f2", edgecolor=COLOR_RISK, lw=1.3))
    ax_a.text(0.84, 0.65, "Outflow Sink", ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_RISK)
    ax_a.text(0.84, 0.53, "Capital Egress\n(≈ $49,800)", ha="center", va="center", fontsize=6.6, color="#991b1b")

    # Bottom Callout Box (Clean padding)
    ax_a.add_patch(patches.Rectangle((0.04, 0.06), 0.92, 0.30, facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=0.9))
    ax_a.text(0.50, 0.28, "Physical Mass-Flow Disambiguation", ha="center", va="center", fontsize=7.4, fontweight="bold", color=COLOR_DARK)
    ax_a.text(0.50, 0.19, "• Laundering Conduit: Strict Pass-Through (Outflow ≈ Inflow, Retention < 0.5%).",
              ha="center", va="center", fontsize=6.6, color=COLOR_RISK)
    ax_a.text(0.50, 0.11, "• Benign Commercial: High Capital Retention (Salaries, Inventory, Retention > 90%).",
              ha="center", va="center", fontsize=6.6, color=COLOR_SAFE)

    # =========================================================================
    # Panel (b): Burst Arrival Dynamics
    # =========================================================================
    ax_b = axes[0, 1]
    ax_b.set_title("(b) Burst Arrival Dynamics (Smurfing vs Benign)", fontsize=9.2, fontweight="bold", color=COLOR_DARK, pad=8)
    
    t_span = np.linspace(0, 24, 300)
    mu_base = 0.08
    smurf_times = [6.0, 6.3, 6.7, 7.1, 7.5, 7.9]
    intensity_smurf = np.full_like(t_span, mu_base)
    for st in smurf_times:
        mask = t_span >= st
        intensity_smurf[mask] += 1.4 * np.exp(-1.1 * (t_span[mask] - st))

    np.random.seed(42)
    poisson_times = np.sort(np.random.uniform(1, 23, 7))
    intensity_benign = np.full_like(t_span, mu_base)
    for pt in poisson_times:
        mask = t_span >= pt
        intensity_benign[mask] += 0.28 * np.exp(-1.5 * (t_span[mask] - pt))

    ax_b.plot(t_span, intensity_smurf, color=COLOR_RISK, lw=2.0, label="Coordinated Burst Cascade")
    ax_b.plot(t_span, intensity_benign, color="#64748b", lw=1.4, linestyle="--", label="Benign Random Baseline")
    ax_b.vlines(smurf_times, 0, 0.45, color=COLOR_RISK, lw=1.2, alpha=0.7)
    
    ax_b.annotate("High-Frequency Arrival Spike\n(Smurfing Cluster)", xy=(7.0, 2.3), xytext=(11.5, 2.3),
                  arrowprops=dict(arrowstyle="->", color=COLOR_RISK, lw=1.3),
                  fontsize=7.2, fontweight="bold", color=COLOR_RISK)

    ax_b.set_xlabel("Observation Window (Hours)", fontsize=8.2, fontweight="bold")
    ax_b.set_ylabel("Transaction Arrival Intensity", fontsize=8.2, fontweight="bold")
    ax_b.set_xlim(0, 24)
    ax_b.set_ylim(0, 2.9)
    ax_b.grid(True, linestyle=":", alpha=0.5)
    ax_b.legend(fontsize=7.2, loc="upper right", framealpha=0.92)

    # =========================================================================
    # Panel (c): Causal Taint Reachability
    # =========================================================================
    ax_c = axes[1, 0]
    ax_c.axis("off")
    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1)
    ax_c.set_title("(c) Bi-Directional Causal Taint Reachability", fontsize=9.2, fontweight="bold", color=COLOR_DARK, pad=8)
    ax_c.add_patch(patches.Rectangle((0.01, 0.01), 0.98, 0.98, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))

    # 4 Nodes: Source -> Conduit A & B -> Sink
    ax_c.add_patch(patches.Rectangle((0.05, 0.40), 0.18, 0.28, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.3))
    ax_c.text(0.14, 0.58, "Sanctioned\nSource", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_RISK)
    ax_c.text(0.14, 0.47, "100% Forward\nTaint Origin", ha="center", va="center", fontsize=6.0, color="#991b1b")

    ax_c.add_patch(patches.Rectangle((0.40, 0.65), 0.20, 0.24, facecolor="#eff6ff", edgecolor=COLOR_INGEST, lw=1.2))
    ax_c.text(0.50, 0.80, "Conduit Mule A", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_INGEST)
    ax_c.text(0.50, 0.71, "Forward Taint Flow", ha="center", va="center", fontsize=6.0, color="#1e40af")

    ax_c.add_patch(patches.Rectangle((0.40, 0.18), 0.20, 0.24, facecolor="#eff6ff", edgecolor=COLOR_INGEST, lw=1.2))
    ax_c.text(0.50, 0.33, "Conduit Mule B", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_INGEST)
    ax_c.text(0.50, 0.24, "Forward Taint Flow", ha="center", va="center", fontsize=6.0, color="#1e40af")

    ax_c.add_patch(patches.Rectangle((0.77, 0.40), 0.18, 0.28, facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=1.3))
    ax_c.text(0.86, 0.58, "High-Risk\nCashout Sink", ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_RISK)
    ax_c.text(0.86, 0.47, "100% Backward\nTaint Origin", ha="center", va="center", fontsize=6.0, color="#991b1b")

    # Arrows
    ax_c.annotate("", xy=(0.39, 0.75), xytext=(0.24, 0.58), arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_RISK))
    ax_c.annotate("", xy=(0.39, 0.30), xytext=(0.24, 0.50), arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_RISK))
    ax_c.annotate("", xy=(0.76, 0.58), xytext=(0.61, 0.75), arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_RISK))
    ax_c.annotate("", xy=(0.76, 0.50), xytext=(0.61, 0.30), arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_RISK))

    ax_c.text(0.50, 0.08, "Dual forward-backward reachability flags active money laundering pathways.",
              ha="center", va="center", fontsize=6.6, fontweight="bold", color=COLOR_DARK)

    # =========================================================================
    # Panel (d): Normalized Invariant Signature Comparison (Horizontal Bars!)
    # =========================================================================
    ax_d = axes[1, 1]
    ax_d.set_title("(d) Normalized Invariant Signature Comparison", fontsize=9.2, fontweight="bold", color=COLOR_DARK, pad=8)

    metrics = [
        "Flow Conservation",
        "Arrival Velocity",
        "Forward Taint",
        "Backward Taint",
        "Time Variance",
        "Degree Asymmetry"
    ]
    illicit_vals = [0.95, 0.90, 0.85, 0.80, 0.88, 0.78]
    benign_vals  = [0.15, 0.20, 0.10, 0.08, 0.25, 0.12]

    y_pos = np.arange(len(metrics))[::-1]
    bh = 0.36

    ax_d.barh(y_pos + bh/2, illicit_vals, height=bh, color=COLOR_RISK, edgecolor=COLOR_DARK, lw=0.7, label="Illicit Syndicate Pattern")
    ax_d.barh(y_pos - bh/2, benign_vals,  height=bh, color=COLOR_INGEST, edgecolor=COLOR_DARK, lw=0.7, label="Benign Commercial Pattern")

    ax_d.set_yticks(y_pos)
    ax_d.set_yticklabels(metrics, fontsize=7.6, fontweight="bold")
    ax_d.set_xlabel("Normalized Invariant Value", fontsize=8.2, fontweight="bold")
    ax_d.set_xlim(0, 1.15)
    ax_d.grid(True, axis="x", linestyle=":", alpha=0.5)
    ax_d.legend(fontsize=7.2, loc="lower right", framealpha=0.92)

    save_figure(fig, "fig_12d_toy_model_schematic", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
