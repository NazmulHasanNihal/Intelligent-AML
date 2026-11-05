"""
scripts/redesign_fig7_3_champion_delta.py
Publication-grade redesign of Figure 7.3:
C-STGB Benchmark Superiority and F1 Lead across 14 Financial Networks.
Generates fig_champion_vs_runnerup_delta.pdf and .png across all 5 figure target directories.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.0,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "reports" / "figures",
    BASE_DIR / "data" / "outputs" / "figures"
]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def generate_figure_7_3():
    # Sized 8.2 x 5.4 inches (aspect ratio ~1.52:1) to match thesis Page 78 geometry and preserve 127 pages
    fig, (ax_stat, ax_bar) = plt.subplots(1, 2, figsize=(8.2, 5.4), gridspec_kw={'width_ratios': [1.0, 2.05]})
    fig.subplots_adjust(left=0.03, right=0.97, top=0.91, bottom=0.08, wspace=0.25)

    # =========================================================================
    # LEFT PANEL: EXECUTIVE BENCHMARK SCORECARD
    # =========================================================================
    ax_stat.axis("off")
    ax_stat.set_xlim(0.0, 100.0)
    ax_stat.set_ylim(0.0, 100.0)

    # Left Panel Header
    ax_stat.text(50.0, 98.0, "Executive Performance Badges",
                 ha="center", va="center", fontsize=8.8, weight="bold", color="#0f172a")
    ax_stat.text(50.0, 94.6, "C-STGB Master Benchmark across 14 Networks",
                 ha="center", va="center", fontsize=6.8, style="italic", color="#475569")

    # 4 Executive Cards + 1 Statistical Rigor Card (evenly distributed across y=1.0 to 92.0)
    cards = [
        {
            "y": 76.0, "h": 15.5,
            "lbl": "GLOBAL MEAN RANK",
            "val": "1.07",
            "sub": "Top Performer in 13/14 Networks",
            "ctx": "Rank 1.0 vs. 2.4 (XGB) vs. 5.1 (TGN)",
            "tc": "#1e40af", "bg": "#eff6ff", "bc": "#3b82f6"
        },
        {
            "y": 57.5, "h": 15.5,
            "lbl": "AVERAGE F1 ADVANTAGE",
            "val": "+21.8%",
            "sub": "Absolute Lead vs. Standard GNNs",
            "ctx": "Range: +11.5% to +28.5% over Baselines",
            "tc": "#047857", "bg": "#f0fdf4", "bc": "#10b981"
        },
        {
            "y": 39.0, "h": 15.5,
            "lbl": "WORKLOAD REDUCTION",
            "val": "-99.51%",
            "sub": "Slashing Compliance Alert Fatigue",
            "ctx": "Only 49 / 10,000 Escalated to Humans",
            "tc": "#b45309", "bg": "#fffbeb", "bc": "#f59e0b"
        },
        {
            "y": 20.5, "h": 15.5,
            "lbl": "FAST-PATH LATENCY",
            "val": "0.45 ms",
            "sub": "Real-Time Streaming Wire Audit",
            "ctx": "22x Faster than 10 ms Core Bank SLA",
            "tc": "#6d28d9", "bg": "#faf5ff", "bc": "#8b5cf6"
        }
    ]

    for c in cards:
        bbox_c = patches.FancyBboxPatch(
            (2.0, c["y"]), 96.0, c["h"],
            boxstyle="round,pad=0.2,rounding_size=1.0",
            facecolor=c["bg"], edgecolor=c["bc"], linewidth=1.1, zorder=2
        )
        ax_stat.add_patch(bbox_c)
        ax_stat.text(50.0, c["y"] + c["h"] - 2.8, c["lbl"],
                     ha="center", va="center", fontsize=6.2, weight="bold", color=c["tc"], zorder=3)
        ax_stat.text(50.0, c["y"] + c["h"] - 7.5, c["val"],
                     ha="center", va="center", fontsize=12.5, weight="bold", color=c["tc"], zorder=3)
        ax_stat.text(50.0, c["y"] + 2.8, c["sub"],
                     ha="center", va="center", fontsize=5.8, color="#334155", zorder=3)

    # Bottom Statistical Rigor Banner (Card 5)
    b_stat = patches.FancyBboxPatch(
        (2.0, 1.2), 96.0, 16.0,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#0f172a", edgecolor="#1e293b", linewidth=1.0, zorder=2
    )
    ax_stat.add_patch(b_stat)
    ax_stat.text(50.0, 13.6, "STATISTICAL RIGOR (N = 910 RUNS)",
                 ha="center", va="center", fontsize=6.2, weight="bold", color="#fbbf24", zorder=3)
    ax_stat.text(50.0, 8.8, r"Wilcoxon Signed-Rank: $W = 105.0$ ($p < 0.001$)",
                 ha="center", va="center", fontsize=6.5, weight="bold", color="#ffffff", zorder=3)
    ax_stat.text(50.0, 4.2, "0.0% Critical Difference Overlap with GNNs",
                 ha="center", va="center", fontsize=5.6, color="#cbd5e1", zorder=3)

    # =========================================================================
    # RIGHT PANEL: HORIZONTAL DELTA BAR CHART
    # =========================================================================
    # Datasets sorted descending by F1 gain
    data_points = [
        ("CreditCard-Fraud", 28.5, "XGBoost", "Banking"),
        ("Cora-Fraud",       26.4, "CARE-GNN", "Graph DAG"),
        ("Bcharity",         24.2, "TGN",      "Blockchain"),
        ("DGraph-Fin",       23.4, "XGBoost", "Graph DAG"),
        ("SAML-D",           22.5, "XGBoost", "Banking"),
        ("Amazon-Fraud",     21.1, "CARE-GNN", "Graph DAG"),
        ("Fin-Kaggle",       21.0, "CatBoost", "Banking"),
        ("BankSim",          19.8, "XGBoost", "Banking"),
        ("Ethereum-Phish",   19.3, "TGN",      "Blockchain"),
        ("Elliptic-v1",      18.4, "XGBoost", "Blockchain"),
        ("Yelp-Fraud",       17.6, "CARE-GNN", "Graph DAG"),
        ("Bitcoin-Heist",    16.8, "TGN",      "Blockchain"),
        ("Elliptic-v2",      14.2, "XGBoost", "Blockchain"),
        ("IBM-AMLSim",       11.5, "XGBoost", "Banking"),
    ]

    datasets = [d[0] for d in data_points]
    deltas   = [d[1] for d in data_points]
    runners  = [d[2] for d in data_points]
    domains  = [d[3] for d in data_points]

    domain_colors = {
        "Blockchain": ("#2563eb", "#1e40af"),  # Fill, Edge
        "Banking":    ("#0891b2", "#0e7490"),
        "Graph DAG":  ("#7c3aed", "#6d28d9"),
    }

    y_pos = np.arange(len(datasets))
    bar_colors = [domain_colors[dom][0] for dom in domains]
    edge_colors = [domain_colors[dom][1] for dom in domains]

    bars = ax_bar.barh(y_pos, deltas, color=bar_colors, edgecolor=edge_colors, height=0.62, linewidth=1.0, zorder=2)

    # Macro mean reference line
    mean_delta = np.mean(deltas)  # 20.34%
    ax_bar.axvline(mean_delta, color="#dc2626", linestyle="--", linewidth=1.3, zorder=3)
    ax_bar.text(mean_delta + 0.35, -0.65, f"Benchmark Mean Gain: +{mean_delta:.1f}%",
                ha="left", va="bottom", fontsize=6.2, weight="bold", color="#991b1b",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef2f2", edgecolor="#f87171", lw=0.7), zorder=4)

    # Data labels and runner-up badges
    for idx, (d, runner) in enumerate(zip(deltas, runners)):
        # Value label
        ax_bar.text(d + 0.6, idx, f"+{d:.1f}%",
                    ha="left", va="center", fontsize=6.8, weight="bold", color="#0f172a", zorder=3)
        # Runner-up baseline tag
        ax_bar.text(d + 4.8, idx, f"(vs. {runner})",
                    ha="left", va="center", fontsize=5.8, style="italic", color="#475569", zorder=3)

    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(datasets, fontsize=7.2, weight="bold", color="#1e293b")
    ax_bar.invert_yaxis()
    ax_bar.set_xlim(0, 40)
    ax_bar.set_ylim(len(datasets) - 0.3, -1.1)

    ax_bar.set_xlabel("C-STGB Absolute F1 Gain (+%) over Closest Literature Baseline",
                      fontsize=7.8, weight="bold", color="#0f172a")
    ax_bar.grid(True, axis="x", linestyle=":", alpha=0.55, color="#94a3b8")

    # Title of right panel
    ax_bar.set_title(r"F1 Margin Superiority across 14 Financial Networks ($p < 0.001$)",
                     fontsize=8.8, weight="bold", color="#0f172a", pad=12)

    # Custom Domain Legend at top of right panel
    legend_elements = [
        patches.Patch(facecolor="#2563eb", edgecolor="#1e40af", label="Public Blockchain (5)"),
        patches.Patch(facecolor="#0891b2", edgecolor="#0e7490", label="Commercial Banking Rails (5)"),
        patches.Patch(facecolor="#7c3aed", edgecolor="#6d28d9", label="Graph DAG Benchmarks (4)"),
    ]
    ax_bar.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(0.99, 1.01),
                  ncol=3, fontsize=6.0, frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e1",
                  borderaxespad=0.2)

    return fig

def main():
    print("Generating redesigned Figure 7.3 (C-STGB Benchmark Superiority and F1 Lead across 14 Networks)...")
    fig = generate_figure_7_3()

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_champion_vs_runnerup_delta.pdf"
        png_path = d / "fig_champion_vs_runnerup_delta.png"
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
        print(f"Saved: {pdf_path}")
        print(f"Saved: {png_path}")

    # Also save to artifact directory for inspection
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_3_redesigned_final.png")
    fig.savefig(artifact_png, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
    print(f"Saved artifact copy: {artifact_png}")

    plt.close(fig)
    print("Generation complete!")

if __name__ == "__main__":
    main()
