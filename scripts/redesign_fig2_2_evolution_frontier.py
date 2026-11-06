import sys
from pathlib import Path
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
    'axes.labelsize': 9.0,
    'axes.titlesize': 10.5,
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

def generate_fig2_2():
    fig, ax = plt.subplots(figsize=(11, 6.8), dpi=300)

    # Quadrant backgrounds
    ax.add_patch(patches.Rectangle((0, 0), 50, 50, facecolor="#F8FAFC", alpha=0.8, zorder=1))
    ax.add_patch(patches.Rectangle((0, 50), 50, 50, facecolor="#FEF2F2", alpha=0.55, zorder=1))
    ax.add_patch(patches.Rectangle((50, 0), 50, 50, facecolor="#ECFDF5", alpha=0.55, zorder=1))
    ax.add_patch(patches.Rectangle((50, 50), 50, 50, facecolor="#EFF6FF", alpha=0.75, zorder=1))

    # Quadrant watermark labels
    ax.text(25, 4, "QUADRANT I: Static Tabular & Spatial Baselines",
            fontsize=8.5, color="#64748B", ha="center", va="bottom", fontweight="bold", alpha=0.7)
    ax.text(25, 96, "QUADRANT II: Topological Imbalance & Camouflage Specialists",
            fontsize=8.5, color="#DC2626", ha="center", va="top", fontweight="bold", alpha=0.7)
    ax.text(75, 4, "QUADRANT III: Continuous-Time Dynamic GNNs",
            fontsize=8.5, color="#059669", ha="center", va="bottom", fontweight="bold", alpha=0.7)
    ax.text(75, 96, "QUADRANT IV: Unified Neuro-Symbolic & Statistical Safety",
            fontsize=8.5, color="#1D4ED8", ha="center", va="top", fontweight="bold", alpha=0.7)

    ax.axhline(50, color="#64748B", linestyle="--", linewidth=1.2, zorder=2)
    ax.axvline(50, color="#64748B", linestyle="--", linewidth=1.2, zorder=2)

    # (x: Temporal Expressiveness, y: Camouflage & Statistical Safety, label, color, marker)
    models = [
        # Quadrant I: Static Tabular & Spatial Baselines
        (16, 42, "XGBoost\n(88.35% F1)", "#334155", "o"),
        (25, 38, "CatBoost\n(87.90% F1)", "#334155", "o"),
        (18, 22, "GCN\n(43.55% F1)", "#2563EB", "o"),
        (26, 28, "GraphSAGE\n(49.07% F1)", "#2563EB", "o"),
        (33, 18, "GAT / GATv2\n(31.35% F1)", "#2563EB", "o"),
        (21, 12, "GIN\n(22.32% F1)", "#2563EB", "o"),
        (39, 34, "HGT\n(48.20% F1)", "#2563EB", "o"),
        # Quadrant II: Topological Imbalance & Camouflage Specialists
        (27, 68, "GraphSMOTE\n(74.20% F1)", "#D97706", "o"),
        (36, 64, "CARE-GNN\n(64.50% F1)", "#7C3AED", "o"),
        (44, 76, "H2-IDE\n(84.10% F1)", "#7C3AED", "o"),
        (47, 83, "CamFD\n(85.30% F1)", "#7C3AED", "o"),
        # Quadrant III: Continuous-Time Dynamic GNNs
        (62, 32, "EvolveGCN\n(51.04% F1)", "#059669", "o"),
        (73, 41, "TGAT\n(66.20% F1)", "#059669", "o"),
        (80, 46, "TGN\n(68.40% F1)", "#059669", "o"),
        # Quadrant IV: Unified Neuro-Symbolic & Statistical Safety Frontier
        (92, 91, "C-STGB (Ours)\n(91.42% F1 | 0.9312 PR-AUC)", "#DC2626", "*"),
    ]

    for x, y, label, col, m in models:
        size = 280 if m == "*" else 105
        ax.scatter(x, y, c=col, s=size, marker=m, edgecolors="black", linewidths=1.2, zorder=5)
        offset_y = -6.5 if m == "*" else 2.2
        weight = "bold" if m == "*" else "semibold"
        fsize = 8.5 if m == "*" else 7.5
        ax.annotate(label, (x, y + offset_y), fontsize=fsize, fontweight=weight,
                    ha="center", va="bottom", color=col if m == "*" else "#0F172A", zorder=6,
                    linespacing=1.35,
                    bbox=dict(boxstyle="square,pad=0.20", fc="#ffffff", ec="#cbd5e1", lw=0.6, alpha=0.90) if m != "*" else None)

    # Highlight Pareto Frontier curve
    px = [16, 25, 47, 92]
    py = [42, 38, 83, 91]

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Static Snapshots  --->  CONTINUOUS-TIME HARMONIC VELOCITY\n(Tri-Band Decay 2.4h / 24h / 168h & Hawkes Burst Intensity)", fontsize=9.5, fontweight="bold", linespacing=1.35)
    ax.set_ylabel("Uncalibrated  --->  TOPOLOGICAL DENOISING & CONFORMAL SAFETY\n(Edge-Trust Gating >= 0.10, 12-D Invariant Fusion & Class-Cond. CRC)", fontsize=9.5, fontweight="bold", linespacing=1.35)
    ax.set_title("2D Financial Crime Graph Learning Evolution Frontier (Elliptic-v1 Benchmark F1)", fontsize=11.5, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.45)
    plt.tight_layout()

    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in [".pdf", ".png"]:
            out_file = d / f"fig_lit_evolution_frontier{ext}"
            plt.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
            print(f"Saved: {out_file}")

    plt.close()

if __name__ == "__main__":
    generate_fig2_2()
