"""
Figure 6.1: Multi-Agent Forensic Reasoning and Dual-Governance Pipeline
Redesigned as an authoritative 4-Horizontal-Swimlane Diagram:
Lanes for Coordinator, Specialist, Drafter, and Verifier agents with avatar circles,
step-by-step alert progression arrows, simplified Grammar/Schema validation blocks,
and zero raw EBNF / Pydantic code clutter.
All inter-lane arrows routed cleanly through gutters to guarantee zero collision with text or action blocks.
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
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_LIGHT, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE_LIGHT,
    COLOR_RISK, COLOR_RISK_BG, COLOR_RISK_LIGHT,
    COLOR_REVIEW, COLOR_REVIEW_BG, COLOR_REVIEW_LIGHT,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def draw_agent_avatar(ax, cx, cy, radius, color, label, role_title):
    """Draws an agent avatar circle with role header and label."""
    # Outer halo
    ax.add_patch(patches.Circle((cx, cy), radius + 0.005, facecolor="none", edgecolor=color, lw=1.2, linestyle=":"))
    # Agent circle
    ax.add_patch(patches.Circle((cx, cy), radius, facecolor=color, edgecolor=COLOR_DARK, lw=1.3))
    # Head & shoulders stylized avatar
    head_r = radius * 0.35
    ax.add_patch(patches.Circle((cx, cy + radius*0.25), head_r, facecolor="#ffffff", edgecolor="none"))
    # Shoulders arc
    ax.add_patch(patches.Arc((cx, cy - radius*0.35), radius*1.15, radius*0.9, theta1=0, theta2=180,
                             facecolor="#ffffff", edgecolor="#ffffff", lw=2.0))
    # Title badge below
    ax.text(cx, cy - radius - 0.024, label, ha="center", va="center",
            fontsize=7.2, fontweight="bold", color=COLOR_DARK)
    ax.text(cx, cy - radius - 0.046, role_title, ha="center", va="center",
            fontsize=6.0, color=COLOR_MUTED)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous widescreen canvas for 4 swimlanes with ample gutter room
    fig, ax = plt.subplots(figsize=(11.5, 6.4), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (0.015, 0.930), 0.970, 0.060,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.966, "MULTI-AGENT FORENSIC INVESTIGATION & DUAL-GOVERNANCE WORKFLOW",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.944, "Four-Lane Autonomous Swarm: Ingestion -> Typology Attribution -> Narrative Drafting -> Deterministic Audit",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # 4 HORIZONTAL SWIMLANES with generous 0.030 gutters
    lane_h = 0.190
    lanes = [
        {
            "y": 0.715, "name": "LANE 1",
            "agent": "Coordinator Agent", "role": "Swarm Orchestrator", "color": COLOR_INGEST, "bg": COLOR_INGEST_BG,
            "blocks": [
                {"title": "Conformal Alert Ingress", "desc": "Receives Tier 2 CRC set\nTriggers <15 min SLA clock", "col": COLOR_RISK, "bg": COLOR_RISK_BG, "x": 0.22, "w": 0.21},
                {"title": "DuckDB Graph Hydration", "desc": "Hydrates 2-hop subgraphs\nExtracts 12-D invariants", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.48, "w": 0.22},
                {"title": "Swarm Task Dispatch", "desc": "Partitions evidence tasks\nMonitors agent deadlines", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.75, "w": 0.21}
            ]
        },
        {
            "y": 0.490, "name": "LANE 2",
            "agent": "Specialist Agent", "role": "Typology Detective", "color": COLOR_GNN, "bg": COLOR_GNN_BG,
            "blocks": [
                {"title": "Smurfing & Wash Cycle Trace", "desc": "Identifies circular flow patterns\nTracks Hawkes burst acceleration", "col": COLOR_GNN, "bg": "#ffffff", "x": 0.28, "w": 0.29},
                {"title": "Causal Taint Attribution", "desc": "Computes forward & backward reach\nQuantifies illicit capital retention", "col": COLOR_GNN, "bg": "#ffffff", "x": 0.63, "w": 0.29}
            ]
        },
        {
            "y": 0.265, "name": "LANE 3",
            "agent": "Drafter Agent", "role": "SAR Dossier Author", "color": COLOR_GNN_PURPLE, "bg": "#FAF5FF",
            "blocks": [
                {"title": "Case Narrative Assembly", "desc": "Compiles suspect timeline\nCorrelates evidence patterns", "col": COLOR_GNN_PURPLE, "bg": "#ffffff", "x": 0.28, "w": 0.29},
                {"title": "FinCEN Form 111 Structure", "desc": "Structured narrative sections\nZero-temperature deterministic", "col": COLOR_GNN_PURPLE, "bg": "#ffffff", "x": 0.63, "w": 0.29}
            ]
        },
        {
            "y": 0.040, "name": "LANE 4",
            "agent": "Verifier Agent", "role": "Audit & Compliance Officer", "color": COLOR_SAFE, "bg": COLOR_SAFE_BG,
            "blocks": [
                {"title": "Grammar Check", "desc": "Strict token lexical check\nEliminates hallucinations", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.22, "w": 0.17},
                {"title": "Schema Check", "desc": "Account continuity verify\nValidates financial sums", "col": COLOR_REVIEW, "bg": "#ffffff", "x": 0.41, "w": 0.17},
                {"title": "4-Eyes Approval", "desc": "Human compliance sign-off\nSenior analyst decision", "col": COLOR_SAFE, "bg": "#ffffff", "x": 0.60, "w": 0.17},
                {"title": "Cryptographic Seal", "desc": "SHA-256 Merkle Audit Root\nImmutable Court Record", "col": COLOR_DARK, "bg": "#ffffff", "x": 0.79, "w": 0.18}
            ]
        }
    ]

    for idx, lane in enumerate(lanes):
        ly = lane["y"]
        # Lane container
        ax.add_patch(patches.Rectangle(
            (0.015, ly), 0.970, lane_h,
            facecolor=lane["bg"], edgecolor=COLOR_BORDER, lw=1.0
        ))
        # Left Lane Header Strip (widened to 0.030, clean, non-overlapping label)
        strip_w = 0.028
        ax.add_patch(patches.Rectangle(
            (0.015, ly), strip_w, lane_h,
            facecolor=lane["color"], edgecolor="none"
        ))
        ax.text(0.015 + strip_w/2, ly + lane_h/2, lane["name"],
                ha="center", va="center", rotation=90, fontsize=6.8, fontweight="bold", color="#ffffff")

        # Agent Avatar Circle
        avatar_cx = 0.116
        avatar_cy = ly + lane_h/2 + 0.020
        draw_agent_avatar(ax, avatar_cx, avatar_cy, 0.036, lane["color"], lane["agent"], lane["role"])

        # Lane Blocks
        for b in lane["blocks"]:
            bx, bw = b["x"], b["w"]
            bh = 0.120
            by = ly + (lane_h - bh)/2
            
            # Action Block Card
            ax.add_patch(patches.Rectangle(
                (bx, by), bw, bh,
                facecolor=b["bg"], edgecolor=b["col"], lw=1.3
            ))
            # Block Title Banner
            ax.add_patch(patches.Rectangle(
                (bx, by + bh - 0.032), bw, 0.032,
                facecolor=b["col"], edgecolor="none"
            ))
            ax.text(bx + bw/2, by + bh - 0.016, b["title"],
                    ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
            # Block Description
            ax.text(bx + bw/2, by + (bh - 0.032)/2, b["desc"],
                    ha="center", va="center", fontsize=6.2, color=COLOR_DARK, linespacing=1.2)

    # -------------------------------------------------------------------------
    # INTRA-LANE FLOW ARROWS (Horizontal, between adjacent blocks)
    # -------------------------------------------------------------------------
    # Lane 1 internal flow: Ingress -> Hydration -> Dispatch
    ax.annotate("", xy=(0.48, 0.810), xytext=(0.43, 0.810),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.75, 0.810), xytext=(0.70, 0.810),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # Lane 2 internal flow: Cycle Trace -> Taint Attribution
    ax.annotate("", xy=(0.63, 0.585), xytext=(0.57, 0.585),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # Lane 3 internal flow: Narrative -> Structuring
    ax.annotate("", xy=(0.63, 0.360), xytext=(0.57, 0.360),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # Lane 4 internal pipeline: Grammar -> Schema -> 4-Eyes -> Merkle
    ax.annotate("", xy=(0.41, 0.135), xytext=(0.39, 0.135),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.60, 0.135), xytext=(0.58, 0.135),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.79, 0.135), xytext=(0.77, 0.135),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # -------------------------------------------------------------------------
    # INTER-LANE ORTHOGONAL GUTTER ARROWS (Zero collision with any block or text)
    # -------------------------------------------------------------------------
    # 1. Lane 1 Dispatch (x=0.855, bottom=0.750) -> Gutter 1 (y=0.697) -> Lane 2 Smurfing (x=0.425, top=0.645)
    ax.plot([0.855, 0.855], [0.750, 0.697], color=COLOR_INGEST, lw=1.8)
    ax.plot([0.855, 0.425], [0.697, 0.697], color=COLOR_INGEST, lw=1.8)
    ax.annotate("", xy=(0.425, 0.645), xytext=(0.425, 0.697),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_INGEST, mutation_scale=12))
    # Gutter 1 Badge
    ax.text(0.640, 0.697, "Forensic Investigation Package", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=COLOR_INGEST,
            bbox=dict(boxstyle="square,pad=0.25", fc="#ffffff", ec=COLOR_INGEST, lw=1.0))

    # 2. Lane 2 Taint (x=0.775, bottom=0.525) -> Gutter 2 (y=0.472) -> Lane 3 Narrative (x=0.425, top=0.420)
    ax.plot([0.775, 0.775], [0.525, 0.472], color=COLOR_GNN, lw=1.8)
    ax.plot([0.775, 0.425], [0.472, 0.472], color=COLOR_GNN, lw=1.8)
    ax.annotate("", xy=(0.425, 0.420), xytext=(0.425, 0.472),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_GNN, mutation_scale=12))
    # Gutter 2 Badge
    ax.text(0.600, 0.472, "Attributed Subgraph & Typology Invariants", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=COLOR_GNN,
            bbox=dict(boxstyle="square,pad=0.25", fc="#ffffff", ec=COLOR_GNN, lw=1.0))

    # 3. Lane 3 FinCEN Structure (x=0.775, bottom=0.300) -> Gutter 3 (y=0.247) -> Lane 4 Grammar (x=0.305, top=0.195)
    ax.plot([0.775, 0.775], [0.300, 0.247], color=COLOR_GNN_PURPLE, lw=1.8)
    ax.plot([0.775, 0.305], [0.247, 0.247], color=COLOR_GNN_PURPLE, lw=1.8)
    ax.annotate("", xy=(0.305, 0.195), xytext=(0.305, 0.247),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_GNN_PURPLE, mutation_scale=12))
    # Gutter 3 Badge
    ax.text(0.540, 0.247, "Raw Candidate SAR Narrative Dossier", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=COLOR_GNN_PURPLE,
            bbox=dict(boxstyle="square,pad=0.25", fc="#ffffff", ec=COLOR_GNN_PURPLE, lw=1.0))

    save_figure(fig, "fig_forensic_swarm", pad_inches=0.12)
    save_figure(fig, "fig20_multi_agent_forensic_swarm", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
