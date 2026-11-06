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
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
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

def generate_fig7_7():
    steps = [
        "(1a) GCN Raw\n(tau=0.50)",
        "(1b) +Bayes tau*\n(Cost Opt)",
        "(2) +12-D Space\n(z_inv)",
        "(3) +Tri-Band\n(w(dt))",
        "(4) +Edge Gate\n(g_ij>=0.10)",
        "(5) +SMOTE\n(Typology)",
        "(6) +Fusion\n(h_u*)",
        "(7) Full C-STGB\n(End-to-End)"
    ]

    elliptic = [10.33, 26.40, 54.80, 68.50, 76.20, 86.12, 89.80, 91.42]
    samld    = [6.20,  18.50, 46.20, 61.40, 71.80, 81.50, 89.80, 93.68]
    amlsim   = [2.10,   6.80, 18.40, 26.50, 32.40, 39.80, 43.20, 46.85]

    x = np.arange(len(steps))
    w = 0.26

    fig, ax = plt.subplots(figsize=(11.5, 4.6), dpi=300)
    b1 = ax.bar(x - w, elliptic, w, label="Elliptic-v1 (Bitcoin UTXO)", color="#1E3A8A", edgecolor="black", linewidth=0.8, zorder=3)
    b2 = ax.bar(x,     samld,    w, label="SAML-D (15-Bank Rail)", color="#15803D", edgecolor="black", linewidth=0.8, zorder=3)
    b3 = ax.bar(x + w, amlsim,   w, label="IBM AMLSim HI (Multi-Bank)", color="#EA580C", edgecolor="black", linewidth=0.8, zorder=3)

    # Label each bar with staggered heights to eliminate any text overlap
    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#1E3A8A", rotation=90, zorder=4)

    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#15803D", rotation=90, zorder=4)

    for bar in b3:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=6.8, fontweight="bold", color="#EA580C", rotation=90, zorder=4)

    ax.set_ylim(0, 115)
    ax.set_ylabel("Macro F1-Score (%)", fontsize=10.0, fontweight="bold")
    ax.set_title("Stepwise Architectural Ablation Progression across 3 Diverse Financial Archetypes", fontsize=11.5, fontweight="bold", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(steps, fontsize=8.5, fontweight="bold")
    ax.legend(loc="upper left", ncol=3, frameon=True, fontsize=9.0)
    ax.grid(axis="y", linestyle=":", alpha=0.5, zorder=1)
    plt.tight_layout()

    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for stem in ["fig3_ablation_component_study", "fig7_7_ablation_progression"]:
            for ext in [".pdf", ".png"]:
                out_file = d / f"{stem}{ext}"
                plt.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
                print(f"Saved: {out_file}")

    artifact_out = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_7_redesigned_final.png")
    plt.savefig(artifact_out, bbox_inches="tight", pad_inches=0.15, dpi=300)
    print(f"Saved artifact: {artifact_out}")

    plt.close()

if __name__ == "__main__":
    generate_fig7_7()

