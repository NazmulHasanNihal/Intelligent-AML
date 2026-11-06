"""
scripts/redesign_fig9_1_enterprise_lifecycle.py
Publication-grade phased enterprise deployment pipeline diagram.

Architecture:
- Stage I: Passive Shadow Deployment & Rolling Conformal Calibration (Zero Live Overhead, 90d Horizon, DKW Conformal Tuning)
- Stage II: Dual-Run Conformal Pilot & Selective Abstention (Active Learning Loop, GNNExplainer Dossiers, SLA Stress Test)
- Stage III: Full-Scale Autonomous Straight-Through Surveillance (STP >99.38%, Tier-1 Freeze, FinCEN XML, Merkle WORM)
- Sharp rectangular engineering blocks, clear horizontal progression connectors, strictly NO consumer card ribbons.
"""

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

def generate_figure_9_1():
    # Sized for aspect ratio ~2.48:1 (9.6 x 4.0 inches)
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    ax.axis('off')
    ax.set_xlim([-0.010, 1.010])
    ax.set_ylim([-0.015, 1.015])

    # 1. Outer Master Canvas Frame (sharp rectangle)
    ax.add_patch(patches.Rectangle(
        (0.000, 0.000), 1.000, 1.000,
        facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1.0
    ))

    # 2. Master Header Banner
    ax.add_patch(patches.Rectangle(
        (0.005, 0.925), 0.990, 0.068,
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.018, 0.966, 'Phased Enterprise Production Deployment Lifecycle & Verification Gates',
            ha='left', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')
    ax.text(0.018, 0.941,
            r'Tier-1 Core Banking Adoption Framework: Passive Shadow Ingestion $\rightarrow$ Dual-Run Conformal Pilot $\rightarrow$ Straight-Through Autonomous Surveillance',
            ha='left', va='center', fontsize=6.2, color='#94a3b8')

    # Top Right Status Pill
    ax.add_patch(patches.Rectangle(
        (0.748, 0.932), 0.240, 0.054,
        facecolor='#065f46', edgecolor='#10b981', linewidth=0.8
    ))
    ax.text(0.868, 0.959, 'OPERATIONAL MATURITY: STAGE I -> II -> III',
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')

    # =========================================================================
    # 3 PROGRESSIVE MATURITY STAGES ACROSS x in [0.010, 0.990]
    # =========================================================================
    col_w = 0.316
    spacing = 0.016
    col_x = [0.010, 0.010 + col_w + spacing, 0.010 + 2*(col_w + spacing)] # 0.010, 0.342, 0.674
    c_top, c_bot = 0.910, 0.025
    c_h = c_top - c_bot

    stages = [
        {
            "id": "STAGE I: PASSIVE SHADOW DEPLOYMENT",
            "sub": "Zero-Impact Ingestion & 90-Day Conformal Calibration",
            "bg": "#f8fafc", "border": "#94a3b8", "hdr_bg": "#334155", "hdr_fg": "#ffffff",
            "gate": "GATE 1: CALIBRATION STABILIZATION (1-alpha >= 99.0%)",
            "gate_bg": "#f1f5f9", "gate_border": "#64748b", "gate_fg": "#334155",
            "items": [
                ("1. Passive Payment Rail Ingestion", "Mirrored Kafka / Pulsar stream subscriber; zero-copy DuckDB + PyArrow IPC memory buffer. Live core banking overhead: 0.00 ms.", "#0369a1"),
                ("2. Real-Time Shadow Scoring Engine", "Executes C-STGB forward pass asynchronously in shadow mode alongside legacy rule engines, logging continuous non-conformity scores.", "#0f766e"),
                ("3. 90-Day Rolling Calibration Horizon", r"Accumulates quarterly calibration split $\mathcal{D}_{\text{cal}}$, tuning class-conditional quantiles $\hat{q}^{(0)}, \hat{q}^{(1)}$ to guarantee $1-\alpha \geq 99.0\%$.", "#c2410c"),
                ("4. Streaming Drift Stability Audit", r"Monitors two-sample Kolmogorov-Smirnov drift statistics ($p > 0.05$), validating exchangeability before live transaction routing.", "#6d28d9")
            ]
        },
        {
            "id": "STAGE II: DUAL-RUN CONFORMAL PILOT",
            "sub": "Human-in-the-Loop Collaboration & Hard-Negative Active Learning",
            "bg": "#fff7ed", "border": "#fb923c", "hdr_bg": "#ea580c", "hdr_fg": "#ffffff",
            "gate": "GATE 2: ZERO-DEFECT STRESS SLA (<2.5 ms @ 31.2k tx/s)",
            "gate_bg": "#ffedd5", "gate_border": "#ea580c", "gate_fg": "#9a3412",
            "items": [
                ("1. Dual-Run Concurrency & Reconciliation", "C-STGB operates in parallel with existing compliance platforms (Actimize/Falcon), cross-validating false negatives on live transactions.", "#c2410c"),
                ("2. Selective Tier-2 Conformal Routing", r"Ambiguous boundary alerts ($\Gamma(u) = \{0, 1\}$) routed to human investigators with automated GNNExplainer topological subgraph dossiers.", "#b45309"),
                ("3. Active Learning & Memory Bank Feedback", r"Analyst adjudication outcomes fed directly into hard-negative mining memory bank ($\mathcal{B}_{\text{hard}}$) to continuously refine decision boundaries.", "#0f766e"),
                ("4. Peak Load Stress SLA Validation", r"Stress-tested under $31,250\,\text{tx/s}$ burst load on Kubernetes EKS/GKE with HPA ($4 \leftrightarrow 32$ pods), maintaining $P99 < 2.5\,\text{ms}$.", "#15803d")
            ]
        },
        {
            "id": "STAGE III: AUTONOMOUS STP PRODUCTION",
            "sub": "Full Straight-Through Clearance, Asset Holds & Merkle WORM",
            "bg": "#f0fdf4", "border": "#4ade80", "hdr_bg": "#15803d", "hdr_fg": "#ffffff",
            "gate": "GATE 3: FULL PRODUCTION AUTONOMY & STATUTORY COMPLIANCE",
            "gate_bg": "#dcfce7", "gate_border": "#16a34a", "gate_fg": "#14532d",
            "items": [
                ("1. Automated Tier-3 Straight-Through Clearance", "Authorizes >99.33% of transactions for instantaneous Straight-Through Processing (STP) in 0.45 ms, slashing analyst backlogs by >99.4%.", "#15803d"),
                ("2. Automated Tier-1 Real-Time Asset Quarantine", r"Enforces instantaneous programmatic asset freezes on high-confidence illicit nodes ($\Gamma(u) = \{1\}$), halting money laundering in flight.", "#b91c1c"),
                ("3. Autonomous FinCEN Form 111 XML Swarm", "4-agent forensic swarm compiles complete regulatory dossiers in <30 seconds, verified via deterministic AST grammar validators (0% hallucination).", "#0369a1"),
                ("4. Immutable SHA-256 Merkle WORM Ledger", "Anchors cryptographic audit roots into append-only WORM storage, certified under FRE Rule 902(11) satisfying Fed SR 11-7 / SR 21-8 mandates.", "#6d28d9")
            ]
        }
    ]

    for i, stg in enumerate(stages):
        sx = col_x[i]
        
        # Outer Stage Box (sharp rectangle)
        ax.add_patch(patches.Rectangle(
            (sx, c_bot), col_w, c_h,
            facecolor=stg["bg"], edgecolor=stg["border"], linewidth=1.0
        ))
        
        # Header Strip
        ax.add_patch(patches.Rectangle(
            (sx, c_top - 0.038), col_w, 0.038,
            facecolor=stg["hdr_bg"], edgecolor=stg["hdr_bg"], linewidth=0.5
        ))
        ax.text(sx + col_w/2, c_top - 0.019, stg["id"],
                ha='center', va='center', fontsize=6.0, fontweight='bold', color=stg["hdr_fg"])
        
        # Subtitle Box
        ax.add_patch(patches.Rectangle(
            (sx, c_top - 0.070), col_w, 0.032,
            facecolor='#ffffff', edgecolor=stg["border"], linewidth=0.5
        ))
        ax.text(sx + col_w/2, c_top - 0.054, stg["sub"],
                ha='center', va='center', fontsize=5.1, color='#475569', fontweight='bold')

        # 4 Operational Capability Blocks (Stacked)
        y_item_starts = [0.665, 0.490, 0.315, 0.140]
        item_h = 0.165
        for (item_title, item_desc, item_clr), iy in zip(stg["items"], y_item_starts):
            ax.add_patch(patches.Rectangle(
                (sx + 0.006, iy), col_w - 0.012, item_h,
                facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.7
            ))
            # Title
            ax.text(sx + 0.012, iy + item_h - 0.022, item_title,
                    ha='left', va='center', fontsize=5.5, fontweight='bold', color=item_clr)
            # Description lines
            ax.text(sx + 0.012, iy + item_h - 0.052, item_desc[:62],
                    ha='left', va='center', fontsize=5.0, color='#334155')
            ax.text(sx + 0.012, iy + item_h - 0.082, item_desc[62:128],
                    ha='left', va='center', fontsize=5.0, color='#475569')
            if len(item_desc) > 128:
                ax.text(sx + 0.012, iy + item_h - 0.112, item_desc[128:195],
                        ha='left', va='center', fontsize=5.0, color='#64748b')

        # Verification Gate at Bottom of Column
        ax.add_patch(patches.Rectangle(
            (sx + 0.006, c_bot + 0.008), col_w - 0.012, 0.090,
            facecolor=stg["gate_bg"], edgecolor=stg["gate_border"], linewidth=0.9
        ))
        ax.text(sx + col_w/2, c_bot + 0.068, 'VERIFICATION EXIT CRITERIA',
                ha='center', va='center', fontsize=5.0, fontweight='bold', color='#64748b')
        ax.text(sx + col_w/2, c_bot + 0.038, stg["gate"],
                ha='center', va='center', fontsize=5.5, fontweight='bold', color=stg["gate_fg"])

    # Connecting Progression Arrows between Stage Columns
    arr_y = 0.520
    ax.annotate("", xy=(col_x[1], arr_y), xytext=(col_x[0] + col_w, arr_y),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color='#ea580c', lw=1.8))
    ax.annotate("", xy=(col_x[2], arr_y), xytext=(col_x[1] + col_w, arr_y),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color='#15803d', lw=1.8))

    plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    return fig

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    TARGET_DIRS = [
        BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
        BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
        BASE_DIR / "papers" / "EAAI_Submission" / "figures",
        BASE_DIR / "data" / "outputs" / "figures",
        BASE_DIR / "reports" / "figures",
    ]
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    print("Generating Clean Enterprise Deployment Lifecycle (NO Cards)...")
    fig = generate_figure_9_1()
    
    stems = ["fig_26week_roadmap_gantt", "fig_enterprise_deployment_lifecycle"]
    for stem in stems:
        for d in TARGET_DIRS:
            fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.10)
            fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.10)
            print(f"  [SAVED] {d / f'{stem}.pdf'}")
    
    plt.close(fig)
    print("Done generating Figure 9.1!")
