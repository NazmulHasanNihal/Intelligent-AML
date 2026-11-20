"""
Figure 7.3: C-STGB Benchmark Superiority and F1 Lead across 14 Networks
Left: Executive performance badges (Global Mean Rank 1.07, +24.6 pp F1 lead, -99.51% workload cut, <0.45 ms latency)
Right: Horizontal delta bar chart across all 14 networks with widened spacing and 6.8pt dataset tick labels to prevent any collision.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

data = [
    ("DGraphFin",        97.91 - 3.20,  "vs. TGN", "#7C3AED", "Dynamic Credit Graph"),
    ("Elliptic-v2",      99.10 - 62.10, "vs. TGN", "#2563EB", "Multi-Asset Blockchain"),
    ("SAML-D",           93.68 - 59.40, "vs. TGN", "#0D9488", "15-Bank Wire Rail"),
    ("XBlock-ETH",       97.40 - 67.50, "vs. TGN", "#2563EB", "Ethereum EVM Smart Contracts"),
    ("PaySim-Extended",  99.80 - 73.10, "vs. TGN", "#0D9488", "Mobile E-Wallet Multi-Hop"),
    ("Elliptic-v1",      91.42 - 68.40, "vs. TGN", "#2563EB", "Bitcoin UTXO Network"),
    ("DataGenerator",    99.93 - 81.50, "vs. TGN", "#7C3AED", "Complex Typology Cycles"),
    ("MtGox-Leaked",     74.20 - 55.80, "vs. TGN", "#2563EB", "CEX Orderbook Transfers"),
    ("CC-Transactions",  56.48 - 38.20, "vs. TGN", "#0D9488", "Point-of-Sale Card Streams"),
    ("PaySim1",          16.66 - 2.50,  "vs. TGN", "#0D9488", "Mobile E-Wallet Log"),
    ("IBM-AMLSim-HI-Med",46.85 - 35.20, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-HI-Sml",39.70 - 28.40, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-LI-Med",23.74 - 19.20, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-LI-Sml",15.83 - 12.90, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
]

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig = plt.figure(figsize=(12.5, 6.6), dpi=300)
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.0, 3.2], wspace=0.32,
                           left=0.03, right=0.97, top=0.91, bottom=0.09)

    ax_left = fig.add_subplot(gs[0])
    ax_right = fig.add_subplot(gs[1])

    # =========================================================================
    # LEFT PANEL: EXECUTIVE PERFORMANCE BADGES
    # =========================================================================
    ax_left.axis("off")
    ax_left.set_xlim(0, 1)
    ax_left.set_ylim(0, 1)
    ax_left.set_title("Benchmark Metrics", fontsize=9.2, fontweight="bold", color=COLOR_DARK, pad=10)

    badges = [
        {
            "header": "GLOBAL MEAN RANK",
            "val": "1.21",
            "sub": "Outperforms all 10 baseline\nfamilies across 14 networks",
            "border": COLOR_INGEST, "bg": COLOR_INGEST_BG
        },
        {
            "header": "MACRO F1 MARGIN",
            "val": "+24.66 pp",
            "sub": "Decisive lead over closest\npublished baseline GNN (TGN)",
            "border": COLOR_GNN, "bg": COLOR_GNN_BG
        },
        {
            "header": "WORKLOAD SLASHING",
            "val": "-99.43%",
            "sub": "Cross-benchmark macro mean\n(99.51% on live stream)",
            "border": COLOR_SAFE, "bg": COLOR_SAFE_BG
        },
        {
            "header": "FAST-PATH LATENCY",
            "val": "< 0.45 ms",
            "sub": "P99 0.82 ms; complies with\nbanking SLA (< 10 ms)",
            "border": COLOR_REVIEW, "bg": COLOR_REVIEW_BG
        }
    ]

    card_h = 0.210
    card_gap = 0.035
    for i, b in enumerate(badges):
        cy = 0.960 - (i + 1) * card_h - i * card_gap
        ax_left.add_patch(patches.Rectangle(
            (0.02, cy), 0.96, card_h,
            facecolor=b["bg"], edgecolor=b["border"], lw=1.5
        ))
        ax_left.text(0.50, cy + card_h - 0.038, b["header"],
                     ha="center", va="center", fontsize=7.0, fontweight="bold", color=b["border"])
        ax_left.text(0.50, cy + card_h - 0.098, b["val"],
                     ha="center", va="center", fontsize=14.0, fontweight="bold", color=COLOR_DARK)
        ax_left.text(0.50, cy + 0.040, b["sub"],
                     ha="center", va="center", fontsize=6.2, color=COLOR_MUTED, linespacing=1.1)

    # =========================================================================
    # RIGHT PANEL: HORIZONTAL DELTA BAR CHART
    # =========================================================================
    labels  = [d[0] for d in data][::-1]
    gains   = [d[1] for d in data][::-1]
    refs    = [d[2] for d in data][::-1]
    colors  = [d[3] for d in data][::-1]

    y_pos = np.arange(len(labels))
    bars = ax_right.barh(y_pos, gains, color=colors, edgecolor="black", height=0.66, linewidth=0.9, zorder=3)

    mean_gain = np.mean(gains)
    ax_right.axvline(mean_gain, color=COLOR_RISK, linestyle="--", linewidth=1.8, zorder=4,
                     label=f"Macro Mean Lead: +{mean_gain:.2f} pp (Paired Wilcoxon W = 105.0, p < 0.0001)")

    for bar, gain, ref in zip(bars, gains, refs):
        ax_right.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height() / 2,
                      f"+{gain:.1f} pp ({ref})", va="center", ha="left", fontsize=7.0, fontweight="bold", color=COLOR_DARK)

    ax_right.set_yticks(y_pos)
    # Reduced font size to 6.8pt with clear bold typography and padding to eliminate any collision with left panel
    ax_right.set_yticklabels(labels, fontsize=6.8, fontweight="bold", color=COLOR_DARK)
    ax_right.tick_params(axis="y", pad=5)

    ax_right.set_xlabel("Minority Illicit Class Macro F1-Score Margin (+pp over Leading Baseline)",
                        fontsize=8.5, fontweight="bold", labelpad=8)
    ax_right.set_title("C-STGB Lead vs. Strongest Continuous-Time GNN (TGN)",
                       fontsize=9.8, fontweight="bold", pad=10)

    ax_right.set_xlim(0, 135)
    ax_right.grid(axis="x", linestyle="--", alpha=0.5, zorder=0)

    # Legend for domain color swatches
    domains = [
        ("Mobile Money / Wire Rails (bKash, SAML-D, PaySim)", "#0D9488"),
        ("Blockchain / Cryptographic Ledgers (Elliptic, ETH)", "#2563EB"),
        ("Complex Credit & Typology Graphs (DGraphFin, Synth)", "#7C3AED"),
    ]
    custom_lines = [Line2D([0], [0], color=c, lw=6) for _, c in domains]
    custom_lines.append(Line2D([0], [0], color=COLOR_RISK, lw=2, linestyle="--"))
    domain_labels = [d[0] for d in domains]
    domain_labels.append(f"Mean Lead (+{mean_gain:.1f} pp)")

    ax_right.legend(custom_lines, domain_labels, loc="lower right",
                    framealpha=0.92, facecolor="#ffffff", edgecolor=COLOR_BORDER,
                    fontsize=6.8)

    save_figure(fig, "fig_champion_vs_runnerup_delta", pad_inches=0.10)
    save_figure(fig, "fig15_champion_vs_runnerup_delta", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
