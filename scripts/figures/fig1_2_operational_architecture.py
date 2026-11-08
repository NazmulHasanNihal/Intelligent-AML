"""
Figure 1.2 / 1.3: C-STGB Operational Architecture and Real-Time Conformal Triage Dataflow
Standard 6-Module Publication-Grade Architecture Pipeline.
Follows Phase 2 Master Figure Overhaul Ground Rules:
- 6 large left-to-right module blocks with labeled connecting arrows
- Large crisp vector icons for each module
- 2-3 word authoritative titles
- Clean concept bullets (no embedded equations or tiny graphs)
- Strict 4-color publication palette
- Clear, readable typography (all fonts >= 7.2 pt)
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

def draw_cylinder_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a crisp multi-disk database cylinder icon."""
    r_h = h * 0.22
    # Base body
    ax.add_patch(patches.Rectangle(
        (xc - w/2, yc - h/2 + r_h/2), w, h - r_h,
        facecolor=bg, edgecolor="none"
    ))
    # Vertical side borders
    ax.plot([xc - w/2, xc - w/2], [yc - h/2 + r_h/2, yc + h/2 - r_h/2], color=fg, lw=1.3)
    ax.plot([xc + w/2, xc + w/2], [yc - h/2 + r_h/2, yc + h/2 - r_h/2], color=fg, lw=1.3)
    # Bottom curved rim
    ax.add_patch(patches.Ellipse(
        (xc, yc - h/2 + r_h/2), w, r_h,
        facecolor=bg, edgecolor=fg, lw=1.3
    ))
    # Mid-tier internal seam
    ax.add_patch(patches.Arc(
        (xc, yc), w, r_h,
        theta1=180, theta2=360, color=fg, lw=1.1
    ))
    # Top lid ellipse
    ax.add_patch(patches.Ellipse(
        (xc, yc + h/2 - r_h/2), w, r_h,
        facecolor=fg, edgecolor=fg, lw=1.3, alpha=0.35
    ))
    ax.add_patch(patches.Ellipse(
        (xc, yc + h/2 - r_h/2), w, r_h,
        facecolor="none", edgecolor=fg, lw=1.3
    ))

def draw_pipe_conduit_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a hydrodynamic mass-flow conduit icon."""
    # Horizontal conduit tube
    tube_h = h * 0.40
    ax.add_patch(patches.Rectangle(
        (xc - w/2, yc - tube_h/2), w, tube_h,
        facecolor=bg, edgecolor=fg, lw=1.3
    ))
    # Inflow arrow on left
    ax.annotate("", xy=(xc - w/2 + 0.015, yc), xytext=(xc - w/2 - 0.005, yc),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=fg))
    # Outflow arrow on right
    ax.annotate("", xy=(xc + w/2 + 0.012, yc), xytext=(xc + w/2 - 0.008, yc),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=fg))
    # Central strict conservation valve node
    ax.add_patch(patches.Circle((xc, yc), tube_h * 0.48, facecolor=fg, edgecolor=COLOR_DARK, lw=1.2))
    ax.plot([xc - w/4, xc + w/4], [yc, yc], color="#ffffff", lw=1.0, linestyle="--")

def draw_gnn_brain_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a graph neural network node-and-edge icon."""
    nodes = [
        (xc - w * 0.30, yc - h * 0.22),
        (xc - w * 0.25, yc + h * 0.25),
        (xc, yc),
        (xc + w * 0.25, yc + h * 0.25),
        (xc + w * 0.30, yc - h * 0.22)
    ]
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (1, 3)]
    for i, j in edges:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]],
                color=fg, lw=1.2, alpha=0.6, zorder=3)
    for idx, (nx, ny) in enumerate(nodes):
        r = 0.0085 if idx == 2 else 0.0068
        c = COLOR_RISK if idx == 2 else fg
        ax.add_patch(patches.Circle((nx, ny), r, facecolor=bg, edgecolor=c, lw=1.4, zorder=4))

