"""
scripts/redesign_fig1_1_benign_smurfing.py
Fixes Figure 1.1:
- Left margin padding added (xlim expanded on left so '(a)' is not clipped)
- Bottom invariant equations positioned with ample clearance (no overlapping characters)
- Crisp vector export with pad_inches=0.15
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
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'stix',
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
    BASE_DIR / "reports" / "figures",
]

def generate_fig1_1():
    fig, (ax_b, ax_m) = plt.subplots(1, 2, figsize=(8.2, 3.4), dpi=300, gridspec_kw={'wspace': 0.22})
    ax_b.axis('off')
    ax_m.axis('off')

    # Left Panel: Benign Retail Merchant Star Graph
    ax_b.set_xlim([-1.42, 1.35])
    ax_b.set_ylim([-1.35, 1.25])
    ax_b.set_title("(a) Benign Commercial Hub (Star Topology)", fontweight="bold", fontsize=8.8, pad=8)

    # Central merchant node
    circle_m = patches.Circle((0, 0), 0.22, facecolor="#1e40af", edgecolor="#0f172a", lw=1.2, zorder=5)
    ax_b.add_patch(circle_m)
    ax_b.text(0, 0, "Retail Hub\n(deg=85)", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff", zorder=6)

    # Surrounding customer nodes
    n_cust = 12
    angles = np.linspace(0, 2*np.pi, n_cust, endpoint=False)
    for ang in angles:
        x_c = 0.85 * np.cos(ang)
        y_c = 0.85 * np.sin(ang)
        c_node = patches.Circle((x_c, y_c), 0.10, facecolor="#e0f2fe", edgecolor="#0284c7", lw=0.8, zorder=4)
        ax_b.add_patch(c_node)
        ax_b.annotate("", xy=(0.18 * np.cos(ang), 0.18 * np.sin(ang)), xytext=(x_c, y_c),
                      arrowprops=dict(arrowstyle="->,head_width=0.15,head_length=0.22", color="#0284c7", lw=1.1))

    ax_b.text(0, -1.22, r"Invariant: $\Phi_{\mathrm{flow}} \approx 0.02$ (Inflow $\gg$ Outflow) | $\lambda_u \approx \mathrm{Poisson}$",
              ha="center", va="center", fontsize=6.4, fontweight="bold", color="#1e40af")

    # Right Panel: Illicit Placement -> Layering Wash -> Integration Sink
    ax_m.set_xlim([-0.12, 1.15])
    ax_m.set_ylim([-0.30, 1.25])
    ax_m.set_title("(b) Laundering Syndicate (Smurfing, Wash Loops & Sink)", fontweight="bold", fontsize=8.6, pad=8)

    # Placement Source S0
    ax_m.add_patch(patches.Circle((0.08, 0.5), 0.08, facecolor="#b91c1c", edgecolor="black", lw=1.0, zorder=5))
    ax_m.text(0.08, 0.5, "Source S0\n$485k", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#ffffff", zorder=6)

    # Mules M1, M2, M3
    mule_y = [0.85, 0.5, 0.15]
    for i, my in enumerate(mule_y):
        ax_m.add_patch(patches.Circle((0.36, my), 0.065, facecolor="#fee2e2", edgecolor="#b91c1c", lw=0.9, zorder=5))
        ax_m.text(0.36, my, f"Mule {i+1}", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#b91c1c", zorder=6)
        ax_m.annotate("", xy=(0.30, my), xytext=(0.16, 0.5),
                      arrowprops=dict(arrowstyle="->,head_width=0.14,head_length=0.20", color="#b91c1c", lw=1.1))

    # Layering Wash Cycle L1 -> L2 -> L3 -> L1
    ax_m.add_patch(patches.Circle((0.68, 0.72), 0.06, facecolor="#ffedd5", edgecolor="#ea580c", lw=0.9, zorder=5))
    ax_m.text(0.68, 0.72, "L1", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#ea580c", zorder=6)
    ax_m.add_patch(patches.Circle((0.68, 0.28), 0.06, facecolor="#ffedd5", edgecolor="#ea580c", lw=0.9, zorder=5))
    ax_m.text(0.68, 0.28, "L2", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#ea580c", zorder=6)

    # Mule to Layering arrows
    ax_m.annotate("", xy=(0.62, 0.72), xytext=(0.425, 0.85),
                  arrowprops=dict(arrowstyle="->", color="#ea580c", lw=1.1))
    ax_m.annotate("", xy=(0.62, 0.28), xytext=(0.425, 0.15),
                  arrowprops=dict(arrowstyle="->", color="#ea580c", lw=1.1))

    # Cycle arrows
    ax_m.annotate("", xy=(0.68, 0.34), xytext=(0.68, 0.66),
                  arrowprops=dict(arrowstyle="->,head_width=0.12", color="#ea580c", lw=1.2, connectionstyle="arc3,rad=-0.35"))
    ax_m.annotate("", xy=(0.68, 0.66), xytext=(0.68, 0.34),
                  arrowprops=dict(arrowstyle="->,head_width=0.12", color="#ea580c", lw=1.2, connectionstyle="arc3,rad=-0.35"))
    ax_m.text(0.68, 0.50, "Wash Loop\nCycle", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#ea580c")

    # Integration Sink C4
    ax_m.add_patch(patches.Circle((0.95, 0.5), 0.08, facecolor="#7c3aed", edgecolor="black", lw=1.0, zorder=5))
    ax_m.text(0.95, 0.5, "Sink C4\n(Offshore)", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#ffffff", zorder=6)

    ax_m.annotate("", xy=(0.87, 0.5), xytext=(0.74, 0.72),
                  arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.2))
    ax_m.annotate("", xy=(0.87, 0.5), xytext=(0.74, 0.28),
                  arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.2))

    ax_m.text(0.50, -0.20, r"Invariant: $\Phi_{\mathrm{flow}} \approx 0.994$ (Mass Conserved) | $\lambda_u = 74.2$ (Self-Exciting Burst)",
              ha="center", va="center", fontsize=6.4, fontweight="bold", color="#b91c1c")

    plt.tight_layout()

    stems = ["fig_benign_vs_smurfing_topology", "fig_topological_cam_contrast"]
    for stem in stems:
        for d in TARGET_DIRS:
            d.mkdir(parents=True, exist_ok=True)
            for ext in [".pdf", ".png"]:
                out_file = d / f"{stem}{ext}"
                fig.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
                print(f"Saved: {out_file}")

    plt.close()

if __name__ == "__main__":
    generate_fig1_1()

