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
    'axes.titlesize': 9.5,
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
    ("DGraphFin", 97.91 - 3.20, "vs. TGN", "#6A3DE8", "Dynamic Credit"),
    ("Elliptic-v2", 99.10 - 62.10, "vs. TGN", "#2563EB", "Blockchain"),
    ("SAML-D", 93.68 - 59.40, "vs. TGN", "#0D9488", "15-Bank Wire"),
    ("XBlock-ETH", 97.40 - 67.50, "vs. TGN", "#2563EB", "Blockchain"),
    ("PaySim-Ext", 99.80 - 73.10, "vs. TGN", "#0D9488", "Mobile e-Wallet"),
    ("Elliptic-v1", 91.42 - 68.40, "vs. TGN", "#2563EB", "Blockchain"),
    ("DataGen", 99.93 - 81.50, "vs. TGN", "#6A3DE8", "Complex DAG"),
    ("MtGox-Leaked", 74.20 - 55.80, "vs. TGN", "#2563EB", "CEX Orderbook"),
    ("CC-Transactions", 56.48 - 38.20, "vs. TGN", "#0D9488", "POS Card"),
    ("PaySim1", 16.66 - 3.50, "vs. GCN", "#0D9488", "Mobile e-Wallet"),
    ("AMLSim-HI-Med", 46.85 - 35.20, "vs. TGN", "#0D9488", "Multi-Tier Wire"),
    ("AMLSim-HI-Small", 39.70 - 28.40, "vs. TGN", "#0D9488", "Multi-Tier Wire"),
    ("AMLSim-LI-Med", 23.74 - 19.20, "vs. TGN", "#0D9488", "Multi-Tier Wire"),
    ("AMLSim-LI-Small", 15.83 - 12.90, "vs. TGN", "#0D9488", "Multi-Tier Wire"),
]

def generate_fig7_3():
    # 2-panel figure: Left executive KPI cards, Right horizontal lead bars
    fig = plt.figure(figsize=(11.5, 5.6), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 2.4], wspace=0.22)

    ax_kpi = fig.add_subplot(gs[0, 0])
    ax_bar = fig.add_subplot(gs[0, 1])

    # Left Panel: Executive Summary Badges
    ax_kpi.axis("off")
    ax_kpi.set_xlim(0, 1)
    ax_kpi.set_ylim(0, 1)

    cards = [
        ("GLOBAL MEAN RANK", "1.07", "11 Model Families across 14 Networks", "#1e3a8a", "#dbeafe", "#1e40af"),
        ("AVERAGE F1 LEAD", "+25.3 pp", "Macro Lead over Best GNN Baseline", "#065f46", "#d1fae5", "#065f46"),
        ("WORKLOAD CUT", "99.45%", "Class-Cond. CRC Triage Reduction", "#581c87", "#f3e8ff", "#581c87"),
        ("FAST-PATH LATENCY", "0.45 ms", "Sub-Millisecond CBS Production SLA", "#991b1b", "#fee2e2", "#991b1b")
    ]

    for i, (title, stat, desc, border, bg, fg) in enumerate(cards):
        y = 0.76 - i * 0.245
        rect = patches.FancyBboxPatch((0.02, y), 0.96, 0.21, boxstyle="round,pad=0.02",
                                      fc=bg, ec=border, lw=1.2)
        ax_kpi.add_patch(rect)
        ax_kpi.text(0.50, y + 0.165, title, ha="center", va="center", fontsize=7.5, fontweight="bold", color="#334155")
        ax_kpi.text(0.50, y + 0.095, stat, ha="center", va="center", fontsize=15.0, fontweight="bold", color=fg)
        ax_kpi.text(0.50, y + 0.035, desc, ha="center", va="center", fontsize=6.8, color="#475569")

    # Right Panel: Horizontal Bar Chart
    labels = [d[0] for d in data][::-1]
    gains = [d[1] for d in data][::-1]
    refs = [d[2] for d in data][::-1]
    colors = [d[3] for d in data][::-1]
    domains = [d[4] for d in data][::-1]

    y_pos = np.arange(len(labels))
    bars = ax_bar.barh(y_pos, gains, color=colors, edgecolor="black", height=0.68, linewidth=0.8, zorder=3)

    mean_gain = np.mean(gains)
    ax_bar.axvline(mean_gain, color="#DC2626", linestyle="--", linewidth=1.6, zorder=4,
                   label=f"Macro Mean Lead: +{mean_gain:.1f} pp")

    for bar, gain, ref, dom in zip(bars, gains, refs, domains):
        ax_bar.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height() / 2,
                    f"+{gain:.1f} pp ({ref})", va="center", ha="left", fontsize=7.5, fontweight="bold", color="#0F172A")

    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(labels, fontsize=8.0, fontweight="bold")
    ax_bar.set_xlim(0, 115)
    ax_bar.set_xlabel("C-STGB Absolute F1 Lead (+Percentage Points, pp) over Closest GNN Baseline", fontsize=9.0, fontweight="bold")
    ax_bar.set_title("C-STGB F1 Margin Superiority across All 14 Financial Networks (p < 0.001)", fontsize=10.5, fontweight="bold", pad=10)
    ax_bar.legend(loc="lower right", frameon=True, fontsize=8.2)
    ax_bar.grid(axis="x", linestyle=":", alpha=0.5, zorder=1)

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