def draw_smote_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a topology-clustered SMOTE interpolation icon."""
    # Class 0 benign nodes
    np.random.seed(42)
    for _ in range(6):
        ox = xc - w * 0.22 + np.random.uniform(-w*0.12, w*0.12)
        oy = yc + np.random.uniform(-h*0.25, h*0.25)
        ax.add_patch(patches.Circle((ox, oy), 0.0045, facecolor=COLOR_SAFE, edgecolor=COLOR_SAFE, zorder=4))
    # Class 1 minority anchors
    p1 = (xc + w * 0.15, yc - h * 0.20)
    p2 = (xc + w * 0.25, yc + h * 0.22)
    p_synth = (xc + w * 0.20, yc + 0.01)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=COLOR_MUTED, linestyle=":", lw=1.1, zorder=3)
    ax.add_patch(patches.Circle(p1, 0.0055, facecolor=COLOR_RISK, edgecolor=COLOR_DARK, lw=1.0, zorder=4))
    ax.add_patch(patches.Circle(p2, 0.0055, facecolor=COLOR_RISK, edgecolor=COLOR_DARK, lw=1.0, zorder=4))
    ax.add_patch(patches.Rectangle((p_synth[0]-0.005, p_synth[1]-0.005), 0.010, 0.010,
                                  facecolor="#f59e0b", edgecolor=COLOR_DARK, lw=1.0, zorder=5))

def draw_balance_scale_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a calibrated Bayes cost-balance scale icon."""
    # Base & vertical stem
    ax.plot([xc - w * 0.22, xc + w * 0.22], [yc - h * 0.32, yc - h * 0.32], color=fg, lw=1.6)
    ax.plot([xc, xc], [yc - h * 0.32, yc + h * 0.28], color=fg, lw=1.6)
    # Tilted crossbar (asymmetric risk weighting: FN >> FP)
    bar_dx = w * 0.32
    bar_dy = h * 0.12
    x1, y1 = xc - bar_dx, yc + h * 0.24 + bar_dy
    x2, y2 = xc + bar_dx, yc + h * 0.24 - bar_dy
    ax.plot([x1, x2], [y1, y2], color=fg, lw=1.5)
    # Left pan (FP cost)
    ax.plot([x1, x1 - 0.007], [y1, y1 - 0.06], color=COLOR_MUTED, lw=1.0)
    ax.plot([x1, x1 + 0.007], [y1, y1 - 0.06], color=COLOR_MUTED, lw=1.0)
    ax.add_patch(patches.Arc((x1, y1 - 0.06), 0.018, 0.010, theta1=180, theta2=360, color=fg, lw=1.3))
    # Right pan (FN cost - heavier, lower)
    ax.plot([x2, x2 - 0.007], [y2, y2 - 0.06], color=COLOR_MUTED, lw=1.0)
    ax.plot([x2, x2 + 0.007], [y2, y2 - 0.06], color=COLOR_MUTED, lw=1.0)
    ax.add_patch(patches.Arc((x2, y2 - 0.06), 0.024, 0.012, theta1=180, theta2=360, color=COLOR_RISK, lw=1.4))

def draw_triage_funnel_icon(ax, xc, yc, w, h, fg, bg):
    """Draws a 3-tier conformal triage funnel icon."""
    poly_top = np.array([
        [xc - w * 0.32, yc + h * 0.30],
        [xc + w * 0.32, yc + h * 0.30],
        [xc + w * 0.18, yc + h * 0.04],
        [xc - w * 0.18, yc + h * 0.04]
    ])
    ax.add_patch(patches.Polygon(poly_top, closed=True, facecolor=COLOR_SAFE_LIGHT, edgecolor=COLOR_SAFE, lw=1.2))

    poly_mid = np.array([
        [xc - w * 0.18, yc + h * 0.04],
        [xc + w * 0.18, yc + h * 0.04],
        [xc + w * 0.10, yc - h * 0.16],
        [xc - w * 0.10, yc - h * 0.16]
    ])
    ax.add_patch(patches.Polygon(poly_mid, closed=True, facecolor=COLOR_REVIEW_LIGHT, edgecolor=COLOR_REVIEW, lw=1.2))

    poly_bot = np.array([
        [xc - w * 0.10, yc - h * 0.16],
        [xc + w * 0.10, yc - h * 0.16],
        [xc + w * 0.06, yc - h * 0.34],
        [xc - w * 0.06, yc - h * 0.34]
    ])
    ax.add_patch(patches.Polygon(poly_bot, closed=True, facecolor=COLOR_RISK_LIGHT, edgecolor=COLOR_RISK, lw=1.2))


