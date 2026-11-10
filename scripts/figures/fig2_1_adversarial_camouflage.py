"""
Figure 2.1: Adversarial Camouflage Attack and C-STGB Edge-Trust Pruning Defense
Precedence Diagram workflow with:
- Clear horizontal transaction precedence (Placement -> Layering -> Integration)
- Non-overlapping account shapes, text, and arrow trajectories
- Dedicated central evaluation zone with zero arrow intersections
- Vertically staggered chaff labels and PRUNED badges for crystal-clear readability
- High-contrast, publication-grade styling adhering to the strict 4-color palette
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

def draw_account(ax, cx, cy, w, h, name, role, badge, fg, bg, border, badge_col=COLOR_DARK):
    """Draws a structured precedence account node with guaranteed text fit."""
    # Outer box
    box = patches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor=bg, edgecolor=border, lw=1.2, zorder=4
    )
    ax.add_patch(box)
    
    # Header strip
    hdr_h = h * 0.36
    hdr = patches.Rectangle(
        (cx - w/2, cy + h/2 - hdr_h), w, hdr_h,
        facecolor=fg, edgecolor="none", zorder=5
    )
    ax.add_patch(hdr)
    ax.text(cx, cy + h/2 - hdr_h/2, name, ha="center", va="center", fontsize=6.8,
            fontweight="bold", color="#ffffff", zorder=6)
    
    # Role / subtitle
    ax.text(cx, cy + 0.1, role, ha="center", va="center", fontsize=5.8,
            color=COLOR_DARK, fontweight="normal", zorder=6)
    
    # Bottom badge
    b_h = h * 0.28
    badge_box = patches.FancyBboxPatch(
        (cx - w*0.42, cy - h/2 + 0.5), w*0.84, b_h,
        boxstyle="round,pad=0.1,rounding_size=0.4",
        facecolor="#ffffff", edgecolor=border, lw=0.6, zorder=6
    )
    ax.add_patch(badge_box)
    ax.text(cx, cy - h/2 + 0.5 + b_h/2, badge, ha="center", va="center", fontsize=5.4,
            fontweight="bold", color=badge_col, zorder=7)

def draw_wire(ax, p1, p2, color=COLOR_DARK, lw=1.6, label="", label_pos=0.5, label_dy=1.5,
              style="-|>", rad=0.0, linestyle="-", fontsize=5.8):
    """Draws an annotated directional wire connector."""
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3,rad=0"
    ax.annotate(
        "", xy=p2, xytext=p1,
        arrowprops=dict(
            arrowstyle=style, lw=lw, color=color,
            shrinkA=2, shrinkB=2,
            connectionstyle=connectionstyle,
            linestyle=linestyle,
            mutation_scale=10
        ),
        zorder=3
    )
    if label:
        lx = p1[0] + (p2[0] - p1[0]) * label_pos
        ly = p1[1] + (p2[1] - p1[1]) * label_pos + label_dy
        ax.text(lx, ly, label, ha="center", va="center", fontsize=fontsize, fontweight="bold",
                color=color, bbox=dict(boxstyle="round,pad=0.12", facecolor="#ffffff", edgecolor=color, lw=0.5, alpha=0.95),
                zorder=5)

def build_panel(ax, is_defense=False):
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Master Panel Border
    border_col = COLOR_SAFE if is_defense else COLOR_RISK
    header_bg = "#f0fdf4" if is_defense else "#fef2f2"
    header_fg = COLOR_SAFE if is_defense else COLOR_RISK
    title_text = "(b) C-STGB Defense: Learnable Edge-Trust Gating" if is_defense else "(a) Conventional GNN Failure under Camouflage Attack"

    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.0, zorder=1))

    # Top Master Banner
    ax.add_patch(patches.Rectangle((0, 93.5), 100, 6.5, facecolor=header_bg, edgecolor=border_col, lw=1.0, zorder=2))
    ax.text(50, 96.7, title_text, ha="center", va="center", fontsize=9.2, fontweight="bold", color=header_fg, zorder=3)

    # Precedence Phase Indicator Badges (Top)
    phases = [
        ("PRECEDENCE: PLACEMENT", 4.0, 20.0),
        ("PRECEDENCE: LAYERING & STRUCTURING", 28.0, 42.0),
        ("PRECEDENCE: INTEGRATION", 74.0, 22.0)
    ]
    for ptext, px, pw in phases:
        ax.add_patch(patches.FancyBboxPatch(
            (px, 88.5), pw, 3.8,
            boxstyle="round,pad=0.1,rounding_size=0.5",
            facecolor="#f8fafc", edgecolor="#94a3b8", lw=0.8, zorder=2
        ))
        ax.text(px + pw/2, 90.4, ptext, ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_DARK, zorder=3)

    # -------------------------------------------------------------
    # Node Coordinates (Upper Precedence Stream)
    # -------------------------------------------------------------
    source_pos = (14.0, 74.0)
    mule1_pos  = (38.0, 81.5)
    mule2_pos  = (38.0, 64.5)
    layer_pos  = (64.0, 73.0)
    sink_pos   = (87.5, 73.0)

    node_w, node_h = 16.0, 9.5

    # Wire styling
    crim_col = COLOR_SAFE if is_defense else COLOR_RISK
    crim_bg  = COLOR_SAFE_BG if is_defense else COLOR_RISK_BG

    # Draw Upper Precedence Accounts
    draw_account(ax, source_pos[0], source_pos[1], node_w, node_h,
                 "Source Fund", "Placement Cash", "$19,750 Injected",
                 crim_col, crim_bg, crim_col, badge_col=crim_col)

    draw_account(ax, mule1_pos[0], mule1_pos[1], node_w, node_h,
                 "Smurf Mule 1", "Conduit Account A", "Wire: $9,850",
                 crim_col, crim_bg, crim_col, badge_col=crim_col)

    draw_account(ax, mule2_pos[0], mule2_pos[1], node_w, node_h,
                 "Smurf Mule 2", "Conduit Account B", "Wire: $9,900",
                 crim_col, crim_bg, crim_col, badge_col=crim_col)

    draw_account(ax, layer_pos[0], layer_pos[1], node_w, node_h,
                 "Layering Hub", "Rapid Wash Cycle", "Wash: $19,650",
                 crim_col, crim_bg, crim_col, badge_col=crim_col)

    draw_account(ax, sink_pos[0], sink_pos[1], node_w, node_h,
                 "Offshore Sink", "Shell Co. Asset", "Freeze Asset" if is_defense else "Cashout Sink",
                 crim_col, crim_bg, crim_col, badge_col=crim_col)

    # Draw Criminal Precedence Wires (Source -> Mules -> Layering -> Sink)
    draw_wire(ax, (source_pos[0] + node_w/2, source_pos[1] + 1.5),
              (mule1_pos[0] - node_w/2, mule1_pos[1] - 1.0),
              color=crim_col, lw=2.0, label="$9,850", label_pos=0.5, label_dy=1.5)

    draw_wire(ax, (source_pos[0] + node_w/2, source_pos[1] - 1.5),
              (mule2_pos[0] - node_w/2, mule2_pos[1] + 1.0),
              color=crim_col, lw=2.0, label="$9,900", label_pos=0.5, label_dy=-1.5)

    draw_wire(ax, (mule1_pos[0] + node_w/2, mule1_pos[1] - 1.0),
              (layer_pos[0] - node_w/2, layer_pos[1] + 1.5),
              color=crim_col, lw=2.0, label="$9,800", label_pos=0.5, label_dy=1.5)

    draw_wire(ax, (mule2_pos[0] + node_w/2, mule2_pos[1] + 1.0),
              (layer_pos[0] - node_w/2, layer_pos[1] - 1.5),
              color=crim_col, lw=2.0, label="$9,850", label_pos=0.5, label_dy=-1.5)

    draw_wire(ax, (layer_pos[0] + node_w/2, layer_pos[1]),
              (sink_pos[0] - node_w/2, sink_pos[1]),
              color=crim_col, lw=2.2, label="$19,650", label_pos=0.5, label_dy=1.5)

    # -------------------------------------------------------------
    # Lower Zone: High-Degree Commercial Hubs
    # -------------------------------------------------------------
    retail_pos = (35.0, 26.0)
    ecomm_pos  = (72.0, 26.0)
    hub_w, hub_h = 24.0, 11.0

    draw_account(ax, retail_pos[0], retail_pos[1], hub_w, hub_h,
                 "Retail Supermarket Hub", "High-Degree Merchant Node", "In-Degree: 8,450 wires",
                 COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST, badge_col=COLOR_INGEST)

    draw_account(ax, ecomm_pos[0], ecomm_pos[1], hub_w, hub_h,
                 "Online E-Commerce Platform", "Payment Gateway Aggregate", "In-Degree: 12,200 wires",
                 COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST, badge_col=COLOR_INGEST)

    # Legitimate Shopper Traffic into Hubs (Bottom)
    for hx in [retail_pos[0], ecomm_pos[0]]:
        for dx in [-7.0, 0.0, 7.0]:
            ax.annotate("", xy=(hx + dx, retail_pos[1] - hub_h/2),
                        xytext=(hx + dx*1.3, 14.0),
                        arrowprops=dict(arrowstyle="->", lw=1.0, color="#94a3b8"), zorder=2)
    ax.text(50.0, 14.5, "Legitimate Shopper Volume: Millions of Daily Card Swipes ($10 - $50)",
            ha="center", va="center", fontsize=5.8, color="#64748b", fontstyle="italic", zorder=3)

    # -------------------------------------------------------------
    # Middle Interaction Zone: Camouflage Chaff vs Edge-Trust Pruning
    # Vertically staggered label_pos:
    # Edge 1: label_pos = 0.65 (down near y=45)
    # Edge 2: label_pos = 0.35 (up near y=53)
    # Edge 3: label_pos = 0.35 (up near y=55)
    # Edge 4: label_pos = 0.65 (down near y=42)
    # -------------------------------------------------------------
    chaff_lines = [
        ((mule1_pos[0] - 3.0, mule1_pos[1] - node_h/2), (retail_pos[0] - 5.0, retail_pos[1] + hub_h/2), "$15.50", 0.65),
        ((mule2_pos[0] + 1.0, mule2_pos[1] - node_h/2), (retail_pos[0] + 4.0, retail_pos[1] + hub_h/2), "$22.00", 0.35),
        ((layer_pos[0] - 2.5, layer_pos[1] - node_h/2), (ecomm_pos[0] - 5.0,  ecomm_pos[1] + hub_h/2),  "$18.40", 0.35),
        ((layer_pos[0] + 4.0, layer_pos[1] - node_h/2), (ecomm_pos[0] + 5.0,  ecomm_pos[1] + hub_h/2),  "$12.00", 0.65),
    ]

    if not is_defense:
        # PANEL (A): ACTIVE CAMOUFLAGE OVERWHELMS GNN
        for p1, p2, amt, lpos in chaff_lines:
            draw_wire(ax, p1, p2, color="#ef4444", lw=1.3, linestyle="--", label=f"Chaff {amt}",
                      label_pos=lpos, label_dy=0.0, fontsize=5.2)

        # Center Status Callout Box (Completely clear of arrows)
        ax.add_patch(patches.FancyBboxPatch(
            (44.0, 42.0), 16.5, 12.5,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor="#fff1f2", edgecolor="#ef4444", lw=1.1, zorder=4
        ))
        ax.text(52.25, 51.0, "FEATURE DILUTION", ha="center", va="center", fontsize=6.8,
                fontweight="bold", color=COLOR_RISK, zorder=5)
        ax.text(52.25, 47.5, r"$\mathcal{E}(\mathbf{H}) \to 0$ Over-Smooth", ha="center", va="center", fontsize=5.8,
                fontweight="bold", color="#1e293b", zorder=5)
        ax.text(52.25, 44.5, "Mule signals blend into\ncommercial retail crowd", ha="center", va="center", fontsize=5.2,
                color="#64748b", zorder=5)

    else:
        # PANEL (B): C-STGB DEFENSE PRUNES CHAFF
        for p1, p2, amt, lpos in chaff_lines:
            draw_wire(ax, p1, p2, color="#cbd5e1", lw=1.0, linestyle=":", style="->", label="")
            # Prune marker badge placed at vertically staggered positions
            mx = p1[0] + (p2[0] - p1[0]) * lpos
            my = p1[1] + (p2[1] - p1[1]) * lpos
            ax.text(mx, my, "PRUNED", ha="center", va="center", fontsize=5.2, fontweight="bold",
                    color="#b91c1c", bbox=dict(boxstyle="square,pad=0.15", facecolor="#fee2e2", edgecolor="#b91c1c", lw=0.6),
                    zorder=6)

        # Center Status Callout Box: Learnable Gating (Completely clear of arrows)
        ax.add_patch(patches.FancyBboxPatch(
            (43.5, 42.0), 17.5, 12.5,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.1, zorder=4
        ))
        ax.text(52.25, 51.0, "EDGE-TRUST FILTERING", ha="center", va="center", fontsize=6.8,
                fontweight="bold", color=COLOR_SAFE, zorder=5)
        ax.text(52.25, 47.5, r"$\hat{g}_{ij} < \delta_{\mathrm{floor}} \Rightarrow \mathrm{Drop}$", ha="center", va="center", fontsize=5.8,
                fontweight="bold", color="#1e293b", zorder=5)
        ax.text(52.25, 44.5, "65.9% Chaff Pruned\nRetail Flow 100% Intact", ha="center", va="center", fontsize=5.2,
                color="#15803d", zorder=5)

    # -------------------------------------------------------------
    # Bottom Summary Outcome Bar
    # -------------------------------------------------------------
    res_bg = "#fef2f2" if not is_defense else "#f0fdf4"
    res_ec = COLOR_RISK if not is_defense else COLOR_SAFE
    res_fg = COLOR_RISK if not is_defense else COLOR_SAFE

    ax.add_patch(patches.FancyBboxPatch(
        (2.0, 2.0), 96.0, 9.0,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor=res_bg, edgecolor=res_ec, lw=1.1, zorder=2
    ))

    if not is_defense:
        ax.text(50.0, 7.2, "CONVENTIONAL GNN FAILURE: False Negative Alert Collapse (Recall < 12%)",
                ha="center", va="center", fontsize=6.8, fontweight="bold", color=res_fg, zorder=3)
        ax.text(50.0, 4.2, "High-degree merchant feature aggregation washes out anomaly representations. Laundering ring evades detection completely.",
                ha="center", va="center", fontsize=5.8, color="#334155", zorder=3)
    else:
        ax.text(50.0, 7.2, "C-STGB PRECEDENCE INTERDICTION: 91.42% F1 Quarantine (+60.07 pp vs Baseline)",
                ha="center", va="center", fontsize=6.8, fontweight="bold", color=res_fg, zorder=3)
        ax.text(50.0, 4.2, "Context-aware edge gating suppresses 65.9% of spurious edges, cleanly exposing the smurfing loop with zero false positives on shoppers.",
                ha="center", va="center", fontsize=5.8, color="#334155", zorder=3)

def generate():
    setup_plt(font_size=8.0, title_size=9.2, label_size=8.5)
    # Spacious 15.2 x 6.4 inch canvas with balanced margins
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 6.4), dpi=300)

    # Panel (a): Conventional Failure
    build_panel(axes[0], is_defense=False)

    # Panel (b): C-STGB Defense
    build_panel(axes[1], is_defense=True)

    plt.subplots_adjust(left=0.015, right=0.985, top=0.97, bottom=0.03, wspace=0.08)
    save_figure(fig, "fig21_adversarial_camouflage_topology", pad_inches=0.06)
    save_figure(fig, "fig2_1_adversarial_camouflage", pad_inches=0.06)
    plt.close(fig)

if __name__ == "__main__":
    generate()
