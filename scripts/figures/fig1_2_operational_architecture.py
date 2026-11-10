"""
Figure 1.2: C-STGB End-to-End Operational Architecture & Real-Time Flowchart Workflow.
Redesigned from static cards into an authentic, publication-grade diagram workflow.
Features:
- Perfectly fitted labels without any overlap or text clipping
- Clean directional flow from multi-rail streaming ingestion to CRC 3-tier triage
- Standard database cylinders, structured process nodes, decision diamond, and outcome endpoints
- Cryptographic Merkle Seal regulatory governance banner
- Three-column quantitative SLA benchmark footer
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

def draw_cylinder(ax, x, y, w, h, facecolor, edgecolor, lw=1.2, label_top="", label_bottom=""):
    """Draws a standard data storage / event stream cylinder symbol."""
    cap_h = h * 0.16
    # Body
    rect = patches.Rectangle((x, y + cap_h/2), w, h - cap_h, facecolor=facecolor, edgecolor="none", zorder=2)
    ax.add_patch(rect)
    # Side lines
    ax.plot([x, x], [y + cap_h/2, y + h - cap_h/2], color=edgecolor, lw=lw, zorder=3)
    ax.plot([x + w, x + w], [y + cap_h/2, y + h - cap_h/2], color=edgecolor, lw=lw, zorder=3)
    # Bottom ellipse (half visible)
    bottom_arc = patches.Arc((x + w/2, y + cap_h/2), w, cap_h, angle=0, theta1=180, theta2=360,
                             color=edgecolor, lw=lw, zorder=3)
    ax.add_patch(bottom_arc)
    bottom_fill = patches.Ellipse((x + w/2, y + cap_h/2), w, cap_h, facecolor=facecolor, edgecolor="none", zorder=2)
    ax.add_patch(bottom_fill)
    # Top ellipse
    top_ellipse = patches.Ellipse((x + w/2, y + h - cap_h/2), w, cap_h, facecolor=facecolor,
                                  edgecolor=edgecolor, lw=lw, zorder=4)
    ax.add_patch(top_ellipse)
    if label_top:
        ax.text(x + w/2, y + h*0.50, label_top, ha="center", va="center", fontsize=6.3, fontweight="bold",
                color=COLOR_DARK, zorder=5)
    if label_bottom:
        ax.text(x + w/2, y + h*0.26, label_bottom, ha="center", va="center", fontsize=5.2,
                color=COLOR_MUTED, zorder=5)

def draw_process_node(ax, x, y, w, h, title, subtitle, items, border_color, fill_color, title_color, badge=None):
    """Draws a spacious workflow process node with internal specifications."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.9",
        facecolor=fill_color, edgecolor=border_color, lw=1.3, zorder=2
    )
    ax.add_patch(box)
    
    # Header divider line
    ax.plot([x + 0.5, x + w - 0.5], [y + h - 5.0, y + h - 5.0], color=border_color, lw=0.8, alpha=0.5, zorder=3)
    
    # Title & Subtitle
    ax.text(x + w/2, y + h - 2.4, title, ha="center", va="center", fontsize=7.4, fontweight="bold",
            color=title_color, zorder=4)
    ax.text(x + w/2, y + h - 3.9, subtitle, ha="center", va="center", fontsize=5.8, fontstyle="italic",
            color=COLOR_MUTED, zorder=4)
    
    # Itemized steps inside node
    n_items = len(items)
    step_y = (h - 9.0) / max(n_items, 1)
    for i, itxt in enumerate(items):
        cur_y = (y + h - 6.4) - (i + 0.5) * step_y
        ax.plot([x + 1.0], [cur_y], marker=">", markersize=2.8, color=border_color, zorder=4)
        ax.text(x + 1.8, cur_y, itxt, ha="left", va="center", fontsize=5.7, color="#1e293b", zorder=4)
        
    # SLA/Tech Badge at bottom
    if badge:
        bw = w - 2.0
        badge_box = patches.FancyBboxPatch(
            (x + 1.0, y + 0.9), bw, 2.8,
            boxstyle="round,pad=0.1,rounding_size=0.5",
            facecolor="#ffffff", edgecolor=border_color, lw=0.8, zorder=4
        )
        ax.add_patch(badge_box)
        ax.text(x + w/2, y + 2.3, badge, ha="center", va="center", fontsize=5.8, fontweight="bold",
                color=border_color, zorder=5)

