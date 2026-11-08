"""
Figure 3.1: End-to-End Architectural Dataflow of C-STGB
Standard 6-Module Publication-Grade Visual Pipeline
Phase 2 Overhaul: Sharp rectangular geometry, no embedded equations, strict 4-color palette.
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

def draw_cylinder(ax, x_center, y_bottom, width, height, facecolor, edgecolor):
    """Draws a clean database cylinder icon."""
    r_h = height * 0.18
    # Body
    ax.add_patch(patches.Rectangle(
        (x_center - width/2, y_bottom + r_h/2), width, height - r_h,
        facecolor=facecolor, edgecolor="none"
    ))
    # Left & right side lines
    ax.plot([x_center - width/2, x_center - width/2], [y_bottom + r_h/2, y_bottom + height - r_h/2], color=edgecolor, lw=1.2)
    ax.plot([x_center + width/2, x_center + width/2], [y_bottom + r_h/2, y_bottom + height - r_h/2], color=edgecolor, lw=1.2)
    # Bottom ellipse
    ax.add_patch(patches.Ellipse(
        (x_center, y_bottom + r_h/2), width, r_h,
        facecolor=facecolor, edgecolor=edgecolor, lw=1.2
    ))
    # Middle disk seam
    ax.add_patch(patches.Arc(
        (x_center, y_bottom + height*0.5), width, r_h,
        theta1=180, theta2=360, color=edgecolor, lw=1.0
    ))
    # Top ellipse
    ax.add_patch(patches.Ellipse(
        (x_center, y_bottom + height - r_h/2), width, r_h,
        facecolor=edgecolor, edgecolor=edgecolor, lw=1.2, alpha=0.3
    ))
    ax.add_patch(patches.Ellipse(
        (x_center, y_bottom + height - r_h/2), width, r_h,
        facecolor="none", edgecolor=edgecolor, lw=1.2
    ))

def draw_waveform(ax, x_left, y_mid, width, height, color):
    """Draws a continuous multi-harmonic sinusoidal wave."""
    xs = np.linspace(x_left, x_left + width, 80)
    ys = y_mid + (height/2.2) * (0.65 * np.sin(2 * np.pi * 2.2 * (xs - x_left) / width) +
                                  0.35 * np.sin(2 * np.pi * 5.0 * (xs - x_left) / width))
    ax.plot(xs, ys, color=color, lw=1.8)
    ax.plot([x_left, x_left + width], [y_mid, y_mid], color=COLOR_MUTED, linestyle=":", lw=0.8, alpha=0.7)

def draw_network_gate(ax, x_center, y_center, radius, color_keep, color_prune):
    """Draws a graph gating module with retained and pruned edges."""
    nodes = [
        (x_center - radius*0.8, y_center - radius*0.5),
        (x_center - radius*0.8, y_center + radius*0.5),
        (x_center + radius*0.8, y_center - radius*0.6),
        (x_center + radius*0.8, y_center + radius*0.6),
        (x_center, y_center)
    ]
    # Retained edges
    ax.plot([nodes[0][0], nodes[4][0]], [nodes[0][1], nodes[4][1]], color=color_keep, lw=1.6)
    ax.plot([nodes[1][0], nodes[4][0]], [nodes[1][1], nodes[4][1]], color=color_keep, lw=1.6)
    ax.plot([nodes[4][0], nodes[3][0]], [nodes[4][1], nodes[3][1]], color=color_keep, lw=1.6)
    # Pruned edge (dashed)
    ax.plot([nodes[4][0], nodes[2][0]], [nodes[4][1], nodes[2][1]], color=color_prune, lw=1.3, linestyle="--")
    # Draw nodes
    for i, (nx, ny) in enumerate(nodes):
        c = color_keep if i != 2 else color_prune
        ax.add_patch(patches.Circle((nx, ny), radius*0.22, facecolor="#ffffff", edgecolor=c, lw=1.4, zorder=4))
        ax.add_patch(patches.Circle((nx, ny), radius*0.11, facecolor=c, zorder=5))

def draw_smote_clusters(ax, x_center, y_center, span, color_synth, color_maj):
    """Draws minority synthesis cluster."""
    maj_pts = [(-0.6, 0.4), (-0.4, 0.7), (-0.7, 0.1), (-0.3, 0.3)]
    min_pts = [(0.3, -0.4), (0.7, -0.2), (0.5, -0.6)]
    synth_pts = [(0.42, -0.32), (0.58, -0.48)]
    for dx, dy in maj_pts:
        ax.add_patch(patches.Circle((x_center + dx*span, y_center + dy*span), span*0.12, facecolor=color_maj, edgecolor="none", alpha=0.6))
    for dx, dy in min_pts:
        ax.add_patch(patches.Circle((x_center + dx*span, y_center + dy*span), span*0.14, facecolor="#ffffff", edgecolor=color_synth, lw=1.5))
    for dx, dy in synth_pts:
        ax.add_patch(patches.Rectangle((x_center + dx*span - span*0.10, y_center + dy*span - span*0.10), span*0.20, span*0.20,
                                       facecolor=color_synth, edgecolor=COLOR_DARK, lw=0.9))

def draw_bayes_scale(ax, x_center, y_center, span, color):
    """Draws an asymmetric Bayes cost decision scale."""
    # Fulcrum triangle
    f_h = span * 0.45
    ax.add_patch(patches.Polygon([
        (x_center, y_center - span*0.1),
        (x_center - span*0.3, y_center - span*0.1 - f_h),
        (x_center + span*0.3, y_center - span*0.1 - f_h)
    ], facecolor=color, edgecolor=COLOR_DARK, lw=1.0))
    # Beam tilted slightly
    ax.plot([x_center - span*0.8, x_center + span*0.8], [y_center + span*0.15, y_center - span*0.15], color=COLOR_DARK, lw=2.0)
    # Heavy pan (FN penalty)
    ax.add_patch(patches.Rectangle((x_center - span*0.9, y_center - span*0.1), span*0.35, span*0.25, facecolor=COLOR_RISK, edgecolor=COLOR_DARK, lw=1.0))
    # Light pan (FP penalty)
    ax.add_patch(patches.Rectangle((x_center + span*0.6, y_center - span*0.4), span*0.25, span*0.18, facecolor=COLOR_SAFE, edgecolor=COLOR_DARK, lw=1.0))

def draw_triage_funnel(ax, x_center, y_center, span):
    """Draws 3-tier routing output icon."""
    h = span * 0.28
    # Tier 1 (Red)
    ax.add_patch(patches.Rectangle((x_center - span*0.7, y_center + span*0.35), span*1.4, h, facecolor=COLOR_RISK, edgecolor=COLOR_DARK, lw=1.0))
    # Tier 2 (Orange)
    ax.add_patch(patches.Rectangle((x_center - span*0.5, y_center - span*0.02), span*1.0, h, facecolor=COLOR_REVIEW, edgecolor=COLOR_DARK, lw=1.0))
    # Tier 3 (Green)
    ax.add_patch(patches.Rectangle((x_center - span*0.8, y_center - span*0.40), span*1.6, h, facecolor=COLOR_SAFE, edgecolor=COLOR_DARK, lw=1.0))

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(11.2, 5.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # MASTER TITLE BANNER (Sharp rectangular container)
    ax.add_patch(patches.Rectangle(
        (0.02, 0.905), 0.96, 0.080,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.952, "C-STGB END-TO-END ARCHITECTURAL DATAFLOW PIPELINE",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.923, "Modular Neuro-Symbolic Graph Learning Framework for Real-Time Financial Crime Surveillance",
            ha="center", va="center", fontsize=7.6, color="#94a3b8")

    # 6 MODULE GEOMETRY
    x_start = 0.022
    w_block = 0.138
    gap = 0.026
    y_block = 0.170
    h_block = 0.690

    modules = [
        {
            "num": "MODULE 1",
            "title": "Streaming\nIngestion",
            "border": COLOR_INGEST,
            "header_bg": COLOR_INGEST,
            "bg": COLOR_INGEST_BG,
            "bullets": [
                "12-D Mass-Flow Invariants",
                "Zero-Copy Arrow RecordBatches",
                "Sub-Millisecond Pipeline (<0.45 ms)"
            ],
            "icon_type": "cylinder"
        },
        {
            "num": "MODULE 2",
            "title": "Continuous-Time\nEncoder",
            "border": COLOR_GNN,
            "header_bg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "bullets": [
                "Tri-Band Positional Waves",
                "Hawkes Temporal Decay",
                "Causal Sequence Preservation"
            ],
            "icon_type": "waveform"
        },
        {
            "num": "MODULE 3",
            "title": "Edge-Trust\nGating",
            "border": COLOR_GNN,
            "header_bg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "bullets": [
                "Camouflage Noise Filter",
                "Learnable Soft Pruning (Floor 0.10)",
                "Preserves Dirichlet Energy"
            ],
            "icon_type": "gate"
        },
        {
            "num": "MODULE 4",
            "title": "Latent\nGraphSMOTE",
            "border": COLOR_GNN_PURPLE,
            "header_bg": COLOR_GNN_PURPLE,
            "bg": "#FAF5FF",
            "bullets": [
                "Typology-Clustered Synthesis",
                "Extreme Skew Balancing",
                "Topology-Consistent Manifold"
            ],
            "icon_type": "smote"
        },
        {
            "num": "MODULE 5",
            "title": "Bayes Risk\nHead",
            "border": COLOR_GNN,
            "header_bg": COLOR_GNN,
            "bg": COLOR_GNN_BG,
            "bullets": [
                "Asymmetric 15:1 Cost Matrix",
                "Evidence-Adaptive Fusion",
                "Strict False-Negative Penalization"
            ],
            "icon_type": "bayes"
        },
        {
            "num": "MODULE 6",
            "title": "Conformal\nTriage Engine",
            "border": COLOR_SAFE,
            "header_bg": COLOR_SAFE,
            "bg": COLOR_SAFE_BG,
            "bullets": [
                "Guaranteed 99.0% Coverage",
                "Tier 1: Quarantine SAR (0.18%)",
                "Tier 2: Review Desk (0.49%)",
                "Tier 3: Straight-Through (99.33%)"
            ],
            "icon_type": "triage"
        }
    ]

    inter_labels = [
        "Event\nStream",
        "Temporal\nTensors",
        "Denoised\nTopology",
        "Balanced\nGraph",
        "Calibrated\nRisk"
    ]

    for i, mod in enumerate(modules):
        bx = x_start + i * (w_block + gap)
        
        # Outer Card Container (Sharp rectangle)
        ax.add_patch(patches.Rectangle(
            (bx, y_block), w_block, h_block,
            facecolor=mod["bg"], edgecolor=mod["border"], lw=1.6
        ))
        
        # Header Band
        h_band = 0.055
        ax.add_patch(patches.Rectangle(
            (bx, y_block + h_block - h_band), w_block, h_band,
            facecolor=mod["header_bg"], edgecolor=mod["border"], lw=1.0
        ))
        ax.text(bx + w_block/2, y_block + h_block - h_band/2, mod["num"],
                ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff")
        
        # Module Title
        ax.text(bx + w_block/2, y_block + h_block - 0.105, mod["title"],
                ha="center", va="center", fontsize=8.6, fontweight="bold", color=COLOR_DARK,
                linespacing=1.1)

        # Separator line
        ax.plot([bx + 0.012, bx + w_block - 0.012], [y_block + h_block - 0.155, y_block + h_block - 0.155],
                color=COLOR_BORDER, lw=0.8)

        # Large Visual Icon Container
        icon_cx = bx + w_block/2
        icon_cy = y_block + 0.380
        
        if mod["icon_type"] == "cylinder":
            draw_cylinder(ax, icon_cx, icon_cy - 0.075, 0.065, 0.150, COLOR_INGEST_LIGHT, COLOR_INGEST)
        elif mod["icon_type"] == "waveform":
            draw_waveform(ax, icon_cx - 0.055, icon_cy, 0.110, 0.140, COLOR_GNN)
        elif mod["icon_type"] == "gate":
            draw_network_gate(ax, icon_cx, icon_cy, 0.065, COLOR_GNN, COLOR_RISK)
        elif mod["icon_type"] == "smote":
            draw_smote_clusters(ax, icon_cx, icon_cy, 0.065, COLOR_GNN_PURPLE, COLOR_MUTED)
        elif mod["icon_type"] == "bayes":
            draw_bayes_scale(ax, icon_cx, icon_cy, 0.065, COLOR_GNN)
        elif mod["icon_type"] == "triage":
            draw_triage_funnel(ax, icon_cx, icon_cy, 0.065)

        # Separator line above bullets
        ax.plot([bx + 0.012, bx + w_block - 0.012], [y_block + 0.250, y_block + 0.250],
                color=COLOR_BORDER, lw=0.8)

        # Bullet Points (Concept only, zero raw equations)
        b_start_y = y_block + 0.215
        for j, bullet in enumerate(mod["bullets"]):
            ax.text(bx + 0.010, b_start_y - j * 0.065, "•", fontsize=8.0, fontweight="bold", color=mod["border"])
            ax.text(bx + 0.018, b_start_y - j * 0.065, bullet, fontsize=6.8, color=COLOR_DARK,
                    va="center", wrap=True)

        # Inter-Block Flow Arrows
        if i < 5:
            arr_x0 = bx + w_block
            arr_x1 = arr_x0 + gap
            arr_y = y_block + h_block * 0.55
            ax.annotate(
                "", xy=(arr_x1, arr_y), xytext=(arr_x0, arr_y),
                arrowprops=dict(arrowstyle="->", color=COLOR_DARK, lw=1.8, mutation_scale=14)
            )
            # Arrow label pill
            ax.text(arr_x0 + gap/2, arr_y + 0.038, inter_labels[i],
                    ha="center", va="center", fontsize=6.4, fontweight="bold", color=COLOR_MUTED,
                    linespacing=0.95)

    # BOTTOM STAGE CATEGORIZATION RIBBON (Sharp rectangular blocks)
    ribbon_y = 0.050
    ribbon_h = 0.075

    # Stage 1: Ingestion
    ax.add_patch(patches.Rectangle(
        (x_start, ribbon_y), w_block, ribbon_h,
        facecolor=COLOR_INGEST_BG, edgecolor=COLOR_INGEST, lw=1.2
    ))
    ax.text(x_start + w_block/2, ribbon_y + ribbon_h/2, "STREAMING INGESTION\nZero-Copy Ingestion Layer",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_INGEST, linespacing=1.1)

    # Stage 2: Spatio-Temporal Core
    st2_x = x_start + w_block + gap
    st2_w = 3 * w_block + 2 * gap
    ax.add_patch(patches.Rectangle(
        (st2_x, ribbon_y), st2_w, ribbon_h,
        facecolor=COLOR_GNN_BG, edgecolor=COLOR_GNN, lw=1.2
    ))
    ax.text(st2_x + st2_w/2, ribbon_y + ribbon_h/2, "SPATIO-TEMPORAL REPRESENTATION & ADVERSARIAL DENOISING\nTri-Band Harmonic Waves • Edge-Trust Camouflage Pruning • Latent Typology Synthesis",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_GNN, linespacing=1.1)

    # Stage 3: Risk Calibration & Autonomous Triage
    st3_x = st2_x + st2_w + gap
    st3_w = 2 * w_block + gap
    ax.add_patch(patches.Rectangle(
        (st3_x, ribbon_y), st3_w, ribbon_h,
        facecolor=COLOR_SAFE_BG, edgecolor=COLOR_SAFE, lw=1.2
    ))
    ax.text(st3_x + st3_w/2, ribbon_y + ribbon_h/2, "RISK CALIBRATION & AUTONOMOUS TRIAGE\nAsymmetric Bayes Head • Conformal Class-Conditional Risk Control (99% Guaranteed Recall)",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_SAFE, linespacing=1.1)

    save_figure(fig, "fig3_1_tensor_flow", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
