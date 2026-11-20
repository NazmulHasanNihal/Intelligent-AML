"""
Figure 3.8: C-STGB Dual-Lane Execution Lifecycle: Training and Inference
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=300)
    ax.axis("off")
    ax.set_xlim([-0.008, 1.008])
    ax.set_ylim([-0.015, 1.015])

    # Lane 1 (Top)
    ax.add_patch(Rectangle(
        (0.010, 0.470), 0.980, 0.510,
        facecolor="#f8fafc", edgecolor="#1e40af", linewidth=1.1
    ))
    ax.add_patch(Rectangle(
        (0.020, 0.915), 0.520, 0.048,
        facecolor="#1e40af", edgecolor="#1e40af"
    ))
    ax.text(0.280, 0.939, "LANE 1: OFFLINE MULTI-STAGE TRAINING (ALGORITHM 1)",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color="#ffffff")

    train_boxes = [
        ("1. 12-D Flow Invariants", "Mass-Flow Invariant Space\nZero-Retention Conduits", 0.020, 0.520, 0.170, 0.360, "#eff6ff", "#1e40af"),
        ("2. Latent GraphSMOTE", "Cluster Manifold Synthesis\nExtreme Skew Balancing", 0.215, 0.520, 0.170, 0.360, "#fff7ed", "#c2410c"),
        ("3. Tri-Band Attn GNN", "Edge-Trust Soft Gating\nHawkes Temporal Attention", 0.410, 0.520, 0.170, 0.360, "#f0fdfa", "#0f766e"),
        ("4. Adaptive Fusion", "Evidence-Adaptive Gate\nLow-Degree Tabular Union", 0.605, 0.520, 0.170, 0.360, "#faf5ff", "#6d28d9"),
        ("5. Bayes & Conformal", "Asymmetric 15:1 Cost Head\nClass-Conditional CRC Arbiter", 0.800, 0.520, 0.170, 0.360, "#fef2f2", "#b91c1c")
    ]

    for t_head, t_body, x_b, y_b, w_b, h_b, c_bg, c_fg in train_boxes:
        ax.add_patch(Rectangle(
            (x_b, y_b), w_b, h_b,
            facecolor=c_bg, edgecolor=c_fg, linewidth=0.85
        ))
        ax.text(x_b + w_b/2, y_b + h_b - 0.050, t_head, ha="center", va="top", fontsize=6.8, fontweight="bold", color=c_fg)
        t_lines = t_body.split("\n")
        if len(t_lines) == 2:
            ax.text(x_b + w_b/2, y_b + 0.145, t_lines[0], ha="center", va="center", fontsize=5.3, color="#334155")
            ax.text(x_b + w_b/2, y_b + 0.070, t_lines[1], ha="center", va="center", fontsize=5.3, color="#334155")
        else:
            ax.text(x_b + w_b/2, y_b + 0.090, t_body, ha="center", va="center", fontsize=5.3, color="#334155")

    for x_arr in [0.193, 0.388, 0.583, 0.778]:
        ax.annotate("", xy=(x_arr + 0.016, 0.700), xytext=(x_arr - 0.002, 0.700),
                    arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color="#64748b", lw=1.2))

    # Lane 2 (Bottom)
    ax.add_patch(Rectangle(
        (0.010, 0.015), 0.980, 0.420,
        facecolor="#f8fafc", edgecolor="#15803d", linewidth=1.1
    ))
    ax.add_patch(Rectangle(
        (0.020, 0.365), 0.580, 0.048,
        facecolor="#15803d", edgecolor="#15803d"
    ))
    ax.text(0.310, 0.389, "LANE 2: ONLINE STREAMING FAST-PATH INFERENCE (<0.45 ms SLA)",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color="#ffffff")

    infer_boxes = [
        ("1. Live Ingest & Top-15", "Zero-Copy Arrow RecordBatch\n2-Hop Top-15 Cache", 0.020, 0.035, 0.225, 0.300, "#f0fdf4", "#15803d"),
        ("2. Incremental Invariants", "Flow Conservation & Velocity\nHawkes Burst Arrival Spike", 0.265, 0.035, 0.225, 0.300, "#f0fdfa", "#0f766e"),
        ("3. Frozen GNN & Bayes", "Forward Pass on Cached Weights\nCalibrated Bayes Risk Score", 0.510, 0.035, 0.225, 0.300, "#faf5ff", "#6d28d9"),
        ("4. 3-Tier CRC Triage", "Class-Conditional CRC Gate\nT1 Quarantine / T2 Rev / T3 STP", 0.755, 0.035, 0.225, 0.300, "#fef2f2", "#b91c1c")
    ]

    for i_head, i_body, x_b, y_b, w_b, h_b, c_bg, c_fg in infer_boxes:
        ax.add_patch(Rectangle(
            (x_b, y_b), w_b, h_b,
            facecolor=c_bg, edgecolor=c_fg, linewidth=0.85
        ))
        ax.text(x_b + w_b/2, y_b + h_b - 0.045, i_head, ha="center", va="top", fontsize=6.8, fontweight="bold", color=c_fg)
        lines_body = i_body.split("\n")
        if len(lines_body) == 2:
            ax.text(x_b + w_b/2, y_b + 0.125, lines_body[0], ha="center", va="center", fontsize=5.4, color="#334155")
            ax.text(x_b + w_b/2, y_b + 0.060, lines_body[1], ha="center", va="center", fontsize=5.4, color="#334155")
        else:
            ax.text(x_b + w_b/2, y_b + 0.075, i_body, ha="center", va="center", fontsize=5.4, color="#334155")

    for x_arr in [0.247, 0.492, 0.737]:
        ax.annotate("", xy=(x_arr + 0.016, 0.185), xytext=(x_arr - 0.002, 0.185),
                    arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color="#64748b", lw=1.2))

    plt.subplots_adjust(left=0.004, right=0.996, top=0.985, bottom=0.015)
    save_figure(fig, "fig_algorithm1_flowchart", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