def draw_diamond(ax, cx, cy, rx, ry, title, subtitle, fill_color, border_color):
    """Draws a decision diamond for Conformal Risk Control."""
    pts = np.array([
        [cx - rx, cy],
        [cx, cy + ry],
        [cx + rx, cy],
        [cx, cy - ry]
    ])
    diamond = patches.Polygon(pts, facecolor=fill_color, edgecolor=border_color, lw=1.6, zorder=3)
    ax.add_patch(diamond)
    ax.text(cx, cy + 1.4, title, ha="center", va="center", fontsize=7.0, fontweight="bold",
            color=border_color, zorder=4)
    ax.text(cx, cy - 1.6, subtitle, ha="center", va="center", fontsize=5.6, fontstyle="italic",
            color=COLOR_DARK, zorder=4)

def draw_pipe(ax, p1, p2, color=COLOR_DARK, lw=1.4, label="", label_pos=0.5, label_dy=1.4,
              style="-|>", rad=0.0, fontsize=5.6):
    """Draws an annotated directional workflow connector pipe."""
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3,rad=0"
    ax.annotate(
        "", xy=p2, xytext=p1,
        arrowprops=dict(
            arrowstyle=style, lw=lw, color=color,
            shrinkA=1, shrinkB=1,
            connectionstyle=connectionstyle,
            mutation_scale=10
        ),
        zorder=5
    )
    if label:
        lx = p1[0] + (p2[0] - p1[0]) * label_pos
        ly = p1[1] + (p2[1] - p1[1]) * label_pos + label_dy
        ax.text(lx, ly, label, ha="center", va="center", fontsize=fontsize, fontweight="bold",
                color=color, bbox=dict(boxstyle="round,pad=0.12", facecolor="#ffffff", edgecolor=color, lw=0.5, alpha=0.95),
                zorder=6)

