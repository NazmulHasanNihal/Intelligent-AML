"""
Figure 3.2: 12-Dimensional Canonical Invariant Taxonomy Tree
Redesigned as an authoritative hierarchical Taxonomy Tree:
Root: 12-D Invariant Vector (z_inv)
Branches: 4 Logical Categories (Flow Conservation, Temporal Dynamics, Graph Topology, Amount & Scale)
Leaves: 12 Distinct Empirical Metrics with plain English definitions and zero equation clutter.
"""
import sys
from pathlib import Path
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

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # 11.2 x 6.5 generous canvas for hierarchical tree
    fig, ax = plt.subplots(figsize=(11.2, 6.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 1.0, 1.0, facecolor="#ffffff", edgecolor="none"))

    # Master Top Header
    ax.add_patch(patches.Rectangle(
        (0.015, 0.925), 0.970, 0.065,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(0.50, 0.965, "TAXONOMY TREE: UNIVERSAL 12-DIMENSIONAL INVARIANT SYSTEM",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.940, "Deterministic Protocol-Agnostic Feature Representation for Cross-Ledger Zero-Shot Generalization",
            ha="center", va="center", fontsize=7.4, color="#94a3b8")

    # =========================================================================
    # LEVEL 1: ROOT NODE (12-D Invariant Vector)
    # =========================================================================
    root_x, root_y = 0.50, 0.840
    root_w, root_h = 0.320, 0.065
    
    ax.add_patch(patches.Rectangle(
        (root_x - root_w/2, root_y - root_h/2), root_w, root_h,
        facecolor=COLOR_DARK, edgecolor="#38bdf8", lw=1.8, zorder=3
    ))
    ax.text(root_x, root_y + 0.012, "12-D INVARIANT VECTOR",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff", zorder=4)
    ax.text(root_x, root_y - 0.014, "Universal Normalized Feature Manifold",
            ha="center", va="center", fontsize=7.2, color="#38bdf8", zorder=4)

    # =========================================================================
    # LEVEL 2: 4 CATEGORY BRANCH NODES
    # =========================================================================
    cats = [
        {
            "id": "CAT 1", "title": "Flow Conservation",
            "cx": 0.145, "col": COLOR_INGEST, "bg": COLOR_INGEST_BG,
            "metrics": [
                ("Flow Symmetry Ratio", "Inflow vs Outflow balance;\ndetects zero-retention conduits"),
                ("Capital Transmission Velocity", "Duration money is held;\nflags pass-through mules"),
                ("Conduit Retention Ratio", "Fraction retained as fee;\ncharacterizes layering accounts")
            ]
        },
        {
            "id": "CAT 2", "title": "Temporal Dynamics",
            "cx": 0.380, "col": COLOR_REVIEW, "bg": COLOR_REVIEW_BG,
            "metrics": [
                ("Hawkes Burst Acceleration", "Rapid-fire transaction bursts;\ndetects coordinated smurfing"),
                ("Inter-Arrival Variance", "Automated script timing;\nseparates bots from humans"),
                ("Dormancy Wakeup Index", "Hibernating sleeper accounts\nsuddenly activated for laundering")
            ]
        },
        {
            "id": "CAT 3", "title": "Graph Topology",
            "cx": 0.620, "col": COLOR_GNN, "bg": COLOR_GNN_BG,
            "metrics": [
                ("Bi-Directional Causal Taint", "Forward dispersal & backward\ntrace to illicit seed nodes"),
                ("Circular Wash-Cycle Ratio", "Direct & indirect closed loops\nused for fund obfuscation"),
                ("Ego-Neighborhood Fan-Out", "Branching factor & degree\nsymmetry across entities")
            ]
        },
        {
            "id": "CAT 4", "title": "Amount & Scale",
            "cx": 0.855, "col": COLOR_RISK, "bg": COLOR_RISK_BG,
            "metrics": [
                ("CTR Threshold Proximity", "Transactions clustered just\nbelow statutory filing limits"),
                ("Benford First-Digit Deviation", "Anomalous digit frequencies;\nflags synthetic fabrication"),
                ("Amount Variance & Entropy", "Uniform amounts vs natural\nlog-normal financial flows")
            ]
        }
    ]

    cat_y = 0.690
    cat_w, cat_h = 0.205, 0.065

    # Connect Root to 4 Categories
    for c in cats:
        cx = c["cx"]
        # Polyline connector from root to category
        ax.plot([root_x, root_x], [root_y - root_h/2, 0.765], color=COLOR_DARK, lw=1.5, zorder=1)
        ax.plot([root_x, cx], [0.765, 0.765], color=COLOR_DARK, lw=1.5, zorder=1)
        ax.plot([cx, cx], [0.765, cat_y + cat_h/2], color=COLOR_DARK, lw=1.5, zorder=1)

        # Category Node Box
        ax.add_patch(patches.Rectangle(
            (cx - cat_w/2, cat_y - cat_h/2), cat_w, cat_h,
            facecolor=c["bg"], edgecolor=c["col"], lw=1.6, zorder=3
        ))
        # Header banner inside category
        ax.add_patch(patches.Rectangle(
            (cx - cat_w/2, cat_y + cat_h/2 - 0.024), cat_w, 0.024,
            facecolor=c["col"], edgecolor="none", zorder=4
        ))
        ax.text(cx, cat_y + cat_h/2 - 0.012, c["id"],
                ha="center", va="center", fontsize=6.4, fontweight="bold", color="#ffffff", zorder=5)
        ax.text(cx, cat_y - 0.008, c["title"],
                ha="center", va="center", fontsize=7.8, fontweight="bold", color=c["col"], zorder=5)

    # =========================================================================
    # LEVEL 3: 12 LEAF METRIC CARDS (3 under each category)
    # =========================================================================
    leaf_w = 0.210
    leaf_h = 0.135
    leaf_ys = [0.475, 0.315, 0.155]

    for c in cats:
        cx = c["cx"]
        for j, (m_name, m_desc) in enumerate(c["metrics"]):
            ly = leaf_ys[j]
            
            # Connector line from Category to Leaf Card
            ax.plot([cx, cx], [cat_y - cat_h/2, ly + leaf_h/2], color=c["col"], lw=1.2, zorder=1)

            # Leaf Card Container
            ax.add_patch(patches.Rectangle(
                (cx - leaf_w/2, ly - leaf_h/2), leaf_w, leaf_h,
                facecolor="#ffffff", edgecolor=c["col"], lw=1.2, zorder=3
            ))
            # Left Accent Bar
            ax.add_patch(patches.Rectangle(
                (cx - leaf_w/2, ly - leaf_h/2), 0.008, leaf_h,
                facecolor=c["col"], edgecolor="none", zorder=4
            ))
            # Metric Index & Name
            metric_num = f"Invariant #{len(cats)*j + (cats.index(c)+1)}"
            ax.text(cx - leaf_w/2 + 0.016, ly + leaf_h/2 - 0.025, m_name,
                    ha="left", va="center", fontsize=7.4, fontweight="bold", color=COLOR_DARK, zorder=5)
            # Metric Plain English Description
            ax.text(cx - leaf_w/2 + 0.016, ly - 0.012, m_desc,
                    ha="left", va="center", fontsize=6.4, color=COLOR_MUTED, linespacing=1.2, zorder=5)

    # Bottom Takeaway Strip
    ax.add_patch(patches.Rectangle(
        (0.015, 0.025), 0.970, 0.050,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=0.9
    ))
    ax.text(0.50, 0.050, "PHYSICAL INVARIANCE PRINCIPLE: These 12 physical metrics are topologically invariant across SWIFT MT103, Bitcoin UTXO, and Ethereum EVM ledgers.",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color=COLOR_DARK)

    save_figure(fig, "fig_canonical_invariants", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
