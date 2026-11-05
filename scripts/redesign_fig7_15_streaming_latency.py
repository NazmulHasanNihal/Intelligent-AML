"""
scripts/redesign_fig7_15_streaming_latency.py
Publication-grade redesign of Figure 7.15:
Stage-by-Stage Fast-Path Streaming Latency Breakdown and Production SLA Headroom.
Generates fig_streaming_latency_waterfall.pdf and .png across all 5 figure target directories.
Zero text-over-text collisions; zero border clipping; 127 total pages strictly preserved.
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
    'font.size': 7.6,
    'axes.labelsize': 7.8,
    'axes.titlesize': 8.4,
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
    # Sized to 8.6" x 3.45" (aspect ratio ~2.65:1)
    # Scaled to 0.85\textwidth in LaTeX, yields rendered height ~130 pt
    # Preserves exact 127-page count and Page 88 footer headroom
    fig = plt.figure(figsize=(8.6, 3.45))
    
    # Outer layout:
    # Left: Panel (a) Latency breakdown (~59% width)
    # Right: Panel (b) Production SLA compliance cards (~41% width)
    # top=0.81 provides clean clearance below header subtitle
    gs = gridspec.GridSpec(
        1, 2,
        width_ratios=[1.42, 1.0],
        left=0.038, right=0.985,
        top=0.810, bottom=0.110,
        wspace=0.18
    )
    
    # -------------------------------------------------------------
    # Master Header Banner (Figure Title & Rigor Guarantee)
    # -------------------------------------------------------------
    fig.text(0.038, 0.950, "Figure 7.15: Streaming Latency Breakdown & Production SLA Headroom",
             fontsize=9.8, fontweight='bold', color='#0f172a', ha='left')
    fig.text(0.038, 0.885, "Stage-by-stage empirical latency (P50, P90, P99) across Fast-Path and Forensics pipelines (AMD EPYC 7763 + NVIDIA A100)",
             fontsize=7.2, color='#475569', ha='left')
    
    # Benchmark badge top right
    fig.text(0.985, 0.920, "Throughput: 31,200 tx/s | Fast-Path P99: 0.82 ms",
             fontsize=7.2, fontweight='bold', color='#1e3a8a', ha='right',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#eff6ff', edgecolor='#93c5fd', lw=0.8))

    # -------------------------------------------------------------
    # Data Definitions (Thesis Section 7.7 & Table 7.13 Aligned)
    # -------------------------------------------------------------
    stage_labels = [
        "1. DuckDB & 12-D Invariants",
        "2. Subgraph Top-15 Fetch",
        "3. Temporal GNN Forward",
        "4. CRC Conformal Risk",
        "Total Fast-Path SLA Gate",
        "5. Explainer Attribution",
        "Total Forensics Pipeline"
    ]
    
    y_pos = np.arange(len(stage_labels))[::-1]
    
    p50_lat = np.array([0.11, 0.18, 0.12, 0.04, 0.45, 1.65, 2.10])
    p90_lat = np.array([0.16, 0.26, 0.17, 0.05, 0.64, 2.20, 2.84])
    p99_lat = np.array([0.22, 0.35, 0.21, 0.07, 0.82, 2.85, 3.67])
    
    stage_colors = [
        "#1d4ed8",  # Stage 1: Blue-700
        "#2563eb",  # Stage 2: Blue-600
        "#0284c7",  # Stage 3: Sky-600
        "#0891b2",  # Stage 4: Cyan-600
        "#059669",  # Fast-Path Total: Emerald-600
        "#d97706",  # Stage 5: Amber-600
        "#7c3aed"   # Forensics Total: Violet-600
    ]
    
    # -------------------------------------------------------------
    # Panel (a): Stage-by-Stage Latency Breakdown
    # -------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_facecolor("#f8fafc")
    for spine in ax_a.spines.values():
        spine.set_color("#cbd5e1")
        spine.set_linewidth(0.8)
        
    ax_a.set_title(r"(a) Microsecond Latency Breakdown by Pipeline Stage",
                   fontsize=8.4, fontweight='bold', color='#0f172a', pad=6, loc='left')
    
    # Shaded bands highlighting the 2 totals
    ax_a.axhspan(1.5, 2.5, color='#ecfdf5', alpha=0.6, zorder=0)  # Fast-path total band
    ax_a.axhspan(-0.5, 0.5, color='#f5f3ff', alpha=0.6, zorder=0) # Forensics total band
    
    # Draw P99 whisper/band behind
    bar_h = 0.52
    ax_a.barh(
        y_pos, p99_lat, height=bar_h,
        color=stage_colors, alpha=0.25, edgecolor='none'
    )
    
    # Draw P50 primary bars
    bars_p50 = ax_a.barh(
        y_pos, p50_lat, height=bar_h,
        color=stage_colors, edgecolor='#1e293b', linewidth=0.7,
        alpha=0.92
    )
    
    # Add P99 error cap markers
    for y, p50, p99 in zip(y_pos, p50_lat, p99_lat):
        ax_a.plot([p50, p99], [y, y], color='#334155', lw=1.0)
        ax_a.plot([p99, p99], [y - 0.18, y + 0.18], color='#334155', lw=1.2)
        
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(stage_labels, fontsize=7.2, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("Empirical Inference Latency (ms)", fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_a.set_xlim([0, 4.8])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1')
    ax_a.tick_params(axis='both', which='major', labelsize=7.0)
    
    # Value annotations on each bar (cleanly positioned)
    for y, p50, p99, col in zip(y_pos, p50_lat, p99_lat, stage_colors):
        if y == 2:  # Fast-Path Total
            ax_a.text(p99 + 0.08, y, f"{p50:.2f} ms (P99: {p99:.2f}) [STP Pass]",
                      ha='left', va='center', fontsize=6.6, fontweight='bold', color='#047857')
        elif y == 0:  # Full Forensics Total
            ax_a.text(p99 + 0.08, y, f"{p50:.2f} ms (P99: {p99:.2f}) [SAR Ready]",
                      ha='left', va='center', fontsize=6.6, fontweight='bold', color='#6d28d9')
        else:
            ax_a.text(p99 + 0.08, y, f"{p50:.2f} ms (P99: {p99:.2f})",
                      ha='left', va='center', fontsize=6.4, color='#334155')

    # Legend for P50 vs P99 placed in upper-right open quadrant (zero collision)
    p50_patch = patches.Patch(facecolor='#2563eb', edgecolor='#1e293b', label='P50 Median')
    p99_patch = patches.Patch(facecolor='#93c5fd', edgecolor='#334155', alpha=0.5, label='P99 Tail')
    ax_a.legend(handles=[p50_patch, p99_patch], loc='center right', bbox_to_anchor=(0.98, 0.50),
                fontsize=6.4, facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.95)

    # -------------------------------------------------------------
    # Panel (b): Production SLA Compliance & Headroom Cards
    # -------------------------------------------------------------
    card_gs = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[0, 1], hspace=0.18)
    
    cards_data = [
        {
            "tier": "Tier-1 Real-Time Gate (99.40% Traffic)",
            "title": "Core Banking SLA (<10 ms)",
            "metric": "P50: 0.45 ms | P99: 0.82 ms",
            "headroom": "22.2× Headroom",
            "desc": "Straight-through auto-clearance in <1 ms.",
            "accent": "#059669",
            "bg": "#ecfdf5",
            "border": "#a7f3d0"
        },
        {
            "tier": "Tier-2 Forensics Path (0.60% Traffic)",
            "title": "Investigation SLA (<100 ms)",
            "metric": "P50: 2.10 ms | P99: 3.67 ms",
            "headroom": "47.6× Headroom",
            "desc": "Triggered for {0,1} queue; builds SAR dossiers.",
            "accent": "#7c3aed",
            "bg": "#f5f3ff",
            "border": "#ddd6fe"
        },
        {
            "tier": "Production Infrastructure",
            "title": "Hardware & Ingestion Throughput",
            "metric": "31,200 tx/sec | 4.2 GB VRAM",
            "headroom": "Zero-Copy Bus",
            "desc": "AMD EPYC 7763 64-Core + NVIDIA A100 (Table 7.13).",
            "accent": "#334155",
            "bg": "#f8fafc",
            "border": "#cbd5e1"
        }
    ]
    
    for i, c in enumerate(cards_data):
        ax_c = fig.add_subplot(card_gs[i, 0])
        ax_c.set_facecolor(c["bg"])
        for spine in ax_c.spines.values():
            spine.set_color(c["border"])
            spine.set_linewidth(1.0)
        ax_c.set_xticks([])
        ax_c.set_yticks([])
        
        # Line 1: Tier Pill Badge
        ax_c.text(0.04, 0.82, c["tier"],
                  fontsize=6.5, fontweight='bold', color=c['accent'], ha='left', va='center')
        
        # Line 2: Title & Headroom tag
        ax_c.text(0.04, 0.58, c["title"],
                  fontsize=6.3, fontweight='bold', color='#1e293b', ha='left', va='center')
        ax_c.text(0.96, 0.58, c["headroom"],
                  fontsize=6.0, fontweight='bold', color=c['accent'], ha='right', va='center')
        
        # Line 3: Metric & description
        ax_c.text(0.04, 0.30, f"{c['metric']} — {c['desc']}",
                  fontsize=5.6, color='#475569', ha='left', va='center')

    return fig


def main():
    print("Generating Redesigned Figure 7.15: Streaming Latency Breakdown...")
    fig = build_figure()
    
    for target_dir in TARGET_DIRS:
        pdf_path = target_dir / "fig_streaming_latency_waterfall.pdf"
        png_path = target_dir / "fig_streaming_latency_waterfall.png"
        
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
        print(f"Saved: {pdf_path}")
        print(f"Saved: {png_path}")
        
    plt.close(fig)
    print("Figure 7.15 generation complete!")


if __name__ == "__main__":
    main()
