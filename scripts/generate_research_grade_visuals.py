"""
generate_research_grade_visuals.py — Research-Grade Publication Vector Visual Generator.

Upgrades the 3 core diagrams into publication-grade vector graphics for IEEE TIFS:
1. Figure 6: C-STGB End-to-End System Architecture Blueprint (4 Tiers with modular sub-cards)
2. Figure 12: Deterministic 3-Tier Conformal Risk Control (CRC) Operational Triage Flowchart
3. Figure 15: Canonical 12-D Spatio-Temporal Feature Projection Space for Zero-Shot Cross-Network Transfer
"""

import sys
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# IEEE Publication Typography & Rendering Settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

BASE_DIR = Path(__file__).resolve().parent.parent

ieee_fig_dir = BASE_DIR / "papers" / "IEEE_Research_Paper" / "figures"
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"

OUT_DIRS = [data_fig_dir, ieee_fig_dir, thesis_fig_dir]
for d in OUT_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_fig_all(fig, stem_name):
    for d in OUT_DIRS:
        pdf_p = d / f"{stem_name}.pdf"
        png_p = d / f"{stem_name}.png"
        fig.savefig(pdf_p, bbox_inches="tight", pad_inches=0.04)
        fig.savefig(png_p, dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"   ✓ Generated research-grade visual: {stem_name}.pdf / .png")


# ==============================================================================
# 1. FIGURE 6: RESEARCH-GRADE C-STGB SYSTEM ARCHITECTURE (7.16" x 2.45")
# ==============================================================================
print("[1/3] Generating High-Grade Figure 6: C-STGB System Architecture...")
fig, ax = plt.subplots(figsize=(7.16, 2.45))
ax.axis('off')
ax.set_xlim([-0.015, 1.015])
ax.set_ylim([-0.02, 1.02])

# Background Canvas Card
canvas_card = patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 0.98,
    boxstyle="round,pad=0.015",
    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8
)
ax.add_patch(canvas_card)

