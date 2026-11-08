"""
Figure 3.6: Three-Step Typology-Clustered Latent GraphSMOTE Pipeline
Standalone publication script for C-STGB monograph.
Phase 2 Overhaul: Sharp rectangular geometry, proper mathtext, strict 4-color palette, readable fonts (>=7.2pt).
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
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    fig = plt.figure(figsize=(9.2, 4.4), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[0.42, 0.58], wspace=0.18, left=0.07, right=0.98, top=0.90, bottom=0.10)

    ax_sketch = fig.add_subplot(gs[0])
    ax_steps = fig.add_subplot(gs[1])
    ax_steps.axis("off")

    # Left Panel: 2D Latent Manifold Topology Scatter Sketch
    np.random.seed(42)
    # Cluster 1: Smurfing Rings (Blue)
    c1_center = np.array([2.0, 3.0])
    c1_pts = c1_center + np.random.randn(25, 2) * 0.45
    # Cluster 2: Peeling Chains (Teal)
    c2_center = np.array([4.2, 1.8])
    c2_pts = c2_center + np.random.randn(25, 2) * 0.42

    ax_sketch.scatter(c1_pts[:, 0], c1_pts[:, 1], color=COLOR_INGEST, alpha=0.70, s=32, label=r"$\mathcal{C}_1$: Smurfing Ring")
    ax_sketch.scatter(c2_pts[:, 0], c2_pts[:, 1], color=COLOR_GNN, alpha=0.70, s=32, label=r"$\mathcal{C}_2$: Peeling Chain")

    # Interpolated synthetic nodes strictly inside Cluster 1
    syn_c1 = []
    for _ in range(6):
        idx_u, idx_v = np.random.choice(len(c1_pts), 2, replace=False)
        rho = np.random.uniform(0.25, 0.75)
        syn_pt = (1 - rho) * c1_pts[idx_u] + rho * c1_pts[idx_v]
        syn_c1.append(syn_pt)
        ax_sketch.plot([c1_pts[idx_u, 0], c1_pts[idx_v, 0]], [c1_pts[idx_u, 1], c1_pts[idx_v, 1]], 
                       color="#f97316", linestyle=":", lw=1.1, alpha=0.7)
    syn_c1 = np.array(syn_c1)
    ax_sketch.scatter(syn_c1[:, 0], syn_c1[:, 1], color=COLOR_RISK, marker="*", s=95, edgecolor=COLOR_DARK, lw=0.7,
                      label=r"$\mathbf{h}_{\mathrm{syn}}$ (Intra-Cluster)", zorder=5)

    # Interpolated synthetic nodes strictly inside Cluster 2
    syn_c2 = []
    for _ in range(5):
        idx_u, idx_v = np.random.choice(len(c2_pts), 2, replace=False)
        rho = np.random.uniform(0.25, 0.75)
        syn_pt = (1 - rho) * c2_pts[idx_u] + rho * c2_pts[idx_v]
        syn_c2.append(syn_pt)
        ax_sketch.plot([c2_pts[idx_u, 0], c2_pts[idx_v, 0]], [c2_pts[idx_u, 1], c2_pts[idx_v, 1]], 
                       color="#f97316", linestyle=":", lw=1.1, alpha=0.7)
    syn_c2 = np.array(syn_c2)
    ax_sketch.scatter(syn_c2[:, 0], syn_c2[:, 1], color=COLOR_RISK, marker="*", s=95, edgecolor=COLOR_DARK, lw=0.7, zorder=5)

    # Cluster boundary hulls
    c1_circle = patches.Circle(c1_center, 1.15, fill=False, edgecolor=COLOR_INGEST, linestyle="--", lw=1.3, alpha=0.85)
    c2_circle = patches.Circle(c2_center, 1.10, fill=False, edgecolor=COLOR_GNN, linestyle="--", lw=1.3, alpha=0.85)
    ax_sketch.add_patch(c1_circle)
    ax_sketch.add_patch(c2_circle)

    # Cross-cluster forbidden boundary
    ax_sketch.plot([2.8, 3.4], [1.2, 3.8], color=COLOR_RISK, linestyle="-.", lw=1.6, alpha=0.9)
    ax_sketch.text(3.1, 2.5, "Forbidden Cross-Interp.\n(Zero Typology Blur)", ha="center", va="center",
                   fontsize=7.2, fontweight="bold", linespacing=1.2, color=COLOR_RISK,
                   bbox=dict(boxstyle="square,pad=0.25", facecolor=COLOR_RISK_BG, edgecolor=COLOR_RISK, lw=0.8))

    ax_sketch.set_title("Latent Manifold Space", fontsize=8.8, fontweight="bold", pad=6)
    ax_sketch.set_xlabel("Latent Dim 1", fontsize=8.0)
    ax_sketch.set_ylabel("Latent Dim 2", fontsize=8.0)
    ax_sketch.tick_params(labelsize=7.5)
    ax_sketch.grid(True, linestyle=":", alpha=0.5)
    ax_sketch.legend(loc="upper left", fontsize=7.0, framealpha=0.92, handletextpad=0.25, borderpad=0.25)

    # Right Panel: Exactly 3 Steps
    steps_data = [
        ("Step 1: Latent Typology Partitioning",
         ["• Minority illicit nodes partitioned into clusters $\\mathcal{C}_1, \\dots, \\mathcal{C}_K$",
          "• Cosine similarity threshold $\\tau_{\\mathrm{sim}} \\geq 0.75$",
          "• Preserves distinct criminal topological signatures"],
         0.00, 0.69, 0.98, 0.29, COLOR_INGEST_BG, COLOR_INGEST),
        ("Step 2: Intra-Cluster Latent Interpolation",
         ["• Sample seed pair $u, v \\in \\mathcal{C}_k$ within same cluster",
          "• Convex combination: $\\mathbf{h}_{\\mathrm{syn}} = (1-\\rho)\\mathbf{h}_u + \\rho\\mathbf{h}_v$",
          "• Generates realistic synthetic minority representations"],
         0.00, 0.35, 0.98, 0.29, COLOR_REVIEW_BG, COLOR_REVIEW),
        ("Step 3: Bilinear Edge Gen. & Flow Invariants",
         [r"• Bilinear link head: $\hat{\mathbf{A}}_{\mathrm{syn}, w} = \sigma(\mathbf{h}_{\mathrm{syn}}^T \mathbf{W}_e \mathbf{h}_w)$",
          r"• Invariant check: preserves flow balance $\Phi_{\mathrm{flow}} \approx 1.0$",
          r"• Synthetic nodes quarantined strictly to $\mathcal{D}_{\mathrm{train}}$"],
         0.00, 0.01, 0.98, 0.29, COLOR_SAFE_BG, COLOR_SAFE)
    ]

    for s_title, s_bullets, sx, sy, sw, sh, s_bg, s_fg in steps_data:
        ax_steps.add_patch(patches.Rectangle(
            (sx, sy), sw, sh,
            facecolor=s_bg, edgecolor=s_fg, linewidth=1.1
        ))
        ax_steps.text(sx + 0.03, sy + sh - 0.055, s_title, ha="left", va="center", fontsize=7.8, fontweight="bold", color=s_fg)
        for b_idx, b_txt in enumerate(s_bullets):
            ax_steps.text(sx + 0.03, sy + sh - 0.115 - (b_idx * 0.065), b_txt,
                          ha="left", va="center", fontsize=7.2, color=COLOR_DARK)

    # Downward connecting arrows
    for y_conn in [0.665, 0.325]:
        ax_steps.annotate("", xy=(0.49, y_conn - 0.015), xytext=(0.49, y_conn + 0.015),
                          arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#64748b", lw=1.4))

    fig.suptitle("Three-Step Typology-Clustered Latent GraphSMOTE & Bilinear Edge Synthesis Pipeline",
                 fontsize=9.6, fontweight="bold", color="#0f172a", y=0.97)

    save_figure(fig, "fig18_graphsmote_synthesis_pipeline", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
