"""
Figure 9.1: Phased Enterprise Production Deployment Roadmap
Redesigned with enlarged, highly legible typography (all text >= 7.0pt to 11.2pt),
spacious card layout (width=23.5), wide 13.0-unit inter-card progression corridors,
and prominent verification gateway cards (Gate 1 & Gate 2) linking phases.
Phase 1: Passive Shadow (Weeks 1-8) -> Gateway 1: KS Drift Stabilization
Phase 2: Dual-Run Co-Pilot (Weeks 9-16) -> Gateway 2: SLA Burst Stress Test
Phase 3: Autonomous STP (Weeks 17-26) -> Statutory Production Handover
Zero text clipping, zero crowding, professional enterprise architecture standards.
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
    # Spacious widescreen canvas (14.2 x 7.2 inches)
    fig, ax = plt.subplots(figsize=(14.2, 7.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Top Master Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 92.2), 96.5, 6.6,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(49.75, 96.2, "ENTERPRISE PRODUCTION DEPLOYMENT ROADMAP (26-WEEK MIGRATION)",
            ha="center", va="center", fontsize=11.2, fontweight="bold", color="#ffffff")
    ax.text(49.75, 93.6, "Three-Phase Governance Flowchart: Passive Shadow -> Dual-Run Pilot -> Full Autonomous Straight-Through Processing",
            ha="center", va="center", fontsize=8.0, color="#94a3b8")

    # Layout Coordinates
    card_y = 18.0
    card_h = 71.5
    hdr_h = 9.0

    # 3 Main Phase Cards with width 23.5 and 13.0-unit wide corridors
    phases = [
        {
            "x": 1.5, "w": 23.5,
            "phase": "PHASE 1 (WEEKS 1–8)",
            "title": "Passive Shadow Mode",
            "tagline": "Zero Live Banking Disruption",
            "fc": COLOR_INGEST_BG, "ec": COLOR_INGEST,
            "bullets": [
                ("Passive Kafka Tap", "0.0 ms impact mirror on core stream."),
                ("90-Day Calibration", "Accumulates non-stationary distribution."),
                ("Two-Sample KS Test", "Continuous drift tracking (target p > 0.05)."),
                ("Invariant Proof", "Validates 12-D mass-flow conservation.")
            ],
            "target_label": "Objective: 100% Shadow Isolation"
        },
        {
            "x": 38.0, "w": 23.5,
            "phase": "PHASE 2 (WEEKS 9–16)",
            "title": "Dual-Run Co-Pilot",
            "tagline": "Parallel Human-in-the-Loop Triage",
            "fc": COLOR_REVIEW_BG, "ec": COLOR_REVIEW,
            "bullets": [
                ("Parallel Scoring", "Runs concurrently with legacy rule engine."),
                ("Ambiguity Triage", "Routes Tier-2 alerts to compliance desks."),
                ("Active Learning", "Incorporates analyst verdicts into memory."),
                ("Burst Stress Test", "Validates 31,250 tx/s under peak stress.")
            ],
            "target_label": "Objective: Analyst Queue Cut >= 90%"
        },
        {
            "x": 74.5, "w": 23.5,
            "phase": "PHASE 3 (WEEKS 17–26)",
            "title": "Autonomous STP",
            "tagline": "Straight-Through Clearance",
            "fc": COLOR_SAFE_BG, "ec": COLOR_SAFE,
            "bullets": [
                ("99.33% Straight-Thru", "Automated instant clearing in sub-0.45 ms."),
                ("Tier-1 Quarantine", "Immediate sub-second freeze on illicit risk."),
                ("Autonomous SAR", "Sub-30s dossiers generated for regulators."),
                ("Immutable WORM", "Cryptographic Merkle seal to 7-yr vault.")
            ],
            "target_label": "Objective: Statutory Autonomous STP"
        }
    ]

    # Draw Phase Cards
    for p in phases:
        px, pw = p["x"], p["w"]
        
        # Outer Card Container
        ax.add_patch(patches.Rectangle((px, card_y), pw, card_h, facecolor=p["fc"], edgecolor=p["ec"], lw=1.6, zorder=2))
        
        # Header Banner
        ax.add_patch(patches.Rectangle((px, card_y + card_h - hdr_h), pw, hdr_h, facecolor=p["ec"], edgecolor="none", zorder=3))
        ax.text(px + pw/2, card_y + card_h - 2.8, p["phase"], ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff", zorder=4)
        ax.text(px + pw/2, card_y + card_h - 6.2, p["title"], ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff", zorder=4)

        # Tagline
        ax.text(px + pw/2, card_y + card_h - 11.5, p["tagline"], ha="center", va="center", fontsize=8.0, color=COLOR_DARK, fontweight="bold", zorder=4)
        ax.plot([px + 1.2, px + pw - 1.2], [card_y + card_h - 14.2, card_y + card_h - 14.2], color=COLOR_BORDER, lw=0.9, zorder=4)

        # 4 Operational Bullets inside Card
        b_y_start = card_y + card_h - 17.2
        dy = 12.4
        for bi, (btitle, bsub) in enumerate(p["bullets"]):
            by = b_y_start - bi * dy
            # Milestone Box
            ax.add_patch(patches.Rectangle((px + 1.0, by - 5.2), pw - 2.0, 10.8, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.8, zorder=3))
            ax.plot([px + 2.4], [by + 2.0], marker="s", markersize=3.8, color=p["ec"], zorder=4)
            ax.text(px + 3.8, by + 2.0, btitle, ha="left", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK, zorder=4)
            ax.text(px + 3.8, by - 2.0, bsub, ha="left", va="center", fontsize=7.0, color="#334155", zorder=4)

        # Bottom Verification Strip
        strip_y = card_y + 1.6
        strip_h = 6.4
        ax.add_patch(patches.Rectangle((px + 1.0, strip_y), pw - 2.0, strip_h, facecolor="#ffffff", edgecolor=p["ec"], lw=1.2, zorder=3))
        ax.text(px + pw/2, strip_y + strip_h / 2, p["target_label"], ha="center", va="center",
                fontsize=7.4, fontweight="bold", color=p["ec"], zorder=4)

    # =========================================================================
    # HIGH-VISIBILITY PROGRESSION GATEWAYS (Bridges between Phase Cards)
    # =========================================================================
    gateways = [
        {
            "id": "GATEWAY 1",
            "timing": "WEEK 8 AUDIT",
            "cond1": "KS Drift p > 0.05",
            "cond2": "Coverage ≥ 99%",
            "status": "VERIFIED & SIGNED",
            "start_x": 25.0,
            "end_x": 38.0,
            "gw_cx": 31.5,
            "gw_w": 9.2,
            "ec": COLOR_RISK,
            "badge_color": COLOR_RISK
        },
        {
            "id": "GATEWAY 2",
            "timing": "WEEK 16 AUDIT",
            "cond1": "P99 SLA < 2.5 ms",
            "cond2": "Peak 31,250 tx/s",
            "status": "VERIFIED & SIGNED",
            "start_x": 61.5,
            "end_x": 74.5,
            "gw_cx": 68.0,
            "gw_w": 9.2,
            "ec": COLOR_REVIEW,
            "badge_color": COLOR_REVIEW
        }
    ]

    gw_y = 51.5
    gw_h = 28.0

    for gw in gateways:
        gx = gw["gw_cx"]
        gw_w = gw["gw_w"]
        
        # Directional entry and exit chevrons with clean margins
        ax.annotate("", xy=(gx - gw_w/2 - 0.2, gw_y), xytext=(gw["start_x"] + 0.4, gw_y),
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_DARK, mutation_scale=11),
                    zorder=3)
        ax.annotate("", xy=(gw["end_x"] - 0.4, gw_y), xytext=(gx + gw_w/2 + 0.2, gw_y),
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_SAFE, mutation_scale=11),
                    zorder=3)

        # Gateway Card Container
        ax.add_patch(patches.Rectangle(
            (gx - gw_w/2, gw_y - gw_h/2), gw_w, gw_h,
            facecolor="#ffffff", edgecolor=gw["ec"], lw=1.5, zorder=4
        ))

        # Gateway Top Pill Header
        header_gw_h = 5.2
        ax.add_patch(patches.Rectangle(
            (gx - gw_w/2, gw_y + gw_h/2 - header_gw_h), gw_w, header_gw_h,
            facecolor=gw["badge_color"], edgecolor="none", zorder=5
        ))
        ax.text(gx, gw_y + gw_h/2 - header_gw_h/2, gw["id"], ha="center", va="center",
                fontsize=7.8, fontweight="bold", color="#ffffff", zorder=6)

        # Timing tag above criteria
        ax.text(gx, gw_y + gw_h/2 - 7.6, gw["timing"], ha="center", va="center",
                fontsize=6.8, fontweight="bold", color=COLOR_MUTED, zorder=6)

        # Criteria Box
        ax.add_patch(patches.Rectangle(
            (gx - gw_w/2 + 0.5, gw_y - 7.0), gw_w - 1.0, 12.0,
            facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=0.7, zorder=5
        ))
        ax.text(gx, gw_y + 2.6, "Pass Condition:", ha="center", va="center",
                fontsize=6.6, color=COLOR_MUTED, zorder=6)
        ax.text(gx, gw_y - 0.6, gw["cond1"], ha="center", va="center",
                fontsize=7.2, fontweight="bold", color=COLOR_SAFE, zorder=6)
        ax.text(gx, gw_y - 4.0, gw["cond2"], ha="center", va="center",
                fontsize=7.2, fontweight="bold", color=COLOR_INGEST, zorder=6)

        # Verified Status Seal Pill at Bottom of Gateway
        seal_h = 4.6
        ax.add_patch(patches.Rectangle(
            (gx - gw_w/2 + 0.5, gw_y - gw_h/2 + 1.2), gw_w - 1.0, seal_h,
            facecolor="#dcfce7", edgecolor=COLOR_SAFE, lw=1.0, zorder=5
        ))
        ax.text(gx, gw_y - gw_h/2 + 1.2 + seal_h/2, gw["status"], ha="center", va="center",
                fontsize=6.4, fontweight="bold", color=COLOR_SAFE, zorder=6)

    # Bottom Executive Takeaway Callout Box
    ax.add_patch(patches.Rectangle(
        (1.5, 2.0), 96.5, 13.0,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.2
    ))
    ax.text(49.75, 11.5, "EXECUTIVE ROADMAP TAKEAWAY: 26-WEEK PHASED ENTERPRISE PRODUCTION MIGRATION",
            ha="center", va="center", fontsize=8.8, fontweight="bold", color=COLOR_DARK)
    ax.text(49.75, 7.8, "Phase 1 (Shadow): Zero live banking disruption; verifies KS drift bounds (p > 0.05) & accumulates 90-day conformal calibration.",
            ha="center", va="center", fontsize=7.8, color="#334155")
    ax.text(49.75, 4.6, "Phase 2 & 3: Dual-run co-pilot stress-tests 31,250 tx/s, scaling to 99.33% autonomous straight-through settlement with 4-eyes oversight.",
            ha="center", va="center", fontsize=7.8, color="#334155")

    save_figure(fig, "fig_enterprise_deployment_lifecycle", pad_inches=0.10)
    save_figure(fig, "fig_26week_roadmap_gantt", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
