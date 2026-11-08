"""
Figure 3.1: End-to-End Architectural Dataflow of C-STGB
Standard 6-Module Publication-Grade Visual Pipeline.
High-tech tensor contract architecture cards, perfectly fitted inter-module labels, and zero crude doodles.
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
    fig, ax = plt.subplots(figsize=(13.6, 5.4), dpi=300)
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
    ax.text(50.0, 96.5, "C-STGB: END-TO-END ARCHITECTURAL DATAFLOW & TENSOR TRANSFORMATION PIPELINE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 94.0, "Six Canonical Modules: Multi-Rail Ingestion -> Continuous Encoder -> Edge Gating -> SMOTE -> Bayes Calibration -> CRC Triage",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # Module Layout Parameters: 6 Large Structured Blocks
    modules = [
        {
            "num": "MODULE 1",
            "title": "Data Ingestion",
            "spec": "Tensor: [B, 12] RecordBatches",
            "border": COLOR_INGEST,
            "header_bg": COLOR_INGEST,
            "bg": COLOR_INGEST_BG,
            "items": [
                "Zero-Copy Arrow Memory",
                "DuckDB 2-Hop Aggregation",
                "Multi-Rail Ledger Ingestion"
            ],
            "sla": "Inference: <0.05 ms"
        },
        {
            "num": "MODULE 2",
            "title": "Continuous Encoder",
            "spec": "Tensor: [B, T, 64] Harmonic",
            "border": COLOR_GNN,
            "header_bg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "items": [
                "3-Band Temporal Waveforms",
                "Hawkes Point Process Decay",
                "Causal Sequence Integrity"
            ],
            "sla": "Inference: <0.08 ms"
        },
        {
            "num": "MODULE 3",
            "title": "Edge-Trust Gating",
            "spec": "Weights: [E, 1] Trust Gate",
            "border": COLOR_GNN,
            "header_bg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "items": [
                "Camouflage Noise Filter",
                "Soft Pruning Threshold",
                "Dirichlet Energy Retention"
            ],
            "sla": "Inference: <0.06 ms"
        },
        {
            "num": "MODULE 4",
            "title": "Latent SMOTE",
            "spec": "Manifold: [K, d] Balanced",
            "border": COLOR_GNN_PURPLE,
            "header_bg": COLOR_GNN_PURPLE,
            "bg": "#faf5ff",
            "items": [
                "Typology Subgraph Clustering",
                "Bilinear Edge Interpolation",
                "Extreme Skew Rectification"
            ],
            "sla": "Offline Pre-Trained"
        },
        {
            "num": "MODULE 5",
            "title": "Bayes Risk Head",
            "spec": "Estimates: [B, 2] Risk Vector",
            "border": COLOR_REVIEW,
            "header_bg": COLOR_REVIEW,
            "bg": COLOR_REVIEW_BG,
            "items": [
                "Asymmetric Loss Head",
                "Evidence-Adaptive Fusion",
                "Cost-Sensitive Cutoffs"
            ],
            "sla": "Inference: <0.04 ms"
        },
        {
            "num": "MODULE 6",
            "title": "Conformal Triage",
            "spec": "Routing: 99.33% STP",
            "border": COLOR_SAFE,
            "header_bg": COLOR_SAFE,
            "bg": COLOR_SAFE_BG,
            "items": [
                "Class-Conditional CRC",
                "Tier-1 Sub-Second Freeze",
                "Assisted SAR Dossier"
            ],
            "sla": "Inference: <0.14 ms"
        }
    ]

    card_w = 14.2
    gap_w = 2.4
    x_start = 1.5
    card_y = 17.0
    card_h = 71.0
    hdr_h = 8.5

    for i, m in enumerate(modules):
        cx = x_start + i * (card_w + gap_w)

        # Outer Card
        ax.add_patch(patches.Rectangle((cx, card_y), card_w, card_h, facecolor=m["bg"], edgecolor=m["border"], lw=1.4))

        # Header Banner
        ax.add_patch(patches.Rectangle((cx, card_y + card_h - hdr_h), card_w, hdr_h, facecolor=m["header_bg"], edgecolor="none"))
        ax.text(cx + card_w/2, card_y + card_h - 2.8, m["num"], ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
        ax.text(cx + card_w/2, card_y + card_h - 5.8, m["title"], ha="center", va="center", fontsize=7.4, fontweight="bold", color="#ffffff")

        # Tensor Contract Pill
        ax.add_patch(patches.Rectangle((cx + 1.0, card_y + card_h - hdr_h - 6.2), card_w - 2.0, 5.2,
                                       facecolor="#ffffff", edgecolor=m["border"], lw=0.9))
        ax.text(cx + card_w/2, card_y + card_h - hdr_h - 3.6, m["spec"],
                ha="center", va="center", fontsize=6.0, fontweight="bold", color=m["border"])

        # 3 Structured Detail Items
        item_y_start = card_y + card_h - hdr_h - 14.5
        dy = 13.0
        for ii, itxt in enumerate(m["items"]):
            iy = item_y_start - ii * dy
            ax.add_patch(patches.Rectangle((cx + 1.0, iy - 4.5), card_w - 2.0, 10.5,
                                           facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.7))
            ax.plot([cx + 2.2], [iy], marker="s", markersize=3.0, color=m["header_bg"])
            ax.text(cx + 3.4, iy, itxt, ha="left", va="center", fontsize=6.0, color=COLOR_DARK, fontweight="normal")

        # Bottom SLA Badge
        ax.add_patch(patches.Rectangle((cx + 1.0, card_y + 1.8), card_w - 2.0, 5.2,
                                       facecolor="#ffffff", edgecolor=m["border"], lw=0.9))
        ax.text(cx + card_w/2, card_y + 4.4, m["sla"],
                ha="center", va="center", fontsize=6.4, fontweight="bold", color=m["border"])

        # Clean Inter-Module Connector Arrow
        if i < len(modules) - 1:
            arr_x1 = cx + card_w
            arr_x2 = arr_x1 + gap_w
            ax.annotate("", xy=(arr_x2, 52.5), xytext=(arr_x1, 52.5),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLOR_DARK, mutation_scale=10), zorder=5)

    # Bottom Architectural Specification Summary Callout
    ax.add_patch(patches.Rectangle(
        (1.5, 2.5), 97.0, 11.0,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.1
    ))
    ax.text(50.0, 10.5, "DATA TRANSFORMATION PIPELINE: Guaranteed Microsecond Latency with High Statistical Rigor",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=COLOR_DARK)
    ax.text(50.0, 7.2, "Raw ISO 20022 events undergo continuous-time harmonic encoding and edge-trust gating before class-conditional triage.",
            ha="center", va="center", fontsize=6.8, color="#334155")
    ax.text(50.0, 4.4, "Total end-to-end forward execution takes 0.45 ms, enabling 99.33% straight-through processing at 31,250 tx/s burst rate.",
            ha="center", va="center", fontsize=6.8, color="#334155")

    save_figure(fig, "fig3_1_tensor_flow", pad_inches=0.10)
    save_figure(fig, "fig13_tensor_flow", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
