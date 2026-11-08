"""
Figure 6.2: AST Grammar Compiler and Anti-Hallucination SAR Pipeline
Redesigned with simplified functional blocks (Grammar Validation, Schema Check, etc.),
zero raw EBNF or Pydantic syntax clutter, and strict 4-color palette.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG, COLOR_INGEST_LIGHT,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_LIGHT, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_BG, COLOR_SAFE_LIGHT,
    COLOR_RISK, COLOR_RISK_BG, COLOR_RISK_LIGHT,
    COLOR_REVIEW, COLOR_REVIEW_BG, COLOR_REVIEW_LIGHT,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 48.0)

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 100, 48, facecolor="#ffffff", edgecolor="none"))

    # Top Master Banner
    ax.add_patch(patches.Rectangle((1.0, 41.5), 98.0, 5.5, facecolor=COLOR_DARK, edgecolor="none"))
    ax.text(50.0, 45.0, "DETERMINISTIC ANTI-HALLUCINATION VERIFICATION PIPELINE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 42.8, "Four-Stage Deterministic Shield: Guarantees 0.00% Entity Hallucination in Regulatory Filings",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # 4 Pipeline Stage Blocks
    stages = [
        {
            "x": 2.0, "w": 22.0, "num": "STAGE 1", "title": "Narrative\nSynthesis",
            "border": COLOR_MUTED, "bar": "#334155", "bg": "#f8fafc",
            "items": [
                "Forensic Swarm Agents",
                "Draft Narrative Proposal",
                "Temperature Locked (Zero)",
                "Deterministic Context",
                "2-Hop Graph Evidence"
            ]
        },
        {
            "x": 26.5, "w": 22.0, "num": "STAGE 2", "title": "Grammar\nValidation",
            "border": COLOR_INGEST, "bar": COLOR_INGEST, "bg": COLOR_INGEST_BG,
            "items": [
                "Formal Grammar Lexer",
                "Recursive Descent Parser",
                "Tag Hierarchy Check",
                "Syntax Conformance Gate",
                "Rejection of Malformed Text"
            ]
        },
        {
            "x": 51.5, "w": 22.0, "num": "STAGE 3", "title": "Schema\nCheck",
            "border": COLOR_REVIEW, "bar": COLOR_REVIEW, "bg": COLOR_REVIEW_BG,
            "items": [
                "Grounding Assertion Gate",
                "Graph Subgraph Containment",
                "Strict Account Continuity",
                "Amount Conservation Check",
                "Automated Redraft Feedback"
            ]
        },
        {
            "x": 76.5, "w": 22.0, "num": "STAGE 4", "title": "Audit & Merkle\nVerification",
            "border": COLOR_SAFE, "bar": COLOR_SAFE, "bg": COLOR_SAFE_BG,
            "items": [
                "4-Eyes Compliance Approval",
                "Zero-Hallucination Proof",
                "Cryptographic SHA-256 Seal",
                "Merkle Tree Tamper Proof",
                "Court-Admissible Filing"
            ]
        }
    ]

    for i, s in enumerate(stages):
        sx, sw = s["x"], s["w"]
        sy, sh = 7.5, 31.0

        # Card container
        ax.add_patch(patches.Rectangle(
            (sx, sy), sw, sh,
            facecolor=s["bg"], edgecolor=s["border"], lw=1.5
        ))
        # Top banner
        h_h = 7.5
        ax.add_patch(patches.Rectangle(
            (sx, sy + sh - h_h), sw, h_h,
            facecolor=s["bar"], edgecolor="none"
        ))
        ax.text(sx + sw/2, sy + sh - 2.5, s["num"],
                ha="center", va="center", fontsize=7.2, fontweight="bold", color="#94a3b8")
        ax.text(sx + sw/2, sy + sh - 5.4, s["title"].replace("\n", " - "),
                ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff")

        # Items list
        for j, item in enumerate(s["items"]):
            iy = sy + sh - h_h - 3.2 - j * 4.2
            ax.text(sx + 2.0, iy, "•", fontsize=8.0, fontweight="bold", color=s["bar"])
            ax.text(sx + 3.8, iy, item, fontsize=7.0, color=COLOR_DARK, va="center")

        # Connecting arrow to next stage
        if i < 3:
            arr_x0 = sx + sw
            arr_x1 = arr_x0 + 2.5
            arr_y = sy + sh * 0.50
            ax.annotate("", xy=(arr_x1, arr_y), xytext=(arr_x0, arr_y),
                        arrowprops=dict(arrowstyle="->", lw=2.0, color=COLOR_DARK, mutation_scale=14))

    # Bottom Summary Callout
    ax.add_patch(patches.Rectangle((1.0, 1.5), 98.0, 4.5, facecolor="#f1f5f9", edgecolor=COLOR_BORDER, lw=0.9))
    ax.text(50.0, 3.75, "Grammar and Schema Validation guarantee that every entity, account, and transfer in the SAR is strictly grounded in observed evidence.",
            ha="center", va="center", fontsize=7.2, style="italic", color=COLOR_DARK)

    save_figure(fig, "fig_ast_grammar_pipeline", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
