"""
Figure 8.3: Enterprise Cloud-Native Deployment Topology and Kubernetes Orchestration
Structured as two clean, highly legible architectural panels:
Panel (a): Ingress Gateway & Kubernetes Compute Mesh (HPA Autoscaling 4 to 32 Pods)
Panel (b): Distributed State Store, Zero-Copy Graph Cache & WORM Compliance Vault
Enlarged typography (all text >= 7.2pt to 10.2pt), spacious card layout, zero text collisions.
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
    # Generous, massive canvas (14.5 x 9.8 inches) for optimal readability and zero crowding
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(14.5, 9.8), dpi=300)
    
    for ax in (ax_top, ax_bot):
        ax.axis("off")
        ax.set_xlim(0.0, 100.0)
        ax.set_ylim(0.0, 100.0)

    # Master canvas backgrounds
    ax_top.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))
    ax_bot.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # =========================================================================
    # TOP PANEL (A): INGRESS GATEWAY & KUBERNETES COMPUTE MESH
    # =========================================================================
    # Header Banner (a)
    ax_top.add_patch(patches.Rectangle((1.5, 87.0), 97.0, 11.5, facecolor=COLOR_DARK, edgecolor="none"))
    ax_top.text(3.0, 94.2, "(a) INGRESS GATEWAY & ELASTIC KUBERNETES COMPUTE MESH (HPA 4 TO 32 PODS)",
                ha="left", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax_top.text(3.0, 89.8, "Mutual TLS 1.3 Ingress -> Envoy Token Bucket -> Kubernetes HPA Pod Scaling -> Sub-0.45 ms GNN Forward Pass",
                ha="left", va="center", fontsize=8.0, color="#94a3b8")
    ax_top.add_patch(patches.Rectangle((74.0, 88.5), 23.0, 8.5, facecolor=COLOR_SAFE, edgecolor="none"))
    ax_top.text(85.5, 92.7, "BURST SLA: 31,250 TX/S", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff")

    # Ingress Block (Left: x: 1.5 to 25.5)
    ax_top.add_patch(patches.Rectangle((1.5, 5.0), 24.0, 78.0, facecolor="#f8fafc", edgecolor=COLOR_INGEST, lw=1.4))
    ax_top.add_patch(patches.Rectangle((1.5, 75.0), 24.0, 8.0, facecolor=COLOR_INGEST, edgecolor="none"))
    ax_top.text(13.5, 79.0, "SECURE INGRESS GATEWAY", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#ffffff")

    ingress_items = [
        ("Core Banking Stream", "ISO 20022 pacs.008 & camt.053\nPayment Webhooks via Kafka"),
        ("Envoy Edge Proxy", "Mutual TLS 1.3 Termination\nToken-Bucket Rate Limiter"),
        ("Zero-Trust Security", "OAuth2 & JWT Token Validation\nSHA-256 PII De-Identification")
    ]
    for idx, (title, sub) in enumerate(ingress_items):
        iy = 63.5 - idx * 22.0
        ax_top.add_patch(patches.Rectangle((3.0, iy - 9.5), 21.0, 19.0, facecolor=COLOR_INGEST_BG, edgecolor=COLOR_INGEST, lw=1.0))
        ax_top.text(13.5, iy + 4.8, title, ha="center", va="center", fontsize=8.0, fontweight="bold", color=COLOR_DARK)
        ax_top.text(13.5, iy - 3.2, sub, ha="center", va="center", fontsize=7.2, color="#334155", linespacing=1.2)

    # Ingress -> K8s Connector
    ax_top.annotate("", xy=(29.5, 44.0), xytext=(25.5, 44.0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=COLOR_DARK, mutation_scale=12))
    ax_top.text(27.5, 49.0, "mTLS\nStream", ha="center", va="center", fontsize=6.8, fontweight="bold", color=COLOR_DARK)

    # Kubernetes Compute Mesh Block (Right: x: 29.5 to 98.5)
    ax_top.add_patch(patches.Rectangle((29.5, 5.0), 69.0, 78.0, facecolor="#f0fdf4", edgecolor=COLOR_SAFE, lw=1.4))
    ax_top.add_patch(patches.Rectangle((29.5, 75.0), 69.0, 8.0, facecolor=COLOR_SAFE, edgecolor="none"))
    ax_top.text(64.0, 79.0, "KUBERNETES PRODUCTION COMPUTE MESH (ELASTIC AUTOSCALER)",
                ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff")

    # HPA Controller Banner
    ax_top.add_patch(patches.Rectangle((31.5, 59.5), 65.0, 12.0, facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=1.2))
    ax_top.text(64.0, 66.8, "Horizontal Pod Autoscaler (HPA Controller: Elastic Target 4 to 32 Pods)",
                ha="center", va="center", fontsize=8.4, fontweight="bold", color=COLOR_SAFE)
    ax_top.text(64.0, 62.8, "Dynamic Scaling Policy: Scales Out when CPU > 70% or Queue Latency > 2.5 ms",
                ha="center", va="center", fontsize=7.4, color="#475569")

    # Two Worker Pods Side-by-Side
    pod_w = 31.0
    pod_h = 49.0
    for pi, pname in enumerate(["FastAPI Worker Pod 1 (Active Core)", "FastAPI Worker Pod N (Scaled Replica)"]):
        px = 32.0 + pi * 34.0
        ax_top.add_patch(patches.Rectangle((px, 7.5), pod_w, pod_h, facecolor="#ffffff", edgecolor=COLOR_GNN, lw=1.2))
        ax_top.add_patch(patches.Rectangle((px, 7.5 + pod_h - 6.8), pod_w, 6.8, facecolor=COLOR_GNN, edgecolor="none"))
        ax_top.text(px + pod_w/2, 7.5 + pod_h - 3.4, pname, ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff")

        # Modules inside Pod
        pod_mods = [
            ("TorchScript Inference Core", "CPU-Native LibTorch GNN (Optional GPU Burst)", COLOR_GNN_BG, COLOR_GNN),
            ("In-Memory Graph Buffer", "DuckDB Zero-Copy 2-Hop (<0.12 ms)", COLOR_INGEST_BG, COLOR_INGEST),
            ("Conformal CRC Arbiter", "Guaranteed >= 99% Coverage Triage", COLOR_SAFE_BG, COLOR_SAFE)
        ]
        for mi, (mtitle, msub, mbg, mec) in enumerate(pod_mods):
            my = 38.0 - mi * 13.5
            ax_top.add_patch(patches.Rectangle((px + 1.5, my), pod_w - 3.0, 11.8, facecolor=mbg, edgecolor=mec, lw=0.9))
            ax_top.text(px + pod_w/2, my + 7.8, mtitle, ha="center", va="center", fontsize=7.8, fontweight="bold", color=COLOR_DARK)
            ax_top.text(px + pod_w/2, my + 3.2, msub, ha="center", va="center", fontsize=7.0, color="#334155")

    # =========================================================================
    # BOTTOM PANEL (B): DISTRIBUTED STATE STORAGE & WORM VAULT
    # =========================================================================
    # Header Banner (b)
    ax_bot.add_patch(patches.Rectangle((1.5, 87.0), 97.0, 11.5, facecolor=COLOR_DARK, edgecolor="none"))
    ax_bot.text(3.0, 94.2, "(b) DISTRIBUTED STATE STORE, ZERO-COPY GRAPH CACHE & WORM COMPLIANCE VAULT",
                ha="left", va="center", fontsize=10.2, fontweight="bold", color="#ffffff")
    ax_bot.text(3.0, 89.8, "Tier 1: DuckDB In-Memory Subgraph -> Tier 2: TimescaleDB Transaction Ledger -> Tier 3: SHA-256 Merkle WORM Vault",
                ha="left", va="center", fontsize=8.0, color="#94a3b8")
    ax_bot.add_patch(patches.Rectangle((74.0, 88.5), 23.0, 8.5, facecolor="#0284c7", edgecolor="none"))
    ax_bot.text(85.5, 92.7, "7-YEAR STATUTORY HOLD", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff")

    # 3 Distinct Storage Tiers Across Panel (b)
    tiers = [
        {
            "x": 1.5, "w": 31.0,
            "title": "TIER 1: IN-MEMORY GRAPH CACHE",
            "tech": "DuckDB & Apache Arrow Engine",
            "fc": COLOR_INGEST_BG, "ec": COLOR_INGEST,
            "items": [
                ("Zero-Copy Memory", "Columnar Arrow format shared directly with CPU/GPU."),
                ("2-Hop Subgraph", "Sub-0.12 ms localized ego-network retrieval."),
                ("50k Node LRU Cache", "250 MB RAM for 50k nodes | 88.4% Hit Rate.")
            ]
        },
        {
            "x": 34.5, "w": 31.0,
            "title": "TIER 2: RELATIONAL STATE STORE",
            "tech": "PostgreSQL & TimescaleDB Cluster",
            "fc": COLOR_REVIEW_BG, "ec": COLOR_REVIEW,
            "items": [
                ("Customer KYC Master", "Entity identity profiles and static risk ratings."),
                ("Case Audit Records", "Dual 4-eyes compliance signoffs & state history."),
                ("Partitioned Ledger", "Hypertables partitioned by transaction timestamp.")
            ]
        },
        {
            "x": 67.5, "w": 31.0,
            "title": "TIER 3: WORM COMPLIANCE VAULT",
            "tech": "AWS S3 Object Lock & HSM Signing",
            "fc": COLOR_SAFE_BG, "ec": COLOR_SAFE,
            "items": [
                ("FRE Rule 902(11)", "Self-authenticating cryptographic court evidence."),
                ("SHA-256 Merkle Root", "Immutable leaf hashing for every generated SAR."),
                ("Write-Once Retention", "Hardware-enforced 7-year non-erasable vault.")
            ]
        }
    ]

    for t in tiers:
        tx, tw = t["x"], t["w"]
        # Outer Box
        ax_bot.add_patch(patches.Rectangle((tx, 5.0), tw, 78.0, facecolor=t["fc"], edgecolor=t["ec"], lw=1.4))
        # Header Box
        ax_bot.add_patch(patches.Rectangle((tx, 75.0), tw, 8.0, facecolor=t["ec"], edgecolor="none"))
        ax_bot.text(tx + tw/2, 79.0, t["title"], ha="center", va="center", fontsize=8.0, fontweight="bold", color="#ffffff")

        # Subtitle badge
        ax_bot.add_patch(patches.Rectangle((tx + 1.5, 66.5), tw - 3.0, 6.8, facecolor="#ffffff", edgecolor=t["ec"], lw=1.0))
        ax_bot.text(tx + tw/2, 69.9, t["tech"], ha="center", va="center", fontsize=7.6, fontweight="bold", color=t["ec"])

        # Items
        for ii, (ititle, isub) in enumerate(t["items"]):
            iy = 53.5 - ii * 18.0
            ax_bot.add_patch(patches.Rectangle((tx + 1.5, iy - 8.5), tw - 3.0, 17.0, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.8))
            ax_bot.text(tx + 3.0, iy + 3.6, ititle, ha="left", va="center", fontsize=7.8, fontweight="bold", color=COLOR_DARK)
            ax_bot.text(tx + 3.0, iy - 2.8, isub, ha="left", va="center", fontsize=7.0, color="#334155")

    # Inter-Tier Connectors in Panel (b)
    ax_bot.annotate("", xy=(34.3, 44.0), xytext=(32.7, 44.0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_DARK, mutation_scale=11))
    ax_bot.annotate("", xy=(67.3, 44.0), xytext=(65.7, 44.0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_DARK, mutation_scale=11))

    save_figure(fig, "fig8_1_fastapi_k8s_topology", pad_inches=0.10)
    save_figure(fig, "fig23_fastapi_k8s_topology", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
