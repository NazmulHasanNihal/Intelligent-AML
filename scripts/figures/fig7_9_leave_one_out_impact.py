"""
Figure 7.9: Leave-One-Out Component Removal Waterfall & Asymmetry Analysis
Redesigned with expanded xlim, widened canvas, and an enlarged, highly legible component impact table.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig = plt.figure(figsize=(10.8, 6.4), dpi=300)
    
    gs = gridspec.GridSpec(
        2, 2,
        height_ratios=[2.8, 1.8],
        width_ratios=[1.15, 1.0],
        left=0.06, right=0.98,
        top=0.88, bottom=0.06,
        wspace=0.22, hspace=0.38
    )

    # -------------------------------------------------------------
    # Master Header Banner
    # -------------------------------------------------------------
    fig.text(0.06, 0.965, "Leave-One-Out Component Removal Waterfall & Asymmetry Analysis",
             fontsize=10.2, fontweight='bold', color='#0f172a', ha='left')
    fig.text(0.06, 0.932, "Marginal degradation on Elliptic-v1 benchmark (N=5 Seeds, Table 7.4 Aligned) — Full Model: 91.42 ± 0.65% F1",
             fontsize=7.6, color='#475569', ha='left')

    # Component definitions
    components = [
        r"Typology GraphSMOTE",
        r"12-D Canonical Invariants ($\mathbf{z}_{\mathrm{inv}}$)",
        r"Edge-Trust Gating ($\hat{g}_{ij} \geq 0.10$)",
        r"Tri-Band Temporal Decay ($w(\Delta t)$)",
        r"Adaptive Graph-Tabular Fusion ($\mathbf{h}_u^*$)",
        r"Hawkes Intensity ($\lambda_u(t)$)"
    ]
    
    y_pos = np.arange(len(components))[::-1]
    
    drops_f1 = np.array([9.92, 7.46, 5.62, 5.32, 3.30, 2.30])
    stds_f1 = np.array([0.82, 0.80, 0.72, 0.70, 0.65, 0.64])
    retained_f1 = np.array([81.50, 83.96, 85.80, 86.10, 88.12, 89.12])
    
    drops_prec = np.array([4.40, 7.20, 9.60, 4.70, 3.30, 2.30])
    drops_rec = np.array([14.50, 7.70, 1.60, 5.90, 3.30, 2.30])

    bar_colors = [
        "#dc2626",  # Red-600
        "#ea580c",  # Orange-600
        "#d97706",  # Amber-600
        "#0284c7",  # Sky-600
        "#2563eb",  # Blue-600
        "#4f46e5",  # Indigo-600
    ]

    # =============================================================
    # PANEL (A): F1 DEGRADATION WATERFALL
    # =============================================================
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_title(r"(a) Marginal Macro F1 Degradation ($\Delta\mathrm{F1}$ in percentage points)",
                   fontsize=8.8, fontweight='bold', color='#0f172a', pad=8)
    
    bars_a = ax_a.barh(
        y_pos, drops_f1, xerr=stds_f1, height=0.55,
        color=bar_colors, edgecolor='#0f172a', linewidth=0.8,
        error_kw=dict(ecolor='#334155', lw=1.2, capsize=3, capthick=1.0),
        zorder=3
    )
    
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(components, fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("F1 Degradation (−pp relative to 91.42%)", fontsize=8.0, fontweight='bold', color='#1e293b')
    # Expanded xlim to 16.0 so the 9.92 pp label fits cleanly with plenty of margin
    ax_a.set_xlim([0, 16.0])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)
    
    for y, d, s, ret in zip(y_pos, drops_f1, stds_f1, retained_f1):
        ax_a.text(d + s + 0.35, y, f"−{d:.2f} pp  ({ret:.2f}% F1)",
                  ha='left', va='center', fontsize=6.8, fontweight='bold', color='#0f172a', zorder=4)

    # =============================================================
    # PANEL (B): PRECISION VS RECALL ASYMMETRY
    # =============================================================
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title(r"(b) Decoupled Sensitivity: Precision Drop vs Recall Crash",
                   fontsize=8.8, fontweight='bold', color='#0f172a', pad=8)
    
    bar_h = 0.30
    bars_p = ax_b.barh(y_pos + bar_h/2, drops_prec, height=bar_h, color='#0284c7', edgecolor='#0369a1',
                       linewidth=0.8, label=r'$\Delta\mathrm{Precision}$ (False Positives)', zorder=3)
    bars_r = ax_b.barh(y_pos - bar_h/2, drops_rec, height=bar_h, color='#e11d48', edgecolor='#be123c',
                       linewidth=0.8, label=r'$\Delta\mathrm{Recall}$ (Missed Laundering)', zorder=3)
    
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels(["" for _ in y_pos])  # Shared with left
    ax_b.set_xlabel("Metric Degradation (−pp)", fontsize=8.0, fontweight='bold', color='#1e293b')
    ax_b.set_xlim([0, 18.5])
    ax_b.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)
    ax_b.legend(loc='lower right', fontsize=7.2, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')
    
    # Text callouts for key extremes
    ax_b.text(drops_rec[0] + 0.4, y_pos[0] - bar_h/2, "−14.5 pp (Recall Crash)",
              ha='left', va='center', fontsize=6, fontweight='bold', color='#be123c')
    ax_b.text(drops_prec[2] + 0.4, y_pos[2] + bar_h/2, "−9.6 pp (Precision Drop)",
              ha='left', va='center', fontsize=6, fontweight='bold', color='#0369a1')

    # =============================================================
    # BOTTOM PANEL (C): ENLARGED, HIGHLY READABLE MECHANISM TABLE
    # =============================================================
    ax_tbl = fig.add_subplot(gs[1, :])
    ax_tbl.axis('off')
    ax_tbl.set_xlim(0, 1.0)
    ax_tbl.set_ylim(0, 1.0)

    col_widths = [0.24, 0.16, 0.38, 0.22]
    cols = ["Architectural Component", "Marginal Impact", "Theoretical & Operational Failure Mode", "Statutory Risk"]
    
    table_data = [
        ["Typology GraphSMOTE", "ΔF1: −9.92 pp\nΔRec: −14.5 pp", "Severe minority class collapse under 0.05% skew; failure to learn motifs", "High FN Regulatory Fines"],
        ["12-D Canonical Invariants", "ΔF1: −7.46 pp\nSymmetric drop", "Violation of flow conservation & capital velocity kinetics across hops", "Cross-Rail Non-Transfer"],
        ["Edge-Trust Gating", "ΔF1: −5.62 pp\nΔPrec: −9.6 pp", "Spurious camouflage chaff overwhelms message passing (smurfing noise)", "Severe Alert Fatigue"],
        ["Tri-Band Decay + Hawkes", "ΔF1: −7.62 pp\nTime sensitivity", "Inability to decouple microsecond transaction bursts from 90-day dormancy", "Evasion via Temporal Gap"]
    ]

    # Draw structured table grid
    y_top = 0.96
    hdr_h = 0.18
    row_h = 0.195
    
    # Table Header
    ax_tbl.add_patch(patches.Rectangle((0, y_top - hdr_h), 1.0, hdr_h, facecolor='#1e293b', edgecolor='#0f172a', lw=0.9))
    x_curr = 0.0
    for w, c in zip(col_widths, cols):
        ax_tbl.text(x_curr + 0.012, y_top - hdr_h/2, c, ha='left', va='center', fontsize=7.6, fontweight='bold', color='#ffffff')
        x_curr += w

    # Table Rows
    for r_idx, row in enumerate(table_data):
        y_r = y_top - hdr_h - (r_idx + 1) * row_h
        bg_col = "#ffffff" if (r_idx % 2 == 0) else "#f8fafc"
        ax_tbl.add_patch(patches.Rectangle((0, y_r), 1.0, row_h, facecolor=bg_col, edgecolor='#cbd5e1', lw=0.6))
        
        x_c = 0.0
        # Col 0: Component Name
        ax_tbl.text(x_c + 0.012, y_r + row_h/2, row[0], ha='left', va='center', fontsize=7.4, fontweight='bold', color='#0f172a')
        x_c += col_widths[0]
        # Col 1: Marginal Impact
        ax_tbl.text(x_c + 0.012, y_r + row_h/2, row[1], ha='left', va='center', fontsize=7.2, fontweight='bold', color='#b91c1c')
        x_c += col_widths[1]
        # Col 2: Theoretical Failure Mode
        ax_tbl.text(x_c + 0.012, y_r + row_h/2, row[2], ha='left', va='center', fontsize=7.0, color='#334155')
        x_c += col_widths[2]
        # Col 3: Statutory Risk
        ax_tbl.text(x_c + 0.012, y_r + row_h/2, row[3], ha='left', va='center', fontsize=7.0, fontweight='bold', color='#d97706')

    save_figure(fig, "fig_leave_one_out_impact", pad_inches=0.10)
    save_figure(fig, "fig17_leave_one_out_impact", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
