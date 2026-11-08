"""
Figure 5.3: 3-Tier Conformal Risk Control (CRC) Triage Funnel
Redesigned with clean Sankey-style proportional volume flows, huge internal percentages,
externalized arrow volume labels, single bold action sentences, and zero quantile formula clutter.
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
    setup_plt(font_size=8.5, title_size=10.2, label_size=8.5)
    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (2.0, 91.0), 96.0, 7.5,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(50.0, 95.5, "THREE-TIER CONFORMAL RISK CONTROL (CRC) OPERATIONAL TRIAGE FUNNEL",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 92.5, "Mathematical Guarantee: Finite-Sample 99.0% True-Positive Recall with 99.51% Review Queue Reduction",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # STAGE 1: INGESTION STREAM (x: 2.0 to 19.0)
    s1_x, s1_w = 2.0, 17.0
    s1_y, s1_h = 16.0, 71.0
    ax.add_patch(patches.Rectangle(
        (s1_x, s1_y), s1_w, s1_h,
        facecolor=COLOR_INGEST_BG, edgecolor=COLOR_INGEST, lw=1.6
    ))
    ax.add_patch(patches.Rectangle(
        (s1_x, s1_y + s1_h - 7.5), s1_w, 7.5,
        facecolor=COLOR_INGEST, edgecolor=COLOR_INGEST
    ))
    ax.text(s1_x + s1_w/2, s1_y + s1_h - 3.75, "STAGE 1: INGESTION",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

    ax.text(s1_x + s1_w/2, 68.0, "100%", ha="center", va="center", fontsize=22.0, fontweight="bold", color=COLOR_INGEST)
    ax.text(s1_x + s1_w/2, 59.0, "10,000 Transactions", ha="center", va="center", fontsize=8.2, fontweight="bold", color=COLOR_DARK)
    ax.text(s1_x + s1_w/2, 50.0, "Multi-Rail Ingress\nSWIFT • ACH • bKash", ha="center", va="center", fontsize=7.2, color=COLOR_MUTED, linespacing=1.2)
    ax.text(s1_x + s1_w/2, 38.0, "12-D Mass-Flow Invariants\nExtracted in <0.11 ms", ha="center", va="center", fontsize=7.0, color="#0369a1", linespacing=1.2)
    ax.text(s1_x + s1_w/2, 24.0, "Zero-Copy Arrow Pipeline\nEmbedded DuckDB Engine", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK, linespacing=1.2)

    # Ingestion -> Neural Core Arrow
    ax.annotate("", xy=(22.5, 51.5), xytext=(19.0, 51.5),
                arrowprops=dict(arrowstyle="->", lw=2.0, color=COLOR_INGEST, mutation_scale=14))
    ax.text(20.75, 54.5, "Streaming\nBatches", ha="center", va="bottom", fontsize=6.2, fontweight="bold", color=COLOR_INGEST)

    # STAGE 2: C-STGB NEURAL ARBITER (x: 22.5 to 44.5)
    s2_x, s2_w = 22.5, 22.0
    s2_y, s2_h = 24.0, 55.0
    ax.add_patch(patches.Rectangle(
        (s2_x, s2_y), s2_w, s2_h,
        facecolor=COLOR_GNN_BG, edgecolor=COLOR_GNN, lw=1.6
    ))
    ax.add_patch(patches.Rectangle(
        (s2_x, s2_y + s2_h - 7.5), s2_w, 7.5,
        facecolor=COLOR_GNN, edgecolor=COLOR_GNN
    ))
    ax.text(s2_x + s2_w/2, s2_y + s2_h - 3.75, "STAGE 2: C-STGB ARBITER",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

    ax.text(s2_x + s2_w/2, 63.5, "Conformal Risk Engine", ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_DARK)
    ax.text(s2_x + s2_w/2, 55.0, "Continuous Harmonic Attention\nEdge-Trust Camouflage Gating\nLatent Typology Oversampling",
            ha="center", va="center", fontsize=7.0, color=COLOR_MUTED, linespacing=1.3)
    
    # Decision Diamond Symbol
    diamond_pts = [[s2_x + s2_w/2, 44.0], [s2_x + s2_w/2 + 5.5, 38.0], [s2_x + s2_w/2, 32.0], [s2_x + s2_w/2 - 5.5, 38.0]]
    ax.add_patch(patches.Polygon(diamond_pts, closed=True, facecolor="#fef3c7", edgecolor="#d97706", lw=1.2))
    ax.text(s2_x + s2_w/2, 38.0, "99% Safety\nCalibration", ha="center", va="center", fontsize=6.0, fontweight="bold", color="#92400e")
    ax.text(s2_x + s2_w/2, 27.5, "Inference Latency: <0.45 ms", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_SAFE)

    # 3 OUTLET SANKEY-STYLE DISPATCH ARROWS & CHANNELS
    # Arrow coords from Arbiter (x=44.5) to Tier Blocks (x=59.0)
    
    # Tier 1 Arrow (Red)
    ax.annotate("", xy=(58.5, 76.0), xytext=(44.5, 55.0),
                arrowprops=dict(arrowstyle="->", lw=2.2, color=COLOR_RISK,
                                connectionstyle="arc3,rad=-0.12", mutation_scale=14))
    # Volume label next to arrow
    ax.text(50.5, 73.0, "Volume: 18 / 10k tx\n(High-Confidence Alert)",
            ha="center", va="bottom", fontsize=6.4, fontweight="bold", color=COLOR_RISK, linespacing=1.1)

    # Tier 2 Arrow (Amber/Orange)
    ax.annotate("", xy=(58.5, 51.5), xytext=(44.5, 51.5),
                arrowprops=dict(arrowstyle="->", lw=2.2, color=COLOR_REVIEW, mutation_scale=14))
    # Volume label next to arrow
    ax.text(51.0, 53.5, "Volume: 49 / 10k tx\n(Selective Abstention)",
            ha="center", va="bottom", fontsize=6.4, fontweight="bold", color=COLOR_REVIEW, linespacing=1.1)

    # Tier 3 Arrow (Green)
    ax.annotate("", xy=(58.5, 27.0), xytext=(44.5, 48.0),
                arrowprops=dict(arrowstyle="->", lw=2.8, color=COLOR_SAFE,
                                connectionstyle="arc3,rad=0.12", mutation_scale=16))
    # Volume label next to arrow
    ax.text(50.5, 30.0, "Volume: 9,933 / 10k tx\n(Straight-Through Clear)",
            ha="center", va="top", fontsize=6.4, fontweight="bold", color=COLOR_SAFE, linespacing=1.1)

    # =========================================================================
    # STAGE 3: THREE DESTINATION TIERS (x: 58.5 to 98.0)
    # With huge percentages inside and single bold action sentences
    # =========================================================================
    t_x, t_w = 58.5, 39.5

    # --- TIER 1: AUTO-QUARANTINE (Red) ---
    t1_y, t1_h = 66.0, 21.0
    ax.add_patch(patches.Rectangle(
        (t_x, t1_y), t_w, t1_h,
        facecolor=COLOR_RISK_BG, edgecolor=COLOR_RISK, lw=1.6
    ))
    # Huge percentage inside shape
    ax.add_patch(patches.Rectangle((t_x + 1.2, t1_y + 1.5), 11.5, t1_h - 3.0, facecolor=COLOR_RISK, edgecolor="none"))
    ax.text(t_x + 6.95, t1_y + t1_h/2, "0.18%", ha="center", va="center", fontsize=16.0, fontweight="bold", color="#ffffff")

    # Header and Single Bold Action Sentence
    ax.text(t_x + 14.5, t1_y + 14.8, "TIER 1: HIGH-RISK QUARANTINE",
            ha="left", va="center", fontsize=8.2, fontweight="bold", color=COLOR_RISK)
    ax.text(t_x + 14.5, t1_y + 9.5, "Tier 1: Auto-Block Transaction & Dispatch SAR Dossier",
            ha="left", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 14.5, t1_y + 4.5, "Immediate wire freeze • Cryptographic SHA-256 Merkle audit trail",
            ha="left", va="center", fontsize=6.8, color=COLOR_MUTED)

    # --- TIER 2: HUMAN COMPLIANCE DESK (Amber / Orange) ---
    t2_y, t2_h = 41.5, 21.0
    ax.add_patch(patches.Rectangle(
        (t_x, t2_y), t_w, t2_h,
        facecolor=COLOR_REVIEW_BG, edgecolor=COLOR_REVIEW, lw=1.6
    ))
    # Huge percentage inside shape
    ax.add_patch(patches.Rectangle((t_x + 1.2, t2_y + 1.5), 11.5, t2_h - 3.0, facecolor=COLOR_REVIEW, edgecolor="none"))
    ax.text(t_x + 6.95, t2_y + t2_h/2, "0.49%", ha="center", va="center", fontsize=16.0, fontweight="bold", color="#ffffff")

    # Header and Single Bold Action Sentence
    ax.text(t_x + 14.5, t2_y + 14.8, "TIER 2: SELECTIVE ABSTENTION DESK",
            ha="left", va="center", fontsize=8.2, fontweight="bold", color=COLOR_REVIEW)
    ax.text(t_x + 14.5, t2_y + 9.5, "Tier 2: Route to Senior 4-Eyes Compliance Investigation",
            ha="left", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 14.5, t2_y + 4.5, "-99.51% Human review queue slashing • Multi-agent forensic dossier",
            ha="left", va="center", fontsize=6.8, color=COLOR_MUTED)

    # --- TIER 3: STRAIGHT-THROUGH CLEARANCE (Green) ---
    t3_y, t3_h = 16.0, 22.0
    ax.add_patch(patches.Rectangle(
        (t_x, t3_y), t_w, t3_h,
        facecolor=COLOR_SAFE_BG, edgecolor=COLOR_SAFE, lw=1.8
    ))
    # Huge percentage inside shape
    ax.add_patch(patches.Rectangle((t_x + 1.2, t3_y + 1.5), 11.5, t3_h - 3.0, facecolor=COLOR_SAFE, edgecolor="none"))
    ax.text(t_x + 6.95, t3_y + t3_h/2, "99.33%", ha="center", va="center", fontsize=16.0, fontweight="bold", color="#ffffff")

    # Header and Single Bold Action Sentence
    ax.text(t_x + 14.5, t3_y + 15.5, "TIER 3: STRAIGHT-THROUGH CLEARANCE (STP)",
            ha="left", va="center", fontsize=8.2, fontweight="bold", color=COLOR_SAFE)
    ax.text(t_x + 14.5, t3_y + 10.2, "Tier 3: Instant Automated Straight-Through Release (<0.45 ms)",
            ha="left", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(t_x + 14.5, t3_y + 5.0, "Zero manual friction • Verified empirical leakage rate under 0.12%",
            ha="left", va="center", fontsize=6.8, color=COLOR_MUTED)

    # BOTTOM EXECUTIVE GUARANTEE SUMMARY (Sharp rectangular bar)
    ax.add_patch(patches.Rectangle(
        (2.0, 4.0), 96.0, 8.5,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    ax.text(18.0, 8.25, "STATISTICAL SAFETY\nFinite-Sample 99% Recall Guarantee",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK, linespacing=1.2)
    ax.text(50.0, 8.25, "OPERATIONAL EFFICIENCY\n-99.51% Human Review Queue Slashing",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_GNN, linespacing=1.2)
    ax.text(82.0, 8.25, "COMMERCIAL VELOCITY\n99.33% Straight-Through Flow at <0.45 ms",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_SAFE, linespacing=1.2)

    save_figure(fig, "fig_conformal_conveyor_funnel", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
