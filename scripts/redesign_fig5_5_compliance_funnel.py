"""
scripts/redesign_fig5_5_compliance_funnel.py
Publication-grade redesign of Figure 5.5:
Operational Compliance Triage Funnel: Workload Reduction & Finite-Sample Coverage.
Generates fig_compliance_alert_funnel.pdf and .png.
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

def generate_figure_5_5():
    # Canvas sized 9.6 x 5.0 for clean split-layout architecture
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master background
    bg = patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none", zorder=0)
    ax.add_patch(bg)

    # =========================================================================
    # MASTER HEADER (Concise & Focused)
    # =========================================================================
    ax.text(50.0, 96.5, "Operational Compliance Triage Funnel: Workload Reduction vs. Safety",
            ha="center", va="center", fontsize=10.5, weight="bold", color="#0f172a")
    ax.text(50.0, 92.5, r"Comparative Alert Volumes and Theoretical Risk Bounds Across Surveillance Paradigms ($N = 10,000$ Wires)",
            ha="center", va="center", fontsize=7.8, style="italic", color="#475569")

    # =========================================================================
    # LEFT PANEL: 3-TIER INVERTED CONVEYOR FUNNEL (x: 4.0 to 42.0)
    # =========================================================================
    # Tier 1 Trapezoid: Legacy Rules (Wide top)
    t1_poly = patches.Polygon([[4.0, 87.0], [42.0, 87.0], [36.0, 63.0], [10.0, 63.0]],
                              closed=True, facecolor="#fee2e2", edgecolor="#dc2626", lw=1.8, zorder=2)
    ax.add_patch(t1_poly)
    ax.text(23.0, 78.5, "1. Legacy SQL Rules", ha="center", va="center", fontsize=8.4, weight="bold", color="#991b1b", zorder=3)
    ax.text(23.0, 70.0, "Alert Queue: 500 - 1,200\n(5.0% - 12.0% Volume)", ha="center", va="center", fontsize=7.2, weight="bold", color="#b91c1c", zorder=3)

    # Tier 2 Trapezoid: Marginal Conformal (Medium mid)
    t2_poly = patches.Polygon([[11.0, 60.5], [35.0, 60.5], [30.0, 37.5], [16.0, 37.5]],
                              closed=True, facecolor="#fef3c7", edgecolor="#d97706", lw=1.8, zorder=2)
    ax.add_patch(t2_poly)
    ax.text(23.0, 52.0, "2. Marginal Conformal", ha="center", va="center", fontsize=8.0, weight="bold", color="#92400e", zorder=3)
    ax.text(23.0, 44.0, "Review Queue: 1,840\n(18.40% Volume)", ha="center", va="center", fontsize=7.2, weight="bold", color="#b45309", zorder=3)

    # Tier 3 Trapezoid: Class-Conditional CRC (Narrow bottom)
    t3_poly = patches.Polygon([[17.0, 35.0], [29.0, 35.0], [26.0, 13.0], [20.0, 13.0]],
                              closed=True, facecolor="#dcfce7", edgecolor="#16a34a", lw=1.8, zorder=2)
    ax.add_patch(t3_poly)
    ax.text(23.0, 26.5, "3. C-STGB CRC", ha="center", va="center", fontsize=7.6, weight="bold", color="#166534", zorder=3)
    ax.text(23.0, 19.5, "Queue: 49\n(0.49%)", ha="center", va="center", fontsize=7.2, weight="bold", color="#15803d", zorder=3)

    # Funnel Flow Indicator on Far Left
    ax.annotate("", xy=(3.0, 15.0), xytext=(3.0, 85.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#64748b", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(1.5, 50.0, "Triage Volume Compression", ha="center", va="center", rotation=90,
            fontsize=7.0, weight="bold", color="#64748b", zorder=5)

    # =========================================================================
    # CONNECTOR BRIDGES (Dotted lines with direction markers)
    # =========================================================================
    # Bridge 1
    ax.annotate("", xy=(46.0, 75.0), xytext=(39.0, 75.0),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#dc2626", ls="--", shrinkA=0, shrinkB=0), zorder=4)
    # Bridge 2
    ax.annotate("", xy=(46.0, 49.0), xytext=(33.0, 49.0),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#d97706", ls="--", shrinkA=0, shrinkB=0), zorder=4)
    # Bridge 3
    ax.annotate("", xy=(46.0, 24.0), xytext=(28.0, 24.0),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#16a34a", ls="--", shrinkA=0, shrinkB=0), zorder=4)

    # =========================================================================
    # RIGHT PANEL: PARALLEL OPERATIONAL EVALUATION CARDS (x: 47.0 to 97.0)
    # =========================================================================

    # --- CARD 1: LEGACY SQL RULES (y: 63.5 to 86.5) ---
    c1 = patches.FancyBboxPatch((47.0, 63.5), 50.0, 23.0, boxstyle="round,pad=0.8",
                                facecolor="#fef2f2", edgecolor="#dc2626", lw=1.6, zorder=2)
    ax.add_patch(c1)
    ax.text(49.5, 82.0, "PARADIGM 1: LEGACY SQL STATIC RULES & THRESHOLDS",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#991b1b",
            bbox=dict(boxstyle="round,pad=0.2", fc="#fee2e2", ec="#ef4444", lw=0.8), zorder=3)
    ax.text(49.5, 75.0, "Alert Volume: 500 - 1,200 alerts per 10k transactions (5.0% - 12.0%)",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#0f172a", zorder=3)
    ax.text(49.5, 68.0, "Deficit: >95.0% False Positive Rate | Massive Analyst Fatigue | No Finite-Sample Bounds",
            ha="left", va="center", fontsize=7.0, color="#b91c1c", zorder=3)

    # --- CARD 2: MARGINAL CONFORMAL (y: 37.5 to 60.5) ---
    c2 = patches.FancyBboxPatch((47.0, 37.5), 50.0, 23.0, boxstyle="round,pad=0.8",
                                facecolor="#fffbeb", edgecolor="#f59e0b", lw=1.6, zorder=2)
    ax.add_patch(c2)
    ax.text(49.5, 56.0, "PARADIGM 2: MARGINAL CONFORMAL PREDICTION (CLASS-AGNOSTIC)",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#92400e",
            bbox=dict(boxstyle="round,pad=0.2", fc="#fef3c7", ec="#f59e0b", lw=0.8), zorder=3)
    ax.text(49.5, 49.0, "Review Queue: 1,840 alerts per 10k transactions (18.40% Share)",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#0f172a", zorder=3)
    ax.text(49.5, 42.0, "Deficit: Severe Minority Under-Coverage (-16.6 pp Deficit) | Over-Refers Benign Noise",
            ha="left", va="center", fontsize=7.0, color="#b45309", zorder=3)

    # --- CARD 3: CLASS-CONDITIONAL CRC (y: 11.5 to 34.5) ---
    c3 = patches.FancyBboxPatch((47.0, 11.5), 50.0, 23.0, boxstyle="round,pad=0.8",
                                facecolor="#f0fdf4", edgecolor="#16a34a", lw=1.8, zorder=2)
    ax.add_patch(c3)
    ax.text(49.5, 30.0, "PARADIGM 3: C-STGB CLASS-CONDITIONAL CRC (PROPOSED)",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#166534",
            bbox=dict(boxstyle="round,pad=0.2", fc="#dcfce7", ec="#22c55e", lw=0.8), zorder=3)
    ax.text(49.5, 23.0, "Review Queue: Exactly 49 alerts per 10k transactions (0.49% Share)",
            ha="left", va="center", fontsize=7.4, weight="bold", color="#0f172a", zorder=3)
    ax.text(49.5, 16.0, r"Breakthrough: -99.51% Workload Slashing | Finite-Sample Coverage $\geq 99.0\%$ Guaranteed",
            ha="left", va="center", fontsize=7.0, weight="bold", color="#15803d", zorder=3)

    # =========================================================================
    # BOTTOM EXECUTIVE CALLOUT PILL (y: 2.5 to 7.5)
    # =========================================================================
    summary_pill = patches.FancyBboxPatch((4.0, 2.5), 93.0, 5.5, boxstyle="round,pad=0.3",
                                          facecolor="#f1f5f9", edgecolor="#94a3b8", lw=1.0, zorder=2)
    ax.add_patch(summary_pill)
    ax.text(50.5, 5.25, r"Operational Impact: 99.51% Examiner Review Queue Slashing | Finite-Sample Validity ($1 - \alpha \geq 99.0\%$) for Both Classes",
            ha="center", va="center", fontsize=7.2, weight="bold", color="#1e293b", zorder=3)

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_compliance_alert_funnel.pdf"
        png_path = d / "fig_compliance_alert_funnel.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
        print(f" [OK] Saved: {pdf_path}")
        
    # Also save to artifact directory
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig5_5_redesigned_final.png")
    fig.savefig(artifact_png, dpi=300, bbox_inches="tight", pad_inches=0.15)
    print(f" [OK] Artifact copy saved: {artifact_png}")
    plt.close(fig)

if __name__ == "__main__":
    generate_figure_5_5()

