"""
scripts/redesign_fig8_2_sequence_lifeline.py
Publication-grade UML 2.5 Sequence Diagram representing the Real-Time Operational
Execution Lifeline & Microsecond Latency Trace of the C-STGB system.

Conforms strictly to formal UML sequence specifications:
- 6 Formal Lifeline Actors with distinct enterprise roles
- Explicit UML Activation Bars (execution specifications)
- UML Semantic Boundary Frames (Synchronous Real-Time vs Asynchronous Forensics)
- Clear Message Arrows (solid for calls, dashed for returns, dash-dot for async dispatch)
- Millisecond/Microsecond latency timestamps along a left vertical timeline axis
- Strictly NO marketing/consumer card ribbons at the bottom; full vertical lifeline extension
- Preserves canvas aspect ratio (~2.13:1) for seamless thesis integration
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

def generate_figure_8_2():
    # Aspect ratio ~2.13:1 (9.4 x 4.4 inches)
    fig, ax = plt.subplots(figsize=(9.4, 4.40))
    ax.axis('off')
    ax.set_xlim([-0.010, 1.010])
    ax.set_ylim([-0.015, 1.015])

    # 1. Outer Technical Canvas Frame (sharp rectangle)
    ax.add_patch(patches.Rectangle(
        (0.000, 0.000), 1.000, 1.000,
        facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1.0
    ))

    # 2. Top Header Banner
    ax.add_patch(patches.Rectangle(
        (0.005, 0.932), 0.990, 0.062,
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.018, 0.967, 'Real-Time Operational UML Sequence Lifeline & Microsecond Execution Trace',
            ha='left', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')
    ax.text(0.018, 0.945,
            r'Deterministic Pipeline: ISO 20022 Ingress $\rightarrow$ Vectorized Arrow Cache $\rightarrow$ C-STGB Forward Pass $\rightarrow$ Conformal Triage $\rightarrow$ Merkle WORM',
            ha='left', va='center', fontsize=6.3, color='#94a3b8')

    # Top Right SLA Badge
    ax.add_patch(patches.Rectangle(
        (0.772, 0.938), 0.218, 0.050,
        facecolor='#065f46', edgecolor='#10b981', linewidth=0.8
    ))
    ax.text(0.881, 0.963, 'FAST-PATH: 0.45 ms (SLA < 10.0 ms)',
            ha='center', va='center', fontsize=6.2, fontweight='bold', color='#ecfdf5')

    # 3. 6 Lifeline Actors
    actors = [
        {
            "id": 0, "name": "Core Banking (CBS)", "sub": "ISO 20022 Webhook",
            "x": 0.072, "w": 0.114, "hh": 0.068,
            "fg": "#334155", "bg": "#f8fafc", "border": "#64748b", "bar_bg": "#cbd5e1", "bar_border": "#475569",
            "tag": "CLIENT"
        },
        {
            "id": 1, "name": "FastAPI ASGI Gateway", "sub": "Async Event Worker",
            "x": 0.255, "w": 0.118, "hh": 0.068,
            "fg": "#0369a1", "bg": "#f0f9ff", "border": "#0284c7", "bar_bg": "#bae6fd", "bar_border": "#0284c7",
            "tag": "GATEWAY"
        },
        {
            "id": 2, "name": "DuckDB / Arrow Store", "sub": "Zero-Copy L1 LRU Cache",
            "x": 0.438, "w": 0.120, "hh": 0.068,
            "fg": "#0f766e", "bg": "#f0fdfa", "border": "#0d9488", "bar_bg": "#99f6e4", "bar_border": "#0f766e",
            "tag": "CACHE"
        },
        {
            "id": 3, "name": "C-STGB Neural Pod", "sub": "TorchScript GNN on GPU",
            "x": 0.618, "w": 0.116, "hh": 0.068,
            "fg": "#c2410c", "bg": "#fff7ed", "border": "#ea580c", "bar_bg": "#fed7aa", "bar_border": "#c2410c",
            "tag": "INFERENCE"
        },
        {
            "id": 4, "name": "Conformal Arbiter", "sub": "Class-Conditional CRC",
            "x": 0.785, "w": 0.114, "hh": 0.068,
            "fg": "#6d28d9", "bg": "#faf5ff", "border": "#7c3aed", "bar_bg": "#ddd6fe", "bar_border": "#6d28d9",
            "tag": "SAFETY"
        },
        {
            "id": 5, "name": "4-Agent Forensic Swarm", "sub": "Autonomous SAR & WORM",
            "x": 0.932, "w": 0.116, "hh": 0.068,
            "fg": "#15803d", "bg": "#f0fdf4", "border": "#16a34a", "bar_bg": "#bbf7d0", "bar_border": "#15803d",
            "tag": "WORM AUDIT"
        }
    ]

    header_y = 0.852
    lifeline_bottom_y = 0.035

    # 4. UML Grouping Frames
    # Frame 1: Synchronous Fast-Path (<0.45 ms)
    ax.add_patch(patches.Rectangle(
        (0.010, 0.380), 0.855, 0.455,
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=0.9, linestyle='-', alpha=0.55
    ))
    ax.add_patch(patches.Rectangle(
        (0.014, 0.812), 0.285, 0.022,
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(0.018, 0.823, 'alt [SYNCHRONOUS IN-FLIGHT FAST-PATH (SLA < 10.0 ms)]',
            ha='left', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')
    ax.text(0.858, 0.823, 'Total Latency: 0.45 ms (22.2x SLA Safety Margin)',
            ha='right', va='center', fontsize=5.5, fontweight='bold', color='#0369a1')

    # Frame 2: Asynchronous Swarm Investigation & WORM
    ax.add_patch(patches.Rectangle(
        (0.010, 0.038), 0.980, 0.332,
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=0.9, linestyle='--', alpha=0.60
    ))
    ax.add_patch(patches.Rectangle(
        (0.014, 0.346), 0.380, 0.022,
        facecolor='#ca8a04', edgecolor='#ca8a04', linewidth=0.5
    ))
    ax.text(0.018, 0.357, 'par [ASYNCHRONOUS TIER-1/2 SWARM FORENSICS & MERKLE WORM VAULT]',
            ha='left', va='center', fontsize=5.6, fontweight='bold', color='#ffffff')
    ax.text(0.982, 0.357, 'Triggered on Tier-1 Quarantine (0.18%) & Tier-2 Human Review (0.49%) | Non-blocking Queue',
            ha='right', va='center', fontsize=5.2, fontweight='bold', color='#854d0e')

    # Draw Actor Headers and Vertical Lifeline Guides
    for act in actors:
        lx = act["x"]
        w = act["w"]
        hh = act["hh"]
        
        # Vertical Lifeline
        ax.plot([lx, lx], [lifeline_bottom_y, header_y], color='#94a3b8', linestyle=':', lw=0.9, alpha=0.7)
        
        # Header Box
        ax.add_patch(patches.Rectangle(
            (lx - w/2, header_y), w, hh,
            facecolor=act["bg"], edgecolor=act["border"], linewidth=1.0, zorder=3
        ))
        # Top color tag strip
        ax.add_patch(patches.Rectangle(
            (lx - w/2, header_y + hh - 0.007), w, 0.007,
            facecolor=act["border"], edgecolor=act["border"], linewidth=0.2, zorder=4
        ))
        ax.text(lx, header_y + hh - 0.024, act["name"],
                ha='center', va='center', fontsize=6.3, fontweight='bold', color='#0f172a', zorder=5)
        ax.text(lx, header_y + 0.022, act["sub"],
                ha='center', va='center', fontsize=5.1, color='#475569', zorder=5)
        ax.text(lx, header_y + 0.007, f"«{act['tag']}»",
                ha='center', va='center', fontsize=4.6, fontweight='bold', color=act["fg"], zorder=5)

    # 5. UML Activation Bars (Execution Specifications)
    act_w = 0.013
    activations = [
        # Actor 0: CBS Webhook active during request & clearance
        (0, 0.400, 0.785),
        # Actor 1: Gateway active for fast path + async dispatch
        (1, 0.220, 0.775),
        # Actor 2: DuckDB / Arrow cache lookup
        (2, 0.620, 0.730),
        # Actor 3: C-STGB neural inference
        (3, 0.505, 0.605),
        # Actor 4: Conformal arbiter check
        (4, 0.415, 0.490),
        # Actor 5: Swarm agent execution & WORM seal
        (5, 0.060, 0.280),
    ]

    for a_id, y_bot, y_top in activations:
        act = actors[a_id]
        ax.add_patch(patches.Rectangle(
            (act["x"] - act_w/2, y_bot), act_w, y_top - y_bot,
            facecolor=act["bar_bg"], edgecolor=act["bar_border"], linewidth=0.8, zorder=3
        ))

    # 6. UML Sequence Messages
    messages = [
        # 1. Ingress Webhook
        {
            "step": "1", "from": 0, "to": 1, "y": 0.770, "is_return": False, "is_async": False,
            "title": "POST /v1/transactions/score {pacs.008 XML / JSON-LD}", "time": "t = 0.00 ms",
            "detail": "Core Banking Wire Event Ingress (mTLS 1.3)",
            "color": "#0284c7"
        },
        # 2. Subgraph Fetch
        {
            "step": "2", "from": 1, "to": 2, "y": 0.715, "is_return": False, "is_async": False,
            "title": "Zero-Copy 2-Hop Ego-Graph Slice & Invariant Feature Extraction", "time": "t = +0.05 ms",
            "detail": "DuckDB Arrow IPC Memory Map Query",
            "color": "#0d9488"
        },
        # 3. Return Subgraph
        {
            "step": "3", "from": 2, "to": 1, "y": 0.640, "is_return": True, "is_async": False,
            "title": r"Return Ego-Graph Tensor Batch $\mathbf{X}_u \in \mathbb{R}^{B \times 12}$ (88.4% Cache Hit)", "time": "t = +0.15 ms",
            "detail": r"Vectorized Apache Arrow Shared Memory Segment ($\Delta t = 0.10\,\text{ms}$)",
            "color": "#0d9488"
        },
        # 4. Neural Forward Pass
        {
            "step": "4", "from": 1, "to": 3, "y": 0.585, "is_return": False, "is_async": False,
            "title": r"C-STGB Forward Pass: $\hat{y}_u = f_\theta(\mathcal{G}_u^{(t)}, \mathbf{z}_{\mathrm{inv}})$", "time": "t = +0.18 ms",
            "detail": "Continuous Fourier Convolution on TensorRT GPU",
            "color": "#c2410c"
        },
        # 5. Return Neural Score
        {
            "step": "5", "from": 3, "to": 1, "y": 0.520, "is_return": True, "is_async": False,
            "title": r"Return Posterior Score $\hat{p}_u \in [0, 1]$ & Invariant Embedding", "time": "t = +0.28 ms",
            "detail": r"TorchScript JIT Inference Latency ($\Delta t = 0.10\,\text{ms}$)",
            "color": "#c2410c"
        },
        # 6. Conformal Calibration Check
        {
            "step": "6", "from": 1, "to": 4, "y": 0.465, "is_return": False, "is_async": False,
            "title": r"Class-Conditional Conformal Calibration Check: $S_i \leq \hat{q}^{(y)}$", "time": "t = +0.30 ms",
            "detail": "Distribution-Free Dual-Quantile Evaluation (CRC Guarantee)",
            "color": "#6d28d9"
        },
        # 7. Return Triage Verdict
        {
            "step": "7", "from": 4, "to": 1, "y": 0.415, "is_return": True, "is_async": False,
            "title": r"Return Triage Verdict: Tier-3 STP (99.33%) / Tier-2 Escalate (0.49%) / Tier-1 Quarantine (0.18%)", "time": "t = +0.32 ms",
            "detail": r"Scalar In-Memory Table Lookup ($\Delta t = 0.02\,\text{ms}$)",
            "color": "#6d28d9"
        },
        # 8. Synchronous SLA Clearance Response
        {
            "step": "8", "from": 1, "to": 0, "y": 0.365, "is_return": True, "is_async": False,
            "title": "HTTP 200 OK: {status: 'CLEARED_STP', latency: 0.45 ms}", "time": "t = +0.45 ms",
            "detail": "Straight-Through Clearance Returned to CBS (22.2x SLA Headroom)",
            "color": "#059669"
        },
        # 9. Asynchronous Swarm Dispatch
        {
            "step": "9", "from": 1, "to": 5, "y": 0.275, "is_return": False, "is_async": True,
            "title": "«async» Kafka Non-Blocking Queue: Dispatch Flagged Alert to 4-Agent Forensic Swarm", "time": "t = +1.10 ms",
            "detail": "Autonomous Lead Coordinator -> Topology Specialist -> Legal Drafter -> Rule Verifier",
            "color": "#b45309"
        },
        # 10. Autonomous Forensic Synthesis & Merkle WORM
        {
            "step": "10", "from": 5, "to": 5, "y": 0.175, "is_return": False, "is_async": True,
            "title": "Multi-Agent SAR Compilation: Context-Free AST Grammar Verification & FinCEN XML Dossier", "time": "t = +24.8 s",
            "detail": "Anchor Cryptographic SHA-256 Merkle Root to WORM Vault (FRE 902(11) Certified)",
            "color": "#15803d"
        },
        # 11. Final Merkle Audit Trail Receipt
        {
            "step": "11", "from": 5, "to": 1, "y": 0.085, "is_return": True, "is_async": True,
            "title": "Return SAR Audit Receipt: {receipt_hash: 9f86d081...00a08, worm_vault_status: 'COMMITTED'}", "time": "t = +25.1 s",
            "detail": "Immutable Supervisory Audit Ledger Entry Archived to Tamper-Proof Storage",
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
            loop_h = 0.038
            
            ax.plot([x_base, x_base + loop_w, x_base + loop_w, x_base],
                    [ym, ym, ym - loop_h, ym - loop_h],
                    color=m_clr, lw=1.2, linestyle='-', zorder=4)
            ax.annotate("", xy=(x_base, ym - loop_h), xytext=(x_base + 0.008, ym - loop_h),
                        arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color=m_clr, lw=1.2), zorder=4)
            
            # Text placed inside Frame 2 to the left of the loop
            ax.text(x_base - 0.015, ym + 0.004, f"{msg['step']}. {msg['title']}  [{msg['time']}]",
                    ha='right', va='bottom', fontsize=5.6, fontweight='bold', color=m_clr)
            ax.text(x_base - 0.015, ym - 0.006, msg["detail"],
                    ha='right', va='top', fontsize=4.9, color='#475569')

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
            ax.text(mid_x, ym + 0.004, f"{msg['step']}. {msg['title']}  [{msg['time']}]",
                    ha='center', va='bottom', fontsize=5.5, fontweight='bold', color=m_clr, zorder=5)
            # Secondary detail text
            ax.text(mid_x, ym - 0.005, msg["detail"],
                    ha='center', va='top', fontsize=4.9, color='#475569', zorder=5)

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

    print("Generating Redesigned UML Sequence Lifeline (NO Cards)...")
    fig = generate_figure_8_2()
    
    stem = "fig8_2_uml_sequence_lifeline"
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.10)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.10)
        print(f"  [SAVED] {d / f'{stem}.pdf'}")
    
    plt.close(fig)
    print("Done generating Figure 8.2!")
