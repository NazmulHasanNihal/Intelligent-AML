"""
Figure 8.2: Real-Time Operational UML Sequence Lifeline
Redesigned with reduced text, large legible fonts (>= 7.0pt), and a clean, intuitive 2-phase sequence.
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
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor='#ffffff', edgecolor='none'))

    # Top Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor='none'
    ))
    ax.text(2.8, 96.5, 'REAL-TIME OPERATIONAL SEQUENCE LIFELINE & EXECUTION TRACE',
            ha='left', va='center', fontsize=9.8, fontweight='bold', color='#ffffff')
    ax.text(2.8, 94.0, 'Deterministic In-Flight Pipeline: Ingress -> Cache -> Neural Forward Pass -> Conformal Triage -> Merkle WORM',
            ha='left', va='center', fontsize=7.2, color='#94a3b8')

    # Top Right SLA Badge
    ax.add_patch(patches.Rectangle(
        (76.0, 93.2), 22.0, 5.0,
        facecolor='#065f46', edgecolor='#10b981', linewidth=1.0
    ))
    ax.text(87.0, 95.7, 'FAST-PATH: 0.45 ms (SLA < 10 ms)',
            ha='center', va='center', fontsize=6.8, fontweight='bold', color='#ecfdf5')

    # 6 Lifeline Actors
    actors = [
        {"name": "Core Banking", "sub": "ISO 20022 Webhook", "x": 9.0, "col": COLOR_DARK, "bg": "#f8fafc"},
        {"name": "FastAPI Gateway", "sub": "Async Event Worker", "x": 25.5, "col": COLOR_INGEST, "bg": COLOR_INGEST_BG},
        {"name": "DuckDB Cache", "sub": "Zero-Copy Arrow", "x": 42.0, "col": COLOR_GNN, "bg": COLOR_GNN_BG},
        {"name": "C-STGB Neural Pod", "sub": "TorchScript GNN", "x": 58.5, "col": "#ea580c", "bg": "#fff7ed"},
        {"name": "Conformal Arbiter", "sub": "Class-Cond. CRC", "x": 75.0, "col": "#7c3aed", "bg": "#faf5ff"},
        {"name": "WORM Vault", "sub": "SHA-256 S3 Lock", "x": 91.5, "col": COLOR_SAFE, "bg": COLOR_SAFE_BG},
    ]

    header_y = 83.5
    header_h = 7.0
    header_w = 14.5
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
    # PHASE 1 FRAME: SYNCHRONOUS FAST-PATH (y: 38.0 to 81.5)
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (2.0, 38.0), 96.0, 43.5,
        facecolor='#f0fdf4', edgecolor=COLOR_SAFE, linewidth=1.2, linestyle='-', zorder=1
    ))
    ax.add_patch(patches.Rectangle(
        (2.0, 78.5), 45.0, 3.0,
        facecolor=COLOR_SAFE, edgecolor='none', zorder=2
    ))
    ax.text(3.5, 80.0, "SYNCHRONOUS IN-FLIGHT FAST PATH (< 0.45 ms SLA)",
            ha='left', va='center', fontsize=7.2, fontweight='bold', color='#ffffff', zorder=3)
    ax.text(96.0, 80.0, "22.2x Safety Margin vs 10 ms Banking SLA",
            ha='right', va='center', fontsize=6.8, fontweight='bold', color='#15803d', zorder=3)

    # Sync Messages (Numbered 1 to 6)
    sync_msgs = [
        {"y": 74.0, "x1": 9.0, "x2": 25.5, "txt": "1. POST /v1/transactions (ISO 20022)", "col": COLOR_DARK},
        {"y": 67.0, "x1": 25.5, "x2": 42.0, "txt": "2. Query 2-Hop Historical Subgraph", "col": COLOR_INGEST},
        {"y": 60.0, "x1": 42.0, "x2": 58.5, "txt": "3. Zero-Copy Arrow Tensor Stream (<0.12 ms)", "col": COLOR_GNN},
        {"y": 53.0, "x1": 58.5, "x2": 75.0, "txt": "4. Forward Pass & Edge-Trust Gating (<0.28 ms)", "col": "#ea580c"},
        {"y": 46.0, "x1": 75.0, "x2": 25.5, "txt": "5. CRC Prediction Set: {0} Safe vs {1} Quarantined", "col": "#7c3aed"},
        {"y": 40.0, "x1": 25.5, "x2": 9.0, "txt": "6. Return Decision (HTTP 200 STP Clear / Quarantine)", "col": COLOR_SAFE},
    ]

    for m in sync_msgs:
        y, x1, x2 = m["y"], m["x1"], m["x2"]
        # Draw Arrow
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color=m["col"], mutation_scale=10), zorder=4)
        # Message Label with white background pill
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.8, m["txt"], ha="center", va="bottom",
                fontsize=6.8, fontweight="bold", color=m["col"],
                bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=m["col"], lw=0.8), zorder=5)

    # =========================================================================
    # PHASE 2 FRAME: ASYNCHRONOUS TIER-1/2 SWARM & WORM AUDIT (y: 8.0 to 35.5)
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (2.0, 8.0), 96.0, 27.5,
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=1.2, linestyle='--', zorder=1
    ))
    ax.add_patch(patches.Rectangle(
        (2.0, 32.5), 52.0, 3.0,
        facecolor='#ca8a04', edgecolor='none', zorder=2
    ))
    ax.text(3.5, 34.0, "ASYNCHRONOUS SWARM FORENSICS & WORM AUDIT (TIER 1 & 2)",
            ha='left', va='center', fontsize=7.2, fontweight='bold', color='#ffffff', zorder=3)
    ax.text(96.0, 34.0, "Non-blocking background queue | Zero core banking impact",
            ha='right', va='center', fontsize=6.8, fontweight='bold', color='#854d0e', zorder=3)

    # Async Messages (Numbered 7 to 9)
    async_msgs = [
        {"y": 26.5, "x1": 25.5, "x2": 58.5, "txt": "7. Async Dispatch: High-Risk Alert to Forensic Queue", "col": '#b45309'},
        {"y": 19.5, "x1": 58.5, "x2": 75.0, "txt": "8. 4-Agent LLM Swarm Generates Certified SAR Dossier", "col": '#b45309'},
        {"y": 12.5, "x1": 75.0, "x2": 91.5, "txt": "9. Seal SHA-256 Merkle Leaf in Immutable S3 WORM Vault", "col": COLOR_SAFE},
    ]

    for m in async_msgs:
        y, x1, x2 = m["y"], m["x1"], m["x2"]
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color=m["col"], linestyle="--", mutation_scale=10), zorder=4)
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.8, m["txt"], ha="center", va="bottom",
                fontsize=6.8, fontweight="bold", color=m["col"],
                bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=m["col"], lw=0.8), zorder=5)

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
