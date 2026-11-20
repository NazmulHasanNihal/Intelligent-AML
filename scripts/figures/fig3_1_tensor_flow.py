"""
Figure 3.1: End-to-End Architectural Dataflow of C-STGB
Standard 6-Module Publication-Grade Flowchart Architecture.
Converts the previous static card layout into a true end-to-end dataflow flowchart:
- Data Ingestion & Physical Invariant Feeds (Multi-Rail Ledgers, DuckDB, Arrow Memory)
- 6 Interconnected Canonical Modules with explicit tensor dimensions and mathematical specifications
- Dedicated Decision Diamond for Class-Conditional Conformal Risk Control (CRC)
- Decoupled 3-Tier Operational Triage Endpoints (Tier 1 Quarantine, Tier 2 Assisted Desk, Tier 3 Straight-Through)
- Parallel, decoupled routing channels with zero overlapping lines or clipping text
- Strict adherence to the master 4-color palette
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_LIGHT, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_PURPLE, COLOR_GNN_LIGHT, COLOR_GNN_BG,
    COLOR_SAFE, COLOR_SAFE_LIGHT, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_LIGHT, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_LIGHT, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)


def draw_cylinder(ax, x, y, w, h, facecolor, edgecolor, lw=1.2, label_top="", label_bottom="", bullets=None):
    """Draws a clean cylindrical database / streaming data store with non-overlapping text."""
    cap_h = h * 0.16
    # Body
    rect = patches.Rectangle((x, y + cap_h / 2), w, h - cap_h, facecolor=facecolor, edgecolor="none", zorder=2)
    ax.add_patch(rect)
    # Side boundaries
    ax.plot([x, x], [y + cap_h / 2, y + h - cap_h / 2], color=edgecolor, lw=lw, zorder=3)
    ax.plot([x + w, x + w], [y + cap_h / 2, y + h - cap_h / 2], color=edgecolor, lw=lw, zorder=3)
    # Bottom ellipse arc
    bottom_arc = patches.Arc(
        (x + w / 2, y + cap_h / 2), w, cap_h, angle=0, theta1=180, theta2=360,
        color=edgecolor, lw=lw, zorder=3
    )
    ax.add_patch(bottom_arc)
    bottom_fill = patches.Ellipse(
        (x + w / 2, y + cap_h / 2), w, cap_h, facecolor=facecolor, edgecolor="none", zorder=2
    )
    ax.add_patch(bottom_fill)
    # Top ellipse
    top_ellipse = patches.Ellipse(
        (x + w / 2, y + h - cap_h / 2), w, cap_h, facecolor=facecolor, edgecolor=edgecolor, lw=lw, zorder=4
    )
    ax.add_patch(top_ellipse)

    # Text hierarchy inside cylinder (properly spaced from top to bottom)
    if label_top:
        ax.text(x + w / 2, y + h - cap_h - 2.0, label_top, ha="center", va="center",
                fontsize=6.2, fontweight="bold", color=COLOR_DARK, zorder=5)
    if label_bottom:
        ax.text(x + w / 2, y + h - cap_h - 4.4, label_bottom, ha="center", va="center",
                fontsize=5.0, fontstyle="italic", color=COLOR_MUTED, zorder=5)

    if bullets:
        # Divider line
        ax.plot([x + 1.2, x + w - 1.2], [y + h - cap_h - 6.0, y + h - cap_h - 6.0],
                color=edgecolor, lw=0.6, alpha=0.4, zorder=5)
        n_b = len(bullets)
        top_b = y + h - cap_h - 8.2
        bot_b = y + cap_h + 1.2
        dy = (top_b - bot_b) / max(n_b - 1, 1)
        for i, btxt in enumerate(bullets):
            by = top_b - i * dy
            ax.text(x + w / 2, by, btxt, ha="center", va="center",
                    fontsize=4.9, color="#1e293b", zorder=5)


def draw_process_node(ax, x, y, w, h, num_tag, title, subtitle, spec_badge, items, border_color, fill_color, header_color, sla_badge=""):
    """Draws a standardized, high-precision flowchart process node with zero text overflow."""
    # Outer Rounded Card
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor=fill_color, edgecolor=border_color, lw=1.2, zorder=2
    )
    ax.add_patch(box)

    # Header Strip
    hdr_h = 5.2
    hdr = patches.Rectangle(
        (x, y + h - hdr_h), w, hdr_h,
        facecolor=header_color, edgecolor="none", zorder=3
    )
    ax.add_patch(hdr)
    ax.text(x + w / 2, y + h - 2.0, num_tag, ha="center", va="center", fontsize=5.8, fontweight="bold", color="#ffffff", zorder=4)
    ax.text(x + w / 2, y + h - 3.8, title, ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff", zorder=4)

    # Subtitle under header
    ax.text(x + w / 2, y + h - 6.6, subtitle, ha="center", va="center", fontsize=5.2, fontstyle="italic", color=COLOR_MUTED, zorder=4)

    # Spec / Tensor Badge
    badge_y = y + h - 10.4
    ax.add_patch(patches.FancyBboxPatch(
        (x + 1.0, badge_y - 1.8), w - 2.0, 3.6,
        boxstyle="round,pad=0.1,rounding_size=0.3",
        facecolor="#ffffff", edgecolor=border_color, lw=0.8, zorder=3
    ))
    ax.text(x + w / 2, badge_y, spec_badge, ha="center", va="center", fontsize=5.4, fontweight="bold", color=border_color, zorder=4)

    # Itemized flowchart steps
    n_items = len(items)
    content_top = badge_y - 2.8
    content_bot = y + 4.8 if sla_badge else y + 1.5
    avail_h = content_top - content_bot
    dy = avail_h / max(n_items, 1)

    for i, itxt in enumerate(items):
        cur_y = content_top - (i + 0.5) * dy
        ax.plot([x + 1.5], [cur_y], marker=">", markersize=2.4, color=border_color, zorder=4)
        ax.text(x + 2.3, cur_y, itxt, ha="left", va="center", fontsize=5.1, color="#1e293b", zorder=4)

    # SLA Footer Badge
    if sla_badge:
        ax.add_patch(patches.FancyBboxPatch(
            (x + 1.0, y + 1.0), w - 2.0, 3.2,
            boxstyle="round,pad=0.1,rounding_size=0.3",
            facecolor="#ffffff", edgecolor=border_color, lw=0.7, zorder=3
        ))
        ax.text(x + w / 2, y + 2.6, sla_badge, ha="center", va="center", fontsize=5.2, fontweight="bold", color=border_color, zorder=4)


def draw_diamond(ax, cx, cy, w, h, title, subtitle, items, border_color, fill_color):
    """Draws a classic decision diamond for Conformal Risk Control triage."""
    pts = [
        [cx, cy + h / 2],      # Top vertex
        [cx + w / 2, cy],      # Right vertex
        [cx, cy - h / 2],      # Bottom vertex
        [cx - w / 2, cy]       # Left vertex
    ]
    poly = patches.Polygon(pts, facecolor=fill_color, edgecolor=border_color, lw=1.3, zorder=3)
    ax.add_patch(poly)

    # Text inside diamond
    ax.text(cx, cy + 3.4, title, ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_DARK, zorder=4)
    ax.text(cx, cy + 1.4, subtitle, ha="center", va="center", fontsize=5.0, fontstyle="italic", color=COLOR_MUTED, zorder=4)
    ax.text(cx, cy - 1.2, items[0], ha="center", va="center", fontsize=5.2, fontweight="bold", color=COLOR_REVIEW, zorder=4)
    ax.text(cx, cy - 3.2, items[1], ha="center", va="center", fontsize=4.8, color="#334155", zorder=4)


def draw_endpoint(ax, x, y, w, h, tier_label, pct_label, subtext, items, border_color, fill_color, text_color):
    """Draws a dedicated operational outcome endpoint node."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.5",
        facecolor=fill_color, edgecolor=border_color, lw=1.2, zorder=2
    )
    ax.add_patch(box)

    # Header
    ax.text(x + w / 2, y + h - 2.4, tier_label, ha="center", va="center", fontsize=6.2, fontweight="bold", color=text_color, zorder=4)
    ax.text(x + w / 2, y + h - 4.4, pct_label, ha="center", va="center", fontsize=5.4, fontweight="bold", color=text_color, zorder=4)
    ax.text(x + w / 2, y + h - 6.2, subtext, ha="center", va="center", fontsize=4.8, fontstyle="italic", color=COLOR_MUTED, zorder=4)

    # Divider
    ax.plot([x + 0.8, x + w - 0.8], [y + h - 7.5, y + h - 7.5], color=border_color, lw=0.6, alpha=0.5, zorder=3)

    # Bullets
    n_items = len(items)
    content_top = y + h - 9.0
    content_bot = y + 1.2
    dy = (content_top - content_bot) / max(n_items, 1)

    for i, itxt in enumerate(items):
        cur_y = content_top - (i + 0.5) * dy
        ax.plot([x + 1.2], [cur_y], marker="s", markersize=2.0, color=border_color, zorder=4)
        ax.text(x + 2.0, cur_y, itxt, ha="left", va="center", fontsize=4.9, color="#1e293b", zorder=4)


