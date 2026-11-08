"""
Figure 6.1: Multi-Agent Forensic Reasoning and Dual-Governance Pipeline
Redesigned as an authoritative 4-Horizontal-Swimlane Diagram:
Lanes for Coordinator, Specialist, Drafter, and Verifier agents with avatar circles,
step-by-step alert progression arrows, simplified Grammar/Schema validation blocks,
and zero raw EBNF / Pydantic code clutter.
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
    ax.add_patch(patches.Circle((cx, cy), radius + 0.006, facecolor="none", edgecolor=color, lw=1.2, linestyle=":"))
    # Agent circle
    ax.add_patch(patches.Circle((cx, cy), radius, facecolor=color, edgecolor=COLOR_DARK, lw=1.4))
    # Head & shoulders stylized avatar
    head_r = radius * 0.35
    ax.add_patch(patches.Circle((cx, cy + radius*0.25), head_r, facecolor="#ffffff", edgecolor="none"))
    # Shoulders arc
    ax.add_patch(patches.Arc((cx, cy - radius*0.35), radius*1.15, radius*0.9, theta1=0, theta2=180,
                             facecolor="#ffffff", edgecolor="#ffffff", lw=2.0))
    # Title badge below
    ax.text(cx, cy - radius - 0.024, label, ha="center", va="center",
            fontsize=7.4, fontweight="bold", color=COLOR_DARK)
    ax.text(cx, cy - radius - 0.046, role_title, ha="center", va="center",
            fontsize=6.2, color=COLOR_MUTED)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous widescreen canvas for 4 swimlanes
    fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (0.015, 0.925), 0.970, 0.065,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.965, "MULTI-AGENT FORENSIC INVESTIGATION & DUAL-GOVERNANCE WORKFLOW",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.940, "Four-Lane Autonomous Swarm: Ingestion -> Typology Attribution -> Narrative Drafting -> Deterministic Audit",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # 4 HORIZONTAL SWIMLANES
    # Lane y-boundaries:
    # Lane 1 (Top):    0.700 to 0.910 (Ingestion & Coordinator)
    # Lane 2:          0.485 to 0.695 (Specialist & Typology)
    # Lane 3:          0.270 to 0.480 (Drafter & Synthesis)
    # Lane 4 (Bottom): 0.055 to 0.265 (Verifier & Governance)
    
    lane_h = 0.200
    lanes = [
        {
            "y": 0.710, "name": "LANE 1: COORDINATION & HYDRATION",
            "agent": "Coordinator Agent", "role": "Swarm Orchestrator", "color": COLOR_INGEST, "bg": COLOR_INGEST_BG,
            "blocks": [
                {"title": "Conformal Alert Ingress", "desc": "Receives Tier 2 CRC abstention set\nTriggers <15 min forensic SLA clock", "col": COLOR_RISK, "bg": COLOR_RISK_BG, "x": 0.23, "w": 0.20},
                {"title": "DuckDB Graph Hydration", "desc": "Hydrates 2-hop causal subgraphs\nExtracts 12-D mass-flow invariants", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.49, "w": 0.22},
                {"title": "Swarm Task Dispatch", "desc": "Partitions evidence into forensic tasks\nMonitors agent execution deadlines", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.77, "w": 0.20}
            ]
        },
        {
            "y": 0.495, "name": "LANE 2: TOPOLOGICAL REASONING",
            "agent": "Specialist Agent", "role": "Typology Detective", "color": COLOR_GNN, "bg": COLOR_GNN_BG,
            "blocks": [
                {"title": "Smurfing & Wash Cycle Trace", "desc": "Identifies circular flow patterns\nTracks Hawkes burst acceleration", "col": COLOR_GNN, "bg": "#ffffff", "x": 0.32, "w": 0.25},
                {"title": "Causal Taint Attribution", "desc": "Computes forward & backward reach\nQuantifies illicit capital retention", "col": COLOR_GNN, "bg": "#ffffff", "x": 0.65, "w": 0.25}
            ]
        },
        {
            "y": 0.280, "name": "LANE 3: NARRATIVE SYNTHESIS",
            "agent": "Drafter Agent", "role": "SAR Dossier Author", "color": COLOR_GNN_PURPLE, "bg": "#FAF5FF",
            "blocks": [
                {"title": "Case Narrative Assembly", "desc": "Compiles chronological suspect timeline\nCorrelates evidence with typology patterns", "col": COLOR_GNN_PURPLE, "bg": "#ffffff", "x": 0.32, "w": 0.25},
                {"title": "FinCEN Form 111 Structure", "desc": "Generates structured narrative sections\nTemperature locked at zero (deterministic)", "col": COLOR_GNN_PURPLE, "bg": "#ffffff", "x": 0.65, "w": 0.25}
            ]
        },
        {
            "y": 0.065, "name": "LANE 4: DETERMINISTIC GOVERNANCE",
            "agent": "Verifier Agent", "role": "Audit & Compliance Officer", "color": COLOR_SAFE, "bg": COLOR_SAFE_BG,
            "blocks": [
                {"title": "Grammar Validation", "desc": "Strict lexical token verification\nEliminates hallucinations", "col": COLOR_INGEST, "bg": "#ffffff", "x": 0.23, "w": 0.17},
                {"title": "Schema Check", "desc": "Verifies account continuity\nValidates financial sums", "col": COLOR_REVIEW, "bg": "#ffffff", "x": 0.44, "w": 0.17},
                {"title": "4-Eyes Approval Desk", "desc": "Human compliance officer sign-off\nSenior analyst review decision", "col": COLOR_SAFE, "bg": "#ffffff", "x": 0.65, "w": 0.16},
                {"title": "Cryptographic Seal", "desc": "SHA-256 Merkle audit root\nImmutable court-ready record", "col": COLOR_DARK, "bg": "#ffffff", "x": 0.84, "w": 0.14}
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
        # Left Lane Header Strip
        ax.add_patch(patches.Rectangle(
            (0.015, ly), 0.025, lane_h,
            facecolor=lane["color"], edgecolor="none"
        ))
        ax.text(0.027, ly + lane_h/2, lane["name"],
                ha="center", va="center", rotation=90, fontsize=6.8, fontweight="bold", color="#ffffff")

        # Agent Avatar Circle
        avatar_cx = 0.115
        avatar_cy = ly + lane_h/2 + 0.020
        draw_agent_avatar(ax, avatar_cx, avatar_cy, 0.040, lane["color"], lane["agent"], lane["role"])

        # Lane Blocks
        for b in lane["blocks"]:
            bx, bw = b["x"], b["w"]
            bh = 0.125
            by = ly + (lane_h - bh)/2
            
            # Action Block Card
            ax.add_patch(patches.Rectangle(
                (bx, by), bw, bh,
                facecolor=b["bg"], edgecolor=b["col"], lw=1.3
            ))
            # Block Title Banner
            ax.add_patch(patches.Rectangle(
                (bx, by + bh - 0.034), bw, 0.034,
                facecolor=b["col"], edgecolor="none"
            ))
            ax.text(bx + bw/2, by + bh - 0.017, b["title"],
                    ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
            # Block Description
            ax.text(bx + bw/2, by + (bh - 0.034)/2, b["desc"],
                    ha="center", va="center", fontsize=6.4, color=COLOR_DARK, linespacing=1.2)

    # INTER-STAGE / INTER-AGENT ALERT FLOW ARROWS
    # 1. Lane 1 internal flow: Ingress -> Hydration -> Dispatch
    ax.annotate("", xy=(0.49, 0.810), xytext=(0.43, 0.810),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.77, 0.810), xytext=(0.71, 0.810),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # 2. Lane 1 Dispatch -> Lane 2 Specialist (Down & Left)
    ax.annotate("", xy=(0.32, 0.620), xytext=(0.85, 0.745),
                arrowprops=dict(arrowstyle="->", lw=2.0, color=COLOR_INGEST,
                                connectionstyle="arc3,rad=0.18", mutation_scale=14))
    ax.text(0.60, 0.700, "Forensic Investigation Package", ha="center", va="center",
            fontsize=6.4, fontweight="bold", color=COLOR_INGEST,
            bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=COLOR_INGEST, lw=0.8))

    # 3. Lane 2 internal flow: Cycle Trace -> Taint
    ax.annotate("", xy=(0.65, 0.595), xytext=(0.57, 0.595),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # 4. Lane 2 Taint -> Lane 3 Drafter (Down & Left)
    ax.annotate("", xy=(0.32, 0.405), xytext=(0.77, 0.530),
                arrowprops=dict(arrowstyle="->", lw=2.0, color=COLOR_GNN,
                                connectionstyle="arc3,rad=0.18", mutation_scale=14))
    ax.text(0.55, 0.485, "Attributed Subgraph & Typology Invariants", ha="center", va="center",
            fontsize=6.4, fontweight="bold", color=COLOR_GNN,
            bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=COLOR_GNN, lw=0.8))

    # 5. Lane 3 internal flow: Narrative -> Structuring
    ax.annotate("", xy=(0.65, 0.380), xytext=(0.57, 0.380),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    # 6. Lane 3 Structuring -> Lane 4 Verifier (Down & Left)
    ax.annotate("", xy=(0.23, 0.190), xytext=(0.77, 0.315),
                arrowprops=dict(arrowstyle="->", lw=2.0, color=COLOR_GNN_PURPLE,
                                connectionstyle="arc3,rad=0.18", mutation_scale=14))
    ax.text(0.50, 0.270, "Raw Candidate SAR Narrative", ha="center", va="center",
            fontsize=6.4, fontweight="bold", color=COLOR_GNN_PURPLE,
            bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=COLOR_GNN_PURPLE, lw=0.8))

    # 7. Lane 4 internal pipeline: Grammar -> Schema -> 4-Eyes -> Merkle
    ax.annotate("", xy=(0.44, 0.165), xytext=(0.40, 0.165),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.65, 0.165), xytext=(0.61, 0.165),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))
    ax.annotate("", xy=(0.84, 0.165), xytext=(0.81, 0.165),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK, mutation_scale=12))

    save_figure(fig, "fig_forensic_swarm", pad_inches=0.12)
    save_figure(fig, "fig20_multi_agent_forensic_swarm", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
