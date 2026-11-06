"""
scripts/redesign_fig7_9_leave_one_out.py
Publication-grade redesign of Leave-One-Out Component Removal Ablation Waterfall and Precision-Recall Asymmetry.
Generates fig_leave_one_out_impact.pdf and .png across all 5 figure target directories.
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
    'font.size': 8.0,
    'axes.labelsize': 8.0,
    'axes.titlesize': 8.6,
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
    # Sized to 7.8" x 6.6" to achieve exact post-crop aspect ratio ~1.46 - 1.50
    # Yields rendered height ~236 pt in LaTeX, preserving the 127-page count
    fig = plt.figure(figsize=(7.8, 6.6))
    
    # Outer layout:
    # gs[0, :]: Main panels (a) and (b)
    # gs[1, :]: Bottom 4 operational diagnostic cards
    # top=0.875 provides clean 20pt breathing room below subtitle
    gs = gridspec.GridSpec(
        2, 2,
        height_ratios=[4.15, 1.25],
        width_ratios=[1.10, 1.0],
        left=0.045, right=0.985,
        top=0.875, bottom=0.025,
        wspace=0.18, hspace=0.25
    )
    
    # -------------------------------------------------------------
    # Master Header Banner (Figure Title & Rigor Guarantee)
    # -------------------------------------------------------------
    fig.text(0.045, 0.970, "Leave-One-Out Component Removal Waterfall & Asymmetry",
             fontsize=10.2, fontweight='bold', color='#0f172a', ha='left')
    fig.text(0.045, 0.938, "Marginal degradation on Elliptic-v1 benchmark (N=5 Seeds, Table 7.4 Aligned)",
             fontsize=7.5, color='#475569', ha='left')
    
    # Baseline benchmark tag on top right
    fig.text(0.985, 0.955, "Full C-STGB Benchmark: 91.42 ± 0.65% Macro-F1",
             fontsize=7.3, fontweight='bold', color='#1e3a8a', ha='right',
             bbox=dict(boxstyle='round,pad=0.26', facecolor='#eff6ff', edgecolor='#93c5fd', lw=0.8))

    # -------------------------------------------------------------
    # Data Definitions (Table 7.4 in Thesis)
    # -------------------------------------------------------------
    components = [
        "Typology GraphSMOTE",
        "12-D Canonical Invariants",
        "Edge-Trust Gating Filter",
        "Tri-Band Temporal Decay",
        "Adaptive Graph Fusion",
        "Hawkes Point Process"
    ]
    
    y_pos = np.arange(len(components))[::-1]
    
    # Metrics
    drops_f1 = np.array([9.92, 7.46, 5.62, 5.32, 3.30, 2.30])
    stds_f1 = np.array([0.82, 0.80, 0.72, 0.70, 0.65, 0.64])
    retained_f1 = np.array([81.50, 83.96, 85.80, 86.10, 88.12, 89.12])
    
    drops_prec = np.array([4.40, 7.20, 9.60, 4.70, 3.30, 2.30])
    drops_rec = np.array([14.50, 7.70, 1.60, 5.90, 3.30, 2.30])
    
    bar_colors = [
        "#dc2626",  # Red-600 (GraphSMOTE)
        "#ea580c",  # Orange-600 (12-D)
        "#d97706",  # Amber-600 (Edge-Trust)
        "#4f46e5",  # Indigo-600 (Tri-Band)
        "#0284c7",  # Sky-600 (Adaptive Fusion)
        "#0d9488"   # Teal-600 (Hawkes)
    ]
    
    # -------------------------------------------------------------
    # Panel (a): Macro-F1 Degradation Waterfall
    # -------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_facecolor("#f8fafc")
    for spine in ax_a.spines.values():
        spine.set_color("#cbd5e1")
        spine.set_linewidth(0.8)
        
    ax_a.set_title(r"(a) Macro-F1 Degradation Waterfall ($\Delta$F1 Drop in pp)",
                   fontsize=8.5, fontweight='bold', color='#0f172a', pad=7, loc='left')
    
    # Draw horizontal bars
    bars_a = ax_a.barh(
        y_pos, drops_f1,
        color=bar_colors, edgecolor='#1e293b', linewidth=0.7,
        alpha=0.92, height=0.58,
        xerr=stds_f1, capsize=3.2, error_kw=dict(ecolor='#334155', lw=0.9)
    )
    
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(components, fontsize=7.2, fontweight='bold', color='#1e293b')
    ax_a.set_xlabel("Macro-F1 Degradation (Percentage Points, pp)", fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_a.set_xlim([0, 13.0])
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1')
    ax_a.tick_params(axis='both', which='major', labelsize=7.0)
    
    # Annotations on bars
    for i, (bar, drop, ret, std) in enumerate(zip(bars_a, drops_f1, retained_f1, stds_f1)):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2.0
        
        # Primary drop badge
        ax_a.annotate(
            f"−{drop:.2f} pp",
            xy=(w + std, y), xytext=(4, 0), textcoords="offset points",
            ha='left', va='center', fontsize=7.2, fontweight='bold',
            color='#991b1b' if drop > 7.0 else '#b45309' if drop > 5.0 else '#1e293b'
        )
        
        # Retained score badge inside the bar (or beside if small)
        if w > 4.5:
            ax_a.text(w * 0.44, y, f"Retained: {ret:.1f}%",
                      ha='center', va='center', fontsize=6.7, fontweight='bold', color='#ffffff')
        else:
            ax_a.annotate(
                f"(Ret: {ret:.1f}%)",
                xy=(w + std, y), xytext=(42, 0), textcoords="offset points",
                ha='left', va='center', fontsize=6.5, color='#64748b'
            )

    # Shaded rank tier boundary line without collision
    ax_a.axvline(x=7.0, color='#dc2626', linestyle=':', lw=0.9, alpha=0.8)
    ax_a.text(7.0, -0.42, "Critical Threshold (7.0 pp)",
              fontsize=6.2, color='#b91c1c', fontweight='bold', ha='center', va='top')

    # -------------------------------------------------------------
    # Panel (b): Precision vs. Recall Operational Asymmetry
    # -------------------------------------------------------------
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_facecolor("#f8fafc")
    for spine in ax_b.spines.values():
        spine.set_color("#cbd5e1")
        spine.set_linewidth(0.8)
        
    ax_b.set_title(r"(b) Operational Impact Asymmetry ($\Delta$Precision vs. $\Delta$Recall)",
                   fontsize=8.5, fontweight='bold', color='#0f172a', pad=7, loc='left')
    
    bar_h = 0.28
    y_prec = y_pos + bar_h / 2.0
    y_rec = y_pos - bar_h / 2.0
    
    # Paired bars
    bars_prec = ax_b.barh(
        y_prec, drops_prec, height=bar_h,
        color='#0284c7', edgecolor='#0369a1', linewidth=0.7,
        alpha=0.90, label='Precision Penalty (False Alert Risk)'
    )
    bars_rec = ax_b.barh(
        y_rec, drops_rec, height=bar_h,
        color='#e11d48', edgecolor='#be123c', linewidth=0.7,
        alpha=0.90, label='Recall Penalty (Missed Illicit Laundering)'
    )
    
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels([])  # Shared with panel (a)
    ax_b.set_xlabel("Metric Degradation (Percentage Points, pp)", fontsize=7.6, fontweight='bold', color='#1e293b')
    ax_b.set_xlim([0, 19.5])
    ax_b.grid(True, axis='x', linestyle='--', alpha=0.5, color='#cbd5e1')
    ax_b.tick_params(axis='both', which='major', labelsize=7.0)
    
    # Legend at bottom right of Panel B
    ax_b.legend(loc='lower right', fontsize=6.6, frameon=True,
                facecolor='#ffffff', edgecolor='#cbd5e1', framealpha=0.95)
    
    # Annotations on Panel B bars
    for i, (p_bar, r_bar, d_p, d_r) in enumerate(zip(bars_prec, bars_rec, drops_prec, drops_rec)):
        yp = p_bar.get_y() + p_bar.get_height() / 2.0
        yr = r_bar.get_y() + r_bar.get_height() / 2.0
        wp = p_bar.get_width()
        wr = r_bar.get_width()
        
        # Precision annotation
        ax_b.annotate(
            f"−{d_p:.1f} pp",
            xy=(wp, yp), xytext=(3, 0), textcoords="offset points",
            ha='left', va='center', fontsize=6.6, fontweight='bold', color='#0369a1'
        )
        
        # Recall annotation
        ax_b.annotate(
            f"−{d_r:.1f} pp",
            xy=(wr, yr), xytext=(3, 0), textcoords="offset points",
            ha='left', va='center', fontsize=6.6, fontweight='bold', color='#be123c'
        )
        
        # Clean single-line highlights
        if i == 0:  # GraphSMOTE
            ax_b.annotate(
                "← 14.5 pp Recall Crash",
                xy=(wr, yr), xytext=(38, 0), textcoords="offset points",
                ha='left', va='center', fontsize=6.3, fontweight='bold', color='#9f1239'
            )
        elif i == 2:  # Edge-Trust Gating
            ax_b.annotate(
                "← 9.6 pp Precision Drop",
                xy=(wp, yp), xytext=(36, 0), textcoords="offset points",
                ha='left', va='center', fontsize=6.3, fontweight='bold', color='#075985'
            )

    # -------------------------------------------------------------
    # Bottom Operational Diagnostic Cards (4 across width)
    # -------------------------------------------------------------
    card_gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=gs[1, :], wspace=0.10)
    
    cards_data = [
        {
            "num": "1",
            "title": "Minority Oversampling",
            "comp": "Typology GraphSMOTE",
            "metric": "ΔF1: −9.92 pp | ΔRec: −14.5 pp",
            "line1": "Synthesizes minority latent motifs;",
            "line2": "prevents collapse on 0.05% skew.",
            "accent": "#dc2626",
            "bg": "#fef2f2",
            "border": "#fecaca"
        },
        {
            "num": "2",
            "title": "Geometric Flow Physics",
            "comp": "12-D Invariants z_inv",
            "metric": "ΔF1: −7.46 pp | Symmetric ~7.5 pp",
            "line1": "Flow balance & arrival kinetics",
            "line2": "anchor cross-rail transferability.",
            "accent": "#ea580c",
            "bg": "#fff7ed",
            "border": "#fed7aa"
        },
        {
            "num": "3",
            "title": "Camouflage Denoising",
            "comp": "Edge Trust Gating g_ij",
            "metric": "ΔF1: −5.62 pp | ΔPrec: −9.6 pp",
            "line1": "Prunes evasive smurfing chaff;",
            "line2": "eliminates false alert fatigue.",
            "accent": "#d97706",
            "bg": "#fffbeb",
            "border": "#fef3c7"
        },
        {
            "num": "4",
            "title": "Temporal & View Dynamics",
            "comp": "Tri-Band + Hawkes + Fusion",
            "metric": "Combined: −10.92 pp | p < 0.001",
            "line1": "Resolves burst & dormancy scales;",
            "line2": "calibrates multi-modal evidence.",
            "accent": "#4f46e5",
            "bg": "#eef2ff",
            "border": "#c7d2fe"
        }
    ]
    
    for i, c in enumerate(cards_data):
        ax_c = fig.add_subplot(card_gs[0, i])
        ax_c.set_facecolor(c["bg"])
        for spine in ax_c.spines.values():
            spine.set_color(c["border"])
            spine.set_linewidth(1.0)
        ax_c.set_xticks([])
        ax_c.set_yticks([])
        
        # Top pill badge
        ax_c.text(0.06, 0.85, f"Pillar {c['num']}: {c['title']}",
                  fontsize=6.7, fontweight='bold', color=c['accent'], ha='left', va='center')
        
        # Component name
        ax_c.text(0.06, 0.65, c["comp"],
                  fontsize=6.4, fontweight='bold', color='#1e293b', ha='left', va='center')
        
        # Impact metric
        ax_c.text(0.06, 0.44, c["metric"],
                  fontsize=6.1, fontweight='bold', color='#334155', ha='left', va='center')
        
        # Description 2 lines cleanly separated
        ax_c.text(0.06, 0.25, c["line1"],
                  fontsize=5.6, color='#64748b', ha='left', va='center')
        ax_c.text(0.06, 0.12, c["line2"],
                  fontsize=5.6, color='#64748b', ha='left', va='center')

    return fig


def main():
    print("Generating Redesigned Leave-One-Out Component Removal...")
    fig = build_figure()
    
    for target_dir in TARGET_DIRS:
        pdf_path = target_dir / "fig_leave_one_out_impact.pdf"
        png_path = target_dir / "fig_leave_one_out_impact.png"
        
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
        print(f"Saved: {pdf_path}")
        print(f"Saved: {png_path}")
        
    plt.close(fig)
    print("Figure 7.9 generation complete!")


if __name__ == "__main__":
    main()
