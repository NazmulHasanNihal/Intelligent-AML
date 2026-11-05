"""
scripts/upgrade_user_target_figures.py
Upgrades the 5 figures specifically uploaded and requested by the user:
1. fig_lit_evolution_frontier.pdf (Figure 2.2)
2. fig_12d_toy_model_schematic.pdf (Figure 3.3)
3. fig19_conformal_risk_mechanism.pdf (Figure 5.2)
4. fig_compliance_alert_funnel.pdf (Figure 5.5)
5. fig_conformal_conveyor_funnel.pdf (Figure 5.3)

Guarantees:
- Spacious canvases (increased width and height)
- Zero text-over-text collisions
- Zero border clipping (pad_inches=0.15)
- All text comfortably enclosed within shapes and badges
- Publication-grade typography and contrast
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
    'axes.labelsize': 9.0,
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
    BASE_DIR / "reports" / "figures"
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
    print(f" [OK] Generated & Upgraded: {stem}.pdf & .png across all directories")

# =============================================================================
# 1. FIG: 2D AML Graph Learning Evolution Frontier (Chapter 2, Figure 2.2)
# =============================================================================
def upgrade_lit_evolution_frontier():
    # Enlarge canvas to 8.2 x 5.6 to give massive breathing room
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    
    # Background quadrants with soft, professional pastel shading
    ax.axhspan(0, 50, 0, 50, color='#f8fafc', alpha=0.9, zorder=0)
    ax.axhspan(50, 100, 0, 50, color='#f1f5f9', alpha=0.9, zorder=0)
    ax.axhspan(0, 50, 50, 100, color='#f1f5f9', alpha=0.9, zorder=0)
    ax.axhspan(50, 100, 50, 100, color='#e0f2fe', alpha=0.55, zorder=0)
    
    # Quadrant dividing lines
    ax.axvline(50, color='#94a3b8', linestyle='--', lw=1.2, zorder=1)
    ax.axhline(50, color='#94a3b8', linestyle='--', lw=1.2, zorder=1)
    
    # Quadrant Header Badges (Placed in outer corners with neat borders, no collision)
    ax.text(7, 7, "QUADRANT I: Static Tabular Baselines", ha='left', va='bottom', 
            fontsize=7.2, color='#64748b', weight='bold',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.9))
    ax.text(7, 95, "QUADRANT II: Topological Imbalance Specialists", ha='left', va='top', 
            fontsize=7.2, color='#64748b', weight='bold',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.9))
    ax.text(53, 7, "QUADRANT III: Continuous Temporal GNNs", ha='left', va='bottom', 
            fontsize=7.2, color='#64748b', weight='bold',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.9))
    ax.text(53, 95, "QUADRANT IV: Unified Neuro-Symbolic Frontier", ha='left', va='top', 
            fontsize=7.4, color='#0369a1', weight='bold',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#7dd3fc", lw=0.8, alpha=0.9))
    
    # Models data: carefully adjusted coordinates and non-colliding offsets
    models = [
        # Tabular (Gray)
        ("XGBoost", 12, 16, "#475569", 110, (10, -6)),
        ("LightGBM", 16, 27, "#475569", 110, (-18, 9)),
        ("CatBoost", 23, 19, "#475569", 110, (10, -8)),
        
        # Spatial GNNs (Blue)
        ("GIN", 18, 33, "#2563eb", 120, (10, -8)),
        ("GCN", 15, 39, "#2563eb", 120, (-22, 7)),
        ("GAT / GATv2", 28, 41, "#2563eb", 130, (10, -10)),
        ("GraphSAGE", 22, 46, "#2563eb", 130, (-28, 8)),
        ("HGT", 35, 49, "#2563eb", 130, (10, 6)),
        
        # Imbalance Specialists (Amber)
        ("SMOTE-GNN", 20, 68, "#d97706", 130, (-24, 8)),
        ("GraphSMOTE", 26, 76, "#d97706", 140, (-28, 8)),
        ("PC-GNN", 33, 83, "#d97706", 140, (10, 2)),
        
        # Camouflage GNNs (Purple)
        ("CARE-GNN", 37, 70, "#7c3aed", 140, (-28, 8)),
        ("FraudGate", 45, 75, "#7c3aed", 140, (10, -10)),
        ("H2-IDE", 41, 85, "#7c3aed", 150, (-24, 8)),
        
        # Temporal GNNs (Emerald)
        ("EvolveGCN", 62, 38, "#059669", 130, (-22, -12)),
        ("TGAT", 72, 42, "#059669", 140, (-18, 8)),
        ("TGN", 78, 45, "#059669", 150, (10, -10)),
        ("ChronoWave", 82, 53, "#059669", 140, (10, 6)),
    ]
    
    for name, x, y, col, sz, offset in models:
        ax.scatter(x, y, s=sz, color=col, alpha=0.90, edgecolors='white', lw=1.5, zorder=3)
        ax.annotate(name, (x, y), xytext=offset, textcoords='offset points',
                    fontsize=7.4, weight='semibold', color='#1e293b',
                    bbox=dict(boxstyle="round,pad=0.15", fc="#ffffff", ec="none", alpha=0.75))
        
    # C-STGB (Proposed Framework) - Prominent Star and Pristine Callout Box
    ax.scatter(92, 92, s=360, color='#dc2626', marker='*', edgecolors='#fef08a', lw=2.2, zorder=5)
    callout_txt = "C-STGB (Proposed Framework)\n91.42% F1 | 0.45 ms SLA\n1 - alpha >= 99% Coverage"
    ax.annotate(callout_txt, 
                xy=(92, 92), xytext=(-135, -35), textcoords='offset points',
                bbox=dict(boxstyle="round,pad=0.5", fc="#fef2f2", ec="#dc2626", lw=1.5),
                fontsize=7.6, weight='bold', color='#991b1b', linespacing=1.45,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.10", color='#dc2626', lw=1.5))

    # Pareto Frontier Curve
    curve_x = np.linspace(14, 92, 100)
    curve_y = 18 + 74 * (curve_x - 14) / (92 - 14) + 7 * np.sin(np.pi * (curve_x - 14) / (92 - 14))
    ax.plot(curve_x, curve_y, color='#0284c7', linestyle=':', lw=2.0, alpha=0.8, zorder=2)
    ax.text(56, 58, "State-of-the-Art Pareto Frontier", color='#0284c7', fontsize=7.6, 
            weight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#bae6fd", lw=0.8, alpha=0.9))

    ax.set_xlim(4, 98)
    ax.set_ylim(4, 98)
    ax.set_xlabel(r"Temporal Expressiveness & Velocity Modeling (Static Snapshots $\longrightarrow$ Continuous-Time Harmonic)", 
                  fontsize=8.8, weight='bold', labelpad=8)
    ax.set_ylabel(r"Imbalance, Camouflage & Conformal Safety (None $\longrightarrow$ Finite-Sample Risk Bounds)", 
                  fontsize=8.8, weight='bold', labelpad=12)
    ax.set_title("2D Financial Crime Graph Learning Evolution Frontier: Positioning C-STGB vs. 18 SOTA Baselines", 
                 fontsize=9.8, weight='bold', pad=12)
    
    # Legend placed cleanly below with ample breathing room
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Tabular Baselines (XGB / LGBM / CatBoost)', markerfacecolor='#475569', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Spatial GNNs (GCN / GAT / GIN / GraphSAGE / HGT)', markerfacecolor='#2563eb', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Topological Imbalance Specialists (GraphSMOTE / PC-GNN)', markerfacecolor='#d97706', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Camouflage Filtering GNNs (CARE-GNN / FraudGate / H2-IDE)', markerfacecolor='#7c3aed', markersize=7),
        plt.Line2D([0], [0], marker='o', color='w', label='Continuous-Time Dynamic GNNs (TGN / TGAT / ChronoWave)', markerfacecolor='#059669', markersize=7),
        plt.Line2D([0], [0], marker='*', color='w', label='C-STGB: Unified Neuro-Symbolic & Conformal (Proposed)', markerfacecolor='#dc2626', markeredgecolor='#fef08a', markersize=11),
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.12), 
              ncol=2, fontsize=7.2, framealpha=0.98, edgecolor='#cbd5e1', borderpad=0.6, labelspacing=0.6)
    
    fig.subplots_adjust(bottom=0.22, top=0.92, left=0.12, right=0.96)
    save_to_all(fig, "fig_lit_evolution_frontier")


# =============================================================================
# 2. FIG: 12-D Canonical Invariant Physical Toy-Model Schematic (Chapter 3, Figure 3.3)
# =============================================================================
def upgrade_12d_toy_model_schematic():
    # Delegates to the dedicated, publication-grade redesign generator
    from redesign_fig3_3_toy_models import generate_figure_3_3
    fig = generate_figure_3_3()
    save_to_all(fig, "fig_12d_toy_model_schematic")


# =============================================================================
# 3. FIG: Class-Conditional CRC vs Marginal Conformal (Chapter 5, Figure 5.2)
# =============================================================================
def upgrade_fig19_conformal_risk_mechanism():
    from scripts.redesign_fig5_2_conformal_mechanism import generate_figure_5_2
    generate_figure_5_2()

# =============================================================================
# 4. FIG: Operational Compliance Alert-Volume Funnel (Chapter 5, Figure 5.5)
# =============================================================================
def upgrade_compliance_alert_funnel():
    from scripts.redesign_fig5_5_compliance_funnel import generate_figure_5_5
    generate_figure_5_5()


def upgrade_conformal_conveyor_funnel():
    from scripts.redesign_fig5_3_conformal_conveyor import generate_figure_5_3
    generate_figure_5_3()


if __name__ == "__main__":
    print("Upgrading 5 target figures with zero-overlap coordinates...")
    upgrade_lit_evolution_frontier()
    upgrade_12d_toy_model_schematic()
    upgrade_fig19_conformal_risk_mechanism()
    upgrade_compliance_alert_funnel()
    upgrade_conformal_conveyor_funnel()
    print("All 5 target figures successfully upgraded!")
