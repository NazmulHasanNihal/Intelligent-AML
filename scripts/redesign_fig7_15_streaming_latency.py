"""
scripts/redesign_fig7_15_streaming_latency.py
Publication-grade redesign of Figure 7.15:
Stage-by-Stage Streaming Latency Breakdown and Cumulative Production SLA Headroom.
Strictly NO cards: pure technical engineering plots with formal annotations, error whiskers, and SLA step functions.
Generates fig_streaming_latency_waterfall.pdf and .png across all 5 directories.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.0,
    'axes.labelsize': 8.2,
    'axes.titlesize': 9.0,
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


def build_figure():
    fig = plt.figure(figsize=(9.8, 4.4), dpi=300)
    
    gs = gridspec.GridSpec(
        1, 2,
        width_ratios=[1.25, 1.0],
        left=0.06, right=0.98,
        top=0.88, bottom=0.12,
        wspace=0.25
    )

    # -------------------------------------------------------------
    # Master Header Banner
    # -------------------------------------------------------------
    fig.text(0.06, 0.965, "Streaming Latency Breakdown & Production SLA Safety Margins",
             fontsize=10.2, fontweight='bold', color='#0f172a', ha='left')
    fig.text(0.06, 0.925, "Stage-by-stage empirical latency (P50, P90, P99) across Fast-Path and Forensics pipelines (AMD EPYC 7763 + NVIDIA A100)",
             fontsize=7.6, color='#475569', ha='left')
    fig.text(0.98, 0.940, "Peak Throughput: 31,200 tx/s | Fast-Path P99: 0.82 ms",
             fontsize=7.6, fontweight='bold', color='#1e3a8a', ha='right',
             bbox=dict(boxstyle='square,pad=0.25', facecolor='#eff6ff', edgecolor='#93c5fd', lw=0.8))

    # -------------------------------------------------------------
    # SUBPLOT (A): STAGE-BY-STAGE LATENCY BREAKDOWN
    # -------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_title(r"(a) Stage-by-Stage Latency (P50 Median & P99 Tail Whisker)",
                   fontsize=8.8, fontweight='bold', color='#0f172a', pad=8)

    stage_labels = [
        r"1. DuckDB Invariants ($\mathbf{z}_{\mathrm{inv}}$)",
        r"2. Subgraph Top-15 Fetch",
        r"3. Spatio-Temporal Forward",
        r"4. Conformal Risk Gate ($\Gamma$)",
        r"TOTAL Fast-Path Gate",
        r"5. GNNExplainer Mask",
        r"TOTAL Forensics Pipeline"
    ]
    
    y_pos = np.arange(len(stage_labels))[::-1]
    
    p50_lat = np.array([0.11, 0.18, 0.12, 0.04, 0.45, 1.65, 2.10])
    p90_lat = np.array([0.16, 0.26, 0.17, 0.05, 0.64, 2.20, 2.84])
    p99_lat = np.array([0.22, 0.35, 0.21, 0.07, 0.82, 2.85, 3.67])

    stage_colors = [
        "#1d4ed8",  # Stage 1: Blue
        "#2563eb",  # Stage 2: Blue
        "#0284c7",  # Stage 3: Sky
        "#0d9488",  # Stage 4: Teal
        "#059669",  # Fast-Path Total: Emerald
        "#d97706",  # Stage 5: Amber
        "#7c3aed"   # Forensics Total: Purple
    ]

    # Draw horizontal bars for P50
    ax_a.barh(y_pos, p50_lat, height=0.52, color=stage_colors, edgecolor='#0f172a', linewidth=0.8, zorder=3)

    # Draw whiskers from P50 to P99 with caps
    for y, p50, p99 in zip(y_pos, p50_lat, p99_lat):
        ax_a.plot([p50, p99], [y, y], color='#334155', lw=1.4, zorder=4)
        ax_a.plot([p99, p99], [y - 0.20, y + 0.20], color='#0f172a', lw=1.6, zorder=4)

    # Shift all text annotations cleanly to the RIGHT of the P99 whisker caps
    for y, p50, p99 in zip(y_pos, p50_lat, p99_lat):
        if y == 2:  # Fast-Path Total
            ax_a.text(p99 + 0.12, y, f"{p50:.2f} ms (P99: {p99:.2f}) [STP Pass]",
                      ha='left', va='center', fontsize=6.8, fontweight='bold', color='#047857')
        elif y == 0:  # Full Forensics Total
            ax_a.text(p99 + 0.12, y, f"{p50:.2f} ms (P99: {p99:.2f}) [SAR Ready]",
                      ha='left', va='center', fontsize=6.8, fontweight='bold', color='#6d28d9')
        else:
            ax_a.text(p99 + 0.12, y, f"{p50:.2f} ms (P99: {p99:.2f})",
                      ha='left', va='center', fontsize=6.6, color='#334155')

    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(stage_labels, fontsize=7.5, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("Empirical Inference Latency (ms)", fontsize=8.0, fontweight='bold', color='#1e293b')
    ax_a.set_xlim([0, 5.2])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)

    # Legend for P50 and P99
    p50_patch = patches.Patch(facecolor='#2563eb', edgecolor='#0f172a', label='P50 Median')
    p99_line = plt.Line2D([0], [0], color='#334155', lw=1.4, marker='|', markersize=8, markeredgewidth=1.6, label='P99 Tail Cap')
    ax_a.legend(handles=[p50_patch, p99_line], loc='upper right', fontsize=6.8, facecolor='#ffffff', edgecolor='#cbd5e1')

    # =============================================================
    # SUBPLOT (B): CUMULATIVE PIPELINE VS PRODUCTION SLA THRESHOLDS
    # =============================================================
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title(r"(b) Cumulative Latency vs Statutory Banking SLAs",
                   fontsize=8.8, fontweight='bold', color='#0f172a', pad=8)

    # Staircase stages
    step_stages = ["Triage Ingestion", "Invariant Calc", "Top-15 Graph", "GNN Inference", "CRC Decision", "GNNExplainer", "SAR Packaging"]
    x_steps = np.arange(len(step_stages))
    
    # Cumulative medians and P99s
    cum_p50 = np.array([0.05, 0.11, 0.29, 0.41, 0.45, 1.85, 2.10])
    cum_p99 = np.array([0.08, 0.22, 0.57, 0.75, 0.82, 3.20, 3.67])

    # Plot cumulative step curves
    ax_b.step(x_steps, cum_p50, where='mid', color='#0284c7', lw=2.0, label='Cumulative P50 Median', zorder=3)
    ax_b.step(x_steps, cum_p99, where='mid', color='#7c3aed', lw=2.0, linestyle='--', label='Cumulative P99 Tail', zorder=3)
    ax_b.scatter(x_steps, cum_p50, color='#0284c7', s=25, zorder=4)
    ax_b.scatter(x_steps, cum_p99, color='#7c3aed', s=25, zorder=4)

    # Statutory SLA Threshold Lines
    ax_b.axhline(10.0, color='#dc2626', linestyle=':', lw=1.8, label=r'Core Banking SLA ($10.0\,\mathrm{ms}$)')
    ax_b.axhline(100.0, color='#9333ea', linestyle=':', lw=1.8, label=r'Investigation SLA ($100.0\,\mathrm{ms}$)')

    # Shaded Headroom Bands
    ax_b.fill_between(x_steps[:5], cum_p99[:5], 10.0, color='#ecfdf5', alpha=0.6, zorder=1)
    ax_b.text(2.0, 3.5, "22.2× Headroom\n(Straight-Through Auto-Clear)", ha='center', va='center',
              fontsize=7.0, fontweight='bold', color='#047857',
              bbox=dict(boxstyle='square,pad=0.2', facecolor='#ffffff', edgecolor='#86efac', lw=0.6))

    ax_b.set_yscale('log')
    ax_b.set_ylim([0.03, 160.0])
    ax_b.set_xticks(x_steps)
    ax_b.set_xticklabels(step_stages, fontsize=6.8, rotation=35, ha='right', fontweight='bold', color='#1e293b')
    ax_b.set_ylabel(r"Cumulative Wall-Clock Latency ($\mathrm{ms}$, $\log_{10}$ Scale)", fontsize=8.0, fontweight='bold', color='#1e293b')
    ax_b.grid(True, which='both', linestyle=':', alpha=0.5, color='#cbd5e1')
    ax_b.legend(loc='lower right', fontsize=6.6, facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.95)

    return fig

def main():
    print("Generating redesigned Figure 7.15 (Stage-by-Stage Streaming Latency Waterfall)...")
    fig = build_figure()

    for d in TARGET_DIRS:
        for stem in ["fig_streaming_latency_waterfall", "fig7_15_streaming_latency"]:
            pdf_path = d / f"{stem}.pdf"
            png_path = d / f"{stem}.png"
            fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.10)
            fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
            print(f" [OK] Saved: {pdf_path}")

    artifact_path = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_15_redesigned_final.png")
    fig.savefig(artifact_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
    print(f" [OK] Saved artifact: {artifact_path}")
    plt.close(fig)
    print("Figure 7.15 redesign completed successfully!")

if __name__ == "__main__":
    main()
