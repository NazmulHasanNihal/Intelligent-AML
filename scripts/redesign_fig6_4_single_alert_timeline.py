"""
scripts/redesign_fig6_4_single_alert_timeline.py
Publication-grade redesign of Figure 6.4:
Chronological Forensic Timeline of the 15-Node Laundering Case.
Generates fig_single_alert_timeline.pdf and .png.
"""

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
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 8.8,
    'axes.titlesize': 9.2,
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

def generate_figure_6_4():
    # Canvas sized 10.2 x 3.8 to maintain perfect aspect ratio (~2.68:1) for Page 73
    fig, ax = plt.subplots(figsize=(10.2, 3.8))
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master background
    bg = patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none", zorder=0)
    ax.add_patch(bg)

    # =========================================================================
    # MASTER HEADER
    # =========================================================================
    ax.text(50.0, 96.0, "Chronological Forensic Event Timeline: 15-Node Smurfing Incident",
            ha="center", va="center", fontsize=10.0, weight="bold", color="#0f172a")
    ax.text(50.0, 91.5, r"Real-Time Detection Lifecycle: Influx $\rightarrow$ Smurfing $\rightarrow$ Wash $\rightarrow$ Offshore Sink $\rightarrow$ Tier 1 Quarantine SAR",
            ha="center", va="center", fontsize=7.6, style="italic", color="#475569")

    # =========================================================================
    # CENTRAL TIMELINE AXIS & INTERVAL CHEVRONS (y = 52.0)
    # =========================================================================
    y_axis = 51.0
    ax.annotate("", xy=(97.5, y_axis), xytext=(2.5, y_axis),
                arrowprops=dict(arrowstyle="->", lw=2.4, color="#334155", shrinkA=0, shrinkB=0), zorder=2)
    ax.text(98.5, y_axis, "UTC", ha="left", va="center", fontsize=6.8, weight="bold", color="#334155")

    # Five Stages Data: (center_x, time_utc, stage_title, details_lines, color, delta_t)
    stages = [
        {
            "x": 10.5,
            "time": "14:15:02 UTC",
            "title": "Stage 1: Primary Influx",
            "entity": "Source S0 (ACC_9941)",
            "metric": r"Wire Influx: $\$485{,}000$",
            "sub": "Dormant account reactivation",
            "fc": "#eff6ff",
            "ec": "#2563eb",
            "tc": "#1e40af",
            "dt": "T = 0.0m"
        },
        {
            "x": 30.0,
            "time": "14:19:12 UTC",
            "title": "Stage 2: Smurfing Dispersal",
            "entity": r"Mules $M_1 \rightarrow M_4$ ($4 \times \$9.8\text{k}$)",
            "metric": r"Burst Rate: $\lambda_u(t) = 74.2$",
            "sub": "Sub-threshold structuring (<$10k)",
            "fc": "#fff7ed",
            "ec": "#ea580c",
            "tc": "#9a3412",
            "dt": "+4m 10s"
        },
        {
            "x": 50.0,
            "time": "14:23:01 UTC",
            "title": "Stage 3: Layering Wash",
            "entity": r"Conduits $L_1 \rightarrow L_2$ (Wash Ring)",
            "metric": r"Pruned Chaff: $M_e \geq 0.65$",
            "sub": r"Rapid hop dwell ($\Delta t < 3.8\text{m}$)",
            "fc": "#faf5ff",
            "ec": "#9333ea",
            "tc": "#6b21a8",
            "dt": "+3m 49s"
        },
        {
            "x": 70.0,
            "time": "14:27:45 UTC",
            "title": "Stage 4: Offshore Sink",
            "entity": "Offshore Account Sink (C4)",
            "metric": r"Mass Flow: $\Phi_{\text{flow}} = 0.994$",
            "sub": r"Reconsolidated: $\$482{,}300$",
            "fc": "#fef2f2",
            "ec": "#dc2626",
            "tc": "#991b1b",
            "dt": "+4m 44s"
        },
        {
            "x": 89.5,
            "time": "14:28:12 UTC",
            "title": "Stage 5: Conformal Triage",
            "entity": r"Verdict: $\mathbf{\Gamma(u) = \{1\}}$ (Quarantine)",
            "metric": "Action: Wire Freeze (<0.45 ms)",
            "sub": "SHA-256 Merkle WORM Sealed",
            "fc": "#f0fdf4",
            "ec": "#16a34a",
            "tc": "#166534",
            "dt": "+27s"
        }
    ]

    # Draw Stage Cards alternating cleanly with elegant pin connectors
    # Stage 1, 3, 5: Placed ABOVE timeline (y: 57.0 to 86.0)
    # Stage 2, 4: Placed BELOW timeline (y: 16.0 to 45.0)

    for i, s in enumerate(stages):
        cx = s["x"]
        is_above = (i % 2 == 0)

        # Milestone Pin Circle on Central Axis
        pin = patches.Circle((cx, y_axis), 1.6, facecolor=s["ec"], edgecolor="#ffffff", lw=1.2, zorder=5)
        ax.add_patch(pin)

        # Timestamp Badge right beside the pin
        if is_above:
            ax.text(cx, y_axis - 3.2, s["time"], ha="center", va="top",
                    fontsize=6.8, weight="bold", color="#1e293b",
                    bbox=dict(boxstyle="round,pad=0.18", fc="#f8fafc", ec="#cbd5e1", lw=0.6), zorder=6)
            # Connector vertical line up to card
            ax.plot([cx, cx], [y_axis + 1.6, 58.0], color=s["ec"], lw=1.6, zorder=3)

            # Card Above
            card = patches.FancyBboxPatch((cx - 8.8, 58.0), 17.6, 27.5, boxstyle="round,pad=0.6",
                                          facecolor=s["fc"], edgecolor=s["ec"], lw=1.4, zorder=3)
            ax.add_patch(card)

            # Content inside Card Above
            ax.text(cx, 82.5, s["title"], ha="center", va="center", fontsize=7.2, weight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 76.0, s["entity"], ha="center", va="center", fontsize=6.4, weight="bold", color="#0f172a", zorder=4)
            ax.text(cx, 69.5, s["metric"], ha="center", va="center", fontsize=6.6, weight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 63.0, s["sub"], ha="center", va="center", fontsize=6.0, color="#475569", style="italic", zorder=4)

        else:
            ax.text(cx, y_axis + 3.2, s["time"], ha="center", va="bottom",
                    fontsize=6.8, weight="bold", color="#1e293b",
                    bbox=dict(boxstyle="round,pad=0.18", fc="#f8fafc", ec="#cbd5e1", lw=0.6), zorder=6)
            # Connector vertical line down to card
            ax.plot([cx, cx], [y_axis - 1.6, 44.0], color=s["ec"], lw=1.6, zorder=3)

            # Card Below
            card = patches.FancyBboxPatch((cx - 8.8, 16.5), 17.6, 27.5, boxstyle="round,pad=0.6",
                                          facecolor=s["fc"], edgecolor=s["ec"], lw=1.4, zorder=3)
            ax.add_patch(card)

            # Content inside Card Below
            ax.text(cx, 41.0, s["title"], ha="center", va="center", fontsize=7.2, weight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 34.5, s["entity"], ha="center", va="center", fontsize=6.4, weight="bold", color="#0f172a", zorder=4)
            ax.text(cx, 28.0, s["metric"], ha="center", va="center", fontsize=6.6, weight="bold", color=s["tc"], zorder=4)
            ax.text(cx, 21.5, s["sub"], ha="center", va="center", fontsize=6.0, color="#475569", style="italic", zorder=4)

        # Elapsed Interval Indicator between milestones
        if i > 0:
            prev_x = stages[i-1]["x"]
            mid_x = (prev_x + cx) / 2.0
            # Solid white pill on the timeline axis to cleanly occlude line
            ax.text(mid_x, y_axis, s["dt"], ha="center", va="center", fontsize=6.0, weight="bold", color="#1e293b",
                    bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#64748b", lw=0.8, alpha=1.0), zorder=10)

    # =========================================================================
    # BOTTOM EXECUTIVE SUMMARY RIBBON (y: 2.5 to 8.5)
    # =========================================================================
    summary_card = patches.FancyBboxPatch((2.5, 2.5), 95.0, 6.5, boxstyle="round,pad=0.4",
                                          facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.0, zorder=2)
    ax.add_patch(summary_card)

    ax.text(50.0, 5.75, r"Total Incident Velocity: 13.1 Minutes from Influx to Autonomous Tier 1 Quarantine | Latency: < 0.45 ms STP Clearance | Fed SR 11-7 / SR 21-8 Aligned",
            ha="center", va="center", fontsize=7.0, weight="bold", color="#1e293b", zorder=3)

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_single_alert_timeline.pdf"
        png_path = d / "fig_single_alert_timeline.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
        print(f" [OK] Saved: {pdf_path}")
        
    # Also save to artifact directory
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig6_4_redesigned_final.png")
    fig.savefig(artifact_png, dpi=300, bbox_inches="tight", pad_inches=0.15)
    print(f" [OK] Artifact copy saved: {artifact_png}")
    plt.close(fig)

if __name__ == "__main__":
    generate_figure_6_4()

