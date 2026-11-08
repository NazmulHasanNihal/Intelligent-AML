"""
Figure 2.1: Adversarial Camouflage Attack and C-STGB Edge-Trust Pruning Defense
Standalone publication script for C-STGB monograph.
Human-made, practical banking diagram with intuitive accounts, clean topology, and zero generative artifacts.
Enlarged canvas with reduced, perfectly fitted text.
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

def draw_account_box(ax, x, y, w, h, name, role, fg, bg, border):
    """Draws a clean, human-designed banking account node."""
    ax.add_patch(patches.Rectangle(
        (x - w/2, y - h/2), w, h,
        facecolor=bg, edgecolor=border, lw=1.2, zorder=4
    ))
    # Top header strip
    ax.add_patch(patches.Rectangle(
        (x - w/2, y + h/2 - 0.042), w, 0.042,
        facecolor=fg, edgecolor="none", zorder=5
    ))
    ax.text(x, y + h/2 - 0.021, name, ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff", zorder=6)
    ax.text(x, y - 0.012, role, ha="center", va="center", fontsize=5.8, color=COLOR_DARK, fontweight="normal", zorder=6)

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.6), dpi=300)

    for ax in axes:
        ax.axis("off")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)

    # -------------------------------------------------------------
    # Common Node Layout (Normalized [0, 1] coordinates)
    # -------------------------------------------------------------
    pos = {
        "Source": (0.12, 0.72),
        "Mule1":  (0.38, 0.85),
        "Mule2":  (0.38, 0.58),
        "Wash":   (0.66, 0.72),
        "Sink":   (0.90, 0.72),
        "Retail": (0.28, 0.22),
        "E-Comm": (0.68, 0.22),
    }

    node_w, node_h = 0.17, 0.11
    hub_w, hub_h = 0.21, 0.12

    # =============================================================
    # PANEL (A): CONVENTIONAL SURVEILLANCE UNDER CAMOUFLAGE ATTACK
    # =============================================================
    ax0 = axes[0]
    ax0.add_patch(patches.Rectangle((0.00, 0.00), 1.00, 1.00, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))
    
    # Header banner
    ax0.add_patch(patches.Rectangle((0.00, 0.92), 1.00, 0.08, facecolor="#fef2f2", edgecolor="#fca5a5", lw=0.8))
    ax0.text(0.50, 0.960, "(a) Adversarial Camouflage Attack (Standard GNN Failure)",
             ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_RISK)

    # Legitimate customer traffic to merchants
    for ox in [-0.07, 0.0, 0.07]:
        ax0.annotate("", xy=(pos["Retail"][0] + ox, pos["Retail"][1] + hub_h/2),
                     xytext=(pos["Retail"][0] + ox*1.4, 0.04),
                     arrowprops=dict(arrowstyle="->", lw=0.9, color="#94a3b8"))
        ax0.annotate("", xy=(pos["E-Comm"][0] + ox, pos["E-Comm"][1] + hub_h/2),
                     xytext=(pos["E-Comm"][0] + ox*1.4, 0.04),
                     arrowprops=dict(arrowstyle="->", lw=0.9, color="#94a3b8"))
    ax0.text(0.48, 0.05, "Thousands of Legitimate Shopper Purchases ($10 - $50)",
             ha="center", va="center", fontsize=6.0, color="#64748b", style="italic")

    # Criminal Smurfing Backbone
    criminal_wires = [
        ("Source", "Mule1", "$9,850"),
        ("Source", "Mule2", "$9,900"),
        ("Mule1",  "Wash",  "$9,800"),
        ("Mule2",  "Wash",  "$9,850"),
        ("Wash",   "Sink",  "$19,650"),
    ]
    for src, dst, amt in criminal_wires:
        p1, p2 = pos[src], pos[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="-|>", lw=2.2, color=COLOR_RISK, mutation_scale=11), zorder=2)

    # Camouflage Chaff
    chaff_edges = [
        ("Mule1", "Retail", "Fake $15"),
        ("Mule2", "Retail", "Fake $20"),
        ("Mule2", "E-Comm", "Fake $18"),
        ("Wash",  "E-Comm", "Fake $12"),
    ]
    for src, dst, lbl in chaff_edges:
        p1, p2 = pos[src], pos[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#f87171", linestyle="--", mutation_scale=10), zorder=2)

    # Draw Nodes
    draw_account_box(ax0, pos["Source"][0], pos["Source"][1], node_w, node_h, "Source Fund", "Placement Cash", COLOR_RISK, COLOR_RISK_BG, COLOR_RISK)
    draw_account_box(ax0, pos["Mule1"][0],  pos["Mule1"][1],  node_w, node_h, "Smurf Mule 1", "Conduit Account", COLOR_RISK, COLOR_RISK_BG, COLOR_RISK)
    draw_account_box(ax0, pos["Mule2"][0],  pos["Mule2"][1],  node_w, node_h, "Smurf Mule 2", "Conduit Account", COLOR_RISK, COLOR_RISK_BG, COLOR_RISK)
    draw_account_box(ax0, pos["Wash"][0],   pos["Wash"][1],   node_w, node_h, "Layering Hub", "Rapid Wash Ring", COLOR_RISK, COLOR_RISK_BG, COLOR_RISK)
    draw_account_box(ax0, pos["Sink"][0],   pos["Sink"][1],   node_w, node_h, "Offshore Sink", "Cashout Shell Co", COLOR_DARK, "#f1f5f9", COLOR_DARK)

    # Merchant Hubs
    draw_account_box(ax0, pos["Retail"][0], pos["Retail"][1], hub_w, hub_h, "Retail Supermarket", "High-Degree Merchant", COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST)
    draw_account_box(ax0, pos["E-Comm"][0], pos["E-Comm"][1], hub_w, hub_h, "Online Marketplace", "High-Degree Merchant", COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST)

    # Explanatory Callout Box at bottom
    ax0.add_patch(patches.Rectangle((0.04, 0.38), 0.92, 0.12, facecolor="#fff1f2", edgecolor=COLOR_RISK, lw=1.0, zorder=7))
    ax0.text(0.50, 0.455, "Standard GNN Failure: Feature Camouflage Dilution",
             ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_RISK, zorder=8)
    ax0.text(0.50, 0.410, "Fake $15 retail transactions blend mules into the legitimate shopping crowd.\nStandard GNNs average neighbor features, completely missing the $9,800 laundering loop!",
             ha="center", va="center", fontsize=6.0, color=COLOR_DARK, zorder=8, linespacing=1.2)

    # =============================================================
    # PANEL (B): C-STGB LEARNABLE EDGE-TRUST PRUNING DEFENSE
    # =============================================================
    ax1 = axes[1]
    ax1.add_patch(patches.Rectangle((0.00, 0.00), 1.00, 1.00, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=1.0))
    
    # Header banner
    ax1.add_patch(patches.Rectangle((0.00, 0.92), 1.00, 0.08, facecolor="#f0fdf4", edgecolor="#86efac", lw=0.8))
    ax1.text(0.50, 0.960, "(b) C-STGB Defense: Learnable Edge-Trust Gating",
             ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_SAFE)

    # Legitimate customer traffic
    for ox in [-0.07, 0.0, 0.07]:
        ax1.annotate("", xy=(pos["Retail"][0] + ox, pos["Retail"][1] + hub_h/2),
                     xytext=(pos["Retail"][0] + ox*1.4, 0.04),
                     arrowprops=dict(arrowstyle="->", lw=0.9, color="#94a3b8"))
        ax1.annotate("", xy=(pos["E-Comm"][0] + ox, pos["E-Comm"][1] + hub_h/2),
                     xytext=(pos["E-Comm"][0] + ox*1.4, 0.04),
                     arrowprops=dict(arrowstyle="->", lw=0.9, color="#94a3b8"))
    ax1.text(0.48, 0.05, "Legitimate Commercial Flow Preserved Unchanged",
             ha="center", va="center", fontsize=6.0, color="#15803d", style="italic")

    # Criminal Smurfing Backbone Retained & Highlighted
    for src, dst, amt in criminal_wires:
        p1, p2 = pos[src], pos[dst]
        ax1.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="-|>", lw=2.4, color=COLOR_SAFE, mutation_scale=12), zorder=2)

    # Chaff Edges Soft-Pruned
    for src, dst, lbl in chaff_edges:
        p1, p2 = pos[src], pos[dst]
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        ax1.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#cbd5e1", linestyle=":", mutation_scale=8), zorder=2)
        ax1.text(mid_x, mid_y, "Pruned", ha="center", va="center", fontsize=5.6, fontweight="bold",
                 color="#ef4444", bbox=dict(boxstyle="square,pad=0.15", fc="#fee2e2", ec="#ef4444", lw=0.6), zorder=5)

    # Draw Nodes
    draw_account_box(ax1, pos["Source"][0], pos["Source"][1], node_w, node_h, "Source Fund", "Quarantined Node", COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE)
    draw_account_box(ax1, pos["Mule1"][0],  pos["Mule1"][1],  node_w, node_h, "Smurf Mule 1", "Identified Mule", COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE)
    draw_account_box(ax1, pos["Mule2"][0],  pos["Mule2"][1],  node_w, node_h, "Smurf Mule 2", "Identified Mule", COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE)
    draw_account_box(ax1, pos["Wash"][0],   pos["Wash"][1],   node_w, node_h, "Layering Hub", "Unmasked Ring", COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE)
    draw_account_box(ax1, pos["Sink"][0],   pos["Sink"][1],   node_w, node_h, "Offshore Sink", "Freezable Asset", COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE)

    # Merchant Hubs
    draw_account_box(ax1, pos["Retail"][0], pos["Retail"][1], hub_w, hub_h, "Retail Supermarket", "Zero Disruption", COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST)
    draw_account_box(ax1, pos["E-Comm"][0], pos["E-Comm"][1], hub_w, hub_h, "Online Marketplace", "Zero Disruption", COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST)

    # Explanatory Callout Box at bottom
    ax1.add_patch(patches.Rectangle((0.04, 0.38), 0.92, 0.12, facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.0, zorder=7))
    ax1.text(0.50, 0.455, "C-STGB Defense: Invariant-Guided Edge-Trust Pruning",
             ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_SAFE, zorder=8)
    ax1.text(0.50, 0.410, "Learnable gating heads detect flow inconsistencies and suppress 65.9% of camouflage noise.\nThe laundering ring is unmasked with 99.33% straight-through accuracy!",
             ha="center", va="center", fontsize=6.0, color=COLOR_DARK, zorder=8, linespacing=1.2)

    save_figure(fig, "fig21_adversarial_camouflage_topology", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
