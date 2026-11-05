"""
generate_action_plan_diagrams.py — Publication Vector Visuals for Thesis and EAAI:
1. Fig 4.2: Database Entity-Relationship Diagram (ERD) with 12-D View & Causal Indexes (fig4_2_database_erd)
2. Fig 3.1: Neural Tensor Flow & Message-Passing Block Diagram with dedicated Math Strip (fig3_1_tensor_flow)
3. Fig 8.2: Real-Time UML Sequence Lifeline Diagram with Latency Timestamps (fig8_2_uml_sequence_lifeline)
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import numpy as np

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
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'stix',
})

BASE_DIR = Path(__file__).resolve().parent.parent
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"

TARGET_DIRS = [data_fig_dir, thesis_fig_dir, eaai_fig_dir]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_fig(fig, stem):
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f" [OK] Generated: {stem}.pdf & .png")


# ==============================================================================
# 1. FIG 4.2: DATABASE ENTITY-RELATIONSHIP DIAGRAM (ERD) (7.16" x 3.60")
# ==============================================================================
print("Generating Fig 4.2: Relational Database ERD & Materialized Graph View...")
fig, ax = plt.subplots(figsize=(7.16, 4.20))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Outer background
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

# Master Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.920), 0.984, 0.072,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.956, 'Relational Database Schema (ERD), Causal Time Indexes & 12-D Graph Feature View',
        ha='center', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')

# TABLE 1: entities_master (Left)
# x: 0.015, y: 0.460, w: 0.280, h: 0.435
t1_x, t1_y, t1_w, t1_h = 0.015, 0.460, 0.280, 0.435
ax.add_patch(patches.FancyBboxPatch((t1_x, t1_y), t1_w, t1_h, boxstyle='round,pad=0.003,rounding_size=0.006',
                                    facecolor='#f8fafc', edgecolor='#0284c7', linewidth=1.1))
# Header
ax.add_patch(patches.FancyBboxPatch((t1_x + 0.004, t1_y + t1_h - 0.065), t1_w - 0.008, 0.060,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#0284c7', edgecolor='#0284c7'))
ax.text(t1_x + t1_w/2, t1_y + t1_h - 0.035, 'TABLE: entities_master', ha='center', va='center',
        fontsize=6.8, fontweight='bold', color='#ffffff')

t1_fields = [
    ("PK", "entity_id", "BIGINT / UUID", True),
    ("  ", "entity_type", "VARCHAR(32)", False),
    ("  ", "kyc_risk_tier", "SMALLINT (1-5)", False),
    ("FK", "country_iso", "CHAR(2) -> Jurisdictions", False),
    ("  ", "created_timestamp", "TIMESTAMP WITH TZ", False),
    ("  ", "is_pep_flag", "BOOLEAN DEFAULT FALSE", False),
    ("  ", "initial_balance", "NUMERIC(18, 4)", False)
]
for i, (pk, fname, ftype, is_pk) in enumerate(t1_fields):
    y_row = t1_y + t1_h - 0.100 - (i * 0.046)
    bg_color = "#e0f2fe" if is_pk else ("#f1f5f9" if i % 2 == 1 else "#ffffff")
    ax.add_patch(patches.Rectangle((t1_x + 0.006, y_row - 0.015), t1_w - 0.012, 0.040, facecolor=bg_color, edgecolor='none'))
    ax.text(t1_x + 0.014, y_row + 0.005, pk, ha='left', va='center', fontsize=5.8, fontweight='bold', color='#0284c7' if is_pk else '#64748b')
    ax.text(t1_x + 0.050, y_row + 0.005, fname, ha='left', va='center', fontsize=5.8, fontweight='bold' if is_pk else 'normal', color='#0f172a')
    ax.text(t1_x + t1_w - 0.014, y_row + 0.005, ftype, ha='right', va='center', fontsize=5.4, color='#475569')

# TABLE 2: streaming_transactions (Center)
# x: 0.355, y: 0.400, w: 0.320, h: 0.495
t2_x, t2_y, t2_w, t2_h = 0.355, 0.400, 0.320, 0.495
ax.add_patch(patches.FancyBboxPatch((t2_x, t2_y), t2_w, t2_h, boxstyle='round,pad=0.003,rounding_size=0.006',
                                    facecolor='#f8fafc', edgecolor='#0f766e', linewidth=1.2))
# Header
ax.add_patch(patches.FancyBboxPatch((t2_x + 0.004, t2_y + t2_h - 0.065), t2_w - 0.008, 0.060,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#0f766e', edgecolor='#0f766e'))
ax.text(t2_x + t2_w/2, t2_y + t2_h - 0.035, 'TABLE: streaming_transactions', ha='center', va='center',
        fontsize=6.8, fontweight='bold', color='#ffffff')

t2_fields = [
    ("PK", "transaction_id", "BIGINT / UUID", True),
    ("FK", "source_entity_id", "BIGINT -> entities", False),
    ("FK", "target_entity_id", "BIGINT -> entities", False),
    ("  ", "amount_usd", "NUMERIC(18, 4)", False),
    ("  ", "timestamp_utc", "TIMESTAMP WITH TZ", False),
    ("  ", "payment_rail", "VARCHAR(16) [SWIFT/bKash]", False),
    ("  ", "channel_code", "VARCHAR(16) [ATM/API/WIRE]", False),
    ("  ", "conformal_label", "SMALLINT [0=Benign, 1=Illicit]", False)
]
for i, (pk, fname, ftype, is_pk) in enumerate(t2_fields):
    y_row = t2_y + t2_h - 0.100 - (i * 0.046)
    bg_color = "#ccfbf1" if is_pk else ("#f1f5f9" if i % 2 == 1 else "#ffffff")
    ax.add_patch(patches.Rectangle((t2_x + 0.006, y_row - 0.015), t2_w - 0.012, 0.040, facecolor=bg_color, edgecolor='none'))
    ax.text(t2_x + 0.014, y_row + 0.005, pk, ha='left', va='center', fontsize=5.8, fontweight='bold', color='#0f766e' if is_pk else '#64748b')
    ax.text(t2_x + 0.050, y_row + 0.005, fname, ha='left', va='center', fontsize=5.8, fontweight='bold' if is_pk else 'normal', color='#0f172a')
    ax.text(t2_x + t2_w - 0.014, y_row + 0.005, ftype, ha='right', va='center', fontsize=5.4, color='#475569')

# TABLE 3: high_risk_jurisdictions (Right)
# x: 0.730, y: 0.520, w: 0.255, h: 0.375
t3_x, t3_y, t3_w, t3_h = 0.730, 0.520, 0.255, 0.375
ax.add_patch(patches.FancyBboxPatch((t3_x, t3_y), t3_w, t3_h, boxstyle='round,pad=0.003,rounding_size=0.006',
                                    facecolor='#f8fafc', edgecolor='#b91c1c', linewidth=1.1))
# Header
ax.add_patch(patches.FancyBboxPatch((t3_x + 0.004, t3_y + t3_h - 0.065), t3_w - 0.008, 0.060,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#b91c1c', edgecolor='#b91c1c'))
ax.text(t3_x + t3_w/2, t3_y + t3_h - 0.035, 'TABLE: high_risk_jurisdictions', ha='center', va='center',
        fontsize=6.8, fontweight='bold', color='#ffffff')

t3_fields = [
    ("PK", "country_iso", "CHAR(2)", True),
    ("  ", "country_name", "VARCHAR(48)", False),
    ("  ", "fatf_status", "VARCHAR(24)", False),
    ("  ", "basel_aml_idx", "NUMERIC(4, 2)", False),
    ("  ", "sanction_auth", "VARCHAR(32)", False),
    ("  ", "effective_date", "DATE", False)
]
for i, (pk, fname, ftype, is_pk) in enumerate(t3_fields):
    y_row = t3_y + t3_h - 0.100 - (i * 0.046)
    bg_color = "#fee2e2" if is_pk else ("#f1f5f9" if i % 2 == 1 else "#ffffff")
    ax.add_patch(patches.Rectangle((t3_x + 0.006, y_row - 0.015), t3_w - 0.012, 0.040, facecolor=bg_color, edgecolor='none'))
    ax.text(t3_x + 0.014, y_row + 0.005, pk, ha='left', va='center', fontsize=5.8, fontweight='bold', color='#b91c1c' if is_pk else '#64748b')
    ax.text(t3_x + 0.050, y_row + 0.005, fname, ha='left', va='center', fontsize=5.8, fontweight='bold' if is_pk else 'normal', color='#0f172a')
    ax.text(t3_x + t3_w - 0.014, y_row + 0.005, ftype, ha='right', va='center', fontsize=5.4, color='#475569')

# Crow's Foot ERD Relationship Connectors
# 1. entities_master (PK: entity_id) -> streaming_transactions (source_entity_id & target_entity_id) (1-to-Many)
ax.plot([t1_x + t1_w, 0.325, 0.325, t2_x], [0.795, 0.795, 0.745, 0.745], color='#0284c7', lw=1.3)
ax.plot([t1_x + t1_w + 0.008, t1_x + t1_w + 0.008], [0.785, 0.805], color='#0284c7', lw=1.3) # "1" tick
ax.plot([t2_x - 0.008, t2_x], [0.750, 0.745], color='#0284c7', lw=1.3) # Crow foot
ax.plot([t2_x - 0.008, t2_x], [0.740, 0.745], color='#0284c7', lw=1.3)
ax.text(0.325, 0.810, "1 : N (Source)", ha='center', va='bottom', fontsize=5.4, fontweight='bold', color='#0284c7')

ax.plot([t1_x + t1_w, 0.325, 0.325, t2_x], [0.795, 0.795, 0.700, 0.700], color='#0f766e', lw=1.3, linestyle='--')
ax.text(0.325, 0.675, "1 : N (Target)", ha='center', va='top', fontsize=5.4, fontweight='bold', color='#0f766e')

# 2. high_risk_jurisdictions (PK: country_iso) -> entities_master (FK: country_iso)
ax.plot([t3_x, 0.695, 0.695, 0.160, 0.160, 0.160], [0.815, 0.815, 0.905, 0.905, 0.895, 0.895], color='#b91c1c', lw=1.2, linestyle=':')
ax.text(0.440, 0.908, "1 : N (Jurisdiction FK)", ha='center', va='bottom', fontsize=5.2, fontweight='bold', color='#b91c1c')

# BOTTOM PANEL: Composite Time-Causal Indexes & 12-D Invariant Materialization
b_x, b_y, b_w, b_h = 0.015, 0.020, 0.970, 0.350
ax.add_patch(patches.FancyBboxPatch((b_x, b_y), b_w, b_h, boxstyle='round,pad=0.003,rounding_size=0.006',
                                    facecolor='#f8fafc', edgecolor='#64748b', linewidth=1.0))
# Subheader
ax.add_patch(patches.FancyBboxPatch((b_x + 0.004, b_y + b_h - 0.055), b_w - 0.008, 0.050,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#1e293b', edgecolor='#1e293b'))
ax.text(b_x + b_w/2, b_y + b_h - 0.030,
        r'DUCKDB / POSTGRESQL TIME-CAUSAL COMPOSITE INDEXES & MATERIALIZED 12-D INVARIANT VIEW',
        ha='center', va='center', fontsize=6.8, fontweight='bold', color='#ffffff')

# Left Column: Indexes
idx_box_x, idx_box_w = b_x + 0.012, 0.440
ax.add_patch(patches.FancyBboxPatch((idx_box_x, b_y + 0.015), idx_box_w, 0.260,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.7))
ax.text(idx_box_x + 0.015, b_y + 0.245, "Composite Causal Indexes (Zero Lookahead):", ha='left', va='center',
        fontsize=6.2, fontweight='bold', color='#0f172a')
indexes = [
    ("CREATE INDEX idx_source_time", "ON streaming_transactions(source_entity_id, timestamp_utc DESC)"),
    ("CREATE INDEX idx_target_time", "ON streaming_transactions(target_entity_id, timestamp_utc DESC)"),
    ("Execution Guarantee:", "O(log |E|) 2-hop causal ego-graph extraction in <0.18 ms"),
    ("Lookahead Invariant:", "Strictly t_e <= t_eval (eliminates future edge leakage)")
]
for i, (i_head, i_desc) in enumerate(indexes):
    y_idx = b_y + 0.195 - (i * 0.054)
    clr = '#0284c7' if i < 2 else ('#15803d' if i == 2 else '#b91c1c')
    ax.text(idx_box_x + 0.015, y_idx + 0.016, i_head, ha='left', va='center', fontsize=5.6, fontweight='bold', color=clr)
    ax.text(idx_box_x + 0.015, y_idx - 0.014, i_desc, ha='left', va='center', fontsize=5.2, color='#475569')

# Right Column: Materialized 12-D Invariant View
view_box_x, view_box_w = b_x + 0.468, 0.490
ax.add_patch(patches.FancyBboxPatch((view_box_x, b_y + 0.015), view_box_w, 0.260,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.7))
ax.text(view_box_x + 0.015, b_y + 0.245, r"CREATE VIEW v_canonical_invariants_12d AS (Mapping to Directed Multigraph):",
        ha='left', va='center', fontsize=6.2, fontweight='bold', color='#0f172a')
view_groups = [
    (r"1. Flow Regularity: $\Phi_{\mathrm{flow}} = \ln(1 + \sum A_{\mathrm{out}} / (\sum A_{\mathrm{in}} + \epsilon))$", "#0f766e"),
    (r"2. Hawkes Arrival Rate: $\lambda_u(t) = \mu_u + \sum_{t_i < t} \alpha \cdot e^{-\beta (t - t_i)}$", "#1e40af"),
    (r"3. Directed Causal Taints: $\mathbf{s}_{\mathrm{fwd}} \in [0, 1]$ (Dispersion), $\mathbf{s}_{\mathrm{bwd}} \in [0, 1]$ (Aggregation)", "#b91c1c"),
    (r"4. Graph Multi-Moments: $[\mu_A, \mathrm{Var}(A), \gamma_A, \kappa_A] \parallel [\text{deg}_{\mathrm{in}}, \text{deg}_{\mathrm{out}}, v_A, \nu_{\mathrm{io}}] \to \mathbb{R}^{12}$", "#6d28d9")
]
for i, (v_line, v_clr) in enumerate(view_groups):
    y_v = b_y + 0.195 - (i * 0.054)
    ax.text(view_box_x + 0.015, y_v, v_line, ha='left', va='center', fontsize=5.4, fontweight='bold', color=v_clr)

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig4_2_database_erd")


# ==============================================================================
# 2. FIG 3.1: NEURAL TENSOR FLOW & MESSAGE-PASSING BLOCK DIAGRAM (7.16" x 3.65")
# ==============================================================================
print("Generating Fig 3.1: Dedicated Neural Tensor Flow & Message-Passing Block Diagram...")
fig, ax = plt.subplots(figsize=(7.16, 3.65))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Outer background
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.920), 0.984, 0.072,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.956, 'C-STGB Neural Tensor Flow: Message Passing, Harmonic Encoders, Edge Gates & Fusion',
        ha='center', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')

# 5 Main Processing Columns across the Neural Tensor Pipeline
# Col 1: 3-Band Harmonic Encoder
# Col 2: Edge-Trust MLP Gate
# Col 3: Spatio-Temporal Temporal Conv / Attention
# Col 4: Typology GraphSMOTE Bilinear Head
# Col 5: Cold-Start Fusion & Bayes Risk Head

cols = [
    {
        "id": "STEP 1: ENCODER",
        "title": "3-Band Temporal",
        "badge_bg": "#1e40af", "badge_fg": "#eff6ff", "card_bg": "#f8fafc", "border": "#93c5fd",
        "x": 0.012, "w": 0.182,
        "items": [
            ("Raw Input Tensors", r"$\mathbf{x}_u \in \mathbb{R}^d, \; \mathbf{e}_{uv} \in \mathbb{R}^{d_e}$", "#0f172a"),
            ("Harmonic Band 1", r"$\Phi_{\text{burst}}(\Delta t) \in \mathbb{R}^{d/3}$", "#1e40af"),
            ("Harmonic Band 2", r"$\Phi_{\text{diurnal}}(\Delta t) \; (24\text{h})$", "#0f766e"),
            ("Harmonic Band 3", r"$\Phi_{\text{macro}}(\Delta t) \; (90\text{d})$", "#b91c1c"),
            ("Hawkes State", r"$\lambda_u(t) = \mu_0 + \sum_i \alpha e^{-\beta \Delta t}$", "#6d28d9")
        ],
        "out_tensor": r"$\mathbf{h}_u^{\,(0)} \in \mathbb{R}^{d_{\text{embed}}}$"
    },
    {
        "id": "STEP 2: EDGE GATE",
        "title": "Edge-Trust MLP",
        "badge_bg": "#0f766e", "badge_fg": "#f0fdfa", "card_bg": "#f8fafc", "border": "#99f6e4",
        "x": 0.208, "w": 0.182,
        "items": [
            ("Edge Context Cat", r"$[\mathbf{h}_u \parallel \mathbf{h}_v \parallel \mathbf{e}_{uv} \parallel \Phi_{\text{time}}]$", "#0f172a"),
            ("Trust Scoring MLP", r"$g_{ij} = \sigma(\mathbf{W}_g^\top [\cdot] + b_g)$", "#0f766e"),
            ("Floor Regularizer", r"$\hat{g}_{ij} = \delta_0 + (1 - \delta_0) g_{ij}$", "#0f766e"),
            ("Threshold Floor", r"$\delta_{\text{floor}} = 0.10 \text{ (Prunes 65.9\%)}$", "#b91c1c"),
            ("Denoised Graph", r"$\tilde{\mathcal{E}} = \{(u, v) : \hat{g}_{uv} \geq 0.10\}$", "#15803d")
        ],
        "out_tensor": r"$\mathbf{A}_{\text{gated}} = \hat{\mathbf{G}} \odot \mathbf{A}$"
    },
    {
        "id": "STEP 3: MESSAGE PASS",
        "title": "Continuous HGT",
        "badge_bg": "#c2410c", "badge_fg": "#fff7ed", "card_bg": "#f8fafc", "border": "#fed7aa",
        "x": 0.404, "w": 0.182,
        "items": [
            ("Hetero Message", r"$\mathbf{m}_{vu} = \mathbf{W}_v \mathbf{h}_v^{(l-1)} \hat{g}_{vu}$", "#0f172a"),
            ("Harmonic Attention", r"$\alpha_{vu} = \mathrm{Softmax}(\mathbf{q}_u^\top \mathbf{k}_v / \sqrt{d})$", "#c2410c"),
            ("Brody Curvature", r"$\kappa(u, v) \text{ Riemannian bound}$", "#c2410c"),
            ("Neighborhood Agg", r"$\tilde{\mathbf{h}}_u = \sum_{v \in \mathcal{N}_u} \alpha_{vu} \mathbf{m}_{vu}$", "#0f766e"),
            ("Feed-Forward Layer", r"$\mathbf{h}_u^{(l)} = \mathrm{LayerNorm}(\mathbf{h}_u + \mathrm{MLP})$", "#6d28d9")
        ],
        "out_tensor": r"$\mathbf{h}_u^{\,(L)} \in \mathbb{R}^d \text{ (Structural)}$"
    },
    {
        "id": "STEP 4: GRAPH-SMOTE",
        "title": "Latent Typology",
        "badge_bg": "#6d28d9", "badge_fg": "#faf5ff", "card_bg": "#f8fafc", "border": "#e9d5ff",
        "x": 0.600, "w": 0.182,
        "items": [
            ("Typology Clusters", r"$\mathcal{C}_1, \dots, \mathcal{C}_K \; (\tau_{\mathrm{sim}} \geq 0.75)$", "#0f172a"),
            ("Intra-Cluster Interp", r"$\mathbf{h}_{\mathrm{syn}} = (1-\rho)\mathbf{h}_u + \rho \mathbf{h}_v$", "#6d28d9"),
            ("Bilinear Link Head", r"$\hat{A}_{\mathrm{syn}, w} = \sigma(\mathbf{h}_{\mathrm{syn}}^T \mathbf{W}_e \mathbf{h}_w)$", "#6d28d9"),
            ("Flow Invariant Check", r"$\Phi_{\mathrm{flow}}(\mathrm{syn}) \approx 1.0 \text{ (Pass-thru)}$", "#15803d"),
            ("Train Isolation", r"100% Quarantined to $\mathcal{D}_{\mathrm{train}}$", "#b91c1c")
        ],
        "out_tensor": r"$\tilde{\mathcal{G}}_{\mathrm{train}} \text{ (+9.92 pp Lift)}$"
    },
    {
        "id": "STEP 5: FUSION & HEAD",
        "title": "Cold-Start & Bayes",
        "badge_bg": "#15803d", "badge_fg": "#f0fdf4", "card_bg": "#f8fafc", "border": "#bbf7d0",
        "x": 0.796, "w": 0.192,
        "items": [
            ("Universal Invariant", r"$\mathbf{z}_{\mathrm{inv}} \in \mathbb{R}^{12} \text{ (Kirchhoff)}$", "#0f172a"),
            ("Evidence Gating", r"$\alpha_u = \sigma(\mathbf{w}_\alpha^\top [\mathbf{h}_u \parallel \mathbf{z}_{\mathrm{inv}}])$", "#15803d"),
            ("Fused Embedding", r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$", "#15803d"),
            ("Bayes Loss Policy", r"$\mathcal{L}_{\mathrm{asym}} = 15 \cdot \mathrm{FN} + 1 \cdot \mathrm{FP}$", "#b91c1c"),
            ("Optimal Cutoff", r"$\tau^* = 0.18 \rightarrow \hat{y} = \mathbf{1}(\hat{p} \geq 0.18)$", "#b91c1c")
        ],
        "out_tensor": r"$\hat{p}_u \in [0, 1] \rightarrow \Gamma(u)$"
    }
]

y_card = 0.225
h_card = 0.680

for col in cols:
    cx, cw = col["x"], col["w"]
    # Outer card
    ax.add_patch(patches.FancyBboxPatch((cx, y_card), cw, h_card, boxstyle='round,pad=0.003,rounding_size=0.006',
                                        facecolor=col["card_bg"], edgecolor=col["border"], linewidth=1.1))
    # Header Pill
    ax.add_patch(patches.FancyBboxPatch((cx + 0.004, y_card + h_card - 0.082), cw - 0.008, 0.076,
                                        boxstyle='round,pad=0.002,rounding_size=0.004',
                                        facecolor=col["badge_bg"], edgecolor=col["badge_bg"]))
    ax.text(cx + cw/2, y_card + h_card - 0.026, col["id"], ha='center', va='center',
            fontsize=6.2, fontweight='bold', color='#ffffff')
    ax.text(cx + cw/2, y_card + h_card - 0.058, col["title"], ha='center', va='center',
            fontsize=5.8, color=col["badge_fg"], style='italic')

    # Item rows
    y_row_top = y_card + h_card - 0.096
    for idx, (label, math_str, clr) in enumerate(col["items"]):
        y_r = y_row_top - (idx * 0.100) - 0.040
        ax.add_patch(patches.FancyBboxPatch((cx + 0.006, y_r - 0.045), cw - 0.012, 0.086,
                                            boxstyle='round,pad=0.002,rounding_size=0.003',
                                            facecolor='#ffffff', edgecolor='#e2e8f0', linewidth=0.5))
        ax.text(cx + 0.012, y_r + 0.024, label, ha='left', va='center', fontsize=5.3, fontweight='bold', color='#334155')
        ax.text(cx + cw/2, y_r - 0.016, math_str, ha='center', va='center', fontsize=5.5, color=clr)

    # Output Tensor tag
    y_out = y_card + 0.014
    ax.add_patch(patches.FancyBboxPatch((cx + 0.006, y_out), cw - 0.012, 0.048,
                                        boxstyle='round,pad=0.002,rounding_size=0.003',
                                        facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(cx + cw/2, y_out + 0.024, col["out_tensor"], ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#0f172a')

# Tensor Flow Arrows across columns
for i in range(len(cols) - 1):
    x_st = cols[i]["x"] + cols[i]["w"] + 0.001
    x_en = cols[i+1]["x"] - 0.001
    y_arr = y_card + h_card / 2
    ax.annotate("", xy=(x_en, y_arr), xytext=(x_st, y_arr),
                arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color="#64748b", lw=1.2))

# DEDICATED BOTTOM MATH STRIP (Full Width)
ms_x, ms_y, ms_w, ms_h = 0.012, 0.016, 0.976, 0.190
ax.add_patch(patches.FancyBboxPatch((ms_x, ms_y), ms_w, ms_h, boxstyle='round,pad=0.003,rounding_size=0.005',
                                    facecolor='#f8fafc', edgecolor='#0f172a', linewidth=1.0))
# Strip Header
ax.add_patch(patches.FancyBboxPatch((ms_x + 0.004, ms_y + ms_h - 0.046), ms_w - 0.008, 0.042,
                                    boxstyle='round,pad=0.002,rounding_size=0.003',
                                    facecolor='#0f172a', edgecolor='#0f172a'))
ax.text(ms_x + ms_w/2, ms_y + ms_h - 0.025,
        r'MATHEMATICAL INVARIANT & GUARANTEE STRIP (EQUATIONS 1–22 ALIGNMENT)',
        ha='center', va='center', fontsize=6.8, fontweight='bold', color='#ffffff')

math_blocks = [
    (r"1. Invariant Space $\mathbf{z}_{\mathrm{inv}}$",
     r"$\tilde{\Phi}_{\mathrm{flow}} = \ln(1 + \frac{\sum A_{\mathrm{out}}}{\sum A_{\mathrm{in}}+\epsilon})$",
     0.025, 0.220),
    (r"2. Harmonic Encoder $\Phi_{\text{time}}$",
     r"$w(\Delta t) = \sum_{b=1}^3 \pi_b e^{-\lambda_b \Delta t} \cos(\omega_b \Delta t)$",
     0.260, 0.230),
    (r"3. Edge-Trust Floor $\hat{g}_{ij}$",
     r"$\hat{g}_{ij} \in [0.10, 1.0], \; \delta_{\text{floor}} = 0.10$",
     0.505, 0.220),
    (r"4. Adaptive Gating & Head $\mathbf{h}_u^*$",
     r"$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}, \; \tau^*=0.18$",
     0.740, 0.240)
]

for m_title, m_eq, mx, mw in math_blocks:
    ax.add_patch(patches.FancyBboxPatch((mx, ms_y + 0.012), mw, 0.120,
                                        boxstyle='round,pad=0.002,rounding_size=0.003',
                                        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(mx + mw/2, ms_y + 0.098, m_title, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#1e293b')
    ax.text(mx + mw/2, ms_y + 0.046, m_eq, ha='center', va='center', fontsize=6.0, color='#0f172a')

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig3_1_tensor_flow")


# ==============================================================================
# 3. FIG 8.2: UNIFIED UML SEQUENCE LIFELINE DIAGRAM (7.16" x 3.60")
# ==============================================================================
print("Generating Fig 8.2: Real-Time UML Sequence Lifeline with Latency Timestamps...")
fig, ax = plt.subplots(figsize=(7.16, 4.20))
ax.axis('off')
ax.set_xlim([-0.010, 1.010])
ax.set_ylim([-0.015, 1.015])

# Outer background
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

# Top Title Banner
ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.920), 0.984, 0.072,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.956, 'Real-Time Operational UML Sequence Lifeline: Webhook to Conformal Decision & Merkle Seal',
        ha='center', va='center', fontsize=9.0, fontweight='bold', color='#ffffff')

# 6 Lifeline Actors across the transaction lifecycle
lifelines = [
    ("Core Banking (CBS)\nPayment Webhook", 0.080, "#334155", "#f1f5f9"),
    ("FastAPI ASGI\nWorker Gateway", 0.245, "#0284c7", "#e0f2fe"),
    ("DuckDB / Arrow\nZero-Copy L1 LRU", 0.415, "#0f766e", "#ccfbf1"),
    ("C-STGB Neural\nInference Pod", 0.585, "#c2410c", "#ffedd5"),
    ("Conformal Arbiter\n3-Tier Dispatcher", 0.755, "#7c3aed", "#ede9fe"),
    ("Assisted 4-Agent\n& Merkle WORM", 0.920, "#15803d", "#dcfce7")
]

for name, lx, fg_col, bg_col in lifelines:
    # Actor Header Box
    ax.add_patch(patches.FancyBboxPatch((lx - 0.070, 0.810), 0.140, 0.085,
                                        boxstyle='round,pad=0.002,rounding_size=0.004',
                                        facecolor=bg_col, edgecolor=fg_col, linewidth=0.9))
    ax.text(lx, 0.852, name, ha='center', va='center', fontsize=5.8, fontweight='bold', color=fg_col, linespacing=1.2)
    # Vertical Lifeline
    ax.plot([lx, lx], [0.080, 0.810], color=fg_col, linestyle='--', lw=0.9, alpha=0.45)

# Messages & Timestamps down the sequence
messages = [
    # (step_num, from_idx, to_idx, y_pos, title, latency_str, color, is_async)
    (1, 0, 1, 0.745, "POST /v1/transactions/stream (JSON/ISO 20022)", "t = +0.00 ms", "#0284c7", False),
    (2, 1, 2, 0.675, "Zero-copy PyArrow Buffer & LRU Subgraph Lookup", "t = +0.05 ms", "#0f766e", False),
    (3, 2, 1, 0.615, "2-Hop Ego Subgraph G_t^(K) + 12-D Invariants (88.4% Hit)", "t = +0.16 ms", "#0f766e", False),
    (4, 1, 3, 0.545, "TorchScript Forward Pass (Harmonic + Edge Gating)", "t = +0.18 ms", "#c2410c", False),
    (5, 3, 1, 0.475, "Posterior Score p_u in [0, 1] & Invariant Embedding", "t = +0.28 ms", "#c2410c", False),
    (6, 1, 4, 0.405, "Dual-Quantile Check s_u <= q^(y) (CRC Calibration)", "t = +0.30 ms", "#7c3aed", False),
    (7, 4, 1, 0.335, "Triage Verdict: Tier 3 STP (99.32%) / Tier 1 (0.18%)", "t = +0.32 ms", "#7c3aed", False),
    (8, 1, 0, 0.265, "HTTP 200 OK: {status: 'CLEARED_STP', sla_ms: 0.45}", "t = +0.45 ms [SLA MET]", "#15803d", False),
    (9, 1, 5, 0.185, "Async Dispatch Tier-1/2 Case: 4-Agent Swarm (Investigator -> SAR)", "t = +1.10 ms [ASYNC]", "#b91c1c", True),
    (10, 5, 5, 0.115, "SHA-256 Merkle Root Sealed to WORM Vault (FRE 902(11))", "t = +24.8 s [SEALED]", "#15803d", True)
]

for s_num, f_idx, t_idx, y_m, m_txt, t_stamp, m_clr, is_async in messages:
    x_from = lifelines[f_idx][1]
    x_to = lifelines[t_idx][1]
    
    if f_idx == t_idx:
        # Self-loop arrow
        ax.annotate("", xy=(x_from + 0.010, y_m - 0.025), xytext=(x_from + 0.010, y_m),
                    arrowprops=dict(arrowstyle="->,head_width=0.15,head_length=0.22", color=m_clr, lw=1.2))
        ax.plot([x_from, x_from + 0.050, x_from + 0.050, x_from], [y_m, y_m, y_m - 0.025, y_m - 0.025],
                color=m_clr, lw=1.1, linestyle=':' if is_async else '-')
        ax.text(x_from + 0.055, y_m - 0.012, f"{s_num}. {m_txt}", ha='left', va='center',
                fontsize=5.3, fontweight='bold', color=m_clr)
        ax.text(x_from + 0.055, y_m - 0.032, t_stamp, ha='left', va='center',
                fontsize=5.0, color='#64748b', style='italic')
    else:
        # Cross-actor message arrow
        ls = '--' if is_async else '-'
        ax.annotate("", xy=(x_to, y_m), xytext=(x_from, y_m),
                    arrowprops=dict(arrowstyle="->,head_width=0.18,head_length=0.25", color=m_clr, lw=1.2, linestyle=ls))
        mid_x = (x_from + x_to) / 2
        ax.text(mid_x, y_m + 0.014, f"{s_num}. {m_txt}", ha='center', va='bottom',
                fontsize=5.2, fontweight='bold', color=m_clr)
        ax.text(mid_x, y_m - 0.016, f"[{t_stamp}]", ha='center', va='top',
                fontsize=4.9, color='#475569', style='italic')

# Bottom SLA SLA Guarantee Bar
ax.add_patch(patches.FancyBboxPatch((0.012, 0.012), 0.976, 0.058,
                                    boxstyle='round,pad=0.002,rounding_size=0.004',
                                    facecolor='#0f172a', edgecolor='#0f172a'))
ax.text(0.50, 0.041,
        "Total Synchronous Fast-Path SLA: 0.45 ms (22x Faster than 10.0 ms Bank Core SLA) | Async Swarm Investigation: <30 s",
        ha='center', va='center', fontsize=6.2, fontweight='bold', color='#38bdf8')

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig8_2_uml_sequence_lifeline")

print("All 3 New / Upgraded Action Plan Diagrams generated successfully!")