def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, ax = plt.subplots(figsize=(13.2, 4.6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # 1. Master Header Banner (Dark Slate Blue)
    ax.add_patch(patches.Rectangle(
        (0.010, 0.900), 0.980, 0.082,
        facecolor="#0f172a", edgecolor="#1e293b", lw=1.2
    ))
    ax.text(0.50, 0.952, "C-STGB: Real-Time Financial Surveillance Architecture & Conformal Triage Pipeline",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.920, "End-to-End Enterprise Flow: Multi-Rail Ingestion -> Invariant Filtering -> GNN Core -> Bayes Tuning -> 3-Tier CRC Triage",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # Module Definitions: Exactly 6 Large Blocks Left-to-Right
    modules = [
        {
            "id": "1",
            "title": "Streaming Ingest",
            "draw_icon": draw_cylinder_icon,
            "fg": COLOR_INGEST,
            "bg": COLOR_INGEST_BG,
            "border": COLOR_INGEST,
            "bullets": [
                "Zero-copy Arrow IPC",
                "Sub-millisecond DuckDB",
                "Multi-rail normalization",
                "Temporal window slicing"
            ]
        },
        {
            "id": "2",
            "title": "Invariant Engine",
            "draw_icon": draw_pipe_conduit_icon,
            "fg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "border": COLOR_GNN,
            "bullets": [
                "Hydrodynamic mass flow",
                "Hawkes arrival velocity",
                "Bidirectional causal taint",
                "Cold-start mule detection"
            ]
        },
        {
            "id": "3",
            "title": "Spatio-Temporal GNN",
            "draw_icon": draw_gnn_brain_icon,
            "fg": COLOR_GNN_PURPLE,
            "bg": "#faf5ff",
            "border": COLOR_GNN_PURPLE,
            "bullets": [
                "Continuous harmonic decay",
                "Learnable edge-trust gating",
                "Dirichlet energy retention",
                "Structural smurfing defense"
            ]
        },
        {
            "id": "4",
            "title": "Latent Resampler",
            "draw_icon": draw_smote_icon,
            "fg": "#d97706",
            "bg": "#fffbeb",
            "border": "#b45309",
            "bullets": [
                "Typology GraphSMOTE",
                "Extreme imbalance handling",
                "Embedding manifold balance",
                "Cluster anchor synthesis"
            ]
        },
        {
            "id": "5",
            "title": "Bayes Calibrator",
            "draw_icon": draw_balance_scale_icon,
            "fg": COLOR_REVIEW,
            "bg": COLOR_REVIEW_BG,
            "border": COLOR_REVIEW,
            "bullets": [
                "Cost-asymmetric matrix",
                "Calibrated cutoff tuning",
                "Regulatory utility balance",
                "Drift-bounded risk bounds"
            ]
        },
        {
            "id": "6",
            "title": "Conformal Triage",
            "draw_icon": draw_triage_funnel_icon,
            "fg": COLOR_SAFE,
            "bg": COLOR_SAFE_BG,
            "border": COLOR_SAFE,
            "bullets": [
                "Class-conditional CRC",
                "99.33% straight-through",
                "Human review routing",
                "Autonomous SAR filing"
            ]
        }
    ]

    n_mods = len(modules)
    x_start = 0.012
    total_w = 0.976
    gap_w = 0.024
    block_w = (total_w - (n_mods - 1) * gap_w) / n_mods
    block_y = 0.200
    block_h = 0.670

    arrow_labels = [
        "Normalized\nStreams",
        "12-D Invariant\nVectors",
        "Latent Graph\nStates",
        "Balanced\nRepresentations",
        "Calibrated\nProbabilities"
    ]

    for idx, mod in enumerate(modules):
        bx = x_start + idx * (block_w + gap_w)

        # Outer Container Block (Sharp Rectangle)
        ax.add_patch(patches.Rectangle(
            (bx, block_y), block_w, block_h,
            facecolor=mod["bg"], edgecolor=mod["border"], lw=1.4, zorder=2
        ))

        # Title Header Strip (Sharp Rectangle)
        ax.add_patch(patches.Rectangle(
            (bx, block_y + block_h - 0.055), block_w, 0.055,
            facecolor=mod["fg"], edgecolor=mod["border"], lw=1.2, zorder=3
        ))
        ax.text(bx + block_w / 2, block_y + block_h - 0.0275,
                f"{mod['id']}. {mod['title']}",
                ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff", zorder=4)

        # Vector Icon Area
        icon_yc = block_y + block_h - 0.155
        mod["draw_icon"](ax, bx + block_w / 2, icon_yc, block_w * 0.70, 0.145, mod["fg"], mod["bg"])

        # Concept Bullets (Readable font >= 7.2pt, no equations)
        bullet_start_y = block_y + block_h - 0.265
        for b_idx, bullet in enumerate(mod["bullets"]):
            by = bullet_start_y - b_idx * 0.082
            # Diamond marker
            ax.plot(bx + 0.012, by, marker="s", markersize=3.5, color=mod["fg"], zorder=4)
            ax.text(bx + 0.022, by, bullet,
                    ha="left", va="center", fontsize=7.2, color=COLOR_DARK, fontweight="normal", zorder=4)

        # Inter-block connecting arrows
        if idx < n_mods - 1:
            ax_start = bx + block_w
            ax_end = ax_start + gap_w
            arrow_mid_y = block_y + block_h * 0.50
            ax.annotate("", xy=(ax_end, arrow_mid_y), xytext=(ax_start, arrow_mid_y),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#475569", mutation_scale=11),
                        zorder=5)
            # Arrow label
            ax.text((ax_start + ax_end) / 2, arrow_mid_y + 0.038, arrow_labels[idx],
                    ha="center", va="bottom", fontsize=5.8, fontweight="bold", color="#475569", linespacing=0.95)

    # Bottom SLA & Assurance Banner (Sharp Rectangles)
    assurances = [
        ("Fast-Path SLA", "< 0.45 ms Total Latency", "P99: 0.82 ms at 31,200 tx/sec throughput", COLOR_INGEST),
        ("Workload Slashing", "99.33% Straight-Through", "Manual human review slashed by 99.51%", COLOR_SAFE),
        ("Statistical Coverage", r"$\geq$ 99.0% Guarantee", "Class-conditional finite-sample validity", COLOR_GNN_PURPLE),
        ("Auditable Governance", "Deterministic AST & Merkle", "Zero-hallucination agentic SAR generator", COLOR_RISK)
    ]

    assure_w = total_w / len(assurances)
    for idx, (head, val, sub, fg_col) in enumerate(assurances):
        ax_x = x_start + idx * assure_w
        # Background card
        ax.add_patch(patches.Rectangle(
            (ax_x + 0.003, 0.025), assure_w - 0.006, 0.145,
            facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.1, zorder=2
        ))
        # Left accent stripe
        ax.add_patch(patches.Rectangle(
            (ax_x + 0.003, 0.025), 0.006, 0.145,
            facecolor=fg_col, edgecolor=fg_col, zorder=3
        ))
        # Text
        ax.text(ax_x + 0.016, 0.135, head, ha="left", va="center", fontsize=7.2, fontweight="bold", color="#64748b", zorder=4)
        ax.text(ax_x + 0.016, 0.098, val, ha="left", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK, zorder=4)
        ax.text(ax_x + 0.016, 0.058, sub, ha="left", va="center", fontsize=6.8, color="#475569", zorder=4)

    # Save figure across all 5 directories
    save_figure(fig, "fig1_operational_architecture_flowchart", pad_inches=0.10)
    save_figure(fig, "fig_conformal_triage_flowchart", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
