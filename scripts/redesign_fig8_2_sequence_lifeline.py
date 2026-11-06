"""
scripts/redesign_fig8_2_sequence_lifeline.py
Dedicated publication-grade redesign for Real-Time Operational UML Sequence Lifeline & Microsecond Execution Trace.

Conforms to standard UML 2.5 sequence specifications:
- 6 Lifeline Actors with distinct enterprise roles and color signatures
- Explicit UML Activation Bars (execution specifications)
- UML Semantic Boundary Frames (Synchronous Real-Time vs. Asynchronous Forensics)
- Clear Message Arrows (solid for calls, dashed for returns, dash-dot for async dispatch)
- Millisecond/Microsecond latency timestamps with statutory SLA validation
- Bottom 4-card enterprise SLA & compliance summary ribbon
- Strictly preserved canvas aspect ratio (~2.13:1) ensuring zero page drift in the thesis
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

def generate_figure_8_2():
    # Figure size chosen so that after tight bbox cropping, aspect ratio is ~2.13:1
    fig, ax = plt.subplots(figsize=(9.4, 4.30))
    ax.axis('off')
    ax.set_xlim([-0.010, 1.010])
    ax.set_ylim([-0.015, 1.015])

    # 1. Outer Container Card
    ax.add_patch(patches.FancyBboxPatch(
        (0.000, 0.000), 1.000, 1.000,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
    ))

    # 2. Top Title Banner
    ax.add_patch(patches.FancyBboxPatch(
        (0.006, 0.926), 0.988, 0.066,
        boxstyle='round,pad=0.003,rounding_size=0.005',
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.018, 0.966, 'Real-Time Operational UML Sequence Lifeline & Microsecond Execution Trace',
            ha='left', va='center', fontsize=8.6, fontweight='bold', color='#ffffff')
    ax.text(0.018, 0.941,
            r'Deterministic Microservice Pipeline: ISO 20022 Ingress $\rightarrow$ Vectorized LRU Cache $\rightarrow$ C-STGB Forward Pass $\rightarrow$ Conformal Triage $\rightarrow$ Merkle WORM',
            ha='left', va='center', fontsize=6.2, color='#94a3b8')

    # Top Right SLA Pill
    ax.add_patch(patches.FancyBboxPatch(
        (0.772, 0.933), 0.216, 0.052,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#065f46', edgecolor='#10b981', linewidth=0.7
    ))
    ax.text(0.880, 0.959, 'FAST-PATH: 0.45 ms (SLA < 10.0 ms MET)',
            ha='center', va='center', fontsize=6.0, fontweight='bold', color='#ecfdf5')

    # 3. 6 Lifeline Actors
    actors = [
        {
            "id": 0, "name": "Core Banking (CBS)", "sub": "ISO 20022 Payment Webhook",
            "x": 0.068, "w": 0.112, "hh": 0.076,
            "fg": "#334155", "bg": "#f8fafc", "border": "#64748b", "bar_bg": "#cbd5e1", "bar_border": "#475569",
            "tag": "CLIENT"
        },
        {
            "id": 1, "name": "FastAPI ASGI Gateway", "sub": "Distributed Event Worker",
            "x": 0.272, "w": 0.120, "hh": 0.076,
            "fg": "#0369a1", "bg": "#f0f9ff", "border": "#0284c7", "bar_bg": "#bae6fd", "bar_border": "#0284c7",
            "tag": "GATEWAY"
        },
        {
            "id": 2, "name": "DuckDB / Arrow Store", "sub": "Zero-Copy L1 Subgraph LRU",
            "x": 0.480, "w": 0.120, "hh": 0.076,
            "fg": "#0f766e", "bg": "#f0fdfa", "border": "#0d9488", "bar_bg": "#99f6e4", "bar_border": "#0f766e",
            "tag": "CACHE"
        },
        {
            "id": 3, "name": "C-STGB Neural Pod", "sub": "TorchScript GNN on GPU",
            "x": 0.655, "w": 0.114, "hh": 0.076,
            "fg": "#c2410c", "bg": "#fff7ed", "border": "#ea580c", "bar_bg": "#fed7aa", "bar_border": "#c2410c",
            "tag": "INFERENCE"
        },
        {
            "id": 4, "name": "Conformal Arbiter", "sub": "3-Tier Class-Conditional CRC",
            "x": 0.795, "w": 0.114, "hh": 0.076,
            "fg": "#6d28d9", "bg": "#faf5ff", "border": "#7c3aed", "bar_bg": "#ddd6fe", "bar_border": "#6d28d9",
            "tag": "SAFETY"
        },
        {
            "id": 5, "name": "4-Agent Forensic Swarm", "sub": "Autonomous SAR & Merkle Vault",
            "x": 0.932, "w": 0.118, "hh": 0.076,
            "fg": "#15803d", "bg": "#f0fdf4", "border": "#16a34a", "bar_bg": "#bbf7d0", "bar_border": "#15803d",
            "tag": "WORM AUDIT"
        }
    ]

    header_y = 0.834
    lifeline_bottom_y = 0.158

    # 4. UML Grouping Frames
    # Frame 1: Synchronous Fast-Path
    ax.add_patch(patches.FancyBboxPatch(
        (0.010, 0.312), 0.855, 0.512,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=0.8, linestyle='-', alpha=0.55
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (0.014, 0.800), 0.260, 0.022,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(0.018, 0.811, 'alt: SYNCHRONOUS FAST-PATH (SLA < 10.0 ms)',
            ha='left', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')
    ax.text(0.858, 0.811, 'Total Latency: 0.45 ms (22.2x SLA Safety Margin)',
            ha='right', va='center', fontsize=5.4, fontweight='bold', color='#0369a1')

    # Frame 2: Asynchronous Swarm Investigation
    ax.add_patch(patches.FancyBboxPatch(
        (0.010, 0.160), 0.980, 0.144,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=0.8, linestyle='--', alpha=0.60
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (0.014, 0.280), 0.330, 0.022,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#ca8a04', edgecolor='#ca8a04', linewidth=0.5
    ))
    ax.text(0.018, 0.291, 'par: ASYNCHRONOUS TIER-1/2 SWARM FORENSICS & MERKLE WORM',
            ha='left', va='center', fontsize=5.6, fontweight='bold', color='#ffffff')
    ax.text(0.982, 0.291, 'Non-blocking background queue | Triggered on flagged alerts (0.18% Tier-1, 0.50% Tier-2)',
            ha='right', va='center', fontsize=5.2, fontweight='bold', color='#854d0e')

    # Draw Actor Headers and Lifelines
    for act in actors:
        lx = act["x"]
        w = act["w"]
        hh = act["hh"]
        
        # Vertical Lifeline Guide
        ax.plot([lx, lx], [lifeline_bottom_y, header_y], color='#94a3b8', linestyle=':', lw=0.9, alpha=0.7)
        
        # Header Box
        ax.add_patch(patches.FancyBboxPatch(
            (lx - w/2, header_y), w, hh,
            boxstyle='round,pad=0.002,rounding_size=0.004',
            facecolor=act["bg"], edgecolor=act["border"], linewidth=0.9
        ))
        
        # Role Badge
        ax.add_patch(patches.FancyBboxPatch(
            (lx - 0.034, header_y + hh - 0.017), 0.068, 0.015,
            boxstyle='round,pad=0.001,rounding_size=0.002',
            facecolor=act["border"], edgecolor=act["border"], linewidth=0.5
        ))
        ax.text(lx, header_y + hh - 0.0095, act["tag"], ha='center', va='center',
                fontsize=4.6, fontweight='bold', color='#ffffff')
        
        # Actor Name & Subtitle
        ax.text(lx, header_y + 0.038, act["name"], ha='center', va='center',
                fontsize=5.8, fontweight='bold', color=act["fg"])
        ax.text(lx, header_y + 0.010, act["sub"], ha='center', va='center',
                fontsize=4.7, color='#64748b')

    # 5. UML Activation Bars
    act_w = 0.014
    activations = [
        (0, 0.785, 0.745),  # CBS sending POST
        (0, 0.355, 0.315),  # CBS receiving HTTP 200 OK
        (1, 0.765, 0.335),  # FastAPI active continuously during sync transaction
        (1, 0.265, 0.235),  # FastAPI dispatching async swarm task
        (2, 0.725, 0.645),  # DuckDB active during L1 ego-graph query
        (3, 0.605, 0.525),  # C-STGB Neural Pod active during forward pass
        (4, 0.485, 0.405),  # Conformal Arbiter active during CRC calibration check
        (5, 0.255, 0.170),  # 4-Agent Swarm active during background investigation & WORM seal
    ]

    for a_idx, y_top, y_bot in activations:
        act_info = actors[a_idx]
        ax.add_patch(patches.FancyBboxPatch(
            (act_info["x"] - act_w/2, y_bot), act_w, y_top - y_bot,
            boxstyle='round,pad=0.0005,rounding_size=0.002',
            facecolor=act_info["bar_bg"], edgecolor=act_info["bar_border"], linewidth=0.8, zorder=3
        ))

    # 6. Messages and Timestamps
    messages = [
        # 1. Webhook Ingress
        {
            "step": "1", "from": 0, "to": 1, "y": 0.755, "is_return": False, "is_async": False,
            "title": "POST /v1/transactions/stream", "time": "t = 0.00 ms",
            "detail": "ISO 20022 Webhook Ingress (mTLS 1.3)",
            "color": "#0284c7"
        },
        # 2. Ingest & Ego-Graph Fetch
        {
            "step": "2", "from": 1, "to": 2, "y": 0.695, "is_return": False, "is_async": False,
            "title": "Zero-Copy Ingest & Subgraph Fetch", "time": "t = +0.05 ms",
            "detail": "PyArrow Buffer & DuckDB LRU Lookup",
            "color": "#0f766e"
        },
        # 3. Return Ego-Graph & Invariants
        {
            "step": "3", "from": 2, "to": 1, "y": 0.635, "is_return": True, "is_async": False,
            "title": r"Return 2-Hop Ego-Graph $\mathcal{G}_t^{(K)}$ + 12-D Flow Invariants", "time": "t = +0.16 ms",
            "detail": r"88.4% LRU L1 Cache Hit Rate ($\Delta t = 0.11\,\text{ms}$)",
            "color": "#0f766e"
        },
        # 4. Neural Forward Pass
        {
            "step": "4", "from": 1, "to": 3, "y": 0.575, "is_return": False, "is_async": False,
            "title": "TorchScript GNN Forward Pass (Tri-Band Harmonic + Edge Gate)", "time": "t = +0.18 ms",
            "detail": "Spatio-Temporal Continuous Fourier Convolution on GPU",
            "color": "#c2410c"
        },
        # 5. Return Score & Embedding
        {
            "step": "5", "from": 3, "to": 1, "y": 0.515, "is_return": True, "is_async": False,
            "title": r"Return Posterior Score $p_u \in [0, 1]$ & Invariant Embedding", "time": "t = +0.28 ms",
            "detail": r"Inference Forward Execution Latency ($\Delta t = 0.10\,\text{ms}$)",
            "color": "#c2410c"
        },
        # 6. Conformal Calibration Check
        {
            "step": "6", "from": 1, "to": 4, "y": 0.455, "is_return": False, "is_async": False,
            "title": r"Class-Conditional Conformal Calibration Check $s_u \leq \hat{q}^{(y)}$", "time": "t = +0.30 ms",
            "detail": "Dual-Quantile Non-Conformity Evaluation (CRC Guarantee)",
            "color": "#6d28d9"
        },
        # 7. Return Triage Verdict
        {
            "step": "7", "from": 4, "to": 1, "y": 0.395, "is_return": True, "is_async": False,
            "title": "Return Triage Verdict: Tier-3 STP (99.32%) / Tier-1 Quarantine (0.18%)", "time": "t = +0.32 ms",
            "detail": r"Scalar In-Memory Table Lookup ($\Delta t = 0.02\,\text{ms}$)",
            "color": "#6d28d9"
        },
        # 8. Synchronous SLA Clearance Response
        {
            "step": "8", "from": 1, "to": 0, "y": 0.335, "is_return": True, "is_async": False,
            "title": "HTTP 200 OK: {status: 'CLEARED_STP', elapsed: 0.45 ms}", "time": "t = +0.45 ms",
            "detail": "Straight-Through Clearance Returned to CBS (SLA Met)",
            "color": "#059669"
        },
        # 9. Asynchronous Swarm Dispatch
        {
            "step": "9", "from": 1, "to": 5, "y": 0.245, "is_return": False, "is_async": True,
            "title": "<<async>> Non-Blocking Queue: Dispatch Flagged Case to 4-Agent Swarm", "time": "t = +1.10 ms",
            "detail": "Autonomous Investigator -> Auditor -> SAR Typology Compilation Pipeline",
            "color": "#b45309"
        },
        # 10. SAR Assembly & Merkle Seal
        {
            "step": "10", "from": 5, "to": 5, "y": 0.182, "is_return": False, "is_async": True,
            "title": "Synthesize FinCEN SAR XML & Anchor SHA-256 Merkle Root to WORM Vault", "time": "t = +24.8 s",
            "detail": "Autonomous Dossier Assembly & Immutable Audit Trail (FRE 902(11) Certified)",
            "color": "#15803d"
        }
    ]

    for msg in messages:
        f_idx = msg["from"]
        t_idx = msg["to"]
        ym = msg["y"]
        x_from = actors[f_idx]["x"]
        x_to = actors[t_idx]["x"]
        m_clr = msg["color"]
        
        if f_idx == t_idx:
            # Self-call loop on actor 5
            x_base = x_from + act_w/2
            loop_w = 0.032
            loop_h = 0.022
            
            ax.plot([x_base, x_base + loop_w, x_base + loop_w, x_base],
                    [ym, ym, ym - loop_h, ym - loop_h],
                    color=m_clr, lw=1.2, linestyle='-', zorder=4)
            ax.annotate("", xy=(x_base, ym - loop_h), xytext=(x_base + 0.008, ym - loop_h),
                        arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color=m_clr, lw=1.2), zorder=4)
            
            # Text placed inside Frame 2 to the left of the loop
            ax.text(x_base - 0.015, ym + 0.003, f"{msg['step']}. {msg['title']}  [{msg['time']}]",
                    ha='right', va='bottom', fontsize=5.5, fontweight='bold', color=m_clr)
            ax.text(x_base - 0.015, ym - 0.005, msg["detail"],
                    ha='right', va='top', fontsize=4.8, color='#475569')

        else:
            if x_to > x_from:
                x_start = x_from + act_w/2
                x_end = x_to - act_w/2
            else:
                x_start = x_from - act_w/2
                x_end = x_to + act_w/2
            
            ls = '--' if msg["is_return"] else ('-.' if msg["is_async"] else '-')
            arr_style = "->,head_width=0.20,head_length=0.28"
            
            ax.annotate("", xy=(x_end, ym), xytext=(x_start, ym),
                        arrowprops=dict(arrowstyle=arr_style, color=m_clr, lw=1.2, linestyle=ls), zorder=4)
            
            mid_x = (x_start + x_end) / 2
            
            # Primary label with step and time tag
            ax.text(mid_x, ym + 0.003, f"{msg['step']}. {msg['title']}  [{msg['time']}]",
                    ha='center', va='bottom', fontsize=5.4, fontweight='bold', color=m_clr, zorder=5)
            # Secondary detail text
            ax.text(mid_x, ym - 0.004, msg["detail"],
                    ha='center', va='top', fontsize=4.8, color='#475569', zorder=5)

    # 7. Bottom SLA & Production Metric Strip (4 Cards)
    kpis = [
        {
            "x": 0.010, "w": 0.236,
            "title": "CORE BANKING SLA HEADROOM",
            "metric": "0.45 ms P50 | 0.82 ms P99",
            "sub": "22.2x Faster than 10.0 ms Statutory Limit",
            "bg": "#f0f9ff", "border": "#38bdf8", "fg": "#0369a1", "bar": "#0284c7"
        },
        {
            "x": 0.258, "w": 0.236,
            "title": "AUTOMATED TRIAGE COVERAGE",
            "metric": "99.32% STP Clearance",
            "sub": "0.18% Quarantined | 0.50% Escalated",
            "bg": "#f0fdf4", "border": "#4ade80", "fg": "#15803d", "bar": "#16a34a"
        },
        {
            "x": 0.506, "w": 0.236,
            "title": "MULTI-AGENT INVESTIGATION",
            "metric": "24.8 s Forensic Synthesis",
            "sub": "Autonomous FinCEN SAR XML Assembly",
            "bg": "#fefce8", "border": "#facc15", "fg": "#a16207", "bar": "#ca8a04"
        },
        {
            "x": 0.754, "w": 0.236,
            "title": "LEGAL TAMPER-PROOF AUDIT",
            "metric": "SHA-256 Merkle WORM",
            "sub": "FRE Rule 902(11) Self-Authenticating Record",
            "bg": "#faf5ff", "border": "#c084fc", "fg": "#6d28d9", "bar": "#7c3aed"
        }
    ]

    card_y = 0.014
    card_h = 0.128

    for kpi in kpis:
        kx = kpi["x"]
        kw = kpi["w"]
        
        ax.add_patch(patches.FancyBboxPatch(
            (kx, card_y), kw, card_h,
            boxstyle='round,pad=0.002,rounding_size=0.004',
            facecolor=kpi["bg"], edgecolor=kpi["border"], linewidth=0.8
        ))
        ax.add_patch(patches.FancyBboxPatch(
            (kx + 0.004, card_y + card_h - 0.010), kw - 0.008, 0.006,
            boxstyle='round,pad=0.0005,rounding_size=0.001',
            facecolor=kpi["bar"], edgecolor=kpi["bar"], linewidth=0.3
        ))
        ax.text(kx + kw/2, card_y + card_h - 0.024, kpi["title"],
                ha='center', va='center', fontsize=5.2, fontweight='bold', color=kpi["fg"])
        ax.text(kx + kw/2, card_y + card_h - 0.058, kpi["metric"],
                ha='center', va='center', fontsize=7.2, fontweight='bold', color='#0f172a')
        ax.text(kx + kw/2, card_y + 0.026, kpi["sub"],
                ha='center', va='center', fontsize=5.1, color='#475569')

    plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    return fig

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
    eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
    eaai_sub_dir = BASE_DIR / "papers" / "EAAI_Submission" / "figures"
    data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"
    reports_fig_dir = BASE_DIR / "reports" / "figures"

    TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, eaai_sub_dir, data_fig_dir, reports_fig_dir]
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    print("Generating Redesigned Real-Time Operational UML Sequence Lifeline...")
    fig = generate_figure_8_2()
    
    stem = "fig8_2_uml_sequence_lifeline"
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.15)
        print(f"  [SAVED] {d / f'{stem}.pdf'}")
    
    plt.close(fig)
    print("Done generating Figure 8.2!")