# Header Title Banner
title_banner = patches.FancyBboxPatch(
    (0.02, 0.88), 0.96, 0.08,
    boxstyle="round,pad=0.008",
    facecolor="#0f172a", edgecolor="#0f172a", linewidth=0.5
)
ax.add_patch(title_banner)
ax.text(0.50, 0.92, "C-STGB: Conformal Spatio-Temporal GraphBoost End-to-End Architecture",
        ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")

# 4 Architectural Tier Cards
tiers_data = [
    {
        "line1": "TIER 1: STREAMING INGEST",
        "line2": "DuckDB Invariants & Hawkes",
        "badge_bg": "#1e40af",
        "card_bg": "#eff6ff",
        "card_border": "#93c5fd",
        "x": 0.015, "w": 0.228,
        "items": [
            ("• DuckDB / Arrow Engine", "O(1) zero-copy micro-batch"),
            ("• Dynamic Top-K Capping", r"$K \leq 15$ neighbor ceiling"),
            ("• 12-D Invariants", r"$\mathbf{z}_{\mathrm{inv}} \in \mathbf{R}^{12}$ flow basis"),
            ("• Hawkes Intensity", r"$\lambda_u(t)$ burst acceleration"),
        ],
        "tech_tag": "Latency: 0.45 ms | DuckDB"
    },
    {
        "line1": "TIER 2: GNN BACKBONE",
        "line2": "Tri-Band & Camouflage Filter",
        "badge_bg": "#15803d",
        "card_bg": "#f0fdf4",
        "card_border": "#86efac",
        "x": 0.262, "w": 0.232,
        "items": [
            ("• Tri-Band Harmonic Attn.", r"$\Phi_{\mathrm{time}}(\Delta t)$ harmonic bank"),
            ("• Edge-Trust Gating", r"$g_{ij} \geq 0.10$ (65.9% pruned)"),
            ("• Typology GraphSMOTE", r"$\mathcal{C}_k$ latent interpolation"),
            ("• Hard-Negative Mining", r"Suppresses merchant hubs"),
        ],
        "tech_tag": "Continuous-Time HGT"
    },
    {
        "line1": "TIER 3: FUSION & RISK",
        "line2": "Evidence-Adaptive Bayes",
        "badge_bg": "#c2410c",
        "card_bg": "#fff7ed",
        "card_border": "#fdba74",
        "x": 0.513, "w": 0.232,
        "items": [
            ("• Evidence-Adaptive Gate", r"$\alpha_u \in [0, 1]$ cold-start blend"),
            ("• Cold-Start Embed Fused", r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$"),
            ("• Asym. Focal Tversky Loss", r"$\mathcal{L}_{\mathrm{task}}$ cost-sensitive"),
            ("• Optimal Bayes Policy", r"$\tau^*$ threshold tuning"),
        ],
        "tech_tag": "Cold-Start + Bayes Risk"
    },
    {
        "line1": "TIER 4: CONFORMAL SWARM",
        "line2": "CRC Triage & FinCEN SAR",
        "badge_bg": "#6b21a8",
        "card_bg": "#faf5ff",
        "card_border": "#d8b4fe",
        "x": 0.764, "w": 0.222,
        "items": [
            ("• Class-Conditional CRC", r"$1-\alpha \geq 99.0\%$ coverage"),
            ("• 3-Tier Selective Triage", r"$\Gamma(X) \subseteq \{0, 1\}$"),
            ("• Multi-Agent Swarm", "AST compiler invariant"),
            ("• FinCEN Form 111 XML", "SHA-256 Merkle audit seal"),
        ],
        "tech_tag": "Fed SR 11-7 Verifiable"
    }
]

y_bottom = 0.035
card_h = 0.815

for t in tiers_data:
    x0 = t["x"]
    w0 = t["w"]
    
    # Outer card
    card = patches.FancyBboxPatch(
        (x0, y_bottom), w0, card_h,
        boxstyle="round,pad=0.012",
        facecolor=t["card_bg"], edgecolor=t["card_border"], linewidth=1.1
    )
    ax.add_patch(card)
    
    # Card Header Pill
    header_pill = patches.FancyBboxPatch(
        (x0 + 0.006, y_bottom + card_h - 0.170), w0 - 0.012, 0.155,
        boxstyle="round,pad=0.006",
        facecolor=t["badge_bg"], edgecolor=t["badge_bg"], linewidth=0.5
    )
    ax.add_patch(header_pill)
    
    # Header text
    ax.text(x0 + w0/2, y_bottom + card_h - 0.050, t["line1"],
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")
    ax.text(x0 + w0/2, y_bottom + card_h - 0.115, t["line2"],
            ha="center", va="center", fontsize=5.8, color="#e2e8f0", style="italic")
    
    # Items
    y_text = y_bottom + card_h - 0.220
    for it_h, it_d in t["items"]:
        ax.text(x0 + 0.008, y_text + 0.012, it_h, ha="left", va="center", fontsize=6.2, fontweight="bold", color="#0f172a")
        ax.text(x0 + 0.016, y_text - 0.025, it_d, ha="left", va="center", fontsize=5.6, color="#475569")
        y_text -= 0.110
        
    # Bottom Tech Tag Pill
    tag_pill = patches.FancyBboxPatch(
        (x0 + 0.008, y_bottom + 0.020), w0 - 0.016, 0.065,
        boxstyle="round,pad=0.004",
        facecolor="#ffffff", edgecolor=t["card_border"], linewidth=0.75
    )
    ax.add_patch(tag_pill)
    ax.text(x0 + w0/2, y_bottom + 0.052, t["tech_tag"],
            ha="center", va="center", fontsize=5.8, fontweight="bold", color=t["badge_bg"])

# Connective Flow Arrows between Tiers with Tensor Signatures
tensor_arrows = [
    (0.243, 0.262, r"$\mathbf{z}_{\mathrm{inv}}, \mathcal{G}$"),
    (0.494, 0.513, r"$\mathbf{h}_u^{(L)}$"),
    (0.745, 0.764, r"$\hat{p}_u, \mathbf{h}_u^*$")
]

for x_from, x_to, label in tensor_arrows:
    ax.annotate(
        "", xy=(x_to, 0.44), xytext=(x_from, 0.44),
        arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.30", lw=1.5, color="#0f172a")
    )
    ax.text((x_from + x_to)/2, 0.50, label, ha="center", va="bottom", fontsize=6.2, fontweight="bold", color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.10", facecolor="#ffffff", edgecolor="#cbd5e1", lw=0.6))

plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
save_fig_all(fig, "fig6_system_architecture")

for d in OUT_DIRS:
    shutil.copyfile(d / "fig6_system_architecture.pdf", d / "pipeline_cstgb.pdf")
    shutil.copyfile(d / "fig6_system_architecture.pdf", d / "arch_triband.pdf")


# ==============================================================================
# 2. FIGURE 15: RESEARCH-GRADE 12-D CANONICAL INVARIANTS FOR TRANSFER (7.16" x 2.45")
# ==============================================================================
print("[2/3] Generating High-Grade Figure 15: Canonical 12-D Invariant Projection...")
fig, ax = plt.subplots(figsize=(7.16, 2.45))
ax.axis('off')
ax.set_xlim([-0.015, 1.015])
ax.set_ylim([-0.02, 1.02])

# Outer canvas
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 0.98,
    boxstyle="round,pad=0.015",
    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8
))

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.02, 0.88), 0.96, 0.08,
    boxstyle="round,pad=0.008",
    facecolor="#064e3b", edgecolor="#064e3b", linewidth=0.5
))
ax.text(0.50, 0.92, "Canonical 12-D Spatio-Temporal Feature Projection for Zero-Shot Cross-Network Transfer",
        ha="center", va="center", fontsize=8.8, fontweight="bold", color="#ffffff")

