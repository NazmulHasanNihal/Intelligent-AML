"""
scripts/redesign_fig3_1_neural_tensor_flow.py
Completely redesigns Figure 3.1 for Chapter 3 (System Architecture):
End-to-End Architectural Dataflow of C-STGB v2.

Radical Redesign Highlights:
- Completely removes the repetitive 5-column text-table card format.
- Implements an authentic 2-Tier Neuro-Symbolic System Architecture Schematic:
  * TIER 1 (Top): Spatio-Temporal Representation & Graph Denoising
    - Module 1: Continuous Multi-Scale Temporal Graph Encoder (Harmonic Waves + Hawkes Point Process)
    - Module 2: Context-Aware Adaptive Edge-Trust Gating (Chaff Pruner & Attention Valve)
    - Module 3: Typology-Clustered Latent GraphSMOTE (Offline Typology Manifold Synthesis)
  * INTER-TIER BUS: Tensor Flow Conduit (Embeddings h_u, Invariants z_inv, Edge Gates g_uv)
  * TIER 2 (Bottom): Adaptive Evidence Fusion & Conformal Risk Governance
    - Module 4: Evidence-Adaptive Graph-Tabular Fusion (Cold-Start Inductive Switch alpha_u)
    - Module 5: Cost-Sensitive Bayesian Risk Head (15:1 Asymmetric Loss, Optimal Cutoff tau*=0.18)
    - Module 6: Class-Conditional Conformal Risk Control (CRC Arbiter & 3-Tier Operational Dispatch)
- Every module features authentic embedded visual mini-diagrams:
  * Sine wave tracks for tau_1, tau_2, tau_3
  * Hawkes self-exciting spike train
  * Edge-trust valve separating chaff vs wash conduits
  * Manifold clusters & synthetic interpolation
  * Dynamic balance slider for cold-start vs dense graph
  * Calibrated Bayes threshold curve
  * Conformal 3-way operational triage dispatch
- 100% collision-free, clipping-free, publication-grade typography.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines

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
    'axes.labelsize': 8.8,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "reports" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_to_all(fig, stem):
    for d in TARGET_DIRS:
        pdf_path = d / f"{stem}.pdf"
        png_path = d / f"{stem}.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f" [OK] Generated & Saved: {stem}.pdf & .png across all target directories")


def generate_new_fig3_1():
    # Canvas dimensions: 10.2 x 6.8 inches (generous, elegant, high information density)
    fig, ax = plt.subplots(figsize=(10.2, 6.8))
    ax.axis('off')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # -------------------------------------------------------------------------
    # MASTER SYSTEM HEADER
    # -------------------------------------------------------------------------
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, 0.935), 0.970, 0.055,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#0f172a", edgecolor="#1e293b", lw=1.2
    ))
    ax.text(0.50, 0.968, "C-STGB v2: End-to-End Architectural Dataflow & Neuro-Symbolic Tensor Pipeline",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.948, "Six Interconnected Modules: Continuous Time -> Edge Denoising -> Latent SMOTE -> Evidence Fusion -> Bayes Head -> Conformal CRC",
            ha="center", va="center", fontsize=6.8, color="#94a3b8", style="italic")

    # =========================================================================
    # TIER 1: SPATIO-TEMPORAL REPRESENTATION & DENOISING (y: 0.52 to 0.92)
    # =========================================================================
    
    # Tier 1 Container Background
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, 0.520), 0.970, 0.400,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.2, linestyle="--"
    ))
    ax.text(0.030, 0.905, "TIER 1: SPATIO-TEMPORAL NEURAL ENCODING & ADVERSARIAL DENOISING",
            ha="left", va="center", fontsize=7.2, fontweight="bold", color="#334155")

    # -------------------------------------------------------------------------
    # MODULE 1: Continuous Multi-Scale Temporal Encoder (x: 0.025 to 0.325)
    # -------------------------------------------------------------------------
    m1_x, m1_y, m1_w, m1_h = 0.025, 0.535, 0.300, 0.355
    ax.add_patch(patches.FancyBboxPatch(
        (m1_x, m1_y), m1_w, m1_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#2563eb", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m1_x + 0.008, m1_y + m1_h - 0.038), m1_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#2563eb", edgecolor="#1d4ed8"
    ))
    ax.text(m1_x + m1_w/2, m1_y + m1_h - 0.022, "Module 1: Continuous Temporal Encoder",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Mini Visual: 3 Harmonic Waveform Tracks
    w_box_y = m1_y + 0.175
    ax.add_patch(patches.Rectangle((m1_x + 0.012, w_box_y), m1_w - 0.024, 0.130, fc="#f0f9ff", ec="#bae6fd", lw=0.8))
    ax.text(m1_x + 0.020, w_box_y + 0.115, "Tri-Band Harmonic Position Pos(t):", fontsize=5.8, fontweight="bold", color="#0369a1")
    
    t_pts = np.linspace(0, 1, 100)
    x_wave = m1_x + 0.025 + t_pts * (m1_w - 0.050)
    # Band 1 (Burst - high frequency)
    y_b1 = w_box_y + 0.085 + 0.014 * np.sin(2 * np.pi * 5 * t_pts)
    ax.plot(x_wave, y_b1, color="#2563eb", lw=1.2)
    ax.text(m1_x + m1_w - 0.018, w_box_y + 0.085, r"$\tau_1=2.4\mathrm{h}$", ha="right", va="center", fontsize=5.0, color="#1e40af", fontweight="bold")
    
    # Band 2 (Diurnal - 24h)
    y_b2 = w_box_y + 0.052 + 0.014 * np.sin(2 * np.pi * 1.5 * t_pts)
    ax.plot(x_wave, y_b2, color="#0284c7", lw=1.2)
    ax.text(m1_x + m1_w - 0.018, w_box_y + 0.052, r"$\tau_2=24\mathrm{h}$", ha="right", va="center", fontsize=5.0, color="#0369a1", fontweight="bold")

    # Band 3 (Hibernation - 168h slow wave)
    y_b3 = w_box_y + 0.020 + 0.012 * np.sin(2 * np.pi * 0.4 * t_pts)
    ax.plot(x_wave, y_b3, color="#0f766e", lw=1.2)
    ax.text(m1_x + m1_w - 0.018, w_box_y + 0.020, r"$\tau_3=168\mathrm{h}$", ha="right", va="center", fontsize=5.0, color="#0f766e", fontweight="bold")

    # Mini Visual: Hawkes Point Process
    h_box_y = m1_y + 0.045
    ax.add_patch(patches.Rectangle((m1_x + 0.012, h_box_y), m1_w - 0.024, 0.115, fc="#fff7ed", ec="#fed7aa", lw=0.8))
    ax.text(m1_x + 0.020, h_box_y + 0.098, r"Self-Exciting Hawkes Rate $\lambda_u(t)$:", fontsize=5.8, fontweight="bold", color="#c2410c")
    t_hwk = np.linspace(0, 1, 100)
    x_hwk = m1_x + 0.025 + t_hwk * (m1_w - 0.050)
    y_hwk = h_box_y + 0.022 + 0.065 * np.exp(-14 * (t_hwk - 0.3)**2) + 0.035 * np.exp(-22 * (t_hwk - 0.65)**2)
    ax.plot(x_hwk, y_hwk, color="#ea580c", lw=1.4)
    ax.text(m1_x + m1_w/2, h_box_y + 0.016, r"Micro-Burst Smurfing Detection ($\lambda_u > 12.0$)", ha="center", va="center", fontsize=5.2, color="#9a3412")

    # Tensor Output
    ax.text(m1_x + m1_w/2, m1_y + 0.018, r"Output Tensor: $\mathbf{h}_u^{(0)} \in \mathbb{R}^d$ (Temporal Seed)",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#1e40af")

    # Connecting Arrow M1 -> M2
    ax.annotate("", xy=(0.355, 0.710), xytext=(0.325, 0.710),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#2563eb"))

    # -------------------------------------------------------------------------
    # MODULE 2: Edge-Trust Filter & Spatio-Temporal Attention (x: 0.355 to 0.655)
    # -------------------------------------------------------------------------
    m2_x, m2_y, m2_w, m2_h = 0.355, 0.535, 0.300, 0.355
    ax.add_patch(patches.FancyBboxPatch(
        (m2_x, m2_y), m2_w, m2_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#7c3aed", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m2_x + 0.008, m2_y + m2_h - 0.038), m2_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#7c3aed", edgecolor="#6d28d9"
    ))
    ax.text(m2_x + m2_w/2, m2_y + m2_h - 0.022, "Module 2: Edge-Trust Filter & GNN",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Mini Visual: Edge-Trust Gating Valve & Camouflage Chaff Pruning
    v_box_y = m2_y + 0.170
    ax.add_patch(patches.Rectangle((m2_x + 0.012, v_box_y), m2_w - 0.024, 0.135, fc="#faf5ff", ec="#e9d5ff", lw=0.8))
    ax.text(m2_x + 0.020, v_box_y + 0.120, "Learnable Edge-Trust Gating Mechanism:", fontsize=5.8, fontweight="bold", color="#6b21a8")

    # Graph Nodes & Valve
    node_u = (m2_x + 0.050, v_box_y + 0.065)
    node_v = (m2_x + 0.250, v_box_y + 0.085)
    node_chaff = (m2_x + 0.245, v_box_y + 0.025)
    
    # Legitimate wash edge (Green)
    ax.plot([node_u[0], node_v[0]], [node_u[1], node_v[1]], color="#16a34a", lw=2.2)
    ax.text((node_u[0]+node_v[0])/2, (node_u[1]+node_v[1])/2 + 0.020, r"$\hat{g}_{vu} \geq 0.92$ (Retained)",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#15803d")
    
    # Spurious camouflage chaff edge (Dashed red with cross)
    ax.plot([node_u[0], node_chaff[0]], [node_u[1], node_chaff[1]], color="#f87171", lw=1.2, ls="--")
    ax.text((node_u[0]+node_chaff[0])/2, (node_u[1]+node_chaff[1])/2 - 0.015, "× Chaff Pruned (-65.9%)",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#dc2626")

    # Draw nodes
    ax.scatter([node_u[0]], [node_u[1]], s=160, color="#2563eb", edgecolors="#ffffff", lw=1.2, zorder=4)
    ax.text(node_u[0], node_u[1], "u", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#ffffff", zorder=5)
    
    ax.scatter([node_v[0]], [node_v[1]], s=140, color="#16a34a", edgecolors="#ffffff", lw=1.2, zorder=4)
    ax.text(node_v[0], node_v[1], "v", ha="center", va="center", fontsize=6.0, fontweight="bold", color="#ffffff", zorder=5)

    ax.scatter([node_chaff[0]], [node_chaff[1]], s=130, color="#94a3b8", edgecolors="#ffffff", lw=1.0, zorder=4)
    ax.text(node_chaff[0], node_chaff[1], "c", ha="center", va="center", fontsize=5.6, color="#ffffff", zorder=5)

    # GNN Message Passing Formula Box
    m_box_y = m2_y + 0.045
    ax.add_patch(patches.Rectangle((m2_x + 0.012, m_box_y), m2_w - 0.024, 0.115, fc="#f3e8ff", ec="#d8b4fe", lw=0.8))
    ax.text(m2_x + 0.020, m_box_y + 0.098, "Spatio-Temporal Attention Aggregation:", fontsize=5.8, fontweight="bold", color="#581c87")
    ax.text(m2_x + m2_w/2, m_box_y + 0.068, r"$\tilde{\mathbf{h}}_u = \sum_{v \in \mathcal{N}_u} \alpha_{vu} \mathbf{W}_v \mathbf{h}_v^{(l-1)} \hat{g}_{vu}$",
            ha="center", va="center", fontsize=5.8, fontweight="bold", color="#6b21a8")
    ax.text(m2_x + m2_w/2, m_box_y + 0.032, r"Dirichlet Energy Preserved: $\mathcal{E}(\mathbf{H}) > 0.75$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#059669")
    ax.text(m2_x + m2_w/2, m_box_y + 0.012, r"Threshold Floor: $\delta_{\mathrm{floor}} = 0.10$",
            ha="center", va="center", fontsize=5.0, color="#475569")

    # Tensor Output
    ax.text(m2_x + m2_w/2, m2_y + 0.018, r"Structural Embedding: $\mathbf{h}_u^{(L)} \in \mathbb{R}^d$",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#6b21a8")

    # -------------------------------------------------------------------------
    # MODULE 3: Typology-Clustered Latent GraphSMOTE (x: 0.685 to 0.965)
    # -------------------------------------------------------------------------
    m3_x, m3_y, m3_w, m3_h = 0.685, 0.535, 0.280, 0.355
    ax.add_patch(patches.FancyBboxPatch(
        (m3_x, m3_y), m3_w, m3_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#d97706", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m3_x + 0.008, m3_y + m3_h - 0.038), m3_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#d97706", edgecolor="#b45309"
    ))
    ax.text(m3_x + m3_w/2, m3_y + m3_h - 0.022, "Module 3: Latent GraphSMOTE",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Mini Visual: Latent Typology Clusters & Convex Interpolation
    c_box_y = m3_y + 0.170
    ax.add_patch(patches.Rectangle((m3_x + 0.012, c_box_y), m3_w - 0.024, 0.135, fc="#fffbeb", ec="#fde68a", lw=0.8))
    ax.text(m3_x + 0.020, c_box_y + 0.120, "Latent Typology Manifold Synthesis:", fontsize=5.8, fontweight="bold", color="#92400e")

    # Cluster ellipses
    ax.add_patch(patches.Ellipse((m3_x + 0.065, c_box_y + 0.065), 0.065, 0.055, fc="#fed7aa", ec="#ea580c", lw=0.8, alpha=0.7))
    ax.text(m3_x + 0.065, c_box_y + 0.065, "Mule\nRing", ha="center", va="center", fontsize=4.8, fontweight="bold", color="#9a3412")

    ax.add_patch(patches.Ellipse((m3_x + 0.205, c_box_y + 0.075), 0.075, 0.055, fc="#fef08a", ec="#ca8a04", lw=0.8, alpha=0.7))
    ax.text(m3_x + 0.205, c_box_y + 0.075, "Layering\nChain", ha="center", va="center", fontsize=4.8, fontweight="bold", color="#854d0e")

    # Synthetic node interpolation
    p_a = np.array([m3_x + 0.085, c_box_y + 0.045])
    p_b = np.array([m3_x + 0.180, c_box_y + 0.055])
    p_syn = 0.55 * p_a + 0.45 * p_b
    ax.plot([p_a[0], p_b[0]], [p_a[1], p_b[1]], color="#b45309", lw=1.0, ls=":")
    ax.scatter([p_syn[0]], [p_syn[1]], s=80, marker="D", color="#dc2626", edgecolors="#fef08a", lw=1.2, zorder=5)
    ax.text(p_syn[0], p_syn[1] - 0.022, r"$\mathbf{h}_{\mathrm{syn}} = (1-\rho)\mathbf{h}_u + \rho\mathbf{h}_v$",
            ha="center", va="center", fontsize=5.0, fontweight="bold", color="#b91c1c")

    # Bilinear Edge Reconstruction & Guardrails Box
    b_box_y = m3_y + 0.045
    ax.add_patch(patches.Rectangle((m3_x + 0.012, b_box_y), m3_w - 0.024, 0.115, fc="#fef3c7", ec="#fcd34d", lw=0.8))
    ax.text(m3_x + 0.020, b_box_y + 0.098, "Bilinear Link Gen & Physical Bounds:", fontsize=5.8, fontweight="bold", color="#78350f")
    ax.text(m3_x + m3_w/2, b_box_y + 0.068, r"$\hat{A}_{\mathrm{syn}, w} = \sigma(\mathbf{h}_{\mathrm{syn}}^T \mathbf{W}_e \mathbf{h}_w)$",
            ha="center", va="center", fontsize=5.8, fontweight="bold", color="#92400e")
    ax.text(m3_x + m3_w/2, b_box_y + 0.035, r"Physical Invariant Guardrail: $\Phi_{\mathrm{flow}} \approx 1.0$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#059669")
    ax.text(m3_x + m3_w/2, b_box_y + 0.014, "Offline Training Quarantined (0% Test Leak)",
            ha="center", va="center", fontsize=5.0, color="#b45309", style="italic")

    # Tensor Output
    ax.text(m3_x + m3_w/2, m3_y + 0.018, r"Balanced Training Graph: $\tilde{\mathcal{G}}_{\mathrm{train}}$ (+9.92 pp Lift)",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#b45309")

    # Offline path connection down to M4
    ax.annotate("Offline Augmentation", xy=(0.825, 0.490), xytext=(0.825, 0.535),
                ha="center", va="center", fontsize=5.4, fontweight="bold", color="#b45309",
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#b45309", ls="--"))

    # =========================================================================
    # INTER-TIER CENTRAL TENSOR CONDUIT BUS (y: 0.470 to 0.520)
    # =========================================================================
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, 0.472), 0.970, 0.038,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#1e293b", edgecolor="#334155", lw=1.0
    ))
    ax.text(0.160, 0.491, r"Structural Embedding $\mathbf{h}_u^{(L)} \in \mathbb{R}^d$",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color="#a5b4fc")
    ax.text(0.500, 0.491, r"12-D Canonical Invariants $\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$ (Hydrodynamic Mass-Flow + Hawkes + Taint)",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color="#6ee7b7")
    ax.text(0.850, 0.491, r"Edge Gates $\hat{g}_{vu} \geq 0.10$",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color="#fde047")

    # Downward Arrow from M2 to Conduit Bus
    ax.annotate("", xy=(0.505, 0.510), xytext=(0.505, 0.535),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#7c3aed"))

    # =========================================================================
    # TIER 2: ADAPTIVE FUSION, BAYES RISK & CONFORMAL TRIAGE (y: 0.03 to 0.46)
    # =========================================================================
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, 0.030), 0.970, 0.435,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.2, linestyle="--"
    ))
    ax.text(0.030, 0.448, "TIER 2: EVIDENCE FUSION, BAYESIAN OPTIMIZATION & CONFORMAL RISK CONTROL",
            ha="left", va="center", fontsize=7.2, fontweight="bold", color="#334155")

    # -------------------------------------------------------------------------
    # MODULE 4: Evidence-Adaptive Fusion Engine (x: 0.025 to 0.325)
    # -------------------------------------------------------------------------
    m4_x, m4_y, m4_w, m4_h = 0.025, 0.045, 0.300, 0.385
    ax.add_patch(patches.FancyBboxPatch(
        (m4_x, m4_y), m4_w, m4_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#059669", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m4_x + 0.008, m4_y + m4_h - 0.038), m4_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#059669", edgecolor="#047857"
    ))
    ax.text(m4_x + m4_w/2, m4_y + m4_h - 0.022, "Module 4: Evidence-Adaptive Fusion",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Dynamic Fusion Gate Visual (Switch / Balance Slider)
    f_box_y = m4_y + 0.170
    ax.add_patch(patches.Rectangle((m4_x + 0.012, f_box_y), m4_w - 0.024, 0.170, fc="#f0fdf4", ec="#bbf7d0", lw=0.8))
    ax.text(m4_x + 0.020, f_box_y + 0.150, r"Adaptive Inductive Gating Unit $\alpha_u \in [0, 1]$:", fontsize=5.8, fontweight="bold", color="#065f46")

    # Equation
    ax.text(m4_x + m4_w/2, f_box_y + 0.122, r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u^{(L)} + (1 - \alpha_u) \mathbf{z}_{\mathrm{inv}}$",
            ha="center", va="center", fontsize=6.2, fontweight="bold", color="#047857")
    ax.text(m4_x + m4_w/2, f_box_y + 0.098, r"where $\alpha_u = \sigma(\mathbf{w}_\alpha^T [\mathbf{h}_u^{(L)} \| \mathbf{z}_{\mathrm{inv}}])$",
            ha="center", va="center", fontsize=5.4, color="#166534")

    # Two Branch Slider Cards
    # Cold-Start regime
    ax.add_patch(patches.FancyBboxPatch(
        (m4_x + 0.020, f_box_y + 0.012), 0.125, 0.070,
        boxstyle="round,pad=0.002", fc="#dcfce7", ec="#16a34a", lw=0.8
    ))
    ax.text(m4_x + 0.082, f_box_y + 0.062, "Cold-Start (deg <= 1)", ha="center", va="center", fontsize=5.0, fontweight="bold", color="#14532d")
    ax.text(m4_x + 0.082, f_box_y + 0.042, r"$\alpha_u \to 0$ (Inv Dominates)", ha="center", va="center", fontsize=4.8, color="#15803d")
    ax.text(m4_x + 0.082, f_box_y + 0.022, "89.60% Cold-Start F1", ha="center", va="center", fontsize=5.0, fontweight="bold", color="#065f46")

    # Dense Network regime
    ax.add_patch(patches.FancyBboxPatch(
        (m4_x + 0.155, f_box_y + 0.012), 0.125, 0.070,
        boxstyle="round,pad=0.002", fc="#eff6ff", ec="#3b82f6", lw=0.8
    ))
    ax.text(m4_x + 0.217, f_box_y + 0.062, "Dense Graph (deg >> 1)", ha="center", va="center", fontsize=5.0, fontweight="bold", color="#1e3a8a")
    ax.text(m4_x + 0.217, f_box_y + 0.042, r"$\alpha_u \to 1$ (GNN Dominates)", ha="center", va="center", fontsize=4.8, color="#2563eb")
    ax.text(m4_x + 0.217, f_box_y + 0.022, "Multi-Hop Topology", ha="center", va="center", fontsize=5.0, fontweight="bold", color="#1d4ed8")

    # Invariant Feed Footnote
    inv_box_y = m4_y + 0.045
    ax.add_patch(patches.Rectangle((m4_x + 0.012, inv_box_y), m4_w - 0.024, 0.110, fc="#f8fafc", ec="#cbd5e1", lw=0.8))
    ax.text(m4_x + 0.020, inv_box_y + 0.090, "12-D Canonical Invariant Inputs:", fontsize=5.8, fontweight="bold", color="#334155")
    ax.text(m4_x + m4_w/2, inv_box_y + 0.065, r"$\Phi_{\mathrm{flow}}$ (Kirchhoff Mass-Flow) + $\lambda_u$ (Hawkes)",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#0f766e")
    ax.text(m4_x + m4_w/2, inv_box_y + 0.040, r"$\mathbf{s}_{\mathrm{fwd}}, \mathbf{s}_{\mathrm{bwd}}$ (Causal Taints) + Moments $(\mu, \sigma^2, \gamma, \kappa)$",
            ha="center", va="center", fontsize=5.0, color="#475569")
    ax.text(m4_x + m4_w/2, inv_box_y + 0.018, "Zero Retraining across Heterogeneous Ledgers",
            ha="center", va="center", fontsize=5.0, color="#059669", fontweight="bold")

    # Tensor Output
    ax.text(m4_x + m4_w/2, m4_y + 0.018, r"Fused Evidence Vector: $\mathbf{h}_u^* \in \mathbb{R}^d$",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#047857")

    # Arrow M4 -> M5
    ax.annotate("", xy=(0.355, 0.240), xytext=(0.325, 0.240),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#059669"))

    # -------------------------------------------------------------------------
    # MODULE 5: Cost-Sensitive Bayesian Decision Boundary Head (x: 0.355 to 0.655)
    # -------------------------------------------------------------------------
    m5_x, m5_y, m5_w, m5_h = 0.355, 0.045, 0.300, 0.385
    ax.add_patch(patches.FancyBboxPatch(
        (m5_x, m5_y), m5_w, m5_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#dc2626", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m5_x + 0.008, m5_y + m5_h - 0.038), m5_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#dc2626", edgecolor="#b91c1c"
    ))
    ax.text(m5_x + m5_w/2, m5_y + m5_h - 0.022, "Module 5: Cost-Sensitive Bayes Head",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Mini Visual: 15:1 Asymmetric Cost & Optimal Threshold Shift
    c_curve_y = m5_y + 0.170
    ax.add_patch(patches.Rectangle((m5_x + 0.012, c_curve_y), m5_w - 0.024, 0.170, fc="#fef2f2", ec="#fecaca", lw=0.8))
    ax.text(m5_x + 0.020, c_curve_y + 0.150, "Bayesian Cost-Sensitive Risk Optimization:", fontsize=5.8, fontweight="bold", color="#991b1b")

    # Asymmetric loss formula
    ax.text(m5_x + m5_w/2, c_curve_y + 0.125, r"$\mathcal{L}_{\mathrm{asym}} = 15 \cdot \mathbb{I}(y=1)\log \hat{p} + 1 \cdot \mathbb{I}(y=0)\log(1-\hat{p})$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#b91c1c")
    ax.text(m5_x + m5_w/2, c_curve_y + 0.102, r"15:1 Asymmetry: \$150k FinCEN Penalty vs \$10k Review Cost",
            ha="center", va="center", fontsize=5.0, color="#7f1d1d")

    # Threshold shift curve
    t_axis = np.linspace(0, 1, 80)
    x_axis = m5_x + 0.030 + t_axis * (m5_w - 0.060)
    y_curve = c_curve_y + 0.030 + 0.045 * (t_axis - 0.18)**2 / (1 - 0.18)**2
    ax.plot(x_axis, y_curve, color="#dc2626", lw=1.4)
    
    # Naive threshold line (0.50)
    x_50 = m5_x + 0.030 + 0.50 * (m5_w - 0.060)
    ax.axvline(x_50, ymin=(c_curve_y + 0.015), ymax=(c_curve_y + 0.080), color="#94a3b8", ls=":", lw=1.0)
    ax.text(x_50, c_curve_y + 0.075, r"Naive $\tau=0.50$", ha="center", va="center", fontsize=4.8, color="#64748b")

    # Optimal Bayes threshold line (0.18)
    x_18 = m5_x + 0.030 + 0.18 * (m5_w - 0.060)
    ax.axvline(x_18, ymin=(c_curve_y + 0.015), ymax=(c_curve_y + 0.080), color="#dc2626", ls="--", lw=1.2)
    ax.text(x_18, c_curve_y + 0.014, r"$\tau^*=0.18$", ha="center", va="center", fontsize=5.2, fontweight="bold", color="#dc2626",
            bbox=dict(boxstyle="round,pad=0.15", fc="#ffffff", ec="#fca5a5", lw=0.6, alpha=0.95), zorder=6)

    # Expected Cost Minimum Callout
    ax.scatter([x_18], [c_curve_y + 0.030], s=40, color="#dc2626", edgecolors="#ffffff", lw=1.0, zorder=5)

    # Multi-Objective Loss Card
    m_loss_y = m5_y + 0.045
    ax.add_patch(patches.Rectangle((m5_x + 0.012, m_loss_y), m5_w - 0.024, 0.110, fc="#fff1f2", ec="#f43f5e", lw=0.8))
    ax.text(m5_x + 0.020, m_loss_y + 0.090, "Multi-Task Representation Loss:", fontsize=5.8, fontweight="bold", color="#881337")
    ax.text(m5_x + m5_w/2, m_loss_y + 0.065, r"$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{asym}} + \lambda_1 \mathcal{L}_{\mathrm{edge}} + \lambda_2 \mathcal{L}_{\mathrm{flow}}$",
            ha="center", va="center", fontsize=5.4, fontweight="bold", color="#be123c")
    ax.text(m5_x + m5_w/2, m_loss_y + 0.038, r"Non-Conformity Scoring: $s_i = 1 - \hat{p}_i(y)$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#9f1239")
    ax.text(m5_x + m5_w/2, m_loss_y + 0.016, "Calibrated Posterior for Distribution-Free CRC",
            ha="center", va="center", fontsize=5.0, color="#4c0519", style="italic")

    # Tensor Output
    ax.text(m5_x + m5_w/2, m5_y + 0.018, r"Calibrated Risk Score: $\hat{p}_u \in [0, 1]$",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#dc2626")

    # Arrow M5 -> M6
    ax.annotate("", xy=(0.685, 0.240), xytext=(0.655, 0.240),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#dc2626"))

    # -------------------------------------------------------------------------
    # MODULE 6: Class-Conditional Conformal Risk Control & 3-Tier Dispatch
    # (x: 0.685 to 0.965)
    # -------------------------------------------------------------------------
    m6_x, m6_y, m6_w, m6_h = 0.685, 0.045, 0.280, 0.385
    ax.add_patch(patches.FancyBboxPatch(
        (m6_x, m6_y), m6_w, m6_h,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        facecolor="#ffffff", edgecolor="#0284c7", lw=1.4
    ))
    # Header badge
    ax.add_patch(patches.FancyBboxPatch(
        (m6_x + 0.008, m6_y + m6_h - 0.038), m6_w - 0.016, 0.032,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#0284c7", edgecolor="#0369a1"
    ))
    ax.text(m6_x + m6_w/2, m6_y + m6_h - 0.022, "Module 6: Conformal CRC Arbiter",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#ffffff")

    # Calibration quantile info
    q_box_y = m6_y + 0.255
    ax.add_patch(patches.Rectangle((m6_x + 0.012, q_box_y), m6_w - 0.024, 0.085, fc="#f0f9ff", ec="#bae6fd", lw=0.8))
    ax.text(m6_x + 0.020, q_box_y + 0.068, r"Class-Conditional Quantiles ($1-\alpha \geq 99\%$):", fontsize=5.8, fontweight="bold", color="#0369a1")
    ax.text(m6_x + m6_w/2, q_box_y + 0.045, r"$\hat{q}^{(0)} = \mathrm{Quantile}\left(s_i^{(0)}, \frac{\lceil(n_0+1)(1-\alpha_0)\rceil}{n_0}\right)$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#0284c7")
    ax.text(m6_x + m6_w/2, q_box_y + 0.018, r"$\hat{q}^{(1)} = \mathrm{Quantile}\left(s_i^{(1)}, \frac{\lceil(n_1+1)(1-\alpha_1)\rceil}{n_1}\right)$",
            ha="center", va="center", fontsize=5.2, fontweight="bold", color="#0284c7")

    # Three-Tier Dispatch Funnel (Real 3-way branching boxes)
    t_h = 0.058
    # Tier 1 (Red)
    t1_y = m6_y + 0.175
    ax.add_patch(patches.FancyBboxPatch(
        (m6_x + 0.012, t1_y), m6_w - 0.024, t_h,
        boxstyle="round,pad=0.003", fc="#fee2e2", ec="#dc2626", lw=1.2
    ))
    ax.text(m6_x + 0.022, t1_y + 0.038, "Tier 1: Quarantine Hold", fontsize=5.6, fontweight="bold", color="#991b1b")
    ax.text(m6_x + m6_w - 0.022, t1_y + 0.038, "0.18% (18/10k)", ha="right", fontsize=5.2, fontweight="bold", color="#dc2626")
    ax.text(m6_x + 0.022, t1_y + 0.016, r"$\Gamma(u) = \{1\}$ | Auto Wire Freeze & FinCEN Form 111", fontsize=4.8, color="#7f1d1d")

    # Tier 2 (Amber)
    t2_y = m6_y + 0.110
    ax.add_patch(patches.FancyBboxPatch(
        (m6_x + 0.012, t2_y), m6_w - 0.024, t_h,
        boxstyle="round,pad=0.003", fc="#fef9c3", ec="#ca8a04", lw=1.2
    ))
    ax.text(m6_x + 0.022, t2_y + 0.038, "Tier 2: Compliance Desk", fontsize=5.6, fontweight="bold", color="#854d0e")
    ax.text(m6_x + m6_w - 0.022, t2_y + 0.038, "0.49% (49/10k)", ha="right", fontsize=5.2, fontweight="bold", color="#b45309")
    ax.text(m6_x + 0.022, t2_y + 0.016, r"$\Gamma(u) = \{0, 1\}$ | -99.51% Human Review Queue Cut", fontsize=4.8, color="#78350f", fontweight="bold")

    # Tier 3 (Green)
    t3_y = m6_y + 0.045
    ax.add_patch(patches.FancyBboxPatch(
        (m6_x + 0.012, t3_y), m6_w - 0.024, t_h,
        boxstyle="round,pad=0.003", fc="#dcfce7", ec="#16a34a", lw=1.2
    ))
    ax.text(m6_x + 0.022, t3_y + 0.038, "Tier 3: Straight-Through (STP)", fontsize=5.6, fontweight="bold", color="#166534")
    ax.text(m6_x + m6_w - 0.022, t3_y + 0.038, "99.33% (9.9k/10k)", ha="right", fontsize=5.2, fontweight="bold", color="#15803d")
    ax.text(m6_x + 0.022, t3_y + 0.016, r"$\Gamma(u) = \{0\}$ | 0.45 ms Real-Time Clear (<10ms SLA)", fontsize=4.8, color="#14532d", fontweight="bold")

    # Final Verdict Label
    ax.text(m6_x + m6_w/2, m6_y + 0.018, r"Deterministic Decision Set: $\Gamma(u) \subseteq \{0, 1\}$",
            ha="center", va="center", fontsize=5.6, fontweight="bold", color="#0369a1")

    # Save to all directories
    save_to_all(fig, "fig3_1_tensor_flow")


if __name__ == "__main__":
    print("Generating redesigned Figure 3.1: C-STGB End-to-End Architectural Dataflow...")
    generate_new_fig3_1()
    print("Done!")
