"""
scripts/test_redesign_fig4_2.py
Publication-grade redesign of Figure 4.2:
Relational Database Schema (ERD), Causal Time Indexes & Materialized 12-D View
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Matplotlib configuration for publication quality
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.2,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

def create_figure_4_2():
    # Canvas: 9.6 x 5.2 inches (aspect ratio ~ 0.541)
    fig = plt.figure(figsize=(9.6, 5.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor('#ffffff')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Master Top Banner
    title_box = FancyBboxPatch((0.012, 0.938), 0.976, 0.052, boxstyle="round,pad=0.01",
                               fc="#0f172a", ec="#0f172a", lw=1.0, zorder=2)
    ax.add_patch(title_box)
    ax.text(0.50, 0.964, "Relational Schema (ERD), Time-Causal Composite Indexes & Materialized 12-D Feature View",
            ha='center', va='center', fontsize=9.2, weight='bold', color='#ffffff', zorder=3)

    # =========================================================================
    # TOP ZONE: RELATIONAL ENTITY-RELATIONSHIP DIAGRAM (ERD) (y: 0.44 -> 0.92)
    # Natural reference order: Reference (Left) -> Master (Center) -> Stream (Right)
    # ZERO HOPPING / CROSSING CONNECTORS!
    # =========================================================================

    # -------------------------------------------------------------------------
    # TABLE 1: high_risk_jurisdictions (Left, x: 0.015 -> 0.245)
    # -------------------------------------------------------------------------
    t1_x, t1_y, t1_w, t1_h = 0.015, 0.455, 0.230, 0.465
    ax.add_patch(FancyBboxPatch((t1_x, t1_y), t1_w, t1_h, boxstyle='round,pad=0.008',
                                fc='#f8fafc', edgecolor='#b91c1c', linewidth=1.2, zorder=2))
    # Header
    ax.add_patch(FancyBboxPatch((t1_x + 0.004, t1_y + t1_h - 0.058), t1_w - 0.008, 0.052,
                                boxstyle='round,pad=0.004', fc='#b91c1c', edgecolor='#b91c1c', zorder=3))
    ax.text(t1_x + t1_w/2, t1_y + t1_h - 0.032, "TABLE: high_risk_jurisdictions", ha='center', va='center',
            fontsize=7.2, weight='bold', color='#ffffff', zorder=4)

    t1_fields = [
        ("PK", "country_iso", "CHAR(2)", True),
        ("  ", "country_name", "VARCHAR(48)", False),
        ("  ", "fatf_status", "VARCHAR(24)", False),
        ("  ", "basel_aml_idx", "NUMERIC(4, 2)", False),
        ("  ", "sanction_auth", "VARCHAR(32)", False),
        ("  ", "effective_date", "DATE", False)
    ]
    for i, (pk, fname, ftype, is_pk) in enumerate(t1_fields):
        y_row = t1_y + t1_h - 0.098 - (i * 0.052)
        bg_color = "#fee2e2" if is_pk else ("#f1f5f9" if i % 2 == 1 else "#ffffff")
        ax.add_patch(FancyBboxPatch((t1_x + 0.006, y_row - 0.016), t1_w - 0.012, 0.044,
                                    boxstyle='round,pad=0.002', fc=bg_color, ec='#fca5a5' if is_pk else 'none', lw=0.6, zorder=3))
        if is_pk:
            ax.add_patch(FancyBboxPatch((t1_x + 0.010, y_row - 0.010), 0.024, 0.032,
                                        boxstyle='round,pad=0.002', fc='#dc2626', ec='none', zorder=4))
            ax.text(t1_x + 0.022, y_row + 0.006, pk, ha='center', va='center', fontsize=5.8, weight='bold', color='#ffffff', zorder=5)
        ax.text(t1_x + 0.040, y_row + 0.006, fname, ha='left', va='center',
                fontsize=6.2, weight='bold' if is_pk else 'normal', color='#0f172a', zorder=4)
        ax.text(t1_x + t1_w - 0.012, y_row + 0.006, ftype, ha='right', va='center',
                fontsize=5.6, color='#475569', zorder=4)

    # Summary pill
    ax.add_patch(FancyBboxPatch((t1_x + 0.006, t1_y + 0.012), t1_w - 0.012, 0.036,
                                boxstyle='round,pad=0.002', fc='#fef2f2', ec='#f87171', lw=0.8, zorder=3))
    ax.text(t1_x + t1_w/2, t1_y + 0.030, "Regulatory Sanction Data", ha='center', va='center',
            fontsize=5.8, weight='bold', color='#991b1b', zorder=4)

    # -------------------------------------------------------------------------
    # TABLE 2: entities_master (Center, x: 0.305 -> 0.605)
    # -------------------------------------------------------------------------
    t2_x, t2_y, t2_w, t2_h = 0.305, 0.440, 0.300, 0.480
    ax.add_patch(FancyBboxPatch((t2_x, t2_y), t2_w, t2_h, boxstyle='round,pad=0.008',
                                fc='#f8fafc', edgecolor='#0284c7', linewidth=1.2, zorder=2))
    # Header
    ax.add_patch(FancyBboxPatch((t2_x + 0.004, t2_y + t2_h - 0.058), t2_w - 0.008, 0.052,
                                boxstyle='round,pad=0.004', fc='#0284c7', edgecolor='#0284c7', zorder=3))
    ax.text(t2_x + t2_w/2, t2_y + t2_h - 0.032, "TABLE: entities_master", ha='center', va='center',
            fontsize=7.4, weight='bold', color='#ffffff', zorder=4)

    t2_fields = [
        ("PK", "entity_id", "BIGINT / UUID", True, False),
        ("  ", "entity_type", "VARCHAR(32)", False, False),
        ("  ", "kyc_risk_tier", "SMALLINT (1-5)", False, False),
        ("FK", "country_iso", "CHAR(2) -> Jurisdictions", False, True),
        ("  ", "created_timestamp", "TIMESTAMP WITH TZ", False, False),
        ("  ", "is_pep_flag", "BOOLEAN DEFAULT FALSE", False, False),
        ("  ", "initial_balance", "NUMERIC(18, 4)", False, False)
    ]
    for i, (pk, fname, ftype, is_pk, is_fk) in enumerate(t2_fields):
        y_row = t2_y + t2_h - 0.098 - (i * 0.048)
        bg_color = "#e0f2fe" if is_pk else ("#fee2e2" if is_fk else ("#f1f5f9" if i % 2 == 1 else "#ffffff"))
        ax.add_patch(FancyBboxPatch((t2_x + 0.006, y_row - 0.015), t2_w - 0.012, 0.042,
                                    boxstyle='round,pad=0.002', fc=bg_color, ec='#7dd3fc' if is_pk else ('#fca5a5' if is_fk else 'none'), lw=0.6, zorder=3))
        if is_pk:
            ax.add_patch(FancyBboxPatch((t2_x + 0.010, y_row - 0.009), 0.024, 0.030,
                                        boxstyle='round,pad=0.002', fc='#0284c7', ec='none', zorder=4))
            ax.text(t2_x + 0.022, y_row + 0.006, pk, ha='center', va='center', fontsize=5.8, weight='bold', color='#ffffff', zorder=5)
        elif is_fk:
            ax.add_patch(FancyBboxPatch((t2_x + 0.010, y_row - 0.009), 0.024, 0.030,
                                        boxstyle='round,pad=0.002', fc='#b91c1c', ec='none', zorder=4))
            ax.text(t2_x + 0.022, y_row + 0.006, pk, ha='center', va='center', fontsize=5.8, weight='bold', color='#ffffff', zorder=5)
        
        ax.text(t2_x + 0.040, y_row + 0.006, fname, ha='left', va='center',
                fontsize=6.2, weight='bold' if (is_pk or is_fk) else 'normal', color='#0f172a', zorder=4)
        ax.text(t2_x + t2_w - 0.012, y_row + 0.006, ftype, ha='right', va='center',
                fontsize=5.6, color='#475569', zorder=4)

    # Summary pill
    ax.add_patch(FancyBboxPatch((t2_x + 0.006, t2_y + 0.010), t2_w - 0.012, 0.034,
                                boxstyle='round,pad=0.002', fc='#f0f9ff', ec='#38bdf8', lw=0.8, zorder=3))
    ax.text(t2_x + t2_w/2, t2_y + 0.027, "Primary Entity Vertex Store (N ≈ 100k)", ha='center', va='center',
            fontsize=5.8, weight='bold', color='#0369a1', zorder=4)

    # -------------------------------------------------------------------------
    # TABLE 3: streaming_transactions (Right, x: 0.665 -> 0.985)
    # -------------------------------------------------------------------------
    t3_x, t3_y, t3_w, t3_h = 0.665, 0.420, 0.320, 0.500
    ax.add_patch(FancyBboxPatch((t3_x, t3_y), t3_w, t3_h, boxstyle='round,pad=0.008',
                                fc='#f8fafc', edgecolor='#0f766e', linewidth=1.2, zorder=2))
    # Header
    ax.add_patch(FancyBboxPatch((t3_x + 0.004, t3_y + t3_h - 0.058), t3_w - 0.008, 0.052,
                                boxstyle='round,pad=0.004', fc='#0f766e', edgecolor='#0f766e', zorder=3))
    ax.text(t3_x + t3_w/2, t3_y + t3_h - 0.032, "TABLE: streaming_transactions", ha='center', va='center',
            fontsize=7.4, weight='bold', color='#ffffff', zorder=4)

    t3_fields = [
        ("PK", "transaction_id", "BIGINT / UUID", True, False),
        ("FK", "source_entity_id", "BIGINT -> entities", False, True),
        ("FK", "target_entity_id", "BIGINT -> entities", False, True),
        ("  ", "amount_usd", "NUMERIC(18, 4)", False, False),
        ("  ", "timestamp_utc", "TIMESTAMP WITH TZ", False, False),
        ("  ", "payment_rail", "VARCHAR(16) [SWIFT/bKash]", False, False),
        ("  ", "channel_code", "VARCHAR(16) [ATM/API/WIRE]", False, False),
        ("  ", "conformal_label", "SMALLINT [0=Benign, 1=Illicit]", False, False)
    ]
    for i, (pk, fname, ftype, is_pk, is_fk) in enumerate(t3_fields):
        y_row = t3_y + t3_h - 0.096 - (i * 0.046)
        bg_color = "#ccfbf1" if is_pk else ("#e0f2fe" if is_fk else ("#f1f5f9" if i % 2 == 1 else "#ffffff"))
        ax.add_patch(FancyBboxPatch((t3_x + 0.006, y_row - 0.015), t3_w - 0.012, 0.040,
                                    boxstyle='round,pad=0.002', fc=bg_color, ec='#5eead4' if is_pk else ('#7dd3fc' if is_fk else 'none'), lw=0.6, zorder=3))
        if is_pk:
            ax.add_patch(FancyBboxPatch((t3_x + 0.010, y_row - 0.009), 0.024, 0.028,
                                        boxstyle='round,pad=0.002', fc='#0f766e', ec='none', zorder=4))
            ax.text(t3_x + 0.022, y_row + 0.005, pk, ha='center', va='center', fontsize=5.8, weight='bold', color='#ffffff', zorder=5)
        elif is_fk:
            ax.add_patch(FancyBboxPatch((t3_x + 0.010, y_row - 0.009), 0.024, 0.028,
                                        boxstyle='round,pad=0.002', fc='#0284c7', ec='none', zorder=4))
            ax.text(t3_x + 0.022, y_row + 0.005, pk, ha='center', va='center', fontsize=5.8, weight='bold', color='#ffffff', zorder=5)

        ax.text(t3_x + 0.040, y_row + 0.005, fname, ha='left', va='center',
                fontsize=6.2, weight='bold' if (is_pk or is_fk) else 'normal', color='#0f172a', zorder=4)
        ax.text(t3_x + t3_w - 0.012, y_row + 0.005, ftype, ha='right', va='center',
                fontsize=5.6, color='#475569', zorder=4)

    # Summary pill
    ax.add_patch(FancyBboxPatch((t3_x + 0.006, t3_y + 0.010), t3_w - 0.012, 0.034,
                                boxstyle='round,pad=0.002', fc='#f0fdf4', ec='#22c55e', lw=0.8, zorder=3))
    ax.text(t3_x + t3_w/2, t3_y + 0.027, "Directed Multigraph Edge Stream (M > 10M)", ha='center', va='center',
            fontsize=5.8, weight='bold', color='#15803d', zorder=4)

    # -------------------------------------------------------------------------
    # CROW'S FOOT ERD CONNECTORS (Clean, Local, No Hopping!)
    # -------------------------------------------------------------------------

    # 1. high_risk_jurisdictions (PK: country_iso) -> entities_master (FK: country_iso)
    # Direct horizontal connection from Table 1 right edge to Table 2 left edge!
    y_fk1 = t1_y + t1_h - 0.098 # country_iso in Table 1 (~0.822)
    y_fk2 = t2_y + t2_h - 0.098 - (3 * 0.048) # country_iso in Table 2 (~0.678)
    
    # Clean step line between Table 1 and Table 2
    ax.plot([t1_x + t1_w, 0.275, 0.275, t2_x], [y_fk1, y_fk1, y_fk2, y_fk2], color='#b91c1c', lw=1.4, zorder=5)
    # '1' tick on Table 1 side
    ax.plot([t1_x + t1_w + 0.006, t1_x + t1_w + 0.006], [y_fk1 - 0.012, y_fk1 + 0.012], color='#b91c1c', lw=1.4, zorder=5)
    # Crow foot on Table 2 side
    ax.plot([t2_x - 0.010, t2_x], [y_fk2 + 0.008, y_fk2], color='#b91c1c', lw=1.4, zorder=5)
    ax.plot([t2_x - 0.010, t2_x], [y_fk2 - 0.008, y_fk2], color='#b91c1c', lw=1.4, zorder=5)
    # Badge
    ax.text(0.275, y_fk1 + 0.014, "1 : N (Country FK)", ha='center', va='bottom',
            fontsize=5.6, weight='bold', color='#b91c1c',
            bbox=dict(boxstyle="round,pad=0.18", fc="#ffffff", ec="#fca5a5", lw=0.6), zorder=6)

    # 2. entities_master (PK: entity_id) -> streaming_transactions (source_entity_id)
    y_pk_e = t2_y + t2_h - 0.098 # entity_id in Table 2 (~0.822)
    y_src = t3_y + t3_h - 0.096 - 0.046 # source_entity_id in Table 3 (~0.778)

    ax.plot([t2_x + t2_w, 0.635, 0.635, t3_x], [y_pk_e, y_pk_e, y_src, y_src], color='#0284c7', lw=1.4, zorder=5)
    # '1' tick on Table 2 side
    ax.plot([t2_x + t2_w + 0.006, t2_x + t2_w + 0.006], [y_pk_e - 0.012, y_pk_e + 0.012], color='#0284c7', lw=1.4, zorder=5)
    # Crow foot on Table 3 side
    ax.plot([t3_x - 0.010, t3_x], [y_src + 0.008, y_src], color='#0284c7', lw=1.4, zorder=5)
    ax.plot([t3_x - 0.010, t3_x], [y_src - 0.008, y_src], color='#0284c7', lw=1.4, zorder=5)
    # Badge
    ax.text(0.635, y_pk_e + 0.014, "1 : N (Source)", ha='center', va='bottom',
            fontsize=5.6, weight='bold', color='#0284c7',
            bbox=dict(boxstyle="round,pad=0.18", fc="#ffffff", ec="#7dd3fc", lw=0.6), zorder=6)

    # 3. entities_master (PK: entity_id) -> streaming_transactions (target_entity_id)
    y_tgt = t3_y + t3_h - 0.096 - (2 * 0.046) # target_entity_id in Table 3 (~0.732)

    ax.plot([t2_x + t2_w, 0.635, 0.635, t3_x], [y_pk_e - 0.015, y_pk_e - 0.015, y_tgt, y_tgt],
            color='#0f766e', lw=1.4, linestyle='--', zorder=5)
    # Crow foot on Table 3 side
    ax.plot([t3_x - 0.010, t3_x], [y_tgt + 0.008, y_tgt], color='#0f766e', lw=1.4, zorder=5)
    ax.plot([t3_x - 0.010, t3_x], [y_tgt - 0.008, y_tgt], color='#0f766e', lw=1.4, zorder=5)
    # Badge
    ax.text(0.635, y_tgt - 0.014, "1 : N (Target)", ha='center', va='top',
            fontsize=5.6, weight='bold', color='#0f766e',
            bbox=dict(boxstyle="round,pad=0.18", fc="#ffffff", ec="#5eead4", lw=0.6), zorder=6)

    # =========================================================================
    # BOTTOM ZONE: INDEX ARCHITECTURE & 12-D INVARIANT VIEW (y: 0.020 -> 0.400)
    # =========================================================================

    # -------------------------------------------------------------------------
    # LEFT CARD: Composite Time-Causal Indexes & Guarantees (x: 0.015 -> 0.485)
    # -------------------------------------------------------------------------
    b1_x, b1_y, b1_w, b1_h = 0.015, 0.020, 0.470, 0.385
    ax.add_patch(FancyBboxPatch((b1_x, b1_y), b1_w, b1_h, boxstyle='round,pad=0.008',
                                fc='#ffffff', edgecolor='#cbd5e1', lw=1.2, zorder=2))
    # Subheader
    ax.add_patch(FancyBboxPatch((b1_x + 0.004, b1_y + b1_h - 0.052), b1_w - 0.008, 0.046,
                                boxstyle='round,pad=0.003', fc='#1e293b', edgecolor='#1e293b', zorder=3))
    ax.text(b1_x + b1_w/2, b1_y + b1_h - 0.029,
            "TIME-CAUSAL COMPOSITE B-TREE INDEX ARCHITECTURE",
            ha='center', va='center', fontsize=7.2, weight='bold', color='#ffffff', zorder=4)

    # SQL Code Block
    sql_box = FancyBboxPatch((b1_x + 0.010, b1_y + 0.170), b1_w - 0.020, 0.150,
                             boxstyle='round,pad=0.004', fc='#0f172a', ec='#334155', lw=0.8, zorder=3)
    ax.add_patch(sql_box)
    
    sql_lines = [
        ("-- Vectorized Zero-Lookahead Causal Indexes", "#94a3b8", True),
        ("CREATE INDEX idx_source_time", "#38bdf8", True),
        ("  ON streaming_transactions (source_entity_id, timestamp_utc DESC);", "#f1f5f9", False),
        ("CREATE INDEX idx_target_time", "#38bdf8", True),
        ("  ON streaming_transactions (target_entity_id, timestamp_utc DESC);", "#f1f5f9", False),
    ]
    for idx, (s_text, s_color, is_kw) in enumerate(sql_lines):
        y_sql = b1_y + 0.292 - idx * 0.028
        ax.text(b1_x + 0.020, y_sql, s_text, ha='left', va='center',
                fontsize=5.8, weight='bold' if is_kw else 'normal', color=s_color, fontfamily='monospace', zorder=4)

    # Engineering Guarantees
    guarantees = [
        ("O(log |E|) Query SLA:", "Sub-millisecond 2-hop causal ego-graph extraction in < 0.18 ms", "#0284c7"),
        ("Strict Invariant:", "t_e <= t_eval strictly enforced (eliminates temporal lookahead leak)", "#dc2626"),
        ("Prefix Clustering:", "Descending epoch ordering allows zero-copy contiguous range scans", "#15803d")
    ]
    for idx, (g_title, g_desc, g_col) in enumerate(guarantees):
        y_g = b1_y + 0.125 - idx * 0.046
        ax.add_patch(FancyBboxPatch((b1_x + 0.010, y_g - 0.012), b1_w - 0.020, 0.038,
                                    boxstyle='round,pad=0.002', fc='#f8fafc', ec='#e2e8f0', lw=0.6, zorder=3))
        ax.plot([b1_x + 0.018], [y_g + 0.007], marker='s', markersize=3.5, color=g_col, zorder=4)
        ax.text(b1_x + 0.026, y_g + 0.007, g_title, ha='left', va='center',
                fontsize=6.0, weight='bold', color=g_col, zorder=4)
        ax.text(b1_x + 0.135, y_g + 0.007, g_desc, ha='left', va='center',
                fontsize=5.6, color='#334155', zorder=4)

    # -------------------------------------------------------------------------
    # RIGHT CARD: Materialized 12-D Canonical Invariant View (x: 0.515 -> 0.985)
    # -------------------------------------------------------------------------
    b2_x, b2_y, b2_w, b2_h = 0.515, 0.020, 0.470, 0.385
    ax.add_patch(FancyBboxPatch((b2_x, b2_y), b2_w, b2_h, boxstyle='round,pad=0.008',
                                fc='#ffffff', edgecolor='#cbd5e1', lw=1.2, zorder=2))
    # Subheader
    ax.add_patch(FancyBboxPatch((b2_x + 0.004, b2_y + b2_h - 0.052), b2_w - 0.008, 0.046,
                                boxstyle='round,pad=0.003', fc='#065f46', edgecolor='#065f46', zorder=3))
    ax.text(b2_x + b2_w/2, b2_y + b2_h - 0.029,
            "MATERIALIZED VIEW: v_canonical_invariants_12d",
            ha='center', va='center', fontsize=7.2, weight='bold', color='#ffffff', zorder=4)

    # View Explanation Pill
    ax.add_patch(FancyBboxPatch((b2_x + 0.010, b2_y + 0.282), b2_w - 0.020, 0.038,
                                boxstyle='round,pad=0.002', fc='#f0fdf4', ec='#86efac', lw=0.7, zorder=3))
    ax.text(b2_x + b2_w/2, b2_y + 0.301,
            "Maps Relational SQL Streams -> Universal 12-D PyG Multigraph Tensors",
            ha='center', va='center', fontsize=6.0, weight='bold', color='#166534', zorder=4)

    # 4 Mathematical Invariant Dimension Cards
    inv_cards = [
        ("1. Kirchhoff Flow Balance", r"$\Phi_{\mathrm{flow}} = \ln(1 + \sum A_{\mathrm{out}} / (\sum A_{\mathrm{in}} + \epsilon))$",
         "Pass-through mule relay (~1.0)", "#0369a1", "#f0f9ff", "#bae6fd"),
        ("2. Hawkes Burst Rate", r"$\lambda_u(t) = \mu_u + \sum_{t_i < t} \alpha e^{-\beta(t - t_i)}$",
         "Micro-burst smurfing spikes (>12.0)", "#b45309", "#fffbeb", "#fde68a"),
        ("3. Bi-Directional Taint", r"$\mathbf{s}_{\mathrm{fwd}}, \mathbf{s}_{\mathrm{bwd}} = (1-\alpha)(\mathbf{I} - \alpha \mathbf{P})^{-1} \mathbf{s}_0$",
         "Causal PageRank walk (no leak)", "#b91c1c", "#fef2f2", "#fecaca"),
        ("4. Ego Multi-Moments", r"$[\mu_A, \sigma_A^2, \gamma_A, \kappa_A] \parallel [\mathrm{deg}_{\mathrm{in}}, \mathrm{deg}_{\mathrm{out}}, v_A, \nu_{\mathrm{io}}] \in \mathbb{R}^8$",
         "Higher-order amount/time jitter", "#6d28d9", "#f5f3ff", "#ddd6fe")
    ]
    for idx, (title, formula, desc, col, bg, bdr) in enumerate(inv_cards):
        y_c = b2_y + 0.222 - idx * 0.062
        ax.add_patch(FancyBboxPatch((b2_x + 0.010, y_c - 0.012), b2_w - 0.020, 0.054,
                                    boxstyle='round,pad=0.003', fc=bg, ec=bdr, lw=0.8, zorder=3))
        ax.text(b2_x + 0.020, y_c + 0.022, title, fontsize=6.2, weight='bold', color=col, zorder=4)
        ax.text(b2_x + 0.155, y_c + 0.022, desc, fontsize=5.6, style='italic', color='#475569', zorder=4)
        ax.text(b2_x + 0.020, y_c - 0.002, formula, fontsize=5.8, weight='bold', color='#0f172a', zorder=4)

    # Bottom summary tag
    ax.text(b2_x + b2_w/2, b2_y + 0.008,
            "100% Deterministic Feature Basis: Universal Zero-Shot Cross-Ledger Compatibility",
            ha='center', va='bottom', fontsize=5.6, weight='bold', color='#065f46', zorder=4)

    return fig

if __name__ == "__main__":
    fig = create_figure_4_2()
    test_pdf = Path("test_fig4_2.pdf")
    test_png = Path("test_fig4_2.png")
    fig.savefig(test_pdf, bbox_inches='tight', pad_inches=0.15)
    fig.savefig(test_png, dpi=300, bbox_inches='tight', pad_inches=0.15)
    print("Test Figure 4.2 generated successfully.")