# Panel 1: Raw Heterogeneous Financial Schemas (Left)
p1 = patches.FancyBboxPatch(
    (0.015, 0.035), 0.220, 0.815,
    boxstyle="round,pad=0.012",
    facecolor="#f1f5f9", edgecolor="#94a3b8", linewidth=1.1
)
ax.add_patch(p1)

ax.add_patch(patches.FancyBboxPatch(
    (0.022, 0.690), 0.206, 0.145,
    boxstyle="round,pad=0.006",
    facecolor="#334155", edgecolor="#334155", linewidth=0.5
))
ax.text(0.125, 0.785, "Raw Heterogeneous", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
ax.text(0.125, 0.725, "Financial Schemas", ha="center", va="center", fontsize=6.8, color="#cbd5e1")

schemas = [
    ("Bitcoin UTXO (DAG)", "166-D Raw Attributes", "#b45309", "#fef3c7"),
    ("Ethereum EVM (Calls)", "14-D Smart Contracts", "#4338ca", "#e0e7ff"),
    ("PaySim (Mobile Money)", "9-D High-Velocity Tree", "#047857", "#d1fae5"),
    ("SAML-D (Multi-Bank)", "12-D Wire Mesh", "#b91c1c", "#fee2e2"),
]
y_sch = 0.585
for name, desc, c_bd, c_bg in schemas:
    sch_box = patches.FancyBboxPatch(
        (0.022, y_sch), 0.206, 0.095,
        boxstyle="round,pad=0.005",
        facecolor=c_bg, edgecolor=c_bd, linewidth=0.75
    )
    ax.add_patch(sch_box)
    ax.text(0.030, y_sch + 0.062, name, ha="left", va="center", fontsize=6.0, fontweight="bold", color=c_bd)
    ax.text(0.030, y_sch + 0.025, desc, ha="left", va="center", fontsize=5.3, color="#475569")
    y_sch -= 0.118

# Panel 2: 12-D Canonical Invariant Projection Space (Center)
p2 = patches.FancyBboxPatch(
    (0.260, 0.035), 0.485, 0.815,
    boxstyle="round,pad=0.012",
    facecolor="#ecfdf5", edgecolor="#6ee7b7", linewidth=1.1
)
ax.add_patch(p2)

ax.add_patch(patches.FancyBboxPatch(
    (0.268, 0.690), 0.469, 0.145,
    boxstyle="round,pad=0.006",
    facecolor="#047857", edgecolor="#047857", linewidth=0.5
))
ax.text(0.502, 0.785, r"12-D Canonical Invariant Projection Space ($\mathbf{z}_{\mathrm{inv}} \in \mathbf{R}^{12}$)",
        ha="center", va="center", fontsize=7.6, fontweight="bold", color="#ffffff")
ax.text(0.502, 0.725, "Physical Mass-Conservation & Causal Graph Topological Invariants",
        ha="center", va="center", fontsize=6.2, color="#a7f3d0")

invariants_list = [
    (r"1. Flow Conservation: $\Phi_{\mathrm{flow}}(u, t) = \Sigma A_{\mathrm{out}} / (\Sigma A_{\mathrm{in}} + \epsilon)$",
     r"$\rightarrow$ Layering Mule Flow Balance (~1.0 unity ratio)"),
    (r"2. Degree Asymmetry: $\Psi_{\mathrm{asym}}(u, t) = |d_{\mathrm{in}} - d_{\mathrm{out}}| / (d_{\mathrm{in}} + d_{\mathrm{out}} + \epsilon)$",
     r"$\rightarrow$ Conduit vs High-Degree Structural In/Out Skew"),
    (r"3. Hawkes Arrival: $\lambda_u(t) = \mu_0 + \Sigma \alpha e^{-\beta (t - t_i)}$",
     r"$\rightarrow$ Continuous-Time Micro-Burst Velocity Acceleration"),
    (r"4-5. PPR Taint: $(\mathbf{s}_{\mathrm{fwd}}, \mathbf{s}_{\mathrm{bwd}}) = (1-\alpha_{\mathrm{ppr}})(\mathbf{I} - \alpha_{\mathrm{ppr}}\mathbf{P})^{-1}\mathbf{s}_{\mathrm{seed}}$",
     r"$\rightarrow$ Causal Illicit Taint Network Proximity (Bi-Directional)"),
    (r"6-12. 5-Moment & Jitter: $(\mu_A, \sigma_A^2, \gamma_A, \kappa_A, \nu_{\mathrm{io}}, \sigma_{\Delta t}, v_A)$",
     r"$\rightarrow$ Higher-Order Ego Distribution Statistics & Temporal Dispersion"),
]

y_inv = 0.575
for line1_txt, line2_txt in invariants_list:
    inv_box = patches.FancyBboxPatch(
        (0.268, y_inv), 0.469, 0.098,
        boxstyle="round,pad=0.005",
        facecolor="#ffffff", edgecolor="#a7f3d0", linewidth=0.6
    )
    ax.add_patch(inv_box)
    ax.text(0.276, y_inv + 0.065, line1_txt, ha="left", va="center", fontsize=5.8, color="#064e3b")
    ax.text(0.276, y_inv + 0.022, line2_txt, ha="left", va="center", fontsize=5.2, style="italic", color="#047857")
    y_inv -= 0.112

# Panel 3: Frozen GNN Backbone & Target Transfer (Right)
p3 = patches.FancyBboxPatch(
    (0.768, 0.035), 0.218, 0.815,
    boxstyle="round,pad=0.012",
    facecolor="#eff6ff", edgecolor="#93c5fd", linewidth=1.1
)
ax.add_patch(p3)

ax.add_patch(patches.FancyBboxPatch(
    (0.775, 0.690), 0.204, 0.145,
    boxstyle="round,pad=0.006",
    facecolor="#1e40af", edgecolor="#1e40af", linewidth=0.5
))
ax.text(0.877, 0.785, "Frozen GNN Backbone", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
ax.text(0.877, 0.725, "& Target Transfer", ha="center", va="center", fontsize=6.8, color="#bfdbfe")

transfer_points = [
    ("100% Frozen Weights", r"Zero target fine-tuning ($\eta=0$)", "#1e3a8a"),
    ("Universal Alignment", "Cross-rail canonical basis", "#0284c7"),
    ("Target Transfer F1", "82.40% Macro F1 Score", "#059669"),
    ("Invariant Advantage", "+28.20 pp vs Raw Projection", "#b91c1c")
]

y_tr = 0.585
for h_txt, b_txt, c_clr in transfer_points:
    tr_box = patches.FancyBboxPatch(
        (0.775, y_tr), 0.204, 0.095,
        boxstyle="round,pad=0.005",
        facecolor="#ffffff", edgecolor="#bfdbfe", linewidth=0.75
    )
    ax.add_patch(tr_box)
    ax.text(0.783, y_tr + 0.062, h_txt, ha="left", va="center", fontsize=6.0, fontweight="bold", color=c_clr)
    ax.text(0.783, y_tr + 0.025, b_txt, ha="left", va="center", fontsize=5.3, color="#475569")
    y_tr -= 0.118

# Connection arrows
ax.annotate("", xy=(0.260, 0.44), xytext=(0.235, 0.44),
            arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.30", lw=1.5, color="#0f172a"))
ax.annotate("", xy=(0.768, 0.44), xytext=(0.745, 0.44),
            arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.30", lw=1.5, color="#0f172a"))

plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
save_fig_all(fig, "fig_canonical_invariants")


# ==============================================================================
# 3. FIGURE 12: RESEARCH-GRADE 3-TIER CONFORMAL OPERATIONAL TRIAGE (7.16" x 2.45")
# ==============================================================================
print("[3/3] Generating High-Grade Figure 12: Conformal Triage Operational Flowchart...")
fig, ax = plt.subplots(figsize=(7.16, 2.45))
ax.axis('off')
ax.set_xlim([-0.015, 1.015])
ax.set_ylim([-0.02, 1.02])

# Background Canvas Card
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 0.98,
    boxstyle="round,pad=0.015",
    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8
))

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.02, 0.88), 0.96, 0.08,
    boxstyle="round,pad=0.008",
    facecolor="#0f172a", edgecolor="#0f172a", linewidth=0.5
))
ax.text(0.50, 0.92, "Deterministic 3-Tier Conformal Risk Control (CRC) Operational Triage Pipeline",
        ha="center", va="center", fontsize=8.8, fontweight="bold", color="#ffffff")

