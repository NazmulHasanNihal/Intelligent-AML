"""
laundering_chain_detector.py — Multi-Hop Money Laundering Typology & Chain Detector.

Detects and extracts structured graph topology signals for canonical AML patterns:
1. Fan-Out (Smurfing/Structuring dispersion from a single source)
2. Fan-In (Aggregation into mule or collector accounts)
3. Multi-Hop Stacks (Sequential A -> B -> C -> D flow layering)
4. Scatter-Gather (Fan-Out followed by rapid Fan-In)
5. Cross-Bank Boundary Hops & Payment Format Discrepancies
"""

import numpy as np
import polars as pl
import pandas as pd
from typing import Dict, Tuple, Optional


class LaunderingChainDetector:
    """
    Extracts multi-hop transaction chain dynamics and AML typology features
    per node from tabular transaction edge streams.
    """

    def __init__(self, time_window_seconds: float = 86400.0 * 7):
        self.time_window_seconds = time_window_seconds

    def extract_typology_features(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame, dataset_name: str = "") -> np.ndarray:
        """
        Extracts an 8-dimensional AML typology feature vector for each node:
        [0] cross_bank_trans_ratio (Fraction of transactions crossing bank institutions)
        [1] fan_out_intensity (Smurfing / Structuring dispersion score)
        [2] scatter_gather_score (Non-linear divergence between in/out counterparties)
        [3] layering_stack_depth (Approximated flow throughput velocity)
        [4] payment_format_entropy (Shannon diversity of payment rails)
        [5] kirchhoff_flow_divergence (Flow balance differential Delta_flow)
        [6] fan_in_intensity (Mule / Collector aggregation score)
        [7] structuring_cluster_density (Density of transactions near regulatory reporting thresholds)
        """
        num_nodes = len(nodes_df)
        feats = np.zeros((num_nodes, 12), dtype=np.float32)

        if edges_df is None or len(edges_df) == 0 or num_nodes == 0:
            return feats

        # Convert to polars for ultra-fast vectorized aggregation
        if isinstance(edges_df, pd.DataFrame):
            cols = [c for c in edges_df.columns if c in [
                "src", "dst", "ts", "timestamp", "time", "step", "amount", "Amount", "Amount Paid", 
                "Amount Received", "Payment Format", "From Bank", "To Bank", "label"
            ]]
            df = pl.from_pandas(edges_df[cols])
        else:
            df = edges_df

        src_col = "src"
        dst_col = "dst"
        if src_col not in df.columns or dst_col not in df.columns:
            return feats

        node_id_list = nodes_df["node_id"].astype(str).tolist()
        node_id_to_idx = {nid: i for i, nid in enumerate(node_id_list)}

        # 1. Cross-Bank Activity
        if "From Bank" in df.columns and "To Bank" in df.columns:
            cross_bank_df = df.with_columns(
                (pl.col("From Bank") != pl.col("To Bank")).cast(pl.Float32).alias("is_cross_bank")
            )
            src_cross = cross_bank_df.group_by(src_col).agg(
                pl.col("is_cross_bank").mean().alias("src_cb_mean")
            )
            dst_cross = cross_bank_df.group_by(dst_col).agg(
                pl.col("is_cross_bank").mean().alias("dst_cb_mean")
            )
            
            for row in src_cross.iter_rows():
                nid, cb_mean = str(row[0]), row[1]
                if nid in node_id_to_idx:
                    idx = node_id_to_idx[nid]
                    feats[idx, 0] = float(cb_mean or 0.0)
                    
            for row in dst_cross.iter_rows():
                nid, cb_mean = str(row[0]), row[1]
                if nid in node_id_to_idx:
                    idx = node_id_to_idx[nid]
                    feats[idx, 0] = max(feats[idx, 0], float(cb_mean or 0.0))

        # 2. Payment Format Rails & Exact Shannon Information Entropy
        if "Payment Format" in df.columns:
            pf_counts = df.group_by([src_col, "Payment Format"]).len()
            src_totals = df.group_by(src_col).len().rename({"len": "total_len"})
            pf_probs = pf_counts.join(src_totals, on=src_col)
            pf_probs = pf_probs.with_columns(
                (pl.col("len") / pl.col("total_len")).alias("p_k")
            ).with_columns(
                (-pl.col("p_k") * (pl.col("p_k") + 1e-12).log(2)).alias("h_k")
            )
            shannon_df = pf_probs.group_by(src_col).agg(pl.col("h_k").sum().alias("shannon_entropy"))
            for row in shannon_df.iter_rows():
                nid, h = str(row[0]), row[1]
                if nid in node_id_to_idx:
                    feats[node_id_to_idx[nid], 4] = float(h or 0.0)

        # 3. Graphlet Structural Typologies: Fan-Out, Fan-In, Scatter-Gather, Layering Depth
        src_unique_dst = df.group_by(src_col).agg(pl.col(dst_col).n_unique().alias("out_deg_unique"))
        dst_unique_src = df.group_by(dst_col).agg(pl.col(src_col).n_unique().alias("in_deg_unique"))

        out_map = {str(r[0]): float(r[1]) for r in src_unique_dst.iter_rows()}
        in_map = {str(r[0]): float(r[1]) for r in dst_unique_src.iter_rows()}

        for nid, idx in node_id_to_idx.items():
            in_d = in_map.get(nid, 0.0)
            out_d = out_map.get(nid, 0.0)
            tot_d = in_d + out_d
            if tot_d > 0.0:
                # [1] Fan-out structuring intensity: d_out / (d_in + 1)
                feats[idx, 1] = float((out_d / (in_d + 1.0)) * (1.0 if out_d >= 3.0 else 0.5))
                # [6] Fan-in mule aggregation intensity: d_in / (d_out + 1)
                feats[idx, 6] = float((in_d / (out_d + 1.0)) * (1.0 if in_d >= 3.0 else 0.5))
                # [2] Scatter-gather balance: symmetric non-linear harmonic flow
                feats[idx, 2] = float(4.0 * (in_d * out_d) / ((tot_d ** 2) + 1e-6))
                # [3] Layering stack depth
                feats[idx, 3] = float(np.log1p(min(in_d, out_d)))

        # 4. Structuring Density ($8k - $10k threshold bands) & Kirchhoff Flow Balance
        amt_col = None
        for c in ["Amount Paid", "amount", "Amount", "value", "Value"]:
            if c in df.columns:
                amt_col = c
                break

        if amt_col:
            # Structuring threshold band
            struct_df = df.with_columns(
                ((pl.col(amt_col) >= 7500.0) & (pl.col(amt_col) <= 9999.0)).cast(pl.Float32).alias("is_structuring")
            )
            struct_agg = struct_df.group_by(src_col).agg(pl.col("is_structuring").mean().alias("struct_ratio"))
            for row in struct_agg.iter_rows():
                nid, sr = str(row[0]), row[1]
                if nid in node_id_to_idx:
                    feats[node_id_to_idx[nid], 7] = float(sr or 0.0)

            # Exact Kirchhoff Flow Balance: Delta_flow = |sum_in - sum_out| / max(sum_in, sum_out)
            amt_in_df = df.group_by(dst_col).agg(pl.col(amt_col).sum().alias("amt_in"))
            amt_out_df = df.group_by(src_col).agg(pl.col(amt_col).sum().alias("amt_out"))
            amt_in_map = {str(r[0]): float(r[1] or 0.0) for r in amt_in_df.iter_rows()}
            amt_out_map = {str(r[0]): float(r[1] or 0.0) for r in amt_out_df.iter_rows()}
            
            for nid, idx in node_id_to_idx.items():
                a_in = amt_in_map.get(nid, 0.0)
                a_out = amt_out_map.get(nid, 0.0)
                max_a = max(a_in, a_out)
                tot_a = a_in + a_out
                if max_a > 0.0:
                    feats[idx, 5] = float(abs(a_in - a_out) / (max_a + 1e-6))
                    # [10] Wash Ratio: Volume to Net Balance Discrepancy
                    feats[idx, 10] = float(np.log10((tot_a + 1.0) / (abs(a_in - a_out) + 1.0)))

        # 5. Temporal Periodicity Regularity & Fast-Drain Dynamics
        ts_col = None
        for c in ["ts", "timestamp", "time", "step"]:
            if c in df.columns:
                ts_col = c
                break

        if ts_col:
            try:
                # Inter-transaction deltas per source
                time_df = df.sort([src_col, ts_col]).with_columns([
                    (pl.col(ts_col) - pl.col(ts_col).shift(1).over(src_col)).fill_null(0.0).alias("delta_t")
                ])
                time_stats = time_df.filter(pl.col("delta_t") > 0).group_by(src_col).agg([
                    pl.col("delta_t").mean().alias("mean_dt"),
                    pl.col("delta_t").std().alias("std_dt")
                ])
                for row in time_stats.iter_rows():
                    nid, m_dt, s_dt = str(row[0]), row[1] or 0.0, row[2] or 0.0
                    if nid in node_id_to_idx:
                        # [8] Periodicity Regularity Score (High for erratic mules, low for periodic payroll)
                        feats[node_id_to_idx[nid], 8] = float(s_dt / (m_dt + 1e-4))

                # [9] Fast-Drain Ratio (<24 hours holding time)
                fast_drain_df = time_df.filter(pl.col("delta_t") <= 86400.0).group_by(src_col).len().rename({"len": "fast_cnt"})
                total_cnt_df = time_df.group_by(src_col).len().rename({"len": "tot_cnt"})
                drain_ratio_df = fast_drain_df.join(total_cnt_df, on=src_col).with_columns(
                    (pl.col("fast_cnt") / pl.col("tot_cnt")).alias("drain_ratio")
                )
                for row in drain_ratio_df.iter_rows():
                    nid, dr = str(row[0]), row[3] or 0.0
                    if nid in node_id_to_idx:
                        feats[node_id_to_idx[nid], 9] = float(dr)
            except Exception:
                pass

        # 6. User-Merchant Amount Z-Score
        if amt_col:
            try:
                amt_vals = df[amt_col].to_numpy().astype(np.float64)
                m_amt = float(np.mean(amt_vals))
                s_amt = float(max(1.0, np.std(amt_vals)))
                src_max_z = df.with_columns(
                    ((pl.col(amt_col) - m_amt) / s_amt).alias("z_amt")
                ).group_by(src_col).agg(pl.col("z_amt").max().alias("max_z"))
                for row in src_max_z.iter_rows():
                    nid, mz = str(row[0]), row[1] or 0.0
                    if nid in node_id_to_idx:
                        feats[node_id_to_idx[nid], 11] = float(np.log1p(max(0.0, mz)))
            except Exception:
                pass

        return np.nan_to_num(feats, nan=0.0, posinf=1.0, neginf=0.0)

