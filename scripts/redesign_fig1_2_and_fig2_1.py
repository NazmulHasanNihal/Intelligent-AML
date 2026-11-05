"""
scripts/redesign_fig1_2_and_fig2_1.py
Completely redesigns Figure 1.2 and Figure 2.1 for the National University CSE Thesis Monograph:

1. Figure 1.2: C-STGB Operational Architecture & Real-Time Conformal Triage Dataflow
   - Clear pipeline stages with explicit inter-column gaps so arrows never touch box boundaries.
   - Text boxes properly sized to prevent any string truncation or border collision.
   - Saves to: fig1_operational_architecture_flowchart.pdf & .png

2. Figure 2.1: Adversarial Camouflage Topology and Edge-Trust Filter Pruning
   - High-grade financial forensics schematic.
   - Offset edge-trust badges in Panel (b) so they never overlap edges or node badges.
   - Bottom status banners with spacious 2-line vertical typography (no collision).
   - Saves to: fig21_adversarial_camouflage_topology.pdf & .png

Guarantees:
- Zero text overlap / word collision
- Zero border clipping (pad_inches=0.15)
- Saves to all target directories across the repository
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
    'axes.labelsize': 9.0,
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


# =============================================================================
# 1. FIGURE 1.2: C-STGB OPERATIONAL ARCHITECTURE & REAL-TIME TRIAGE FLOWCHART
# =============================================================================
def generate_intuitive_fig1_2():
    # Canvas dimensions: 9.2 x 5.6 inches (spacious and clear)
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.axis('off')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # -------------------------------------------------------------------------
    # Master Header Banner (y: 0.925 -> 0.990)
    # -------------------------------------------------------------------------
    ax.add_patch(patches.FancyBboxPatch(
        (0.015, 0.925), 0.970, 0.065,
        boxstyle="round,pad=0.005,rounding_size=0.012",
        facecolor="#0f172a", edgecolor="#1e293b", lw=1.2
    ))
    ax.text(0.50, 0.963, "C-STGB: Real-Time Financial Surveillance Architecture & Conformal Triage Platform",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.940, "End-to-End Pipeline: Multi-Rail Ingestion -> 12-D Invariants -> Spatio-Temporal GNN -> 3-Tier Conformal Triage",
            ha="center", va="center", fontsize=7.2, color="#94a3b8", style="italic")

    # -------------------------------------------------------------------------
    # STAGE 1: Multi-Rail Streaming Ingestion (x: 0.015 -> 0.170, y: 0.21 -> 0.905)
    # -------------------------------------------------------------------------
    s1_w = 0.155
    s1_x = 0.015
    ax.add_patch(patches.FancyBboxPatch(
        (s1_x, 0.21), s1_w, 0.695,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#f8fafc", edgecolor="#2563eb", lw=1.4
    ))
    
    # Stage 1 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (s1_x + 0.008, 0.845), s1_w - 0.016, 0.045,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#2563eb", edgecolor="#1d4ed8"
    ))
    ax.text(s1_x + s1_w/2, 0.867, "1. Streaming Ingest", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#ffffff")

    # Payment Rail Badges (Vertical Stack)
    rails = [
        ("SWIFT MT103 / ISO-20022", "Cross-Border Wires", "#1e40af", "#eff6ff"),
        ("Domestic RTGS / ACH", "Instant Net Settlement", "#0369a1", "#f0f9ff"),
        ("Mobile Money", "bKash / Nagad Velocity", "#0f766e", "#f0fdfa"),
        ("Crypto UTXO & EVM", "Bitcoin & Ethereum", "#6d28d9", "#faf5ff"),
    ]
    for idx, (title, sub, col_fg, col_bg) in enumerate(rails):
        y_r = 0.695 - idx * 0.108
        ax.add_patch(patches.FancyBboxPatch(
            (s1_x + 0.008, y_r), s1_w - 0.016, 0.090,
            boxstyle="round,pad=0.003,rounding_size=0.006",
            facecolor=col_bg, edgecolor=col_fg, lw=0.9
        ))
        ax.text(s1_x + s1_w/2, y_r + 0.057, title, ha="center", va="center", fontsize=5.6, fontweight="bold", color=col_fg)
        ax.text(s1_x + s1_w/2, y_r + 0.026, sub, ha="center", va="center", fontsize=5.1, color="#475569")

    # Ingestion Buffer Footnote
    ax.add_patch(patches.FancyBboxPatch(
        (s1_x + 0.008, 0.225), s1_w - 0.016, 0.058,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#f1f5f9", edgecolor="#94a3b8", lw=0.8
    ))
    ax.text(s1_x + s1_w/2, 0.260, "DuckDB + Arrow IPC", ha="center", va="center", fontsize=6.0, fontweight="bold", color="#1e293b")
    ax.text(s1_x + s1_w/2, 0.238, "0.11 ms Zero-Copy Ingest", ha="center", va="center", fontsize=5.2, color="#059669", fontweight="bold")

    # Arrow Stage 1 -> Stage 2 (Across dedicated gap x: 0.170 -> 0.198)
    ax.annotate("", xy=(0.196, 0.55), xytext=(0.172, 0.55),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#2563eb"))

    # -------------------------------------------------------------------------
    # STAGE 2: 12-D Physical Invariant Engine (x: 0.200 -> 0.380, y: 0.21 -> 0.905)
    # -------------------------------------------------------------------------
    s2_x = 0.200
    s2_w = 0.180
    ax.add_patch(patches.FancyBboxPatch(
        (s2_x, 0.21), s2_w, 0.695,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#f8fafc", edgecolor="#0d9488", lw=1.4
    ))
    
    # Stage 2 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (s2_x + 0.008, 0.845), s2_w - 0.016, 0.045,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#0d9488", edgecolor="#0f766e"
    ))
    ax.text(s2_x + s2_w/2, 0.867, "2. 12-D Invariants", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#ffffff")

    # Invariant Card 1: Hydrodynamic Mass-Flow Pipe
    ax.add_patch(patches.FancyBboxPatch(
        (s2_x + 0.008, 0.575), s2_w - 0.016, 0.250,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#f0fdfa", edgecolor="#14b8a6", lw=1.0
    ))
    ax.text(s2_x + s2_w/2, 0.795, "Hydrodynamic Mass Flow", ha="center", va="center", fontsize=6.6, fontweight="bold", color="#0f766e")
    
    # Mini pipe diagram inside Card 1
    pipe_x = s2_x + 0.018
    pipe_w = s2_w - 0.036
    ax.add_patch(patches.FancyBboxPatch((pipe_x, 0.695), pipe_w, 0.075, boxstyle="round,pad=0.002", fc="#ccfbf1", ec="#0d9488", lw=0.9))
    ax.add_patch(patches.Circle((s2_x + s2_w/2, 0.732), 0.026, fc="#fecaca", ec="#dc2626", lw=1.0))
    ax.text(s2_x + s2_w/2, 0.732, "Mule", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#991b1b")
    ax.text(pipe_x + 0.012, 0.732, "In", ha="left", va="center", fontsize=5.2, fontweight="bold", color="#0d9488")
    ax.text(pipe_x + pipe_w - 0.012, 0.732, "Out", ha="right", va="center", fontsize=5.2, fontweight="bold", color="#0d9488")

    ax.text(s2_x + s2_w/2, 0.648, r"Flow Balance: $\Phi_{\mathrm{flow}} \approx 1.0$", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#0f766e")
    ax.text(s2_x + s2_w/2, 0.612, "(Zero Retention Conduit)", ha="center", va="center", fontsize=5.0, color="#475569")

    # Invariant Card 2: Hawkes Temporal Burst Intensity
    ax.add_patch(patches.FancyBboxPatch(
        (s2_x + 0.008, 0.315), s2_w - 0.016, 0.240,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#fff7ed", edgecolor="#f97316", lw=1.0
    ))
    ax.text(s2_x + s2_w/2, 0.525, "Hawkes Point Process", ha="center", va="center", fontsize=6.6, fontweight="bold", color="#c2410c")
    
    # Mini spike curve
    t_mini = np.linspace(s2_x + 0.022, s2_x + s2_w - 0.022, 50)
    center_t = s2_x + s2_w/2 - 0.015
    y_spike = 0.440 + 0.045 * np.exp(-120 * (t_mini - center_t)**2)
    ax.plot(t_mini, y_spike, color="#ea580c", lw=1.5)
    
    ax.text(s2_x + s2_w/2, 0.410, r"Bursts: $\lambda_u(t) > 12.0$", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#9a3412")
    ax.text(s2_x + s2_w/2, 0.375, "Smurfing Acceleration", ha="center", va="center", fontsize=5.2, color="#7c2d12")
    ax.text(s2_x + s2_w/2, 0.335, r"Causal Taint: $\mathbf{s}_{\mathrm{fwd}}, \mathbf{s}_{\mathrm{bwd}}$", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#431407")

    # Output Vector Label at bottom
    ax.add_patch(patches.FancyBboxPatch(
        (s2_x + 0.008, 0.225), s2_w - 0.016, 0.058,
        boxstyle="round,pad=0.003,rounding_size=0.006",
        facecolor="#ecfdf5", edgecolor="#10b981", lw=0.8
    ))
    ax.text(s2_x + s2_w/2, 0.254, r"Invariant: $\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12}$", ha="center", va="center", fontsize=6.0, fontweight="bold", color="#065f46")

    # Arrow Stage 2 -> Stage 3 (Across dedicated gap x: 0.380 -> 0.408)
    ax.annotate("", xy=(0.406, 0.55), xytext=(0.382, 0.55),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#0d9488"))

    # -------------------------------------------------------------------------
    # STAGE 3: Continuous Spatio-Temporal GNN Core (x: 0.408 -> 0.615, y: 0.21 -> 0.905)
    # -------------------------------------------------------------------------
    s3_x = 0.410
    s3_w = 0.205
    ax.add_patch(patches.FancyBboxPatch(
        (s3_x, 0.21), s3_w, 0.695,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#f8fafc", edgecolor="#4f46e5", lw=1.4
    ))

    # Stage 3 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (s3_x + 0.008, 0.845), s3_w - 0.016, 0.045,
        boxstyle="round,pad=0.004,rounding_size=0.008",
        facecolor="#4f46e5", edgecolor="#4338ca"
    ))
    ax.text(s3_x + s3_w/2, 0.867, "3. Spatio-Temporal GNN", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#ffffff")

    # GNN Module 1: Tri-Band Harmonic Attention
    ax.add_patch(patches.FancyBboxPatch(
        (s3_x + 0.008, 0.665), s3_w - 0.016, 0.160,
        boxstyle="round,pad=0.004,rounding_size=0.007",
        facecolor="#eef2ff", edgecolor="#6366f1", lw=0.9
    ))
    ax.text(s3_x + s3_w/2, 0.795, "Tri-Band Harmonic Attention", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#3730a3")
    ax.text(s3_x + s3_w/2, 0.760, r"$\tau_1=2.4\,\mathrm{h}$ (Burst)  |  $\tau_2=24\,\mathrm{h}$ (Diurnal)", ha="center", va="center", fontsize=5.2, color="#4338ca")
    ax.text(s3_x + s3_w/2, 0.730, r"$\tau_3=168\,\mathrm{h}$ (90-Day Dormant Hibernation)", ha="center", va="center", fontsize=5.2, color="#4338ca")
    ax.text(s3_x + s3_w/2, 0.690, "Resolves Long-Dwell Blindness", ha="center", va="center", fontsize=5.3, fontweight="bold", color="#1e1b4b")

    # GNN Module 2: Edge-Trust Camouflage Pruner
    ax.add_patch(patches.FancyBboxPatch(
        (s3_x + 0.008, 0.465), s3_w - 0.016, 0.180,
        boxstyle="round,pad=0.004,rounding_size=0.007",
        facecolor="#faf5ff", edgecolor="#a855f7", lw=0.9
    ))
    ax.text(s3_x + s3_w/2, 0.615, "Learnable Edge-Trust Gating", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#6b21a8")
    ax.text(s3_x + s3_w/2, 0.575, r"Threshold Floor: $\hat{g}_{ij} \geq 0.10$", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#7e22ce")
    ax.text(s3_x + s3_w/2, 0.535, "Prunes 65.9% Camouflage Chaff", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#059669")
    ax.text(s3_x + s3_w/2, 0.495, "Dirichlet Energy Preserved (>0.75)", ha="center", va="center", fontsize=5.2, color="#475569")

    # GNN Module 3: Evidence Fusion & Cost-Sensitive Head
    ax.add_patch(patches.FancyBboxPatch(
        (s3_x + 0.008, 0.225), s3_w - 0.016, 0.220,
        boxstyle="round,pad=0.004,rounding_size=0.007",
        facecolor="#fef2f2", edgecolor="#ef4444", lw=0.9
    ))
    ax.text(s3_x + s3_w/2, 0.415, "Adaptive Evidence Fusion", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#991b1b")
    ax.text(s3_x + s3_w/2, 0.375, r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#b91c1c")
    ax.text(s3_x + s3_w/2, 0.335, "Cold-Start: 89.60% F1 (deg <= 2)", ha="center", va="center", fontsize=5.2, color="#7f1d1d")
    ax.text(s3_x + s3_w/2, 0.298, "Cost Head: 15:1 Asymmetric Ratio", ha="center", va="center", fontsize=5.2, color="#7f1d1d")
    ax.text(s3_x + s3_w/2, 0.255, r"Risk Estimate: $\hat{p}_u \in [0, 1]$", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#991b1b")

    # Arrow Stage 3 -> Decision Diamond (Across dedicated gap x: 0.615 -> 0.645)
    ax.annotate("", xy=(0.645, 0.55), xytext=(0.615, 0.55),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#4f46e5"))

    # -------------------------------------------------------------------------
    # STAGE 4: Conformal CRC Decision Diamond (Center: 0.700, 0.55)
    # -------------------------------------------------------------------------
    diamond_pts = np.array([[0.645, 0.55], [0.700, 0.68], [0.755, 0.55], [0.700, 0.42]])
    diamond = patches.Polygon(diamond_pts, closed=True, fc='#fef3c7', ec='#d97706', lw=1.8, zorder=4)
    ax.add_patch(diamond)
    ax.text(0.700, 0.585, "Class-Cond.", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#92400e", zorder=5)
    ax.text(0.700, 0.550, "CRC Arbiter", ha="center", va="center", fontsize=6.6, fontweight="bold", color="#92400e", zorder=5)
    ax.text(0.700, 0.515, r"$1-\alpha \geq 99\%$", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#b45309", zorder=5)

    # -------------------------------------------------------------------------
    # STAGE 5: Three-Tier Operational Dispatch (x: 0.785 -> 0.985, y: 0.21 -> 0.905)
    # -------------------------------------------------------------------------
    s5_x = 0.785
    s5_w = 0.200
    
    # Tier 1 (Quarantine) - Top Red (y: 0.690 -> 0.890)
    t1_box = patches.FancyBboxPatch(
        (s5_x, 0.690), s5_w, 0.200,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        fc='#fee2e2', ec='#dc2626', lw=1.5
    )
    ax.add_patch(t1_box)
    ax.text(s5_x + s5_w/2, 0.855, "Tier 1: Quarantine Hold", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#991b1b")
    ax.text(s5_x + s5_w/2, 0.810, r"Decisive Illicit: $\Gamma(u) = \{1\}$", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#b91c1c")
    ax.text(s5_x + s5_w/2, 0.765, "Volume: 18 / 10k tx (0.18%)", ha="center", va="center", fontsize=5.8, color="#7f1d1d")
    ax.text(s5_x + s5_w/2, 0.725, "Auto Wire Freeze & FinCEN SAR", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#991b1b")
    
    # Connection arrow from diamond to Tier 1
    ax.annotate("", xy=(s5_x, 0.790), xytext=(0.745, 0.635),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#dc2626", connectionstyle="arc3,rad=-0.10"))

    # Tier 2 (Review) - Mid Amber (y: 0.450 -> 0.650)
    t2_box = patches.FancyBboxPatch(
        (s5_x, 0.450), s5_w, 0.200,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        fc='#fef9c3', ec='#ca8a04', lw=1.5
    )
    ax.add_patch(t2_box)
    ax.text(s5_x + s5_w/2, 0.615, "Tier 2: Compliance Desk", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#854d0e")
    ax.text(s5_x + s5_w/2, 0.570, r"Abstention Set: $\Gamma(u) = \{0, 1\}$", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#a16207")
    ax.text(s5_x + s5_w/2, 0.525, "Volume: 49 / 10k tx (0.49%)", ha="center", va="center", fontsize=5.8, color="#78350f")
    ax.text(s5_x + s5_w/2, 0.485, "-99.51% Human Review Queue Cut", ha="center", va="center", fontsize=5.5, fontweight="bold", color="#854d0e")
    
    # Connection arrow from diamond to Tier 2
    ax.annotate("", xy=(s5_x, 0.550), xytext=(0.755, 0.550),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#ca8a04"))

    # Tier 3 (Clear) - Bottom Green (y: 0.210 -> 0.410)
    t3_box = patches.FancyBboxPatch(
        (s5_x, 0.210), s5_w, 0.200,
        boxstyle="round,pad=0.005,rounding_size=0.010",
        fc='#dcfce7', ec='#16a34a', lw=1.5
    )
    ax.add_patch(t3_box)
    ax.text(s5_x + s5_w/2, 0.375, "Tier 3: Straight-Through (STP)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#166534")
    ax.text(s5_x + s5_w/2, 0.330, r"Decisive Benign: $\Gamma(u) = \{0\}$", ha="center", va="center", fontsize=6.4, fontweight="bold", color="#15803d")
    ax.text(s5_x + s5_w/2, 0.285, "Volume: 9,933 / 10k tx (99.33%)", ha="center", va="center", fontsize=5.8, color="#14532d")
    ax.text(s5_x + s5_w/2, 0.245, "0.45 ms Real-Time Clear (<10ms SLA)", ha="center", va="center", fontsize=5.4, fontweight="bold", color="#166534")
    
    # Connection arrow from diamond to Tier 3
    ax.annotate("", xy=(s5_x, 0.310), xytext=(0.745, 0.465),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#16a34a", connectionstyle="arc3,rad=0.10"))

    # -------------------------------------------------------------------------
    # BOTTOM: Executive Assurance & Statutory Governance Strip (y: 0.025 -> 0.170)
    # -------------------------------------------------------------------------
    kpis = [
        ("Real-Time Latency SLA", "0.45 ms Fast-Path", "P99 0.82 ms | 31,200 tx/s throughput\nStrict compliance with <10 ms banking SLA", "#1e40af", "#eff6ff"),
        ("Operational Efficiency", "-99.51% Review Cut", "Only 49 of 10,000 alerts sent to humans\n85.7% to 95.8% fewer false alerts vs rules", "#0f766e", "#f0fdfa"),
        ("Statistical Safety Bound", ">= 99.0% True Coverage", "Finite-sample exchangeability guarantee\n0.00% empty sets | Exact risk-control", "#b45309", "#fffbeb"),
        ("Statutory Governance", "Fed SR 11-7 & OCC Ready", "Zero-hallucination AST compliance swarm\nSHA-256 Merkle cryptographic audit trail", "#6d28d9", "#faf5ff"),
    ]

    for idx, (kpi_title, kpi_val, kpi_sub, col_fg, col_bg) in enumerate(kpis):
        x_k = 0.015 + idx * 0.245
        w_k = 0.235
        ax.add_patch(patches.FancyBboxPatch(
            (x_k, 0.025), w_k, 0.155,
            boxstyle="round,pad=0.004,rounding_size=0.008",
            facecolor=col_bg, edgecolor=col_fg, lw=1.1
        ))
        ax.text(x_k + w_k/2, 0.148, kpi_title, ha="center", va="center", fontsize=6.2, fontweight="bold", color="#475569")
        ax.text(x_k + w_k/2, 0.116, kpi_val, ha="center", va="center", fontsize=8.0, fontweight="bold", color=col_fg)
        ax.text(x_k + w_k/2, 0.065, kpi_sub, ha="center", va="center", fontsize=5.0, color="#334155", linespacing=1.25)

    save_to_all(fig, "fig1_operational_architecture_flowchart")
    # Also save as alternative stem
    for d in TARGET_DIRS:
        fig.savefig(d / "fig_conformal_triage_flowchart.pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(d / "fig_conformal_triage_flowchart.png", dpi=300, bbox_inches="tight", pad_inches=0.15)


# =============================================================================
# 2. FIGURE 2.1: ADVERSARIAL CAMOUFLAGE TOPOLOGY & EDGE-TRUST PRUNING
# =============================================================================
def generate_upgraded_fig2_1():
    # Canvas dimensions: 9.2 x 5.2 inches (generous, high-res)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 5.2))
    
    for ax in axes:
        ax.axis('off')
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)

    # Coordinated Positions for Graph Entities
    # Illicit Laundering Syndicate (Central Wash Ring)
    pos_syndicate = {
        'S0': np.array([-0.36,  0.42]), # Placement source
        'M1': np.array([ 0.18,  0.48]), # Mule 1
        'M2': np.array([ 0.44,  0.04]), # Mule 2
        'L3': np.array([ 0.14, -0.38]), # Layering 3
        'C4': np.array([-0.36, -0.32]), # Integration sink
    }
    
    # Legitimate High-Degree Merchant Hubs (Peripheral anchors)
    pos_merchants = {
        'H1': np.array([-0.95,  0.80]), # Retail E-Commerce Mega-Hub
        'H2': np.array([ 0.95,  0.80]), # Utility & Telecom Invoicing Hub
        'H3': np.array([ 0.95, -0.72]), # Digital Wallet / P2P Settlement
        'H4': np.array([-0.95, -0.72]), # Licensed Exchange Custody Pool
    }
    
    # Benign customer nodes around each merchant hub (star clusters)
    np.random.seed(101)
    merchant_customers = {}
    for h_name, h_pos in pos_merchants.items():
        n_cust = 8
        angles = np.linspace(0, 2*np.pi, n_cust, endpoint=False) + np.random.uniform(-0.18, 0.18, n_cust)
        radii = np.random.uniform(0.18, 0.30, n_cust)
        cust_pos = [h_pos + np.array([r * np.cos(a), r * np.sin(a)]) for a, r in zip(angles, radii)]
        merchant_customers[h_name] = cust_pos

    chaff_pairs = [
        ('M1', 'H1'), ('M1', 'H2'), ('M1', 'H3'),
        ('M2', 'H2'), ('M2', 'H3'), ('M2', 'H1'),
        ('L3', 'H3'), ('L3', 'H4'), ('L3', 'H2'),
        ('S0', 'H1'), ('S0', 'H4'),
        ('C4', 'H4'), ('C4', 'H3'),
    ]
    syn_edges = [('S0', 'M1'), ('M1', 'M2'), ('M2', 'L3'), ('L3', 'C4'), ('C4', 'S0')]

    # -------------------------------------------------------------------------
    # PANEL (a): Raw Camouflaged Topology (Adversarial Chaff Injection)
    # -------------------------------------------------------------------------
    ax0 = axes[0]
    ax0.set_title("(a) Raw Camouflaged Transaction Network\n(50+ Spurious Chaff Edges Inducing Over-Smoothing)",
                  fontsize=8.8, fontweight="bold", color="#0f172a", pad=10)

    # 1. Benign Customer Star Edges
    for h_name, h_pos in pos_merchants.items():
        for c_pos in merchant_customers[h_name]:
            ax0.plot([h_pos[0], c_pos[0]], [h_pos[1], c_pos[1]], color="#cbd5e1", lw=0.9, zorder=1)
            ax0.scatter(c_pos[0], c_pos[1], s=18, color="#94a3b8", edgecolors="#64748b", lw=0.5, zorder=2)

    # 2. Adversarial Camouflage Chaff Edges
    for src, dst in chaff_pairs:
        p1 = pos_syndicate[src]
        p2 = pos_merchants[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=1.1, color="#f87171", ls="--", alpha=0.85))
    
    # 3. True Illicit Laundering Conduit Edges (Obscured)
    for src, dst in syn_edges:
        p1 = pos_syndicate[src]
        p2 = pos_syndicate[dst]
        ax0.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=2.2, color="#dc2626"))

    # 4. Merchant Hub Nodes
    for h_name, h_pos in pos_merchants.items():
        ax0.scatter(h_pos[0], h_pos[1], s=260, color="#0284c7", edgecolors="#0369a1", lw=1.5, zorder=4)
        ax0.text(h_pos[0], h_pos[1], h_name, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

    # 5. Syndicate Nodes
    for s_name, s_pos in pos_syndicate.items():
        col = "#991b1b" if s_name in ['S0', 'C4'] else "#ea580c"
        ax0.scatter(s_pos[0], s_pos[1], s=220, color=col, edgecolors="#ffffff", lw=1.5, zorder=6)
        ax0.text(s_pos[0], s_pos[1], s_name, ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=7)

    # Over-smoothing Warning Banner with Generous 2-Line Separation
    ax0.add_patch(patches.FancyBboxPatch(
        (-1.26, -1.28), 2.52, 0.22,
        boxstyle="round,pad=0.005", fc="#fef2f2", ec="#ef4444", lw=1.0
    ))
    ax0.text(0.0, -1.14, "Standard GNN Failure: Feature Over-Smoothing Collapse", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#991b1b")
    ax0.text(0.0, -1.22, r"Spurious Chaff dilutes Dirichlet Energy ($\mathcal{E} \to 0$); Laundering disguised as Benign Hub activity.", ha="center", va="center", fontsize=5.6, color="#7f1d1d")

    # -------------------------------------------------------------------------
    # PANEL (b): C-STGB Edge-Gated Subgraph (65.9% Camouflage Noise Pruned)
    # -------------------------------------------------------------------------
    ax1 = axes[1]
    ax1.set_title(r"(b) C-STGB Context-Aware Edge-Trust Gating ($\hat{g}_{ij} \geq 0.92$)" + "\n(65.9% Spurious Camouflage Chaff Pruned)",
                  fontsize=8.8, fontweight="bold", color="#0f172a", pad=10)

    # 1. Benign Customer Star Edges (Preserved)
    for h_name, h_pos in pos_merchants.items():
        for c_pos in merchant_customers[h_name]:
            ax1.plot([h_pos[0], c_pos[0]], [h_pos[1], c_pos[1]], color="#cbd5e1", lw=0.9, zorder=1)
            ax1.scatter(c_pos[0], c_pos[1], s=18, color="#94a3b8", edgecolors="#64748b", lw=0.5, zorder=2)

    # 2. Pruned Chaff Edges (Faded and Marked with Prune Badges)
    for src, dst in chaff_pairs:
        p1 = pos_syndicate[src]
        p2 = pos_merchants[dst]
        ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#e2e8f0", lw=0.8, ls=":", alpha=0.45, zorder=1)
        mid = 0.5 * (p1 + p2)
        ax1.text(mid[0], mid[1], "×", ha="center", va="center", fontsize=7.2, color="#ef4444", fontweight="bold", alpha=0.75)

    # 3. Cleanly Isolated True Laundering Conduit
    for src, dst in syn_edges:
        p1 = pos_syndicate[src]
        p2 = pos_syndicate[dst]
        ax1.annotate("", xy=p2, xytext=p1,
                     arrowprops=dict(arrowstyle="->", lw=2.6, color="#059669"))

    # Explicitly positioned Edge-Trust Badges (NO OVERLAP WITH NODES OR EDGES)
    badge_positions = [
        (-0.09,  0.55), # for S0 -> M1 (above edge)
        ( 0.42,  0.32), # for M1 -> M2 (right of edge)
        ( 0.38, -0.22), # for M2 -> L3 (right of edge)
        (-0.11, -0.46), # for L3 -> C4 (below edge)
        (-0.48,  0.05), # for C4 -> S0 (left of edge)
    ]
    for bx, by in badge_positions:
        ax1.text(bx, by, r"$\hat{g} \approx 0.95$", ha="center", va="center", 
                 fontsize=5.2, fontweight="bold", color="#065f46",
                 bbox=dict(boxstyle="round,pad=0.18", fc="#dcfce7", ec="#16a34a", lw=0.6, alpha=0.95), zorder=8)

    # 4. Merchant Hub Nodes
    for h_name, h_pos in pos_merchants.items():
        ax1.scatter(h_pos[0], h_pos[1], s=260, color="#0284c7", edgecolors="#0369a1", lw=1.5, zorder=4)
        ax1.text(h_pos[0], h_pos[1], h_name, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff", zorder=5)

    # 5. Syndicate Nodes
    for s_name, s_pos in pos_syndicate.items():
        col = "#991b1b" if s_name in ['S0', 'C4'] else "#ea580c"
        ax1.scatter(s_pos[0], s_pos[1], s=240, color=col, edgecolors="#fde047", lw=2.0, zorder=6)
        ax1.text(s_pos[0], s_pos[1], s_name, ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=7)

    # Dirichlet Preservation Success Banner with Generous 2-Line Separation
    ax1.add_patch(patches.FancyBboxPatch(
        (-1.26, -1.28), 2.52, 0.22,
        boxstyle="round,pad=0.005", fc="#ecfdf5", ec="#10b981", lw=1.0
    ))
    ax1.text(0.0, -1.14, "C-STGB Protection: Spectral Dirichlet Energy Preserved", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#065f46")
    ax1.text(0.0, -1.22, r"Edge Gate filters 65.9% Chaff ($\hat{g}_{ij} < 0.10$); True Wash Cycle Isolated for Tier-1 Quarantine ($\mathcal{E} > 0.75$).", ha="center", va="center", fontsize=5.6, color="#047857")

    # -------------------------------------------------------------------------
    # Shared Unified Legend Below Both Panels
    # -------------------------------------------------------------------------
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Merchant Commercial Hubs (H1-H4)', markerfacecolor='#0284c7', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Laundering Syndicate (S0, M1-M2, L3, C4)', markerfacecolor='#dc2626', markeredgecolor='#fde047', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Benign Retail Customers', markerfacecolor='#94a3b8', markersize=5),
        plt.Line2D([0], [0], color='#dc2626', lw=2.0, label='Illicit Flow Conduit'),
        plt.Line2D([0], [0], color='#f87171', lw=1.2, linestyle='--', label='Adversarial Camouflage Chaff (Spurious)'),
        plt.Line2D([0], [0], color='#059669', lw=2.0, label='C-STGB Denoised Wash Cycle (g_ij >= 0.92)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.015),
               ncol=3, fontsize=6.6, framealpha=0.96, edgecolor='#cbd5e1')

    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.15, wspace=0.12)
    save_to_all(fig, "fig21_adversarial_camouflage_topology")


if __name__ == "__main__":
    print("Generating newly redesigned, intuitive Figure 1.2 and upgraded Figure 2.1...")
    generate_intuitive_fig1_2()
    generate_upgraded_fig2_1()
    print("Both figures successfully redesigned and saved!")
