"""
render_publication_diagrams.py — Research-Grade Publication Vector Visual Generator.

Generates the core conceptual diagrams for EAAI & Thesis:
1. Figure 6 / Fig 1.1 / Fig 3.1: C-STGB End-to-End Master Pipeline Flowchart
   (6 Modular Boxes: Ingest -> Temporal GNN -> GraphSMOTE -> Fusion -> Bayes -> CRC)
2. Figure 3.2: 12-D Canonical Invariants Funnel
   (4 Ledgers -> Universal 12-D Invariant Vector -> Frozen GNN Backbone)
3. Figure 5.1 / Figure 12: Deterministic 3-Tier Conformal Risk Control (CRC) Decision Tree
   (Root Score -> Dual-Quantile Diamond -> Tier 1 / 2 / 3 + 10k Stacked Volume Bar)
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Publication Typography & Rendering Settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent

eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"

OUT_DIRS = [data_fig_dir, eaai_fig_dir, thesis_fig_dir]
for d in OUT_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_fig_all(fig, stem_names):
    if isinstance(stem_names, str):
        stem_names = [stem_names]
    for stem in stem_names:
        for d in OUT_DIRS:
            pdf_p = d / f"{stem}.pdf"
            png_p = d / f"{stem}.png"
            fig.savefig(pdf_p, bbox_inches="tight", pad_inches=0.04)
            fig.savefig(png_p, dpi=300, bbox_inches="tight", pad_inches=0.04)
        print(f"   ✓ Generated: {stem}.pdf & .png")
    plt.close(fig)


# ==============================================================================
# 1. MASTER PIPELINE FLOWCHART (Fig 1.1, Fig 3.1, Fig 6) (7.16" x 2.30")
# ==============================================================================
print("[1/3] Generating Master Pipeline Flowchart (Fig 1.1 / Fig 3.1 / Fig 6)...")
fig, ax = plt.subplots(figsize=(7.16, 2.30))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.020, 1.020])

# Top Master Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.010, 0.905), 0.980, 0.082,
    boxstyle="round,pad=0.003,rounding_size=0.006",
    facecolor="#0f172a", edgecolor="#0f172a", linewidth=0.5
))
ax.text(0.50, 0.946, "C-STGB: Conformal Spatio-Temporal GraphBoost End-to-End Surveillance Platform",
        ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff")

# 6 Module Definitions with unified color per module
modules = [
    {
        "num": "M1", "title": "Ingest & Invariants",
        "badge_bg": "#1e40af", "badge_fg": "#eff6ff", "card_bg": "#f8fafc", "border": "#93c5fd",
        "headline": "12-D Invariants", "hl_bg": "#dbeafe", "hl_fg": "#1e40af",
        "bullets": ["Kirchhoff mass balance", "Hawkes arrival intensity"],
        "out": r"$\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$",
        "x": 0.012, "w": 0.150
    },
    {
        "num": "M2", "title": "Temporal GNN",
        "badge_bg": "#0f766e", "badge_fg": "#f0fdfa", "card_bg": "#f8fafc", "border": "#99f6e4",
        "headline": "3-Band Harmonic", "hl_bg": "#ccfbf1", "hl_fg": "#0f766e",
        "bullets": ["Brody dynamic attention", "Edge-trust chaff pruning"],
        "out": r"$\mathbf{h}_u^{(L)} \in \mathbb{R}^{d}$",
        "x": 0.176, "w": 0.150
    },
    {
        "num": "M3", "title": "Latent GraphSMOTE",
        "badge_bg": "#c2410c", "badge_fg": "#fff7ed", "card_bg": "#f8fafc", "border": "#fed7aa",
        "headline": "+9.92 pp Minority", "hl_bg": "#ffedd5", "hl_fg": "#c2410c",
        "bullets": ["Latent typology clusters", "Bilinear link prediction"],
        "out": r"$\tilde{\mathcal{G}}_{\mathrm{train}}$",
        "x": 0.340, "w": 0.150
    },
    {
        "num": "M4", "title": "Adaptive Fusion",
        "badge_bg": "#6d28d9", "badge_fg": "#faf5ff", "card_bg": "#f8fafc", "border": "#e9d5ff",
        "headline": "89.60% Cold-Start", "hl_bg": "#ede9fe", "hl_fg": "#6d28d9",
        "bullets": ["Degree-adaptive gating", "Graph-tabular union"],
        "out": r"$\mathbf{h}_u^* \in \mathbb{R}^{d^*}$",
        "x": 0.504, "w": 0.150
    },
    {
        "num": "M5", "title": "Bayes Risk Head",
        "badge_bg": "#15803d", "badge_fg": "#f0fdf4", "card_bg": "#f8fafc", "border": "#bbf7d0",
        "headline": r"$\tau^* = 0.18$ Optimal", "hl_bg": "#dcfce7", "hl_fg": "#15803d",
        "bullets": ["Asymmetric loss head", "15:1 cost-sensitive tuning"],
        "out": r"$\hat{p}_u \in [0, 1]$",
        "x": 0.668, "w": 0.150
    },
    {
        "num": "M6", "title": "Conformal Triage",
        "badge_bg": "#b91c1c", "badge_fg": "#fef2f2", "card_bg": "#f8fafc", "border": "#fecaca",
        "headline": "99.50% STP Cut", "hl_bg": "#fee2e2", "hl_fg": "#b91c1c",
        "bullets": ["Dual-quantile threshold", "Assisted FinCEN SAR Dossier"],
        "out": r"$\Gamma(u) \subseteq \{0, 1\}$",
        "x": 0.832, "w": 0.156
    }
]

y_bottom = 0.025
card_h = 0.855

for i, m in enumerate(modules):
    x0 = m["x"]
    w0 = m["w"]
    
    # Outer Container Card
    ax.add_patch(patches.FancyBboxPatch(
        (x0, y_bottom), w0, card_h,
        boxstyle="round,pad=0.004,rounding_size=0.007",
        facecolor=m["card_bg"], edgecolor=m["border"], linewidth=1.1
    ))
    
    # Header Module Pill
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.004, y_bottom + card_h - 0.088), w0 - 0.008, 0.080,
        boxstyle="round,pad=0.003,rounding_size=0.005",
        facecolor=m["badge_bg"], edgecolor=m["badge_bg"], linewidth=0.5
    ))
    ax.text(x0 + w0/2, y_bottom + card_h - 0.030, m["num"],
            ha="center", va="center", fontsize=6.2, fontweight="bold", color=m["badge_fg"])
    ax.text(x0 + w0/2, y_bottom + card_h - 0.062, m["title"],
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
    
    # Headline Highlight Pill
    y_hl = y_bottom + card_h - 0.165
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.006, y_hl), w0 - 0.012, 0.068,
        boxstyle="round,pad=0.002,rounding_size=0.004",
        facecolor=m["hl_bg"], edgecolor=m["border"], linewidth=0.7
    ))
    ax.text(x0 + w0/2, y_hl + 0.034, m["headline"],
            ha="center", va="center", fontsize=6.8, fontweight="bold", color=m["hl_fg"])
    
    # 2 Bullet Points
    y_bullets = y_hl - 0.045
    for b_idx, bullet in enumerate(m["bullets"]):
        y_b = y_bullets - (b_idx * 0.070)
        ax.plot([x0 + 0.012], [y_b], marker="o", markersize=2.6, color=m["badge_bg"])
        ax.text(x0 + 0.020, y_b, bullet, ha="left", va="center", fontsize=5.8, color="#334155")
    
    # Bottom Output Tag
    y_out = y_bottom + 0.045
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.006, y_out - 0.032), w0 - 0.012, 0.060,
        boxstyle="round,pad=0.002,rounding_size=0.004",
        facecolor="#f1f5f9", edgecolor="#cbd5e1", linewidth=0.6
    ))
    ax.text(x0 + w0/2, y_out - 0.002, m["out"],
            ha="center", va="center", fontsize=6.3, fontweight="bold", color="#0f172a")

    # Arrow to Next Module
    if i < len(modules) - 1:
        x_arrow_start = x0 + w0 + 0.002
        x_arrow_end = modules[i+1]["x"] - 0.002
        y_arrow = y_bottom + card_h / 2
        ax.annotate("", xy=(x_arrow_end, y_arrow), xytext=(x_arrow_start, y_arrow),
                    arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", lw=1.3, color="#64748b"))

plt.subplots_adjust(left=0.005, right=0.995, top=0.985, bottom=0.015)
save_fig_all(fig, ["fig6_system_architecture", "pipeline_cstgb"])


# ==============================================================================
# 2. FIGURE 3.2: 12-D CANONICAL INVARIANTS FUNNEL (7.16" x 2.65")
# ==============================================================================
print("[2/3] Generating Fig 3.2: 12-D Invariants Funnel Diagram...")
fig, ax = plt.subplots(figsize=(7.16, 2.65))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.010, 0.910), 0.980, 0.080,
    boxstyle="round,pad=0.003,rounding_size=0.006",
    facecolor="#0f172a", edgecolor="#0f172a", linewidth=0.5
))
ax.text(0.50, 0.950, "Canonical 12-D Invariant Funnel: Universal Zero-Shot Cross-Ledger Transfer",
        ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff")

# Panel 1: 4 Heterogeneous Source Ledgers (Left: x = 0.015 to 0.245)
ledgers = [
    ("Bitcoin UTXO", "Mempool timestamps & coin age", "#1e3a8a", "#dbeafe"),
    ("Ethereum EVM", "Smart contract gas & ERC-20", "#0369a1", "#e0f2fe"),
    ("ISO 20022 Rails", "SWIFT pacs.008 & Fedwire", "#0f766e", "#ccfbf1"),
    ("Agent Simulators", "IBM AMLSim & PaySim rings", "#4338ca", "#e0e7ff")
]

y_l = 0.700
h_l = 0.170
for name, desc, c_fg, c_bg in ledgers:
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, y_l), 0.230, h_l,
        boxstyle="round,pad=0.003,rounding_size=0.005",
        facecolor="#ffffff", edgecolor=c_fg, linewidth=0.9
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (0.020, y_l + h_l - 0.062), 0.220, 0.054,
        boxstyle="round,pad=0.002,rounding_size=0.004",
        facecolor=c_bg, edgecolor=c_bg, linewidth=0.2
    ))
    ax.text(0.130, y_l + h_l - 0.035, name, ha="center", va="center", fontsize=6.8, fontweight="bold", color=c_fg)
    ax.text(0.130, y_l + 0.045, desc, ha="center", va="center", fontsize=5.8, color="#475569")
    
    # Funnel trajectory arrows pointing toward the neck (x=0.290, y=0.450)
    y_center = y_l + h_l / 2
    ax.annotate("", xy=(0.285, 0.450), xytext=(0.248, y_center),
                arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color=c_fg, lw=1.2, alpha=0.75))
    y_l -= 0.215

# Funnel Neck / Center: Universal 12-D Canonical Invariant Capsule (x = 0.290 to 0.710)
funnel_card = patches.FancyBboxPatch(
    (0.290, 0.045), 0.415, 0.835,
    boxstyle="round,pad=0.006,rounding_size=0.008",
    facecolor="#f0fdf4", edgecolor="#15803d", linewidth=1.2
)
ax.add_patch(funnel_card)

# Center Header
ax.add_patch(patches.FancyBboxPatch(
    (0.300, 0.795), 0.395, 0.075,
    boxstyle="round,pad=0.003,rounding_size=0.005",
    facecolor="#15803d", edgecolor="#15803d", linewidth=0.5
))
ax.text(0.4975, 0.832, r"Universal 12-D Canonical Invariant Vector ($\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$)",
        ha="center", va="center", fontsize=7.4, fontweight="bold", color="#ffffff")

inv_groups = [
    ("Group 1: Kirchhoff Flow Balance", r"$\Phi_{\mathrm{flow}} = \sum A_{\mathrm{out}} / (\sum A_{\mathrm{in}} + \epsilon)$", "Mule pass-through ~1.0 balance", "#14532d"),
    ("Group 2: Hawkes Burst Rate", r"$\lambda_u(t) = \mu_0 + \sum \alpha e^{-\beta(t - t_i)}$", "Continuous micro-burst acceleration", "#166534"),
    ("Group 3: Bi-Directional Taint", r"$\mathbf{s}_{\mathrm{fwd}}, \mathbf{s}_{\mathrm{bwd}} = (1-\alpha)(\mathbf{I}-\alpha\mathbf{P})^{-1}\mathbf{s}_0$", "Causal illicit PageRank proximity", "#15803d"),
    ("Group 4: 5-Moment Amount Stats", r"$\mu_A, \mathrm{Var}(A), \gamma_A, \kappa_A, \nu_{\mathrm{io}}$ & Temporal Jitter", "Higher-order ego transaction dispersion", "#16a34a"),
]

y_grp = 0.615
for g_title, g_math, g_desc, g_clr in inv_groups:
    ax.add_patch(patches.FancyBboxPatch(
        (0.300, y_grp), 0.395, 0.160,
        boxstyle="round,pad=0.003,rounding_size=0.004",
        facecolor="#ffffff", edgecolor="#bbf7d0", linewidth=0.7
    ))
    ax.text(0.312, y_grp + 0.122, g_title, ha="left", va="center", fontsize=6.4, fontweight="bold", color=g_clr)
    ax.text(0.4975, y_grp + 0.074, g_math, ha="center", va="center", fontsize=6.2, color="#0f172a")
    ax.text(0.312, y_grp + 0.028, g_desc, ha="left", va="center", fontsize=5.6, color="#475569")
    y_grp -= 0.185

# Expanding Funnel Arrows to Right Panel
ax.annotate("", xy=(0.755, 0.650), xytext=(0.710, 0.450),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", color="#1e40af", lw=1.4))
ax.annotate("", xy=(0.755, 0.450), xytext=(0.710, 0.450),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", color="#1e40af", lw=1.4))
ax.annotate("", xy=(0.755, 0.250), xytext=(0.710, 0.450),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", color="#1e40af", lw=1.4))

# Panel 3: Frozen GNN Backbone & Target Transfer (Right: x = 0.755 to 0.985)
ax.add_patch(patches.FancyBboxPatch(
    (0.755, 0.045), 0.230, 0.835,
    boxstyle="round,pad=0.006,rounding_size=0.008",
    facecolor="#eff6ff", edgecolor="#1e40af", linewidth=1.2
))
ax.add_patch(patches.FancyBboxPatch(
    (0.762, 0.795), 0.216, 0.075,
    boxstyle="round,pad=0.003,rounding_size=0.005",
    facecolor="#1e40af", edgecolor="#1e40af", linewidth=0.5
))
ax.text(0.870, 0.832, "Frozen GNN Backbone", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")

frozen_cards = [
    ("Zero Fine-Tuning", r"100% frozen weights ($\eta=0$)", "#1e3a8a"),
    ("Target Transfer F1", "82.40% Macro F1 Score", "#059669"),
    ("Invariant Lift", "+28.2 pp vs raw features", "#b91c1c"),
    ("Universal Basis", "Consistent cross-rail space", "#6d28d9")
]

y_fr = 0.615
for f_head, f_sub, f_clr in frozen_cards:
    ax.add_patch(patches.FancyBboxPatch(
        (0.762, y_fr), 0.216, 0.160,
        boxstyle="round,pad=0.003,rounding_size=0.004",
        facecolor="#ffffff", edgecolor="#bfdbfe", linewidth=0.7
    ))
    ax.text(0.870, y_fr + 0.108, f_head, ha="center", va="center", fontsize=6.6, fontweight="bold", color=f_clr)
    ax.text(0.870, y_fr + 0.045, f_sub, ha="center", va="center", fontsize=5.8, color="#334155")
    y_fr -= 0.185

plt.subplots_adjust(left=0.005, right=0.995, top=0.985, bottom=0.015)
save_fig_all(fig, "fig_canonical_invariants")


# ==============================================================================
# 3. FIGURE 5.1: 3-TIER CONFORMAL TRIAGE DECISION TREE (7.16" x 2.80")
# ==============================================================================
print("[3/3] Generating Fig 5.1: Conformal Triage Decision Tree & Stacked Bar...")
fig, ax = plt.subplots(figsize=(7.16, 2.80))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.010, 0.910), 0.980, 0.080,
    boxstyle="round,pad=0.003,rounding_size=0.006",
    facecolor="#0f172a", edgecolor="#0f172a", linewidth=0.5
))
ax.text(0.50, 0.950, "Deterministic 3-Tier Conformal Risk Control (CRC) Operational Triage Pipeline",
        ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff")

# Root Node: Posterior Score p_u (x = 0.020, y = 0.520)
ax.add_patch(patches.FancyBboxPatch(
    (0.020, 0.440), 0.190, 0.220,
    boxstyle="round,pad=0.004,rounding_size=0.006",
    facecolor="#f8fafc", edgecolor="#0284c7", linewidth=1.2
))
ax.add_patch(patches.FancyBboxPatch(
    (0.025, 0.590), 0.180, 0.060,
    boxstyle="round,pad=0.002,rounding_size=0.004",
    facecolor="#0284c7", edgecolor="#0284c7", linewidth=0.5
))
ax.text(0.115, 0.620, "C-STGB Risk Engine", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
ax.text(0.115, 0.520, r"Posterior Risk: $\hat{p}_u \in [0, 1]$", ha="center", va="center", fontsize=6.5, fontweight="bold", color="#0f172a")
ax.text(0.115, 0.465, r"Non-conf: $s_u^{(y)} = 1 - \hat{p}_u(y)$", ha="center", va="center", fontsize=5.8, color="#475569")

# Decision Diamond in Center: Dual Quantile Evaluation
# Diamond points: center at (0.340, 0.550)
diamond_x = 0.340
diamond_y = 0.550
d_w = 0.085
d_h = 0.130
diamond = patches.Polygon([
    (diamond_x, diamond_y + d_h),
    (diamond_x + d_w, diamond_y),
    (diamond_x, diamond_y - d_h),
    (diamond_x - d_w, diamond_y)
], closed=True, facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.2)
ax.add_patch(diamond)
ax.text(diamond_x, diamond_y + 0.035, "Dual Quantiles", ha="center", va="center", fontsize=6.5, fontweight="bold", color="#92400e")
ax.text(diamond_x, diamond_y - 0.020, r"$\hat{q}^{(0)}, \hat{q}^{(1)}$", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#b45309")
ax.text(diamond_x, diamond_y - 0.065, r"$1-\alpha \geq 99\%$", ha="center", va="center", fontsize=5.8, color="#78350f")

# Connect Root to Decision Diamond
ax.annotate("", xy=(diamond_x - d_w, diamond_y), xytext=(0.210, 0.550),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", color="#0f172a", lw=1.3))

# Three Outcome Branches:
# Branch 1 (Top): Tier 1 Quarantine Gamma = {1}
# Branch 2 (Middle): Tier 2 Human Review Gamma = {0, 1}
# Branch 3 (Bottom): Tier 3 Straight-Through Clear Gamma = {0}

tiers = [
    {
        "tier": "Tier 1: High-Risk Quarantine",
        "set": r"$\Gamma(u) = \{1\}$",
        "action": "Immediate Quarantine Hold & Multi-Agent FinCEN SAR",
        "stat": "18 alerts / 10,000 tx  (0.18%)",
        "badge_bg": "#b91c1c", "card_bg": "#fef2f2", "border": "#fca5a5",
        "y": 0.690, "branch_label": "High Illicit\n" + r"$s_u^{(1)} \le \hat{q}^{(1)}$"
    },
    {
        "tier": "Tier 2: Selective Abstention",
        "set": r"$\Gamma(u) = \{0, 1\} = \bot$",
        "action": "Boundary Ambiguity: Escalate to Compliance Review Desk",
        "stat": "50 alerts / 10,000 tx  (0.50%)",
        "badge_bg": "#d97706", "card_bg": "#fffbeb", "border": "#fde68a",
        "y": 0.440, "branch_label": "Boundary\nAmbiguous"
    },
    {
        "tier": "Tier 3: Straight-Through Clear",
        "set": r"$\Gamma(u) = \{0\}$",
        "action": "High-Confidence Benign: Instant Straight-Through Clear (STP)",
        "stat": "9,932 tx / 10,000 tx  (99.32%)",
        "badge_bg": "#15803d", "card_bg": "#f0fdf4", "border": "#86efac",
        "y": 0.190, "branch_label": "High Benign\n" + r"$s_u^{(0)} \le \hat{q}^{(0)}$"
    }
]

for t in tiers:
    y_t = t["y"]
    # Outer card
    ax.add_patch(patches.FancyBboxPatch(
        (0.520, y_t), 0.465, 0.200,
        boxstyle="round,pad=0.003,rounding_size=0.005",
        facecolor=t["card_bg"], edgecolor=t["border"], linewidth=1.1
    ))
    # Pill
    ax.add_patch(patches.FancyBboxPatch(
        (0.525, y_t + 0.135), 0.155, 0.055,
        boxstyle="round,pad=0.002,rounding_size=0.004",
        facecolor=t["badge_bg"], edgecolor=t["badge_bg"], linewidth=0.5
    ))
    ax.text(0.6025, y_t + 0.162, t["set"], ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
    ax.text(0.690, y_t + 0.162, t["tier"], ha="left", va="center", fontsize=6.8, fontweight="bold", color=t["badge_bg"])
    
    ax.text(0.535, y_t + 0.088, t["action"], ha="left", va="center", fontsize=5.9, color="#0f172a")
    ax.text(0.535, y_t + 0.035, t["stat"], ha="left", va="center", fontsize=6.2, fontweight="bold", color=t["badge_bg"])
    
    # Connecting arrow from diamond to branch card
    y_card_center = y_t + 0.100
    ax.annotate("", xy=(0.518, y_card_center), xytext=(diamond_x + d_w, diamond_y),
                arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color=t["badge_bg"], lw=1.3))

# Bottom Section: Stacked Bar of 10,000 Transactions
y_bar = 0.035
h_bar = 0.090

# Canvas card for bottom section
ax.add_patch(patches.FancyBboxPatch(
    (0.015, 0.010), 0.970, 0.145,
    boxstyle="round,pad=0.003,rounding_size=0.005",
    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8
))

ax.text(0.025, 0.118, "Streaming Volume Triage Breakdown (10,000 Transactions):",
        ha="left", va="center", fontsize=6.4, fontweight="bold", color="#0f172a")

# Stacked bar coordinates
bar_x0 = 0.025
bar_w = 0.950

# Scaled widths visually representing 18 (0.18%), 50 (0.50%), 9932 (99.32%) with visible min sizes
w1 = 0.070  # 18
w2 = 0.120  # 50
w3 = bar_w - w1 - w2  # 9,932

# Tier 1 segment (Red)
ax.add_patch(patches.Rectangle((bar_x0, y_bar), w1, 0.055, facecolor="#b91c1c", edgecolor="none"))
ax.text(bar_x0 + w1/2, y_bar + 0.027, "18 (0.18%)", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#ffffff")

# Tier 2 segment (Amber)
ax.add_patch(patches.Rectangle((bar_x0 + w1, y_bar), w2, 0.055, facecolor="#d97706", edgecolor="none"))
ax.text(bar_x0 + w1 + w2/2, y_bar + 0.027, "50 (0.50%)", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#ffffff")

# Tier 3 segment (Green)
ax.add_patch(patches.Rectangle((bar_x0 + w1 + w2, y_bar), w3, 0.055, facecolor="#15803d", edgecolor="none"))
ax.text(bar_x0 + w1 + w2 + w3/2, y_bar + 0.027, "Tier 3 Straight-Through Automated Clear: 9,932 tx (99.32%)",
        ha="center", va="center", fontsize=6.2, fontweight="bold", color="#ffffff")

# Callout banner
ax.text(0.970, 0.118, "Workload Reduction: -99.50% | Finite-Sample Coverage: 1-α ≥ 99.0%",
        ha="right", va="center", fontsize=6.3, fontweight="bold", color="#15803d")

plt.subplots_adjust(left=0.005, right=0.995, top=0.985, bottom=0.010)
save_fig_all(fig, "fig_conformal_triage_flowchart")

print("render_publication_diagrams.py completed successfully!")
