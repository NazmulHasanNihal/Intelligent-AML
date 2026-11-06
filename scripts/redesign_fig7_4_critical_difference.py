"""
scripts/redesign_fig7_4_critical_difference.py
Publication-grade redesign of Figure 7.4:
Statistical Significance and Domain Archetype Performance Synthesis.
Generates fig_critical_difference_lollipop.pdf and .png across all 5 figure target directories.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    'axes.labelsize': 8.5,
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

def generate_figure_7_4():
    # Sized 9.8 x 3.6 inches (aspect ratio ~2.72:1) for Page 80 multi-figure fit
    fig, (ax_cd, ax_dom) = plt.subplots(1, 2, figsize=(9.8, 3.6), gridspec_kw={'width_ratios': [1.12, 1.28]})
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.12, wspace=0.28)

    # =========================================================================
    # SUBPLOT (A): CRITICAL DIFFERENCE (CD) RANK SPECTRUM (DEMSAR 2006)
    # =========================================================================
    ax_cd.axis("off")
    ax_cd.set_xlim(0.5, 8.5)
    ax_cd.set_ylim(-0.18, 1.18)

    # Title
    ax_cd.text(4.5, 1.15, "(a) Wilcoxon-Holm Critical Difference Rank Spectrum",
               ha="center", va="center", fontsize=8.6, weight="bold", color="#0f172a")

    # Critical Difference Caliper at top
    cd_val = 1.45
    caliper_y = 1.00
    ax_cd.plot([1.0, 1.0 + cd_val], [caliper_y, caliper_y], color="#dc2626", lw=2.0, zorder=3)
    ax_cd.plot([1.0, 1.0], [caliper_y - 0.04, caliper_y + 0.04], color="#dc2626", lw=1.5, zorder=3)
    ax_cd.plot([1.0 + cd_val, 1.0 + cd_val], [caliper_y - 0.04, caliper_y + 0.04], color="#dc2626", lw=1.5, zorder=3)
    ax_cd.text(1.0 + cd_val / 2.0, caliper_y + 0.06, r"$\mathrm{CD} = 1.45$ ($\alpha = 0.05$ Holm)",
               ha="center", va="bottom", fontsize=6.2, weight="bold", color="#991b1b")

    # Shaded Significance Separation Band between C-STGB and GNNs (positioned cleanly above axis)
    rect_sep = patches.Rectangle((1.07 + cd_val, 0.60), 4.21 - (1.07 + cd_val), 0.22,
                                 facecolor="#fee2e2", edgecolor="#fca5a5", linestyle=":", lw=0.8, alpha=0.6, zorder=1)
    ax_cd.add_patch(rect_sep)
    ax_cd.text((1.07 + cd_val + 4.21) / 2.0, 0.71, "Statistically Significant Lead\nOver Deep GNNs (p < 0.001)",
               ha="center", va="center", fontsize=5.0, weight="bold", color="#991b1b", style="italic", zorder=2)

    # Main Horizontal Rank Axis (y = 0.50)
    ax_cd.plot([1.0, 8.0], [0.50, 0.50], color="#0f172a", lw=1.8, zorder=2)

    # Rank Ticks and Numbers
    for r in range(1, 9):
        ax_cd.plot([r, r], [0.46, 0.54], color="#0f172a", lw=1.0, zorder=3)
        tick_label = f"{r} (Best)" if r == 1 else (f"{r} (Worst)" if r == 8 else f"{r}")
        ax_cd.text(r, 0.41, tick_label, ha="center", va="top", fontsize=5.8, weight="bold", color="#334155")

    # Models Specification
    # Staggered: 4 models above axis, 4 models below axis to completely eliminate overlap
    models = [
        {"name": "C-STGB (Ours)", "rank": 1.07, "pos": "top",    "color": "#059669", "marker": "o", "sz": 55},
        {"name": "XGBoost",       "rank": 2.43, "pos": "bottom", "color": "#2563eb", "marker": "s", "sz": 40},
        {"name": "CatBoost",      "rank": 2.79, "pos": "top",    "color": "#1d4ed8", "marker": "s", "sz": 40},
        {"name": "TGN",           "rank": 4.21, "pos": "bottom", "color": "#d97706", "marker": "D", "sz": 40},
        {"name": "CARE-GNN",      "rank": 5.14, "pos": "top",    "color": "#ea580c", "marker": "D", "sz": 40},
        {"name": "GCN",           "rank": 6.71, "pos": "bottom", "color": "#dc2626", "marker": "^", "sz": 40},
        {"name": "GraphSAGE",     "rank": 6.86, "pos": "top",    "color": "#b91c1c", "marker": "^", "sz": 40},
        {"name": "EvolveGCN",     "rank": 7.79, "pos": "bottom", "color": "#991b1b", "marker": "v", "sz": 40},
    ]

    # Non-significant clique horizontal bars
    # Tree clique: XGBoost (2.43) to CatBoost (2.79) - delta = 0.36 < CD
    ax_cd.plot([2.43, 2.79], [0.55, 0.55], color="#2563eb", lw=3.0, solid_capstyle="round", zorder=4)
    # Temporal GNN clique: TGN (4.21) to CARE-GNN (5.14) - delta = 0.93 < CD
    ax_cd.plot([4.21, 5.14], [0.55, 0.55], color="#d97706", lw=3.0, solid_capstyle="round", zorder=4)
    # Static GNN clique: GCN (6.71) to EvolveGCN (7.79) - delta = 1.08 < CD
    ax_cd.plot([6.71, 7.79], [0.55, 0.55], color="#dc2626", lw=3.0, solid_capstyle="round", zorder=4)

    # Plot points and leader lines
    for m in models:
        r_val = m["rank"]
        clr = m["color"]
        ax_cd.scatter([r_val], [0.50], color=clr, edgecolors="#0f172a", s=m["sz"], marker=m["marker"], zorder=5)

        if m["pos"] == "top":
            y_leader = 0.72
            ax_cd.plot([r_val, r_val], [0.50, y_leader], color=clr, lw=0.9, linestyle=":", zorder=3)
            ax_cd.text(r_val, 0.85, m["name"], ha="center", va="center", fontsize=5.8, weight="bold", color=clr)
            ax_cd.text(r_val, 0.76, f"Rank {r_val:.2f}", ha="center", va="center", fontsize=5.4, color="#334155")
        else:
            y_leader = 0.28
            ax_cd.plot([r_val, r_val], [0.50, y_leader], color=clr, lw=0.9, linestyle=":", zorder=3)
            ax_cd.text(r_val, 0.24, m["name"], ha="center", va="center", fontsize=5.8, weight="bold", color=clr)
            ax_cd.text(r_val, 0.15, f"Rank {r_val:.2f}", ha="center", va="center", fontsize=5.4, color="#334155")

    # Bottom Legend for Subplot (a)
    ax_cd.text(4.5, -0.12, "Connected horizontal clique bars indicate no statistically significant difference (p > 0.05)",
               ha="center", va="center", fontsize=5.6, style="italic", color="#475569")

    # =========================================================================
    # SUBPLOT (B): GROUPED MACRO F1 PERFORMANCE BY DOMAIN ARCHETYPE
    # =========================================================================
    # 4 Domain Categories: Public Crypto, Multi-Bank, Card Stream, Overall Macro
    domains = [
        "Public Crypto (4)",
        "Multi-Bank (9)",
        "Card Stream (1)",
        "Overall Macro (14)"
    ]

    cstgb_vals = [90.53, 59.34, 56.48, 68.05]
    xgb_vals   = [86.76, 56.32, 48.20, 64.76]
    gnn_vals   = [60.95, 37.80, 38.20, 43.76]

    y_indices = np.arange(len(domains))
    bar_h = 0.22

    # Invert order so Overall Macro is at top, or Public Crypto is at top
    # We display Public Crypto at top (y=3), down to Overall Macro at bottom (y=0)
    # Using inverted y_indices:
    y_pos = y_indices[::-1]

    # Draw Grouped Bars
    bars_cstgb = ax_dom.barh(y_pos + bar_h, cstgb_vals, height=bar_h, color="#059669", edgecolor="#047857", lw=0.9, label="C-STGB (Proposed)", zorder=3)
    bars_xgb   = ax_dom.barh(y_pos,         xgb_vals,   height=bar_h, color="#2563eb", edgecolor="#1d4ed8", lw=0.9, label="Best Tree (XGBoost)", zorder=3)
    bars_gnn   = ax_dom.barh(y_pos - bar_h, gnn_vals,   height=bar_h, color="#dc2626", edgecolor="#b91c1c", lw=0.9, label="Best GNN (TGN/CARE)", zorder=3)

    # Value Labels and Margins
    for i in range(len(domains)):
        yp = y_pos[i]
        c_v = cstgb_vals[i]
        x_v = xgb_vals[i]
        g_v = gnn_vals[i]

        # C-STGB label
        lead_tree = c_v - x_v
        lead_gnn  = c_v - g_v
        ax_dom.text(c_v + 1.2, yp + bar_h, f"{c_v:.1f}% (+{lead_tree:.1f}%)",
                    ha="left", va="center", fontsize=5.8, weight="bold", color="#065f46", zorder=4)

        # XGBoost label
        ax_dom.text(x_v + 1.2, yp, f"{x_v:.1f}%",
                    ha="left", va="center", fontsize=5.6, color="#1e40af", zorder=4)

        # GNN label
        ax_dom.text(g_v + 1.2, yp - bar_h, f"{g_v:.1f}%",
                    ha="left", va="center", fontsize=5.6, color="#991b1b", zorder=4)

    ax_dom.set_yticks(y_pos)
    ax_dom.set_yticklabels(domains, fontsize=7.2, weight="bold", color="#0f172a")
    ax_dom.set_xlabel("Minority Macro F1-Score (%)", fontsize=7.8, weight="bold", color="#0f172a")
    ax_dom.set_xlim(0, 115)
    ax_dom.set_ylim(-0.55, len(domains) - 0.25)
    ax_dom.grid(True, axis="x", linestyle=":", alpha=0.55, color="#94a3b8")

    # Title of Subplot (b)
    ax_dom.set_title("(b) Performance Synthesis by Domain Archetype",
                     fontsize=8.6, weight="bold", color="#0f172a", pad=10)

    # Legend at Top of Subplot (b)
    ax_dom.legend(loc="upper left", bbox_to_anchor=(0.00, 1.05), ncol=3, fontsize=5.8,
                  frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1", borderaxespad=0.2)

    return fig

def main():
    print("Generating redesigned Figure 7.4 (Statistical Significance and Domain Archetype Synthesis)...")
    fig = generate_figure_7_4()

    # Save to all target directories
    for d in TARGET_DIRS:
        for stem in ["fig_critical_difference_lollipop", "fig7_3_critical_difference_lollipop"]:
            pdf_path = d / f"{stem}.pdf"
            png_path = d / f"{stem}.png"
            fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
            fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
            print(f"Saved: {pdf_path}")
            print(f"Saved: {png_path}")

    # Also save to artifact directory for inspection
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_4_redesigned_final.png")
    fig.savefig(artifact_png, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
    print(f"Saved artifact copy: {artifact_png}")

    plt.close(fig)
    print("Generation complete!")

if __name__ == "__main__":
    main()

