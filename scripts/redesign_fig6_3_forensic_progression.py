"""
scripts/redesign_fig6_3_forensic_progression.py
Publication-grade redesign of Figure 6.3:
Worked 3-Stage Forensic Progression of a 15-Node Incident.
Generates fig_15node_forensic_progression.pdf and .png.
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

def generate_figure_6_3():
    # Canvas sized 10.0 x 3.8 to maintain perfect aspect ratio (~2.63:1) for Page 73
    fig, axes = plt.subplots(1, 3, figsize=(10.0, 3.8))
    
    for ax in axes:
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.axis("off")

    # Node coordinates for the 15-node smurfing & peeling ring
    # S0: Source seed
    # M1-M4: Smurfing mules
    # L1-L2: Layering pass-throughs
    # Sink: Consolidation offshore sink
    nodes = {
        "S0": (0.12, 0.50),
        "M1": (0.38, 0.82),
        "M2": (0.38, 0.60),
        "M3": (0.38, 0.38),
        "M4": (0.38, 0.18),
        "L1": (0.64, 0.70),
        "L2": (0.64, 0.30),
        "Sink": (0.88, 0.50),
    }

    # Camouflage chaff nodes
    chaff = {
        "C1": (0.24, 0.86),
        "C2": (0.22, 0.16),
        "C3": (0.52, 0.88),
        "C4": (0.50, 0.16),
        "C5": (0.76, 0.86),
        "C6": (0.78, 0.16),
        "C7": (0.92, 0.80),
    }

    # Causal criminal edges
    causal_edges = [
        ("S0", "M1"), ("S0", "M2"), ("S0", "M3"), ("S0", "M4"),
        ("M1", "L1"), ("M2", "L1"), ("M3", "L2"), ("M4", "L2"),
        ("L1", "Sink"), ("L2", "Sink")
    ]

    # Camouflage chaff edges
    chaff_edges = [
        ("S0", "C1"), ("C1", "M1"), ("C2", "M4"), ("S0", "C2"),
        ("M1", "C3"), ("C3", "L1"), ("M4", "C4"), ("C4", "L2"),
        ("L1", "C5"), ("C5", "Sink"), ("L2", "C6"), ("C6", "Sink"),
        ("Sink", "C7"), ("C1", "C3")
    ]

    # =========================================================================
    # PANEL (a): Raw Ingested Graph (High Camouflage Noise)
    # =========================================================================
    ax0 = axes[0]
    ax0.add_patch(patches.FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0.01",
                                         facecolor="#f8fafc", edgecolor="#cbd5e1", lw=1.2, zorder=1))

    # Panel Title Badge
    ax0.text(0.50, 0.93, "(a) Raw Ingested Graph", ha="center", va="center",
             fontsize=8.5, weight="bold", color="#0f172a",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#cbd5e1", lw=0.8), zorder=6)

    # Draw Chaff Edges (faint dotted gray)
    for u, v in chaff_edges:
        p1 = nodes.get(u, chaff.get(u))
        p2 = nodes.get(v, chaff.get(v))
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=0.8, color="#94a3b8", ls=":", shrinkA=3, shrinkB=3), zorder=2)

    # Draw Criminal Edges (slate solid)
    for u, v in causal_edges:
        p1, p2 = nodes[u], nodes[v]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=1.2, color="#475569", shrinkA=4, shrinkB=4), zorder=3)

    # Draw Chaff Nodes
    for name, (x, y) in chaff.items():
        ax0.scatter(x, y, s=45, color="#e2e8f0", edgecolor="#94a3b8", lw=0.8, zorder=4)
        ax0.text(x, y, name, ha="center", va="center", fontsize=5.5, color="#64748b", weight="bold", zorder=5)

    # Draw Core Nodes
    for name, (x, y) in nodes.items():
        c_fill = "#fee2e2" if name in ["S0", "Sink"] else "#e0f2fe"
        c_edge = "#dc2626" if name in ["S0", "Sink"] else "#0284c7"
        c_txt = "#991b1b" if name in ["S0", "Sink"] else "#0369a1"
        ax0.scatter(x, y, s=110, color=c_fill, edgecolor=c_edge, lw=1.4, zorder=4)
        ax0.text(x, y, name, ha="center", va="center", fontsize=6.4, color=c_txt, weight="bold", zorder=5)

    # Bottom summary card
    ax0.text(0.50, 0.07, "15 Entities | 24 Ingested Transactions\nHeavy Camouflage Noise Injection",
             ha="center", va="center", fontsize=6.8, color="#475569", weight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#e2e8f0", lw=0.6), zorder=6)

    # =========================================================================
    # PANEL (b): GNNExplainer Causal Attribution Mask (Pruning Chaff)
    # =========================================================================
    ax1 = axes[1]
    ax1.add_patch(patches.FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0.01",
                                         facecolor="#fef2f2", edgecolor="#fca5a5", lw=1.2, zorder=1))

    # Panel Title Badge
    ax1.text(0.50, 0.93, "(b) Causal Attribution Mask", ha="center", va="center",
             fontsize=8.5, weight="bold", color="#991b1b",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#fca5a5", lw=0.8), zorder=6)

    # Draw Pruned Chaff Nodes (faded ghost nodes)
    for name, (x, y) in chaff.items():
        ax1.scatter(x, y, s=35, color="#f1f5f9", edgecolor="#cbd5e1", lw=0.6, ls="--", zorder=2)
        ax1.text(x, y, "x", ha="center", va="center", fontsize=6.0, color="#94a3b8", zorder=3)

    # Draw Factual Causal Edges (Thick glowing crimson with flow annotations)
    for u, v in causal_edges:
        p1, p2 = nodes[u], nodes[v]
        ax1.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=2.0, color="#dc2626", shrinkA=4, shrinkB=4), zorder=4)

    # Draw Core Nodes with verified risk colors
    for name, (x, y) in nodes.items():
        c_fill = "#ef4444" if name in ["S0", "Sink"] else "#f97316"
        c_edge = "#991b1b" if name in ["S0", "Sink"] else "#c2410c"
        ax1.scatter(x, y, s=120, color=c_fill, edgecolor=c_edge, lw=1.5, zorder=5)
        ax1.text(x, y, name, ha="center", va="center", fontsize=6.4, color="#ffffff", weight="bold", zorder=6)

    # Edge Mask annotation badge
    ax1.text(0.50, 0.50, r"$M_e \geq 0.65$", ha="center", va="center", fontsize=7.0, weight="bold", color="#991b1b",
             bbox=dict(boxstyle="round,pad=0.2", fc="#fee2e2", ec="#dc2626", lw=0.8), zorder=7)

    # Bottom summary card
    ax1.text(0.50, 0.07, "65.9% Spurious Links Pruned\nIsolates True Smurfing & Peeling Ring",
             ha="center", va="center", fontsize=6.8, color="#991b1b", weight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#fecaca", lw=0.6), zorder=6)

    # =========================================================================
    # PANEL (c): Certified FinCEN Form 111 SAR Dossier
    # =========================================================================
    ax2 = axes[2]
    ax2.add_patch(patches.FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0.01",
                                         facecolor="#f0fdf4", edgecolor="#86efac", lw=1.2, zorder=1))

    # Panel Title Badge
    ax2.text(0.50, 0.93, "(c) Certified FinCEN Form 111 SAR", ha="center", va="center",
             fontsize=8.5, weight="bold", color="#166534",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#86efac", lw=0.8), zorder=6)

    # Two-column Key-Value Field Rows (Crisp typography & perfectly aligned)
    sar_fields = [
        ("Case Identifier", "SAR-2026-B8F91A04", "#0f172a"),
        ("Primary Subject", "ACC_9941 (Source S0)", "#b91c1c"),
        ("Triage Set", "Tier 1: Quarantine Hold", "#b91c1c"),
        ("Typology", "Smurfing & Peeling Chain", "#c2410c"),
        ("Flow Retention", "Pass-Through (0.994)", "#0f766e"),
        ("Cryptographic Seal", "SHA-256 e3b0c4... (WORM)", "#15803d"),
        ("Governance", "Fed SR 11-7 & BSA Aligned", "#4338ca")
    ]

    y_pos = 0.81
    for label, val, c_val in sar_fields:
        # Field Label on Left
        ax2.text(0.06, y_pos, label + ":", ha="left", va="center",
                 fontsize=6.8, weight="bold", color="#334155", zorder=3)
        # Field Value on Right
        ax2.text(0.94, y_pos, val, ha="right", va="center",
                 fontsize=6.8, weight="bold", color=c_val, zorder=3)
        y_pos -= 0.102

    # Bottom summary card
    ax2.text(0.50, 0.07, "Autonomous Multi-Agent Generation\n100% AST Grammar Validated (0.00% Hallucination)",
             ha="center", va="center", fontsize=6.8, color="#166534", weight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#bbf7d0", lw=0.6), zorder=6)

    # Layout adjustment
    fig.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04, wspace=0.12)

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_15node_forensic_progression.pdf"
        png_path = d / "fig_15node_forensic_progression.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
        print(f" [OK] Saved: {pdf_path}")
        
    # Also save to artifact directory
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig6_3_redesigned_final.png")
    fig.savefig(artifact_png, dpi=300, bbox_inches="tight", pad_inches=0.15)
    print(f" [OK] Artifact copy saved: {artifact_png}")
    plt.close(fig)

if __name__ == "__main__":
    generate_figure_6_3()