def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(15.6, 8.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Title Banner (Dark Slate Blue)
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor="none", zorder=2
    ))
    ax.text(50.0, 96.6, "C-STGB: END-TO-END ARCHITECTURAL DATAFLOW & TENSOR TRANSFORMATION PIPELINE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff", zorder=3)
    ax.text(50.0, 94.1, "Flowchart Architecture: Ledger Feeds -> Temporal Encoding -> Edge Gating -> Latent SMOTE -> Bayes Head -> Conformal CRC Triage",
            ha="center", va="center", fontsize=7.0, color="#94a3b8", zorder=3)

    # =========================================================================
    # COLUMN 1: UPSTREAM INGESTION & 12-D PHYSICAL INVARIANTS (X in [1.8, 17.0])
    # =========================================================================
    # Top Cylinder: Multi-Rail Ledger Ingestion Stream
    draw_cylinder(
        ax, x=1.8, y=66.0, w=15.2, h=23.0,
        facecolor=COLOR_INGEST_BG, edgecolor=COLOR_INGEST, lw=1.2,
        label_top="MULTI-RAIL LEDGERS",
        label_bottom="SWIFT • UTXO • EVM • PaySim",
        bullets=[
            "• High-Velocity Kafka Bus",
            "• Zero-Copy Arrow Memory",
            "• 31,250 tx/s Burst Peak"
        ]
    )

    # Bottom Node: 12-D Flow Invariant Extraction Engine
    draw_process_node(
        ax, x=1.8, y=20.0, w=15.2, h=41.0,
        num_tag="FEATURE ENGINE",
        title="12-D Flow Invariants",
        subtitle="DuckDB 2-Hop Aggregation",
        spec_badge=r"Vector: $\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$",
        items=[
            r"• Mass Balance: $\Phi_{\mathrm{flow}} \in [0, 1]$",
            r"• Hawkes Burst: $\lambda_{\mathrm{burst}}$",
            "• Fan-In / Fan-Out Ratio",
            "• Temporal Entropy Rate",
            "• Multi-Moment Skewness"
        ],
        border_color=COLOR_INGEST,
        fill_color=COLOR_INGEST_BG,
        header_color=COLOR_INGEST,
        sla_badge="Lat: 0.11 ms | LRU: 0.18 ms"
    )

    # Connector from Cylinder down to Invariant Engine
    ax.annotate("", xy=(9.4, 61.5), xytext=(9.4, 65.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=COLOR_INGEST, mutation_scale=9), zorder=4)
    ax.text(10.2, 63.5, "Raw Records", ha="left", va="center", fontsize=4.8, fontstyle="italic", color=COLOR_INGEST, zorder=5)

    # Connectors from Column 1 into Column 2
    # 1. Cylinder -> Module 1 (Events & Topology)
    ax.annotate("", xy=(21.0, 77.0), xytext=(17.0, 77.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(19.0, 78.8, "Events (V, E, t)", ha="center", va="bottom", fontsize=5.0, fontweight="bold", color=COLOR_DARK, zorder=6)

    # 2. Invariant Engine -> Module 2 & Module 4 bus
    ax.annotate("", xy=(21.0, 36.5), xytext=(17.0, 36.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(19.0, 38.3, r"$\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$", ha="center", va="bottom", fontsize=5.0, fontweight="bold", color=COLOR_DARK, zorder=6)

    # =========================================================================
    # COLUMN 2: SPATIO-TEMPORAL NEURAL CORE (X in [21.0, 39.5])
    # =========================================================================
    # Module 1 (Top): Continuous-Time Multi-Scale Temporal Graph Encoder
    draw_process_node(
        ax, x=21.0, y=57.0, w=18.5, h=32.0,
        num_tag="MODULE 1",
        title="Continuous Temporal Encoder",
        subtitle="Harmonic Attention & Hawkes GNN",
        spec_badge=r"Node States: $\mathbf{h}_u(t) \in \mathbb{R}^{64}$",
        items=[
            "• 3-Band Continuous Attention",
            "  (Burst, Diurnal, Dormancy)",
            r"• Hawkes Decay: $\phi(\Delta t) = \alpha e^{-\beta \Delta t}$",
            "• Causal Chronological Passing",
            "• Zero Future Leakage Bound"
        ],
        border_color=COLOR_GNN,
        fill_color=COLOR_GNN_BG,
        header_color=COLOR_GNN,
        sla_badge=r"Lat: 0.03 ms | $\mathcal{O}(K \cdot d_t)$"
    )

    # Module 2 (Bottom): Context-Aware Adaptive Edge-Trust Filter
    draw_process_node(
        ax, x=21.0, y=20.0, w=18.5, h=32.0,
        num_tag="MODULE 2",
        title="Adaptive Edge-Trust Filter",
        subtitle="Adversarial Chaff Pruning Gate",
        spec_badge=r"Weights: $\mathbf{W}_{\mathrm{trust}} \in [0, 1]^{|E|}$",
        items=[
            r"• Soft Attention: $w_e = \sigma(\mathrm{MLP}(\cdot))$",
            "• Prunes 65.9% Synthetic Wires",
            "• Camouflage Noise Suppression",
            "• Dirichlet Smoothness Retention",
            "• Prevents Graph Over-Smoothing"
        ],
        border_color=COLOR_GNN,
        fill_color=COLOR_GNN_BG,
        header_color=COLOR_GNN,
        sla_badge="Lat: 0.02 ms | 65.9% Pruned"
    )

    # Internal Vertical Arrow: Module 1 -> Module 2
    ax.annotate("", xy=(30.25, 52.5), xytext=(30.25, 56.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLOR_GNN, mutation_scale=9), zorder=5)
    ax.text(31.0, 54.5, r"Temporal Embeds: $\mathbf{h}_u$", ha="left", va="center", fontsize=5.0, fontweight="bold", color=COLOR_GNN, zorder=6)

    # Connectors from Column 2 into Column 3
    # 1. Module 1 -> Module 3 (Latent SMOTE manifold input)
    ax.annotate("", xy=(43.5, 73.0), xytext=(39.5, 73.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(41.5, 74.8, r"$\mathbf{h}_u \in \mathbb{R}^{64}$", ha="center", va="bottom", fontsize=5.0, fontweight="bold", color=COLOR_DARK, zorder=6)

    # 2. Module 2 -> Module 4 (Pruned topology)
    ax.annotate("", xy=(43.5, 36.0), xytext=(39.5, 36.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(41.5, 37.8, r"Pruned $\tilde{\mathcal{G}}_t$", ha="center", va="bottom", fontsize=5.0, fontweight="bold", color=COLOR_DARK, zorder=6)

    # =========================================================================
    # COLUMN 3: REPRESENTATION OPTIMIZATION & FUSION (X in [43.5, 62.0])
    # =========================================================================
    # Module 3 (Top): Typology-Clustered Latent GraphSMOTE
    draw_process_node(
        ax, x=43.5, y=57.0, w=18.5, h=32.0,
        num_tag="MODULE 3",
        title="Latent GraphSMOTE",
        subtitle="Extreme Skew Rectification",
        spec_badge=r"Manifold: $\mathbf{Z}_{\mathrm{bal}} \in \mathbb{R}^{K \times 64}$",
        items=[
            "• Typology Subgraph Clustering",
            r"• Latent Interp: $\mathbf{z}_{\mathrm{syn}} = \mathbf{z}_i + \delta(\mathbf{z}_{\mathrm{nn}}-\mathbf{z}_i)$",
            "• Bilinear Edge Reconstruction",
            r"  $P(e_{ij}=1) = \sigma(\mathbf{z}_i \mathbf{W}_e \mathbf{z}_j^T)$",
            "• Rectifies 0.01% Extreme Imbalance"
        ],
        border_color=COLOR_GNN_PURPLE,
        fill_color="#faf5ff",
        header_color=COLOR_GNN_PURPLE,
        sla_badge="Offline Pre-Trained | 1:1 Parity"
    )

    # Module 4 (Bottom): Evidence-Adaptive Graph-Tabular Fusion
    draw_process_node(
        ax, x=43.5, y=20.0, w=18.5, h=32.0,
        num_tag="MODULE 4",
        title="Adaptive Fusion Engine",
        subtitle="Cold-Start Entity Resolution",
        spec_badge=r"Fused: $\mathbf{z}_{\mathrm{fused}} \in \mathbb{R}^{B \times 76}$",
        items=[
            r"• Dynamic Gating Factor: $\alpha_u$",
            r"  $\alpha_u = \sigma(\mathbf{W}_g [\mathrm{deg}(u), \mathrm{var}_t])$",
            r"• Fusion: $\mathbf{z}_f = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$",
            "• Zero-Topology Fallback Mode",
            "• Robust to Isolated Accounts"
        ],
        border_color="#a21caf",
        fill_color="#fdf4ff",
        header_color="#a21caf",
        sla_badge="Lat: 0.02 ms | Zero Cold-Start"
    )

    # Internal Vertical Connector: Module 3 balanced manifold informs Module 4
    ax.annotate("", xy=(52.75, 52.5), xytext=(52.75, 56.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=COLOR_GNN_PURPLE, linestyle="--", mutation_scale=9), zorder=5)
    ax.text(53.5, 54.5, "Balanced Manifold", ha="left", va="center", fontsize=4.9, color=COLOR_GNN_PURPLE, zorder=6)

    # Connectors from Column 3 into Column 4 (Both feed Module 5: Bayes Risk Head)
    # Module 3 -> Module 5
    ax.annotate("", xy=(66.0, 75.0), xytext=(62.0, 75.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(64.0, 76.8, r"$\mathbf{Z}_{\mathrm{bal}}$", ha="center", va="bottom", fontsize=5.0, fontweight="bold", color=COLOR_DARK, zorder=6)

    # Module 4 -> Module 5 (routed with clear upward orthogonal path and white text pill)
    ax.plot([62.0, 64.0, 64.0, 66.0], [36.0, 36.0, 68.0, 68.0], color=COLOR_DARK, lw=1.6, zorder=5)
    ax.annotate("", xy=(66.0, 68.0), xytext=(65.0, 68.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(64.0, 52.0, r"$\mathbf{z}_{\mathrm{fused}}$", ha="center", va="center", fontsize=5.0, fontweight="bold",
            color=COLOR_DARK, bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.6), zorder=6)

    # =========================================================================
    # COLUMN 4: DETECTION HEAD & CONFORMAL CRC DIAMOND (X in [66.0, 81.5])
    # =========================================================================
    # Module 5 (Top): Cost-Sensitive Bayes Risk Head
    draw_process_node(
        ax, x=66.0, y=60.0, w=15.5, h=29.0,
        num_tag="MODULE 5",
        title="Bayes Risk Head",
        subtitle="Asymmetric Cost Optimization",
        spec_badge=r"Risk: $\hat{\mathbf{p}}_u \in [0, 1]^2$",
        items=[
            "• Focal Tversky Multi-Loss",
            "• Heavy False-Negative Penalty",
            "• Evidence-Adaptive Scaling",
            r"• Calibrated Posterior $p_1$"
        ],
        border_color=COLOR_REVIEW,
        fill_color=COLOR_REVIEW_BG,
        header_color=COLOR_REVIEW,
        sla_badge="Lat: 0.05 ms | Cost-Sensitive"
    )

    # Connector from Module 5 down to Conformal CRC Diamond
    ax.annotate("", xy=(73.75, 49.5), xytext=(73.75, 59.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_DARK, mutation_scale=10), zorder=5)
    ax.text(74.5, 55.0, r"Score $p_1$", ha="left", va="center", fontsize=5.2, fontweight="bold", color=COLOR_DARK, zorder=6)

    # Module 6 (Bottom): Class-Conditional Conformal Risk Control (CRC) Diamond
    draw_diamond(
        ax, cx=73.75, cy=35.0, w=15.0, h=26.0,
        title="MODULE 6: CRC",
        subtitle="Conformal Risk Control",
        items=[
            r"Thresholds: $[\tau_1, \tau_2]$",
            r"Bound: $\mathbb{E}[L] \leq \alpha$"
        ],
        border_color=COLOR_SAFE,
        fill_color=COLOR_SAFE_BG
    )

    # =========================================================================
    # DECISION PATHS: CRC DIAMOND -> COLUMN 5 OPERATIONAL ENDPOINTS
    # Completely decoupled parallel tracks:
    # Path 1 (Quarantine) vertical track at x = 82.5
    # Path 2 (Assisted Desk) vertical track at x = 84.1
    # Path 3 (Straight-Through) vertical track at x = 82.5 (downward)
    # =========================================================================
    # Path 1: Tier 1 Illicit Quarantine (Exits top-right facet of Diamond -> Tier 1)
    ax.plot([77.5, 82.5, 82.5, 85.5], [41.5, 41.5, 77.0, 77.0], color=COLOR_RISK, lw=1.6, zorder=5)
    ax.annotate("", xy=(85.5, 77.0), xytext=(84.5, 77.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_RISK, mutation_scale=10), zorder=5)
    ax.text(82.5, 62.0, r"$p_1 > \tau_1$", ha="center", va="center", fontsize=5.0, fontweight="bold",
            color=COLOR_RISK, bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_RISK, lw=0.6), zorder=6)

    # Path 2: Tier 2 Assisted Review Desk (Exits right vertex of Diamond -> Tier 2)
    ax.plot([81.25, 84.1, 84.1, 85.5], [35.0, 35.0, 52.0, 52.0], color=COLOR_REVIEW, lw=1.6, zorder=5)
    ax.annotate("", xy=(85.5, 52.0), xytext=(84.5, 52.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_REVIEW, mutation_scale=10), zorder=5)
    ax.text(84.1, 43.5, r"$\tau_2 \leq p_1 \leq \tau_1$", ha="center", va="center", fontsize=4.8, fontweight="bold",
            color=COLOR_REVIEW, bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_REVIEW, lw=0.6), zorder=6)

    # Path 3: Tier 3 Straight-Through Clearance (Exits bottom-right facet of Diamond -> Tier 3)
    ax.plot([77.5, 82.5, 82.5, 85.5], [28.5, 28.5, 27.0, 27.0], color=COLOR_SAFE, lw=1.6, zorder=5)
    ax.annotate("", xy=(85.5, 27.0), xytext=(84.5, 27.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLOR_SAFE, mutation_scale=10), zorder=5)
    ax.text(82.5, 24.5, r"$p_1 < \tau_2$", ha="center", va="center", fontsize=5.0, fontweight="bold",
            color=COLOR_SAFE, bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=0.6), zorder=6)

    # =========================================================================
    # COLUMN 5: THREE-TIER OPERATIONAL OUTCOMES (X in [85.5, 98.2])
    # =========================================================================
    # Tier 1 (Top): Illicit Quarantine & Autonomous Freeze
    draw_endpoint(
        ax, x=85.5, y=68.0, w=12.7, h=18.0,
        tier_label="TIER 1: QUARANTINE",
        pct_label="0.18% Traffic (18 / 10k)",
        subtext="Autonomous Sub-Second Hold",
        items=[
            "• Instant Capital Freeze",
            "• Merkle Audit Logged",
            "• Zero Fund Escape"
        ],
        border_color=COLOR_RISK,
        fill_color=COLOR_RISK_BG,
        text_color=COLOR_RISK
    )

    # Tier 2 (Middle): Assisted Human-Agent Forensic Desk
    draw_endpoint(
        ax, x=85.5, y=43.0, w=12.7, h=18.0,
        tier_label="TIER 2: ASSISTED DESK",
        pct_label="0.49% Traffic (49 / 10k)",
        subtext="Human-in-the-Loop Review",
        items=[
            "• 4-Agent Forensic Swarm",
            "• Auto-Drafted SAR Dossier",
            "• Four-Eyes Compliance Sign"
        ],
        border_color=COLOR_REVIEW,
        fill_color=COLOR_REVIEW_BG,
        text_color=COLOR_REVIEW
    )

    # Tier 3 (Bottom): Straight-Through Processing (STP)
    draw_endpoint(
        ax, x=85.5, y=18.0, w=12.7, h=18.0,
        tier_label="TIER 3: STRAIGHT-THROUGH",
        pct_label="99.33% Traffic (9,933 / 10k)",
        subtext="Instant Frictionless Flow",
        items=[
            "• Zero Customer Delay",
            "• 0.45 ms Fast-Path Latency",
            "• 99.50%+ Queue Cut"
        ],
        border_color=COLOR_SAFE,
        fill_color=COLOR_SAFE_BG,
        text_color=COLOR_SAFE
    )

    # =========================================================================
    # BOTTOM SLA & PERFORMANCE FOOTER STRIP (Y in [2.5, 12.5])
    # =========================================================================
    footer_cards = [
        {
            "x": 1.8, "w": 30.5,
            "title": "HIGH-VELOCITY SYSTEM SLA BENCHMARKS",
            "lines": [
                "• DuckDB 2-Hop LRU: 0.18 ms | Fast-Path Total: 0.45 ms",
                "• Ingestion Throughput: 31,250 tx/s | Zero-Copy Apache Arrow"
            ],
            "border": COLOR_INGEST, "bg": COLOR_INGEST_BG
        },
        {
            "x": 34.0, "w": 31.0,
            "title": "MATHEMATICAL & STATISTICAL GUARANTEES",
            "lines": [
                r"• Class-Conditional CRC: Finite-Sample Bound $\mathbb{E}[L] \leq \alpha$",
                r"• 12-D Flow Invariants: Strict Injectivity Beyond 1-WL Limit"
            ],
            "border": COLOR_GNN, "bg": COLOR_GNN_BG
        },
        {
            "x": 66.8, "w": 31.4,
            "title": "ENTERPRISE OPERATIONAL EFFICIENCY",
            "lines": [
                "• Straight-Through Rate: 99.33% | Manual Queue Reduced: 99.50%+",
                "• Cryptographic Integrity: Immutable SHA-256 Merkle Provenance"
            ],
            "border": COLOR_SAFE, "bg": COLOR_SAFE_BG
        }
    ]

    for fc in footer_cards:
        ax.add_patch(patches.FancyBboxPatch(
            (fc["x"], 2.5), fc["w"], 10.0,
            boxstyle="round,pad=0.15,rounding_size=0.5",
            facecolor=fc["bg"], edgecolor=fc["border"], lw=0.9, zorder=2
        ))
        ax.text(fc["x"] + fc["w"] / 2, 10.5, fc["title"], ha="center", va="center",
                fontsize=5.8, fontweight="bold", color=COLOR_DARK, zorder=3)
        ax.text(fc["x"] + fc["w"] / 2, 7.8, fc["lines"][0], ha="center", va="center",
                fontsize=5.0, color="#334155", zorder=3)
        ax.text(fc["x"] + fc["w"] / 2, 5.2, fc["lines"][1], ha="center", va="center",
                fontsize=5.0, color="#334155", zorder=3)

    # Save to all target figure repositories
    save_figure(fig, "fig3_1_tensor_flow", pad_inches=0.10)
    save_figure(fig, "fig13_tensor_flow", pad_inches=0.10)
    plt.close(fig)


if __name__ == "__main__":
    generate()
