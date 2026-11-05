"""
scripts/redesign_fig2_2_evolution_frontier.py
Completely redesigns Figure 2.2: 2D Financial Crime Graph Learning Evolution Frontier
Positioning C-STGB against 18 SOTA Baselines with Pristine Detailing and Zero Collisions.
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
    'axes.titlesize': 9.5,
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
    BASE_DIR / "data" / "outputs" / "figures",
]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_to_all(fig, stem):
    for d in TARGET_DIRS:
        pdf_path = d / f"{stem}.pdf"
        png_path = d / f"{stem}.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f" [OK] Generated & Saved: {stem}.pdf & .png across all target directories")


def generate_neat_fig2_2():
    # Canvas dimensions: 9.8 x 6.6 inches (ample breathing room)
    fig, ax = plt.subplots(figsize=(9.8, 6.6))
    
    # Range: X in [0, 100], Y in [0, 100]
    ax.set_xlim(2, 100)
    ax.set_ylim(2, 100)

    # -------------------------------------------------------------------------
    # 1. QUADRANT BACKGROUNDS (Soft Corporate FinTech Tints)
    # -------------------------------------------------------------------------
    # Quadrant I: Bottom-Left (Tabular Foundations)
    ax.add_patch(patches.Rectangle((2, 2), 48, 48, facecolor="#f8fafc", edgecolor="none", zorder=0))
    # Quadrant II: Top-Left (Topological & Camouflage Specialists)
    ax.add_patch(patches.Rectangle((2, 50), 48, 48, facecolor="#faf5ff", edgecolor="none", zorder=0))
    # Quadrant III: Bottom-Right (Continuous Temporal GNNs)
    ax.add_patch(patches.Rectangle((50, 2), 48, 48, facecolor="#f0fdf4", edgecolor="none", zorder=0))
    # Quadrant IV: Top-Right (Unified Frontier - C-STGB)
    ax.add_patch(patches.Rectangle((50, 50), 48, 48, facecolor="#eff6ff", edgecolor="none", zorder=0))

    # Grid dividing lines
    ax.axvline(50, color="#94a3b8", linestyle="--", lw=1.2, zorder=1)
    ax.axhline(50, color="#94a3b8", linestyle="--", lw=1.2, zorder=1)
    
    # Subtle inner quadrant frame borders
    for (x, y, w, h, col) in [
        (3, 3, 46, 46, "#cbd5e1"),
        (3, 51, 46, 46, "#e9d5ff"),
        (51, 3, 46, 46, "#bbf7d0"),
        (51, 51, 46, 46, "#bfdbfe"),
    ]:
        ax.add_patch(patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
            fill=False, edgecolor=col, lw=1.0, linestyle=":", zorder=1
        ))

    # -------------------------------------------------------------------------
    # 2. QUADRANT CORNER HEADER BADGES (ZERO COLLISION WITH NODES)
    # -------------------------------------------------------------------------
    # Quad I Header (Bottom-Left Corner: empty space y in [4, 11])
    ax.text(5.0, 9.5, "QUADRANT I: Static Tabular Baselines", fontsize=7.2, fontweight="bold", color="#475569",
            bbox=dict(boxstyle="round,pad=0.22", fc="#ffffff", ec="#cbd5e1", lw=0.9), zorder=4)
    ax.text(5.0, 6.2, "Bottleneck: Graph-Blind | No Temporal Velocity Modeling", fontsize=5.8, color="#64748b", style="italic", zorder=4)

    # Quad II Header (Top-Left Corner: empty space y in [92, 98])
    ax.text(5.0, 96.5, "QUADRANT II: Topological & Camouflage Specialists", fontsize=7.2, fontweight="bold", color="#5b21b6",
            bbox=dict(boxstyle="round,pad=0.22", fc="#ffffff", ec="#c4b5fd", lw=0.9), zorder=4)
    ax.text(5.0, 93.2, "Bottleneck: Static Graph Snapshots | Long-Dwell Hibernation Blindness", fontsize=5.8, color="#6d28d9", style="italic", zorder=4)

    # Quad III Header (Bottom-Right Corner: empty space y in [4, 11])
    ax.text(53.0, 9.5, "QUADRANT III: Continuous-Time Dynamic GNNs", fontsize=7.2, fontweight="bold", color="#065f46",
            bbox=dict(boxstyle="round,pad=0.22", fc="#ffffff", ec="#86efac", lw=0.9), zorder=4)
    ax.text(53.0, 6.2, "Bottleneck: Over-Smoothing under Camouflage | No Conformal Bounds", fontsize=5.8, color="#047857", style="italic", zorder=4)

    # Quad IV Header (Top-Right: empty space y in [92, 98])
    ax.text(52.5, 96.5, "QUADRANT IV: Unified Neuro-Symbolic & Statistical Safety Frontier", fontsize=7.4, fontweight="bold", color="#1e40af",
            bbox=dict(boxstyle="round,pad=0.25", fc="#eff6ff", ec="#3b82f6", lw=1.2), zorder=4)
    ax.text(52.5, 93.2, "Breakthrough: Harmonic Attention + Edge-Trust Gating + Conformal CRC", fontsize=6.0, fontweight="bold", color="#2563eb", zorder=4)

    # -------------------------------------------------------------------------
    # 3. PRIOR STATE-OF-THE-ART TRADE-OFF FRONTIER VS BREAKTHROUGH
    # -------------------------------------------------------------------------
    # Prior Trade-off Frontier curve connecting best prior specialized models
    # From H2-IDE (43, 86) -> FraudGate (46, 75) -> ChronoWave (84, 54)
    fx = np.array([43, 46, 58, 70, 84])
    fy = np.array([86, 75, 66, 58, 54])
    p_fit = np.polyfit(fx, fy, 2)
    fx_dense = np.linspace(40, 86, 100)
    fy_dense = np.polyval(p_fit, fx_dense)
    ax.plot(fx_dense, fy_dense, color="#ef4444", linestyle="--", lw=1.8, alpha=0.85, zorder=2)
    
    # Prior Trade-off Label Badge
    ax.text(56, 68, "Prior SOTA Trade-Off Frontier\n(Temporal vs Camouflage Dilemma)",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color="#b91c1c",
            bbox=dict(boxstyle="round,pad=0.25", fc="#fef2f2", ec="#f87171", lw=0.9, alpha=0.95), zorder=5)

    # Breakthrough Pareto Leap Arrow from Prior Frontier to C-STGB Card
    ax.annotate("", xy=(74, 75.2), xytext=(74, 58.5),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#2563eb", linestyle="-"), zorder=9)
    ax.text(74, 66.5, "Breakthrough Pareto Leap\n(Simultaneous Frontier)",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color="#1d4ed8",
            bbox=dict(boxstyle="round,pad=0.22", fc="#eff6ff", ec="#60a5fa", lw=0.9, alpha=0.95), zorder=10)

    # -------------------------------------------------------------------------
    # 4. 18 SOTA BASELINE NODES & CAREFULLY PADDED ANNOTATIONS
    # -------------------------------------------------------------------------
    baselines = [
        # --- Quadrant I: Tabular Baselines ---
        ("XGBoost", 14.0, 16.0, "#475569", 110, (12, -4), "68.4% F1", "left"),
        ("LightGBM", 18.0, 26.5, "#475569", 110, (-14, 6), "69.1% F1", "right"),
        ("CatBoost", 26.0, 18.5, "#475569", 110, (12, -4), "70.2% F1", "left"),

        # --- Quadrant I / II: Static Spatial GNNs ---
        ("GIN", 19.0, 34.0, "#2563eb", 120, (12, -4), "72.8% F1", "left"),
        ("GCN", 14.5, 40.0, "#2563eb", 120, (-14, 6), "73.1% F1", "right"),
        ("GraphSAGE", 23.0, 46.5, "#2563eb", 125, (-14, 6), "78.4% F1", "right"),
        ("GAT / GATv2", 30.0, 41.5, "#2563eb", 125, (12, -6), "76.4% F1", "left"),
        ("HGT", 37.0, 48.5, "#2563eb", 130, (12, 4), "79.2% F1", "left"),

        # --- Quadrant II: Imbalance Specialists ---
        ("SMOTE-GNN", 20.5, 68.0, "#d97706", 135, (-14, 6), "77.9% F1", "right"),
        ("GraphSMOTE", 27.0, 76.5, "#d97706", 140, (-14, 6), "81.6% F1", "right"),
        ("PC-GNN", 33.5, 83.0, "#d97706", 140, (-14, 6), "82.8% F1", "right"),

        # --- Quadrant II: Adversarial Camouflage Filtering ---
        ("CARE-GNN", 36.5, 69.5, "#7c3aed", 145, (-14, 6), "80.5% F1", "right"),
        ("FraudGate", 46.5, 75.0, "#7c3aed", 150, (12, -4), "84.1% F1", "left"),
        ("H2-IDE", 43.0, 86.0, "#7c3aed", 150, (12, 6), "84.1% F1", "left"),

        # --- Quadrant III: Continuous-Time Dynamic GNNs ---
        ("EvolveGCN", 62.0, 36.0, "#059669", 135, (-14, -6), "79.5% F1", "right"),
        ("TGAT", 71.0, 41.0, "#059669", 140, (12, -4), "81.0% F1", "left"),
        ("TGN", 78.0, 45.0, "#059669", 150, (12, 4), "81.3% F1", "left"),
        ("ChronoWave", 84.0, 54.0, "#059669", 150, (12, 4), "83.9% F1", "left"),
    ]

    for name, bx, by, col, sz, offset, f1_txt, align in baselines:
        # Subtle drop shadow & node marker
        ax.scatter(bx, by, s=sz+35, color="#000000", alpha=0.08, zorder=3)
        ax.scatter(bx, by, s=sz, color=col, edgecolors="#ffffff", lw=1.6, zorder=4)
        
        # Two-line tag: Name + F1
        lbl_text = f"{name}\n({f1_txt})"
        ax.annotate(lbl_text, (bx, by), xytext=offset, textcoords="offset points",
                    ha=align, va="center", fontsize=6.2, fontweight="bold", color="#1e293b",
                    bbox=dict(boxstyle="round,pad=0.20", fc="#ffffff", ec="#cbd5e1", lw=0.6, alpha=0.92),
                    linespacing=1.2, zorder=5)

    # -------------------------------------------------------------------------
    # 5. C-STGB SUMMIT PINNACLE (Proposed Framework in Quadrant IV)
    # -------------------------------------------------------------------------
    ax.scatter(92.5, 91.5, s=620, color="#fef08a", alpha=0.6, zorder=6)
    ax.scatter(92.5, 91.5, s=420, color="#dc2626", marker="*", edgecolors="#fef08a", lw=2.2, zorder=7)

    # C-STGB Performance Card (Top-Right Pinnacle)
    card_x, card_y = 64.0, 75.5
    ax.add_patch(patches.FancyBboxPatch(
        (card_x, card_y), 24.5, 12.8,
        boxstyle="round,pad=0.3,rounding_size=1.0",
        facecolor="#fef2f2", edgecolor="#dc2626", lw=1.6, zorder=8
    ))
    ax.text(card_x + 12.25, card_y + 10.2, "C-STGB (Proposed Framework)",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color="#991b1b", zorder=9)
    ax.text(card_x + 12.25, card_y + 7.2, "91.42% Macro F1  |  +7.32 pp vs SOTA",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color="#dc2626", zorder=9)
    ax.text(card_x + 12.25, card_y + 4.3, "0.45 ms Real-Time SLA  |  31.2k tx/s",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#b91c1c", zorder=9)
    ax.text(card_x + 12.25, card_y + 1.8, r"$1-\alpha \geq 99.0\%$ Finite-Sample Coverage",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#059669", zorder=9)
    
    # Leader arrow from card to star
    ax.annotate("", xy=(91.5, 90.5), xytext=(card_x + 24.5, card_y + 6.4),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#dc2626", connectionstyle="arc3,rad=-0.10"), zorder=9)

    # -------------------------------------------------------------------------
    # 6. AXIS LABELS AND TITLE
    # -------------------------------------------------------------------------
    ax.set_xlabel(r"$\longleftarrow$ Static Snapshots | CONTINUOUS-TIME HARMONIC VELOCITY $\longrightarrow$" + "\n" +
                  r"(Temporal Expressiveness, Tri-Band Decay $\tau_k \in \{2.4\mathrm{h}, 24\mathrm{h}, 168\mathrm{h}\}$, & Burst Intensity)",
                  fontsize=8.2, fontweight="bold", color="#0f172a", labelpad=8)
    ax.set_ylabel(r"$\longleftarrow$ Heuristic / Uncalibrated | TOPOLOGICAL DENOISING & STATISTICAL SAFETY $\longrightarrow$" + "\n" +
                  r"(Edge-Trust Camouflage Pruning $\hat{g}_{ij} \geq 0.10$, Invariant Fusion, & Conformal CRC Bounds)",
                  fontsize=8.2, fontweight="bold", color="#0f172a", labelpad=10)

    # Master Top Title Banner
    ax.set_title("2D Financial Crime Graph Learning Evolution Frontier: Positioning C-STGB vs. 18 SOTA Baselines",
                 fontsize=9.4, fontweight="bold", color="#0f172a", pad=12)

    # -------------------------------------------------------------------------
    # 7. UNIFIED MODEL FAMILY LEGEND BELOW PLOT
    # -------------------------------------------------------------------------
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Tabular Baselines (XGB / LGBM / CatBoost)', markerfacecolor='#475569', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Spatial GNNs (GCN / GATv2 / GraphSAGE / HGT)', markerfacecolor='#2563eb', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Topological Imbalance (SMOTE-GNN / PC-GNN)', markerfacecolor='#d97706', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Camouflage Filtering (CARE-GNN / FraudGate / H2-IDE)', markerfacecolor='#7c3aed', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Continuous-Time Dynamic GNNs (TGN / TGAT / ChronoWave)', markerfacecolor='#059669', markersize=7),
        plt.Line2D([0], [0], marker='*', color='w', label='C-STGB: Unified Neuro-Symbolic Frontier (Proposed)', markerfacecolor='#dc2626', markeredgecolor='#fef08a', markersize=11),
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.12),
              ncol=3, fontsize=6.8, framealpha=0.98, edgecolor='#cbd5e1', borderpad=0.5, labelspacing=0.5)

    fig.subplots_adjust(left=0.10, right=0.96, top=0.91, bottom=0.20)
    save_to_all(fig, "fig_lit_evolution_frontier")


if __name__ == "__main__":
    print("Generating redesigned Figure 2.2: 2D AML Evolution Frontier...")
    generate_neat_fig2_2()
    print("Done!")