def generate():
    setup_plt(font_size=8, title_size=10.0, label_size=8.5)
    # Spacious 15.6 x 6.8 inch canvas for clean workflow routing
    fig, ax = plt.subplots(figsize=(15.6, 6.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master Clean Background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Top Master Workflow Header
    ax.add_patch(patches.Rectangle(
        (1.0, 93.2), 98.0, 5.8,
        facecolor=COLOR_DARK, edgecolor="none", zorder=2
    ))
    ax.text(50.0, 96.6, "C-STGB END-TO-END OPERATIONAL ARCHITECTURE & HIGH-VELOCITY WORKFLOW",
            ha="center", va="center", fontsize=10.0, fontweight="bold", color="#ffffff", zorder=3)
    ax.text(50.0, 94.4, "Real-Time Pipeline: Multi-Rail Ingestion -> Physical Invariants -> Continuous GNN -> Bayes Fusion -> Conformal Triage",
            ha="center", va="center", fontsize=6.8, color="#94a3b8", zorder=3)

    # Phase Swimlane Banners
    phases = [
        ("STAGE 1: INGESTION & BUFFERS", 1.0, 15.8, COLOR_INGEST),
        ("STAGE 2: PHYSICAL INVARIANTS", 18.2, 17.5, COLOR_GNN),
        ("STAGE 3: NEURAL GNN & SMOTE", 37.2, 17.5, COLOR_GNN_PURPLE),
        ("STAGE 4: BAYES FUSION HEAD", 56.0, 13.5, COLOR_REVIEW),
        ("STAGE 5: CRC DECISION & TRIAGE", 70.8, 28.2, COLOR_SAFE)
    ]
    for ptitle, px, pw, pcol in phases:
        ax.add_patch(patches.FancyBboxPatch(
            (px, 88.5), pw, 3.6,
            boxstyle="round,pad=0.1,rounding_size=0.5",
            facecolor="#f8fafc", edgecolor=pcol, lw=1.1, zorder=2
        ))
        ax.text(px + pw/2, 90.3, ptitle, ha="center", va="center", fontsize=6.2, fontweight="bold",
                color=pcol, zorder=3)

    # =========================================================================
    # STAGE 1: INGESTION & STREAMING BUFFERS (X: 1.0 -> 16.8)
    # =========================================================================
    # Storage Cylinders (widened to 6.0 to give plenty of margin for text)
    draw_cylinder(ax, 1.2, 65.0, 6.0, 18.0, COLOR_INGEST_BG, COLOR_INGEST,
                  label_top="Kafka Stream", label_bottom="ISO 20022 Multi-Rail")
    draw_cylinder(ax, 1.2, 42.0, 6.0, 18.0, "#f1f5f9", COLOR_BORDER,
                  label_top="Historical DB", label_bottom="Neo4j Graph Store")

    # In-Memory Arrow & DuckDB Buffer Node
    draw_process_node(
        ax, 8.8, 45.0, 8.0, 38.0,
        "Arrow Buffer", "Zero-Copy In-Memory",
        [
            "PyArrow RecordBatches",
            "DuckDB Columnar Slices",
            "Sub-ms In-Memory View"
        ],
        COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST, badge="SLA: < 0.05 ms"
    )

    # Stream Feed Connectors (routed to clear cylinder text)
    draw_pipe(ax, (7.2, 74.0), (8.8, 70.0), color=COLOR_INGEST, label="Live Wires", label_pos=0.45, label_dy=1.5)
    draw_pipe(ax, (7.2, 51.0), (8.8, 54.0), color=COLOR_MUTED, label="Subgraphs", label_pos=0.45, label_dy=-1.5)

    # =========================================================================
    # STAGE 2: PHYSICAL INVARIANT ENGINE (X: 18.2 -> 35.7)
    # =========================================================================
    draw_process_node(
        ax, 18.2, 45.0, 17.5, 38.0,
        "12-D Canonical Invariant Engine", "Mass Conservation & Hawkes Dynamics",
        [
            "Kirchhoff Net Mass-Flow (Phi_flow)",
            "Hawkes Self-Exciting Arrival Intensity",
            "Fan-In / Fan-Out Velocity Ratios",
            "Cold-Start Tabular Feature Extraction"
        ],
        COLOR_GNN, COLOR_GNN_BG, COLOR_GNN, badge="Compute SLA: < 0.07 ms"
    )

    # Arrow from Stage 1 to Stage 2
    draw_pipe(ax, (16.8, 64.0), (18.2, 64.0), color=COLOR_INGEST, label="Batch", label_pos=0.5, label_dy=1.4)

    # =========================================================================
    # STAGE 3: GNN CORE & LATENT GRAPH-SMOTE (X: 37.2 -> 54.7)
    # =========================================================================
    # Continuous Temporal GNN Box
    draw_process_node(
        ax, 37.2, 47.0, 17.5, 36.0,
        "Continuous-Time GNN Core", "Harmonic Attention & Edge-Trust Gating",
        [
            "3-Band Temporal Fourier Waveforms",
            "Learnable Edge-Trust Gating (g_ij)",
            "65.9% Camouflage Chaff Pruned",
            "Dirichlet Energy Retention"
        ],
        COLOR_GNN_PURPLE, "#faf5ff", COLOR_GNN_PURPLE, badge="GNN SLA: < 0.16 ms"
    )

    # Offline Latent GraphSMOTE Auxiliary Component (Below GNN)
    smote_box = patches.FancyBboxPatch(
        (37.2, 22.0), 17.5, 21.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#fffbeb", edgecolor="#d97706", lw=1.1, linestyle="--", zorder=2
    )
    ax.add_patch(smote_box)
    ax.text(45.95, 40.0, "Latent Typology GraphSMOTE", ha="center", va="center", fontsize=6.8,
            fontweight="bold", color="#d97706", zorder=3)
    ax.text(45.95, 37.8, "[Offline Training Augmentation]", ha="center", va="center", fontsize=5.4,
            fontstyle="italic", color=COLOR_MUTED, zorder=3)
    ax.text(38.4, 33.6, "> K-Means Typology Clustering", fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(38.4, 30.0, "> Bilinear Edge Reconstruction", fontsize=5.8, color="#1e293b", zorder=3)
    ax.text(38.4, 26.4, "> Extreme Skew Rectification", fontsize=5.8, color="#1e293b", zorder=3)

    # Connector from Stage 2 to Stage 3 GNN
    draw_pipe(ax, (35.7, 64.0), (37.2, 64.0), color=COLOR_GNN, label="12-D", label_pos=0.5, label_dy=1.4)
    # Balanced weights flow from SMOTE to GNN
    draw_pipe(ax, (45.95, 43.0), (45.95, 47.0), color="#d97706", lw=1.2, style="-|>", label="Balanced Weights",
              label_pos=0.5, label_dy=0.0, fontsize=5.4)

    # =========================================================================
    # STAGE 4: EVIDENCE-ADAPTIVE BAYES FUSION HEAD (X: 56.0 -> 69.5)
    # =========================================================================
    draw_process_node(
        ax, 56.0, 45.0, 13.5, 38.0,
        "Bayes Fusion Head", "Evidence-Adaptive Gating",
        [
            "Dynamic Alpha-Gating Fusion",
            "Resolves Isolated Cold-Start",
            "Asymmetric Utility Loss Matrix",
            "Optimal Cutoff (Tau* = 0.18)"
        ],
        COLOR_REVIEW, COLOR_REVIEW_BG, COLOR_REVIEW, badge="Fusion SLA: < 0.04 ms"
    )

    # Arrow from GNN to Bayes Head
    draw_pipe(ax, (54.7, 64.0), (56.0, 64.0), color=COLOR_GNN_PURPLE, label="Embed", label_pos=0.5, label_dy=1.4)

    # =========================================================================
    # STAGE 5: CONFORMAL RISK CONTROL (CRC) DECISION DIAMOND & TRIAGE
    # (X: 71.0 -> 99.0)
    # =========================================================================
    # CRC Decision Diamond
    diamond_cx = 74.0
    diamond_cy = 64.0
    diamond_rx = 3.2
    diamond_ry = 9.5
    draw_diamond(ax, diamond_cx, diamond_cy, diamond_rx, diamond_ry,
                 "CRC TRIAGE", "Dual-Quantile", COLOR_SAFE_BG, COLOR_SAFE)

    # Arrow from Bayes Head to Diamond
    draw_pipe(ax, (69.5, 64.0), (diamond_cx - diamond_rx, 64.0), color=COLOR_REVIEW,
              label="Risk p", label_pos=0.5, label_dy=1.4)

    # Outcome boxes X & dimensions
    out_x = 83.5
    out_w = 15.3
    out_h = 13.5

    # 1. TOP BRANCH: Tier 1 Quarantined (High Risk / Auto-SAR)
    draw_pipe(ax, (diamond_cx, diamond_cy + diamond_ry), (out_x, 79.5),
              color=COLOR_RISK, lw=1.5, label="p >= q1 (0.18%)", label_pos=0.48, label_dy=1.8,
              style="-|>", rad=-0.08)

    t1_box = patches.FancyBboxPatch(
        (out_x, 73.0), out_w, out_h,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor=COLOR_RISK_BG, edgecolor=COLOR_RISK, lw=1.4, zorder=3
    )
    ax.add_patch(t1_box)
    ax.text(out_x + out_w/2, 84.0, "TIER 1: QUARANTINE", ha="center", va="center", fontsize=7.2, fontweight="bold",
            color=COLOR_RISK, zorder=4)
    ax.text(out_x + out_w/2, 81.8, "[Real-Time Interdiction]", ha="center", va="center", fontsize=5.6, fontstyle="italic",
            color=COLOR_DARK, zorder=4)
    ax.text(out_x + 1.2, 78.0, "> Immediate Wire Hold / Freeze", fontsize=5.8, color="#1e293b", zorder=4)
    ax.text(out_x + 1.2, 75.0, "> Assisted FinCEN SAR Dossier Desk", fontsize=5.8, color="#1e293b", zorder=4)

    # 2. MIDDLE BRANCH: Tier 2 Human Review (Uncertainty Band)
    draw_pipe(ax, (diamond_cx + diamond_rx, diamond_cy), (out_x, 62.0),
              color=COLOR_REVIEW, lw=1.5, label="q0 < p < q1", label_pos=0.46, label_dy=1.6)

    t2_box = patches.FancyBboxPatch(
        (out_x, 55.5), out_w, out_h,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor=COLOR_REVIEW_BG, edgecolor=COLOR_REVIEW, lw=1.4, zorder=3
    )
    ax.add_patch(t2_box)
    ax.text(out_x + out_w/2, 66.5, "TIER 2: COMPLIANCE DESK", ha="center", va="center", fontsize=7.2, fontweight="bold",
            color=COLOR_REVIEW, zorder=4)
    ax.text(out_x + out_w/2, 64.3, "[Human-in-the-Loop Review]", ha="center", va="center", fontsize=5.6, fontstyle="italic",
            color=COLOR_DARK, zorder=4)
    ax.text(out_x + 1.2, 60.5, "> 0.49% Workload Queue (49/10k)", fontsize=5.8, color="#1e293b", zorder=4)
    ax.text(out_x + 1.2, 57.5, "> Subgraph Explainability AST", fontsize=5.8, color="#1e293b", zorder=4)

    # 3. BOTTOM BRANCH: Tier 3 Straight-Through Processed (Benign Safe)
    draw_pipe(ax, (diamond_cx, diamond_cy - diamond_ry), (out_x, 44.5),
              color=COLOR_SAFE, lw=1.5, label="p <= q0 (99.33%)", label_pos=0.48, label_dy=-1.8,
              style="-|>", rad=0.08)

    t3_box = patches.FancyBboxPatch(
        (out_x, 38.0), out_w, out_h,
        boxstyle="round,pad=0.2,rounding_size=0.7",
        facecolor=COLOR_SAFE_BG, edgecolor=COLOR_SAFE, lw=1.4, zorder=3
    )
    ax.add_patch(t3_box)
    ax.text(out_x + out_w/2, 49.0, "TIER 3: STRAIGHT-THROUGH", ha="center", va="center", fontsize=7.2, fontweight="bold",
            color=COLOR_SAFE, zorder=4)
    ax.text(out_x + out_w/2, 46.8, "[Automated Instant Clearance]", ha="center", va="center", fontsize=5.6, fontstyle="italic",
            color=COLOR_DARK, zorder=4)
    ax.text(out_x + 1.2, 43.0, "> 99.33% Straight-Through Flow", fontsize=5.8, color="#1e293b", zorder=4)
    ax.text(out_x + 1.2, 40.0, "> Sub-ms Payment Release to Rails", fontsize=5.8, color="#1e293b", zorder=4)

    # =========================================================================
    # GOVERNANCE & AUDIT TRAIL RECTANGLE (Cryptographic Merkle Seal)
    # =========================================================================
    audit_box = patches.FancyBboxPatch(
        (56.0, 22.0), 42.8, 11.5,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.2, zorder=2
    )
    ax.add_patch(audit_box)
    ax.text(77.4, 30.6, "REGULATORY COMPLIANCE & CRYPTOGRAPHIC AUDIT TRACEABILITY",
            ha="center", va="center", fontsize=7.0, fontweight="bold", color=COLOR_DARK, zorder=3)
    ax.text(77.4, 27.6, "Fed SR 11-7 / SR 21-8 Model Risk Governance | FINRA Rule 3110 Supervisory Controls",
            ha="center", va="center", fontsize=5.9, color="#334155", zorder=3)
    ax.text(77.4, 24.6, "Immutable SHA-256 Merkle Ledger Audit Receipt generated for every quarantined wire and triage decision.",
            ha="center", va="center", fontsize=5.9, color="#334155", zorder=3)

    # Feedback/Audit connector from CRC to Governance
    draw_pipe(ax, (diamond_cx, diamond_cy - diamond_ry), (diamond_cx, 33.5),
              color=COLOR_BORDER, lw=1.2, style="-|>", label="Audit Log", label_pos=0.5, label_dy=0.0, fontsize=5.4)

    # =========================================================================
    # BOTTOM SUMMARY ARCHITECTURAL SLA SPECIFICATION BAR
    # =========================================================================
    ax.add_patch(patches.FancyBboxPatch(
        (1.0, 2.0), 98.0, 16.5,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.2, zorder=2
    ))
    
    # 3 Summary Column Cards inside Bottom Bar
    card_w = 31.0
    # Col 1: Fast-Path Latency Budget
    ax.add_patch(patches.Rectangle((2.2, 3.2), card_w, 13.8, facecolor="#ffffff", edgecolor=COLOR_INGEST, lw=0.9, zorder=3))
    ax.text(2.2 + card_w/2, 14.8, "FAST-PATH LATENCY BUDGET", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_INGEST, zorder=4)
    ax.text(3.4, 12.2, "> Total Pipeline Latency: 0.45 ms", fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=4)
    ax.text(3.4, 9.7, "> Ingestion: 0.11 ms | Invariants: 0.08 ms", fontsize=5.8, color="#475569", zorder=4)
    ax.text(3.4, 7.2, "> GNN: 0.16 ms | CRC Triage: 0.04 ms", fontsize=5.8, color="#475569", zorder=4)
    ax.text(3.4, 4.8, "> 22.2x Faster than 10.0 ms Enterprise Banking SLA", fontsize=5.6, fontstyle="italic", color=COLOR_INGEST, zorder=4)

    # Col 2: Conformal Coverage Guarantee
    ax.add_patch(patches.Rectangle((34.5, 3.2), card_w, 13.8, facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=0.9, zorder=3))
    ax.text(34.5 + card_w/2, 14.8, "STATISTICAL COVERAGE GUARANTEE", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_SAFE, zorder=4)
    ax.text(35.7, 12.2, "> Finite-Sample Risk Bound: 1 - alpha >= 99.0%", fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=4)
    ax.text(35.7, 9.7, "> Dvoretzky-Kiefer-Wolfowitz (DKW) Certified", fontsize=5.8, color="#475569", zorder=4)
    ax.text(35.7, 7.2, "> Adaptive Non-Stationarity Calibration (ACI)", fontsize=5.8, color="#475569", zorder=4)
    ax.text(35.7, 4.8, "> Zero False Clears on Coordinated Laundering Flows", fontsize=5.6, fontstyle="italic", color=COLOR_SAFE, zorder=4)

    # Col 3: Operational Triage Distribution
    ax.add_patch(patches.Rectangle((66.8, 3.2), card_w, 13.8, facecolor="#ffffff", edgecolor=COLOR_REVIEW, lw=0.9, zorder=3))
    ax.text(66.8 + card_w/2, 14.8, "OPERATIONAL STREAM VOLUMES", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_REVIEW, zorder=4)
    ax.text(68.0, 12.2, "> Straight-Through Flow: 99.33% (9,933 / 10k wires)", fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=4)
    ax.text(68.0, 9.7, "> Human Review Queue: 0.49% (49 / 10k wires)", fontsize=5.8, color="#475569", zorder=4)
    ax.text(68.0, 7.2, "> Automated Quarantine: 0.18% (18 / 10k wires)", fontsize=5.8, color="#475569", zorder=4)
    ax.text(68.0, 4.8, "> 91.8% Manual Compliance Backlog Reduction", fontsize=5.6, fontstyle="italic", color=COLOR_REVIEW, zorder=4)

    save_figure(fig, "fig1_operational_architecture_flowchart", pad_inches=0.08)
    save_figure(fig, "fig1_2_operational_architecture", pad_inches=0.08)
    plt.close(fig)

if __name__ == "__main__":
    generate()
