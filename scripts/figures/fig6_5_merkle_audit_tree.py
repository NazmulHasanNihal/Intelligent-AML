"""
Figure 6.5: Tamper-Evident SHA-256 Merkle Tree and WORM Archival Ledger
Redesigned as an intuitive 3-Step Verification Pipeline:
Step 1: Real-World Evidence Leaves (Wire Log, Typology Graph, Model Decision, Dual Approval)
Step 2: Cryptographic Branch Pairings (Pairwise validation)
Step 3: Sealed Root in WORM Cold Storage (FRE Rule 902(11) self-authenticating evidence)
Clean orthogonal tree routing through dedicated gutters - zero arrows overlapping text.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG,
    COLOR_SAFE, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)

def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous canvas for 3-tier hierarchical architecture
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Master background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(50.0, 96.5, "CRYPTOGRAPHIC AUDIT TRAIL: SHA-256 MERKLE TREE & WORM ARCHIVAL STORAGE",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#ffffff")
    ax.text(50.0, 94.0, "Federal Reserve SR 11-7 & FRE Rule 902(11) Self-Authenticating Electronic Evidence Architecture",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # =========================================================================
    # TIER 1: EVIDENCE LEAVES (Ground-Truth Incident Data) y: 5.0 to 27.5
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (1.5, 5.0), 97.0, 22.5,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    # Step 1 Header at bottom of Tier 1 container to leave top open for arrows
    ax.add_patch(patches.Rectangle(
        (1.5, 5.0), 97.0, 3.2,
        facecolor=COLOR_INGEST, edgecolor="none"
    ))
    ax.text(50.0, 6.6, "STEP 1: FORENSIC EVIDENCE ARTIFACTS (CRYPTOGRAPHIC LEAF NODES)",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")

    leaves = [
        {
            "cx": 13.5,
            "title": "Evidence Artifact 1",
            "type": "Wire Transfer Payload",
            "entity": "Motijheel Corporate Acc",
            "hash": "SHA-256: 4a2f8c...901e",
            "fc": COLOR_INGEST_BG, "ec": COLOR_INGEST
        },
        {
            "cx": 37.5,
            "title": "Evidence Artifact 2",
            "type": "15-Node Subgraph Ring",
            "entity": "Smurfing & Wash Chains",
            "hash": "SHA-256: 7d1e34...fa82",
            "fc": COLOR_REVIEW_BG, "ec": COLOR_REVIEW
        },
        {
            "cx": 62.5,
            "title": "Evidence Artifact 3",
            "type": "Model Decision Dossier",
            "entity": "Tier 1 Conformal Quarantine",
            "hash": "SHA-256: 9b204c...18d5",
            "fc": COLOR_RISK_BG, "ec": COLOR_RISK
        },
        {
            "cx": 86.5,
            "title": "Evidence Artifact 4",
            "type": "Compliance Officer Signoff",
            "entity": "Dual 4-Eyes Governance",
            "hash": "SHA-256: 3c89aa...44f0",
            "fc": COLOR_SAFE_BG, "ec": COLOR_SAFE
        }
    ]

    card_w = 21.5
    card_h = 17.0
    card_y = 9.5
    for l in leaves:
        cx = l["cx"]
        # Leaf Card
        ax.add_patch(patches.Rectangle((cx - card_w/2, card_y), card_w, card_h,
                                       facecolor=l["fc"], edgecolor=l["ec"], lw=1.3))
        # Card Header
        ax.add_patch(patches.Rectangle((cx - card_w/2, card_y + card_h - 4.0), card_w, 4.0,
                                       facecolor=l["ec"], edgecolor="none"))
        ax.text(cx, card_y + card_h - 2.0, l["title"], ha="center", va="center",
                fontsize=7.0, fontweight="bold", color="#ffffff")
        # Content
        ax.text(cx, card_y + card_h - 6.5, l["type"], ha="center", va="center",
                fontsize=6.8, fontweight="bold", color=COLOR_DARK)
        ax.text(cx, card_y + card_h - 9.8, l["entity"], ha="center", va="center",
                fontsize=6.0, color=COLOR_MUTED)
        # Hash Badge
        ax.text(cx, card_y + 2.8, l["hash"], ha="center", va="center",
                fontsize=6.2, fontweight="bold", color=COLOR_DARK,
                bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=l["ec"], lw=0.8))

    # =========================================================================
    # GUTTER 1: ORTHOGONAL CONNECTORS LEAVES -> BRANCHES (y: 26.5 to 35.5)
    # =========================================================================
    # Left Pair: Leaves 1 & 2 -> Branch 1 (cx: 25.5, y_in: 36.0)
    ax.plot([13.5, 13.5], [26.5, 31.0], color=COLOR_DARK, lw=1.5)
    ax.plot([37.5, 37.5], [26.5, 31.0], color=COLOR_DARK, lw=1.5)
    ax.plot([13.5, 37.5], [31.0, 31.0], color=COLOR_DARK, lw=1.5)
    ax.annotate("", xy=(25.5, 36.0), xytext=(25.5, 31.0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=COLOR_DARK))
    ax.text(25.5, 31.0, "PAIRWISE HASH", ha="center", va="center",
            fontsize=5.5, fontweight="bold", color=COLOR_DARK,
            bbox=dict(boxstyle="square,pad=0.15", fc="#ffffff", ec=COLOR_BORDER, lw=0.6))

    # Right Pair: Leaves 3 & 4 -> Branch 2 (cx: 74.5, y_in: 36.0)
    ax.plot([62.5, 62.5], [26.5, 31.0], color=COLOR_DARK, lw=1.5)
    ax.plot([86.5, 86.5], [26.5, 31.0], color=COLOR_DARK, lw=1.5)
    ax.plot([62.5, 86.5], [31.0, 31.0], color=COLOR_DARK, lw=1.5)
    ax.annotate("", xy=(74.5, 36.0), xytext=(74.5, 31.0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=COLOR_DARK))
    ax.text(74.5, 31.0, "PAIRWISE HASH", ha="center", va="center",
            fontsize=5.5, fontweight="bold", color=COLOR_DARK,
            bbox=dict(boxstyle="square,pad=0.15", fc="#ffffff", ec=COLOR_BORDER, lw=0.6))

    # =========================================================================
    # TIER 2: MERKLE INTERMEDIATE BRANCHES (y: 36.0 to 55.5)
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (1.5, 36.0), 97.0, 19.5,
        facecolor="#f8fafc", edgecolor=COLOR_BORDER, lw=1.0
    ))
    ax.add_patch(patches.Rectangle(
        (1.5, 36.0), 97.0, 3.0,
        facecolor=COLOR_GNN, edgecolor="none"
    ))
    ax.text(50.0, 37.5, "STEP 2: INTERMEDIATE MERKLE BRANCH AGGREGATION (PAIRWISE VALIDATION)",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")

    branches = [
        {
            "cx": 25.5,
            "title": "Left Branch Digest: H(Evidence 1 + 2)",
            "sub": "Binds Transaction Wire to Typology Subgraph",
            "hash": "Branch Hash: e71a08...bb43",
            "ec": COLOR_GNN, "fc": COLOR_GNN_BG
        },
        {
            "cx": 74.5,
            "title": "Right Branch Digest: H(Evidence 3 + 4)",
            "sub": "Binds Model Decision to Human Sign-Off",
            "hash": "Branch Hash: b82c40...39d1",
            "ec": COLOR_GNN, "fc": COLOR_GNN_BG
        }
    ]

    branch_w = 42.0
    branch_h = 13.5
    branch_y = 40.5
    for b in branches:
        cx = b["cx"]
        # Branch Card
        ax.add_patch(patches.Rectangle((cx - branch_w/2, branch_y), branch_w, branch_h,
                                       facecolor=b["fc"], edgecolor=b["ec"], lw=1.3))
        # Branch Header
        ax.add_patch(patches.Rectangle((cx - branch_w/2, branch_y + branch_h - 3.8), branch_w, 3.8,
                                       facecolor=b["ec"], edgecolor="none"))
        ax.text(cx, branch_y + branch_h - 1.9, b["title"], ha="center", va="center",
                fontsize=7.0, fontweight="bold", color="#ffffff")
        # Content
        ax.text(cx, branch_y + branch_h - 6.2, b["sub"], ha="center", va="center",
                fontsize=6.5, color=COLOR_DARK)
        # Hash Badge
        ax.text(cx, branch_y + 2.5, b["hash"], ha="center", va="center",
                fontsize=6.4, fontweight="bold", color=COLOR_DARK,
                bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=b["ec"], lw=0.8))

    # =========================================================================
    # GUTTER 2: ORTHOGONAL CONNECTORS BRANCHES -> MASTER ROOT (y: 54.0 to 65.0)
    # =========================================================================
    # Branch 1 (cx: 25.5) -> Root Left (cx: 38.0)
    # Branch 2 (cx: 74.5) -> Root Right (cx: 62.0)
    ax.plot([25.5, 25.5], [54.0, 59.5], color=COLOR_DARK, lw=1.6)
    ax.plot([25.5, 38.0], [59.5, 59.5], color=COLOR_DARK, lw=1.6)
    ax.annotate("", xy=(38.0, 65.0), xytext=(38.0, 59.5),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK))

    ax.plot([74.5, 74.5], [54.0, 59.5], color=COLOR_DARK, lw=1.6)
    ax.plot([74.5, 62.0], [59.5, 59.5], color=COLOR_DARK, lw=1.6)
    ax.annotate("", xy=(62.0, 65.0), xytext=(62.0, 59.5),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_DARK))

    ax.text(50.0, 59.5, "FINAL ROOT DIGEST PAIRING", ha="center", va="center",
            fontsize=6.0, fontweight="bold", color=COLOR_DARK,
            bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec=COLOR_BORDER, lw=0.8))

    # =========================================================================
    # TIER 3: TAMPER-EVIDENT ROOT & WORM ARCHIVAL LEDGER y: 65.0 to 89.5
    # =========================================================================
    ax.add_patch(patches.Rectangle(
        (1.5, 65.0), 97.0, 24.5,
        facecolor="#fef2f2", edgecolor="#fca5a5", lw=1.2
    ))
    ax.add_patch(patches.Rectangle(
        (1.5, 86.0), 97.0, 3.5,
        facecolor=COLOR_RISK, edgecolor="none"
    ))
    ax.text(50.0, 87.7, "STEP 3: MASTER MERKLE ROOT & WRITE-ONCE-READ-MANY (WORM) COLD STORAGE",
            ha="center", va="center", fontsize=7.2, fontweight="bold", color="#ffffff")

    # Master Root Card (Centered)
    root_w = 68.0
    root_h = 18.0
    root_y = 66.5
    ax.add_patch(patches.Rectangle((50.0 - root_w/2, root_y), root_w, root_h,
                                   facecolor="#ffffff", edgecolor=COLOR_RISK, lw=1.6))
    ax.text(50.0, root_y + root_h - 3.8, "SEALED REGULATORY MERKLE ROOT DIGEST",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=COLOR_RISK)
    ax.text(50.0, root_y + root_h - 8.5, "Root Digest: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            ha="center", va="center", fontsize=6.6, fontweight="bold", color=COLOR_DARK,
            bbox=dict(boxstyle="square,pad=0.25", fc="#fee2e2", ec=COLOR_RISK, lw=0.8))
    ax.text(50.0, root_y + 3.2, "Hardware Security Module (HSM) Signed | S3 Object Lock Enforced (7-Year Statutory Hold)",
            ha="center", va="center", fontsize=6.4, fontweight="bold", color="#15803d")

    # Bottom Takeaway Ribbon
    ax.add_patch(patches.Rectangle(
        (1.5, 0.8), 97.0, 3.2,
        facecolor=COLOR_DARK, edgecolor="none"
    ))
    ax.text(50.0, 2.4, "LEGAL ADMISSIBILITY: Modifying even one transaction character breaks the Merkle tree, guaranteeing 100% court admissibility.",
            ha="center", va="center", fontsize=6.8, fontweight="bold", color="#38bdf8")

    save_figure(fig, "fig_6_5_merkle_audit_tree", pad_inches=0.12)
    save_figure(fig, "fig22_merkle_audit_tree", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    generate()
