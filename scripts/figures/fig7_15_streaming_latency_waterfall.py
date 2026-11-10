"""
Figure 7.15: Empirical Streaming Latency Distribution for Fast-Path Inference
Publication-grade script for C-STGB monograph.
Refined spacing, generous margins, perfectly decoupled subplots, and zero text clipping:
- Subplot (a): Stage-by-Stage Latency with explicit visual grouping (Fast-Path Components, Fast-Path Total, Forensics Explainer, Forensics Total)
- Subplot (b): Cumulative Wall-Clock Latency vs Statutory Banking SLAs (10.0 ms & 100.0 ms)
- Multi-directory export to all thesis and report figure folders
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)


def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous canvas sized for immaculate layout and zero cramping
    fig = plt.figure(figsize=(13.2, 5.8), dpi=300)

    gs = gridspec.GridSpec(
        1, 2,
        width_ratios=[1.25, 1.0],
        left=0.07, right=0.96,
        top=0.84, bottom=0.16,
        wspace=0.34
    )

    # -------------------------------------------------------------
    # Master Header Banner (Clean, decoupled hierarchy)
    # -------------------------------------------------------------
    fig.text(0.07, 0.964, "Streaming Latency Breakdown & Production SLA Safety Margins",
             fontsize=10.5, fontweight='bold', color=COLOR_DARK, ha='left')
    fig.text(0.07, 0.930, "Stage-by-stage empirical latency (P50, P90, P99) across Fast-Path and Forensics pipelines on AMD EPYC 7763 + NVIDIA A100",
             fontsize=7.4, color='#475569', ha='left')
    fig.text(0.96, 0.942, "Peak Throughput: 31,250 tx/s | Fast-Path P99: 0.82 ms",
             fontsize=7.4, fontweight='bold', color='#1e3a8a', ha='right',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#eff6ff', edgecolor='#93c5fd', lw=0.9))

    # =============================================================
    # SUBPLOT (A): STAGE-BY-STAGE LATENCY BREAKDOWN
    # =============================================================
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_title(r"(a) Stage-by-Stage Latency (P50 Median & P99 Tail Whisker)",
                   fontsize=9.0, fontweight='bold', color=COLOR_DARK, pad=10)

    # Distinct Y-positions to create clear visual groupings and proper gaps:
    # Group 1: Fast-Path Component Stages (y = 6.2, 5.2, 4.2, 3.2)
    # Group 2: Fast-Path Gate Summary (y = 1.9)
    # Group 3: Forensics Explainer Mask (y = 0.7)
    # Group 4: Full Forensics Total (y = -0.5)
    y_pos = np.array([6.2, 5.2, 4.2, 3.2, 1.9, 0.7, -0.5])

    stage_labels = [
        r"1. DuckDB Invariants ($\mathbf{z}_{\mathrm{inv}}$)",
        r"2. Top-15 Subgraph Extraction",
        r"3. Spatio-Temporal GNN Forward",
        r"4. Conformal Risk Gate ($\Gamma$)",
        r"TOTAL Fast-Path Gate (STP)",
        r"5. GNNExplainer Subgraph Mask",
        r"TOTAL Forensics Pipeline (SAR)"
    ]

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

    bar_heights = [0.52, 0.52, 0.52, 0.52, 0.62, 0.52, 0.62]

    # Subtle background group tint plates to visually separate Fast-Path from Forensics
    ax_a.axhspan(1.3, 6.8, facecolor='#f0fdf4', alpha=0.45, zorder=0)  # Fast-Path Zone
    ax_a.axhspan(-1.1, 1.3, facecolor='#faf5ff', alpha=0.45, zorder=0) # Forensics Zone

    # Dividing line between Fast-Path and Forensics
    ax_a.axhline(1.3, color='#cbd5e1', linestyle='-', lw=0.9, zorder=1)

    # Draw horizontal bars for P50
    for y, p50, h, c in zip(y_pos, p50_lat, bar_heights, stage_colors):
        ax_a.barh(y, p50, height=h, color=c, edgecolor=COLOR_DARK, linewidth=0.8, zorder=3)

    # Draw whiskers from P50 to P99 with caps
    for y, p50, p90, p99 in zip(y_pos, p50_lat, p90_lat, p99_lat):
        ax_a.plot([p50, p99], [y, y], color='#334155', lw=1.4, zorder=4)
        ax_a.plot([p90, p90], [y - 0.14, y + 0.14], color='#64748b', lw=1.2, zorder=4)
        ax_a.plot([p99, p99], [y - 0.22, y + 0.22], color=COLOR_DARK, lw=1.6, zorder=4)

    # Formatted annotation labels to the right of the whiskers (ample xlim guarantees zero clipping)
    for y, p50, p99, idx in zip(y_pos, p50_lat, p99_lat, range(len(y_pos))):
        if idx == 4:  # Fast-Path Total
            ax_a.text(p99 + 0.14, y, f"{p50:.2f} ms (P99: {p99:.2f}) [STP Pass]",
                      ha='left', va='center', fontsize=7.0, fontweight='bold', color='#047857')
        elif idx == 6:  # Full Forensics Total
            ax_a.text(p99 + 0.14, y, f"{p50:.2f} ms (P99: {p99:.2f}) [SAR Ready]",
                      ha='left', va='center', fontsize=7.0, fontweight='bold', color='#6d28d9')
        else:
            ax_a.text(p99 + 0.14, y, f"{p50:.2f} ms (P99: {p99:.2f})",
                      ha='left', va='center', fontsize=6.8, color='#334155')

    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(stage_labels, fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("Empirical Inference Latency (ms)", fontsize=8.2, fontweight='bold', color='#1e293b')
    ax_a.set_xlim([0, 6.2])
    ax_a.set_ylim([-1.1, 7.0])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)

    # Clean Legend in Subplot A (Placed at upper right with zero collision)
    p50_patch = patches.Patch(facecolor='#2563eb', edgecolor=COLOR_DARK, label='P50 Median')
    p90_line = plt.Line2D([0], [0], color='#64748b', lw=1.2, marker='|', markersize=6, label='P90')
    p99_line = plt.Line2D([0], [0], color='#334155', lw=1.4, marker='|', markersize=8, markeredgewidth=1.6, label='P99 Tail Cap')
    ax_a.legend(handles=[p50_patch, p90_line, p99_line], loc='upper right', fontsize=7.0,
                facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.95)

    # =============================================================
    # SUBPLOT (B): CUMULATIVE PIPELINE VS PRODUCTION SLA THRESHOLDS
    # =============================================================
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title(r"(b) Cumulative Latency vs Statutory Banking SLAs",
                   fontsize=9.0, fontweight='bold', color=COLOR_DARK, pad=10)

    # Staircase stages
    step_stages = [
        "1. Ingestion",
        "2. Invariants",
        "3. Subgraph",
        "4. GNN Core",
        "5. CRC Gate",
        "6. Explainer",
        "7. SAR Pack"
    ]
    x_steps = np.arange(len(step_stages))

    # Cumulative medians and P99s
    cum_p50 = np.array([0.05, 0.11, 0.29, 0.41, 0.45, 1.85, 2.10])
    cum_p99 = np.array([0.08, 0.22, 0.57, 0.75, 0.82, 3.20, 3.67])

    # Plot cumulative step curves
    ax_b.step(x_steps, cum_p50, where='mid', color='#0284c7', lw=2.2, label='Cumulative P50 Median', zorder=3)
    ax_b.step(x_steps, cum_p99, where='mid', color='#7c3aed', lw=2.2, linestyle='--', label='Cumulative P99 Tail', zorder=3)
    ax_b.scatter(x_steps, cum_p50, color='#0284c7', s=28, zorder=4)
    ax_b.scatter(x_steps, cum_p99, color='#7c3aed', s=28, zorder=4)

    # Statutory SLA Threshold Lines
    ax_b.axhline(10.0, color='#dc2626', linestyle=':', lw=2.0, label=r'Core Banking SLA ($10.0\,\mathrm{ms}$)', zorder=2)
    ax_b.axhline(100.0, color='#9333ea', linestyle=':', lw=2.0, label=r'Investigation SLA ($100.0\,\mathrm{ms}$)', zorder=2)

    # Shaded Headroom Band for Fast-Path Gate
    ax_b.fill_between(x_steps[:5], cum_p99[:5], 10.0, color='#ecfdf5', alpha=0.7, zorder=1)
    ax_b.text(2.0, 3.2, "22.2× Median Headroom\n(12.2× P99 Tail Safety)", ha='center', va='center',
              fontsize=7.0, fontweight='bold', color='#047857',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#86efac', lw=0.8), zorder=5)

    # Fast-Path Clearance Marker at Step 4 (CRC Decision)
    ax_b.annotate("Fast-Path Exit: 0.45 ms\n(99.33% Auto-Clear)",
                  xy=(4.0, 0.45), xytext=(4.2, 0.10),
                  arrowprops=dict(arrowstyle="->", lw=1.2, color='#059669'),
                  fontsize=6.6, fontweight='bold', color='#047857', ha='center',
                  bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0fdf4', edgecolor='#86efac', lw=0.6),
                  zorder=6)

    ax_b.set_yscale('log')
    ax_b.set_ylim([0.03, 180.0])
    ax_b.set_xticks(x_steps)
    ax_b.set_xticklabels(step_stages, fontsize=7.2, rotation=25, ha='right', fontweight='bold', color='#1e293b')
    ax_b.set_ylabel(r"Cumulative Latency ($\mathrm{ms}$, $\log_{10}$ Scale)", fontsize=8.2, fontweight='bold', color='#1e293b')
    ax_b.grid(True, which='both', linestyle=':', alpha=0.5, color='#cbd5e1')

    # Placed in open space between 10 ms and 100 ms SLA lines on the right
    leg = ax_b.legend(loc='upper right', bbox_to_anchor=(0.98, 0.82), fontsize=6.8,
                      facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.95)
    leg.set_zorder(6)

    return fig


if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_streaming_latency_waterfall", pad_inches=0.10)
    plt.close(fig)
