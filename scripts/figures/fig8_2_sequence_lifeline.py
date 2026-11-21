"""
Figure 8.2: Real-Time Operational UML Sequence Lifeline
Standalone publication script for C-STGB monograph.
Fixes all text overlapping between lifeline actors and message arrows with compact 2-line badges.
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
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(12.0, 6.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Canvas Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#ffffff', edgecolor='none'))

    # Top Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor='none'
    ))
    ax.text(3.0, 96.6, 'REAL-TIME OPERATIONAL SEQUENCE LIFELINE & EXECUTION TRACE',
            ha='left', va='center', fontsize=9.6, fontweight='bold', color='#ffffff')
    ax.text(3.0, 94.2, 'Deterministic In-Flight Pipeline: Ingress -> Cache -> Neural Forward Pass -> Conformal Triage -> Merkle WORM',
            ha='left', va='center', fontsize=7.2, color='#94a3b8')

    # Top Right SLA Badge
    ax.add_patch(patches.Rectangle(
        (75.5, 93.3), 22.0, 4.8,
        facecolor='#065f46', edgecolor='#10b981', linewidth=1.0
    ))
    ax.text(86.5, 95.7, 'FAST-PATH: 0.45 ms (SLA < 10 ms)',
            ha='center', va='center', fontsize=6.8, fontweight='bold', color='#ecfdf5')

    # 6 Lifeline Actors
    actors = [
        {"name": "Core Banking", "sub": "ISO 20022 Webhook", "x": 8.5, "col": COLOR_DARK, "bg": "#f8fafc"},
        {"name": "FastAPI Gateway", "sub": "Async Event Worker", "x": 25.0, "col": COLOR_INGEST, "bg": COLOR_INGEST_BG},
        {"name": "DuckDB Cache", "sub": "Zero-Copy Arrow", "x": 41.5, "col": COLOR_GNN, "bg": COLOR_GNN_BG},
        {"name": "C-STGB Neural Pod", "sub": "TorchScript GNN", "x": 58.5, "col": "#ea580c", "bg": "#fff7ed"},
        {"name": "Conformal Arbiter", "sub": "Class-Cond. CRC", "x": 75.5, "col": "#7c3aed", "bg": "#faf5ff"},
        {"name": "WORM Vault", "sub": "SHA-256 S3 Lock", "x": 92.0, "col": COLOR_SAFE, "bg": COLOR_SAFE_BG},
    ]

    header_y = 83.5
    header_h = 7.0
    header_w = 14.8
    lifeline_bottom_y = 6.0

    # Draw Actor Headers and Vertical Lifelines
    for act in actors:
        lx = act["x"]
        # Lifeline dotted vertical line
        ax.plot([lx, lx], [lifeline_bottom_y, header_y], color='#94a3b8', linestyle=':', lw=1.2, zorder=2)
        
        # Header Box
        ax.add_patch(patches.Rectangle(
            (lx - header_w/2, header_y), header_w, header_h,
            facecolor=act["bg"], edgecolor=act["col"], linewidth=1.3, zorder=4
        ))
        ax.add_patch(patches.Rectangle(
            (lx - header_w/2, header_y + header_h - 2.2), header_w, 2.2,
            facecolor=act["col"], edgecolor="none", zorder=5
        ))
        ax.text(lx, header_y + header_h - 4.2, act["name"],
                ha='center', va='center', fontsize=7.2, fontweight='bold', color=COLOR_DARK, zorder=6)
        ax.text(lx, header_y + 1.6, act["sub"],
                ha='center', va='center', fontsize=6.2, color=COLOR_MUTED, zorder=6)

    # =========================================================================
    # PHASE 1 FRAME: SYNCHRONOUS FAST-PATH (y: 37.0 to 82.0)
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (2.0, 37.0), 96.0, 45.0,
        facecolor='#f0fdf4', edgecolor=COLOR_SAFE, linewidth=1.2, linestyle='-', zorder=1
    ))
    ax.add_patch(patches.Rectangle(
        (2.0, 79.0), 45.0, 3.0,
        facecolor=COLOR_SAFE, edgecolor='none', zorder=2
    ))
    ax.text(3.5, 80.5, "SYNCHRONOUS IN-FLIGHT FAST PATH (< 0.45 ms SLA)",
            ha='left', va='center', fontsize=7.2, fontweight='bold', color='#ffffff', zorder=3)
    ax.text(96.0, 80.5, "22.2x Safety Margin vs 10 ms Banking SLA",
            ha='right', va='center', fontsize=6.8, fontweight='bold', color='#15803d', zorder=3)

    # Sync Messages (Numbered 1 to 6)
    # Formatted with clean 2-line labels to guarantee zero overlap across lifelines
    sync_msgs = [
        {
            "y": 74.0, "x1": 8.5, "x2": 25.0,
            "title": "1. POST /inference/score",
            "sub": "ISO 20022 Webhook Ingest",
            "col": COLOR_DARK
        },
        {
            "y": 67.0, "x1": 25.0, "x2": 41.5,
            "title": "2. Query Ego-Graph Cache",
            "sub": "DuckDB Zero-Copy Arrow",
            "col": COLOR_INGEST
        },
        {
            "y": 60.0, "x1": 41.5, "x2": 58.5,
            "title": "3. Arrow Tensor Stream",
            "sub": "< 0.12 ms IPC Transport",
            "col": COLOR_GNN
        },
        {
            "y": 53.0, "x1": 58.5, "x2": 75.5,
            "title": "4. Forward Pass & Edge Gating",
            "sub": "< 0.28 ms C-STGB Inference",
            "col": "#ea580c"
        },
        {
            "y": 46.0, "x1": 75.5, "x2": 25.0,
            "title": "5. Calibrated CRC Prediction Set",
            "sub": "{0} Safe · {0,1} Review · {1} Quarantine",
            "col": "#7c3aed"
        },
        {
            "y": 39.5, "x1": 25.0, "x2": 8.5,
            "title": "6. Return Decision (HTTP 200)",
            "sub": "STP Clear / Review / Quarantine",
            "col": COLOR_SAFE
        },
    ]

    for m in sync_msgs:
        y, x1, x2 = m["y"], m["x1"], m["x2"]
        # Draw Arrow
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle="-|>", lw=1.6, color=m["col"], mutation_scale=10),
            zorder=4
        )
        mid_x = (x1 + x2) / 2.0
        label_text = f"{m['title']}\n{m['sub']}"
        ax.text(
            mid_x, y + 1.2, label_text,
            ha="center", va="bottom",
            fontsize=6.2, fontweight="bold", color=m["col"], linespacing=1.15,
            bbox=dict(boxstyle="round,pad=0.22", fc="#ffffff", ec=m["col"], lw=0.75, alpha=0.96),
            zorder=6
        )

    # =========================================================================
    # PHASE 2 FRAME: ASYNCHRONOUS TIER-1/2 SWARM & WORM AUDIT (y: 8.0 to 35.0)
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (2.0, 8.0), 96.0, 27.0,
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=1.2, linestyle='--', zorder=1
    ))
    ax.add_patch(patches.Rectangle(
        (2.0, 32.0), 52.0, 3.0,
        facecolor='#ca8a04', edgecolor='none', zorder=2
    ))
    ax.text(3.5, 33.5, "ASYNCHRONOUS SWARM FORENSICS & WORM AUDIT (TIER 1 & 2)",
            ha='left', va='center', fontsize=7.2, fontweight='bold', color='#ffffff', zorder=3)
    ax.text(96.0, 33.5, "Non-blocking background queue | Zero core banking impact",
            ha='right', va='center', fontsize=6.8, fontweight='bold', color='#854d0e', zorder=3)

    # Async Messages (Numbered 7 to 9)
    async_msgs = [
        {
            "y": 25.5, "x1": 25.0, "x2": 58.5,
            "title": "7. Async Dispatch to Forensic Queue",
            "sub": "High-Risk Tier-1/2 Ambiguous Events",
            "col": '#b45309'
        },
        {
            "y": 19.0, "x1": 58.5, "x2": 75.5,
            "title": "8. 4-Agent Forensic LLM Swarm",
            "sub": "Generates Certified SAR Dossier",
            "col": '#b45309'
        },
        {
            "y": 12.5, "x1": 75.5, "x2": 92.0,
            "title": "9. Seal Immutable Audit Record",
            "sub": "SHA-256 Merkle Leaf in WORM Vault",
            "col": COLOR_SAFE
        },
    ]

    for m in async_msgs:
        y, x1, x2 = m["y"], m["x1"], m["x2"]
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle="-|>", lw=1.6, color=m["col"], linestyle="--", mutation_scale=10),
            zorder=4
        )
        mid_x = (x1 + x2) / 2.0
        label_text = f"{m['title']}\n{m['sub']}"
        ax.text(
            mid_x, y + 1.2, label_text,
            ha="center", va="bottom",
            fontsize=6.2, fontweight="bold", color=m["col"], linespacing=1.15,
            bbox=dict(boxstyle="round,pad=0.22", fc="#ffffff", ec=m["col"], lw=0.75, alpha=0.96),
            zorder=6
        )

    # Bottom Takeaway Ribbon
    ax.add_patch(patches.Rectangle(
        (1.5, 1.0), 97.0, 4.8,
        facecolor=COLOR_DARK, edgecolor='none'
    ))
    ax.text(50.0, 3.4, "EXECUTION RIGOR: In-flight transactions are cleared in 0.45 ms; deep multi-agent SAR drafting runs asynchronously.",
            ha="center", va="center", fontsize=7.0, fontweight="bold", color="#38bdf8")

    save_figure(fig, "fig8_2_uml_sequence_lifeline", pad_inches=0.10)
    save_figure(fig, "fig20_sequence_lifeline", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
