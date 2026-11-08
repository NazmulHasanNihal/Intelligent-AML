"""
Figure 6.5: Tamper-Evident SHA-256 Merkle Tree and WORM Archival Ledger
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    card = patches.FancyBboxPatch((0.1, 0.1), 9.8, 4.8, boxstyle="round,pad=0.1", fc="#F8FAFC", ec="#94A3B8", lw=1.2)
    ax.add_patch(card)

    ax.text(5.0, 4.65, "Tamper-Evident SHA-256 Merkle Tree & WORM Storage Architecture (Fed SR 11-7 / FRE Rule 902(11))",
            fontsize=10.0, fontweight="bold", ha="center", color="#0F172A")

    # Level 0: Leaf Nodes (SAR Payloads)
    leaf_labels = [
        "SAR Dossier #1041\nEntity: 0x4f...8a\n" r"$h_1 = \text{SHA256}(\text{JSON}_1)$",
        "SAR Dossier #1042\nEntity: 0x9b...1c\n" r"$h_2 = \text{SHA256}(\text{JSON}_2)$",
        "SAR Dossier #1043\nEntity: 0x12...de\n" r"$h_3 = \text{SHA256}(\text{JSON}_3)$",
        "SAR Dossier #1044\nEntity: 0x7e...3f\n" r"$h_4 = \text{SHA256}(\text{JSON}_4)$",
    ]
    leaf_x = [1.2, 3.6, 6.4, 8.8]
    for x, lbl in zip(leaf_x, leaf_labels):
        lbox = patches.FancyBboxPatch((x - 0.95, 0.4), 1.9, 0.85, boxstyle="round,pad=0.04", fc="#EFF6FF", ec="#3B82F6", lw=1.0)
        ax.add_patch(lbox)
        ax.text(x, 0.82, lbl, fontsize=6.8, ha="center", va="center", color="#1E3A8A")

    # Level 1: Intermediate Hashes
    int_x = [2.4, 7.6]
    int_labels = [
        r"$h_{12} = \text{SHA256}(h_1 \parallel h_2)$" "\nDigest: 4a2f8c...901e",
        r"$h_{34} = \text{SHA256}(h_3 \parallel h_4)$" "\nDigest: 8b7d1e...342f"
    ]
    for x, lbl in zip(int_x, int_labels):
        ibox = patches.FancyBboxPatch((x - 1.15, 1.9), 2.3, 0.75, boxstyle="round,pad=0.04", fc="#F0FDF4", ec="#22C55E", lw=1.0)
        ax.add_patch(ibox)
        ax.text(x, 2.27, lbl, fontsize=7.2, ha="center", va="center", color="#14532D")

    # Level 2: Merkle Root Hash
    root_box = patches.FancyBboxPatch((3.4, 3.2), 3.2, 0.95, boxstyle="round,pad=0.05", fc="#FEF2F2", ec="#EF4444", lw=1.5)
    ax.add_patch(root_box)
    ax.text(5.0, 3.82, r"TAMPER-EVIDENT MERKLE ROOT $h_{\mathrm{root}}$", fontsize=7.8, fontweight="bold", ha="center", color="#991B1B")
    ax.text(5.0, 3.48, "Root Digest: 9f86d081884c7d659a2feaa0c...\nTimestamp: 2026-08-28T14:32:01.452Z (HSM Signed)",
            fontsize=6.8, ha="center", color="#7F1D1D")

    # Connecting Tree Arrows
    # Leaves to Intermediates
    ax.annotate("", xy=(2.4, 1.9), xytext=(1.2, 1.25), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))
    ax.annotate("", xy=(2.4, 1.9), xytext=(3.6, 1.25), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))
    ax.annotate("", xy=(7.6, 1.9), xytext=(6.4, 1.25), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))
    ax.annotate("", xy=(7.6, 1.9), xytext=(8.8, 1.25), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))
    # Intermediates to Root
    ax.annotate("", xy=(4.4, 3.2), xytext=(2.4, 2.65), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.4))
    ax.annotate("", xy=(5.6, 3.2), xytext=(7.6, 2.65), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.4))

    # WORM Vault Archival Ribbon
    worm_ribbon = patches.FancyBboxPatch((0.4, 4.3), 9.2, 0.32, boxstyle="round,pad=0.02", fc="#1E293B", ec="none")
    ax.add_patch(worm_ribbon)
    ax.text(5.0, 4.46, "S3 Object Lock / WORM Compliant Ledger: Immutability Enforced for 7 Years (FRE 902(11) Self-Authenticating)",
            color="#38BDF8", fontsize=7.0, fontweight="bold", ha="center", va="center")

    plt.tight_layout()
    save_figure(fig, "fig_6_5_merkle_audit_tree", pad_inches=0.12)
    plt.close()

# ==============================================================================
# 8. Figure 9.3: Multi-Bank Observability Gap vs. Federated Split-GNN
# ==============================================================================


if __name__ == "__main__":
    generate()
