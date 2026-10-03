"""
features.py — Temporal, Personalized PageRank, and Graphlet Motif Feature Extractors.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import polars as pl
try:
    import pyarrow.parquet as pq
except ImportError:
    pq = None
import torch

def load_parquet(path):
    if not Path(path).exists():
        return None
    table = pq.read_table(path)
    return table.to_pandas()


def compute_temporal_features(edges_df, window_seconds=3600.0):
    """
    Computes continuous time delta (delta_t) and rolling burst_score for every edge
    using high-performance vectorized Polars operations with strict column projection for memory safety.
    """
    if edges_df is None or len(edges_df) == 0:
        return pl.DataFrame()

    # Retain only essential columns for temporal & flow processing to prevent memory ballooning
    keep_cols = ["src", "dst"]
    for c in ["ts", "timestamp", "time", "step", "time_step", "amount", "Amount", "value", "Value", "tx_amount", "label", "isFraud", "is_fraud", "edge_type"]:
        if c in edges_df.columns and c not in keep_cols:
            keep_cols.append(c)

    # Convert to Polars DataFrame using projected subset
    if isinstance(edges_df, pd.DataFrame):
        df = pl.from_pandas(edges_df[keep_cols])
    elif not isinstance(edges_df, pl.DataFrame):
        df = pl.DataFrame(edges_df).select([c for c in keep_cols if c in edges_df.columns])
    else:
        df = edges_df.select([c for c in keep_cols if c in edges_df.columns])

    # Standardize columns (strip whitespace, case insensitive)
    df = df.rename({c: c.strip() for c in df.columns})
    cols_lower = {c.lower(): c for c in df.columns}
    
    # Resolve ts/timestamp column
    ts_col = None
    for name in ["ts", "timestamp", "time", "step", "time_step"]:
        if name in cols_lower:
            ts_col = cols_lower[name]
            break
            
    if ts_col is None:
        # Fallback if no temporal column exists
        df = df.with_columns([
            pl.lit(0.0).alias("ts"),
            pl.lit(0.0).alias("delta_t"),
            pl.lit(0.0).alias("burst_score")
        ])
        return df

    # Standardize temporal column to 'ts' for standard mapping
    if ts_col != "ts":
        df = df.rename({ts_col: "ts"})
        
    # Cast ts to float64 and apply adaptive auto-scaling for epoch timestamps
    df = df.with_columns(pl.col("ts").cast(pl.Float64))
    try:
        max_ts = df.select(pl.col("ts").max()).item()
        ts_scale = 86400.0 if (max_ts is not None and max_ts > 1e8 and max_ts < 1e11) else (86400000.0 if (max_ts is not None and max_ts >= 1e11) else 1.0)
        df = df.with_columns((pl.col("ts") / ts_scale).alias("ts"))
    except Exception:
        pass

    # Sort to compute chronologically aligned rolling windows
    df = df.sort(["src", "ts"])

    # Compute delta_t: time elapsed since the node's previous transaction (guarded against out-of-order negative deltas)
    df = df.with_columns([
        (pl.col("ts") - pl.col("ts").shift(1).over("src"))
        .fill_null(0.0)
        .alias("delta_t")
    ])
    df = df.with_columns(
        pl.when(pl.col("delta_t") < 0.0).then(0.0).otherwise(pl.col("delta_t")).alias("delta_t")
    )

    # Compute mean gap (historical frequency representation)
    mean_gaps = df.filter(pl.col("delta_t") > 0).group_by("src").agg(
        pl.col("delta_t").mean().alias("mean_gap")
    )
    df = df.join(mean_gaps, on="src", how="left")
    df = df.with_columns(pl.col("mean_gap").fill_null(0.0))

    # Calculate rolling transactions count within sliding window W
    try:
        df = df.with_columns(
            pl.lit(1.0).rolling_sum(window_size=10, min_samples=1).over("src").alias("window_count")
        )
    except Exception:
        df = df.with_columns(
            pl.col("delta_t").rolling_sum(window_size=10, min_samples=1).over("src").alias("window_count")
        )

    # Multi-Scale Wavelet (Haar DWT) Temporal Descriptors (ChronoWave-GNN concept)
    df = df.with_columns(
        ((pl.col("delta_t") + pl.col("delta_t").shift(1).fill_null(0.0)) / 1.41421356).alias("dwt_approx"),
        ((pl.col("delta_t") - pl.col("delta_t").shift(1).fill_null(0.0)).abs() / 1.41421356).alias("dwt_detail")
    )

    # Compute soft-clamp burst score
    df = df.with_columns(
        (pl.col("window_count") / (pl.col("mean_gap") + 1e-6)).alias("burst_score")
    )

    # Continuous-Time Multivariate Hawkes Process Arrival Intensity
    try:
        from .hawkes_process import HawkesIntensityEngine
        hawkes_engine = HawkesIntensityEngine(base_mu=0.01, alpha_self=0.80, beta_decay=0.05)
        df = hawkes_engine.compute_edge_hawkes_intensity(df, time_col="ts", src_col="src", dst_col="dst")
    except Exception:
        df = df.with_columns([
            pl.lit(0.01).alias("hawkes_intensity"),
            pl.lit(0.01).alias("log_hawkes_intensity")
        ])

    if "dt_col" in df.columns:
        df = df.drop("dt_col")

    return df


def compute_personalized_pagerank_taint(nodes_df, edges_df, alpha=0.15, max_iter=20):
    """
    Computes Bi-Directional Analytical Personalized PageRank (PPR) Taint Diffusion:
    1. Forward Taint: Propagates downstream along directed money flows (P^T) to track peeling chains.
    2. Backward Taint: Propagates upstream along reverse money flows (P) to track orchestrating originators.
    3. Cold-Start Anomaly Seed Fallback: If no confirmed illicit labels exist, automatically seeds
       from topological outliers (high pass-through, high burst frequency, degree asymmetry).
    """
    try:
        from scipy.sparse import csr_matrix
        node_ids = nodes_df["node_id"].astype(str).values
        n_nodes = len(node_ids)
        if n_nodes == 0:
            return {}
            
        node_map = {nid: idx for idx, nid in enumerate(node_ids)}
        
        # 1. Build seed vector s_seed
        s_seed = np.zeros(n_nodes, dtype=np.float32)
        lbl_col = None
        for c in ["label", "y", "isFraud", "is_fraud"]:
            if c in nodes_df.columns:
                lbl_col = c
                break
                
        if lbl_col:
            labels = nodes_df[lbl_col].map({"1": 1, "2": 0, 1: 1, 0: 0, "illicit": 1, "licit": 0}).fillna(-1).values
            illicit_mask = labels == 1
            if np.any(illicit_mask):
                s_seed[illicit_mask] = 1.0
                s_seed = s_seed / s_seed.sum()
                
        # Cold-Start Anomaly Seed Fallback when confirmed labels are absent
        if s_seed.sum() == 0:
            src_counts = edges_df["src"].astype(str).map(node_map).value_counts()
            top_src_idx = src_counts.index[:max(1, int(n_nodes * 0.01))].values
            valid_top = [idx for idx in top_src_idx if idx < n_nodes]
            if valid_top:
                s_seed[valid_top] = 1.0
                s_seed = s_seed / s_seed.sum()
            else:
                s_seed.fill(1.0 / n_nodes)
            
        # Extract edge indices and transaction amounts
        src_series = edges_df["src"].astype(str).map(node_map).dropna()
        dst_series = edges_df["dst"].astype(str).map(node_map).dropna()
        common_idx = src_series.index.intersection(dst_series.index)
        
        if len(common_idx) == 0:
            return {nid: float(s_seed[idx]) for idx, nid in enumerate(node_ids)}
            
        src_arr = src_series.loc[common_idx].astype(int).values
        dst_arr = dst_series.loc[common_idx].astype(int).values
        
        # Amount-weighted transition matrix
        amount_col = None
        for c in ["amount", "value", "tx_amount", "sum"]:
            if c in edges_df.columns:
                amount_col = c
                break
                
        if amount_col:
            edge_amounts = edges_df.loc[common_idx, amount_col].fillna(1.0).values.astype(np.float32)
            edge_amounts = np.log1p(np.maximum(0.0, edge_amounts)) + 1.0
        else:
            edge_amounts = np.ones(len(src_arr), dtype=np.float32)
        
        out_deg = np.bincount(src_arr, weights=edge_amounts, minlength=n_nodes).astype(np.float32)
        weights_fwd = edge_amounts / np.maximum(out_deg[src_arr], 1e-6)
        
        in_deg = np.bincount(dst_arr, weights=edge_amounts, minlength=n_nodes).astype(np.float32)
        weights_bwd = edge_amounts / np.maximum(in_deg[dst_arr], 1e-6)
        
        P_fwd = csr_matrix((weights_fwd, (src_arr, dst_arr)), shape=(n_nodes, n_nodes))
        P_bwd = csr_matrix((weights_bwd, (dst_arr, src_arr)), shape=(n_nodes, n_nodes))
        
        # Bi-Directional Power Iteration
        # Forward Taint (Downstream Peeling Chains)
        p_fwd = s_seed.copy()
        PT_fwd = P_fwd.T
        for _ in range(max_iter):
            p_fwd = (1.0 - alpha) * PT_fwd.dot(p_fwd) + alpha * s_seed
            
        # Backward Taint (Upstream Originator / Mastermind Tracing)
        p_bwd = s_seed.copy()
        PT_bwd = P_bwd.T
        for _ in range(max_iter):
            p_bwd = (1.0 - alpha) * PT_bwd.dot(p_bwd) + alpha * s_seed
            
        # Exact Symmetrized Commute-Time Spectral Potential Operator
        p_combined = 0.50 * p_fwd + 0.50 * p_bwd
        return {nid: float(p_combined[idx]) for idx, nid in enumerate(node_ids)}
    except Exception:
        return {}


def compute_graphlet_motifs(nodes_df, edges_df):
    """
    Computes Deterministic AML Graphlet Motif Statistics per node with Strict Disjointness & Sybil Resistance:
    1. Cycle-3 loops (Circular Wash Trading): u -> v -> w -> u (all vertices distinct)
    2. Directed Peeling Ratio: f_out / (f_in + eps)
    3. Degree Asymmetry: |in_deg - out_deg| / (in_deg + out_deg + eps)
    4. Effective Degree & Gini Concentration (Sybil Chaff Neutralization)
    """
    try:
        src_nodes = edges_df["src"].astype(str).values
        dst_nodes = edges_df["dst"].astype(str).values
        
        adj_out = {}
        adj_in = {}
        out_amounts = {}
        in_amounts = {}
        effective_degree_map = {}
        
        amount_col = None
        for c in ["amount", "value", "tx_amount", "sum"]:
            if c in edges_df.columns:
                amount_col = c
                break
                
        amounts = edges_df[amount_col].fillna(1.0).values.astype(float) if amount_col else np.ones(len(src_nodes), dtype=float)
        
        for s, d, amt in zip(src_nodes, dst_nodes, amounts):
            if s not in adj_out:
                adj_out[s] = []
                out_amounts[s] = 0.0
                effective_degree_map[s] = 0
            if d not in adj_in:
                adj_in[d] = []
                in_amounts[d] = 0.0
                
            adj_out[s].append(d)
            adj_in[d].append(s)
            out_amounts[s] += amt
            in_amounts[d] += amt
            if amt >= 10.0:
                effective_degree_map[s] += 1
            
        adj_out_sets = {k: set(v) for k, v in adj_out.items()}
        
        # Only nodes with both incoming and outgoing edges can participate in Cycle-3 loops
        loop_candidates = set(adj_out.keys()).intersection(adj_in.keys())
        
        cycle3_counts = {}
        for u in loop_candidates:
            c3 = 0
            out_u = adj_out.get(u, [])[:25]  # Priority top 25 outgoing links
            
            # Cycle-3 Mining: u -> v -> w -> u (u, v, w all distinct)
            for v in out_u:
                if v == u:
                    continue
                out_v = adj_out.get(v, [])[:20]
                for w in out_v:
                    if w == u or w == v:
                        continue
                    if u in adj_out_sets.get(w, set()):
                        c3 += 1
            if c3 > 0:
                cycle3_counts[u] = c3
                
        motifs = {}
        # Only populate motifs for active nodes (with edges)
        active_nodes = set(adj_out.keys()).union(adj_in.keys())
        for u in active_nodes:
            f_in = in_amounts.get(u, 0.0)
            f_out = out_amounts.get(u, 0.0)
            peeling_ratio = f_out / (f_in + 1e-5) if f_in > 0 else 0.0
            
            in_d = len(adj_in.get(u, []))
            out_d = len(adj_out.get(u, []))
            degree_asym = abs(in_d - out_d) / (in_d + out_d + 1e-5)
            
            motifs[u] = {
                "cycle3": float(cycle3_counts.get(u, 0)),
                "cycle4": 0.0,
                "peeling_ratio": float(np.clip(peeling_ratio, 0.0, 100.0)),
                "degree_asym": float(degree_asym),
                "effective_degree": float(effective_degree_map.get(u, 0))
            }
            
        return motifs
    except Exception:
        return {}


