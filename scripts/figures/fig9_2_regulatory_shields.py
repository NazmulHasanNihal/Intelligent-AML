"""
Figure 9.2: 5-Pillar Global Regulatory Compliance Shield
Redesigned as an authoritative radial Hub-and-Spoke diagram:
Central C-STGB Framework engine connected to 5 statutory compliance pillars
with concise architectural link phrases, strict palette, and zero grid clutter.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST_LIGHT,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_LIGHT,
    COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE_LIGHT,
    COLOR_RISK, COLOR_RISK_BG, COLOR_RISK_LIGHT,
    COLOR_REVIEW, COLOR_REVIEW_BG, COLOR_REVIEW_LIGHT,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(10.0, 7.0), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Top Header Banner
    ax.add_patch(patches.Rectangle(
        (0.02, 0.925), 0.96, 0.065,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.965, "FIVE-PILLAR GLOBAL REGULATORY COMPLIANCE SHIELD",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.940, "Statutory Alignment of C-STGB Neuro-Symbolic Governance with International Banking Mandates",
            ha="center", va="center", fontsize=7.4, color="#94a3b8")

    # Center Hub Coordinates
    cx, cy = 0.50, 0.47
    r_hub = 0.125
    r_orbit = 0.330
    r_node = 0.102

    # 5 Outer Pillars Configuration
    # Angles: 90 (Top), 18 (Top-Right), 306 (Bottom-Right), 234 (Bottom-Left), 162 (Top-Left)
    pillars = [
        {
            "name": "FATF 40 RECS",
            "sub": "Recommendation 16 (Travel Rule)\nRisk-Based Approach (RBA)",
            "link": "Zero-Leakage AST Audit",
            "angle": 90,
            "color": COLOR_INGEST,
            "bg": COLOR_INGEST_BG,
            "text_color": COLOR_INGEST
        },
        {
            "name": "FinCEN BSA / AMLA",
            "sub": "31 CFR § 1020.320\nAutomated SAR Filing Ready",
            "link": "Automated SAR Dossier",
            "angle": 18,
            "color": COLOR_RISK,
            "bg": COLOR_RISK_BG,
            "text_color": COLOR_RISK
        },
        {
            "name": "BFIU GUIDELINES",
            "sub": "Circular No. 26 (MLPA 2012)\nMobile Financial (MFS) Smurfing",
            "link": "Multi-Rail Invariant Profiling",
            "angle": 306,
            "color": COLOR_REVIEW,
            "bg": COLOR_REVIEW_BG,
            "text_color": COLOR_REVIEW
        },
        {
            "name": "EU AI ACT / 6AMLD",
            "sub": "Title III High-Risk AI Systems\nArticle 14 Human Oversight",
            "link": "Conformal 4-Eyes Governance",
            "angle": 234,
            "color": COLOR_SAFE,
            "bg": COLOR_SAFE_BG,
            "text_color": COLOR_SAFE
        },
        {
            "name": "FED SR 11-7 / OCC",
            "sub": "Model Risk Management (MRM)\nContinuous Non-Stationary Drift",
            "link": "DKW Drift Bounds",
            "angle": 162,
            "color": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "text_color": COLOR_GNN
        }
    ]

    # Draw Connecting Spokes & Link Badges FIRST (so nodes sit on top)
    for p in pillars:
        rad = np.radians(p["angle"])
        nx = cx + r_orbit * np.cos(rad)
        ny = cy + r_orbit * np.sin(rad)
        
        # Line from hub boundary to node boundary
        sx = cx + r_hub * np.cos(rad)
        sy = cy + r_hub * np.sin(rad)
        ex = cx + (r_orbit - r_node) * np.cos(rad)
        ey = cy + (r_orbit - r_node) * np.sin(rad)
        
        # Dual stylized connecting line
        ax.plot([sx, ex], [sy, ey], color=p["color"], lw=2.2, zorder=2)
        
        # Midpoint for phrase badge
        mx = (sx + ex) / 2
        my = (sy + ey) / 2
        
        # Shift text slightly perpendicular to line for readability
        perp_rad = rad + np.pi/2
        offset_d = 0.024
        bx = mx + offset_d * np.cos(perp_rad)
        by = my + offset_d * np.sin(perp_rad)
        
        # Pill badge for linking phrase
        ax.text(bx, by, p["link"],
                ha="center", va="center", fontsize=7.2, fontweight="bold",
                color=COLOR_DARK,
                bbox=dict(boxstyle="square,pad=0.35", facecolor="#ffffff",
                          edgecolor=p["color"], lw=1.2),
                zorder=4)

    # Draw Central Hub
    # Outer ring
    ax.add_patch(patches.Circle(
        (cx, cy), r_hub + 0.008,
        facecolor="none", edgecolor=COLOR_DARK, lw=2.0, zorder=5
    ))
    # Main Circle
    ax.add_patch(patches.Circle(
        (cx, cy), r_hub,
        facecolor=COLOR_DARK, edgecolor="#38bdf8", lw=1.6, zorder=6
    ))
    # Hub Text
    ax.text(cx, cy + 0.045, "C-STGB", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="#ffffff", zorder=7)
    ax.text(cx, cy + 0.015, "FRAMEWORK", ha="center", va="center",
            fontsize=9.0, fontweight="bold", color="#38bdf8", zorder=7)
    ax.plot([cx - 0.065, cx + 0.065], [cy - 0.005, cy - 0.005], color="#94a3b8", lw=0.8, zorder=7)
    ax.text(cx, cy - 0.028, "Neuro-Symbolic Core", ha="center", va="center",
            fontsize=7.4, color="#cbd5e1", zorder=7)
    ax.text(cx, cy - 0.055, "Finite-Sample 99% Safety", ha="center", va="center",
            fontsize=6.8, fontweight="bold", color="#4ade80", zorder=7)

    # Draw 5 Outer Pillar Circles
    for p in pillars:
        rad = np.radians(p["angle"])
        nx = cx + r_orbit * np.cos(rad)
        ny = cy + r_orbit * np.sin(rad)
        
        # Background circle
        ax.add_patch(patches.Circle(
            (nx, ny), r_node,
            facecolor=p["bg"], edgecolor=p["color"], lw=2.0, zorder=5
        ))
        # Inner decorative circle rim
        ax.add_patch(patches.Circle(
            (nx, ny), r_node - 0.008,
            facecolor="none", edgecolor=p["color"], lw=0.7, linestyle="--", zorder=6
        ))
        
        # Pillar Header & Subtitle
        ax.text(nx, ny + 0.035, p["name"], ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=p["text_color"], zorder=7)
        ax.plot([nx - 0.055, nx + 0.055], [ny + 0.015, ny + 0.015], color=p["color"], lw=0.8, zorder=7)
        ax.text(nx, ny - 0.025, p["sub"], ha="center", va="center",
                fontsize=6.6, color=COLOR_DARK, linespacing=1.2, zorder=7)

    # Bottom Reference Callout Banner (Directing to Table 9.1)
    ax.add_patch(patches.Rectangle(
        (0.02, 0.025), 0.96, 0.055,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    ax.text(0.50, 0.052, "Note: Full statutory cross-references, supervisory audit clauses, and mathematical validation proofs are detailed in Table 9.1.",
            ha="center", va="center", fontsize=7.4, style="italic", color=COLOR_MUTED)

    save_figure(fig, "fig_regulatory_shields", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
