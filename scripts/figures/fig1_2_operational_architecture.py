"""
Figure 1.2 / 1.3: C-STGB Operational Architecture and Real-Time Conformal Triage Dataflow
Standard 6-Module Publication-Grade Architecture Pipeline.
Sleek, high-tech architectural design with clean tensor specifications, generous spacing, and zero crude doodles.
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
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(13.2, 5.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Title Banner (Dark Slate Blue)
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(50.0, 96.5, "C-STGB: REAL-TIME FINANCIAL SURVEILLANCE & CONFORMAL TRIAGE ARCHITECTURE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 94.0, "End-to-End Enterprise Flow: Ingestion -> Invariant Engine -> GNN Core -> Latent Resampler -> Bayes Tuner -> CRC Triage",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # Module Specifications: Exactly 6 Large Blocks Left-to-Right
    modules = [
        {
            "id": "MODULE 1",
            "title": "Data Ingestion",
            "spec": "Arrow Record Batches",
            "fc": COLOR_INGEST_BG, "ec": COLOR_INGEST, "tc": COLOR_INGEST,
            "items": ["Zero-Copy In-Memory Buffer", "Sub-ms DuckDB Aggregations", "ISO 20022 Multi-Rail Normalizer"],
            "sla": "SLA: < 0.05 ms"
        },
        {
            "id": "MODULE 2",
            "title": "Invariant Engine",
            "spec": "12-D Mass-Flow Vector",
            "fc": COLOR_GNN_BG, "ec": COLOR_GNN, "tc": COLOR_GNN,
            "items": ["Conservation Hydrodynamics", "Hawkes Point Process Burst", "Cold-Start Tabular Gating"],
            "sla": "SLA: < 0.07 ms"
        },
        {
            "id": "MODULE 3",
            "title": "GNN Core",
            "spec": "Harmonic Continuous Time",
            "fc": "#faf5ff", "ec": COLOR_GNN_PURPLE, "tc": COLOR_GNN_PURPLE,
            "items": ["3-Band Temporal Attention", "Learnable Edge-Trust Gating", "65.9% Camouflage Chaff Pruned"],
            "sla": "SLA: < 0.16 ms"
        },
        {
            "id": "MODULE 4",
            "title": "Latent SMOTE",
            "spec": "Typology Manifold Synthesis",
            "fc": "#fffbeb", "ec": "#d97706", "tc": "#d97706",
            "items": ["K-Means Latent Clustering", "Edge-Preserving Interpolation", "Extreme Skew Rectification"],
            "sla": "Offline Train"
        },
        {
            "id": "MODULE 5",
            "title": "Bayes Tuner",
            "spec": "Asymmetric Cost Head",
            "fc": COLOR_REVIEW_BG, "ec": COLOR_REVIEW, "tc": COLOR_REVIEW,
            "items": ["Utility Matrix Optimization", "Cost-Sensitive Bayes Cutoff", "DKW Bounded Non-Stationarity"],
            "sla": "SLA: < 0.04 ms"
        },
        {
            "id": "MODULE 6",
            "title": "CRC Triage",
            "spec": "Finite Statistical Guarantee",
            "fc": COLOR_SAFE_BG, "ec": COLOR_SAFE, "tc": COLOR_SAFE,
            "items": ["99.33% Straight-Through Flow", "Tier-1 Real-Time Quarantine", "Assisted SAR Dossier Desk"],
            "sla": "SLA: < 0.13 ms"
        }
    ]

    card_w = 14.4
    gap = 2.1
    x_start = 1.5
    card_y = 17.0
    card_h = 71.0
    hdr_h = 8.5

    for i, m in enumerate(modules):
        cx = x_start + i * (card_w + gap)
        
        # Outer Card
        ax.add_patch(patches.Rectangle((cx, card_y), card_w, card_h, facecolor=m["fc"], edgecolor=m["ec"], lw=1.4))
        
        # Header Banner
        ax.add_patch(patches.Rectangle((cx, card_y + card_h - hdr_h), card_w, hdr_h, facecolor=m["ec"], edgecolor="none"))
        ax.text(cx + card_w/2, card_y + card_h - 2.8, m["id"], ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
        ax.text(cx + card_w/2, card_y + card_h - 5.8, m["title"], ha="center", va="center", fontsize=7.4, fontweight="bold", color="#ffffff")

        # Technical Spec Pill
        ax.add_patch(patches.Rectangle((cx + 0.8, card_y + card_h - hdr_h - 6.2), card_w - 1.6, 5.2,
                                       facecolor="#ffffff", edgecolor=m["ec"], lw=0.9))
        ax.text(cx + card_w/2, card_y + card_h - hdr_h - 3.6, m["spec"],
                ha="center", va="center", fontsize=6.2, fontweight="bold", color=m["tc"])

        # 3 Structured Detail Items (widened sub-box and optimized 5.5pt typography)
        item_y_start = card_y + card_h - hdr_h - 14.5
        dy = 13.0
        for ii, itxt in enumerate(m["items"]):
            iy = item_y_start - ii * dy
            sub_w = card_w - 1.4
            ax.add_patch(patches.Rectangle((cx + 0.7, iy - 4.5), sub_w, 10.5,
                                           facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.7))
            ax.plot([cx + 1.8], [iy], marker="o", markersize=2.6, color=m["ec"])
            ax.text(cx + 2.7, iy, itxt, ha="left", va="center", fontsize=5.5, color=COLOR_DARK, fontweight="normal")

        # Bottom SLA Badge
        ax.add_patch(patches.Rectangle((cx + 0.8, card_y + 1.8), card_w - 1.6, 5.2,
                                       facecolor="#ffffff", edgecolor=m["ec"], lw=0.9))
        ax.text(cx + card_w/2, card_y + 4.4, m["sla"],
                ha="center", va="center", fontsize=6.4, fontweight="bold", color=m["tc"])

        # Connector Arrow to Next Module
        if i < len(modules) - 1:
            arr_x1 = cx + card_w
            arr_x2 = arr_x1 + gap
            ax.annotate("", xy=(arr_x2, 52.5), xytext=(arr_x1, 52.5),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLOR_DARK, mutation_scale=10), zorder=5)

    # Bottom Architectural Specification Summary Callout
    ax.add_patch(patches.Rectangle(
        (1.5, 2.5), 97.0, 11.0,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.1
    ))
    ax.text(50.0, 10.5, "ARCHITECTURAL GUARANTEE: High-Velocity Stream Ingestion with Sub-Millisecond Conformal Triage",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(50.0, 7.2, "End-to-end forward-pass execution latency totals 0.45 ms (22.2x faster than 10.0 ms enterprise banking SLA).",
            ha="center", va="center", fontsize=6.8, color="#334155")
    ax.text(50.0, 4.4, "Class-conditional Conformal Risk Control delivers rigorous 99.0% statistical coverage on extreme minority money laundering flows.",
            ha="center", va="center", fontsize=6.8, color="#334155")

    save_figure(fig, "fig1_operational_architecture_flowchart", pad_inches=0.10)
    save_figure(fig, "fig1_2_operational_architecture", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
