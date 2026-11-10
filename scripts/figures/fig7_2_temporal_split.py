"""
Figure 7.2: Zero-Leakage Chronological Dataset Split Timeline
Standard 4-Way Chronological Partitioning Architecture:
- Track A: Discrete UTXO Graphs (Bitcoin Networks: 49 Timesteps)
- Track B: High-Velocity Continuous Streams (PaySim, SAML-D, SWIFT, Ethereum)
- Staggered Vertical Causal Firewalls (Model Freeze, Threshold Lock, Holdout Lock)
- Four Architectural Specification Cards with strictly bounded text and generous margins
- Zero text clipping, zero border collisions, 100% publication standard
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
    # Generous canvas sized for immaculate layout and zero cramping
    fig, ax = plt.subplots(figsize=(13.6, 7.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master canvas background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner (Dark Slate Blue)
    ax.add_patch(patches.Rectangle(
        (1.5, 93.0), 97.0, 6.0,
        facecolor=COLOR_DARK, edgecolor="none", zorder=2
    ))
    ax.text(50.0, 96.8, "ZERO-LEAKAGE CHRONOLOGICAL DATASET PARTITIONING ARCHITECTURE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff", zorder=3)
    ax.text(50.0, 94.5, "Strict Causal Timeline Isolation: Eliminating Lookahead Bias, Graph Leakage, and Conformal Contamination",
            ha="center", va="center", fontsize=7.0, color="#94a3b8", zorder=3)

    # =========================================================================
    # TIMELINE CONVEYOR TRACKS (y = 62.0 to 90.0)
    # Perfectly aligned 4-way chronological splits: 60% / 10% / 10% / 20%
    # =========================================================================
    w_tot = 94.0
    x0 = 3.0
    h_track = 6.4

    w_tr = 0.60 * w_tot  # 56.40 -> x in [3.0, 59.4]
    w_vl = 0.10 * w_tot  # 9.40  -> x in [59.4, 68.8]
    w_cl = 0.10 * w_tot  # 9.40  -> x in [68.8, 78.2]
    w_te = 0.20 * w_tot  # 18.80 -> x in [78.2, 97.0]

    x_vl = x0 + w_tr
    x_cl = x_vl + w_vl
    x_te = x_cl + w_cl

    # --- Time Arrow Header at Top Right ---
    ax.annotate("", xy=(97.0, 90.5), xytext=(76.0, 90.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLOR_DARK, mutation_scale=9), zorder=4)
    ax.text(75.0, 90.5, "Causal Time Arrow (Past -> Future)", ha="right", va="center",
            fontsize=6.2, fontweight="bold", color=COLOR_DARK, zorder=4)

    # --- TRACK A: Discrete UTXO Graphs (Elliptic-v1 & v2: 49 Timesteps) ---
    y_track_a = 80.5
    ax.text(3.0, y_track_a + h_track + 1.2, "TRACK A: Discrete UTXO Graphs (Bitcoin Networks: 49 Timesteps, 2-Week Windows)",
            ha="left", va="bottom", fontsize=7.4, fontweight="bold", color=COLOR_DARK, zorder=4)

    # Track A: Train Bar
    ax.add_patch(patches.Rectangle((x0, y_track_a), w_tr, h_track, facecolor=COLOR_INGEST, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x0 + w_tr / 2.0, y_track_a + h_track / 2.0, "Training: Steps 1–30 (61.2%) — In-Sample Graph Learning",
            ha="center", va="center", color="#ffffff", fontsize=7.0, fontweight="bold", zorder=3)

    # Track A: Val Bar
    ax.add_patch(patches.Rectangle((x_vl, y_track_a), w_vl, h_track, facecolor=COLOR_REVIEW, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_vl + w_vl / 2.0, y_track_a + h_track / 2.0 + 1.3, "Val",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_vl + w_vl / 2.0, y_track_a + h_track / 2.0 - 1.4, "31–34",
            ha="center", va="center", color="#ffffff", fontsize=5.8, zorder=3)

    # Track A: Cal Bar
    ax.add_patch(patches.Rectangle((x_cl, y_track_a), w_cl, h_track, facecolor=COLOR_GNN, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_cl + w_cl / 2.0, y_track_a + h_track / 2.0 + 1.3, "Cal",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_cl + w_cl / 2.0, y_track_a + h_track / 2.0 - 1.4, "35–38",
            ha="center", va="center", color="#ffffff", fontsize=5.8, zorder=3)

    # Track A: Test Bar (Stacked text so it fits comfortably with zero clipping)
    ax.add_patch(patches.Rectangle((x_te, y_track_a), w_te, h_track, facecolor=COLOR_SAFE, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_te + w_te / 2.0, y_track_a + h_track / 2.0 + 1.3, "Forward Test: Steps 39–49",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_te + w_te / 2.0, y_track_a + h_track / 2.0 - 1.4, "(22.4% Out-of-Time)",
            ha="center", va="center", color="#ffffff", fontsize=5.8, zorder=3)

    # --- TRACK B: Continuous Streams (PaySim, SAML-D, SWIFT, Ethereum) ---
    y_track_b = 66.5
    ax.text(3.0, y_track_b + h_track + 1.2, "TRACK B: Continuous Streams (PaySim, SAML-D, IBM-AMLSim, Ethereum)",
            ha="left", va="bottom", fontsize=7.4, fontweight="bold", color=COLOR_DARK, zorder=4)

    # Track B: Train Bar
    ax.add_patch(patches.Rectangle((x0, y_track_b), w_tr, h_track, facecolor=COLOR_INGEST, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x0 + w_tr / 2.0, y_track_b + h_track / 2.0, "Training Stream: 0.00 to 0.60 T (60.0%) — Temporal State Learning",
            ha="center", va="center", color="#ffffff", fontsize=7.0, fontweight="bold", zorder=3)

    # Track B: Val Bar
    ax.add_patch(patches.Rectangle((x_vl, y_track_b), w_vl, h_track, facecolor=COLOR_REVIEW, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_vl + w_vl / 2.0, y_track_b + h_track / 2.0 + 1.3, "Val",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_vl + w_vl / 2.0, y_track_b + h_track / 2.0 - 1.4, "0.60–0.70 T",
            ha="center", va="center", color="#ffffff", fontsize=5.6, zorder=3)

    # Track B: Cal Bar
    ax.add_patch(patches.Rectangle((x_cl, y_track_b), w_cl, h_track, facecolor=COLOR_GNN, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_cl + w_cl / 2.0, y_track_b + h_track / 2.0 + 1.3, "Cal",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_cl + w_cl / 2.0, y_track_b + h_track / 2.0 - 1.4, "0.70–0.80 T",
            ha="center", va="center", color="#ffffff", fontsize=5.6, zorder=3)

    # Track B: Test Bar (Stacked text so it fits comfortably with zero clipping)
    ax.add_patch(patches.Rectangle((x_te, y_track_b), w_te, h_track, facecolor=COLOR_SAFE, edgecolor=COLOR_DARK, lw=1.0, zorder=2))
    ax.text(x_te + w_te / 2.0, y_track_b + h_track / 2.0 + 1.3, "Forward Test: 0.80–1.00 T",
            ha="center", va="center", color="#ffffff", fontsize=6.6, fontweight="bold", zorder=3)
    ax.text(x_te + w_te / 2.0, y_track_b + h_track / 2.0 - 1.4, "(20.0% Production Stream)",
            ha="center", va="center", color="#ffffff", fontsize=5.8, zorder=3)

    # =========================================================================
    # VERTICAL CAUSAL FIREWALLS (Staggered Badges to guarantee zero collision)
    # Barrier 1 at x = 59.4 (Upper y_badge = 58.2)
    # Barrier 2 at x = 68.8 (Lower y_badge = 54.0)
    # Barrier 3 at x = 78.2 (Upper y_badge = 58.2)
    # =========================================================================
    firewalls = [
        {"x": 59.4, "title": "Barrier 1: Freeze Model", "sub": "No Weight Updates", "y_badge": 58.2},
        {"x": 68.8, "title": "Barrier 2: Lock Cutoffs", "sub": "Fixed Thresholds", "y_badge": 54.0},
        {"x": 78.2, "title": "Barrier 3: Holdout Lock", "sub": "Zero Contamination", "y_badge": 58.2},
    ]

    for fw in firewalls:
        # Dashed line through tracks down to the badge
        ax.plot([fw["x"], fw["x"]], [fw["y_badge"] + 2.0, 88.0], color=COLOR_RISK, linestyle="--", linewidth=1.6, zorder=4)
        # Dedicated compact badge pill with plenty of horizontal & vertical clearance
        ax.add_patch(patches.FancyBboxPatch(
            (fw["x"] - 4.1, fw["y_badge"] - 1.9), 8.2, 3.8,
            boxstyle="round,pad=0.15,rounding_size=0.4",
            facecolor="#fee2e2", edgecolor=COLOR_RISK, lw=0.9, zorder=5
        ))
        ax.text(fw["x"], fw["y_badge"] + 0.45, fw["title"], ha="center", va="center",
                fontsize=5.1, fontweight="bold", color=COLOR_RISK, zorder=6)
        ax.text(fw["x"], fw["y_badge"] - 0.95, fw["sub"], ha="center", va="center",
                fontsize=4.4, color="#991b1b", zorder=6)

    # =========================================================================
    # FOUR ARCHITECTURAL SPECIFICATION CARDS (y = 11.5 to 51.5)
    # =========================================================================
    cards_data = [
        {
            "x": 3.0, "w": 22.3,
            "theme_bg": COLOR_INGEST_BG, "theme_border": COLOR_INGEST, "theme_header": COLOR_INGEST,
            "tag": "1. Training Split (60%)",
            "subtag": "Model Weights & Topology Learning",
            "items": [
                ("Historical Transactions", "Trains GNN message-passing weights."),
                ("Strict Past-Only Graph", "No future transaction edges visible."),
                ("GraphSMOTE Balance", "Synthetic mules confined to training."),
                ("Horizon Coverage", "Steps 1–30 | 0.00 to 0.60 T.")
            ]
        },
        {
            "x": 27.2, "w": 22.3,
            "theme_bg": COLOR_REVIEW_BG, "theme_border": COLOR_REVIEW, "theme_header": COLOR_REVIEW,
            "tag": "2. Validation Split (10%)",
            "subtag": "Hyperparameter & Cutoff Tuning",
            "items": [
                ("Checkpoint Selection", "50 Bayesian optimization trials."),
                ("Decision Threshold", "Calibrates operational cutoff."),
                ("Model Frozen", "Zero gradient or parameter tuning."),
                ("Horizon Coverage", "Steps 31–34 | 0.60 to 0.70 T.")
            ]
        },
        {
            "x": 51.4, "w": 22.3,
            "theme_bg": COLOR_GNN_BG, "theme_border": COLOR_GNN, "theme_header": COLOR_GNN,
            "tag": "3. Calibration Split (10%)",
            "subtag": "Finite Risk Control Calibration",
            "items": [
                ("Conformal Risk Control", "Computes finite error quantiles."),
                ("Statutory Guarantee", "Enforces 99.0% recall bound."),
                ("Disjoint Holdout", "Zero transaction overlap with train."),
                ("Horizon Coverage", "Steps 35–38 | 0.70 to 0.80 T.")
            ]
        },
        {
            "x": 75.6, "w": 22.3,
            "theme_bg": COLOR_SAFE_BG, "theme_border": COLOR_SAFE, "theme_header": COLOR_SAFE,
            "tag": "4. Forward Test Split (20%)",
            "subtag": "Unseen Production Streaming",
            "items": [
                ("Production Benchmark", "Evaluated across 5 random seeds."),
                ("Streaming SLA Test", "Simulates live core banking flow."),
                ("Pure Forward Pass", "Strict 1-pass forward inference."),
                ("Horizon Coverage", "Steps 39–49 | 0.80 to 1.00 T.")
            ]
        }
    ]

    card_y = 11.5
    card_h = 39.5
    hdr_h = 6.8

    for c in cards_data:
        # Card Body (Rounded for sleek publication finish)
        ax.add_patch(patches.FancyBboxPatch(
            (c["x"], card_y), c["w"], card_h,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor=c["theme_bg"], edgecolor=c["theme_border"], lw=1.2, zorder=2
        ))
        # Card Header Banner
        ax.add_patch(patches.Rectangle((c["x"], card_y + card_h - hdr_h), c["w"], hdr_h,
                                       facecolor=c["theme_header"], edgecolor="none", zorder=3))
        ax.text(c["x"] + c["w"] / 2.0, card_y + card_h - 2.2, c["tag"],
                ha="center", va="center", color="#ffffff", fontsize=7.2, fontweight="bold", zorder=4)
        ax.text(c["x"] + c["w"] / 2.0, card_y + card_h - 4.8, c["subtag"],
                ha="center", va="center", color="#ffffff", fontsize=5.8, zorder=4)

        # Bullets inside Card (Short strings with plenty of margins)
        y_start = card_y + card_h - hdr_h - 3.8
        dy_bullet = 7.4
        for bi, (title_text, body_text) in enumerate(c["items"]):
            item_y = y_start - bi * dy_bullet
            ax.plot([c["x"] + 1.2], [item_y], marker="o", markersize=3.0, color=c["theme_header"], zorder=4)
            ax.text(c["x"] + 2.4, item_y + 1.3, title_text, ha="left", va="center",
                    fontsize=6.4, fontweight="bold", color=COLOR_DARK, zorder=4)
            ax.text(c["x"] + 2.4, item_y - 1.5, body_text, ha="left", va="center",
                    fontsize=5.6, color=COLOR_MUTED, zorder=4)

    # =========================================================================
    # BOTTOM METHODOLOGICAL GUARANTEE BANNER (y = 2.0 to 9.2)
    # =========================================================================
    ax.add_patch(patches.FancyBboxPatch(
        (1.5, 2.0), 97.0, 7.2,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0, zorder=2
    ))
    ax.text(50.0, 6.4, "METHODOLOGICAL RIGOR: Zero-Leakage Guarantee Across All 14 Financial Transaction Networks",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK, zorder=3)
    ax.text(50.0, 3.8, "Future transactions are strictly partitioned behind causal firewalls, eliminating lookahead bias, graph leakage, and conformal contamination.",
            ha="center", va="center", fontsize=6.4, color=COLOR_MUTED, zorder=3)

    # Save to all target figure repositories
    save_figure(fig, "fig_temporal_split", pad_inches=0.12)
    save_figure(fig, "fig14_temporal_split", pad_inches=0.12)
    plt.close(fig)


if __name__ == "__main__":
    generate()
