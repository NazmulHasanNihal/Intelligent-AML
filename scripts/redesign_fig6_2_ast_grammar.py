"""
scripts/redesign_fig6_2_ast_grammar.py
Publication-grade redesign of Figure 6.2:
AST Grammar Compiler and Anti-Hallucination SAR Pipeline.
Strictly NO cards: clean engineering block architecture with formal pipeline lanes.
Generates fig_ast_grammar_pipeline.pdf and .png across all 5 directories.
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
    fig, ax = plt.subplots(figsize=(10.0, 4.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 44)
    ax.axis("off")

    # Top Master Architecture Banner (crisp, professional header)
    ax.add_patch(patches.Rectangle((1.0, 39.0), 98.0, 4.2, facecolor="#0f172a", edgecolor="none"))
    ax.text(50.0, 41.5, "AST GRAMMAR COMPILER & DETERMINISTIC ANTI-HALLUCINATION VERIFICATION PIPELINE",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color="#ffffff")
    ax.text(50.0, 39.8, "Guarantees 0.00% Entity & Counterparty Hallucination in FinCEN Form 111 Regulatory Filings (Proposition 6.1)",
            ha="center", va="center", fontsize=6.2, color="#94a3b8")

    # 4 Pipeline Stage Blocks (Sharp rectangular engineering blocks)
    stages = [
        {
            "x": 1.5, "w": 22.0, "stage": "STAGE 1", "title": "Multi-Agent Synthesis",
            "accent": "#475569", "bar": "#334155",
            "items": [
                "• Forensic Swarm Agents",
                "• Raw Candidate Narrative",
                "• Temperature locked at " + r"$\tau = 0.0$",
                "• Top-$p = 1.0$ (Deterministic)",
                "• Context: " + r"$\mathcal{G}_{\mathrm{sub}}, \mathbf{z}_{\mathrm{inv}}, \mathbf{M}_e$"
            ]
        },
        {
            "x": 26.5, "w": 22.0, "stage": "STAGE 2", "title": "EBNF Grammar Lexer",
            "accent": "#1e40af", "bar": "#1d4ed8",
            "items": [
                "• EBNF Grammar " + r"$\mathcal{G}_{\mathrm{SAR}}$" + " Rules",
                "• Recursive Descent Parser",
                "• Lexical Token Hierarchy",
                "• Structural Tag Validation",
                "• Rejects Malformed Syntax"
            ]
        },
        {
            "x": 51.5, "w": 22.0, "stage": "STAGE 3", "title": "Pydantic Grounding Gate",
            "accent": "#d97706", "bar": "#b45309",
            "items": [
                "• Assertion: " + r"$V(T) \subseteq V_{\mathrm{sub}}$",
                "• Continuity: " + r"$v_i^{\mathrm{dst}} = v_{i+1}^{\mathrm{src}}$",
                "• Amount Bounds: $A > 0$",
                "• Edge Trust: " + r"$\hat{g}_{ij} \in [0, 1]$",
                "• Automated Redraft Loop"
            ]
        },
        {
            "x": 76.5, "w": 22.0, "stage": "STAGE 4", "title": "Statutory Merkle Dossier",
            "accent": "#059669", "bar": "#047857",
            "items": [
                "• FinCEN Form 111 XML Dossier",
                "• 0.00% Entity Hallucination",
                "• SHA-256 Merkle Leaf Seal",
                "• Immutable WORM Audit Vault",
                "• Fed SR 11-7 / SR 21-8 Receipt"
            ]
        }
    ]

    for s in stages:
        # Outer box
        ax.add_patch(patches.Rectangle((s["x"], 13.0), s["w"], 24.5, facecolor="#ffffff", edgecolor=s["accent"], linewidth=1.2))
        # Top title bar
        ax.add_patch(patches.Rectangle((s["x"], 33.2), s["w"], 4.3, facecolor=s["bar"], edgecolor="none"))
        ax.text(s["x"] + s["w"]/2.0, 35.8, s["stage"], ha="center", va="center", fontsize=6.2, fontweight="bold", color="#e2e8f0")
        ax.text(s["x"] + s["w"]/2.0, 34.2, s["title"], ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")

        # Text content inside block
        y_text = 30.5
        for item in s["items"]:
            ax.text(s["x"] + 1.2, y_text, item, ha="left", va="center", fontsize=6.2, color="#0f172a")
            y_text -= 3.8

    # Connecting Arrows between Stages
    arrow_props = dict(arrowstyle="->", lw=1.6, color="#0f172a")
    ax.annotate("", xy=(26.5, 25.0), xytext=(23.5, 25.0), arrowprops=arrow_props)
    ax.text(25.0, 26.5, "Parse", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#1e40af")

    ax.annotate("", xy=(51.5, 25.0), xytext=(48.5, 25.0), arrowprops=arrow_props)
    ax.text(50.0, 26.5, "Validate", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#b45309")

    ax.annotate("", xy=(76.5, 25.0), xytext=(73.5, 25.0), arrowprops=arrow_props)
    ax.text(75.0, 26.5, "Certify", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#047857")

    # Feedback Redraft Loop Arrow (Stage 3 back to Stage 1)
    ax.annotate("", xy=(12.5, 13.0), xytext=(62.5, 13.0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#dc2626", linestyle="--", connectionstyle="arc3,rad=-0.18"))
    ax.text(37.5, 8.5, "Schema Rejection & Automated Retry Loop (0.00% Entity Hallucination Enforced)",
            ha="center", va="center", fontsize=6.0, fontweight="bold", color="#dc2626",
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#fff1f2", edgecolor="#fca5a5", lw=0.8))

    # Bottom Mathematical Rigor & Proof Specification Bar
    ax.add_patch(patches.Rectangle((1.5, 1.2), 97.0, 5.8, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0))
    ax.text(3.0, 5.2, "Mathematical Grounding Proposition 6.1:", fontsize=6.8, fontweight="bold", color="#0f172a")
    ax.text(3.0, 3.2, r"Let $T$ denote the generated SAR syntax tree and $V(T)$ the set of referenced entity identifiers. If $V(T) \subseteq \mathcal{V}_{\mathrm{sub}}$ and $A(e) \equiv \mathrm{Amount}(e)$" + "\n" + r"for all factual edges $e \in \mathcal{E}_{\mathrm{sub}}$, the post-validation entity hallucination error is strictly $\mathbb{P}(\mathrm{Hallucination}) = 0.00\%$.",
            fontsize=6.0, color="#334155")
    ax.text(96.0, 3.8, "[Proposition 6.1 Proven]", ha="right", va="center", fontsize=6.8, fontweight="bold", color="#059669")

    plt.tight_layout()
    return fig

def main():
    print("Generating redesigned Figure 6.2 (AST Grammar Anti-Hallucination Pipeline)...")
    fig = generate_figure()

    for d in TARGET_DIRS:
        pdf_path = d / "fig_ast_grammar_pipeline.pdf"
        png_path = d / "fig_ast_grammar_pipeline.png"
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
        print(f" [OK] Saved: {pdf_path}")

    artifact_path = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig6_2_redesigned_final.png")
    fig.savefig(artifact_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
    print(f" [OK] Saved artifact: {artifact_path}")
    plt.close(fig)
    print("Figure 6.2 redesign completed successfully!")

if __name__ == "__main__":
    main()

