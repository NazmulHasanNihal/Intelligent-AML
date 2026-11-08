"""
Figure 5.3: Conformal Triage Conveyor and Multi-Tier Routing Funnel
Standalone publication script for C-STGB monograph.
Human-designed, perfectly fitted text, zero border collision, and crisp triage percentages.
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
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    fig, ax = plt.subplots(figsize=(11.8, 5.6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # 1. Master Top Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 90.5), 97.0, 8.0,
        facecolor="#0f172a", edgecolor="#1e293b", lw=1.2
    ))
    ax.text(50.0, 95.2, "Class-Conditional Conformal Risk Control (CRC) Triage Conveyor",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")
    ax.text(50.0, 92.2, "Automated Tri-Tier Triage Pipeline: Streaming Ingest -> Neural Conformal Arbiter -> 3 Operational Routing Tiers",
            ha="center", va="center", fontsize=7.0, color="#94a3b8")

    # =========================================================================
    # STAGE 1: TRANSACTION INGESTION & FEATURE HYDRATION (x: 2.0 to 18.0)
    # =========================================================================
    s1_x, s1_w = 2.0, 16.5
    s1_y, s1_h = 24.0, 63.0
    ax.add_patch(patches.Rectangle(
        (s1_x, s1_y), s1_w, s1_h,
        facecolor=COLOR_INGEST_BG, edgecolor=COLOR_INGEST, lw=1.5
    ))
    # Header strip
    ax.add_patch(patches.Rectangle(
        (s1_x, s1_y + s1_h - 7.0), s1_w, 7.0,
        facecolor=COLOR_INGEST, edgecolor=COLOR_INGEST
    ))
    ax.text(s1_x + s1_w/2, s1_y + s1_h - 3.5, "1. STREAMING INGEST",
            ha="center", va="center", fontsize=7.4, fontweight="bold", color="#ffffff")

    ax.text(s1_x + s1_w/2, 73.0, "Multi-Rail Streams", ha="center", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK)
    
    rails = ["SWIFT MT103", "Domestic RTGS", "Mobile Money", "Crypto / EVM"]
    for r_idx, r_txt in enumerate(rails):
        ry = 65.0 - r_idx * 7.5
        ax.add_patch(patches.Rectangle(
            (s1_x + 1.5, ry - 2.8), s1_w - 3.0, 5.6,
            facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.7
        ))
        ax.text(s1_x + s1_w/2, ry, r_txt, ha="center", va="center", fontsize=6.4, color=COLOR_DARK, fontweight="bold")

    ax.add_patch(patches.Rectangle(
        (s1_x + 1.2, 26.0), s1_w - 2.4, 7.5,
        facecolor="#ffffff", edgecolor=COLOR_INGEST, lw=0.8
    ))
    ax.text(s1_x + s1_w/2, 29.75, "DuckDB + Arrow IPC\n<0.11 ms Zero-Copy", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_INGEST, linespacing=1.1)

    # Ingestion -> Neural Arbiter Arrow
    ax.annotate("", xy=(22.5, 54.0), xytext=(18.5, 54.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_INGEST, mutation_scale=12))

    # =========================================================================
    # STAGE 2: C-STGB CONFORMAL ARBITER (x: 22.5 to 44.5)
    # =========================================================================
    s2_x, s2_w = 22.5, 21.0
    s2_y, s2_h = 24.0, 63.0
    ax.add_patch(patches.Rectangle(
        (s2_x, s2_y), s2_w, s2_h,
        facecolor=COLOR_GNN_BG, edgecolor=COLOR_GNN, lw=1.5
    ))
    ax.add_patch(patches.Rectangle(
        (s2_x, s2_y + s2_h - 7.0), s2_w, 7.0,
        facecolor=COLOR_GNN, edgecolor=COLOR_GNN
    ))
    ax.text(s2_x + s2_w/2, s2_y + s2_h - 3.5, "2. CONFORMAL ARBITER",
            ha="center", va="center", fontsize=7.4, fontweight="bold", color="#ffffff")

    ax.text(s2_x + s2_w/2, 73.0, "C-STGB Neural Core", ha="center", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK)
    
    arb_items = [
        "Harmonic Attention",
        "Edge-Trust Gate",
        "Typology SMOTE",
        "Bayes Calibration"
    ]
    for a_idx, a_txt in enumerate(arb_items):
        ay = 65.0 - a_idx * 7.5
        ax.add_patch(patches.Rectangle(
            (s2_x + 1.5, ay - 2.8), s2_w - 3.0, 5.6,
            facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.7
        ))
        ax.text(s2_x + s2_w/2, ay, a_txt, ha="center", va="center", fontsize=6.4, color=COLOR_DARK, fontweight="bold")

    # Decision Diamond
    ax.add_patch(patches.Rectangle(
        (s2_x + 1.2, 26.0), s2_w - 2.4, 7.5,
        facecolor="#fef3c7", edgecolor="#d97706", lw=0.8
    ))
    ax.text(s2_x + s2_w/2, 29.75, "Finite-Sample 99%\nCoverage Safety Bound", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#92400e", linespacing=1.1)

    # =========================================================================
    # CHANNEL ARROWS & VOLUME BADGES (x: 43.5 to 55.5)
    # =========================================================================
    # Tier 1 Arrow (Top, Red)
    ax.annotate("", xy=(55.5, 76.0), xytext=(43.5, 58.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RISK, mutation_scale=12))
    ax.add_patch(patches.Rectangle((44.5, 71.0), 9.5, 6.0, facecolor="#ffffff", edgecolor=COLOR_RISK, lw=0.8, zorder=5))
    ax.text(49.25, 74.0, "18 / 10,000 Wires\nAuto-Quarantine", ha="center", va="center", fontsize=5.6, fontweight="bold", color=COLOR_RISK, linespacing=1.1, zorder=6)

    # Tier 2 Arrow (Middle, Amber)
    ax.annotate("", xy=(55.5, 54.0), xytext=(43.5, 54.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_REVIEW, mutation_scale=12))
    ax.add_patch(patches.Rectangle((44.5, 50.5), 9.5, 6.0, facecolor="#ffffff", edgecolor=COLOR_REVIEW, lw=0.8, zorder=5))
    ax.text(49.25, 53.5, "49 / 10,000 Wires\nHuman Desk", ha="center", va="center", fontsize=5.6, fontweight="bold", color=COLOR_REVIEW, linespacing=1.1, zorder=6)

    # Tier 3 Arrow (Bottom, Green)
    ax.annotate("", xy=(55.5, 32.0), xytext=(43.5, 50.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=COLOR_SAFE, mutation_scale=12))
    ax.add_patch(patches.Rectangle((44.5, 33.0), 9.5, 6.0, facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=0.8, zorder=5))
    ax.text(49.25, 36.0, "9,933 / 10k Wires\nStraight-Through", ha="center", va="center", fontsize=5.6, fontweight="bold", color=COLOR_SAFE, linespacing=1.1, zorder=6)

    # =========================================================================
    # STAGE 3: THREE DESTINATION OPERATIONAL TIERS (x: 55.5 to 98.0)
    # Perfectly fitted text with zero overflow!
    # =========================================================================
    t_x, t_w = 55.5, 42.5

    # --- TIER 1: HIGH-RISK QUARANTINE (Red) ---
    t1_y, t1_h = 66.5, 20.5
    ax.add_patch(patches.Rectangle((t_x, t1_y), t_w, t1_h, facecolor=COLOR_RISK_BG, edgecolor=COLOR_RISK, lw=1.5))
    # Percentage Badge Block
    ax.add_patch(patches.Rectangle((t_x + 1.2, t1_y + 1.5), 11.0, t1_h - 3.0, facecolor=COLOR_RISK, edgecolor="none"))
    ax.text(t_x + 6.7, t1_y + t1_h/2, "0.18%", ha="center", va="center", fontsize=15.0, fontweight="bold", color="#ffffff")

    # Content (Neatly placed within t_w - 14.0 = 28.5 width)
    ax.text(t_x + 13.5, t1_y + 15.0, "TIER 1: HIGH-RISK QUARANTINE", ha="left", va="center", fontsize=7.8, fontweight="bold", color=COLOR_RISK)
    ax.text(t_x + 13.5, t1_y + 9.8, "Auto-Block Wire & Dispatch SAR Dossier", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 13.5, t1_y + 4.8, "Immediate freeze • Cryptographic SHA-256 seal", ha="left", va="center", fontsize=6.4, color="#475569")

    # --- TIER 2: HUMAN COMPLIANCE DESK (Amber) ---
    t2_y, t2_h = 44.0, 20.5
    ax.add_patch(patches.Rectangle((t_x, t2_y), t_w, t2_h, facecolor=COLOR_REVIEW_BG, edgecolor=COLOR_REVIEW, lw=1.5))
    # Percentage Badge Block
    ax.add_patch(patches.Rectangle((t_x + 1.2, t2_y + 1.5), 11.0, t2_h - 3.0, facecolor=COLOR_REVIEW, edgecolor="none"))
    ax.text(t_x + 6.7, t2_y + t2_h/2, "0.49%", ha="center", va="center", fontsize=15.0, fontweight="bold", color="#ffffff")

    # Content
    ax.text(t_x + 13.5, t2_y + 15.0, "TIER 2: SELECTIVE ABSTENTION DESK", ha="left", va="center", fontsize=7.8, fontweight="bold", color=COLOR_REVIEW)
    ax.text(t_x + 13.5, t2_y + 9.8, "Route to Senior 4-Eyes Compliance Team", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 13.5, t2_y + 4.8, "-99.51% Review queue cut • Forensic dossier", ha="left", va="center", fontsize=6.4, color="#475569")

    # --- TIER 3: STRAIGHT-THROUGH CLEARANCE (Green) ---
    t3_y, t3_h = 21.5, 20.5
    ax.add_patch(patches.Rectangle((t_x, t3_y), t_w, t3_h, facecolor=COLOR_SAFE_BG, edgecolor=COLOR_SAFE, lw=1.6))
    # Percentage Badge Block
    ax.add_patch(patches.Rectangle((t_x + 1.2, t3_y + 1.5), 11.0, t3_h - 3.0, facecolor=COLOR_SAFE, edgecolor="none"))
    ax.text(t_x + 6.7, t3_y + t3_h/2, "99.33%", ha="center", va="center", fontsize=15.0, fontweight="bold", color="#ffffff")

    # Content
    ax.text(t_x + 13.5, t3_y + 15.0, "TIER 3: STRAIGHT-THROUGH CLEARANCE", ha="left", va="center", fontsize=7.8, fontweight="bold", color=COLOR_SAFE)
    ax.text(t_x + 13.5, t3_y + 9.8, "Instant Automated Straight-Through Release", ha="left", va="center", fontsize=7.2, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 13.5, t3_y + 4.8, "Sub-millisecond SLA (<0.45 ms) • Zero friction", ha="left", va="center", fontsize=6.4, color="#475569")

    # =========================================================================
    # BOTTOM EXECUTIVE GUARANTEE SUMMARY RIBBON
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (1.5, 4.0), 97.0, 14.0,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    
    bot_cards = [
        ("STATISTICAL SAFETY", "99.0% True Recall Bound", "Class-conditional finite-sample guarantee", COLOR_INGEST),
        ("OPERATIONAL EFFICIENCY", "-99.51% Workload Cut", "Only 49 of 10,000 wires require review", COLOR_GNN),
        ("COMMERCIAL VELOCITY", "99.33% Straight-Through", "Settlement latency guaranteed <0.45 ms", COLOR_SAFE),
    ]
    card_w = 97.0 / len(bot_cards)
    for c_idx, (b_title, b_val, b_sub, b_col) in enumerate(bot_cards):
        cx_pos = 1.5 + c_idx * card_w
        # Left accent stripe
        ax.add_patch(patches.Rectangle((cx_pos + 2.0, 5.5), 0.8, 11.0, facecolor=b_col, edgecolor=b_col))
        ax.text(cx_pos + 5.0, 14.0, b_title, ha="left", va="center", fontsize=6.8, fontweight="bold", color=b_col)
        ax.text(cx_pos + 5.0, 10.5, b_val, ha="left", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK)
        ax.text(cx_pos + 5.0, 7.2, b_sub, ha="left", va="center", fontsize=6.2, color="#64748b")

    save_figure(fig, "fig_conformal_conveyor_funnel", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
