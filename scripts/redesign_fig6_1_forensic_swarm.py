"""
scripts/redesign_fig6_1_forensic_swarm.py
Redesign of Figure 6.1: Multi-Agent Forensic Reasoning and Dual-Governance Pipeline.
Strictly NO cards: pure technical engineering block diagram with formal UML/system connectors.
Standardizes 4 agent names:
1. Lead Forensic Coordinator
2. Subgraph Topology Specialist
3. Legal SAR Drafter
4. Compliance Rule Verifier
Saves to fig_forensic_swarm.pdf/png and fig20_multi_agent_forensic_swarm.pdf/png across all 5 directories.
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
    'font.size': 8.0,
    'axes.labelsize': 8.0,
    'axes.titlesize': 8.5,
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
    BASE_DIR / "data" / "outputs" / "figures"
]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def generate_figure():
    fig, ax = plt.subplots(figsize=(10.2, 4.8), dpi=300)
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 48)
    ax.axis("off")

    # Background canvas
    ax.add_patch(patches.Rectangle((0, 0), 102, 48, facecolor="#ffffff", edgecolor="none"))

    # 4 Major Engineering Stage Columns
    stages = [
        {"x": 1.0,  "w": 20.0, "title": "PHASE 1: INGESTION & CONTEXT", "sub": "Streaming Triage & Cache Hydration", "bg": "#f8fafc", "border": "#94a3b8"},
        {"x": 22.0, "w": 31.0, "title": "PHASE 2: AUTONOMOUS FORENSIC SWARM", "sub": "Topological Attribution & Drafting", "bg": "#f0fdf4", "border": "#86efac"},
        {"x": 54.0, "w": 23.0, "title": "PHASE 3: AST COMPILER GATE", "sub": "Deterministic Anti-Hallucination", "bg": "#eff6ff", "border": "#93c5fd"},
        {"x": 78.0, "w": 23.0, "title": "PHASE 4: DUAL-GOVERNANCE VAULT", "sub": "Four-Eyes Audit & Merkle Proof", "bg": "#faf5ff", "border": "#d8b4fe"}
    ]

    for s in stages:
        # Phase boundary container (sharp rectangle, engineering style)
        rect = patches.Rectangle((s["x"], 1.5), s["w"], 45.0, facecolor=s["bg"], edgecolor=s["border"], linewidth=1.0, linestyle="--")
        ax.add_patch(rect)
        # Phase Header Banner
        header = patches.Rectangle((s["x"], 43.2), s["w"], 3.3, facecolor="#1e293b", edgecolor=s["border"], linewidth=0.8)
        ax.add_patch(header)
        ax.text(s["x"] + s["w"]/2.0, 44.8, s["title"], ha="center", va="center", fontsize=7.2, fontweight="bold", color="#f8fafc")
        ax.text(s["x"] + s["w"]/2.0, 42.0, s["sub"], ha="center", va="center", fontsize=5.8, fontweight="bold", color="#475569")

    # =========================================================================
    # PHASE 1: INGESTION & LEAD FORENSIC COORDINATOR
    # =========================================================================
    # Alert Box
    ax.add_patch(patches.Rectangle((2.5, 30.0), 17.0, 8.5, facecolor="#ffffff", edgecolor="#dc2626", linewidth=1.2))
    ax.text(11.0, 36.2, "CRC Conformal Alert", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#dc2626")
    ax.text(11.0, 33.5, r"$\Gamma(u) \in \{\{1\}, \{0,1\}\}$" + "\nNon-conformity score $S(u)$", ha="center", va="center", fontsize=6.2, color="#1e293b")
    ax.text(11.0, 31.0, "Trigger: P99 SLA < 15 min", ha="center", va="center", fontsize=5.5, color="#64748b")

    # Connecting Arrow
    ax.annotate("", xy=(11.0, 22.5), xytext=(11.0, 30.0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#0f172a"))

    # Lead Forensic Coordinator Box
    ax.add_patch(patches.Rectangle((2.5, 8.0), 17.0, 14.5, facecolor="#ffffff", edgecolor="#1e40af", linewidth=1.4))
    # Header bar
    ax.add_patch(patches.Rectangle((2.5, 18.8), 17.0, 3.7, facecolor="#1e40af", edgecolor="none"))
    ax.text(11.0, 20.6, "Lead Forensic Coordinator", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(3.5, 13.5, "• Context Hydration:\n  DuckDB 2-hop $\\mathcal{G}_{\\mathrm{ego}}$\n• Canonical Invariants:\n  $\\mathbf{z}_{\\mathrm{inv}}(u,t) \\in \\mathbb{R}^{12}$\n• Swarm Task Dispatcher\n• SLA Clock & Watchdog",
            ha="left", va="center", fontsize=5.9, color="#0f172a")

    # Arrow from Phase 1 to Phase 2
    ax.annotate("", xy=(23.5, 34.0), xytext=(19.5, 17.0),
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#1e40af", connectionstyle="arc3,rad=-0.15"))
    ax.text(20.5, 26.5, "Dispatch Task\n& Evidence", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#1e40af",
            bbox=dict(boxstyle="square,pad=0.15", facecolor="#ffffff", edgecolor="#93c5fd", lw=0.6))

    # =========================================================================
    # PHASE 2: AUTONOMOUS FORENSIC SWARM (3 SPECIALISTS)
    # =========================================================================
    # Agent 1: Subgraph Topology Specialist
    ax.add_patch(patches.Rectangle((23.5, 27.5), 28.0, 12.5, facecolor="#ffffff", edgecolor="#0f766e", linewidth=1.2))
    ax.add_patch(patches.Rectangle((23.5, 36.8), 28.0, 3.2, facecolor="#0f766e", edgecolor="none"))
    ax.text(37.5, 38.4, "Subgraph Topology Specialist", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(24.5, 32.2, "• GNNExplainer Masking: $M_e \\geq 0.65$ (Mutual Info $\\max$)\n• Flow Conservation: $\\Phi_{\\mathrm{flow}} = \\sum A_{\\mathrm{in}} / \\sum A_{\\mathrm{out}}$\n• Typology Motifs: Smurfing / Peeling / Circular Wash\n• Output: Causal Attribution Subgraph $\\mathcal{G}_{\\mathrm{sub}} = (\\mathcal{V}_{\\mathrm{sub}}, \\mathcal{E}_{\\mathrm{sub}})$",
            ha="left", va="center", fontsize=5.9, color="#0f172a")

    # Arrow from Subgraph Specialist to Legal SAR Drafter
    ax.annotate("", xy=(37.5, 25.0), xytext=(37.5, 27.5),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#0f766e"))
    ax.text(38.2, 26.2, "Causal Facts $\\mathcal{G}_{\\mathrm{sub}}$", ha="left", va="center", fontsize=5.5, fontweight="bold", color="#0f766e")

    # Agent 2: Legal SAR Drafter
    ax.add_patch(patches.Rectangle((23.5, 14.5), 28.0, 10.5, facecolor="#ffffff", edgecolor="#c2410c", linewidth=1.2))
    ax.add_patch(patches.Rectangle((23.5, 21.8), 28.0, 3.2, facecolor="#c2410c", edgecolor="none"))
    ax.text(37.5, 23.4, "Legal SAR Drafter", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(24.5, 18.0, "• Deterministic Decoding: Temperature $\\tau = 0.0$, top-$p = 1.0$\n• FinCEN Form 111 XML Structured Narrative Synthesis\n• Grounds of Suspicion Narrative grounded in $\\mathcal{G}_{\\mathrm{sub}}$\n• Strict Prompt Constraints: Zero extrapolative claims",
            ha="left", va="center", fontsize=5.9, color="#0f172a")

    # Agent 3: Compliance Rule Verifier
    ax.add_patch(patches.Rectangle((23.5, 3.0), 28.0, 9.5, facecolor="#ffffff", edgecolor="#6d28d9", linewidth=1.2))
    ax.add_patch(patches.Rectangle((23.5, 9.5), 28.0, 3.0, facecolor="#6d28d9", edgecolor="none"))
    ax.text(37.5, 11.0, "Compliance Rule Verifier", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(24.5, 6.2, "• Statutory Rules: BSA / FinCEN / EU AI Act Art. 14\n• PEP & OFAC Sanctions List Verification Gate\n• Model Governance Pre-Check under Fed SR 11-7 / SR 21-8",
            ha="left", va="center", fontsize=5.9, color="#0f172a")

    # Arrow from Phase 2 to Phase 3 (Drafter -> AST Compiler)
    ax.annotate("", xy=(55.5, 32.0), xytext=(51.5, 19.5),
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#c2410c", connectionstyle="arc3,rad=-0.15"))
    ax.text(53.5, 25.5, "Submit Draft\nXML Dossier", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#c2410c",
            bbox=dict(boxstyle="square,pad=0.15", facecolor="#ffffff", edgecolor="#fdba74", lw=0.6))

    # =========================================================================
    # PHASE 3: AST COMPILER GATE (ANTI-HALLUCINATION)
    # =========================================================================
    # Recursive Descent AST Parser Box
    ax.add_patch(patches.Rectangle((55.5, 27.5), 20.0, 12.5, facecolor="#ffffff", edgecolor="#2563eb", linewidth=1.2))
    ax.add_patch(patches.Rectangle((55.5, 36.8), 20.0, 3.2, facecolor="#2563eb", edgecolor="none"))
    ax.text(65.5, 38.4, "AST Grammar Parser", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(56.5, 32.2, "• EBNF Grammar $\\mathcal{G}_{\\mathrm{SAR}}$ Validation\n• Recursive Descent Tokenizer\n• Entity Grounding Check:\n  $V(T) \\subseteq V_{\\mathrm{sub}}$ (Prop. 6.1)\n• Pydantic Schema Contracts",
            ha="left", va="center", fontsize=5.9, color="#0f172a")

    # Grounding Decision Diamond
    diamond_pts = [[65.5, 23.5], [71.5, 20.0], [65.5, 16.5], [59.5, 20.0]]
    diamond = patches.Polygon(diamond_pts, closed=True, facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.2)
    ax.add_patch(diamond)
    ax.text(65.5, 20.8, "Grounded?", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#b45309")
    ax.text(65.5, 19.0, r"$V(T) \subseteq V_{\mathrm{sub}}$", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#b45309")

    # Arrow from AST Parser to Decision Diamond
    ax.annotate("", xy=(65.5, 23.5), xytext=(65.5, 27.5),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#2563eb"))

    # Rejection Loop Arrow: No -> Return to Legal SAR Drafter
    ax.annotate("", xy=(51.5, 17.5), xytext=(59.5, 20.0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#dc2626", linestyle="--", connectionstyle="arc3,rad=-0.15"))
    ax.text(54.0, 18.2, "FAIL: Reject & Redraft\n(0.00% Hallucination)", ha="center", va="center", fontsize=5.2, fontweight="bold", color="#dc2626",
            bbox=dict(boxstyle="square,pad=0.15", facecolor="#ffffff", edgecolor="#fca5a5", lw=0.6))

    # Acceptance Arrow: Yes -> Verified Dossier Box
    ax.annotate("", xy=(65.5, 12.0), xytext=(65.5, 16.5),
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#15803d"))
    ax.text(67.0, 14.5, "PASS: Valid", ha="left", va="center", fontsize=6.0, fontweight="bold", color="#15803d")

    # Verified Dossier Box
    ax.add_patch(patches.Rectangle((55.5, 3.0), 20.0, 9.0, facecolor="#ffffff", edgecolor="#15803d", linewidth=1.2))
    ax.text(65.5, 9.5, "Verified Legal Dossier", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#15803d")
    ax.text(56.5, 5.8, "• FinCEN Form 111 XML Dossier\n• 0.00% Entity Hallucination Rate\n• Topological Chain Continuity Verified",
            ha="left", va="center", fontsize=5.8, color="#0f172a")

    # Arrow from Phase 3 to Phase 4
    ax.annotate("", xy=(79.5, 28.0), xytext=(75.5, 7.5),
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#15803d", connectionstyle="arc3,rad=-0.15"))
    ax.text(77.5, 17.0, "Certified\nXML Payload", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#15803d",
            bbox=dict(boxstyle="square,pad=0.15", facecolor="#ffffff", edgecolor="#86efac", lw=0.6))

    # =========================================================================
    # PHASE 4: DUAL-GOVERNANCE GATE & MERKLE WORM VAULT
    # =========================================================================
    # Four-Eyes Review Box
    ax.add_patch(patches.Rectangle((79.5, 24.5), 20.0, 15.5, facecolor="#ffffff", edgecolor="#7c3aed", linewidth=1.2))
    ax.add_patch(patches.Rectangle((79.5, 36.8), 20.0, 3.2, facecolor="#7c3aed", edgecolor="none"))
    ax.text(89.5, 38.4, "Dual-Governance Gate", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    
    # Sub-blocks Maker & Checker
    ax.add_patch(patches.Rectangle((80.5, 30.5), 18.0, 5.2, facecolor="#f5f3ff", edgecolor="#c4b5fd", linewidth=0.8))
    ax.text(89.5, 34.0, "Primary AML Analyst (Maker)", ha="center", va="center", fontsize=6.3, fontweight="bold", color="#5b21b6")
    ax.text(89.5, 32.0, "Evaluates factual chain & counterfactuals", ha="center", va="center", fontsize=5.5, color="#475569")

    # Dual Concurrence arrows
    ax.annotate("", xy=(89.5, 29.8), xytext=(89.5, 30.5), arrowprops=dict(arrowstyle="<->", lw=1.0, color="#7c3aed"))

    ax.add_patch(patches.Rectangle((80.5, 25.0), 18.0, 5.0, facecolor="#f5f3ff", edgecolor="#c4b5fd", linewidth=0.8))
    ax.text(89.5, 28.2, "Senior Officer (Checker)", ha="center", va="center", fontsize=6.3, fontweight="bold", color="#5b21b6")
    ax.text(89.5, 26.3, "Independent statutory sign-off & seal", ha="center", va="center", fontsize=5.5, color="#475569")

    # Arrow to HSM & WORM Vault
    ax.annotate("", xy=(89.5, 17.5), xytext=(89.5, 24.5),
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#7c3aed"))

    # Merkle WORM Vault Box
    ax.add_patch(patches.Rectangle((79.5, 3.0), 20.0, 14.5, facecolor="#ffffff", edgecolor="#0f172a", linewidth=1.4))
    ax.add_patch(patches.Rectangle((79.5, 14.3), 20.0, 3.2, facecolor="#0f172a", edgecolor="none"))
    ax.text(89.5, 15.9, "Merkle WORM Audit Vault", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")
    ax.text(80.5, 10.5, "• FIPS 140-2 Hardware HSM Seal\n• SHA-256 Merkle Root Ledger:\n  " + r"$h_{\mathrm{leaf}} = \mathrm{SHA256}(\mathcal{G}_{\mathrm{sub}} \,\|\, \mathbf{z}_{\mathrm{inv}} \,\|\, \mathrm{XML})$" + "\n• Statutory Admissibility:\n  Fed SR 11-7 / SR 21-8 / FinCEN",
            ha="left", va="center", fontsize=5.8, color="#0f172a")

    # Bottom Architectural Compliance Legend
    legend_bar = patches.Rectangle((1.0, 0.2), 100.0, 1.0, facecolor="#0f172a", edgecolor="none")
    ax.add_patch(legend_bar)
    ax.text(51.0, 0.7, "Enterprise AML Compliance Architecture: US Interagency SR 11-7 / SR 21-8 Model Risk Governance & EU AI Act Art. 14 Conformity",
            ha="center", va="center", fontsize=5.8, fontweight="bold", color="#38bdf8")

    plt.tight_layout()
    return fig

def main():
    print("Generating redesigned Figure 6.1 (Multi-Agent Forensic Swarm Pipeline)...")
    fig = generate_figure()

    for d in TARGET_DIRS:
        for stem in ["fig_forensic_swarm", "fig20_multi_agent_forensic_swarm"]:
            pdf_path = d / f"{stem}.pdf"
            png_path = d / f"{stem}.png"
            fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.10)
            fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
            print(f" [OK] Saved: {pdf_path}")

    # Artifact PNG
    artifact_path = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig6_1_redesigned_final.png")
    fig.savefig(artifact_path, format="png", bbox_inches="tight", pad_inches=0.10, dpi=300)
    print(f" [OK] Saved artifact: {artifact_path}")
    plt.close(fig)
    print("Figure 6.1 redesign completed successfully!")

if __name__ == "__main__":
    main()
