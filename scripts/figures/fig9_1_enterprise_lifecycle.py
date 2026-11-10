"""
Figure 9.1: 26-Week Enterprise Production Deployment Roadmap
Standard Publication-Grade Process Flow Diagram (PFD) for C-STGB Monograph:
- 3 Dedicated Phased Process Lanes (Stage I: Passive Shadow, Stage II: Dual-Run Co-Pilot, Stage III: Autonomous STP)
- Chronological Top-to-Bottom Process Flow within each Stage with single-line non-overlapping bullets
- Formal Audit Gateway Decision Diamonds (Gate 1: KS Drift, Gate 2: SLA Stress) with Explicit Pass Criteria
- Decoupled Riser Corridors and Directional Transition Connectors
- Three-Column Executive Governance Footer Strip
- Zero text clipping, zero border collisions, strict adherence to master 4-color palette
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    setup_plt, save_figure,
    COLOR_INGEST, COLOR_INGEST_LIGHT, COLOR_INGEST_BG,
    COLOR_GNN, COLOR_GNN_BG, COLOR_GNN_PURPLE,
    COLOR_SAFE, COLOR_SAFE_LIGHT, COLOR_SAFE_BG,
    COLOR_RISK, COLOR_RISK_LIGHT, COLOR_RISK_BG,
    COLOR_REVIEW, COLOR_REVIEW_LIGHT, COLOR_REVIEW_BG,
    COLOR_DARK, COLOR_MUTED, COLOR_BORDER
)


def draw_pfd_node(ax, x, y, w, h, step_tag, title, subtitle, bullets, border_color, fill_color, header_color, badge=""):
    """Draws a standardized, high-precision Process Flow Diagram activity node with zero text collision."""
    # Outer Rounded Node Box
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor=fill_color, edgecolor=border_color, lw=1.2, zorder=2
    )
    ax.add_patch(box)

    # Header Strip
    hdr_h = 4.2
    hdr = patches.Rectangle(
        (x, y + h - hdr_h), w, hdr_h,
        facecolor=header_color, edgecolor="none", zorder=3
    )
    ax.add_patch(hdr)
    ax.text(x + 1.2, y + h - 2.1, step_tag, ha="left", va="center", fontsize=5.8, fontweight="bold", color="#ffffff", zorder=4)
    ax.text(x + w - 1.2, y + h - 2.1, title, ha="right", va="center", fontsize=6.2, fontweight="bold", color="#ffffff", zorder=4)

    # Subtitle under header
    ax.text(x + w / 2, y + h - 5.8, subtitle, ha="center", va="center", fontsize=5.0, fontstyle="italic", color=COLOR_MUTED, zorder=4)

    # Single-line itemized process bullets (uniform vertical spacing with guaranteed clear air)
    n_b = len(bullets)
    content_top = y + h - 7.6
    content_bot = y + 4.2 if badge else y + 1.2
    dy = (content_top - content_bot) / max(n_b, 1)

    for i, btxt in enumerate(bullets):
        cur_y = content_top - (i + 0.5) * dy
        ax.plot([x + 1.6], [cur_y], marker=">", markersize=2.2, color=header_color, zorder=4)
        ax.text(x + 2.6, cur_y, btxt, ha="left", va="center", fontsize=5.0, color="#1e293b", zorder=4)

    # Bottom Status Badge
    if badge:
        ax.add_patch(patches.FancyBboxPatch(
            (x + 1.0, y + 0.9), w - 2.0, 2.8,
            boxstyle="round,pad=0.1,rounding_size=0.3",
            facecolor="#ffffff", edgecolor=border_color, lw=0.7, zorder=3
        ))
        ax.text(x + w / 2, y + 2.3, badge, ha="center", va="center", fontsize=5.0, fontweight="bold", color=border_color, zorder=4)


def draw_gateway_diamond(ax, cx, cy, w, h, title, subtitle, border_color, fill_color):
    """Draws a formal audit gateway decision diamond."""
    pts = [
        [cx, cy + h / 2],      # Top vertex
        [cx + w / 2, cy],      # Right vertex
        [cx, cy - h / 2],      # Bottom vertex
        [cx - w / 2, cy]       # Left vertex
    ]
    poly = patches.Polygon(pts, facecolor=fill_color, edgecolor=border_color, lw=1.3, zorder=3)
    ax.add_patch(poly)

    ax.text(cx, cy + 1.8, title, ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_DARK, zorder=4)
    ax.text(cx, cy - 1.6, subtitle, ha="center", va="center", fontsize=4.8, fontstyle="italic", color=COLOR_MUTED, zorder=4)


def generate():
    setup_plt(font_size=8.5, title_size=10.0, label_size=8.5)
    # Generous canvas sized for immaculate process flow layout
    fig, ax = plt.subplots(figsize=(15.6, 8.4), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master canvas background
    ax.add_patch(patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none"))

    # Master Header Banner (Dark Slate Blue)
    ax.add_patch(patches.Rectangle(
        (1.5, 92.5), 97.0, 6.5,
        facecolor=COLOR_DARK, edgecolor="none", zorder=2
    ))
    ax.text(50.0, 96.6, "C-STGB: 26-WEEK ENTERPRISE PRODUCTION DEPLOYMENT PROCESS FLOW",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#ffffff", zorder=3)
    ax.text(50.0, 94.1, "Three-Stage Governance Lifecycle: Passive Shadow Mirror -> Dual-Run Co-Pilot -> Autonomous Straight-Through Processing",
            ha="center", va="center", fontsize=7.2, color="#94a3b8", zorder=3)

    # =========================================================================
    # LANE GEOMETRY & BACKDROP CORRIDORS
    # Lane 1 (Stage I): x in [2.0, 28.5] (Width 26.5)
    # Channel 1 (Gate 1): x in [28.5, 37.5] (Center 32.5)
    # Lane 2 (Stage II): x in [37.5, 64.0] (Width 26.5)
    # Channel 2 (Gate 2): x in [64.0, 73.0] (Center 68.0)
    # Lane 3 (Stage III): x in [73.0, 98.2] (Width 25.2)
    # =========================================================================
    lane_y = 17.5
    lane_h = 73.0

    lanes_meta = [
        {
            "x": 2.0, "w": 26.5,
            "stage_tag": "STAGE I (WEEKS 1–8)",
            "title": "PASSIVE SHADOW MODE",
            "mandate": "Zero Live Banking Impact & Distribution Baseline",
            "fc": COLOR_INGEST_BG, "ec": COLOR_INGEST, "hdr": COLOR_INGEST
        },
        {
            "x": 37.5, "w": 26.5,
            "stage_tag": "STAGE II (WEEKS 9–16)",
            "title": "DUAL-RUN CO-PILOT",
            "mandate": "Human-in-the-Loop Active Learning & Stress Testing",
            "fc": COLOR_REVIEW_BG, "ec": COLOR_REVIEW, "hdr": COLOR_REVIEW
        },
        {
            "x": 73.0, "w": 25.2,
            "stage_tag": "STAGE III (WEEKS 17–26)",
            "title": "AUTONOMOUS STP",
            "mandate": "99.33% Straight-Through Flow & Real-Time Quarantine",
            "fc": COLOR_SAFE_BG, "ec": COLOR_SAFE, "hdr": COLOR_SAFE
        }
    ]

    # Draw Stage Backdrop Containers and Stage Header Bars
    for lm in lanes_meta:
        # Subtle Corridor Backdrop
        ax.add_patch(patches.FancyBboxPatch(
            (lm["x"], lane_y), lm["w"], lane_h,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            facecolor=lm["fc"], edgecolor=lm["ec"], lw=1.2, alpha=0.35, zorder=1
        ))
        # Stage Master Header Strip
        ax.add_patch(patches.FancyBboxPatch(
            (lm["x"] + 0.6, 84.5), lm["w"] - 1.2, 5.2,
            boxstyle="round,pad=0.15,rounding_size=0.4",
            facecolor=lm["hdr"], edgecolor="none", zorder=3
        ))
        ax.text(lm["x"] + lm["w"] / 2, 87.8, f"{lm['stage_tag']}: {lm['title']}",
                ha="center", va="center", fontsize=6.4, fontweight="bold", color="#ffffff", zorder=4)
        ax.text(lm["x"] + lm["w"] / 2, 85.6, lm["mandate"],
                ha="center", va="center", fontsize=5.0, fontstyle="italic", color="#f1f5f9", zorder=4)

    # =========================================================================
    # STAGE I NODES (WEEKS 1–8: PASSIVE SHADOW PIPELINE)
    # =========================================================================
    # Node 1.1: Kafka Mirror Ingestion (Top)
    draw_pfd_node(
        ax, x=2.6, y=65.0, w=25.3, h=17.5,
        step_tag="STEP 1.1",
        title="Passive Kafka Mirror Tap",
        subtitle="Zero Core Banking Disruption",
        bullets=[
            "• Read-Only Mirror: 0.0 ms impact on core stream",
            "• Apache Arrow Tap: 31,250 tx/s zero-copy stream",
            "• Isolation Mandate: 100% decoupled from live rails"
        ],
        border_color=COLOR_INGEST,
        fill_color="#ffffff",
        header_color=COLOR_INGEST,
        badge="SLA Impact: 0.00 ms Overhead"
    )

    # Internal Downward Arrow 1.1 -> 1.2
    ax.annotate("", xy=(15.25, 60.5), xytext=(15.25, 64.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_INGEST, mutation_scale=9), zorder=4)
    ax.text(16.0, 62.5, "Live Transaction Events", ha="left", va="center", fontsize=4.8, color=COLOR_INGEST, zorder=5)

    # Node 1.2: 90-Day Conformal Calibration (Middle)
    draw_pfd_node(
        ax, x=2.6, y=42.5, w=25.3, h=17.5,
        step_tag="STEP 1.2",
        title="Distribution Profiling",
        subtitle="90-Day Calibration Accumulation",
        bullets=[
            r"• Calibration Set: Collects non-stationary $\mathcal{D}_{\mathrm{cal}}$",
            r"• Invariant Balance: Confirms Kirchhoff flow $\Phi_{\mathrm{flow}}$",
            "• Two-Sample KS Test: Continuous drift tracking"
        ],
        border_color=COLOR_INGEST,
        fill_color="#ffffff",
        header_color=COLOR_INGEST,
        badge="Baseline: 1,000,000+ Transactions"
    )

    # Internal Downward Arrow 1.2 -> 1.3
    ax.annotate("", xy=(15.25, 38.0), xytext=(15.25, 42.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_INGEST, mutation_scale=9), zorder=4)
    ax.text(16.0, 40.0, "Calibrated Embeddings", ha="left", va="center", fontsize=4.8, color=COLOR_INGEST, zorder=5)

    # Node 1.3: Drift Stability & Coverage Verification (Bottom)
    draw_pfd_node(
        ax, x=2.6, y=20.0, w=25.3, h=17.5,
        step_tag="STEP 1.3",
        title="Drift & Stability Audit",
        subtitle="Week 8 Benchmark Readiness",
        bullets=[
            "• KS Drift Hypothesis: Enforces p > 0.05 stability",
            "• Finite-Sample Bound: Validates recall >= 99.0%",
            "• Snapshot Freeze: Locks weights & telemetry"
        ],
        border_color=COLOR_INGEST,
        fill_color="#ffffff",
        header_color=COLOR_INGEST,
        badge="Ready for Gateway 1 Audit"
    )

    # =========================================================================
    # GATEWAY 1: DECISION DIAMOND & AUDIT PASS CRITERIA (X in [28.5, 37.5])
    # =========================================================================
    # Arrow out of Node 1.3 into Gate 1 Diamond
    ax.annotate("", xy=(29.8, 28.75), xytext=(28.1, 28.75),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLOR_DARK, mutation_scale=9), zorder=4)

    # Decision Diamond
    draw_gateway_diamond(
        ax, cx=32.5, cy=28.75, w=5.4, h=11.0,
        title="GATE 1",
        subtitle="Week 8 Audit",
        border_color=COLOR_RISK,
        fill_color="#fee2e2"
    )

    # Criteria Callout Card directly above Gate 1 Diamond
    ax.add_patch(patches.FancyBboxPatch(
        (29.8, 42.5), 5.4, 17.5,
        boxstyle="round,pad=0.15,rounding_size=0.4",
        facecolor="#ffffff", edgecolor=COLOR_RISK, lw=0.9, zorder=3
    ))
    ax.text(32.5, 57.5, "CRITERIA 1", ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_RISK, zorder=4)
    ax.plot([30.3, 34.7], [55.5, 55.5], color=COLOR_BORDER, lw=0.6, alpha=0.5, zorder=4)
    ax.text(32.5, 52.5, "1. KS Drift:", ha="center", va="center", fontsize=5.0, color="#475569", zorder=4)
    ax.text(32.5, 49.5, "p > 0.05", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_SAFE, zorder=4)
    ax.text(32.5, 45.8, "2. Coverage:", ha="center", va="center", fontsize=5.0, color="#475569", zorder=4)
    ax.text(32.5, 43.0, ">= 99.0%", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_INGEST, zorder=4)

    # Connector from Criteria Card down into Gate 1 Diamond
    ax.plot([32.5, 32.5], [42.5, 34.25], color=COLOR_RISK, lw=1.2, linestyle=":", zorder=4)

    # Approved Riser Channel from Gate 1 into Stage II Node 2.1
    # Exits Gate 1 right vertex at (35.2, 28.75) -> rises up corridor at x = 36.2 -> enters Node 2.1 at (38.1, 73.75)
    ax.plot([35.2, 36.2, 36.2, 38.1], [28.75, 28.75, 73.75, 73.75], color=COLOR_SAFE, lw=1.8, zorder=4)
    ax.annotate("", xy=(38.1, 73.75), xytext=(37.2, 73.75),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLOR_SAFE, mutation_scale=10), zorder=5)
    # Floating Approval Badge on Riser
    ax.text(36.2, 51.0, "PASS: PILOT", ha="center", va="center", rotation=90,
            fontsize=4.8, fontweight="bold", color=COLOR_SAFE,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=0.7), zorder=6)

    # =========================================================================
    # STAGE II NODES (WEEKS 9–16: DUAL-RUN CO-PILOT PIPELINE)
    # =========================================================================
    # Node 2.1: Parallel Scoring Engine (Top)
    draw_pfd_node(
        ax, x=38.1, y=65.0, w=25.3, h=17.5,
        step_tag="STEP 2.1",
        title="Concurrent Parallel Scoring",
        subtitle="Runs in Tandem with Legacy SQL",
        bullets=[
            "• Side-by-Side Scoring: Shadow evaluation on live feed",
            "• Discrepancy Logging: Flags multi-hop smurfing loops",
            "• Dual-Run Mode: Legacy engine retains live authority"
        ],
        border_color=COLOR_REVIEW,
        fill_color="#ffffff",
        header_color=COLOR_REVIEW,
        badge="Legacy Rules + C-STGB Dual-Rail Scoring"
    )

    # Internal Downward Arrow 2.1 -> 2.2
    ax.annotate("", xy=(50.75, 60.5), xytext=(50.75, 64.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_REVIEW, mutation_scale=9), zorder=4)
    ax.text(51.5, 62.5, "Boundary Alerts", ha="left", va="center", fontsize=4.8, color=COLOR_REVIEW, zorder=5)

    # Node 2.2: Human-in-the-Loop Active Learning (Middle)
    draw_pfd_node(
        ax, x=38.1, y=42.5, w=25.3, h=17.5,
        step_tag="STEP 2.2",
        title="Active Learning Feedback",
        subtitle="Tier-2 Boundary Adjudication",
        bullets=[
            "• Analyst Triage Desk: Routes boundary alerts with GNN maps",
            "• Ground-Truth Capture: Human adjudications recorded",
            "• Hard-Negative Bank: Refines boundaries on subtle mules"
        ],
        border_color=COLOR_REVIEW,
        fill_color="#ffffff",
        header_color=COLOR_REVIEW,
        badge="Queue Reduction: >= 90.0% Verified"
    )

    # Internal Downward Arrow 2.2 -> 2.3
    ax.annotate("", xy=(50.75, 38.0), xytext=(50.75, 42.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_REVIEW, mutation_scale=9), zorder=4)
    ax.text(51.5, 40.0, "Validated Models", ha="left", va="center", fontsize=4.8, color=COLOR_REVIEW, zorder=5)

    # Node 2.3: Peak Burst SLA Stress Testing (Bottom)
    draw_pfd_node(
        ax, x=38.1, y=20.0, w=25.3, h=17.5,
        step_tag="STEP 2.3",
        title="SLA Burst Stress Test",
        subtitle="Week 16 Enterprise Audit",
        bullets=[
            "• Throughput Saturation: 31,250 tx/s continuous load",
            "• Tail Latency SLA: P99 < 2.50 ms under burst peaks",
            "• Fail-Safe Recovery: Autonomous fallback on memory"
        ],
        border_color=COLOR_REVIEW,
        fill_color="#ffffff",
        header_color=COLOR_REVIEW,
        badge="Ready for Gateway 2 Audit"
    )

    # =========================================================================
    # GATEWAY 2: DECISION DIAMOND & AUDIT PASS CRITERIA (X in [64.0, 73.0])
    # =========================================================================
    # Arrow out of Node 2.3 into Gate 2 Diamond
    ax.annotate("", xy=(65.3, 28.75), xytext=(63.6, 28.75),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLOR_DARK, mutation_scale=9), zorder=4)

    # Decision Diamond
    draw_gateway_diamond(
        ax, cx=68.0, cy=28.75, w=5.4, h=11.0,
        title="GATE 2",
        subtitle="Week 16 Audit",
        border_color=COLOR_REVIEW,
        fill_color="#fffbeb"
    )

    # Criteria Callout Card directly above Gate 2 Diamond
    ax.add_patch(patches.FancyBboxPatch(
        (65.3, 42.5), 5.4, 17.5,
        boxstyle="round,pad=0.15,rounding_size=0.4",
        facecolor="#ffffff", edgecolor=COLOR_REVIEW, lw=0.9, zorder=3
    ))
    ax.text(68.0, 57.5, "CRITERIA 2", ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_REVIEW, zorder=4)
    ax.plot([65.8, 70.2], [55.5, 55.5], color=COLOR_BORDER, lw=0.6, alpha=0.5, zorder=4)
    ax.text(68.0, 52.5, "1. P99 SLA:", ha="center", va="center", fontsize=5.0, color="#475569", zorder=4)
    ax.text(68.0, 49.5, "< 2.5 ms", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_SAFE, zorder=4)
    ax.text(68.0, 45.8, "2. Peak Load:", ha="center", va="center", fontsize=5.0, color="#475569", zorder=4)
    ax.text(68.0, 43.0, "31,250 tx/s", ha="center", va="center", fontsize=5.8, fontweight="bold", color=COLOR_INGEST, zorder=4)

    # Connector from Criteria Card down into Gate 2 Diamond
    ax.plot([68.0, 68.0], [42.5, 34.25], color=COLOR_REVIEW, lw=1.2, linestyle=":", zorder=4)

    # Approved Riser Channel from Gate 2 into Stage III Node 3.1
    ax.plot([70.7, 71.7, 71.7, 73.6], [28.75, 28.75, 73.75, 73.75], color=COLOR_SAFE, lw=1.8, zorder=4)
    ax.annotate("", xy=(73.6, 73.75), xytext=(72.7, 73.75),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLOR_SAFE, mutation_scale=10), zorder=5)
    # Floating Approval Badge on Riser
    ax.text(71.7, 51.0, "PASS: FULL STP", ha="center", va="center", rotation=90,
            fontsize=4.8, fontweight="bold", color=COLOR_SAFE,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#ffffff", edgecolor=COLOR_SAFE, lw=0.7), zorder=6)

    # =========================================================================
    # STAGE III NODES (WEEKS 17–26: FULL AUTONOMOUS STP SURVEILLANCE)
    # =========================================================================
    # Node 3.1: Autonomous Straight-Through Processing (Top)
    draw_pfd_node(
        ax, x=73.6, y=65.0, w=24.0, h=17.5,
        step_tag="STEP 3.1",
        title="Autonomous STP Engine",
        subtitle="Straight-Through Live Execution",
        bullets=[
            "• 99.33% Straight-Thru: Clears 9,933/10k wires instantly",
            "• Zero Delay: Sub-0.45 ms fast-path clearance latency",
            "• Gate Authority: Full autonomous settlement clearance"
        ],
        border_color=COLOR_SAFE,
        fill_color="#ffffff",
        header_color=COLOR_SAFE,
        badge="Clearance Latency: 0.45 ms Fast-Path"
    )

    # Internal Downward Arrow 3.1 -> 3.2
    ax.annotate("", xy=(85.6, 60.5), xytext=(85.6, 64.5),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_SAFE, mutation_scale=9), zorder=4)
    ax.text(86.3, 62.5, "Illicit Triaged Wires", ha="left", va="center", fontsize=4.8, color=COLOR_SAFE, zorder=5)

    # Node 3.2: Real-Time Tier-1 Interdiction & Auto-SAR (Middle)
    draw_pfd_node(
        ax, x=73.6, y=42.5, w=24.0, h=17.5,
        step_tag="STEP 3.2",
        title="Autonomous Interdiction",
        subtitle="Sub-Second Asset Quarantine",
        bullets=[
            "• Tier-1 Real-Time Freeze: Instant hold on syndicates",
            "• Assisted SAR Dossiers: FinCEN Form 111 XML in sub-30s",
            "• Four-Eyes Desk: Analyst digital sign-off before filing"
        ],
        border_color=COLOR_SAFE,
        fill_color="#ffffff",
        header_color=COLOR_SAFE,
        badge="Quarantine Rate: 0.18% Confirmed Illicit"
    )

    # Internal Downward Arrow 3.2 -> 3.3
    ax.annotate("", xy=(85.6, 38.0), xytext=(85.6, 42.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLOR_SAFE, mutation_scale=9), zorder=4)
    ax.text(86.3, 40.0, "Audit Ledger Records", ha="left", va="center", fontsize=4.8, color=COLOR_SAFE, zorder=5)

    # Node 3.3: Statutory Production Handover & Cryptographic Vault (Bottom)
    draw_pfd_node(
        ax, x=73.6, y=20.0, w=24.0, h=17.5,
        step_tag="STEP 3.3",
        title="Statutory Production Handover",
        subtitle="Cryptographic Merkle Vault",
        bullets=[
            "• SHA-256 Provenance: Immutable tamper-proof tree",
            "• 7-Year WORM Storage: Meets BSA & FATF retention rules",
            "• Model Governance: Full SR 11-7 / SR 21-8 approval"
        ],
        border_color=COLOR_SAFE,
        fill_color="#ffffff",
        header_color=COLOR_SAFE,
        badge="PRODUCTION GOVERNANCE COMPLETE"
    )

    # =========================================================================
    # BOTTOM EXECUTIVE GOVERNANCE FOOTER STRIP (Y in [2.5, 14.5])
    # =========================================================================
    footer_cards = [
        {
            "x": 2.0, "w": 29.5,
            "title": "STAGE I: PASSIVE SHADOW DISCIPLINE",
            "lines": [
                "• 100% Shadow Isolation: Zero core banking disruption (0.00 ms).",
                "• 90-Day Calibration: Two-sample KS drift stabilization (target p > 0.05).",
                "• Invariant Verification: Verifies 12-D Kirchhoff mass-flow laws."
            ],
            "border": COLOR_INGEST, "bg": COLOR_INGEST_BG
        },
        {
            "x": 33.5, "w": 33.0,
            "title": "STAGE II: DUAL-RUN CO-PILOT VALIDATION",
            "lines": [
                "• Parallel Execution: Scores in tandem with legacy rule-based engines.",
                "• Active Learning Loop: Incorporates analyst feedback into memory bank.",
                "• Stress Resiliency: Validates 31,250 tx/s burst rate with P99 < 2.5 ms."
            ],
            "border": COLOR_REVIEW, "bg": COLOR_REVIEW_BG
        },
        {
            "x": 68.5, "w": 29.7,
            "title": "STAGE III: AUTONOMOUS PRODUCTION STP",
            "lines": [
                "• 99.33% Straight-Through Flow: Auto-clears wires in sub-0.45 ms.",
                "• Sub-Second Interdiction: Freezes 0.18% confirmed illicit syndicates.",
                "• Immutable Governance: SHA-256 Merkle seal meeting SR 11-7 / FATF."
            ],
            "border": COLOR_SAFE, "bg": COLOR_SAFE_BG
        }
    ]

    for fc in footer_cards:
        ax.add_patch(patches.FancyBboxPatch(
            (fc["x"], 2.5), fc["w"], 12.0,
            boxstyle="round,pad=0.15,rounding_size=0.5",
            facecolor=fc["bg"], edgecolor=fc["border"], lw=0.9, zorder=2
        ))
        ax.text(fc["x"] + fc["w"] / 2, 12.6, fc["title"], ha="center", va="center",
                fontsize=6.0, fontweight="bold", color=COLOR_DARK, zorder=3)
        ax.text(fc["x"] + fc["w"] / 2, 9.8, fc["lines"][0], ha="center", va="center",
                fontsize=4.9, color="#334155", zorder=3)
        ax.text(fc["x"] + fc["w"] / 2, 7.3, fc["lines"][1], ha="center", va="center",
                fontsize=4.9, color="#334155", zorder=3)
        ax.text(fc["x"] + fc["w"] / 2, 4.8, fc["lines"][2], ha="center", va="center",
                fontsize=4.9, color="#334155", zorder=3)

    # Save to all target figure repositories
    save_figure(fig, "fig_enterprise_deployment_lifecycle", pad_inches=0.10)
    save_figure(fig, "fig_26week_roadmap_gantt", pad_inches=0.10)
    plt.close(fig)


if __name__ == "__main__":
    generate()
