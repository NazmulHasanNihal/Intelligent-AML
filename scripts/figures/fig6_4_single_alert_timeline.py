"""
Figure 6.4: Chronological Forensic Timeline of Laundering Incident
Bangladeshi Banking & Mobile Financial Services (MFS) Case Study:
Motijheel Dhaka Influx -> bKash/Nagad Smurfing -> Khatunganj Chattogram Wash -> Offshore Sink -> BFIU SAR
Zero raw math clutter; strictly uses Bangladesh Standard Time (BST, UTC+6) and realistic transaction data.
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
    # Generous widescreen canvas for spacious timeline
    fig, ax = plt.subplots(figsize=(12.8, 5.6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(50.0, 96.5, "CHRONOLOGICAL FORENSIC INVESTIGATION TIMELINE (BANGLADESH BANKING CASE)",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 94.0, "Detection Lifecycle: Motijheel Wire -> bKash/Nagad MFS Structuring -> Chattogram Wash -> Offshore Sink -> BFIU SAR",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # Central Timeline Axis (y = 51.0)
    y_axis = 51.0
    ax.annotate("", xy=(97.0, y_axis), xytext=(3.0, y_axis),
                arrowprops=dict(arrowstyle="->", lw=2.4, color=COLOR_DARK, shrinkA=0, shrinkB=0))
    ax.text(97.5, y_axis, "BST (UTC+6)", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLOR_DARK)

    # Five Stages Data: Pure practical banking without math formulas
    stages = [
        {
            "x": 11.5,
            "time": "10:15:00 BST",
            "title": "Stage 1: Primary Wire",
            "entity": "Motijheel Corporate Acc",
            "metric": "Wire Influx: BDT 5,000,000",
            "sub": "Dormant account reactivation",
            "fc": COLOR_INGEST_BG,
            "ec": COLOR_INGEST,
            "tc": COLOR_INGEST,
            "dt": "T = 0 min"
        },
        {
            "x": 30.5,
            "time": "10:19:10 BST",
            "title": "Stage 2: MFS Smurfing",
            "entity": "bKash & Nagad Wallets",
            "metric": "Structured: BDT 99,000 / tx",
            "sub": "Evades BDT 100,000 CTR limit",
            "fc": COLOR_REVIEW_BG,
            "ec": COLOR_REVIEW,
            "tc": COLOR_REVIEW,
            "dt": "+4m 10s"
        },
        {
            "x": 49.5,
            "time": "10:23:00 BST",
            "title": "Stage 3: Trade Wash",
            "entity": "Khatunganj Commodity Hub",
            "metric": "14 Benign Chaff Links Filtered",
            "sub": "Rapid wash dwell (<3.8 min)",
            "fc": "#FAF5FF",
            "ec": COLOR_GNN,
            "tc": COLOR_GNN,
            "dt": "+3m 50s"
        },
        {
            "x": 68.5,
            "time": "10:27:45 BST",
            "title": "Stage 4: Offshore Remittance",
            "entity": "Singapore / UAE Shell Co",
            "metric": "Consolidated: BDT 4,950,000",
            "sub": "99.0% flow retention through chain",
            "fc": COLOR_RISK_BG,
            "ec": COLOR_RISK,
            "tc": COLOR_RISK,
            "dt": "+4m 45s"
        },
        {
            "x": 87.5,
            "time": "10:28:12 BST",
            "title": "Stage 5: Automated SAR",
            "entity": "BFIU Regulatory Filing Desk",
            "metric": "Real-Time Freeze (<0.45 ms)",
            "sub": "SHA-256 Merkle WORM Sealed",
            "fc": COLOR_SAFE_BG,
            "ec": COLOR_SAFE,
            "tc": COLOR_SAFE,
            "dt": "+27 sec"
        }
    ]

    card_w = 17.5
    card_h = 30.0

    for i, s in enumerate(stages):
        cx = s["x"]
        is_above = (i % 2 == 0)

        # Milestone Pin Circle on Central Axis
        pin = patches.Circle((cx, y_axis), 1.6, facecolor=s["ec"], edgecolor="#ffffff", lw=1.2, zorder=5)
        ax.add_patch(pin)

        # Interval duration badge between pins
        if i > 0:
            prev_cx = stages[i-1]["x"]
            mid_x = (prev_cx + cx) / 2
            ax.text(mid_x, y_axis, s["dt"], ha="center", va="center",
                    fontsize=6.5, fontweight="bold", color=COLOR_DARK,
                    bbox=dict(boxstyle="square,pad=0.25", fc="#ffffff", ec=COLOR_BORDER, lw=0.8), zorder=6)

        if is_above:
            # Timestamp Badge below pin
            ax.text(cx, y_axis - 3.8, s["time"], ha="center", va="top",
                    fontsize=7.0, fontweight="bold", color=COLOR_DARK,
                    bbox=dict(boxstyle="square,pad=0.25", fc="#f8fafc", ec=COLOR_BORDER, lw=0.8), zorder=6)
            # Connector vertical line up to card
            ax.plot([cx, cx], [y_axis + 1.6, 57.0], color=s["ec"], lw=1.6, zorder=3)

            # Card Above (y: 57.0 to 87.0)
            card = patches.Rectangle((cx - card_w/2, 57.0), card_w, card_h,
                                     facecolor=s["fc"], edgecolor=s["ec"], lw=1.4, zorder=3)
            ax.add_patch(card)

            # Header inside Card
            ax.add_patch(patches.Rectangle((cx - card_w/2, 57.0 + card_h - 6.5), card_w, 6.5,
                                           facecolor=s["ec"], edgecolor="none", zorder=4))
            ax.text(cx, 57.0 + card_h - 3.2, s["title"], ha="center", va="center",
                    fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

            # Content inside Card Above
            ax.text(cx, 75.5, s["entity"], ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK, zorder=4)
            ax.text(cx, 68.5, s["metric"], ha="center", va="center", fontsize=6.6, fontweight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 62.0, s["sub"], ha="center", va="center", fontsize=6.2, color=COLOR_MUTED, zorder=4)

        else:
            # Timestamp Badge above pin
            ax.text(cx, y_axis + 3.8, s["time"], ha="center", va="bottom",
                    fontsize=7.0, fontweight="bold", color=COLOR_DARK,
                    bbox=dict(boxstyle="square,pad=0.25", fc="#f8fafc", ec=COLOR_BORDER, lw=0.8), zorder=6)
            # Connector vertical line down to card
            ax.plot([cx, cx], [y_axis - 1.6, 45.0], color=s["ec"], lw=1.6, zorder=3)

            # Card Below (y: 15.0 to 45.0)
            card = patches.Rectangle((cx - card_w/2, 15.0), card_w, card_h,
                                     facecolor=s["fc"], edgecolor=s["ec"], lw=1.4, zorder=3)
            ax.add_patch(card)

            # Header inside Card Below
            ax.add_patch(patches.Rectangle((cx - card_w/2, 15.0 + card_h - 6.5), card_w, 6.5,
                                           facecolor=s["ec"], edgecolor="none", zorder=4))
            ax.text(cx, 15.0 + card_h - 3.2, s["title"], ha="center", va="center",
                    fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

            # Content inside Card Below
            ax.text(cx, 33.5, s["entity"], ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK, zorder=4)
            ax.text(cx, 26.5, s["metric"], ha="center", va="center", fontsize=6.6, fontweight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 20.0, s["sub"], ha="center", va="center", fontsize=6.2, color=COLOR_MUTED, zorder=4)

    # Bottom Takeaway Callout Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 3.0), 97.0, 8.5,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    ax.text(50.0, 8.2, "CRITICAL DETECTION WINDOW: Total Influx-to-Quarantine Elapsed Dwell = 13 Minutes 12 Seconds",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(50.0, 5.2, "C-STGB unmasks sub-threshold bKash/Nagad smurfing and freezes funds before offshore clearing settlement completes.",
            ha="center", va="center", fontsize=6.8, color=COLOR_MUTED)

    save_figure(fig, "fig_single_alert_timeline", pad_inches=0.12)
    save_figure(fig, "fig21_single_alert_timeline", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
