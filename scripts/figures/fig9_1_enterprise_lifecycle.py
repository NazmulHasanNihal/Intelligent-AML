"""
Figure 9.1: Phased Enterprise Production Deployment Timeline
Redesigned as a horizontal Gantt-style timeline with distinct milestones:
Stage I: Shadow Mode (Eye / Clock icons)
Stage II: Human-in-the-Loop Dual-Run (Human / Scale icons)
Stage III: Autonomous Full STP (Rocket / Shield icons)
Strict publication palette and zero paragraph clutter.
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

def draw_eye_icon(ax, cx, cy, span, color):
    """Draws a clean stylized observation eye icon."""
    # Outer eye contour
    ax.add_patch(patches.Arc((cx, cy), span*1.6, span*0.9, theta1=20, theta2=160, color=color, lw=2.0))
    ax.add_patch(patches.Arc((cx, cy), span*1.6, span*0.9, theta1=200, theta2=340, color=color, lw=2.0))
    # Iris & pupil
    ax.add_patch(patches.Circle((cx, cy), span*0.35, facecolor="#ffffff", edgecolor=color, lw=1.5))
    ax.add_patch(patches.Circle((cx, cy), span*0.18, facecolor=color, edgecolor="none"))

def draw_clock_icon(ax, cx, cy, radius, color):
    """Draws a clean clock icon for calibration."""
    ax.add_patch(patches.Circle((cx, cy), radius, facecolor="#ffffff", edgecolor=color, lw=2.0))
    ax.plot([cx, cx], [cy, cy + radius*0.65], color=color, lw=2.0)
    ax.plot([cx, cx + radius*0.5], [cy, cy], color=color, lw=1.8)
    ax.add_patch(patches.Circle((cx, cy), radius*0.12, facecolor=color, edgecolor="none"))

def draw_human_icon(ax, cx, cy, span, color):
    """Draws a human analyst review icon."""
    # Head
    ax.add_patch(patches.Circle((cx, cy + span*0.35), span*0.28, facecolor=color, edgecolor="none"))
    # Shoulders
    ax.add_patch(patches.Arc((cx, cy - span*0.35), span*1.3, span*0.95, theta1=0, theta2=180,
                             facecolor=color, edgecolor=color, lw=2.0))
    ax.add_patch(patches.Polygon([
        (cx - span*0.65, cy - span*0.35),
        (cx + span*0.65, cy - span*0.35),
        (cx + span*0.45, cy - span*0.75),
        (cx - span*0.45, cy - span*0.75)
    ], facecolor=color, edgecolor="none"))

def draw_rocket_icon(ax, cx, cy, span, color):
    """Draws a stylized rocket icon for high-speed production autonomy."""
    # Main fuselage
    ax.add_patch(patches.Polygon([
        (cx, cy + span*0.7),
        (cx - span*0.3, cy - span*0.2),
        (cx + span*0.3, cy - span*0.2)
    ], facecolor=color, edgecolor=COLOR_DARK, lw=1.2))
    # Left fin
    ax.add_patch(patches.Polygon([
        (cx - span*0.25, cy - span*0.1),
        (cx - span*0.55, cy - span*0.45),
        (cx - span*0.25, cy - span*0.35)
    ], facecolor=COLOR_DARK, edgecolor="none"))
    # Right fin
    ax.add_patch(patches.Polygon([
        (cx + span*0.25, cy - span*0.1),
        (cx + span*0.55, cy - span*0.45),
        (cx + span*0.25, cy - span*0.35)
    ], facecolor=COLOR_DARK, edgecolor="none"))
    # Porthole
    ax.add_patch(patches.Circle((cx, cy + span*0.15), span*0.12, facecolor="#ffffff", edgecolor=COLOR_DARK, lw=1.0))
    # Exhaust flame
    ax.add_patch(patches.Polygon([
        (cx - span*0.18, cy - span*0.25),
        (cx, cy - span*0.65),
        (cx + span*0.18, cy - span*0.25)
    ], facecolor=COLOR_RISK, edgecolor="none"))

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (0.015, 0.915), 0.970, 0.070,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.958, "ENTERPRISE PRODUCTION DEPLOYMENT ROADMAP (26 WEEKS)",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.932, "Three Phased Operational Milestones: Passive Shadow -> Dual-Run Pilot -> Full Autonomous STP",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # HORIZONTAL GANTT TIMELINE BAR (x: 0.05 to 0.95, y: 0.810 to 0.865)
    tl_y = 0.815
    tl_h = 0.055

    # Milestone 1 Track (Weeks 1-8: 31% width)
    m1_w = 0.280
    ax.add_patch(patches.Rectangle(
        (0.05, tl_y), m1_w, tl_h,
        facecolor=COLOR_INGEST, edgecolor="#ffffff", lw=1.5
    ))
    ax.text(0.05 + m1_w/2, tl_y + tl_h/2, "STAGE I: WEEKS 1 – 8 (SHADOW)",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

    # Milestone 2 Track (Weeks 9-16: 31% width)
    m2_w = 0.280
    m2_x = 0.05 + m1_w + 0.010
    ax.add_patch(patches.Rectangle(
        (m2_x, tl_y), m2_w, tl_h,
        facecolor=COLOR_REVIEW, edgecolor="#ffffff", lw=1.5
    ))
    ax.text(m2_x + m2_w/2, tl_y + tl_h/2, "STAGE II: WEEKS 9 – 16 (DUAL-RUN)",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

    # Milestone 3 Track (Weeks 17-26: 34% width)
    m3_w = 0.320
    m3_x = m2_x + m2_w + 0.010
    ax.add_patch(patches.Rectangle(
        (m3_x, tl_y), m3_w, tl_h,
        facecolor=COLOR_SAFE, edgecolor="#ffffff", lw=1.5
    ))
    ax.text(m3_x + m3_w/2, tl_y + tl_h/2, "STAGE III: WEEKS 17 – 26 (AUTONOMOUS STP)",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

    # 3 PROGRESSIVE MILESTONE COLUMNS (x: 0.05 to 0.95, y: 0.12 to 0.78)
    card_y = 0.120
    card_h = 0.665

    stages = [
        {
            "x": 0.05, "w": m1_w,
            "header": "Shadow Mode",
            "tagline": "Zero Live Core Banking Disruption",
            "color": COLOR_INGEST, "bg": COLOR_INGEST_BG,
            "icon_type": "eye_clock",
            "bullets": [
                "Passive Payment Rail Mirroring (Kafka)",
                "Zero Overhead on Live Ledger (0.00 ms)",
                "90-Day Calibration Horizon Accumulation",
                "Two-Sample KS Drift Validation (p > 0.05)"
            ],
            "gate": "Gate 1: Calibration Stabilization (1-alpha >= 99%)"
        },
        {
            "x": m2_x, "w": m2_w,
            "header": "Human-in-the-Loop",
            "tagline": "Dual-Run Compliance Co-Pilot",
            "color": COLOR_REVIEW, "bg": COLOR_REVIEW_BG,
            "icon_type": "human",
            "bullets": [
                "Parallel Execution with Legacy Rules",
                "Selective Routing of Ambiguous Alerts",
                "Active Learning Hard-Negative Memory Bank",
                "Stress-Tested at 31,250 tx/s Burst SLA"
            ],
            "gate": "Gate 2: Stress SLA Compliance (P99 < 2.5 ms)"
        },
        {
            "x": m3_x, "w": m3_w,
            "header": "Full STP",
            "tagline": "Autonomous Straight-Through Clearance",
            "color": COLOR_SAFE, "bg": COLOR_SAFE_BG,
            "icon_type": "rocket",
            "bullets": [
                "99.33% Straight-Through Flow (<0.45 ms)",
                "Immediate Tier-1 Real-Time Asset Quarantine",
                "Autonomous FinCEN SAR Filing (<30 s)",
                "Immutable SHA-256 Merkle WORM Ledger"
            ],
            "gate": "Gate 3: Full Autonomy & Statutory Certification"
        }
    ]

    for s in stages:
        sx, sw = s["x"], s["w"]
        
        # Outer Card
        ax.add_patch(patches.Rectangle(
            (sx, card_y), sw, card_h,
            facecolor=s["bg"], edgecolor=s["color"], lw=1.6
        ))

        # Big Bold Header
        ax.text(sx + sw/2, card_y + card_h - 0.055, s["header"],
                ha="center", va="center", fontsize=13.0, fontweight="bold", color=s["color"])
        ax.text(sx + sw/2, card_y + card_h - 0.095, s["tagline"],
                ha="center", va="center", fontsize=7.2, color=COLOR_DARK)

        # Separator line
        ax.plot([sx + 0.02, sx + sw - 0.02], [card_y + card_h - 0.125, card_y + card_h - 0.125],
                color=s["color"], lw=1.0)

        # Icon Visual Area
        icon_cx = sx + sw/2
        icon_cy = card_y + card_h - 0.220
        if s["icon_type"] == "eye_clock":
            draw_eye_icon(ax, icon_cx - 0.045, icon_cy, 0.045, s["color"])
            draw_clock_icon(ax, icon_cx + 0.045, icon_cy, 0.035, s["color"])
        elif s["icon_type"] == "human":
            draw_human_icon(ax, icon_cx, icon_cy, 0.055, s["color"])
        elif s["icon_type"] == "rocket":
            draw_rocket_icon(ax, icon_cx, icon_cy, 0.055, s["color"])

        # Separator line below icons
        ax.plot([sx + 0.02, sx + sw - 0.02], [card_y + card_h - 0.315, card_y + card_h - 0.315],
                color=COLOR_BORDER, lw=0.8)

        # High-Impact Conceptual Bullets (Zero paragraph text)
        b_y = card_y + card_h - 0.365
        for j, bullet in enumerate(s["bullets"]):
            ax.text(sx + 0.015, b_y - j * 0.058, "•", fontsize=9.0, fontweight="bold", color=s["color"])
            ax.text(sx + 0.028, b_y - j * 0.058, bullet, fontsize=6.8, color=COLOR_DARK, va="center")

        # Bottom Verification Exit Gate Bar
        gate_h = 0.070
        ax.add_patch(patches.Rectangle(
            (sx + 0.008, card_y + 0.012), sw - 0.016, gate_h,
            facecolor="#ffffff", edgecolor=s["color"], lw=1.2
        ))
        ax.text(sx + sw/2, card_y + 0.012 + gate_h - 0.022, "VERIFICATION EXIT CRITERIA",
                ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_MUTED)
        ax.text(sx + sw/2, card_y + 0.012 + 0.022, s["gate"],
                ha="center", va="center", fontsize=6.6, fontweight="bold", color=s["color"])

    # Bottom Callout Summary
    ax.add_patch(patches.Rectangle(
        (0.015, 0.025), 0.970, 0.065,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    ax.text(0.50, 0.057, "EXECUTIVE TAKEAWAY: 26-week phased adoption ensures zero core banking disruption during shadow calibration, verified SLA scaling during dual-run, and autonomous straight-through settlement in production.",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK)

    save_figure(fig, "fig_enterprise_deployment_lifecycle", pad_inches=0.12)
    save_figure(fig, "fig_26week_roadmap_gantt", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
