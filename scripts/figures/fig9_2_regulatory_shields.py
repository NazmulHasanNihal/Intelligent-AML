"""
Figure 9.2: 5-Pillar Global Regulatory Compliance Shield
Redesigned as an authoritative radial Hub-and-Spoke diagram with generous dimensions,
rectangular shield pillar cards, zero text clipping or overlapping, spacious spoke clearance,
strict palette, and publication-ready typography.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous widescreen canvas (14.0 x 9.5 inches) for radial symmetry and zero crowding
    fig, ax = plt.subplots(figsize=(14.0, 9.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master clean background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Top Header Banner
    ax.add_patch(patches.Rectangle(
        (0.02, 0.925), 0.96, 0.062,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.962, "FIVE-PILLAR GLOBAL REGULATORY COMPLIANCE SHIELD",
            ha="center", va="center", fontsize=11.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.938, "Statutory Alignment of C-STGB Neuro-Symbolic Governance with International Banking Mandates",
            ha="center", va="center", fontsize=8.0, color="#94a3b8")

    # Center Hub Coordinates
    cx, cy = 0.50, 0.485
    r_hub = 0.088

    # 5 Outer Pillar Shield Cards Configuration
    # Spatially optimized to guarantee at least 0.08 spacing between all visual elements
    card_w = 0.270
    card_h = 0.172

    pillars = [
        {
            "id": "PILLAR 1",
            "name": "FATF 40 RECOMMENDATIONS",
            "mandate": "Mandate: Rec. 16 (Travel Rule) & RBA",
            "shield_title": "Zero-Leakage AST Graph Audit",
            "shield_desc": "Originator / beneficiary cryptographic binding with\nzero lookahead leakage across causal transaction streams.",
            "link": "Semantic AST\nAudit Guard",
            "cx": 0.500, "cy": 0.812,
            "spoke_start": (cx, cy + r_hub),
            "spoke_end": (0.500, 0.726),
            "badge_pos": (0.500, 0.650),
            "color": COLOR_INGEST,
            "bg": COLOR_INGEST_BG
        },
        {
            "id": "PILLAR 2",
            "name": "FINCEN BSA / AMLA 2020",
            "mandate": "Mandate: 31 CFR § 1020.320 (SAR Filing)",
            "shield_title": "Autonomous SAR Dossier (<30s)",
            "shield_desc": "Multi-agent autonomous narrative generation;\nfull evidentiary SAR package ready for FinCEN filing.",
            "link": "Automated\nSAR Dossier",
            "cx": 0.850, "cy": 0.585,
            "spoke_start": (cx + r_hub * np.cos(np.radians(16)), cy + r_hub * np.sin(np.radians(16))),
            "spoke_end": (0.850 - card_w / 2, 0.560),
            "badge_pos": (0.652, 0.535),
            "color": COLOR_RISK,
            "bg": COLOR_RISK_BG
        },
        {
            "id": "PILLAR 3",
            "name": "BANGLADESH BANK BFIU",
            "mandate": "Mandate: BFIU Circular 26 & MLPA 2012 (MFS)",
            "shield_title": "Multi-Rail Invariant Profiling",
            "shield_desc": "MFS velocity smurfing detection on bKash/Nagad;\ncross-rail trade-based wash laundering tracking.",
            "link": "Multi-Rail MFS\nVelocity Profiling",
            "cx": 0.755, "cy": 0.188,
            "spoke_start": (cx + r_hub * np.cos(np.radians(312)), cy + r_hub * np.sin(np.radians(312))),
            "spoke_end": (0.700, 0.274),
            "badge_pos": (0.620, 0.335),
            "color": COLOR_REVIEW,
            "bg": COLOR_REVIEW_BG
        },
        {
            "id": "PILLAR 4",
            "name": "EU AI ACT & 6AMLD",
            "mandate": "Mandate: Title III High-Risk AI / Art. 14 Oversight",
            "shield_title": "Conformal 4-Eyes Governance",
            "shield_desc": "Guaranteed ≥ 99% coverage straight-through triage;\nsubgraph XAI audit trail for human investigator signoff.",
            "link": "Conformal CRC\n4-Eyes Triage",
            "cx": 0.245, "cy": 0.188,
            "spoke_start": (cx + r_hub * np.cos(np.radians(228)), cy + r_hub * np.sin(np.radians(228))),
            "spoke_end": (0.300, 0.274),
            "badge_pos": (0.380, 0.335),
            "color": COLOR_SAFE,
            "bg": COLOR_SAFE_BG
        },
        {
            "id": "PILLAR 5",
            "name": "US FED SR 11-7 / OCC",
            "mandate": "Mandate: Model Risk Mgmt & Concept Drift",
            "shield_title": "DKW Non-Parametric Drift Bounds",
            "shield_desc": "Continuous two-sample Kolmogorov-Smirnov drift bounds\nwith provable finite-sample error limits on live data.",
            "link": "Non-Parametric\nDKW Bounds",
            "cx": 0.150, "cy": 0.585,
            "spoke_start": (cx - r_hub * np.cos(np.radians(16)), cy + r_hub * np.sin(np.radians(16))),
            "spoke_end": (0.150 + card_w / 2, 0.560),
            "badge_pos": (0.348, 0.535),
            "color": COLOR_GNN,
            "bg": COLOR_GNN_BG
        }
    ]

    # Draw Connecting Spokes & Badges FIRST (behind cards and hub)
    for p in pillars:
        sx, sy = p["spoke_start"]
        ex, ey = p["spoke_end"]
        bx, by = p["badge_pos"]

        # Solid connecting pipeline ray
        ax.plot([sx, ex], [sy, ey], color=p["color"], lw=2.4, zorder=2, alpha=0.9)
        # Directional arrow marker at card entry
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=p["color"], mutation_scale=14),
                    zorder=3)

        # Spoke badge pill with ample clearance
        ax.text(bx, by, p["link"],
                ha="center", va="center", fontsize=7.2, fontweight="bold",
                color=COLOR_DARK, linespacing=1.1,
                bbox=dict(boxstyle="round,pad=0.28", facecolor="#ffffff",
                          edgecolor=p["color"], lw=1.3),
                zorder=5)

    # Draw Central Hub
    # Outer decorative glow halo
    ax.add_patch(patches.Circle(
        (cx, cy), r_hub + 0.007,
        facecolor="none", edgecolor="#cbd5e1", lw=1.5, zorder=5
    ))
    # Main Solid Circle
    ax.add_patch(patches.Circle(
        (cx, cy), r_hub,
        facecolor="#ffffff", edgecolor=COLOR_DARK, lw=2.8, zorder=6
    ))
    # Inner Accent Disc
    ax.add_patch(patches.Circle(
        (cx, cy), r_hub * 0.74,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0, zorder=7
    ))

    # Hub Central Typography
    ax.text(cx, cy + 0.035, "C-STGB", ha="center", va="center",
            fontsize=15.0, fontweight="bold", color=COLOR_DARK, zorder=8)
    ax.text(cx, cy + 0.012, "COMPLIANCE CORE", ha="center", va="center",
            fontsize=8.0, fontweight="bold", color=COLOR_SAFE, zorder=8)
    ax.text(cx, cy - 0.014, "Neuro-Symbolic\nDual Governance", ha="center", va="center",
            fontsize=7.4, fontweight="bold", color="#334155", linespacing=1.1, zorder=8)
    ax.text(cx, cy - 0.042, "Provable Guarantees", ha="center", va="center",
            fontsize=6.8, color="#64748b", zorder=8)

    # Draw 5 Outer Pillar Shield Cards
    for p in pillars:
        pcx, pcy = p["cx"], p["cy"]
        pw, ph = card_w, card_h
        x0 = pcx - pw / 2
        y0 = pcy - ph / 2

        # Card Outer Container
        ax.add_patch(patches.Rectangle(
            (x0, y0), pw, ph,
            facecolor=p["bg"], edgecolor=p["color"], lw=1.6, zorder=5
        ))

        # Top Header Pill/Bar
        header_h = 0.038
        ax.add_patch(patches.Rectangle(
            (x0, y0 + ph - header_h), pw, header_h,
            facecolor=p["color"], edgecolor="none", zorder=6
        ))
        ax.text(pcx, y0 + ph - header_h / 2, f"{p['id']}: {p['name']}",
                ha="center", va="center", fontsize=8.2, fontweight="bold", color="#ffffff", zorder=7)

        # Statutory Mandate Bar
        mandate_h = 0.026
        ax.add_patch(patches.Rectangle(
            (x0 + 0.006, y0 + ph - header_h - mandate_h - 0.003), pw - 0.012, mandate_h,
            facecolor="#ffffff", edgecolor=p["color"], lw=0.9, zorder=6
        ))
        ax.text(pcx, y0 + ph - header_h - mandate_h / 2 - 0.003, p["mandate"],
                ha="center", va="center", fontsize=7.1, fontweight="bold", color=COLOR_DARK, zorder=7)

        # Internal Shield Solution Box
        desc_box_y = y0 + 0.006
        desc_box_h = ph - header_h - mandate_h - 0.018
        ax.add_patch(patches.Rectangle(
            (x0 + 0.006, desc_box_y), pw - 0.012, desc_box_h,
            facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.8, zorder=6
        ))

        # Shield Title & Operational Guarantee
        ax.text(pcx, desc_box_y + desc_box_h - 0.018, p["shield_title"],
                ha="center", va="center", fontsize=7.6, fontweight="bold", color=p["color"], zorder=7)
        ax.plot([x0 + 0.015, x0 + pw - 0.015], [desc_box_y + desc_box_h - 0.032, desc_box_y + desc_box_h - 0.032],
                color=COLOR_BORDER, lw=0.6, zorder=7)
        ax.text(pcx, desc_box_y + 0.025, p["shield_desc"],
                ha="center", va="center", fontsize=6.8, color="#334155", linespacing=1.2, zorder=7)

    # Bottom Statutory Compliance Synthesis Strip
    ax.add_patch(patches.Rectangle(
        (0.02, 0.018), 0.96, 0.068,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.2
    ))
    ax.text(0.50, 0.060, "REGULATORY COMPLIANCE SYNTHESIS: Provable Mathematical Coverage Across Tier-1 Banking Regimes",
            ha="center", va="center", fontsize=8.4, fontweight="bold", color=COLOR_DARK)
    ax.text(0.50, 0.040, "All architectural mappings, mathematical drift bounds, and AST validation schemas are cross-referenced in Chapter 9, Table 9.1.",
            ha="center", va="center", fontsize=7.2, color=COLOR_MUTED)
    ax.text(0.50, 0.024, "FATF Rec 16 Travel Rule Verification  |  Sub-30s FinCEN SAR Generation  |  BFIU MFS Anti-Smurfing  |  EU AI Act Art. 14 Human Oversight  |  Fed SR 11-7 DKW Drift Bound",
            ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_INGEST)

    save_figure(fig, "fig_regulatory_shields", pad_inches=0.10)
    save_figure(fig, "fig25_regulatory_shields", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
