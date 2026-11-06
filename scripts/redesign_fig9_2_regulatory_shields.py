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
    'font.size': 8.0,
    'axes.labelsize': 8.0,
    'axes.titlesize': 9.0,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "data" / "outputs" / "figures",
    BASE_DIR / "reports" / "figures",
]

def generate_fig9_2():
    # Aspect ratio: 1.7384 (11.3 x 6.5 inches)
    fig, ax = plt.subplots(figsize=(11.3, 6.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Outer master canvas card
    bg_canvas = patches.FancyBboxPatch(
        (0.005, 0.005), 0.990, 0.990,
        boxstyle="round,pad=0.015",
        fc="#f8fafc", ec="#cbd5e1", lw=1.2, zorder=0
    )
    ax.add_patch(bg_canvas)

    # Master top header banner (WITHOUT "Figure 9.2: " prefix)
    hdr_box = patches.FancyBboxPatch(
        (0.010, 0.938), 0.980, 0.050,
        boxstyle="round,pad=0.008",
        fc="#0f172a", ec="#1e293b", lw=1.0, zorder=1
    )
    ax.add_patch(hdr_box)

    ax.text(0.018, 0.968, '5-Pillar Global Regulatory Compliance Shield: Statutory Banking Alignment',
            fontsize=9.5, fontweight='bold', color='#ffffff', va='center', zorder=2)
    ax.text(0.018, 0.948, 'Enterprise architectural synthesis aligning C-STGB with FATF, FinCEN BSA, Fed SR 11-7, EU AI Act, and BFIU Circular 26 mandates',
            fontsize=7.2, color='#94a3b8', va='center', zorder=2)

    status_badge = patches.FancyBboxPatch(
        (0.850, 0.944), 0.132, 0.038,
        boxstyle="round,pad=0.005",
        fc="#15803d", ec="#166534", lw=0.8, zorder=2
    )
    ax.add_patch(status_badge)
    ax.text(0.916, 0.963, 'COMPLIANCE AUDIT CERTIFIED',
            fontsize=6.5, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=3)

    # 5 Pillars definitions
    col_w = 0.184
    spacing = 0.0125
    col_x = [0.010 + i * (col_w + spacing) for i in range(5)]
    c_top, c_bot = 0.920, 0.150
    c_h = c_top - c_bot

    pillars = [
        {
            "num": "PILLAR 1", "jurisdiction": "GLOBAL MANDATE",
            "authority": "FATF 40 Rec.",
            "directive": "Rec. 16 (Travel Rule) & Rec. 20",
            "mandate_title": "Continuous Entity Tracing",
            "mandate_desc": "Originator/beneficiary identification and multi-hop peeling chain surveillance across cross-border banking wires.",
            "sol_title": "C-STGB Architectural Solution",
            "sol_items": [
                "• 12-D Mass-Flow Invariants z_inv",
                "• Kirchhoff conservation Φ_flow ≈ 1.0",
                "• Tri-band harmonic attention w(Δt)",
                "• 90-day dormant chain persistence"
            ],
            "cert": "VERIFIED: 100% Flow Traceability",
            "hdr_bg": "#1e3a8a", "badge_bg": "#2563eb", "bg": "#f8fafc", "border": "#93c5fd",
            "cert_bg": "#dbeafe", "cert_fg": "#1e40af"
        },
        {
            "num": "PILLAR 2", "jurisdiction": "UNITED STATES",
            "authority": "FinCEN BSA",
            "directive": "31 U.S.C. 5318(g) & Form 111",
            "mandate_title": "Autonomous SAR Dossiers",
            "mandate_desc": "Mandatory detection of sub-$10k smurfing bursts and automated filing of Suspicious Activity Reports (SAR).",
            "sol_title": "C-STGB Architectural Solution",
            "sol_items": [
                "• Self-exciting Hawkes intensity λ(t)",
                "• Edge-trust filtering (65.9% pruned)",
                "• 4-agent autonomous XML compiler",
                "• Deterministic AST anti-hallucination"
            ],
            "cert": "VERIFIED: 0% Entity Hallucination",
            "hdr_bg": "#065f46", "badge_bg": "#059669", "bg": "#f0fdf4", "border": "#6ee7b7",
            "cert_bg": "#d1fae5", "cert_fg": "#065f46"
        },
        {
            "num": "PILLAR 3", "jurisdiction": "US SUPERVISORY",
            "authority": "Fed SR 11-7",
            "directive": "OCC 2011-12 & SR 21-8 Guidance",
            "mandate_title": "Model Risk Governance",
            "mandate_desc": "Comprehensive model validation, finite-sample risk bounds, drift stability, and tamper-evident audit ledgers.",
            "sol_title": "C-STGB Architectural Solution",
            "sol_items": [
                "• Class-conditional CRC Γ(u) in {0, 1}",
                "• Finite-sample DKW bounds (1 − α ≥ 99%)",
                "• Two-sample KS drift test (p = 0.182)",
                "• Append-only SHA-256 Merkle WORM"
            ],
            "cert": "VERIFIED: Distribution-Free Risk Bound",
            "hdr_bg": "#581c87", "badge_bg": "#7c3aed", "bg": "#faf5ff", "border": "#c084fc",
            "cert_bg": "#f3e8ff", "cert_fg": "#581c87"
        },
        {
            "num": "PILLAR 4", "jurisdiction": "EUROPEAN UNION",
            "authority": "EU 6AMLD / AI Act",
            "directive": "Arts. 13-15 & GDPR Art. 22",
            "mandate_title": "XAI & Corporate Liability",
            "mandate_desc": "Explainability of automated triage, right to human explanation, and strict criminal liability for institutional neglect.",
            "sol_title": "C-STGB Architectural Solution",
            "sol_items": [
                "• Tier-2 selective abstention Γ(u) = {0, 1}",
                "• Human-in-the-loop analyst routing",
                "• GNNExplainer subgraph masks",
                "• Grammar-verified decision lineage"
            ],
            "cert": "VERIFIED: Human-in-the-Loop XAI",
            "hdr_bg": "#9a3412", "badge_bg": "#ea580c", "bg": "#fff7ed", "border": "#fdba74",
            "cert_bg": "#ffedd5", "cert_fg": "#9a3412"
        },
        {
            "num": "PILLAR 5", "jurisdiction": "ASIA / EMERGING",
            "authority": "BFIU Circular 26",
            "directive": "MFS Master Circular & MLPA",
            "mandate_title": "Sub-Second Wire Clearance",
            "mandate_desc": "Real-time Anti-Money Laundering surveillance across high-velocity mobile financial services (MFS) agent networks.",
            "sol_title": "C-STGB Architectural Solution",
            "sol_items": [
                "• Sub-millisecond Fast-Path (0.45 ms)",
                "• Zero-copy PyArrow shared memory IPC",
                "• Embedded DuckDB 2-hop cache (88.4%)",
                "• Peak burst capacity: 31,200 tx/s"
            ],
            "cert": "VERIFIED: 22.2x Faster than SLA",
            "hdr_bg": "#991b1b", "badge_bg": "#dc2626", "bg": "#fef2f2", "border": "#fca5a5",
            "cert_bg": "#fee2e2", "cert_fg": "#991b1b"
        }
    ]

    for idx, p in enumerate(pillars):
        px = col_x[idx]

        # Pillar Outer Card
        card = patches.FancyBboxPatch(
            (px, c_bot), col_w, c_h,
            boxstyle="round,pad=0.008",
            fc=p["bg"], ec=p["border"], lw=1.2, zorder=1
        )
        ax.add_patch(card)

        # Pillar Top Header Box
        hdr = patches.FancyBboxPatch(
            (px, c_top - 0.125), col_w, 0.125,
            boxstyle="round,pad=0.008",
            fc=p["hdr_bg"], ec="none", zorder=2
        )
        ax.add_patch(hdr)

        # Header Pills
        badge = patches.FancyBboxPatch(
            (px + 0.010, c_top - 0.030), col_w - 0.020, 0.020,
            boxstyle="round,pad=0.004",
            fc=p["badge_bg"], ec="none", zorder=3
        )
        ax.add_patch(badge)
        ax.text(px + col_w / 2, c_top - 0.020, f"{p['num']} • {p['jurisdiction']}",
                fontsize=6.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)

        ax.text(px + col_w / 2, c_top - 0.065, p["authority"],
                fontsize=11.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
        ax.text(px + col_w / 2, c_top - 0.100, p["directive"],
                fontsize=6.8, color="#cbd5e1", ha="center", va="center", zorder=4)

        # Statutory Mandate Section
        mandate_box = patches.FancyBboxPatch(
            (px + 0.006, c_top - 0.295), col_w - 0.012, 0.155,
            boxstyle="round,pad=0.005",
            fc="#ffffff", ec="#e2e8f0", lw=0.9, zorder=2
        )
        ax.add_patch(mandate_box)

        ax.text(px + 0.012, c_top - 0.152, "STATUTORY MANDATE",
                fontsize=6.5, fontweight="bold", color="#64748b", va="center", zorder=3)
        ax.text(px + 0.012, c_top - 0.176, p["mandate_title"],
                fontsize=7.8, fontweight="bold", color="#0f172a", va="center", zorder=3)

        # Multi-line mandate description
        words = p["mandate_desc"].split()
        lines = []
        cur_line = []
        for w in words:
            if len(" ".join(cur_line + [w])) <= 25:
                cur_line.append(w)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))

        for l_idx, line in enumerate(lines[:5]):
            ax.text(px + 0.012, c_top - 0.205 - l_idx * 0.020, line,
                    fontsize=6.8, color="#334155", va="center", zorder=3)

        # Solution Section
        sol_box = patches.FancyBboxPatch(
            (px + 0.006, c_bot + 0.055), col_w - 0.012, 0.395,
            boxstyle="round,pad=0.005",
            fc="#ffffff", ec="#cbd5e1", lw=0.9, zorder=2
        )
        ax.add_patch(sol_box)

        ax.text(px + 0.012, c_top - 0.320, p["sol_title"],
                fontsize=6.8, fontweight="bold", color=p["hdr_bg"], va="center", zorder=3)

        for s_idx, item in enumerate(p["sol_items"]):
            y_item = c_top - 0.360 - s_idx * 0.078
            ibox = patches.FancyBboxPatch(
                (px + 0.010, y_item - 0.028), col_w - 0.020, 0.065,
                boxstyle="round,pad=0.004",
                fc="#f8fafc", ec="#e2e8f0", lw=0.7, zorder=3
            )
            ax.add_patch(ibox)
            ax.text(px + 0.014, y_item + 0.004, item,
                    fontsize=6.5, fontweight="semibold", color="#1e293b", va="center", zorder=4)

        # Certification Footer Badge
        cert_badge = patches.FancyBboxPatch(
            (px + 0.006, c_bot + 0.008), col_w - 0.012, 0.038,
            boxstyle="round,pad=0.005",
            fc=p["cert_bg"], ec="none", zorder=2
        )
        ax.add_patch(cert_badge)
        ax.text(px + col_w / 2, c_bot + 0.027, p["cert"],
                fontsize=6.2, fontweight="bold", color=p["cert_fg"], ha="center", va="center", zorder=3)

    # Bottom Synthesis Banner (4 SLA Cards)
    b_bot, b_h = 0.015, 0.120
    sla_w = (0.980 - 3 * 0.012) / 4
    sla_cards = [
        ("GLOBAL JURISDICTIONAL REACH", "5 Regulatory Regimes", "FATF, FinCEN BSA, Fed SR 11-7, EU AI Act, Bangladesh Bank", "#1e3a8a", "#dbeafe"),
        ("MATHEMATICAL GUARANTEES", "Finite-Sample DKW Bound", "1 - α ≥ 99.0% statutory recall with zero hyperparameter tuning", "#065f46", "#d1fae5"),
        ("EXPLAINABLE AI COMPLIANCE", "0% Entity Hallucination", "Deterministic AST grammar verification & GNNExplainer masks", "#581c87", "#f3e8ff"),
        ("COURT-ADMISSIBLE FORENSICS", "FRE Rule 902(11) WORM", "Cryptographic SHA-256 Merkle root timestamped audit trail", "#991b1b", "#fee2e2")
    ]

    for s_idx, (stitle, sstat, ssub, sborder, sbg) in enumerate(sla_cards):
        sx = 0.010 + s_idx * (sla_w + 0.012)
        sbox = patches.FancyBboxPatch(
            (sx, b_bot), sla_w, b_h,
            boxstyle="round,pad=0.006",
            fc=sbg, ec=sborder, lw=1.0, zorder=1
        )
        ax.add_patch(sbox)
        ax.text(sx + sla_w / 2, b_bot + 0.095, stitle,
                fontsize=6.5, fontweight="bold", color="#334155", ha="center", va="center", zorder=2)
        ax.text(sx + sla_w / 2, b_bot + 0.060, sstat,
                fontsize=8.5, fontweight="bold", color=sborder, ha="center", va="center", zorder=2)
        ax.text(sx + sla_w / 2, b_bot + 0.025, ssub,
                fontsize=6.0, color="#475569", ha="center", va="center", zorder=2)

    plt.tight_layout()

    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in [".pdf", ".png"]:
            out_file = d / f"fig_regulatory_shields{ext}"
            plt.savefig(out_file, bbox_inches="tight", pad_inches=0.15)
            print(f"Saved: {out_file}")

    plt.close()

if __name__ == "__main__":
    generate_fig9_2()
