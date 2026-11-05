"""
generate_action_plan_diagrams.py — Publication Vector Visuals for Thesis and EAAI:
1. Fig 4.2: Database Entity-Relationship Diagram (ERD) with 12-D View & Causal Indexes (fig4_2_database_erd)
2. Fig 3.1: Neural Tensor Flow & Message-Passing Block Diagram with dedicated Math Strip (fig3_1_tensor_flow)
3. Fig 8.2: Real-Time UML Sequence Lifeline Diagram with Latency Timestamps (fig8_2_uml_sequence_lifeline)
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import numpy as np

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
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'stix',
})

BASE_DIR = Path(__file__).resolve().parent.parent
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"

TARGET_DIRS = [data_fig_dir, thesis_fig_dir, eaai_fig_dir]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_fig(fig, stem):
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f" [OK] Generated: {stem}.pdf & .png")


# ==============================================================================
# 1. FIG 4.2: DATABASE ENTITY-RELATIONSHIP DIAGRAM (ERD)
# ==============================================================================
print("Generating Fig 4.2: Relational Database ERD and Materialized Graph View...")
from redesign_fig4_2_database_erd import generate_figure_4_2
fig = generate_figure_4_2()
save_fig(fig, "fig4_2_database_erd")

# ==============================================================================
# 2. FIG 3.1: NEURAL TENSOR FLOW & MESSAGE-PASSING BLOCK DIAGRAM (7.16" x 3.65")
# ==============================================================================
print("Generating Fig 3.1: Dedicated Neural Tensor Flow & Message-Passing Block Diagram...")
fig, ax = plt.subplots(figsize=(7.16, 3.65))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Outer background
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.920), 0.984, 0.072,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.956, 'C-STGB Neural Tensor Flow: Message Passing, Harmonic Encoders, Edge Gates & Fusion',
        ha='center', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')

# 5 Main Processing Columns across the Neural Tensor Pipeline
# Col 1: 3-Band Harmonic Encoder
# Col 2: Edge-Trust MLP Gate
# Col 3: Spatio-Temporal Temporal Conv / Attention
# Col 4: Typology GraphSMOTE Bilinear Head
# Col 5: Cold-Start Fusion & Bayes Risk Head

cols = [
    {
        "id": "STEP 1: ENCODER",
        "title": "3-Band Temporal",
        "badge_bg": "#1e40af", "badge_fg": "#eff6ff", "card_bg": "#f8fafc", "border": "#93c5fd",
        "x": 0.012, "w": 0.182,
        "items": [
            ("Raw Input Tensors", r"$\mathbf{x}_u \in \mathbb{R}^d, \; \mathbf{e}_{uv} \in \mathbb{R}^{d_e}$", "#0f172a"),
            ("Harmonic Band 1", r"$\Phi_{\text{burst}}(\Delta t) \in \mathbb{R}^{d/3}$", "#1e40af"),
            ("Harmonic Band 2", r"$\Phi_{\text{diurnal}}(\Delta t) \; (24\text{h})$", "#0f766e"),
            ("Harmonic Band 3", r"$\Phi_{\text{macro}}(\Delta t) \; (90\text{d})$", "#b91c1c"),
            ("Hawkes State", r"$\lambda_u(t) = \mu_0 + \sum \alpha e^{-\beta \Delta t}$", "#6d28d9")
        ],
        "out_tensor": r"$\mathbf{h}_u^{\,(0)} \in \mathbb{R}^{d_{\text{embed}}}$"
    },
    {
        "id": "STEP 2: EDGE GATE",
        "title": "Edge-Trust MLP",
        "badge_bg": "#0f766e", "badge_fg": "#f0fdfa", "card_bg": "#f8fafc", "border": "#99f6e4",
        "x": 0.208, "w": 0.182,
        "items": [
            ("Edge Context Cat", r"$[\mathbf{h}_u \parallel \mathbf{h}_v \parallel \mathbf{e}_{uv} \parallel \Phi_{\text{time}}]$", "#0f172a"),
            ("Trust Scoring MLP", r"$g_{ij} = \sigma(\mathbf{W}_g^\top [\cdot] + b_g)$", "#0f766e"),
            ("Floor Regularizer", r"$\hat{g}_{ij} = \delta_0 + (1 - \delta_0) g_{ij}$", "#0f766e"),
            ("Threshold Floor", r"$\delta_{\text{floor}} = 0.10 \text{ (Prunes 65.9\%)}$", "#b91c1c"),
            ("Denoised Graph", r"$\tilde{\mathcal{E}} = \{(u, v) : \hat{g}_{uv} \geq 0.10\}$", "#15803d")
        ],
        "out_tensor": r"$\mathbf{A}_{\text{gated}} = \hat{\mathbf{G}} \odot \mathbf{A}$"
    },
    {
        "id": "STEP 3: MESSAGE PASS",
        "title": "Continuous HGT",
        "badge_bg": "#c2410c", "badge_fg": "#fff7ed", "card_bg": "#f8fafc", "border": "#fed7aa",
        "x": 0.404, "w": 0.182,
        "items": [
            ("Hetero Message", r"$\mathbf{m}_{vu} = \mathbf{W}_v \, \mathbf{h}^{(l-1)}(v) \, \hat{g}_{vu}$", "#0f172a"),
            ("Harmonic Attention", r"$\alpha_{vu} = \mathrm{Softmax}(\mathbf{q}_u^\top \mathbf{k}_v / \sqrt{d})$", "#c2410c"),
            ("Brody Curvature", r"$\kappa(u, v) \text{ Riemannian bound}$", "#c2410c"),
            ("Neighborhood Agg", r"$\tilde{\mathbf{h}}_u = \sum \alpha_{vu} \mathbf{m}_{vu} \quad (v \in \mathcal{N}_u)$", "#0f766e"),
            ("Feed-Forward Layer", r"$\mathbf{h}^{(l)}(u) = \mathrm{LayerNorm}(\mathbf{h}_u + \mathrm{MLP})$", "#6d28d9")
        ],
        "out_tensor": r"$\mathbf{h}_u^{\,(L)} \in \mathbb{R}^d \text{ (Structural)}$"
    },
    {
        "id": "STEP 4: GRAPH-SMOTE",
        "title": "Latent Typology",
        "badge_bg": "#6d28d9", "badge_fg": "#faf5ff", "card_bg": "#f8fafc", "border": "#e9d5ff",
        "x": 0.600, "w": 0.182,
        "items": [
            ("Typology Clusters", r"$\mathcal{C}_1, \dots, \mathcal{C}_K \; (\tau_{\mathrm{sim}} \geq 0.75)$", "#0f172a"),
            ("Intra-Cluster Interp", r"$\mathbf{h}_{\mathrm{syn}} = (1-\rho)\mathbf{h}_u + \rho \mathbf{h}_v$", "#6d28d9"),
            ("Bilinear Link Head", r"$\hat{A}_{\mathrm{syn}, w} = \sigma(\mathbf{h}_{\mathrm{syn}}^T \mathbf{W}_e \mathbf{h}_w)$", "#6d28d9"),
            ("Flow Invariant Check", r"$\Phi_{\mathrm{flow}}(\mathrm{syn}) \approx 1.0 \text{ (Pass-thru)}$", "#15803d"),
            ("Train Isolation", r"100% Quarantined to $\mathcal{D}_{\mathrm{train}}$", "#b91c1c")
        ],
        "out_tensor": r"$\tilde{\mathcal{G}}_{\mathrm{train}} \text{ (+9.92 pp Lift)}$"
    },
    {
        "id": "STEP 5: FUSION & HEAD",
        "title": "Cold-Start & Bayes",
        "badge_bg": "#15803d", "badge_fg": "#f0fdf4", "card_bg": "#f8fafc", "border": "#bbf7d0",
        "x": 0.796, "w": 0.192,
        "items": [
            ("Universal Invariant", r"$\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12} \text{ (Kirchhoff)}$", "#0f172a"),
            ("Evidence Gating", r"$\alpha_u = \sigma(\mathbf{w}_\alpha^\top [\mathbf{h}_u \parallel \mathbf{z}_{\mathrm{inv}}])$", "#15803d"),
            ("Fused Embedding", r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$", "#15803d"),
            ("Bayes Loss Policy", r"$\mathcal{L}_{\mathrm{asym}} = 15 \cdot \mathrm{FN} + 1 \cdot \mathrm{FP}$", "#b91c1c"),
            ("Optimal Cutoff", r"$\tau^* = 0.18 \rightarrow \hat{y} = \mathbf{1}(\hat{p} \geq 0.18)$", "#b91c1c")
        ],
        "out_tensor": r"$\hat{p}_u \in [0, 1] \rightarrow \Gamma(u)$"
    }
]

y_card = 0.225
h_card = 0.680

for col in cols:
    cx, cw = col["x"], col["w"]
    # Outer card
    ax.add_patch(patches.FancyBboxPatch((cx, y_card), cw, h_card, boxstyle='round,pad=0.003,rounding_size=0.006',
                                        facecolor=col["card_bg"], edgecolor=col["border"], linewidth=1.1))
    # Header Pill
    ax.add_patch(patches.FancyBboxPatch((cx + 0.004, y_card + h_card - 0.082), cw - 0.008, 0.076,
                                        boxstyle='round,pad=0.002,rounding_size=0.004',
                                        facecolor=col["badge_bg"], edgecolor=col["badge_bg"]))
    ax.text(cx + cw/2, y_card + h_card - 0.026, col["id"], ha='center', va='center',
            fontsize=6.2, fontweight='bold', color='#ffffff')
    ax.text(cx + cw/2, y_card + h_card - 0.058, col["title"], ha='center', va='center',
            fontsize=5.8, color=col["badge_fg"], style='italic')

    # Item rows
    y_row_top = y_card + h_card - 0.096
    for idx, (label, math_str, clr) in enumerate(col["items"]):
        y_r = y_row_top - (idx * 0.100) - 0.040
        ax.add_patch(patches.FancyBboxPatch((cx + 0.006, y_r - 0.045), cw - 0.012, 0.086,
                                            boxstyle='round,pad=0.002,rounding_size=0.003',
                                            facecolor='#ffffff', edgecolor='#e2e8f0', linewidth=0.5))
        ax.text(cx + 0.012, y_r + 0.024, label, ha='left', va='center', fontsize=5.3, fontweight='bold', color='#334155')
        ax.text(cx + cw/2, y_r - 0.016, math_str, ha='center', va='center', fontsize=5.5, color=clr)

    # Output Tensor tag
    y_out = y_card + 0.014
    ax.add_patch(patches.FancyBboxPatch((cx + 0.006, y_out), cw - 0.012, 0.048,
                                        boxstyle='round,pad=0.002,rounding_size=0.003',
                                        facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(cx + cw/2, y_out + 0.024, col["out_tensor"], ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#0f172a')

# Tensor Flow Arrows across columns
for i in range(len(cols) - 1):
    x_st = cols[i]["x"] + cols[i]["w"] + 0.001
    x_en = cols[i+1]["x"] - 0.001
    y_arr = y_card + h_card / 2
    ax.annotate("", xy=(x_en, y_arr), xytext=(x_st, y_arr),
                arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color="#64748b", lw=1.2))

# DEDICATED BOTTOM MATH STRIP (Full Width)
ms_x, ms_y, ms_w, ms_h = 0.012, 0.016, 0.976, 0.190
ax.add_patch(patches.FancyBboxPatch((ms_x, ms_y), ms_w, ms_h, boxstyle='round,pad=0.003,rounding_size=0.005',
                                    facecolor='#f8fafc', edgecolor='#0f172a', linewidth=1.0))
# Strip Header
ax.add_patch(patches.FancyBboxPatch((ms_x + 0.004, ms_y + ms_h - 0.046), ms_w - 0.008, 0.042,
                                    boxstyle='round,pad=0.002,rounding_size=0.003',
                                    facecolor='#0f172a', edgecolor='#0f172a'))
ax.text(ms_x + ms_w/2, ms_y + ms_h - 0.025,
        r'MATHEMATICAL INVARIANT & GUARANTEE STRIP (EQUATIONS 1–22 ALIGNMENT)',
        ha='center', va='center', fontsize=6.8, fontweight='bold', color='#ffffff')

math_blocks = [
    (r"1. Invariant Space $\mathbf{z}_{\mathrm{inv}}$",
     r"$\tilde{\Phi}_{\mathrm{flow}} = \ln(1 + \frac{\sum A_{\mathrm{out}}}{\sum A_{\mathrm{in}}+\epsilon})$",
     0.025, 0.220),
    (r"2. Harmonic Encoder $\Phi_{\text{time}}$",
     r"$w(\Delta t) = \sum \pi_b e^{-\lambda_b \Delta t} \cos(\omega_b \Delta t) \quad (b=1..3)$",
     0.260, 0.230),
    (r"3. Edge-Trust Floor $\hat{g}_{ij}$",
     r"$\hat{g}_{ij} \in [0.10, 1.0], \; \delta_{\text{floor}} = 0.10$",
     0.505, 0.220),
    (r"4. Adaptive Gating & Head $\mathbf{h}_u^*$",
     r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}, \; \tau^*=0.18$",
     0.740, 0.240)
]

for m_title, m_eq, mx, mw in math_blocks:
    ax.add_patch(patches.FancyBboxPatch((mx, ms_y + 0.012), mw, 0.120,
                                        boxstyle='round,pad=0.002,rounding_size=0.003',
                                        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(mx + mw/2, ms_y + 0.098, m_title, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#1e293b')
    ax.text(mx + mw/2, ms_y + 0.046, m_eq, ha='center', va='center', fontsize=6.0, color='#0f172a')

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig3_1_tensor_flow")


# ==============================================================================
# 3. FIG 8.2: UNIFIED UML SEQUENCE LIFELINE DIAGRAM (9.4" x 4.30")
# ==============================================================================
print("Generating Fig 8.2: Real-Time UML Sequence Lifeline with Latency Timestamps...")
from redesign_fig8_2_sequence_lifeline import generate_figure_8_2
fig = generate_figure_8_2()
save_fig(fig, "fig8_2_uml_sequence_lifeline")

print("All 3 New / Upgraded Action Plan Diagrams generated successfully!")
