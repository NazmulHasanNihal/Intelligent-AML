"""
Figure 4.2: Relational Database Schema and Entity-Relationship Architecture
Standalone publication script for C-STGB monograph.
Clean, human-designed ERD with zero mathematical clutter, zero SQL code, and crisp relational tables.
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

def draw_erd_table(ax, x, y, w, h, table_name, fields, col_header, col_bg):
    """Draws a clean, publication-grade ERD table with PK/FK indicators."""
    # Outer box
    ax.add_patch(patches.Rectangle((x, y), w, h, facecolor="#ffffff", edgecolor=col_header, lw=1.3, zorder=2))
    
    # Header Banner
    header_h = 0.055
    ax.add_patch(patches.Rectangle((x, y + h - header_h), w, header_h, facecolor=col_header, edgecolor=col_header, zorder=3))
    ax.text(x + w/2, y + h - header_h/2, table_name, ha="center", va="center", fontsize=7.8, fontweight="bold", color="#ffffff", zorder=4)

    # Row fields
    n_fields = len(fields)
    row_h = (h - header_h - 0.015) / n_fields
    for i, (key_type, col_name, data_type) in enumerate(fields):
        ry = y + h - header_h - 0.010 - (i + 1) * row_h
        
        # Subtle zebra striping
        if i % 2 == 1:
            ax.add_patch(patches.Rectangle((x + 0.003, ry), w - 0.006, row_h, facecolor="#f8fafc", edgecolor="none", zorder=2))

        # Key badge
        if key_type == "PK":
            ax.add_patch(patches.Rectangle((x + 0.008, ry + row_h*0.18), 0.024, row_h*0.64, facecolor="#dc2626", edgecolor="none", zorder=4))
            ax.text(x + 0.020, ry + row_h/2, "PK", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#ffffff", zorder=5)
        elif key_type == "FK":
            ax.add_patch(patches.Rectangle((x + 0.008, ry + row_h*0.18), 0.024, row_h*0.64, facecolor="#0284c7", edgecolor="none", zorder=4))
            ax.text(x + 0.020, ry + row_h/2, "FK", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#ffffff", zorder=5)

        # Field Name
        ax.text(x + 0.038, ry + row_h/2, col_name, ha="left", va="center", fontsize=6.6,
                fontweight="bold" if key_type != "" else "normal", color=COLOR_DARK, zorder=4)
        # Data Type
        ax.text(x + w - 0.010, ry + row_h/2, data_type, ha="right", va="center", fontsize=6.0, color="#64748b", zorder=4)

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.8)
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.axis("off")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    # Top Master Banner
    ax.add_patch(patches.Rectangle(
        (0.012, 0.915), 0.976, 0.070,
        facecolor="#0f172a", edgecolor="#1e293b", lw=1.2
    ))
    ax.text(0.50, 0.957, "Relational Entity-Relationship Diagram (ERD) & Surveillance Data Model",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="#ffffff")
    ax.text(0.50, 0.930, "Physical Database Schema: Account Masters -> Streaming Edges -> Precomputed Invariants -> Triage Dossiers",
            ha="center", va="center", fontsize=7.2, color="#94a3b8")

    # =========================================================================
    # 4 CORE RELATIONAL ENTITY TABLES (1:1 with Listing C.1 DDL Contracts)
    # =========================================================================

    # Table 1: entities_master (Master Customer & Node Entity)
    t1_fields = [
        ("PK", "entity_id", "VARCHAR(64)"),
        ("  ", "entity_name", "VARCHAR(128)"),
        ("FK", "country_iso", "VARCHAR(3)"),
        ("  ", "kyc_risk_tier", "INTEGER"),
        ("  ", "account_created_epoch", "BIGINT"),
        ("  ", "baseline_volume_usd", "DECIMAL(18,2)"),
    ]
    t1_x, t1_y, t1_w, t1_h = 0.04, 0.50, 0.28, 0.38
    draw_erd_table(ax, t1_x, t1_y, t1_w, t1_h, "TABLE: entities_master", t1_fields, COLOR_INGEST, COLOR_INGEST_BG)

    # Table 2: streaming_transactions (Directed Multigraph Edge Stream)
    t2_fields = [
        ("PK", "transaction_id", "VARCHAR(64)"),
        ("FK", "source_entity_id", "VARCHAR(64)"),
        ("FK", "target_entity_id", "VARCHAR(64)"),
        ("  ", "amount_usd", "DECIMAL(18,2)"),
        ("  ", "timestamp_epoch", "BIGINT"),
        ("  ", "payment_rail", "VARCHAR(32)"),
    ]
    t2_x, t2_y, t2_w, t2_h = 0.68, 0.50, 0.28, 0.38
    draw_erd_table(ax, t2_x, t2_y, t2_w, t2_h, "TABLE: streaming_transactions", t2_fields, COLOR_RISK, COLOR_RISK_BG)

    # Table 3: high_risk_jurisdictions (FATF Regulatory & Sanctions Registry)
    t3_fields = [
        ("PK", "country_iso", "VARCHAR(3)"),
        ("  ", "fatf_status", "VARCHAR(32)"),
        ("  ", "corruption_index", "FLOAT"),
        ("  ", "sanctions_flag", "BOOLEAN"),
    ]
    t3_x, t3_y, t3_w, t3_h = 0.04, 0.10, 0.28, 0.32
    draw_erd_table(ax, t3_x, t3_y, t3_w, t3_h, "TABLE: high_risk_jurisdictions", t3_fields, COLOR_REVIEW, COLOR_REVIEW_BG)

    # Table 4: v_canonical_invariants_12d (Analytical View over Causal Ego-Graphs)
    t4_fields = [
        ("FK", "entity_id", "VARCHAR(64)"),
        ("  ", "eval_timestamp", "BIGINT"),
        ("  ", "phi_flow, psi_asym", "FLOAT (12-D)"),
        ("  ", "lambda_hawkes, s_fwd", "FLOAT (12-D)"),
        ("  ", "s_bwd, mu_a, sigma_a", "FLOAT (12-D)"),
        ("  ", "skew_a, kurt_a, nu_io", "FLOAT (12-D)"),
        ("  ", "sigma_dt, capital_v", "FLOAT (12-D)"),
    ]
    t4_x, t4_y, t4_w, t4_h = 0.68, 0.08, 0.28, 0.36
    draw_erd_table(ax, t4_x, t4_y, t4_w, t4_h, "VIEW: v_canonical_invariants_12d", t4_fields, COLOR_GNN, COLOR_GNN_BG)

    # =========================================================================
    # RELATIONSHIP CONNECTORS (Clean, orthogonal crow's foot lines)
    # =========================================================================

    # 1. entities_master -> streaming_transactions (1 : N for Source and Target)
    y_rel_tx = 0.70
    ax.plot([t1_x + t1_w, 0.50, 0.50, t2_x], [y_rel_tx + 0.05, y_rel_tx + 0.05, y_rel_tx + 0.05, y_rel_tx + 0.05],
            color=COLOR_INGEST, lw=1.6, zorder=3)
    ax.plot([t1_x + t1_w, 0.50, 0.50, t2_x], [y_rel_tx - 0.05, y_rel_tx - 0.05, y_rel_tx - 0.05, y_rel_tx - 0.05],
            color="#0284c7", lw=1.6, linestyle="--", zorder=3)

    # Relationship Badge 1
    ax.add_patch(patches.Rectangle((0.41, y_rel_tx + 0.015), 0.18, 0.075, facecolor="#ffffff", edgecolor=COLOR_BORDER, lw=0.9, zorder=5))
    ax.text(0.50, y_rel_tx + 0.065, "1 : N (Source Entity)", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_INGEST, zorder=6)
    ax.text(0.50, y_rel_tx + 0.035, "1 : N (Target Entity)", ha="center", va="center", fontsize=6.2, fontweight="bold", color="#0284c7", zorder=6)

    # 2. high_risk_jurisdictions -> entities_master (1 : N country lookup)
    x_rel_jur = t1_x + t1_w * 0.40
    ax.plot([x_rel_jur, x_rel_jur], [t3_y + t3_h, t1_y], color=COLOR_REVIEW, lw=1.6, zorder=3)
    ax.add_patch(patches.Rectangle((x_rel_jur - 0.075, 0.445), 0.15, 0.035, facecolor="#ffffff", edgecolor=COLOR_REVIEW, lw=0.8, zorder=5))
    ax.text(x_rel_jur, 0.462, "1 : N (Jurisdiction)", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_REVIEW, zorder=6)

    # 3. entities_master -> v_canonical_invariants_12d (1 : 1 materialized feature vector)
    x_rel_inv = t2_x + t2_w * 0.40
    ax.plot([x_rel_inv, x_rel_inv], [t2_y, t4_y + t4_h], color=COLOR_GNN, lw=1.6, zorder=3)
    ax.add_patch(patches.Rectangle((x_rel_inv - 0.075, 0.455), 0.15, 0.035, facecolor="#ffffff", edgecolor=COLOR_GNN, lw=0.8, zorder=5))
    ax.text(x_rel_inv, 0.472, "1 : 1 (12-D Invariants)", ha="center", va="center", fontsize=6.2, fontweight="bold", color=COLOR_GNN, zorder=6)

    # Center Feature View Box (Zero code, pure high-level architecture)
    ax.add_patch(patches.Rectangle(
        (0.35, 0.12), 0.30, 0.28,
        facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.2, zorder=2
    ))
    ax.add_patch(patches.Rectangle(
        (0.35, 0.35), 0.30, 0.05,
        facecolor="#1e293b", edgecolor="#1e293b", zorder=3
    ))
    ax.text(0.50, 0.375, "COLUMNAR STORAGE & INDEXES", ha="center", va="center",
            fontsize=7.2, fontweight="bold", color="#ffffff", zorder=4)

    storage_points = [
        "DuckDB Columnar Parquet Engine",
        "Apache Arrow Zero-Copy Memory",
        "Time-Causal Composite B-Tree Indexes",
        "Sub-Millisecond 2-Hop Graph Lookups",
        "Immutable WORM Ledger Integration"
    ]
    for sp_idx, sp_txt in enumerate(storage_points):
        spy = 0.315 - sp_idx * 0.045
        ax.plot(0.37, spy, marker="s", markersize=3.5, color=COLOR_INGEST, zorder=4)
        ax.text(0.385, spy, sp_txt, ha="left", va="center", fontsize=6.4, color=COLOR_DARK, zorder=4)

    save_figure(fig, "fig4_2_database_erd", pad_inches=0.10)
    plt.close(fig)

if __name__ == "__main__":
    generate()