# Box 1: Ingest Stream
b1 = patches.FancyBboxPatch(
    (0.015, 0.08), 0.165, 0.72,
    boxstyle="round,pad=0.012",
    facecolor="#f0f9ff", edgecolor="#7dd3fc", linewidth=1.1
)
ax.add_patch(b1)
ax.add_patch(patches.FancyBboxPatch(
    (0.022, 0.64), 0.151, 0.14,
    boxstyle="round,pad=0.006",
    facecolor="#0284c7", edgecolor="#0284c7", linewidth=0.5
))
ax.text(0.097, 0.73, "Incoming Stream", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
ax.text(0.097, 0.67, r"$N = 10,000$ tx", ha="center", va="center", fontsize=6.5, color="#e0f2fe")

ax.text(0.097, 0.48, "• Live Event Buffer\n• High-Throughput\n• Zero-Copy Arrow\n• Dynamic Scoring",
        ha="center", va="center", fontsize=6.2, color="#0f172a", linespacing=1.4)

# Box 2: C-STGB Neural Scoring Engine
b2 = patches.FancyBboxPatch(
    (0.205, 0.08), 0.180, 0.72,
    boxstyle="round,pad=0.012",
    facecolor="#f5f3ff", edgecolor="#c4b5fd", linewidth=1.1
)
ax.add_patch(b2)
ax.add_patch(patches.FancyBboxPatch(
    (0.212, 0.64), 0.166, 0.14,
    boxstyle="round,pad=0.006",
    facecolor="#7c3aed", edgecolor="#7c3aed", linewidth=0.5
))
ax.text(0.295, 0.73, "C-STGB Backbone", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
ax.text(0.295, 0.67, r"Non-Conformity $s_i$", ha="center", va="center", fontsize=6.5, color="#ede9fe")

ax.text(0.295, 0.48, r"• $s_i^{(y)} = 1 - \hat{p}_i(y)$" + "\n" +
                     r"• Dual Non-Conf. Scores" + "\n" +
                     r"• Bayes Policy $\tau^*$" + "\n" +
                     "• Streaming 0.45 ms",
        ha="center", va="center", fontsize=6.2, color="#0f172a", linespacing=1.4)

# Box 3: Class-Conditional Conformal Calibration Engine
b3 = patches.FancyBboxPatch(
    (0.410, 0.05), 0.235, 0.78,
    boxstyle="round,pad=0.012",
    facecolor="#fffbeb", edgecolor="#fcd34d", linewidth=1.1
)
ax.add_patch(b3)
ax.add_patch(patches.FancyBboxPatch(
    (0.418, 0.67), 0.219, 0.14,
    boxstyle="round,pad=0.006",
    facecolor="#d97706", edgecolor="#d97706", linewidth=0.5
))
ax.text(0.527, 0.76, "Class-Conditional CRC", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
ax.text(0.527, 0.70, r"$\Gamma(X) = \{y : s_i^{(y)} \leq \hat{q}^{(y)}\}$", ha="center", va="center", fontsize=6.3, color="#fef3c7")

ax.text(0.527, 0.50, "• Dual Quantiles:\n" +
                     r"  $\hat{q}^{(0)}$ (Benign), $\hat{q}^{(1)}$ (Illicit)" + "\n" +
                     "• Coverage Guarantee:\n" +
                     r"  $P(Y \in \Gamma(X) \mid y) \geq 99\%$" + "\n" +
                     "• Drift Robustness:\n" +
                     r"  DKW Bound $+ \sqrt{|\mathcal{D}_{\mathrm{cal}}|}$",
        ha="center", va="center", fontsize=5.8, color="#0f172a", linespacing=1.35)

# Output Channels (3 Tiers on the right)
tier_outputs = [
    {
        "left_h": "Tier 1: Instant Auto-Block",
        "right_h": r"$\Gamma(X) = \{1\}$",
        "vol": r"$\approx 55$ / 10k tx ($0.55\%$)",
        "action": r"Precision $>99.4\%$ | Freeze & SAR Draft",
        "bg_c": "#fef2f2", "bd_c": "#ef4444", "hdr_bg": "#b91c1c", "y": 0.58, "h": 0.25
    },
    {
        "left_h": "Tier 2: Manual Review Queue",
        "right_h": r"$\Gamma(X) = \{0, 1\}$",
        "vol": r"$\approx 5$ / 10k tx ($0.05\%$ Ambiguous)",
        "action": r"Dispatches Multi-Agent Forensic Dossier",
        "bg_c": "#fff7ed", "bd_c": "#f97316", "hdr_bg": "#c2410c", "y": 0.31, "h": 0.25
    },
    {
        "left_h": "Tier 3: Straight-Through Auto-Clear",
        "right_h": r"$\Gamma(X) = \{0\}$",
        "vol": r"$\approx 9,940$ / 10k tx ($99.40\%$)",
        "action": r"Benign Guarantee $>99.9\%$ | Instant STP",
        "bg_c": "#f0fdf4", "bd_c": "#22c55e", "hdr_bg": "#15803d", "y": 0.04, "h": 0.25
    }
]

for t in tier_outputs:
    y0 = t["y"]
    h0 = t["h"]
    box = patches.FancyBboxPatch(
        (0.665, y0), 0.320, h0,
        boxstyle="round,pad=0.008",
        facecolor=t["bg_c"], edgecolor=t["bd_c"], linewidth=1.0
    )
    ax.add_patch(box)
    
    # Header strip inside tier
    hdr = patches.FancyBboxPatch(
        (0.670, y0 + h0 - 0.080), 0.310, 0.072,
        boxstyle="round,pad=0.004",
        facecolor=t["hdr_bg"], edgecolor=t["hdr_bg"], linewidth=0.5
    )
    ax.add_patch(hdr)
    ax.text(0.678, y0 + h0 - 0.044, t["left_h"], ha="left", va="center", fontsize=6.1, fontweight="bold", color="#ffffff")
    ax.text(0.970, y0 + h0 - 0.044, t["right_h"], ha="right", va="center", fontsize=6.1, fontweight="bold", color="#fef08a")
    
    # Details
    ax.text(0.678, y0 + 0.108, r"• Volume: " + t["vol"], ha="left", va="center", fontsize=5.8, color="#1e293b")
    ax.text(0.678, y0 + 0.045, r"• Action: " + t["action"], ha="left", va="center", fontsize=5.4, fontweight="bold", color=t["hdr_bg"])

# Flow arrows
ax.annotate("", xy=(0.205, 0.44), xytext=(0.180, 0.44),
            arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.30", lw=1.5, color="#0f172a"))
ax.annotate("", xy=(0.410, 0.44), xytext=(0.385, 0.44),
            arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.30", lw=1.5, color="#0f172a"))

# Branching arrows to 3 tiers
ax.annotate("", xy=(0.665, 0.70), xytext=(0.645, 0.48),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", lw=1.4, color="#b91c1c"))
ax.annotate("", xy=(0.665, 0.435), xytext=(0.645, 0.44),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", lw=1.4, color="#c2410c"))
ax.annotate("", xy=(0.665, 0.165), xytext=(0.645, 0.40),
            arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.28", lw=1.4, color="#15803d"))

# Bottom Callout Summary Pill
summary_pill = patches.FancyBboxPatch(
    (0.015, 0.015), 0.630, 0.055,
    boxstyle="round,pad=0.005",
    facecolor="#052e16", edgecolor="#15803d", linewidth=0.75
)
ax.add_patch(summary_pill)
ax.text(0.330, 0.042, r">99.4% Net Compliance Workload Reduction (Human Review Focused Exclusively on the 0.05% Ambiguous Queue)",
        ha="center", va="center", fontsize=5.8, fontweight="bold", color="#4ade80")

plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
save_fig_all(fig, "fig_conformal_triage_flowchart")

print("\n" + "=" * 78)
print("🎉 ALL 3 HIGH-GRADE RESEARCH FIGURES SUCCESSFULLY GENERATED!")
print("=" * 78)
