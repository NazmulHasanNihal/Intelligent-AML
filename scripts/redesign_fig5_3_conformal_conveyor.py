"""
scripts/redesign_fig5_3_conformal_conveyor.py
Publication-grade redesign of Figure 5.3:
3-Tier Conformal Risk Control Triage Conveyor Funnel.
Generates fig_conformal_conveyor_funnel.pdf and .png.
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

def generate_figure_5_3():
    # Enlarge canvas to 10.2 x 5.8 for clean, spacious architecture
    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    ax.axis('off')
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Background canvas
    bg = patches.Rectangle((0, 0), 100, 100, facecolor='#ffffff', edgecolor='none', zorder=0)
    ax.add_patch(bg)

    # =========================================================================
    # MASTER HEADER (Two-line executive styling)
    # =========================================================================
    ax.text(50.0, 96.5, "3-Tier Conformal Risk Control (CRC) Triage Conveyor Funnel",
            ha='center', va='center', fontsize=10.5, weight='bold', color='#0f172a')
    ax.text(50.0, 93.0, r"Finite-Sample Statistical Guarantees ($1 - \alpha \geq 99.0\%$) with -99.51% Human Compliance Queue Slashing",
            ha='center', va='center', fontsize=7.8, style='italic', color='#475569')

    # =========================================================================
    # STAGE 1: STREAMING INGESTION FUNNEL (x: 1.5 to 21.0)
    # =========================================================================
    funnel_pts = [[1.5, 89.0], [21.0, 69.0], [21.0, 31.0], [1.5, 11.0]]
    funnel = patches.Polygon(funnel_pts, closed=True, facecolor='#f8fafc', edgecolor='#64748b', lw=1.6, zorder=2)
    ax.add_patch(funnel)

    # Ingestion badges and details (comfortable margin clearance)
    ax.text(11.0, 72.0, "STAGE 1", ha='center', va='center', fontsize=7.0, weight='bold', color='#64748b',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#cbd5e1", lw=0.8), zorder=3)
    ax.text(11.0, 63.0, "100% Streaming\nTransactions", ha='center', va='center', fontsize=8.2, weight='bold', color='#0f172a', zorder=3)
    ax.text(11.0, 52.0, "N = 10,000 Wires\nMT103 / UTXO Ingress", ha='center', va='center', fontsize=7.2, color='#334155', zorder=3)
    ax.text(11.0, 41.0, "12-D Canonical\nPhysical Invariants", ha='center', va='center', fontsize=7.0, style='italic', color='#64748b', zorder=3)
    ax.text(11.0, 26.0, "Zero-Copy Arrow ABI\nEmbedded DuckDB", ha='center', va='center', fontsize=6.5, weight='bold', color='#0284c7', zorder=3)

    # Arrow from Stage 1 to Stage 2
    ax.annotate("", xy=(23.5, 50.0), xytext=(21.0, 50.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#2563eb", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(22.25, 46.5, r"Raw $\mathbf{x}_u$", ha='center', va='top', fontsize=6.6, weight='bold', color='#1d4ed8', zorder=5)

    # =========================================================================
    # STAGE 2: C-STGB NEURAL RISK CORE (x: 23.5 to 43.5, y: 32.0 to 68.0)
    # =========================================================================
    core_card = patches.FancyBboxPatch((23.5, 32.0), 20.0, 36.0, boxstyle="round,pad=1.0",
                                       facecolor='#eff6ff', edgecolor='#2563eb', lw=1.8, zorder=2)
    ax.add_patch(core_card)

    ax.text(33.5, 63.5, "STAGE 2: NEURAL CORE", ha='center', va='center', fontsize=7.2, weight='bold', color='#1e40af',
            bbox=dict(boxstyle="round,pad=0.22", fc="#dbeafe", ec="#3b82f6", lw=0.8), zorder=3)
    ax.text(33.5, 55.5, "C-STGB Graph Engine", ha='center', va='center', fontsize=8.6, weight='bold', color='#1e3a8a', zorder=3)
    ax.text(33.5, 48.0, "Continuous Harmonic Time\nEdge-Trust Camouflage Gating", ha='center', va='center', fontsize=7.0, color='#1e40af', zorder=3)
    ax.text(33.5, 40.5, r"Risk Output: $\hat{p}_u \in [0, 1]$" + "\n" + r"Score: $s_i^{(y)} = 1 - \hat{p}_i(y)$",
            ha='center', va='center', fontsize=7.4, weight='bold', color='#0f172a', zorder=3)
    ax.text(33.5, 33.0, "Fast-Path Latency: < 0.45 ms", ha='center', va='center', fontsize=6.8, weight='bold', color='#059669', zorder=3)

    # Arrow from Stage 2 to Stage 3
    ax.annotate("", xy=(48.5, 50.0), xytext=(44.5, 50.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#d97706", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(46.5, 53.0, r"Scores $s_u$", ha='center', va='bottom', fontsize=6.6, weight='bold', color='#b45309', zorder=5)

    # =========================================================================
    # STAGE 3: CLASS-CONDITIONAL CRC GATE (x: 48.5 to 68.5, y: 30.0 to 70.0)
    # =========================================================================
    gate_card = patches.FancyBboxPatch((48.5, 30.0), 20.0, 40.0, boxstyle="round,pad=1.0",
                                       facecolor='#fffbeb', edgecolor='#d97706', lw=1.8, zorder=2)
    ax.add_patch(gate_card)

    ax.text(58.5, 65.5, "STAGE 3: CONFORMAL GATE", ha='center', va='center', fontsize=7.2, weight='bold', color='#92400e',
            bbox=dict(boxstyle="round,pad=0.22", fc="#fef3c7", ec="#f59e0b", lw=0.8), zorder=3)
    ax.text(58.5, 58.0, "Class-Conditional CRC", ha='center', va='center', fontsize=8.6, weight='bold', color='#78350f', zorder=3)
    ax.text(58.5, 51.0, r"$\Gamma(u) = \{y \mid 1 - \hat{p}_u(y) \leq \hat{q}^{(y)}\}$",
            ha='center', va='center', fontsize=7.6, weight='bold', color='#92400e', zorder=3)
    ax.text(58.5, 43.5, r"Dual Quantiles ($1 - \alpha = 99\%$):" + "\n" + r"$\hat{q}^{(0)} = 0.52$ | $\hat{q}^{(1)} = 0.94$",
            ha='center', va='center', fontsize=7.2, weight='bold', color='#0f172a', zorder=3)
    ax.text(58.5, 34.0, "Finite-Sample Validity:\n" + r"$\mathbb{P}(Y \in \Gamma \mid Y=y) \geq 99.0\%$",
            ha='center', va='center', fontsize=6.8, weight='bold', color='#15803d', zorder=3)

    # =========================================================================
    # STAGE 4: THREE DESTINATION TIERS (x: 74.0 to 98.0)
    # =========================================================================

    # --- TIER 1: QUARANTINE HOLD (Top Red Card) ---
    ax.annotate("", xy=(74.0, 77.0), xytext=(69.5, 55.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#dc2626",
                                connectionstyle="arc3,rad=-0.15", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(71.5, 78.5, r"$\Gamma=\{1\}$", ha='center', va='bottom', fontsize=6.8, weight='bold', color='#dc2626', zorder=5)

    t1_card = patches.FancyBboxPatch((74.0, 66.0), 24.0, 22.0, boxstyle="round,pad=0.8",
                                     facecolor='#fef2f2', edgecolor='#dc2626', lw=1.8, zorder=2)
    ax.add_patch(t1_card)
    ax.text(86.0, 84.5, "TIER 1: HIGH-RISK QUARANTINE", ha='center', va='center', fontsize=7.4, weight='bold', color='#991b1b',
            bbox=dict(boxstyle="round,pad=0.2", fc="#fee2e2", ec="#ef4444", lw=0.8), zorder=3)
    ax.text(86.0, 78.5, r"Decisive Illicit: $\mathbf{\Gamma(u) = \{1\}}$", ha='center', va='center', fontsize=8.0, weight='bold', color='#b91c1c', zorder=3)
    ax.text(86.0, 73.0, "Volume: 18 / 10,000 tx (0.18%)", ha='center', va='center', fontsize=7.2, weight='bold', color='#7f1d1d', zorder=3)
    ax.text(86.0, 68.0, "Immediate Wire Freeze | Auto-SAR Dossier\nVerified Precision > 99.4%",
            ha='center', va='center', fontsize=6.8, color='#991b1b', zorder=3)

    # --- TIER 2: COMPLIANCE DESK REVIEW (Center Amber Card) ---
    ax.annotate("", xy=(74.0, 50.0), xytext=(69.5, 50.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#ea580c", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(71.5, 52.5, r"$\Gamma=\{0, 1\}$", ha='center', va='bottom', fontsize=6.8, weight='bold', color='#ea580c', zorder=5)

    t2_card = patches.FancyBboxPatch((74.0, 39.0), 24.0, 22.0, boxstyle="round,pad=0.8",
                                     facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.8, zorder=2)
    ax.add_patch(t2_card)
    ax.text(86.0, 57.5, "TIER 2: SELECTIVE ABSTENTION", ha='center', va='center', fontsize=7.4, weight='bold', color='#92400e',
            bbox=dict(boxstyle="round,pad=0.2", fc="#fef3c7", ec="#f59e0b", lw=0.8), zorder=3)
    ax.text(86.0, 51.5, r"Ambiguous Queue: $\mathbf{\Gamma(u) = \{0, 1\}}$", ha='center', va='center', fontsize=8.0, weight='bold', color='#b45309', zorder=3)
    ax.text(86.0, 46.0, "Volume: 49 / 10,000 tx (0.49%)", ha='center', va='center', fontsize=7.2, weight='bold', color='#78350f', zorder=3)
    ax.text(86.0, 41.0, "-99.51% Human Review Queue Slashing\nSenior 4-Eyes Compliance Investigation",
            ha='center', va='center', fontsize=6.8, weight='bold', color='#b45309', zorder=3)

    # --- TIER 3: STRAIGHT-THROUGH CLEARANCE (Bottom Green Card) ---
    ax.annotate("", xy=(74.0, 23.0), xytext=(69.5, 45.0),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#16a34a",
                                connectionstyle="arc3,rad=0.15", shrinkA=0, shrinkB=0), zorder=4)
    ax.text(71.5, 24.5, r"$\Gamma=\{0\}$", ha='center', va='bottom', fontsize=6.8, weight='bold', color='#16a34a', zorder=5)

    t3_card = patches.FancyBboxPatch((74.0, 12.0), 24.0, 22.0, boxstyle="round,pad=0.8",
                                     facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.8, zorder=2)
    ax.add_patch(t3_card)
    ax.text(86.0, 30.5, "TIER 3: AUTOMATED CLEARANCE (STP)", ha='center', va='center', fontsize=7.4, weight='bold', color='#166534',
            bbox=dict(boxstyle="round,pad=0.2", fc="#dcfce7", ec="#22c55e", lw=0.8), zorder=3)
    ax.text(86.0, 24.5, r"Decisive Benign: $\mathbf{\Gamma(u) = \{0\}}$", ha='center', va='center', fontsize=8.0, weight='bold', color='#15803d', zorder=3)
    ax.text(86.0, 19.0, "Volume: 9,933 / 10,000 tx (99.33%)", ha='center', va='center', fontsize=7.2, weight='bold', color='#14532d', zorder=3)
    ax.text(86.0, 14.0, "0.45 ms Real-Time Straight-Through Release\nFinite-Sample Guaranteed Recall >= 99.0%",
            ha='center', va='center', fontsize=6.8, color='#166534', zorder=3)

    # =========================================================================
    # STAGE 5: BOTTOM ARCHITECTURAL SUMMARY BANNER (x: 2.5 to 98.0, y: 2.0 to 8.5)
    # =========================================================================
    summary_card = patches.FancyBboxPatch((2.5, 2.0), 95.5, 6.8, boxstyle="round,pad=0.4",
                                          facecolor='#f1f5f9', edgecolor='#94a3b8', lw=1.0, zorder=2)
    ax.add_patch(summary_card)

    ax.text(18.0, 5.4, "[Pillar 1: Bounded Risk]\n" + r"$\mathbb{P}(Y \in \Gamma(X) \mid Y = y) \geq 99.0\%$",
            ha='center', va='center', fontsize=6.8, weight='bold', color='#1e293b', zorder=3)
    ax.text(50.0, 5.4, "[Pillar 2: Triage Completeness]\n" + r"Zero Empty Sets ($|\Gamma(u)| \geq 1$) | Zero Hangs",
            ha='center', va='center', fontsize=6.8, weight='bold', color='#1e293b', zorder=3)
    ax.text(82.0, 5.4, "[Pillar 3: High-Throughput Clearing]\n" + r"99.33% at < 0.45 ms STP | Leakage $\leq 0.12\%$",
            ha='center', va='center', fontsize=6.8, weight='bold', color='#1e293b', zorder=3)

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_conformal_conveyor_funnel.pdf"
        png_path = d / "fig_conformal_conveyor_funnel.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
        print(f" [OK] Saved: {pdf_path}")
        
    # Also save to artifact directory
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig5_3_redesigned_final.png")
    fig.savefig(artifact_png, dpi=300, bbox_inches="tight", pad_inches=0.15)
    print(f" [OK] Artifact copy saved: {artifact_png}")
    plt.close(fig)

if __name__ == "__main__":
    generate_figure_5_3()
