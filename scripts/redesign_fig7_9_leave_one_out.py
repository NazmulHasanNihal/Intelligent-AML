"""
scripts/redesign_fig7_9_leave_one_out.py
Publication-grade redesign of Figure 7.9:
Leave-One-Out Component Removal Ablation Waterfall & Decoupled Precision-Recall Asymmetry.
Strictly NO cards: pure technical engineering plots with formal annotations and full LaTeX math.
Generates fig_leave_one_out_impact.pdf and .png across all 5 directories.
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
    fig = plt.figure(figsize=(9.6, 4.8), dpi=300)
    
    gs = gridspec.GridSpec(
        2, 2,
        height_ratios=[3.6, 1.1],
        width_ratios=[1.15, 1.0],
        left=0.06, right=0.98,
        top=0.90, bottom=0.06,
        wspace=0.22, hspace=0.32
    )

    # -------------------------------------------------------------
    # Master Header Banner
    # -------------------------------------------------------------
    fig.text(0.06, 0.965, "Leave-One-Out Component Removal Waterfall & Asymmetry Analysis",
             fontsize=10.2, fontweight='bold', color='#0f172a', ha='left')
    fig.text(0.06, 0.930, "Marginal degradation on Elliptic-v1 benchmark (N=5 Seeds, Table 7.4 Aligned) — Full Model: 91.42 ± 0.65% F1",
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
                   fontsize=8.6, fontweight='bold', color='#0f172a', pad=8)
    
    bars_a = ax_a.barh(
        y_pos, drops_f1, xerr=stds_f1, height=0.55,
        color=bar_colors, edgecolor='#0f172a', linewidth=0.8,
        error_kw=dict(ecolor='#334155', lw=1.2, capsize=3, capthick=1.0),
        zorder=3
    )
    
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(components, fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("F1 Degradation (−pp relative to 91.42%)", fontsize=8.0, fontweight='bold', color='#1e293b')
    ax_a.set_xlim([0, 13.5])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)
    
    for y, d, s, ret in zip(y_pos, drops_f1, stds_f1, retained_f1):
        ax_a.text(d + s + 0.35, y, f"−{d:.2f} pp  ({ret:.2f}% F1)",
                  ha='left', va='center', fontsize=7.2, fontweight='bold', color='#0f172a', zorder=4)

    # =============================================================
    # PANEL (B): PRECISION VS RECALL ASYMMETRY
    # =============================================================
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title(r"(b) Decoupled Sensitivity: Precision Drop vs Recall Crash",
                   fontsize=8.6, fontweight='bold', color='#0f172a', pad=8)
    
    bar_h = 0.30
    bars_p = ax_b.barh(y_pos + bar_h/2, drops_prec, height=bar_h, color='#0284c7', edgecolor='#0369a1',
                       linewidth=0.8, label=r'$\Delta\mathrm{Precision}$ (False Positives)', zorder=3)
    bars_r = ax_b.barh(y_pos - bar_h/2, drops_rec, height=bar_h, color='#e11d48', edgecolor='#be123c',
                       linewidth=0.8, label=r'$\Delta\mathrm{Recall}$ (Missed Laundering)', zorder=3)
    
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels(["" for _ in y_pos])  # Shared with left
    ax_b.set_xlabel("Metric Degradation (−pp)", fontsize=8.0, fontweight='bold', color='#1e293b')
    ax_b.set_xlim([0, 17.5])
    ax_b.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1', zorder=1)
    ax_b.legend(loc='lower right', fontsize=7.2, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')
    
    # Text callouts for key extremes
    ax_b.text(drops_rec[0] + 0.4, y_pos[0] - bar_h/2, "−14.5 pp (Recall Crash)",
              ha='left', va='center', fontsize=6.8, fontweight='bold', color='#be123c')
    ax_b.text(drops_prec[2] + 0.4, y_pos[2] + bar_h/2, "−9.6 pp (Precision Drop)",
              ha='left', va='center', fontsize=6.8, fontweight='bold', color='#0369a1')

    # =============================================================
    # BOTTOM PANEL (C): FORMAL MECHANISM DECOUPLING TABLE (NO CARDS!)
    # =============================================================
    ax_tbl = fig.add_subplot(gs[1, :])
    ax_tbl.axis('off')

    col_widths = [0.22, 0.16, 0.38, 0.24]
    cols = ["Architectural Component", "Marginal Impact", "Theoretical & Operational Failure Mode", "Statutory Risk"]
    
    table_data = [
        ["Typology GraphSMOTE", "ΔF1: −9.92 pp\nΔRec: −14.5 pp", "Severe minority class collapse under 0.05% skew; failure to learn motifs", "High FN Regulatory Fines"],
        ["12-D Canonical Invariants", "ΔF1: −7.46 pp\nSymmetric drop", "Violation of flow conservation & capital velocity kinetics across hops", "Cross-Rail Non-Transfer"],
        ["Edge-Trust Gating", "ΔF1: −5.62 pp\nΔPrec: −9.6 pp", "Spurious camouflage chaff overwhelms message passing (smurfing noise)", "Severe Alert Fatigue"],
        ["Tri-Band Decay + Hawkes", "ΔF1: −7.62 pp\nTime sensitivity", "Inability to decouple microsecond transaction bursts from 90-day dormancy", "Evasion via Temporal Gap"]
    ]

    # Draw structured table grid
    y_top = 0.98
    row_h = 0.22
    
    # Table Header
    ax_tbl.add_patch(patches.Rectangle((0, y_top - 0.22), 1.0, 0.22, facecolor='#1e293b', edgecolor='#0f172a', lw=0.8))
    x_curr = 0.0
    for w, c in zip(col_widths, cols):
        ax_tbl.text(x_curr + 0.01, y_top - 0.11, c, ha='left', va='center', fontsize=7.0, fontweight='bold', color='#ffffff')
        x_curr += w

    # Table Rows
    y_row = y_top - 0.22
    for r_idx, row in enumerate(table_data):
        bg = "#f8fafc" if r_idx % 2 == 0 else "#ffffff"
        ax_tbl.add_patch(patches.Rectangle((0, y_row - row_h), 1.0, row_h, facecolor=bg, edgecolor='#e2e8f0', lw=0.6))
        x_curr = 0.0
        for w, val in zip(col_widths, row):
            fontweight = 'bold' if w in [col_widths[0], col_widths[1]] else 'normal'
            color = '#0f172a' if w != col_widths[3] else '#b91c1c'
            ax_tbl.text(x_curr + 0.01, y_row - row_h/2, val, ha='left', va='center', fontsize=6.2,
                        fontweight=fontweight, color=color)
            x_curr += w
        y_row -= row_h

    return fig

def main():
    print("Generating redesigned Figure 7.9 (Leave-One-Out Component Removal Analysis)...")
    fig = build_figure()

    for d in TARGET_DIRS:
        for stem in ["fig_leave_one_out_impact", "fig7_9_leave_one_out"]:
            pdf_path = d / f"{stem}.pdf"
            png_path = d / f"{stem}.png"
            fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.10)
            fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
            print(f" [OK] Saved: {pdf_path}")

    artifact_path = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_9_redesigned_final.png")
    fig.savefig(artifact_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
    print(f" [OK] Saved artifact: {artifact_path}")
    plt.close(fig)
    print("Figure 7.9 redesign completed successfully!")

if __name__ == "__main__":
    main()
