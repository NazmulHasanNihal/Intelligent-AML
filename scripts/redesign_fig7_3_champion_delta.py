import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 8.5,
    'axes.labelsize': 9.5,
    'axes.titlesize': 11.0,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
    BASE_DIR / "reports" / "figures",
]

# Exact 14 datasets from Table 7.1 and Table D.3 (C-STGB F1 vs Best GNN Baseline F1)
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
    ("PaySim1",          16.66 - 3.50,  "vs. GCN", "#0D9488", "Mobile E-Wallet Log"),
    ("IBM-AMLSim-HI-Med",46.85 - 35.20, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-HI-Sml",39.70 - 28.40, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-LI-Med",23.74 - 19.20, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
    ("IBM-AMLSim-LI-Sml",15.83 - 12.90, "vs. TGN", "#0D9488", "Multi-Tier Wire Clearing"),
]

def generate_fig7_3():
    # Pure horizontal bar chart, NO card boxes
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)

    labels  = [d[0] for d in data][::-1]
    gains   = [d[1] for d in data][::-1]
    refs    = [d[2] for d in data][::-1]
    colors  = [d[3] for d in data][::-1]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, gains, color=colors, edgecolor="black", height=0.66, linewidth=0.9, zorder=3)

    mean_gain = np.mean(gains)
    ax.axvline(mean_gain, color="#DC2626", linestyle="--", linewidth=1.8, zorder=4,
               label=f"Macro Mean Lead: +{mean_gain:.1f} pp (Paired Wilcoxon W = 105.0, p < 0.0001)")

    for bar, gain, ref in zip(bars, gains, refs):
        ax.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height() / 2,
                f"+{gain:.1f} pp ({ref})", va="center", ha="left", fontsize=8.2, fontweight="bold", color="#0F172A")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8.8, fontweight="bold")
    ax.set_xlim(0, 114)
    ax.set_xlabel("C-STGB Absolute F1 Lead (+Percentage Points, pp) over Closest Published Baseline per Network", fontsize=9.5, fontweight="bold")
    ax.set_title("C-STGB Minority F1 Margin Superiority across All 14 Financial Transaction Networks", fontsize=11.5, fontweight="bold", pad=12)

    # Custom legend for archetype groups
    from matplotlib.lines import Line2D
    custom_lines = [
        Line2D([0], [0], color="#2563EB", lw=6, label="Public Blockchain / UTXO / EVM"),
        Line2D([0], [0], color="#0D9488", lw=6, label="Commercial Multi-Bank / E-Wallet / POS"),
        Line2D([0], [0], color="#7C3AED", lw=6, label="Dynamic Credit & Synthetic Complex DAG"),
        Line2D([0], [0], color="#DC2626", lw=1.8, linestyle="--", label=f"Macro Mean Lead (+{mean_gain:.1f} pp)")
    ]
    ax.legend(handles=custom_lines, loc="lower right", frameon=True, fontsize=8.5, framealpha=0.95)
    ax.grid(axis="x", linestyle=":", alpha=0.5, zorder=1)

    plt.tight_layout()

    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in [".pdf", ".png"]:
            out_file = d / f"fig_champion_vs_runnerup_delta{ext}"
            plt.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
            print(f"Saved: {out_file}")

    plt.close()

if __name__ == "__main__":
    generate_fig7_3()
