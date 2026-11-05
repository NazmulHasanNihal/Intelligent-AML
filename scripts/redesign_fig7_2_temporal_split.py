"""
scripts/redesign_fig7_2_temporal_split.py
Publication-grade redesign of Figure 7.2:
Zero-Leakage 4-Way Chronological Dataset Split Protocol.
Generates fig_temporal_split.pdf and .png across all 5 figure target directories.
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

def generate_figure_7_2():
    # Sized 10.2 x 4.6 inches for optimal publication elegance and Page 77 headroom
    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    ax.axis("off")
    ax.set_xlim(0.0, 100.0)
    ax.set_ylim(0.0, 100.0)

    # Master canvas background
    bg = patches.Rectangle((0, 0), 100, 100, facecolor="#ffffff", edgecolor="none", zorder=0)
    ax.add_patch(bg)

    # =========================================================================
    # 1. MASTER HEADER
    # =========================================================================
    ax.text(50.0, 97.2, "Zero-Leakage 4-Way Chronological Dataset Partitioning Architecture",
            ha="center", va="center", fontsize=10.2, weight="bold", color="#0f172a")
    ax.text(50.0, 93.6, r"Strict Causal Timeline Isolation: Eliminating Lookahead Bias, Graph Leakage, and Conformal Contamination",
            ha="center", va="center", fontsize=7.4, style="italic", color="#475569")

    # =========================================================================
    # 2. TOP METHODOLOGICAL PILLARS (y = 84.0 to 91.4) - Structured 4-Column Bar
    # =========================================================================
    b_pill_box = patches.FancyBboxPatch(
        (2.5, 84.0), 95.0, 7.4,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.9, zorder=2
    )
    ax.add_patch(b_pill_box)

    pillars = [
        {"x": 14.4, "col_x": 26.25, "text": "[Pillar 1] Causal Graph Flow", "sub": r"Past only: $\tau_{\text{past}} \leq t$", "tc": "#1e40af"},
        {"x": 38.1, "col_x": 50.00, "text": "[Pillar 2] Quarantined SMOTE", "sub": r"Confined strictly to $\mathcal{D}_{\text{train}}$", "tc": "#b45309"},
        {"x": 61.9, "col_x": 73.75, "text": "[Pillar 3] Finite Exchangeability", "sub": r"$\mathcal{D}_{\text{cal}} \cap \mathcal{D}_{\text{val}} = \emptyset$ (Disjoint)", "tc": "#6d28d9"},
        {"x": 85.6, "col_x": None,  "text": "[Pillar 4] Out-of-Time Serving", "sub": "Unseen future stream evaluation", "tc": "#047857"},
    ]

    for p in pillars:
        ax.text(p["x"], 89.5, p["text"], ha="center", va="center", fontsize=6.8, weight="bold", color=p["tc"], zorder=3)
        ax.text(p["x"], 85.5, p["sub"], ha="center", va="center", fontsize=5.8, color="#334155", zorder=3)
        if p["col_x"] is not None:
            ax.plot([p["col_x"], p["col_x"]], [84.4, 91.0], color="#e2e8f0", linewidth=1.0, zorder=3)

    # =========================================================================
    # 3. TIMELINE CONVEYOR TRACKS (y = 53.0 to 82.5)
    # =========================================================================
    w_tot = 95.0
    x0 = 2.5
    h_track = 6.2

    # --- TRACK A: Discrete UTXO Graphs (Elliptic-v1 & Elliptic-v2: 49 Timesteps) ---
    y_track_a = 72.8
    ax.text(2.5, y_track_a + h_track + 1.2, "Track A: Discrete UTXO Graph Snapshots (Elliptic-v1 & Elliptic-v2: 49 Timesteps, 2-Week Windows):",
            ha="left", va="bottom", fontsize=7.0, weight="bold", color="#1e3a8a", zorder=3)
    ax.annotate("", xy=(97.5, y_track_a + h_track + 2.0), xytext=(78.0, y_track_a + h_track + 2.0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#1e3a8a", shrinkA=0, shrinkB=0), zorder=3)
    ax.text(77.5, y_track_a + h_track + 2.0, "Time Arrow", ha="right", va="center", fontsize=5.8, weight="bold", color="#1e3a8a", zorder=3)

    w_d_tr = (30.0 / 49.0) * w_tot  # 58.16
    w_d_vl = (4.0 / 49.0) * w_tot   # 7.76
    w_d_cl = (4.0 / 49.0) * w_tot   # 7.76
    w_d_te = (11.0 / 49.0) * w_tot  # 21.32

    # Track A: Train Bar
    ax.add_patch(patches.Rectangle((x0, y_track_a), w_d_tr, h_track, facecolor="#1e40af", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(x0 + w_d_tr / 2.0, y_track_a + h_track / 2.0, r"$\mathcal{D}_{\text{train}}$: Steps 1–30 (61.2% Horizon) — GNN Parameters $\Theta$",
            ha="center", va="center", color="#ffffff", fontsize=7.0, weight="bold", zorder=3)

    # Track A: Val Bar
    x_vl = x0 + w_d_tr
    ax.add_patch(patches.Rectangle((x_vl, y_track_a), w_d_vl, h_track, facecolor="#d97706", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(x_vl + w_d_vl / 2.0, y_track_a + h_track / 2.0, r"$\mathcal{D}_{\text{val}}$: 31–34",
            ha="center", va="center", color="#ffffff", fontsize=6.2, weight="bold", zorder=3)

    # Track A: Cal Bar
    x_cl = x_vl + w_d_vl
    ax.add_patch(patches.Rectangle((x_cl, y_track_a), w_d_cl, h_track, facecolor="#7c3aed", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(x_cl + w_d_cl / 2.0, y_track_a + h_track / 2.0, r"$\mathcal{D}_{\text{cal}}$: 35–38",
            ha="center", va="center", color="#ffffff", fontsize=6.2, weight="bold", zorder=3)

    # Track A: Test Bar
    x_te = x_cl + w_d_cl
    ax.add_patch(patches.Rectangle((x_te, y_track_a), w_d_te, h_track, facecolor="#059669", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(x_te + w_d_te / 2.0, y_track_a + h_track / 2.0, r"$\mathcal{D}_{\text{test}}$: Steps 39–49 (22.4%) — Out-of-Time",
            ha="center", va="center", color="#ffffff", fontsize=7.0, weight="bold", zorder=3)

    # --- TRACK B: Continuous Streams (PaySim, SAML-D, IBM-AMLSim, Ethereum-Phish) ---
    y_track_b = 60.0
    ax.text(2.5, y_track_b + h_track + 1.2, "Track B: Continuous High-Velocity Streams (PaySim, SAML-D, IBM-AMLSim, Ethereum-Phish):",
            ha="left", va="bottom", fontsize=7.0, weight="bold", color="#1e3a8a", zorder=3)

    w_c_tr = 0.60 * w_tot  # 57.0
    w_c_vl = 0.10 * w_tot  # 9.50
    w_c_cl = 0.10 * w_tot  # 9.50
    w_c_te = 0.20 * w_tot  # 19.00

    # Track B: Train Bar
    ax.add_patch(patches.Rectangle((x0, y_track_b), w_c_tr, h_track, facecolor="#2563eb", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(x0 + w_c_tr / 2.0, y_track_b + h_track / 2.0, r"Training Stream: $t_0 \longrightarrow 0.60\,T$ (60.0% Horizon) — Gradient Updates $\Theta$",
            ha="center", va="center", color="#ffffff", fontsize=7.0, weight="bold", zorder=3)

    # Track B: Val Bar
    xc_vl = x0 + w_c_tr
    ax.add_patch(patches.Rectangle((xc_vl, y_track_b), w_c_vl, h_track, facecolor="#b45309", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(xc_vl + w_c_vl / 2.0, y_track_b + h_track / 2.0, r"Val: 0.60–0.70 T",
            ha="center", va="center", color="#ffffff", fontsize=6.0, weight="bold", zorder=3)

    # Track B: Cal Bar
    xc_cl = xc_vl + w_c_vl
    ax.add_patch(patches.Rectangle((xc_cl, y_track_b), w_c_cl, h_track, facecolor="#6d28d9", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(xc_cl + w_c_cl / 2.0, y_track_b + h_track / 2.0, r"Cal: 0.70–0.80 T",
            ha="center", va="center", color="#ffffff", fontsize=6.0, weight="bold", zorder=3)

    # Track B: Test Bar
    xc_te = xc_cl + w_c_cl
    ax.add_patch(patches.Rectangle((xc_te, y_track_b), w_c_te, h_track, facecolor="#047857", edgecolor="#0f172a", lw=1.0, zorder=2))
    ax.text(xc_te + w_c_te / 2.0, y_track_b + h_track / 2.0, r"Forward Test: $0.80 \to 1.00\,T$ (20.0%)",
            ha="center", va="center", color="#ffffff", fontsize=7.0, weight="bold", zorder=3)

    # --- VERTICAL CAUSAL FIREWALLS (BARRIERS) ---
    firewalls = [
        {"x": 60.1, "c": "#dc2626"},
        {"x": 68.8, "c": "#dc2626"},
        {"x": 77.8, "c": "#dc2626"},
    ]

    for fw in firewalls:
        ax.plot([fw["x"], fw["x"]], [55.5, 79.8], color=fw["c"], linestyle="--", linewidth=1.5, zorder=4)

    # Staggered Firewall Badges
    ax.text(60.1, 53.8, "[Barrier 1: Freeze Topology]", ha="center", va="center", fontsize=5.4, weight="bold",
            color="#991b1b", bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef2f2", edgecolor="#f87171", lw=0.8), zorder=5)
    ax.text(68.8, 50.2, r"[Barrier 2: Lock $\Theta, \tau^*$]", ha="center", va="center", fontsize=5.4, weight="bold",
            color="#991b1b", bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef2f2", edgecolor="#f87171", lw=0.8), zorder=5)
    ax.text(77.8, 53.8, r"[Barrier 3: Lock $\hat{q}^{(y)}$]", ha="center", va="center", fontsize=5.4, weight="bold",
            color="#991b1b", bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef2f2", edgecolor="#f87171", lw=0.8), zorder=5)

    # =========================================================================
    # 4. FOUR ARCHITECTURAL SPECIFICATION CARDS (y = 8.5 to 46.5)
    # =========================================================================
    cards_data = [
        {
            "x": 2.5, "w": 22.3,
            "theme_bg": "#eff6ff", "theme_border": "#93c5fd", "theme_header": "#1e40af",
            "tag": r"1. Training Split ($\mathcal{D}_{\text{train}}$: 60%)",
            "subtag": "Model Weights & Topology Optimization",
            "items": [
                ("Target: Parameter Learning", r"Optimizes neural weights $\Theta$ for STGB."),
                ("Scope: Past-Only Subgraphs", r"Strict $\mathcal{G}_{\leq t_{\text{train}}}$; zero future edges."),
                ("Quarantine: Latent SMOTE", "Synthetic fraud nodes confined here."),
                ("Slices: 60% Chrono Horizon", "Steps 1–30 | Stream 0.00 to 0.60 T.")
            ]
        },
        {
            "x": 26.8, "w": 22.3,
            "theme_bg": "#fffbeb", "theme_border": "#fcd34d", "theme_header": "#b45309",
            "tag": r"2. Validation Split ($\mathcal{D}_{\text{val}}$: 10%)",
            "subtag": "Checkpointing & Bayes Threshold",
            "items": [
                (r"Tuning: Bayes Threshold $\tau^*$", "N=50 Bayesian hyperparameter trials."),
                ("Decision: Macro F1 Optimization", r"Calibrates optimal cutoff $\tau^*$."),
                ("Lock: Zero Gradient Feedback", r"Model weights $\Theta$ frozen during eval."),
                ("Slices: 10% Chrono Horizon", "Steps 31–34 | Stream 0.60 to 0.70 T.")
            ]
        },
        {
            "x": 51.1, "w": 22.3,
            "theme_bg": "#faf5ff", "theme_border": "#d8b4fe", "theme_header": "#6d28d9",
            "tag": r"3. Calibration Split ($\mathcal{D}_{\text{cal}}$: 10%)",
            "subtag": "Class-Conditional Risk Quantiles",
            "items": [
                ("CRC: Conformal Risk Control", r"Computes class quantiles $\hat{q}^{(0)}, \hat{q}^{(1)}$."),
                ("Coverage: Finite Exchangeability", r"Guarantees risk coverage $1-\alpha \geq 99\%$."),
                ("Isolation: Disjoint Holdout", "Zero overlap with train or val sets."),
                ("Slices: 10% Chrono Horizon", "Steps 35–38 | Stream 0.70 to 0.80 T.")
            ]
        },
        {
            "x": 75.4, "w": 22.1,
            "theme_bg": "#f0fdf4", "theme_border": "#86efac", "theme_header": "#047857",
            "tag": r"4. Forward Test Split ($\mathcal{D}_{\text{test}}$: 20%)",
            "subtag": "Out-of-Time Forward Deployment",
            "items": [
                ("Benchmark: Out-of-Sample", "Final reporting across 5 locked seeds."),
                ("Production: Streaming SLA", "Simulates live deployment on unseen tx."),
                ("Zero Peeking: Pure Forward Eval", "Strict one-pass scoring without updates."),
                ("Slices: 20% Chrono Horizon", "Steps 39–49 | Stream 0.80 to 1.00 T.")
            ]
        }
    ]

    card_y = 8.5
    card_h = 38.0
    hdr_h = 6.4

    for c in cards_data:
        # Card Body Background
        b_body = patches.FancyBboxPatch(
            (c["x"], card_y), c["w"], card_h,
            boxstyle="round,pad=0.2,rounding_size=1.2",
            facecolor=c["theme_bg"], edgecolor=c["theme_border"], linewidth=1.1, zorder=2
        )
        ax.add_patch(b_body)

        # Card Header Banner
        b_hdr = patches.FancyBboxPatch(
            (c["x"], card_y + card_h - hdr_h), c["w"], hdr_h,
            boxstyle="round,pad=0.2,rounding_size=1.2",
            facecolor=c["theme_header"], edgecolor=c["theme_header"], linewidth=0.5, zorder=3
        )
        ax.add_patch(b_hdr)

        # Card Header Text
        ax.text(c["x"] + c["w"] / 2.0, card_y + card_h - 2.0, c["tag"],
                ha="center", va="center", color="#ffffff", fontsize=6.8, weight="bold", zorder=4)
        ax.text(c["x"] + c["w"] / 2.0, card_y + card_h - 4.6, c["subtag"],
                ha="center", va="center", color="#f1f5f9", fontsize=5.8, style="italic", zorder=4)

        # Four Bullet Points inside Card
        y_start = card_y + card_h - hdr_h - 3.2
        dy_bullet = 7.1
        dy_line = 3.4

        for bi, (title_text, body_text) in enumerate(c["items"]):
            item_y = y_start - bi * dy_bullet
            # Bullet point marker
            ax.plot([c["x"] + 1.2], [item_y], marker="o", markersize=3.0, color=c["theme_header"], zorder=4)
            # Line 1: Title
            ax.text(c["x"] + 2.5, item_y, title_text, ha="left", va="center",
                    fontsize=5.9, weight="bold", color="#0f172a", zorder=4)
            # Line 2: Body text
            ax.text(c["x"] + 2.5, item_y - dy_line, body_text, ha="left", va="center",
                    fontsize=5.5, color="#334155", zorder=4)

    # =========================================================================
    # 5. BOTTOM METHODOLOGICAL GUARANTEE CALLOUT BANNER (y = 1.2 to 6.2)
    # =========================================================================
    b_bot = patches.FancyBboxPatch(
        (2.5, 1.2), 95.0, 5.2,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor="#0f172a", edgecolor="#1e293b", linewidth=1.0, zorder=2
    )
    ax.add_patch(b_bot)

    ax.text(50.0, 4.4, "METHODOLOGICAL RIGOR: Zero-Leakage Guarantee Across All 14 Financial Transaction Networks",
            ha="center", va="center", fontsize=7.2, weight="bold", color="#fbbf24", zorder=3)
    ax.text(50.0, 2.4, r"Strict Temporal Causality: Past Information Only ($\tau_{\text{past}} \leq t$) | Disjoint Calibration Set $\mathcal{D}_{\text{cal}}$ Guarantees Valid Conformal Risk Coverage ($1-\alpha \geq 99.0\%$)",
            ha="center", va="center", fontsize=6.0, color="#f8fafc", zorder=3)

    return fig

def main():
    print("Generating redesigned Figure 7.2 (Zero-Leakage 4-Way Chronological Dataset Split Protocol)...")
    fig = generate_figure_7_2()

    # Save to all target directories
    for d in TARGET_DIRS:
        pdf_path = d / "fig_temporal_split.pdf"
        png_path = d / "fig_temporal_split.png"
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
        print(f"Saved: {pdf_path}")
        print(f"Saved: {png_path}")

    # Also save to artifact directory for inspection
    artifact_png = Path("C:/Users/SAAD/.gemini/antigravity/brain/26c4505d-0616-4920-a3c3-01117c9a7ce5/fig7_2_redesigned_final.png")
    fig.savefig(artifact_png, format="png", bbox_inches="tight", pad_inches=0.15, dpi=300)
    print(f"Saved artifact copy: {artifact_png}")

    plt.close(fig)
    print("Generation complete!")

if __name__ == "__main__":
    main()
