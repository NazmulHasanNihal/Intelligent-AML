"""
scripts/build_all_figure_scripts.py
Systematically generates modular, standalone, publication-grade Python scripts
for each and every figure in the C-STGB thesis monograph.
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPTS = {}

# ==============================================================================
# CHAPTER 1
# ==============================================================================

SCRIPTS["fig1_3_failure_modes.py"] = '''"""
Figure 1.3: Five Canonical Failure Modes of Conventional AML Architectures
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.0, title_size=9.2, label_size=8.2)
    fig, axes = plt.subplots(1, 5, figsize=(14.0, 3.4), dpi=300)

    # Panel 1: Exponential Decay Vanishing
    ax = axes[0]
    dt = np.linspace(0, 90, 200)
    decay_naive = np.exp(-0.15 * dt)
    decay_triband = 0.5 * np.exp(-0.01 * dt) + 0.3 * np.cos(2 * np.pi * dt / 7) * np.exp(-0.03 * dt) + 0.2
    ax.plot(dt, decay_naive, color="#DC2626", lw=2, label="Static Decay (20d Miss)")
    ax.plot(dt, np.clip(decay_triband, 0, 1), color="#15803D", lw=2, label="C-STGB Tri-Band (90d Active)")
    ax.axvline(20, color="#DC2626", linestyle=":", alpha=0.7)
    ax.set_title("(a) Memory Vanishing", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("Elapsed Time (Days)", fontsize=8.0)
    ax.set_ylabel("Attention Weight", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 2: Dirichlet Energy Collapse (Over-smoothing)
    ax = axes[1]
    layers = np.arange(1, 9)
    energy_gcn = 1.0 * (0.45 ** (layers - 1))
    energy_cstgb = np.array([1.0, 0.92, 0.88, 0.85, 0.83, 0.82, 0.81, 0.80])
    ax.plot(layers, energy_gcn, "-o", color="#DC2626", lw=1.8, ms=4, label=r"Standard GCN $\mathcal{E}(H) \to 0$")
    ax.plot(layers, energy_cstgb, "-s", color="#2563EB", lw=1.8, ms=4, label=r"C-STGB Gate $\mathcal{E}(H) \geq c > 0$")
    ax.set_title("(b) Feature Over-Smoothing", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("GNN Layer Depth (L)", fontsize=8.0)
    ax.set_ylabel(r"Dirichlet Energy $\mathcal{E}(H)$", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 3: Threshold Collapse under Class Skew
    ax = axes[2]
    taus = np.linspace(0.01, 0.90, 100)
    recall = 1.0 / (1.0 + np.exp(12 * (taus - 0.25)))
    ax.plot(taus, recall * 100, color="#7C3AED", lw=2)
    ax.axvline(0.50, color="#DC2626", linestyle="--", lw=1.5, label=r"Naïve $\tau=0.50$ (Recall < 12%)")
    ax.axvline(0.18, color="#15803D", linestyle="-.", lw=1.5, label=r"Bayes $\tau^*=0.18$ (Recall > 90%)")
    ax.set_title("(c) Recall Collapse", fontweight="bold", fontsize=8.8)
    ax.set_xlabel(r"Decision Cutoff ($\tau$)", fontsize=8.0)
    ax.set_ylabel("Minority Recall (%)", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 4: k-Hop VRAM Explosion
    ax = axes[3]
    k_hops = np.arange(1, 5)
    vram_full = np.array([4.2, 18.5, 96.0, 480.0])
    vram_cstgb = np.array([1.2, 3.4, 6.8, 12.5])
    ax.plot(k_hops, vram_full, "-o", color="#DC2626", lw=1.8, ms=4, label="Full $k$-Hop (>80GB OOM)")
    ax.plot(k_hops, vram_cstgb, "-s", color="#059669", lw=1.8, ms=4, label="DuckDB 2-Hop (<16GB)")
    ax.axhline(80, color="#B91C1C", linestyle=":", label="A100 80GB VRAM Limit")
    ax.set_yscale("log")
    ax.set_title("(d) VRAM Explosion", fontweight="bold", fontsize=8.8)
    ax.set_xlabel("Neighborhood Hop ($k$)", fontsize=8.0)
    ax.set_ylabel("Peak VRAM (GB, log)", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="lower right")
    ax.grid(True, linestyle=":", alpha=0.5)

    # Panel 5: Conformal Queue Flooding
    ax = axes[4]
    skews = np.array([0.05, 0.1, 0.5, 1.0, 2.0, 5.0])
    marginal_q = np.array([98.2, 95.0, 82.0, 65.0, 42.0, 25.0])
    cstgb_q = np.array([0.49, 0.52, 0.55, 0.58, 0.62, 0.65])
    ax.plot(skews, marginal_q, "-o", color="#DC2626", lw=1.8, ms=4, label="Marginal Conformal (>90%)")
    ax.plot(skews, cstgb_q, "-s", color="#2563EB", lw=1.8, ms=4, label="Class-Cond. CRC (<0.6%)")
    ax.set_title("(e) Conformal Queue", fontweight="bold", fontsize=8.8)
    ax.set_xlabel(r"Minority Skew $\pi$ (%)", fontsize=8.0)
    ax.set_ylabel("Manual Review %", fontsize=8.0)
    ax.legend(fontsize=6.8, loc="center right")
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    save_figure(fig, "fig_1_3_failure_modes", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
'''

# ==============================================================================
# CHAPTER 2
# ==============================================================================

SCRIPTS["fig2_1_adversarial_camouflage.py"] = '''"""
Figure 2.1: Adversarial Camouflage Topology and Edge-Trust Filter Pruning
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 5.2), dpi=300)
    for ax in axes:
        ax.axis('off')
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)

    # Left: Dense Camouflage Infiltration
    ax1 = axes[0]
    ax1.set_title("(a) Adversarial Camouflage Infiltration (Over-Smoothing)", fontsize=8.8, fontweight="bold", pad=8)
    card1 = patches.Rectangle((-1.30, -1.30), 2.60, 2.60, facecolor="#fef2f2", edgecolor="#ef4444", lw=1.1)
    ax1.add_patch(card1)

    m_x, m_y = 0.0, 0.45
    f_x, f_y = 0.0, -0.65
    ax1.add_patch(patches.Rectangle((m_x-0.35, m_y-0.18), 0.70, 0.36, facecolor="#1e40af", edgecolor="#172554", lw=1.2, zorder=5))
    ax1.text(m_x, m_y, "Merchant Hub M\n(deg=120, Benign)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=6)

    ax1.add_patch(patches.Rectangle((f_x-0.35, f_y-0.18), 0.70, 0.36, facecolor="#dc2626", edgecolor="#7f1d1d", lw=1.2, zorder=5))
    ax1.text(f_x, f_y, "Syndicate Account F\n(Illicit Smurfer)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=6)

    for i, a in enumerate(np.linspace(0.1*np.pi, 0.9*np.pi, 5)):
        bx, by = 0.85 * np.cos(a), m_y + 0.65 * np.sin(a)
        ax1.add_patch(patches.Circle((bx, by), 0.09, facecolor="#dbeafe", edgecolor="#1d4ed8", lw=0.9, zorder=5))
        ax1.text(bx, by, f"B{i+1}", ha="center", va="center", fontsize=6.0, color="#1e3a8a", zorder=6)
        ax1.plot([bx, m_x], [by, m_y], color="#93c5fd", lw=1.2, zorder=3)

    for offset in [-0.22, 0.0, 0.22]:
        ax1.annotate("", xy=(m_x + offset, m_y - 0.18), xytext=(f_x + offset, f_y + 0.18),
                     arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.8, linestyle="--"), zorder=4)
        ax1.text(m_x + offset*1.8, (m_y+f_y)/2, "Chaff $10", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#b91c1c",
                 bbox=dict(boxstyle="square,pad=0.15", facecolor="#ffffff", edgecolor="#fca5a5", lw=0.6))

    ax1.text(0.0, -1.18, r"Collapse: $\mathcal{E}(\mathbf{H}) \to 0$, GNN predicts $\hat{p}_F = 0.04$ (False Negative)",
             ha="center", va="center", fontsize=6.8, fontweight="bold", color="#991b1b",
             bbox=dict(boxstyle="square,pad=0.25", facecolor="#ffffff", edgecolor="#f87171", lw=0.8))

    # Right: Edge-Trust Gating
    ax2 = axes[1]
    ax2.set_title(r"(b) C-STGB Context-Aware Edge Trust Gating ($\hat{g}_{ij} \geq 0.10$)", fontsize=8.8, fontweight="bold", pad=8)
    card2 = patches.Rectangle((-1.30, -1.30), 2.60, 2.60, facecolor="#f0fdf4", edgecolor="#16a34a", lw=1.1)
    ax2.add_patch(card2)

    ax2.add_patch(patches.Rectangle((m_x-0.35, m_y-0.18), 0.70, 0.36, facecolor="#1e40af", edgecolor="#172554", lw=1.2, zorder=5))
    ax2.text(m_x, m_y, "Merchant Hub M\n(Protected Hub)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=6)

    ax2.add_patch(patches.Rectangle((f_x-0.35, f_y-0.18), 0.70, 0.36, facecolor="#dc2626", edgecolor="#7f1d1d", lw=1.2, zorder=5))
    ax2.text(f_x, f_y, "Syndicate Account F\n(Isolated Illicit Node)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=6)

    for i, a in enumerate(np.linspace(0.1*np.pi, 0.9*np.pi, 5)):
        bx, by = 0.85 * np.cos(a), m_y + 0.65 * np.sin(a)
        ax2.add_patch(patches.Circle((bx, by), 0.09, facecolor="#dcfce7", edgecolor="#15803d", lw=0.9, zorder=5))
        ax2.text(bx, by, f"B{i+1}", ha="center", va="center", fontsize=6.0, color="#14532d", zorder=6)
        ax2.plot([bx, m_x], [by, m_y], color="#16a34a", lw=1.6, zorder=3)

    for offset in [-0.22, 0.0, 0.22]:
        ax2.plot([f_x+offset, m_x+offset], [f_y+0.18, m_y-0.18], color="#94a3b8", lw=1.0, linestyle=":", zorder=3)
        ax2.scatter([(f_x+m_x)/2 + offset], [(f_y+m_y)/2], marker="x", s=90, color="#dc2626", lw=2.2, zorder=5)

    ax2.text(0.0, (m_y+f_y)/2, r"PRUNED: $\hat{g}_{ij} < 0.10$ (65.9% Suppressed)", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#991b1b",
             bbox=dict(boxstyle="square,pad=0.25", facecolor="#ffffff", edgecolor="#fca5a5", lw=0.8))

    ax2.text(0.0, -1.18, r"Safety: $\mathcal{E}(\mathbf{H}) \geq 0.78$, C-STGB flags $\hat{p}_F = 0.96$ (Detected)",
             ha="center", va="center", fontsize=6.8, fontweight="bold", color="#166534",
             bbox=dict(boxstyle="square,pad=0.25", facecolor="#ffffff", edgecolor="#86efac", lw=0.8))

    save_figure(fig, "fig21_adversarial_camouflage_topology", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
'''

SCRIPTS["fig2_2_1wl_failure.py"] = '''"""
Figure 2.2: 1-WL Graph Isomorphism Bottleneck vs. 12-D Invariant Disambiguation
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=300)

    # Left: 1-WL Failure (6-Ring vs Disjoint 3-Cycles)
    ax1.set_xlim(-0.2, 4.2)
    ax1.set_ylim(-0.2, 4.2)
    ax1.axis("off")
    ax1.set_title("Standard Spatial GNN (1-WL Bottleneck: Identical Multisets)", fontsize=9.2, fontweight="bold", color="#991B1B")

    card1 = patches.Rectangle((0, 0), 4.0, 4.0, facecolor="#FEF2F2", edgecolor="#FCA5A5", lw=1.2)
    ax1.add_patch(card1)

    angles = np.linspace(0, 2 * np.pi, 7)[:-1]
    cx, cy, r = 1.3, 2.3, 0.85
    pts = [(cx + r * np.cos(a), cy + r * np.sin(a)) for a in angles]
    for i in range(6):
        ax1.plot([pts[i][0], pts[(i+1)%6][0]], [pts[i][1], pts[(i+1)%6][1]], color="#64748B", lw=2, zorder=2)
    for p in pts:
        ax1.scatter(p[0], p[1], s=140, color="#DC2626", edgecolor="black", zorder=3)
    ax1.text(cx, cy, "6-Node Wash Ring\\nMultiset: {{2,2}}", fontsize=7.2, fontweight="bold", ha="center", va="center")

    pts_t1 = [(3.0, 3.1), (3.6, 3.1), (3.3, 3.6)]
    pts_t2 = [(3.0, 1.2), (3.6, 1.2), (3.3, 1.7)]
    for tri in [pts_t1, pts_t2]:
        for i in range(3):
            ax1.plot([tri[i][0], tri[(i+1)%3][0]], [tri[i][1], tri[(i+1)%3][1]], color="#64748B", lw=2, zorder=2)
        for p in tri:
            ax1.scatter(p[0], p[1], s=140, color="#2563EB", edgecolor="black", zorder=3)
    ax1.text(3.3, 2.45, "Disjoint 3-Cycles\\nMultiset: {{2,2}}", fontsize=7.2, fontweight="bold", ha="center", va="center")

    fail_banner = patches.Rectangle((0.2, 0.2), 3.6, 0.65, facecolor="#B91C1C", edgecolor="black")
    ax1.add_patch(fail_banner)
    ax1.text(2.0, 0.52, "1-WL COLOR REFINEMENT FAILS\\nColor Histograms Identical: GNN Cannot Distinguish",
             fontsize=7.2, color="white", fontweight="bold", ha="center", va="center")

    # Right: C-STGB Invariant Disambiguation
    ax2.set_xlim(-0.2, 4.2)
    ax2.set_ylim(-0.2, 4.2)
    ax2.axis("off")
    ax2.set_title("C-STGB Solution (12-D Physical Invariant Disambiguation)", fontsize=9.2, fontweight="bold", color="#15803D")

    card2 = patches.Rectangle((0, 0), 4.0, 4.0, facecolor="#F0FDF4", edgecolor="#86EFAC", lw=1.2)
    ax2.add_patch(card2)

    box1 = patches.Rectangle((0.3, 2.2), 3.4, 1.4, facecolor="#DCFCE7", edgecolor="#16A34A", lw=1.0)
    ax2.add_patch(box1)
    ax2.text(2.0, 3.25, "6-Node Continuous Laundering Ring", fontsize=7.8, fontweight="bold", ha="center", color="#14532D")
    ax2.text(2.0, 2.85, r"Flow Conservation: $\Phi_{\mathrm{flow}} \approx 1.00$", fontsize=7.2, ha="center")
    ax2.text(2.0, 2.50, r"Degree Asymmetry: $\Psi_{\mathrm{asym}} = 0.00$ | $s_{\mathrm{fwd}} \geq 0.88$", fontsize=7.2, ha="center")

    box2 = patches.Rectangle((0.3, 0.6), 3.4, 1.4, facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.0)
    ax2.add_patch(box2)
    ax2.text(2.0, 1.65, "Disjoint 3-Cycles (Separate Merchant Hubs)", fontsize=7.8, fontweight="bold", ha="center", color="#1E3A8A")
    ax2.text(2.0, 1.25, r"Flow Conservation: $\Phi_{\mathrm{flow}} \approx 0.04$ (Absorption)", fontsize=7.2, ha="center")
    ax2.text(2.0, 0.90, r"Degree Asymmetry: $\Psi_{\mathrm{asym}} \ne 0.00$ | $s_{\mathrm{fwd}} \leq 0.05$", fontsize=7.2, ha="center")

    succ_banner = patches.Rectangle((0.2, 0.1), 3.6, 0.4, facecolor="#15803D", edgecolor="black")
    ax2.add_patch(succ_banner)
    ax2.text(2.0, 0.30, "PROVABLY DISAMBIGUATED BY 12-D CANONICAL INVARIANTS",
             fontsize=7.2, color="white", fontweight="bold", ha="center", va="center")

    save_figure(fig, "fig_2_3_1wl_failure_vs_invariants", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
'''

SCRIPTS["fig2_3_lit_evolution.py"] = '''"""
Figure 2.3: 2D Financial Crime Graph Learning Evolution Frontier
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, ax = plt.subplots(figsize=(8.2, 4.8), dpi=300)

    # Baselines data
    models = [
        ("GCN", 15, 43.55, "#94a3b8", "Static"),
        ("GraphSAGE", 25, 48.20, "#94a3b8", "Static"),
        ("EvolveGCN", 35, 51.04, "#38bdf8", "Discrete Dynamic"),
        ("GAT", 30, 52.40, "#94a3b8", "Static Attn"),
        ("CARE-GNN", 40, 64.50, "#f59e0b", "Camouflage Filter"),
        ("TGN", 65, 68.40, "#3b82f6", "Continuous Dynamic"),
        ("TGAT", 60, 67.20, "#3b82f6", "Continuous Dynamic"),
        ("H2-IDE", 43, 74.00, "#f59e0b", "Heterophily"),
        ("CamFD", 51, 83.00, "#f59e0b", "Camouflage Contrast"),
        ("GraphSMOTE", 55, 78.40, "#a855f7", "Imbalance SMOTE"),
        ("XGBoost", 20, 88.35, "#64748b", "Tabular Baseline"),
        ("C-STGB (Ours)", 92, 91.42, "#dc2626", "Proposed Framework")
    ]

    for name, x, y, color, tag in models:
        s = 200 if "C-STGB" in name else (130 if "XGBoost" in name else 85)
        ax.scatter(x, y, s=s, color=color, edgecolor="black", lw=1.0, zorder=5)
        
        # Staggered offsets for zero collision
        ox, oy = 2.0, 1.5
        if name == "H2-IDE": ox, oy = -14.0, 2.0
        elif name == "CamFD": ox, oy = -14.0, 2.0
        elif name == "TGN": ox, oy = 2.0, -3.5
        elif name == "TGAT": ox, oy = -16.0, 1.5
        elif name == "C-STGB (Ours)": ox, oy = -40.0, 2.2
        elif name == "XGBoost": ox, oy = 2.5, -3.5
        
        fw = "bold" if "C-STGB" in name else "normal"
        ax.annotate(name, (x, y), xytext=(x + ox, y + oy), fontsize=7.2, fontweight=fw)

    # Evolution arrows
    ax.annotate("", xy=(33, 50), xytext=(20, 44), arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=1.2, ls="--"))
    ax.annotate("", xy=(62, 67), xytext=(38, 52), arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.2, ls="--"))
    ax.annotate("", xy=(88, 90), xytext=(68, 70), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.6))

    ax.set_xlabel(r"Spatio-Temporal Topological Expressiveness Rating $\longrightarrow$", fontsize=9.0, fontweight="bold")
    ax.set_ylabel(r"Elliptic-v1 Minority Illicit F1-Score (%) $\longrightarrow$", fontsize=9.0, fontweight="bold")
    ax.set_xlim([10, 100])
    ax.set_ylim([35, 96])
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_title("Evolutionary SOTA Frontier in Graph Financial Crime Surveillance", fontweight="bold", fontsize=10.0, pad=10)

    save_figure(fig, "fig_lit_evolution_frontier", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
'''

print(f"Writing {len(SCRIPTS)} scripts to {OUT_DIR}...")
for fname, code in SCRIPTS.items():
    p = OUT_DIR / fname
    with open(p, "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print(f"  [OK] Created: {p}")

