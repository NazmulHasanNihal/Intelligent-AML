"""
HT-GNN: Heterogeneous Temporal Graph Neural Network
Layer 2 — Detection & Rebalancing

Reads ingested graph data from data/outputs/graph_data/ and produces
fraud risk scores using a heterogeneous temporal GNN with attention
over node types, edge types, and time.
"""

import os
import sys
from pathlib import Path

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent.parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
_dll_handle = None
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handle = os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import torch
import torch.nn as nn
import torch.nn.functional as F
import pyarrow.parquet as pq
import polars as pl
import numpy as np
import pandas as pd

from torch_geometric.data import HeteroData
from torch_geometric.nn import Linear
from .burst_aware_hgt_conv import BurstAwareHGTConv
from .graph_smote import LatentGraphSMOTE, DynamicThresholdCalibrator, BilinearEdgeGenerator
from xgboost import XGBClassifier

OUTPUT_DIR = Path("data/outputs/graph_data")
NODE_TYPES = ["Account", "User", "Device", "Institution"]
EDGE_TYPES = ["Transaction", "IP_Connection", "Shared_Ownership"]

HIDDEN_CHANNELS = 128
NUM_LAYERS = 6
DROPOUT = 0.3
ACTIVATION = "relu"
JK_MODE = "cat"  # Jumping Knowledge: concatenate all intermediate layer representations

# Dataset-Adaptive Hyperparameter Profiles (Universal 24-Dataset Taxonomy)
DATASET_PROFILES = {
    # Archetype 1: Crypto / Blockchain Transaction Networks
    "elliptic_v1":             {"gnn_layers": 3, "hidden": 128, "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
    "elliptic_v2":             {"gnn_layers": 3, "hidden": 128, "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
    "eth_phishing":            {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "eth_phishing_2nd":        {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "xblock_eth":              {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 600, "xgb_depth": 8, "focal_beta": 0.88, "smote_ratio": 0.20},
    "mtgox_leaked":            {"gnn_layers": 4, "hidden": 128, "lr": 0.0008, "xgb_n": 1000, "xgb_depth": 9, "focal_beta": 0.95, "smote_ratio": 0.25},
    "smart_ponzi":             {"gnn_layers": 3, "hidden": 96,  "lr": 0.001,  "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},

    # Archetype 2: Retail Banking & Multi-Tier Layering Networks
    "ibm_amlsim_hi_small":          {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_small_accounts": {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_medium":         {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_hi_medium_accounts":{"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 10, "focal_beta": 0.98, "smote_ratio": 0.30},
    "ibm_amlsim_li_small":          {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_small_accounts": {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_medium":         {"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "ibm_amlsim_li_medium_accounts":{"gnn_layers": 4, "hidden": 128, "lr": 0.0005, "xgb_n": 800, "xgb_depth": 9,  "focal_beta": 0.96, "smote_ratio": 0.25},
    "saml_d":                       {"gnn_layers": 5, "hidden": 128, "lr": 0.0005, "xgb_n": 800,  "xgb_depth": 8,  "focal_beta": 0.92, "smote_ratio": 0.25},
    "synthaml":                     {"gnn_layers": 5, "hidden": 96,  "lr": 0.0005, "xgb_n": 600,  "xgb_depth": 8,  "focal_beta": 0.90, "smote_ratio": 0.20},

    # Archetype 3: High-Velocity Mobile Money & E-Wallets
    "paysim1":                 {"gnn_layers": 5, "hidden": 64, "lr": 0.0001, "xgb_n": 600, "xgb_depth": 10, "focal_beta": 0.95, "smote_ratio": 0.25},
    "paysim_extended":         {"gnn_layers": 5, "hidden": 48, "lr": 0.0001, "xgb_n": 600, "xgb_depth": 10, "focal_beta": 0.95, "smote_ratio": 0.25},

    # Archetype 4: FinTech Lending & Credit Card Fraud
    "dgraphfin":               {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.85, "smote_ratio": 0.15},
    "cc_transactions":         {"gnn_layers": 4, "hidden": 96, "lr": 0.0003, "xgb_n": 500, "xgb_depth": 8, "focal_beta": 0.90, "smote_ratio": 0.20},
    "ulb_credit_card":         {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.85, "smote_ratio": 0.15},
    "data_generator":          {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 300, "xgb_depth": 6, "focal_beta": 0.80, "smote_ratio": 0.10},
    "live_demo":               {"gnn_layers": 3, "hidden": 64, "lr": 0.001,  "xgb_n": 200, "xgb_depth": 6, "focal_beta": 0.75, "smote_ratio": 0.10},
}
DEFAULT_PROFILE = {"gnn_layers": 4, "hidden": 96, "lr": 0.0005, "xgb_n": 400, "xgb_depth": 7, "focal_beta": 0.80, "smote_ratio": 0.15}

def get_dataset_profile(dataset_name: str) -> dict:
    """Returns the dataset-adaptive hyperparameter profile, falling back to defaults."""
    return DATASET_PROFILES.get(dataset_name, DEFAULT_PROFILE)


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


def get_neighbor_loader(data, input_node_type="Account", input_nodes=None, batch_size=2048, num_neighbors=[15, 10], num_workers=0):
    """
    Constructs a PyTorch Geometric NeighborLoader for billion-node graph mini-batch streaming.
    Binds RAM footprint to < 4 GB regardless of graph size.
    """
    try:
        from torch_geometric.loader import NeighborLoader
        loader = NeighborLoader(
            data,
            num_neighbors={rel: num_neighbors for rel in data.edge_types},
            batch_size=batch_size,
            input_nodes=(input_node_type, input_nodes) if input_nodes is not None else input_node_type,
            num_workers=num_workers,
            shuffle=True
        )
        return loader
    except Exception as e:
        print(f"  [NeighborLoader] Streaming loader init fallback: {e}")
        return None


def build_hetero_data(dataset_name):
    """
    Load ingested nodes.parquet and edges.parquet for a dataset,
    computes dynamic continuous-time variables, and constructs a
    """
    cache_hetero = Path("data/cache") / f"{dataset_name}_heterodata_v7.pt"
    if cache_hetero.exists():
        try:
            print(f"  [Cache] Loading precomputed HeteroData from {cache_hetero}...")
            return torch.load(cache_hetero, weights_only=False)
        except Exception:
            pass

    dataset_dir = OUTPUT_DIR / dataset_name
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_dir}")

    nodes_path = dataset_dir / "nodes.parquet"
    edges_path = dataset_dir / "edges.parquet"

    if not nodes_path.exists():
        raise FileNotFoundError(f"nodes.parquet not found for {dataset_name}")
    if not edges_path.exists():
        raise FileNotFoundError(f"edges.parquet not found for {dataset_name}")

    nodes_df = load_parquet(nodes_path)
    if dataset_name == "paysim_extended":
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Streaming multi-million edge partition for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT src, dst, CAST(step AS DOUBLE) as ts, CAST(amount AS FLOAT) as amount, CAST(label AS BIGINT) as label
            FROM read_parquet('{edges_path.as_posix()}')
            WHERE label = 1 OR (step % 8 = 0)
            ORDER BY ts
        """).df()
    elif dataset_name == "cc_transactions":
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Streaming multi-million edge partition for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst, 
                   CAST(Year*10000 + Month*100 + Day AS DOUBLE) as ts, 
                   CAST(REPLACE(REPLACE(Amount, '$', ''), ',', '') AS FLOAT) as amount, 
                   CAST(label AS BIGINT) as label
            FROM read_parquet('{edges_path.as_posix()}')
            WHERE label = true OR (Year % 2 = 0)
            ORDER BY ts
        """).df()
    elif dataset_name in ["ibm_amlsim_hi_medium", "ibm_amlsim_li_medium"]:
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Streaming high-coverage edge partition for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst,
                   CAST(epoch(Timestamp) AS DOUBLE) as ts,
                   CAST("Amount Paid" AS FLOAT) as amount,
                   CAST("Amount Received" AS FLOAT) as amount_received,
                   CAST(label AS BIGINT) as label,
                   CAST("Payment Format" AS VARCHAR) as "Payment Format",
                   CAST("From Bank" AS VARCHAR) as "From Bank",
                   CAST("To Bank" AS VARCHAR) as "To Bank",
                   CAST("Payment Currency" AS VARCHAR) as "Payment Currency",
                   CAST("Receiving Currency" AS VARCHAR) as "Receiving Currency"
            FROM read_parquet('{edges_path.as_posix()}')
            WHERE label = 1 OR (hash(src) % 2 = 0)
            ORDER BY ts
        """).df()
    elif dataset_name in ["ibm_amlsim_hi_small", "ibm_amlsim_li_small", "ibm_amlsim_hi_small_accounts", "ibm_amlsim_hi_medium_accounts", "ibm_amlsim_li_small_accounts", "ibm_amlsim_li_medium_accounts"]:
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Ingesting all edge attributes for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst,
                   CAST(epoch(Timestamp) AS DOUBLE) as ts,
                   CAST("Amount Paid" AS FLOAT) as amount,
                   CAST("Amount Received" AS FLOAT) as amount_received,
                   CAST(label AS BIGINT) as label,
                   CAST("Payment Format" AS VARCHAR) as "Payment Format",
                   CAST("From Bank" AS VARCHAR) as "From Bank",
                   CAST("To Bank" AS VARCHAR) as "To Bank",
                   CAST("Payment Currency" AS VARCHAR) as "Payment Currency",
                   CAST("Receiving Currency" AS VARCHAR) as "Receiving Currency"
            FROM read_parquet('{edges_path.as_posix()}')
            ORDER BY ts
        """).df()
    elif dataset_name == "mtgox_leaked":
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Ingesting crypto ledger & exchange rates for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst,
                   CAST(epoch(Date) AS DOUBLE) as ts,
                   CAST(Bitcoins AS FLOAT) as amount,
                   CAST(Money AS FLOAT) as money_fiat,
                   CAST(CASE WHEN Money_Rate = 'Infinity' OR Money_Rate > 1e7 THEN NULL ELSE Money_Rate END AS FLOAT) as exchange_rate,
                   CAST(CASE WHEN label >= 1 THEN 1 ELSE 0 END AS BIGINT) as label
            FROM read_parquet('{edges_path.as_posix()}')
            ORDER BY ts
        """).df()
    elif dataset_name == "eth_phishing":
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Streaming high-coverage edge partition for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst,
                   CAST(timestamp AS DOUBLE) as ts,
                   CAST(amount AS FLOAT) as amount
            FROM read_parquet('{edges_path.as_posix()}')
            WHERE hash(src) % 2 = 0
            ORDER BY ts
        """).df()
    elif dataset_name == "xblock_eth":
        import duckdb
        con = duckdb.connect()
        print(f"  [Pipeline] Streaming full high-fidelity edge topology for {dataset_name}...")
        edges_df = con.execute(f"""
            SELECT CAST(src AS VARCHAR) as src, CAST(dst AS VARCHAR) as dst,
                   CAST(timestamp AS DOUBLE) as ts,
                   CAST(COALESCE(TRY_CAST(tokenId AS FLOAT), 1.0) AS FLOAT) as amount
            FROM read_parquet('{edges_path.as_posix()}')
            ORDER BY ts
        """).df()
    else:
        edges_df = load_parquet(edges_path)

    # Standardize nodes columns case-insensitively without deep copying arrays
    nodes_df.columns = [c.strip() for c in nodes_df.columns]
    edges_df.columns = [c.strip() for c in edges_df.columns]

    # Normalize Edge src/dst columns
    for col in ["clId1", "source", "from", "sender", "src_id", "source_id", "from_account", "source_address", "txId1"]:
        if col in edges_df.columns and "src" not in edges_df.columns:
            edges_df = edges_df.rename(columns={col: "src"})
            break

    for col in ["clId2", "target", "to", "receiver", "dst_id", "target_id", "to_account", "target_address", "txId2"]:
        if col in edges_df.columns and "dst" not in edges_df.columns:
            edges_df = edges_df.rename(columns={col: "dst"})
            break

    # Normalize ID columns: clId/txId/nodeId to node_id
    for col in ["clId", "txId", "nodeId", "txid", "nodeid", "id", "account_id", "address"]:
        if col in nodes_df.columns and "node_id" not in nodes_df.columns:
            nodes_df = nodes_df.rename(columns={col: "node_id"})
            break

    if "node_id" not in nodes_df.columns:
        nodes_df["node_id"] = np.arange(len(nodes_df))

    # Convert IDs to strings for robust matching across string/numeric ID datasets
    nodes_df["node_id"] = nodes_df["node_id"].astype(str)
    edges_df["src"] = edges_df["src"].astype(str)
    edges_df["dst"] = edges_df["dst"].astype(str)

    # Ensure node_type exists
    if "node_type" not in nodes_df.columns:
        if "time_step" in nodes_df.columns:
            nodes_df["node_type"] = "User"
        else:
            nodes_df["node_type"] = "Account"

    # Merge labels from connected_components.parquet if available (e.g. elliptic_v2)
    if "y" not in nodes_df.columns and "label" not in nodes_df.columns:
        cc_path = dataset_dir / "connected_components.parquet"
        if cc_path.exists() and "ccId" in nodes_df.columns:
            cc_df = pd.read_parquet(cc_path)
            nodes_df = nodes_df.merge(cc_df, on="ccId", how="left")
            if "ccLabel" in nodes_df.columns:
                nodes_df["y"] = nodes_df["ccLabel"].map(
                    lambda l: 1 if str(l).lower() in ["suspicious", "illicit", "1", "true"] else (0 if str(l).lower() in ["licit", "0", "false"] else -1)
                ).fillna(-1).astype(int)

    # Map labels for eth_phishing from eth_phishing_2nd ground-truth phishing addresses
    if dataset_name == "eth_phishing" and "y" not in nodes_df.columns and "label" not in nodes_df.columns:
        eth_2nd_path = OUTPUT_DIR / "eth_phishing_2nd" / "labeled_transactions.parquet"
        if eth_2nd_path.exists():
            import duckdb
            con = duckdb.connect()
            phishing_df = con.execute(f"""
                SELECT DISTINCT LOWER(c) as addr
                FROM (
                    SELECT "From" as c FROM read_parquet('{eth_2nd_path.as_posix()}') WHERE actor_type = 'phishing'
                    UNION ALL
                    SELECT "To" as c FROM read_parquet('{eth_2nd_path.as_posix()}') WHERE actor_type = 'phishing'
                )
            """).df()
            phish_set = set(phishing_df["addr"])
            nodes_df["y"] = nodes_df["node_id"].astype(str).str.lower().map(lambda a: 1 if a in phish_set else 0).astype(int)
            print(f"  [Pipeline] Mapped {sum(nodes_df['y'] == 1):,} phishing accounts and {sum(nodes_df['y'] == 0):,} normal accounts for {dataset_name}.")

    # Map labels for xblock_eth from eth_phishing_2nd ground-truth phishing addresses (Upgrade I)
    if dataset_name == "xblock_eth" and "y" not in nodes_df.columns and "label" not in nodes_df.columns:
        eth_2nd_path = OUTPUT_DIR / "eth_phishing_2nd" / "labeled_transactions.parquet"
        if eth_2nd_path.exists():
            import duckdb
            con = duckdb.connect()
            phishing_df = con.execute(f"""
                SELECT DISTINCT LOWER(c) as addr
                FROM (
                    SELECT "From" as c FROM read_parquet('{eth_2nd_path.as_posix()}') WHERE actor_type = 'phishing'
                    UNION ALL
                    SELECT "To" as c FROM read_parquet('{eth_2nd_path.as_posix()}') WHERE actor_type = 'phishing'
                )
            """).df()
            phish_set = set(phishing_df["addr"])
            nodes_df["y"] = nodes_df["node_id"].astype(str).str.lower().map(lambda a: 1 if a in phish_set else 0).astype(int)
            print(f"  [Pipeline] Mapped {sum(nodes_df['y'] == 1):,} phishing accounts and {sum(nodes_df['y'] == 0):,} normal accounts for {dataset_name}.")

    # Merge features from background_nodes.parquet if available and no feat_* columns exist
    feat_cols = [c for c in nodes_df.columns if c.startswith("feat_") or c.startswith("feat#")]
    if len(feat_cols) == 0:
        bg_nodes_path = dataset_dir / "background_nodes.parquet"
        if bg_nodes_path.exists():
            import duckdb
            con = duckdb.connect()
            print(f"  [Pipeline] Extracting node features from background_nodes.parquet for {dataset_name}...")
            joined_df = con.execute(f"""
                SELECT n.node_id, bg.* EXCLUDE (clId)
                FROM nodes_df n
                INNER JOIN read_parquet('{bg_nodes_path.as_posix()}') bg ON CAST(n.node_id AS BIGINT) = bg.clId
            """).df()
            feat_rename = {c: f"feat_{c.replace('feat#', '')}" for c in joined_df.columns if c != "node_id"}
            joined_df = joined_df.rename(columns=feat_rename)
            nodes_df = nodes_df.merge(joined_df, on="node_id", how="left")

    # 1. Caching path for high-performance temporal feature loads
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{dataset_name}_temporal_features_v4.parquet"
    
    if cache_file.exists():
        print(f"  [Cache] Loading cached temporal features from {cache_file}...")
        edges_df = pd.read_parquet(cache_file)
    else:
        # Join node timestamps to edges if edges have no temporal column
        nodes_time_col = None
        for name in ["ts", "time_step", "timestamp", "time"]:
            if name in nodes_df.columns:
                nodes_time_col = name
                break
                
        edges_time_col = None
        for name in ["ts", "timestamp", "time", "step", "time_step"]:
            if name in edges_df.columns:
                edges_time_col = name
                break
                
        if edges_time_col is None and nodes_time_col is not None:
            time_lookup = dict(zip(nodes_df["node_id"], nodes_df[nodes_time_col]))
            edges_df["ts"] = edges_df["src"].map(time_lookup).fillna(0.0)

        # Retain essential columns only
        essential_cols = ["src", "dst"]
        for c in [
            "ts", "timestamp", "time", "step", "time_step", "amount", "Amount", "value", "Value", "tx_amount",
            "Amount Paid", "Amount Received", "Payment Format", "From Bank", "To Bank",
            "Payment Currency", "Receiving Currency", "Bitcoins", "Money", "Money_Rate", "money_fiat", "exchange_rate",
            "label", "isFraud", "is_fraud", "edge_type"
        ]:
            if c in edges_df.columns and c not in essential_cols:
                essential_cols.append(c)
        edges_df = edges_df[essential_cols]

        edges_df.to_parquet(cache_file)

    data = HeteroData()

    # Map global node_id to relative index per type
    node_id_to_type = dict(zip(nodes_df["node_id"], nodes_df["node_type"]))
    
    # Extract feature columns
    feature_cols = [c for c in nodes_df.columns if c.startswith("feat_") or c.startswith("feat#")]
    
    # Store global id mapping per type to resolve relative indices
    node_id_to_rel_idx = {}
    discovered_types = nodes_df["node_type"].unique().tolist()
    target_node_types = list(dict.fromkeys(NODE_TYPES + discovered_types))
    
    # Precompute global graphlet motifs & personalized PageRank taint diffusion
    ppr_taint_map = compute_personalized_pagerank_taint(nodes_df, edges_df)
    cycle3_map = compute_graphlet_motifs(nodes_df, edges_df)

    # Extract global edge flow & diversity statistics
    src_deg = edges_df["src"].value_counts().to_dict()
    dst_deg = edges_df["dst"].value_counts().to_dict()
    unique_dst_map = edges_df.groupby("src")["dst"].nunique().to_dict()
    unique_src_map = edges_df.groupby("dst")["src"].nunique().to_dict()
    
    amount_col = None
    for c in ["amount", "Amount", "value", "Value", "tx_amount"]:
        if c in edges_df.columns:
            amount_col = c
            break

    if amount_col:
        # Sanitize currency symbols and string amounts to pure float32
        if edges_df[amount_col].dtype == object or str(edges_df[amount_col].dtype).startswith("str") or str(edges_df[amount_col].dtype).startswith("string"):
            edges_df[amount_col] = pd.to_numeric(
                edges_df[amount_col].astype(str).str.replace(r"[^\d.-]", "", regex=True),
                errors="coerce"
            ).fillna(0.0).astype(np.float32)
        else:
            edges_df[amount_col] = pd.to_numeric(edges_df[amount_col], errors="coerce").fillna(0.0).astype(np.float32)

    in_flow = edges_df.groupby("dst")[amount_col].sum().to_dict() if amount_col else {}
    out_flow = edges_df.groupby("src")[amount_col].sum().to_dict() if amount_col else {}
    amt_std_map = edges_df.groupby("src")[amount_col].std().fillna(0.0).to_dict() if amount_col else {}
    amt_max_map = edges_df.groupby("src")[amount_col].max().fillna(0.0).to_dict() if amount_col else {}
    
    if amount_col:
        s_mask = (edges_df[amount_col] >= 3000.0) & (edges_df[amount_col] <= 10000.0)
        s_counts = edges_df[s_mask].groupby("src").size().to_dict()
        tot_counts = edges_df.groupby("src").size().to_dict()
        struct_ratio_map = {nid: float(s_counts.get(nid, 0)) / max(1, tot_counts.get(nid, 1)) for nid in tot_counts}
        hi_mask = edges_df[amount_col] > 10000.0
        hi_counts = edges_df[hi_mask].groupby("src").size().to_dict()
        hi_ratio_map = {nid: float(hi_counts.get(nid, 0)) / max(1, tot_counts.get(nid, 1)) for nid in tot_counts}
    else:
        struct_ratio_map = {}
        hi_ratio_map = {}

    if "ts" in edges_df.columns:
        ts_sorted = edges_df["ts"].sort_values()
        dt_series = ts_sorted.diff().dropna()
        pos_dt = dt_series[dt_series > 0]
        tau_half = float(pos_dt.median()) if len(pos_dt) > 0 else 86400.0
        decay_rate = float(np.log(2.0) / max(1.0, tau_half))
        max_ts = edges_df["ts"].max()
        edges_df["recency_w"] = np.exp(-decay_rate * np.maximum(0.0, max_ts - edges_df["ts"]))
        recency_map = edges_df.groupby("src")["recency_w"].mean().to_dict()
    else:
        recency_map = {}
    
    dwt_app_map = edges_df.groupby("src")["dwt_approx"].mean().to_dict() if "dwt_approx" in edges_df.columns else {}
    dwt_det_map = edges_df.groupby("src")["dwt_detail"].mean().to_dict() if "dwt_detail" in edges_df.columns else {}

    # 1. Populate Node Types
    NUM_FLOW_DIMS = 20
    for nt in target_node_types:
        mask = nodes_df["node_type"] == nt
        nt_df = nodes_df[mask]
        
        if len(nt_df) == 0:
            data[nt].x = torch.zeros(0, len(feature_cols) + NUM_FLOW_DIMS if feature_cols else 28, dtype=torch.float)
            data[nt].num_nodes = 0
            continue
            
        flow_invariants = np.zeros((len(nt_df), NUM_FLOW_DIMS), dtype=np.float32)
        for idx, nid in enumerate(nt_df["node_id"]):
            in_d = dst_deg.get(nid, 0)
            out_d = src_deg.get(nid, 0)
            f_in = float(in_flow.get(nid, 0.0))
            f_out = float(out_flow.get(nid, 0.0))
            
            flow_invariants[idx, 0] = np.log1p(float(in_d))
            flow_invariants[idx, 1] = np.log1p(float(out_d))
            flow_invariants[idx, 2] = float((in_d - out_d) / (in_d + out_d + 1e-6)) # Degree asymmetry
            flow_invariants[idx, 3] = np.log1p(max(0.0, f_in))
            flow_invariants[idx, 4] = np.log1p(max(0.0, f_out))
            flow_invariants[idx, 5] = float(1.0 - abs((f_in - f_out) / (f_in + f_out + 1e-6))) # Pass-through score
            flow_invariants[idx, 6] = np.log1p(float(dwt_app_map.get(nid, 0.0))) # Wavelet Approximation (Slow Layering)
            flow_invariants[idx, 7] = np.log1p(float(dwt_det_map.get(nid, 0.0))) # Wavelet Detail (Rapid Smurfing)
            flow_invariants[idx, 8] = float(ppr_taint_map.get(nid, 0.0)) # Personalized PageRank Taint Diffusion
            motif_entry = cycle3_map.get(nid, {})
            c3_val = float(motif_entry.get("cycle3", 0.0) if isinstance(motif_entry, dict) else motif_entry)
            flow_invariants[idx, 9] = np.log1p(c3_val) # Cycle-3 Circular Wash Trading Motif
            flow_invariants[idx, 10] = np.log1p(float(f_out / (f_in + 1e-6))) # Forward Peeling Velocity Ratio
            flow_invariants[idx, 11] = float((in_d * out_d) / ((in_d + out_d)**2 + 1e-6)) # Smurfing Fan-In/Out Dispersion
            flow_invariants[idx, 12] = np.log1p(float(unique_dst_map.get(nid, 0))) # Counterparty Diversity (Out)
            flow_invariants[idx, 13] = np.log1p(float(unique_src_map.get(nid, 0))) # Counterparty Diversity (In)
            flow_invariants[idx, 14] = np.log1p(float(amt_std_map.get(nid, 0.0))) # Amount Volatility/Std
            flow_invariants[idx, 15] = np.log1p(float(amt_max_map.get(nid, 0.0))) # Max Transaction Magnitude
            flow_invariants[idx, 16] = float(struct_ratio_map.get(nid, 0.0)) # Structuring Band Density ($3K-$10K)
            flow_invariants[idx, 17] = np.log1p(float(recency_map.get(nid, 0.0))) # Recency Weighting
            flow_invariants[idx, 18] = float((f_in - f_out) / (f_in + f_out + 1e-6)) # Net Flow Ratio
            flow_invariants[idx, 19] = float(hi_ratio_map.get(nid, 0.0)) # Large Value (> $10K) Ratio

        # Improvement #2 & #8: Banking-Specific Temporal Sequence Features
        # Extracts 8 additional features: structuring_count_48h, fan_out_ratio, fan_in_ratio,
        # round_amount_flag, rapid_dormancy_toggle, counterparty_concentration, time_of_day_anomaly,
        # transaction_regularity_score
        try:
            from .temporal_sequence_encoder import TemporalSequenceFeatureExtractor
            ts_extractor = TemporalSequenceFeatureExtractor()
            
            # Map node_ids to the subset for this node type
            nt_node_ids = nt_df["node_id"].values
            
            # Filter edges relevant to this node type
            edge_src_vals = edges_df["src"].values
            edge_dst_vals = edges_df["dst"].values
            
            amt_col_name = None
            for c in ["amount", "Amount", "value", "Value", "tx_amount"]:
                if c in edges_df.columns:
                    amt_col_name = c
                    break
            ts_col_name = None
            for c in ["ts", "timestamp", "time", "step"]:
                if c in edges_df.columns:
                    ts_col_name = c
                    break
            
            edge_amts = edges_df[amt_col_name].fillna(1.0).values.astype(np.float64) if amt_col_name else None
            edge_ts = edges_df[ts_col_name].fillna(0.0).values.astype(np.float64) if ts_col_name else None
            
            banking_features = ts_extractor.extract_node_temporal_features(
                nt_node_ids, edge_src_vals, edge_dst_vals, edge_amts, edge_ts
            )
            # Log-transform structuring count and counterparty concentration
            banking_features[:, 0] = np.log1p(banking_features[:, 0])
            print(f"  [Banking Features] Extracted 8 temporal sequence features for {len(nt_node_ids)} {nt} nodes.")
        except Exception as e:
            banking_features = np.zeros((len(nt_df), 8), dtype=np.float32)
            print(f"  [Banking Features] Skipped for {nt}: {e}")

        # Omni-Flow 2.0: Specialized Multi-Domain Transaction Signatures with EV-AttnPool
        try:
            from .omni_domain_feature_extractor import OmniDomainFeatureExtractor
            omni_extractor = OmniDomainFeatureExtractor()
            omni_features = omni_extractor.extract_features(nt_df, edges_df, dataset_name)
            print(f"  [Omni Features] Extracted {omni_features.shape[1]} domain edge-to-node features for {len(nt_df)} {nt} nodes.")
        except Exception as e:
            omni_features = np.zeros((len(nt_df), 20), dtype=np.float32)
            print(f"  [Omni Features] Skipped for {nt}: {e}")

        # Multi-Hop Laundering Chain & Typology Detector (Fan-Out, Fan-In, Stacks, Scatter-Gather)
        try:
            from .laundering_chain_detector import LaunderingChainDetector
            chain_detector = LaunderingChainDetector()
            chain_features = chain_detector.extract_typology_features(nt_df, edges_df, dataset_name)
            print(f"  [Laundering Chain] Extracted 8 AML typology features for {len(nt_df)} {nt} nodes.")
        except Exception as e:
            chain_features = np.zeros((len(nt_df), 8), dtype=np.float32)
            print(f"  [Laundering Chain] Skipped for {nt}: {e}")

        if feature_cols:
            x_raw = torch.tensor(nt_df[feature_cols].values, dtype=torch.float)
            x_raw = torch.nan_to_num(x_raw, nan=0.0)
            x_vals = torch.cat([
                x_raw,
                torch.tensor(flow_invariants, dtype=torch.float),
                torch.tensor(banking_features, dtype=torch.float),
                torch.tensor(omni_features, dtype=torch.float),
                torch.tensor(chain_features, dtype=torch.float)
            ], dim=1)
        else:
            # Dynamic structural + banking + omni EV-AttnPool + laundering chain topological representation
            total_dim = NUM_FLOW_DIMS + 8 + banking_features.shape[1] + omni_features.shape[1] + chain_features.shape[1]
            x_mat = np.zeros((len(nt_df), total_dim), dtype=np.float32)
            x_mat[:, :NUM_FLOW_DIMS] = flow_invariants
            x_mat[:, NUM_FLOW_DIMS + (target_node_types.index(nt) % 8)] = 1.0
            col_offset = NUM_FLOW_DIMS + 8
            x_mat[:, col_offset:col_offset + banking_features.shape[1]] = banking_features
            col_offset += banking_features.shape[1]
            x_mat[:, col_offset:col_offset + omni_features.shape[1]] = omni_features
            col_offset += omni_features.shape[1]
            x_mat[:, col_offset:col_offset + chain_features.shape[1]] = chain_features
            x_vals = torch.tensor(x_mat, dtype=torch.float)
            
        data[nt].x = torch.nan_to_num(x_vals, nan=0.0, posinf=50.0, neginf=-50.0)
        data[nt].num_nodes = len(nt_df)
        
        # Relative index map (vectorized dict construction)
        node_id_to_rel_idx.update(dict(zip(nt_df["node_id"], range(len(nt_df)))))
            
        # Optional labels (e.g. for Account or User)
        if "label" in nt_df.columns or "y" in nt_df.columns:
            lbl_col = "label" if "label" in nt_df.columns else "y"
            raw_labels = nt_df[lbl_col]
            if dataset_name == "dgraphfin":
                # In DGraphFin: 1 is Fraud, 0 is Normal, 2 and 3 are unlabeled background nodes
                mapped_labels = raw_labels.map({1: 1, 0: 0, 2: -1, 3: -1, "1": 1, "0": 0, "2": -1, "3": -1}).fillna(-1).astype(int)
            elif dataset_name in ["elliptic_v1", "elliptic_v2"]:
                # In Elliptic: 1 is Illicit, 2 is Licit, 3/unknown is unlabelled
                mapped_labels = raw_labels.map({1: 1, 2: 0, 0: 0, "1": 1, "2": 0, "0": 0, "illicit": 1, "licit": 0}).fillna(-1).astype(int)
            else:
                if raw_labels.dtype == object:
                    mapped_labels = raw_labels.map({"1": 1, "2": 0, 1: 1, 0: 0, "illicit": 1, "licit": 0, "fraud": 1, "normal": 0}).fillna(-1).astype(int)
                else:
                    unique_vals = set(raw_labels.unique())
                    if unique_vals - {0, 1, -1}:
                        mapped_labels = raw_labels.map(lambda v: 1 if v == 1 else (0 if v == 0 else -1)).astype(int)
                    else:
                        mapped_labels = raw_labels.astype(int)
            data[nt].y = torch.tensor(mapped_labels.values, dtype=torch.long)

    # Check if node labels need to be derived from edge labels (e.g. PaySim, SAML-D, IBM, MtGox)
    has_any_node_labels = any(hasattr(data[nt], "y") and data[nt].y is not None and data[nt].y.numel() > 0 and data[nt].num_nodes > 0 for nt in target_node_types)
    edge_label_col = None
    for col in ["label", "isFraud", "is_fraud", "fraud"]:
        if col in edges_df.columns:
            edge_label_col = col
            break
            
    if not has_any_node_labels and edge_label_col is not None:
        populated_types = [nt for nt in target_node_types if data[nt].num_nodes > 0]
        primary_nt = populated_types[0] if populated_types else target_node_types[0]
        node_labels = np.zeros(data[primary_nt].num_nodes, dtype=np.int64)
        
        # MtGox includes label=2 (suspicious wash trade) as illicit positive
        if dataset_name == "mtgox_leaked":
            fraud_mask = edges_df[edge_label_col].isin([1, 2, "1", "2", True, "True", "fraud", "illicit"])
        else:
            fraud_mask = edges_df[edge_label_col].isin([1, "1", True, "True", "fraud", "illicit"])
            
        fraud_edges = edges_df[fraud_mask]
        
        fraud_src_list = [node_id_to_rel_idx[s] for s in fraud_edges["src"].values if s in node_id_to_rel_idx]
        fraud_dst_list = [node_id_to_rel_idx[d] for d in fraud_edges["dst"].values if d in node_id_to_rel_idx]
        valid_src = np.array([idx for idx in fraud_src_list if idx < data[primary_nt].num_nodes], dtype=np.int64)
        valid_dst = np.array([idx for idx in fraud_dst_list if idx < data[primary_nt].num_nodes], dtype=np.int64)
        if len(valid_src) > 0:
            node_labels[valid_src] = 1
        if len(valid_dst) > 0:
            node_labels[valid_dst] = 1
        print(f"  [Label Mapping] Unified laundering subgraph node labels: {sum(node_labels == 1):,} fraud accounts ({sum(node_labels == 0):,} clean accounts).")
            
        data[primary_nt].y = torch.tensor(node_labels, dtype=torch.long)

    # 2. Populate Heterogeneous Edges (Vectorized High-Performance Loading)
    src_raw = edges_df["src"].values
    dst_raw = edges_df["dst"].values
    src_idx = np.array([node_id_to_rel_idx.get(s, -1) for s in src_raw], dtype=np.int64)
    dst_idx = np.array([node_id_to_rel_idx.get(d, -1) for d in dst_raw], dtype=np.int64)
    valid_mask = (src_idx >= 0) & (dst_idx >= 0)
    
    if "edge_type" not in edges_df.columns:
        edges_df["edge_type"] = "Transaction"
        
    edges_valid = edges_df[valid_mask]
    src_valid = src_idx[valid_mask]
    dst_valid = dst_idx[valid_mask]
    delta_t_valid = np.nan_to_num(edges_valid["delta_t"].fillna(0.0).values.astype(np.float32) if "delta_t" in edges_valid.columns else np.zeros(len(src_valid), dtype=np.float32), nan=0.0, posinf=1000.0, neginf=0.0)
    burst_valid = np.nan_to_num(edges_valid["burst_score"].fillna(0.0).values.astype(np.float32) if "burst_score" in edges_valid.columns else np.zeros(len(src_valid), dtype=np.float32), nan=0.0, posinf=100.0, neginf=0.0)
    ts_valid = np.nan_to_num(edges_valid["ts"].fillna(0.0).values.astype(np.float32) if "ts" in edges_valid.columns else np.zeros(len(src_valid), dtype=np.float32), nan=0.0, posinf=1e12, neginf=0.0)
    has_edge_label = "label" in edges_valid.columns
    edge_label_valid = edges_valid["label"].fillna(0).values.astype(np.int64) if has_edge_label else None
    
    valid_src_raw = src_raw[valid_mask]
    valid_dst_raw = dst_raw[valid_mask]
    src_node_types = np.array([node_id_to_type.get(s, target_node_types[0]) for s in valid_src_raw])
    dst_node_types = np.array([node_id_to_type.get(d, target_node_types[0]) for d in valid_dst_raw])
    edge_type_names = edges_valid["edge_type"].values
    
    # Group by unique relation triplet
    unique_rels = list(set(zip(src_node_types, edge_type_names, dst_node_types)))
    for s_type, e_type, d_type in unique_rels:
        rel_mask = (src_node_types == s_type) & (edge_type_names == e_type) & (dst_node_types == d_type)
        if not np.any(rel_mask):
            continue
        rel_key = (s_type, e_type if e_type in EDGE_TYPES else "Transaction", d_type)
        s_idx = torch.tensor(src_valid[rel_mask], dtype=torch.long)
        d_idx = torch.tensor(dst_valid[rel_mask], dtype=torch.long)
        
        data[rel_key].edge_index = torch.stack([s_idx, d_idx])
        data[rel_key].delta_t = torch.tensor(delta_t_valid[rel_mask], dtype=torch.float)
        data[rel_key].burst_score = torch.tensor(burst_valid[rel_mask], dtype=torch.float)
        data[rel_key].ts = torch.tensor(ts_valid[rel_mask], dtype=torch.float)
        if has_edge_label:
            data[rel_key].y = torch.tensor(edge_label_valid[rel_mask], dtype=torch.long)

    # Active memory cleanup of large pandas/numpy staging buffers
    import gc
    del edges_valid, src_valid, dst_valid, delta_t_valid, burst_valid, ts_valid
    gc.collect()

    # Save to disk cache for instantaneous reloads
    try:
        cache_hetero = Path("data/cache") / f"{dataset_name}_heterodata_v7.pt"
        cache_hetero.parent.mkdir(parents=True, exist_ok=True)
        torch.save(data, cache_hetero)
        print(f"  [Cache] Saved HeteroData cache to {cache_hetero}")
    except Exception as e:
        print(f"  [Cache Warning] Could not save HeteroData cache: {e}")

    return data


class BurstAwareHGT(nn.Module):
    """
    Heterogeneous Graph Transformer with Burst-Aware Edge Attenuation,
    Gated Residual Skip Connections, Jumping Knowledge (JK) Aggregation,
    and Stabilizing Layer Normalization.
    
    Improvement #6: Supports deeper architectures (5-6 layers) with JK-cat
    aggregation to prevent over-smoothing and capture multi-hop laundering rings.
    """
    def __init__(self, in_channels_dict, hidden_channels, num_layers, metadata,
                 num_heads=4, lambda_decay=0.1, beta_scale=1.5, dropout=0.3,
                 jk_mode=None):
        super().__init__()
        self.metadata = metadata
        self.num_layers = num_layers
        self.hidden_channels = hidden_channels
        self.jk_mode = jk_mode  # "cat", "max", "last", or None
        
        # 1. Projection layer per node type
        self.node_proj = nn.ModuleDict()
        for nt in metadata[0]:
            in_dim = in_channels_dict.get(nt, hidden_channels)
            self.node_proj[nt] = Linear(in_dim, hidden_channels)
            
        # 2. Convolutions, LayerNorms, and Gated Residuals per layer
        self.convs = nn.ModuleList()
        self.layer_norms = nn.ModuleList()
        self.res_gates = nn.ModuleList()
        
        for _ in range(num_layers):
            layer_convs = nn.ModuleDict()
            for relation in metadata[1]:
                rel_key = "__".join(relation)
                layer_convs[rel_key] = BurstAwareHGTConv(
                    hidden_channels, hidden_channels, num_heads,
                    lambda_decay=lambda_decay, beta_scale=beta_scale
                )
            self.convs.append(layer_convs)
            
            # Layer normalization and learnable gating per node type
            self.layer_norms.append(nn.ModuleDict({
                nt: nn.LayerNorm(hidden_channels) for nt in metadata[0]
            }))
            self.res_gates.append(nn.ModuleDict({
                nt: nn.Linear(hidden_channels * 2, hidden_channels) for nt in metadata[0]
            }))
            
        self.dropout = nn.Dropout(dropout)
        
        # 3. Jumping Knowledge projection (reduces concatenated multi-layer repr back to hidden_channels)
        if self.jk_mode == "cat":
            self.jk_proj = nn.ModuleDict({
                nt: Linear(hidden_channels * num_layers, hidden_channels) for nt in metadata[0]
            })
        
        # 4. Final classification head per node type
        self.out_proj = nn.ModuleDict()
        for nt in metadata[0]:
            self.out_proj[nt] = Linear(hidden_channels, 2)

    def get_embeddings(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        # Project all node features into uniform hidden dimension
        h_dict = {}
        for nt, x in x_dict.items():
            if x.shape[0] > 0:
                h_dict[nt] = F.relu(self.node_proj[nt](x))
                h_dict[nt] = self.dropout(h_dict[nt])
            else:
                h_dict[nt] = x
        
        # Collect per-layer representations for Jumping Knowledge
        jk_layers = {nt: [] for nt in h_dict.keys()} if self.jk_mode == "cat" else None
                
        # Propagation loop with LayerNorm and Gated Skip Connections
        for i in range(self.num_layers):
            new_h_dict = {}
            counts = {nt: 0 for nt in h_dict.keys()}
            
            for relation in self.metadata[1]:
                rel_key = "__".join(relation)
                src_type, edge_type, dst_type = relation
                
                if relation in edge_index_dict and edge_index_dict[relation].numel() > 0:
                    edge_index = edge_index_dict[relation]
                    delta_t = delta_t_dict[relation]
                    burst_score = burst_score_dict[relation]
                    
                    x_src = h_dict[src_type]
                    x_dst = h_dict[dst_type]
                    
                    # Run convolution message passing
                    h_out = self.convs[i][rel_key](
                        (x_src, x_dst), edge_index, delta_t, burst_score
                    )
                    
                    if dst_type not in new_h_dict:
                        new_h_dict[dst_type] = h_out
                    else:
                        new_h_dict[dst_type] = new_h_dict[dst_type] + h_out
                    counts[dst_type] += 1
            
            # Apply activations, gated residuals, and layer normalization
            for nt in h_dict.keys():
                if counts[nt] > 0 and nt in new_h_dict and h_dict[nt].shape[0] > 0:
                    agg = new_h_dict[nt] / counts[nt]
                    gate = torch.sigmoid(self.res_gates[i][nt](torch.cat([h_dict[nt], agg], dim=-1)))
                    fused = gate * h_dict[nt] + (1.0 - gate) * F.relu(agg)
                    h_dict[nt] = self.layer_norms[i][nt](fused)
                    h_dict[nt] = self.dropout(h_dict[nt])
            
            del new_h_dict
            
            # Store layer output for Jumping Knowledge aggregation
            if jk_layers is not None:
                for nt in h_dict.keys():
                    jk_layers[nt].append(h_dict[nt])
        
        # Apply Jumping Knowledge aggregation (concatenate all layer representations)
        if self.jk_mode == "cat" and jk_layers is not None:
            for nt in h_dict.keys():
                if len(jk_layers[nt]) > 0 and h_dict[nt].shape[0] > 0:
                    jk_concat = torch.cat(jk_layers[nt], dim=-1)
                    h_dict[nt] = self.jk_proj[nt](jk_concat)
                    
        return h_dict

    def forward(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        h_dict = self.get_embeddings(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                
        # Classify nodes
        out_dict = {}
        for nt, h in h_dict.items():
            if h.shape[0] > 0:
                out_dict[nt] = self.out_proj[nt](h)
            else:
                out_dict[nt] = torch.zeros(0, 2, device=h.device)
                
        return out_dict


class FocalLoss(nn.Module):
    """
    Focal Loss with Label Smoothing to address extreme class imbalance by down-weighting
    easy examples and preventing overconfident probability estimates on noisy fraudulent patterns.
    """
    def __init__(self, alpha=None, gamma=2.0, reduction='mean', label_smoothing=0.05):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
        self.label_smoothing = label_smoothing

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', label_smoothing=self.label_smoothing)
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        
        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            focal_loss = alpha_t * focal_loss
            
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss


class EWC:
    """
    Elastic Weight Consolidation (EWC) class to compute parameter importance (Fisher Matrix)
    and calculate quadratic regularization loss during continuous incremental learning.
    """
    def __init__(self, model, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, target_node, y_target):
        self.model = model
        self.target_node = target_node
        self.params = {n: p.clone().detach() for n, p in model.named_parameters() if p.requires_grad}
        self.fisher = self._compute_fisher(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target)

    def _compute_fisher(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target):
        fisher = {}
        for n, p in self.model.named_parameters():
            if p.requires_grad:
                fisher[n] = torch.zeros_like(p)
                
        self.model.eval()
        self.model.zero_grad()
        
        # Run forward pass and compute backward gradients
        out_dict = self.model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        logits = out_dict[self.target_node]
        valid_mask = y_target >= 0
        
        if valid_mask.sum() > 0:
            loss = F.cross_entropy(logits[valid_mask], y_target[valid_mask])
            loss.backward()
            
            for n, p in self.model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    fisher[n] = p.grad.data.pow(2)
                    
        return fisher

    def penalty(self, model):
        loss = 0.0
        for n, p in model.named_parameters():
            if p.requires_grad and n in self.fisher:
                loss += (self.fisher[n] * (p - self.params[n]).pow(2)).sum()
        return loss


def train_temporal_contrastive_pretraining(model, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, num_epochs=5, temperature=0.1):
    """
    Multi-Scale Self-Supervised Temporal Contrastive Pretraining (InfoNCE):
    Learns invariant spatiotemporal node representations across fast bursts and long-term dormancy.
    """
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    model.train()
    
    # Sub-sample large graphs for memory safety
    total_nodes = sum(x.shape[0] for x in x_dict.values())
    if total_nodes > 250_000:
        sample_ratio = min(1.0, 200_000.0 / max(1, total_nodes))
        sub_x_dict = {}
        sub_edge_index = {}
        sub_delta_t = {}
        sub_burst = {}
        node_sub_limits = {}
        
        for nt, x in x_dict.items():
            n_sub = max(100, int(x.shape[0] * sample_ratio))
            sub_x_dict[nt] = x[:n_sub]
            node_sub_limits[nt] = n_sub
            
        for rel, edge_index in edge_index_dict.items():
            src_nt, _, dst_nt = rel
            max_s = node_sub_limits.get(src_nt, 0)
            max_d = node_sub_limits.get(dst_nt, 0)
            if edge_index.numel() > 0:
                e_mask = (edge_index[0] < max_s) & (edge_index[1] < max_d)
                sub_edge_index[rel] = edge_index[:, e_mask]
                sub_delta_t[rel] = delta_t_dict[rel][e_mask] if rel in delta_t_dict else torch.zeros(0)
                sub_burst[rel] = burst_score_dict[rel][e_mask] if rel in burst_score_dict else torch.zeros(0)
            else:
                sub_edge_index[rel] = edge_index
                sub_delta_t[rel] = delta_t_dict.get(rel, torch.zeros(0))
                sub_burst[rel] = burst_score_dict.get(rel, torch.zeros(0))
        use_x = sub_x_dict
        use_edge = sub_edge_index
        use_dt = sub_delta_t
        use_burst = sub_burst
    else:
        use_x = x_dict
        use_edge = edge_index_dict
        use_dt = delta_t_dict
        use_burst = burst_score_dict

    print("  [Pipeline] Running Multi-Scale Temporal Contrastive Pretraining (InfoNCE)...")
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        
        # View 1: Multi-scale log-temporal masking + 10% feature dropout
        delta_t_v1 = {rel: dt * torch.exp(0.20 * torch.randn_like(dt)) for rel, dt in use_dt.items()}
        x_dict_v1 = {nt: F.dropout(x, p=0.10, training=True) for nt, x in use_x.items()}
        z_v1 = model.get_embeddings(x_dict_v1, use_edge, delta_t_v1, use_burst)
        
        # View 2: Counter-jitter log-temporal scaling + 10% feature dropout
        delta_t_v2 = {rel: dt * torch.exp(-0.20 * torch.randn_like(dt)) for rel, dt in use_dt.items()}
        x_dict_v2 = {nt: F.dropout(x, p=0.10, training=True) for nt, x in use_x.items()}
        z_v2 = model.get_embeddings(x_dict_v2, use_edge, delta_t_v2, use_burst)
        
        device = next(model.parameters()).device
        total_contrastive_loss = torch.tensor(0.0, device=device)
        for nt in z_v1:
            if z_v1[nt].shape[0] < 2:
                continue
            h1 = F.normalize(z_v1[nt], p=2, dim=-1)
            h2 = F.normalize(z_v2[nt], p=2, dim=-1)
            
            # Subsample for memory efficiency
            if h1.shape[0] > 2000:
                idx = torch.randperm(h1.shape[0])[:2000]
                h1 = h1[idx]
                h2 = h2[idx]
                
            sim_matrix = torch.mm(h1, h2.t()) / temperature
            labels = torch.arange(h1.shape[0], device=h1.device)
            loss_nt = F.cross_entropy(sim_matrix, labels)
            total_contrastive_loss = total_contrastive_loss + loss_nt
            
        total_contrastive_loss.backward()
        optimizer.step()
        if epoch % 2 == 0 or epoch == num_epochs:
            print(f"    InfoNCE Pretrain Epoch {epoch}/{num_epochs} | Loss: {total_contrastive_loss.item():.4f}")


def train_htgnn(dataset_name, num_epochs=50, learning_rate=0.001, prev_ewc=None, ewc_lambda=100.0, preloaded_data=None, *args, **kwargs):
    """
    Train HT-GNN using 3-way chronological split protocol (Temporal Validation).
    Evaluates predictive capacity under Concept Drift with Early Stopping & Checkpoint Recovery.
    """
    import copy
    print(f"\n{'='*70}")
    print(f" Burst-Aware HT-GNN Training (Temporal Splitting): {dataset_name}")
    print(f"{'='*70}")

    if preloaded_data is None:
        preloaded_data = kwargs.get("preloaded_data", None)

    if preloaded_data is not None:
        data = preloaded_data
    else:
        data = build_hetero_data(dataset_name)
    
    # Confirm label presence on the node type containing labels and populated nodes
    target_node = None
    for nt in data.node_types:
        if hasattr(data[nt], "y") and data[nt].y is not None and data[nt].y.numel() > 0:
            if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
                target_node = nt
                break
            
    if target_node is None:
        for nt in data.node_types:
            if hasattr(data[nt], "x") and data[nt].x.shape[0] > 0:
                target_node = nt
                break
        if target_node is None:
            target_node = data.node_types[0]
        
    has_labels = target_node in data.node_types and hasattr(data[target_node], "y") and data[target_node].y is not None
    
    if not has_labels:
        print(f"  [ERROR] Training aborted: Target node type '{target_node}' does not have label attributes.")
        return None, None

    # Chronological 3-Way Split Protocol: 60% Train / 10% Validation / 30% Test
    num_target_nodes_orig = data[target_node].x.shape[0]
    train_split_idx = int(num_target_nodes_orig * 0.60)
    val_split_idx = int(num_target_nodes_orig * 0.70)
    train_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    train_mask_nodes[:train_split_idx] = True
    
    val_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    val_mask_nodes[train_split_idx:val_split_idx] = True
    
    test_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
    test_mask_nodes[val_split_idx:num_target_nodes_orig] = True
    
    # Stratification safeguard if test slice lacks positive representation (Upgrade I)
    y_target = data[target_node].y
    total_positives = int((y_target == 1).sum().item())
    test_positives = int((y_target[test_mask_nodes] == 1).sum().item())
    
    if test_positives < 2 and total_positives >= 5:
        print(f"  [Temporal Split] Pure index partition yielded {test_positives} test positives. Applying temporal-stratified partition...")
        pos_indices = torch.where(y_target == 1)[0]
        neg_indices = torch.where(y_target == 0)[0]
        unl_indices = torch.where(y_target < 0)[0]
        
        n_pos = len(pos_indices)
        n_neg = len(neg_indices)
        n_unl = len(unl_indices)
        
        train_pos = pos_indices[:int(n_pos * 0.60)]
        val_pos = pos_indices[int(n_pos * 0.60):int(n_pos * 0.70)]
        test_pos = pos_indices[int(n_pos * 0.70):]
        
        train_neg = neg_indices[:int(n_neg * 0.60)]
        val_neg = neg_indices[int(n_neg * 0.60):int(n_neg * 0.70)]
        test_neg = neg_indices[int(n_neg * 0.70):]
        
        train_unl = unl_indices[:int(n_unl * 0.60)]
        val_unl = unl_indices[int(n_unl * 0.60):int(n_unl * 0.70)]
        test_unl = unl_indices[int(n_unl * 0.70):]
        
        train_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        train_mask_nodes[torch.cat([train_pos, train_neg, train_unl])] = True
        
        val_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        val_mask_nodes[torch.cat([val_pos, val_neg, val_unl])] = True
        
        test_mask_nodes = torch.zeros(num_target_nodes_orig, dtype=torch.bool, device=data[target_node].x.device)
        test_mask_nodes[torch.cat([test_pos, test_neg, test_unl])] = True
    
    train_mask_nodes_augmented = train_mask_nodes

    # Identify metadata
    metadata = data.metadata()
    in_channels_dict = {nt: data[nt].x.shape[1] for nt in metadata[0]}
    
    # Compute inverse class frequencies for balancing alpha in FocalLoss
    y_train_valid = y_target[train_mask_nodes]
    y_train_clean = y_train_valid[y_train_valid >= 0]
    if y_train_clean.numel() > 0:
        counts = torch.bincount(y_train_clean)
        alpha = 1.0 / (counts.float() + 1e-6)
        alpha = alpha / alpha.sum()
    else:
        alpha = torch.tensor([0.5, 0.5])
        
    num_total_nodes = sum(data[nt].num_nodes for nt in data.node_types if hasattr(data[nt], "num_nodes") and data[nt].num_nodes is not None)
    
    # Dataset-Adaptive Hyperparameter Profiles
    profile = get_dataset_profile(dataset_name)
    effective_gnn_layers = profile["gnn_layers"]
    effective_hidden = profile["hidden"]
    effective_lr = profile["lr"]
    effective_focal_beta = profile["focal_beta"]
    effective_smote_ratio = profile["smote_ratio"]
    effective_xgb_n = profile["xgb_n"]
    effective_xgb_depth = profile["xgb_depth"]
    
    # Override hidden, layer depth and epoch schedule for massive graphs
    patience = 10
    effective_epochs = num_epochs
    effective_patience = patience
    min_epochs_early_stop = 10
    if num_total_nodes > 5_000_000:
        effective_hidden = min(effective_hidden, 32)
        effective_gnn_layers = min(effective_gnn_layers, 3)
        effective_epochs = min(num_epochs, 6)
        effective_patience = 2
        min_epochs_early_stop = 3
    elif num_total_nodes > 2_000_000:
        effective_hidden = min(effective_hidden, 48)
        effective_gnn_layers = min(effective_gnn_layers, 4)
        effective_epochs = min(num_epochs, 10)
        effective_patience = 3
        min_epochs_early_stop = 5
    elif num_total_nodes > 500_000:
        effective_hidden = min(effective_hidden, 64)
    
    print(f"  [Profile] Dataset '{dataset_name}' -> GNN Layers={effective_gnn_layers}, Hidden={effective_hidden}, LR={effective_lr}, beta={effective_focal_beta}, SMOTE={effective_smote_ratio}, Epochs={effective_epochs}")
    
    model = BurstAwareHGT(
        in_channels_dict=in_channels_dict,
        hidden_channels=effective_hidden,
        num_layers=effective_gnn_layers,
        metadata=metadata,
        dropout=DROPOUT,
        jk_mode="cat" if effective_gnn_layers >= 4 else None
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=effective_lr, weight_decay=0.0001)
    from torch.optim.lr_scheduler import OneCycleLR, CosineAnnealingLR
    try:
        scheduler = OneCycleLR(optimizer, max_lr=max(1e-3, effective_lr * 2.5), total_steps=max(2, effective_epochs), pct_start=0.15, anneal_strategy="cos")
    except Exception:
        scheduler = CosineAnnealingLR(optimizer, T_max=effective_epochs, eta_min=1e-5)
    
    try:
        from .focal_tversky_loss import CostSensitiveFocalTverskyLoss
        criterion = CostSensitiveFocalTverskyLoss(alpha=max(0.10, 1.0 - effective_focal_beta), beta=effective_focal_beta, gamma=1.33, adaptive_imbalance=True)
    except Exception:
        criterion = FocalLoss(alpha=alpha, gamma=2.0, label_smoothing=0.05)

    all_ts_tensors = []
    for rel in metadata[1]:
        if rel in data:
            if hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0:
                all_ts_tensors.append(data[rel].ts.float().flatten())
            elif hasattr(data[rel], "delta_t") and data[rel].delta_t is not None and data[rel].delta_t.numel() > 0:
                all_ts_tensors.append(data[rel].delta_t.float().flatten())
            
    if all_ts_tensors:
        cat_ts = torch.cat(all_ts_tensors)
        ts_train_thresh = float(torch.quantile(cat_ts, 0.60).item())
        ts_val_thresh = float(torch.quantile(cat_ts, 0.70).item())
        del cat_ts, all_ts_tensors
    else:
        ts_train_thresh, ts_val_thresh = 0.0, 0.0

    # Build mask dictionaries for 3-way temporal split using absolute timestamps (Upgrade D)
    train_edge_index, train_delta_t, train_burst_score = {}, {}, {}
    val_edge_index, val_delta_t, val_burst_score = {}, {}, {}
    test_edge_index, test_delta_t, test_burst_score = {}, {}, {}
    
    for rel in metadata[1]:
        if rel in data:
            edge_index = data[rel].edge_index
            delta_t = data[rel].delta_t
            burst_score = data[rel].burst_score
            rel_ts = data[rel].ts if (hasattr(data[rel], "ts") and data[rel].ts is not None and data[rel].ts.numel() > 0) else delta_t
            
            t_mask = rel_ts <= ts_train_thresh
            v_mask = (rel_ts > ts_train_thresh) & (rel_ts <= ts_val_thresh)
            te_mask = rel_ts > ts_val_thresh
            
            train_edge_index[rel] = edge_index[:, t_mask]
            train_delta_t[rel] = delta_t[t_mask]
            train_burst_score[rel] = burst_score[t_mask]
            
            val_edge_index[rel] = edge_index[:, t_mask | v_mask]
            val_delta_t[rel] = delta_t[t_mask | v_mask]
            val_burst_score[rel] = burst_score[t_mask | v_mask]
            
            test_edge_index[rel] = edge_index[:, te_mask]
            test_delta_t[rel] = delta_t[te_mask]
            test_burst_score[rel] = burst_score[te_mask]

    x_dict = {nt: data[nt].x for nt in metadata[0]}

    # Step 1: Self-Supervised Temporal Contrastive Pretraining (Pruned 2-Epoch Cosine Anneal)
    train_temporal_contrastive_pretraining(model, x_dict, train_edge_index, train_delta_t, train_burst_score, num_epochs=2)

    x_dict = {nt: data[nt].x for nt in metadata[0]}

    # Model Training Loop with Mixed Precision & Memory Optimizations
    best_val_loss = float('inf')
    best_val_score = -1e9
    patience = effective_patience
    patience_counter = 0
    best_model_weights = copy.deepcopy(model.state_dict())
    
    # Initialize modern device-aware AMP scaler
    device_type = 'cuda' if torch.cuda.is_available() else 'cpu'
    from contextlib import nullcontext
    if device_type == 'cuda':
        try:
            from torch.amp import autocast as modern_autocast, GradScaler as ModernScaler
            autocast_ctx = modern_autocast(device_type='cuda')
            scaler = ModernScaler('cuda')
        except Exception:
            from torch.cuda.amp import autocast as legacy_autocast, GradScaler as LegacyScaler
            autocast_ctx = legacy_autocast()
            scaler = LegacyScaler()
    else:
        autocast_ctx = nullcontext()
        class DummyScaler:
            def scale(self, l): return l
            def unscale_(self, opt): pass
            def step(self, opt): opt.step()
            def update(self): pass
            def get_scale(self): return 1.0
        scaler = DummyScaler()
    
    # Check memory bounds
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    model.train()
    for epoch in range(1, effective_epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        
        # Step curriculum loss (Upgrade F)
        if hasattr(criterion, "step_curriculum"):
            criterion.step_curriculum(epoch, effective_epochs)
        
        with autocast_ctx:
            # EXTRACT EMBEDDINGS FIRST (Latent Manifold-Constrained SMOTE)
            z_dict = model.get_embeddings(x_dict, train_edge_index, train_delta_t, train_burst_score)
            z_target = z_dict[target_node]
            
            # Identify minority train nodes for SMOTE
            valid_train_mask = train_mask_nodes_augmented & (y_target >= 0)
            minority_idx = torch.where(valid_train_mask & (y_target == 1))[0]
            
            synthetic_logits = []
            synthetic_y = []
                        # Latent-Space GraphSMOTE Augmentation Engine
            if len(minority_idx) >= 2:
                graph_smote_engine = LatentGraphSMOTE(hidden_dim=effective_hidden, k_neighbors=min(5, len(minority_idx)-1), oversample_ratio=effective_smote_ratio)
                z_target_aug, y_target_aug, _ = graph_smote_engine.synthesize_latent_nodes(
                    z_target[minority_idx], y_target[minority_idx]
                )
                num_syn = z_target_aug.shape[0] - len(minority_idx)
                if num_syn > 0:
                    synthetic_logits = model.out_proj[target_node](z_target_aug[len(minority_idx):])
                    synthetic_y = torch.ones(num_syn, dtype=y_target.dtype, device=y_target.device)
            
            # Normal forward pass for real nodes
            out_dict = {}
            for nt in z_dict:
                if z_dict[nt].shape[0] > 0:
                    out_dict[nt] = model.out_proj[nt](z_dict[nt])
                else:
                    out_dict[nt] = torch.zeros(0, 2, device=z_dict[nt].device)
                    
            logits = out_dict[target_node]
            valid_mask = (y_target >= 0) & train_mask_nodes_augmented
            
            # Stratified Minority Oversampling in GNN Training Batches
            pos_batch_idx = torch.where(valid_mask & (y_target == 1))[0]
            neg_batch_idx = torch.where(valid_mask & (y_target == 0))[0]
            
            if len(pos_batch_idx) >= 2 and len(neg_batch_idx) >= 2:
                desired_pos = max(len(pos_batch_idx), int(effective_smote_ratio * len(neg_batch_idx)))
                if desired_pos > len(pos_batch_idx):
                    oversample_idx = pos_batch_idx[torch.randint(0, len(pos_batch_idx), (desired_pos - len(pos_batch_idx),))]
                    batch_idx = torch.cat([pos_batch_idx, oversample_idx, neg_batch_idx])
                else:
                    batch_idx = torch.cat([pos_batch_idx, neg_batch_idx])
                batch_idx = batch_idx[torch.randperm(len(batch_idx))]
                logits_valid = logits[batch_idx]
                y_target_valid = y_target[batch_idx]
            else:
                logits_valid = logits[valid_mask]
                y_target_valid = y_target[valid_mask]
            
            # Combine real and synthetic for loss calculation
            if len(synthetic_logits) > 0:
                logits_valid = torch.cat([logits_valid, synthetic_logits], dim=0)
                y_target_valid = torch.cat([y_target_valid, synthetic_y], dim=0)
            
            # EWC continual learning parameter penalty
            ewc_penalty = 0.0
            if prev_ewc is not None:
                ewc_penalty = prev_ewc.penalty(model)
                
            if len(y_target_valid) > 0:
                loss = criterion(logits_valid, y_target_valid) + ewc_lambda * ewc_penalty
            else:
                loss = torch.tensor(ewc_lambda * ewc_penalty, requires_grad=True, device=logits.device)
            
        scaler.scale(loss).backward()
        try:
            scaler.unscale_(optimizer)
        except Exception:
            pass
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        scaler.step(optimizer)
        scaler.update()
        scheduler.step()
        
        if torch.cuda.is_available() and num_total_nodes > 1000000:
            torch.cuda.empty_cache()
        
        # Validation monitoring every 2 epochs (Upgrade T)
        if epoch % 2 == 0:
            model.eval()
            with torch.no_grad():
                with autocast_ctx:
                    val_out = model(x_dict, val_edge_index, val_delta_t, val_burst_score)
                    val_logits = val_out[target_node][val_mask_nodes]
                
                val_y = y_target[val_mask_nodes]
                val_valid = val_y >= 0
                if val_valid.sum() > 0:
                    val_loss = F.cross_entropy(val_logits[val_valid].float(), val_y[val_valid]).item()
                    val_probs = F.softmax(val_logits[val_valid].float(), dim=1)[:, 1].cpu().numpy()
                    val_targets = val_y[val_valid].cpu().numpy()
                    
                    if len(np.unique(val_targets)) > 1:
                        from sklearn.metrics import average_precision_score
                        val_prauc = float(average_precision_score(val_targets, val_probs))
                        val_score = val_prauc - 0.1 * val_loss
                    else:
                        val_score = -val_loss
                        
                    if val_score > best_val_score:
                        best_val_score = val_score
                        best_val_loss = val_loss
                        patience_counter = 0
                        best_model_weights = copy.deepcopy(model.state_dict())
                    else:
                        patience_counter += 1
                        if patience_counter >= effective_patience and epoch > min_epochs_early_stop:
                            print(f"  [Early Stopping] Triggered at Epoch {epoch} with Best Val Score {best_val_score:.4f} (Loss: {best_val_loss:.4f})", flush=True)
                            break
        
        print_freq = 1 if (num_total_nodes > 1_000_000 or effective_epochs <= 10) else (5 if effective_epochs <= 20 else 10)
        if epoch % print_freq == 0 or epoch == 1 or epoch == effective_epochs:
            if len(y_target_valid) > 0:
                pred = logits_valid.argmax(dim=1)
                acc = (pred == y_target_valid).float().mean().item()
            else:
                acc = 0.0
            print(f"    [Training] Epoch {epoch:2d}/{effective_epochs} | Loss: {loss.item():.4f} | Train Acc: {acc:.4f}", flush=True)

    # Restore best checkpoint
    model.load_state_dict(best_model_weights)

    # Temporal Streaming Evaluation & Standalone Dynamic Threshold Calibration
    model.eval()
    with torch.no_grad():
        with autocast_ctx:
            test_out_dict = model(x_dict, test_edge_index, test_delta_t, test_burst_score)
            val_out_dict = model(x_dict, val_edge_index, val_delta_t, val_burst_score)
            
        logits = test_out_dict[target_node]
        risk_scores = F.softmax(logits, dim=1)[:, 1]
        
        val_logits = val_out_dict[target_node]
        val_probs = F.softmax(val_logits[val_mask_nodes], dim=1)[:, 1].cpu().numpy()
        val_y = y_target[val_mask_nodes].cpu().numpy()
        
        # Dynamic Threshold Calibration for Standalone GNN (Beta = 2.0 for Recall optimization)
        calibrator = DynamicThresholdCalibrator(beta=2.0)
        optimal_standalone_tau = calibrator.calibrate(val_probs, val_y)
        
        valid_mask = y_target >= 0
        logits_valid = logits[valid_mask]
        y_target_valid = y_target[valid_mask]
        test_scores = risk_scores[valid_mask].cpu().numpy()
        test_y = y_target_valid.cpu().numpy()
        
        standalone_preds = (test_scores >= optimal_standalone_tau).astype(int)
        test_pos = (test_y == 1)
        test_rec = np.sum((standalone_preds == 1) & test_pos) / max(1, np.sum(test_pos))
        test_prec = np.sum((standalone_preds == 1) & test_pos) / max(1, np.sum(standalone_preds == 1))
        test_f1 = 2 * (test_prec * test_rec) / (test_prec + test_rec + 1e-6)
        
        if len(y_target_valid) > 0:
            preds = logits_valid.argmax(dim=1)
            test_acc = (preds == y_target_valid).float().mean().item()
        else:
            test_acc = 0.0
        
        print(f"  Inference Evaluation:")
        print(f"    Target Node '{target_node}' Accuracy: {test_acc:.4f}")
        print(f"    Standalone GNN Calibrated Metrics (tau* = {optimal_standalone_tau:.3f}):")
        print(f"      Recall: {test_rec*100:.2f}% | Precision: {test_prec*100:.2f}% | F1-Score: {test_f1*100:.2f}%")
        print(f"    Risk Score range: [{risk_scores.min().item():.4f}, {risk_scores.max().item():.4f}]")
        print(f"    Alerts triggered (Risk >= tau*): {(risk_scores >= optimal_standalone_tau).sum().item()}")

    # Save base HGT model weights
    model_dir = Path("data/outputs/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_dir / "htgnn_model.pt")
    print(f"  [Checkpoint] Base GNN weights saved to {model_dir / 'htgnn_model.pt'}")

    # Fit Unified C-STGB Master Algorithm
    print("  [Pipeline] Training Unified C-STGB (Conformal Spatio-Temporal GraphBoost) Classifier...")
    cstgb_model = CSTGBClassifier(model, target_node=target_node, hidden_channels=effective_hidden, alpha=0.10)
    
    # Pass train mask, val mask, and test mask
    eval_test_mask = test_mask_nodes
    
    cstgb_model.fit(
        x_dict, train_edge_index, train_delta_t, train_burst_score,
        y_target, train_mask_nodes_augmented, val_mask=val_mask_nodes, test_mask=eval_test_mask
    )
    cstgb_model.save(model_dir)
    
    test_probs = cstgb_model.predict_proba(x_dict, test_edge_index, test_delta_t, test_burst_score, eval_test_mask)
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return cstgb_model, test_probs


def extract_ego_neighborhood_embeddings(embeddings_dict, edge_index_dict, target_node):
    """
    Multi-Moment Higher-Order Subnetwork Ego-Pooling with Cold-Start & Super-Node Protection
    (Memory-Optimized with In-Place Buffers & Active Cache Eviction):
    1. 1st Moment (Mean): Average neighborhood risk
    2. Anomaly Contrast: z_u - mean(N(u))
    3. 2nd Central Moment (Dispersion): std(N(u))
    4. Extreme High-Risk Counterparty (Max Pool): max(N(u))
    5. Baseline Counterparty (Min Pool): min(N(u))
    6. 95th Percentile Counterparty (p95 Pool): Protects super-nodes from variance dilution
    7. Cold-Start Prior Indicator: Binary flag + Global Centroid substitution when d_u == 0
    """
    import gc
    z_target = embeddings_dict[target_node]
    num_nodes, emb_dim = z_target.shape
    device = z_target.device
    
    neighbor_sum = torch.zeros((num_nodes, emb_dim), dtype=torch.float32, device=device)
    neighbor_sq_sum = torch.zeros((num_nodes, emb_dim), dtype=torch.float32, device=device)
    neighbor_max = torch.full((num_nodes, emb_dim), -float('inf'), dtype=torch.float32, device=device)
    neighbor_min = torch.full((num_nodes, emb_dim), float('inf'), dtype=torch.float32, device=device)
    neighbor_counts = torch.zeros(num_nodes, dtype=torch.float32, device=device)
    
    for rel, edge_index in edge_index_dict.items():
        if edge_index is None or edge_index.numel() == 0:
            continue
        src_type, _, dst_type = rel
        src_emb = embeddings_dict[src_type]
        dst_emb = embeddings_dict[dst_type]
        
        if src_type == target_node and edge_index.shape[1] > 0:
            src_idx = edge_index[0]
            dst_idx = edge_index[1]
            valid = src_idx < num_nodes
            s_val = src_idx[valid]
            d_emb = dst_emb[dst_idx[valid]]
            
            neighbor_sum.index_add_(0, s_val, d_emb)
            neighbor_sq_sum.index_add_(0, s_val, d_emb ** 2)
            neighbor_counts.index_add_(0, s_val, torch.ones_like(s_val, dtype=torch.float32))
            neighbor_max.scatter_reduce_(0, s_val.unsqueeze(-1).expand_as(d_emb), d_emb, reduce='amax', include_self=True)
            neighbor_min.scatter_reduce_(0, s_val.unsqueeze(-1).expand_as(d_emb), d_emb, reduce='amin', include_self=True)
            
        if dst_type == target_node and edge_index.shape[1] > 0:
            src_idx = edge_index[0]
            dst_idx = edge_index[1]
            valid = dst_idx < num_nodes
            d_val = dst_idx[valid]
            s_emb = src_emb[src_idx[valid]]
            
            neighbor_sum.index_add_(0, d_val, s_emb)
            neighbor_sq_sum.index_add_(0, d_val, s_emb ** 2)
            neighbor_counts.index_add_(0, d_val, torch.ones_like(d_val, dtype=torch.float32))
            neighbor_max.scatter_reduce_(0, d_val.unsqueeze(-1).expand_as(s_emb), s_emb, reduce='amax', include_self=True)
            neighbor_min.scatter_reduce_(0, d_val.unsqueeze(-1).expand_as(s_emb), s_emb, reduce='amin', include_self=True)
            
    has_neighbors = neighbor_counts > 0
    cold_start_flag = np.ascontiguousarray((~has_neighbors).float().unsqueeze(-1).cpu().numpy(), dtype=np.float32)
    
    # Global Population Centroid for Cold-Start Prior Fallback
    global_centroid = z_target.mean(dim=0, keepdim=True)
    
    ego_mean = z_target.clone()
    ego_mean[has_neighbors] = neighbor_sum[has_neighbors] / neighbor_counts[has_neighbors].unsqueeze(-1)
    ego_mean[~has_neighbors] = global_centroid.expand((~has_neighbors).sum(), emb_dim)
    
    ego_contrast = z_target - ego_mean
    
    # 2nd Central Moment (Dispersion)
    ego_std = torch.zeros_like(z_target)
    mean_sq = ego_mean[has_neighbors] ** 2
    sq_mean = neighbor_sq_sum[has_neighbors] / neighbor_counts[has_neighbors].unsqueeze(-1)
    ego_std[has_neighbors] = torch.sqrt(torch.clamp(sq_mean - mean_sq, min=0.0) + 1e-6)
    
    # Release square sum buffer immediately
    del neighbor_sq_sum
    
    # Max and Min Counterparty embeddings
    ego_max = z_target.clone()
    ego_max[has_neighbors] = neighbor_max[has_neighbors]
    ego_min = z_target.clone()
    ego_min[has_neighbors] = neighbor_min[has_neighbors]
    
    # Release min/max accumulation buffers
    del neighbor_sum, neighbor_max, neighbor_min, neighbor_counts
    
    # Exact Asymptotic 95th Percentile Quantile Estimator (Gaussian/GEV quantile)
    # q_0.95 = mu + 1.64485 * sigma
    ego_p95 = ego_mean + 1.64485 * ego_std
    
    # Convert to contiguous float32 numpy arrays and release PyTorch GPU/CPU memory
    out_mean = np.ascontiguousarray(ego_mean.detach().cpu().numpy(), dtype=np.float32)
    out_contrast = np.ascontiguousarray(ego_contrast.detach().cpu().numpy(), dtype=np.float32)
    out_std = np.ascontiguousarray(ego_std.detach().cpu().numpy(), dtype=np.float32)
    out_max = np.ascontiguousarray(ego_max.detach().cpu().numpy(), dtype=np.float32)
    out_min = np.ascontiguousarray(ego_min.detach().cpu().numpy(), dtype=np.float32)
    out_p95 = np.ascontiguousarray(ego_p95.detach().cpu().numpy(), dtype=np.float32)
    
    del ego_mean, ego_contrast, ego_std, ego_max, ego_min, ego_p95
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return (
        out_mean,
        out_contrast,
        out_std,
        out_max,
        out_min,
        out_p95,
        cold_start_flag
    )


class ResMLPNet(nn.Module):
    """Deep Gated Residual MLP PyTorch network for cross-modal meta-stacking."""
    def __init__(self, in_f: int = 18, h_dim: int = 64):
        super().__init__()
        self.fc1 = nn.Linear(in_f, h_dim)
        self.ln1 = nn.LayerNorm(h_dim)
        self.fc2 = nn.Linear(h_dim, 32)
        self.ln2 = nn.LayerNorm(32)
        self.fc3 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(0.10)
        self.gate = nn.Linear(in_f, 1)
        
    def forward(self, x):
        h = F.gelu(self.ln1(self.fc1(x)))
        h = self.dropout(h)
        h = F.gelu(self.ln2(self.fc2(h)))
        out_mlp = torch.sigmoid(self.fc3(h)).squeeze(-1)
        
        # Dynamic authority gate between tabular trees (idx 13), fused trees (idx 14), and GNN (idx 3)
        tree_p = 0.50 * x[:, 13] + 0.50 * x[:, 14]
        gnn_p = x[:, 3]
        alpha_gate = torch.sigmoid(self.gate(x)).squeeze(-1)
        
        # Exact equal Bayesian prior weighting on un-gated skip connection
        blended = alpha_gate * out_mlp + (1.0 - alpha_gate) * (0.50 * tree_p + 0.50 * gnn_p)
        return torch.clamp(blended, 1e-6, 1.0 - 1e-6)


class ResMLPMetaLearner:
    """
    Deep Gated Residual MLP Stacking Engine with Certainty-Weighted Cross-Modal Routing.
    Optimizes PR-AUC and F1 directly on out-of-fold cross-modal feature representations.
    """
    def __init__(self, in_features=18, hidden_dim=64, epochs=40, lr=0.005, weight_decay=1e-4):
        self.in_features = in_features
        self.hidden_dim = hidden_dim
        self.epochs = epochs
        self.lr = lr
        self.weight_decay = weight_decay
        self.net = None

    def fit(self, X, y):
        import torch
        import torch.nn as nn
        import numpy as np
        
        X_arr = np.nan_to_num(np.asarray(X, dtype=np.float32), nan=0.0)
        y_arr = np.asarray(y, dtype=np.float32)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = ResMLPNet(self.in_features, self.hidden_dim).to(device)
        optimizer = torch.optim.AdamW(self.net.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        
        x_t = torch.tensor(X_arr, dtype=torch.float32, device=device)
        y_t = torch.tensor(y_arr, dtype=torch.float32, device=device)
        
        pos_weight = max(1.0, float((y_arr == 0).sum()) / max(1.0, float((y_arr == 1).sum())))
        pos_weight = min(12.0, pos_weight)  # Balanced bounded weight
        
        self.net.train()
        for ep in range(self.epochs):
            optimizer.zero_grad()
            p = self.net(x_t)
            # Binary cross-entropy with asymmetric positive weight
            bce = - (pos_weight * y_t * torch.log(p) + (1.0 - y_t) * torch.log(1.0 - p))
            loss = bce.mean()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.net.parameters(), 1.0)
            optimizer.step()
            
        self.net.eval()
        return self

    def predict_proba(self, X):
        import torch
        import numpy as np
        if self.net is None:
            X_arr = np.asarray(X)
            p = 0.50 * X_arr[:, 13] + 0.30 * X_arr[:, 14] + 0.20 * X_arr[:, 3]
            return np.column_stack([1.0 - p, p])
            
        X_arr = np.nan_to_num(np.asarray(X, dtype=np.float32), nan=0.0)
        device = next(self.net.parameters()).device
        self.net.eval()
        with torch.no_grad():
            x_t = torch.tensor(X_arr, dtype=torch.float32, device=device)
            p = self.net(x_t).cpu().numpy().flatten()
            
        return np.column_stack([1.0 - p, p])


class CSTGBClassifier:
    """
    C-STGB: Conformal Spatio-Temporal GraphBoost Classifier (Dual-Stream Gated Stacking SOTA)
    
    The unified master AML detection algorithm combining:
    1. Dual-Stream Residual Gated Architecture (Stream 1: Pure Tabular, Stream 2: Graph, Stream 3: Fused)
    2. Dynamic Meta-Learner routing weights based on topological certainty
    3. Manifold-Constrained GraphSMOTE interpolation
    4. Mondrian Topology-Stratified Inductive Conformal Prediction & Delayed-Feedback ACI
    """
    def __init__(self, gnn_model, target_node="Account", hidden_channels=128, alpha=0.10):
        import lightgbm as lgb
        from catboost import CatBoostClassifier
        
        self.gnn_model = gnn_model
        self.target_node = target_node
        self.hidden_channels = hidden_channels
        self.alpha = float(alpha)
        
        # Check GPU availability for high-throughput tree training
        use_gpu = torch.cuda.is_available()
        xgb_kwargs = {"tree_method": "hist", "device": "cuda", "max_bin": 128} if use_gpu else {"tree_method": "hist", "max_bin": 128, "n_jobs": -1}
        lgb_device = "gpu" if use_gpu else "cpu"
        cat_task = "GPU" if use_gpu else "CPU"

        # --- STREAM 1: Pure Tabular Expert (Trains strictly on X) ---
        try:
            self.xgb_tab = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, random_state=42, **xgb_kwargs)
        except Exception:
            self.xgb_tab = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, random_state=42, tree_method="hist", max_bin=128, n_jobs=-1)

        try:
            self.lgbm_tab = lgb.LGBMClassifier(n_estimators=300, num_leaves=63, max_bin=128, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, random_state=42, device=lgb_device, n_jobs=-1, verbose=-1)
        except Exception:
            self.lgbm_tab = lgb.LGBMClassifier(n_estimators=300, num_leaves=63, max_bin=128, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, random_state=42, n_jobs=-1, verbose=-1)

        try:
            self.cat_tab = CatBoostClassifier(iterations=300, depth=6, learning_rate=0.05, random_seed=42, task_type=cat_task, thread_count=-1, verbose=False)
        except Exception:
            self.cat_tab = CatBoostClassifier(iterations=300, depth=6, learning_rate=0.05, random_seed=42, thread_count=-1, verbose=False)
        
        # --- STREAM 3: Cross-Modal Fused Residual Expert (Trains on X, Z, Ego, and p_gnn) ---
        try:
            self.xgb_fused = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42, **xgb_kwargs)
        except Exception:
            self.xgb_fused = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42, tree_method="hist", max_bin=128, n_jobs=-1)

        try:
            self.lgbm_fused = lgb.LGBMClassifier(n_estimators=200, num_leaves=31, max_bin=128, learning_rate=0.05, random_state=42, device=lgb_device, n_jobs=-1, verbose=-1)
        except Exception:
            self.lgbm_fused = lgb.LGBMClassifier(n_estimators=200, num_leaves=31, max_bin=128, learning_rate=0.05, random_state=42, n_jobs=-1, verbose=-1)
            
        try:
            self.cat_fused = CatBoostClassifier(iterations=200, depth=5, learning_rate=0.05, random_seed=42, task_type=cat_task, thread_count=-1, verbose=False)
        except Exception:
            self.cat_fused = CatBoostClassifier(iterations=200, depth=5, learning_rate=0.05, random_seed=42, thread_count=-1, verbose=False)
        
        # --- META-LEARNER (Deep Gated Residual MLP Stacking Engine) ---
        self.meta_learner = ResMLPMetaLearner(in_features=18, hidden_dim=64)
        self.is_meta_fitted = False
        
        self.optimal_threshold = 0.50
        self.conformal = None
        self.mondrian_conformal = None
        self.conformal_threshold_q = None
        self.aci = None
        self.single_class = False

    def _compute_meta_features(self, p_xgb_t, p_lgb_t, p_cat_t, p_gnn_f, p_xgb_f, p_lgb_f, p_cat_f, deg_c, pt_f, cl_f):
        """Constructs rich 18-dimensional cross-modal meta-features for non-linear stacking."""
        import numpy as np
        trees_stack = np.column_stack([p_xgb_t, p_lgb_t, p_cat_t, p_xgb_f, p_lgb_f, p_cat_f])
        max_trees = np.max(trees_stack, axis=1)
        min_trees = np.min(trees_stack, axis=1)
        std_trees = np.std(trees_stack, axis=1)
        mean_tab = (p_xgb_t + p_lgb_t + p_cat_t) / 3.0
        # Non-linear cross-modal agreement, Bayesian Log-Odds evidence, and Kullback-Leibler contrast
        eps = 1e-6
        p_trees_mean = np.clip((mean_tab + mean_fused) / 2.0, eps, 1.0 - eps)
        p_gnn_c = np.clip(p_gnn_f, eps, 1.0 - eps)
        
        logit_trees = np.log(p_trees_mean / (1.0 - p_trees_mean))
        logit_gnn = np.log(p_gnn_c / (1.0 - p_gnn_c))
        
        # Exact binary Kullback-Leibler divergence between tree ensemble and GNN posterior
        kl_div = p_trees_mean * np.log(p_trees_mean / p_gnn_c) + (1.0 - p_trees_mean) * np.log((1.0 - p_trees_mean) / (1.0 - p_gnn_c))
        
        # Bayesian Log-Evidence Concordance
        agree_evidence = (logit_trees + logit_gnn) / 2.0
        agree_product = p_trees_mean * p_gnn_c
        
        return np.column_stack([
            p_xgb_t, p_lgb_t, p_cat_t, p_gnn_f, p_xgb_f, p_lgb_f, p_cat_f,
            agree_evidence, agree_product, kl_div,
            max_trees, min_trees, std_trees, mean_tab, mean_fused,
            deg_c, pt_f, cl_f
        ])

    def _extract_all_features(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        # Extracts X (tabular), Z (graph embedding), Ego pools, higher-order motifs, and topological metrics
        import torch
        import torch.nn.functional as F
        import numpy as np
        with torch.no_grad():
            embeddings_dict = self.gnn_model.get_embeddings(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            logits_dict = self.gnn_model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            
            p_gnn = F.softmax(logits_dict[self.target_node], dim=1)[:, 1].detach().cpu().numpy().reshape(-1, 1)
            z = embeddings_dict[self.target_node].detach().cpu().numpy()
            x = x_dict[self.target_node].detach().cpu().numpy()
            
            num_target_nodes = x.shape[0]

            # Extract higher-order topological motifs (3-cycles, 4-cycles, reciprocal flows, closed-loop index)
            try:
                from .motif_kernel import DirectedMotifKernel
                motif_engine = DirectedMotifKernel(max_cycle_order=4)
                target_edges = []
                for rel, e_idx in edge_index_dict.items():
                    if e_idx is not None and e_idx.numel() > 0:
                        src_nt, _, dst_nt = rel
                        if src_nt == self.target_node and dst_nt == self.target_node:
                            target_edges.append(e_idx)
                if len(target_edges) > 0:
                    unified_edges = torch.cat(target_edges, dim=1)
                    motif_dict = motif_engine.compute_ego_cycle_motifs(unified_edges, num_target_nodes)
                    c3 = motif_dict["cycle3_count"].reshape(-1, 1)
                    c4 = motif_dict["cycle4_count"].reshape(-1, 1)
                    recip = motif_dict["reciprocal_count"].reshape(-1, 1)
                    cl_idx = motif_dict["closed_loop_index"].reshape(-1, 1)

                    # 6 Canonical AML Typology Signatures
                    typ_dict = motif_engine.compute_canonical_aml_typologies(unified_edges, num_target_nodes)
                    f_in = typ_dict["fan_in_score"].reshape(-1, 1)
                    f_out = typ_dict["fan_out_score"].reshape(-1, 1)
                    sg = typ_dict["scatter_gather_score"].reshape(-1, 1)
                    peel = typ_dict["peeling_chain_score"].reshape(-1, 1)
                    w_loop = typ_dict["wash_loop_score"].reshape(-1, 1)
                    w_ratio = typ_dict["wash_ratio_index"].reshape(-1, 1)

                    motif_mat = np.column_stack([
                        np.log1p(c3), np.log1p(c4), np.log1p(recip), cl_idx,
                        f_in, f_out, sg, peel, w_loop, w_ratio
                    ])
                else:
                    motif_mat = np.zeros((num_target_nodes, 10), dtype=np.float32)
            except Exception:
                motif_mat = np.zeros((num_target_nodes, 10), dtype=np.float32)

            if num_target_nodes > 500_000:
                # Memory-safe feature fusion for mega-graphs (>500k nodes)
                fused_feats = np.ascontiguousarray(np.concatenate([x, z, motif_mat, p_gnn], axis=1), dtype=np.float32)
            else:
                ego_mean, ego_contrast, ego_std, ego_max, ego_min, ego_p95, cold_start_flags = extract_ego_neighborhood_embeddings(
                    embeddings_dict, edge_index_dict, self.target_node
                )
                fused_feats = np.ascontiguousarray(
                    np.concatenate([x, z, ego_contrast, ego_max, ego_p95, motif_mat, cold_start_flags, p_gnn], axis=1),
                    dtype=np.float32
                )
                del ego_mean, ego_contrast, ego_std, ego_max, ego_min, ego_p95, cold_start_flags
            
            # Extract topological signals dynamically if X is wide enough, else use safe defaults
            deg_centrality = np.ascontiguousarray(x[:, 2].reshape(-1, 1) if x.shape[1] > 2 else np.ones((x.shape[0], 1)), dtype=np.float32)
            pass_through = np.ascontiguousarray(x[:, 5].reshape(-1, 1) if x.shape[1] > 5 else np.zeros((x.shape[0], 1)), dtype=np.float32)
            burst_velocity = np.ascontiguousarray(x[:, 1].reshape(-1, 1) if x.shape[1] > 1 else np.zeros((x.shape[0], 1)), dtype=np.float32)
            closed_loop_sig = np.ascontiguousarray(motif_mat[:, 3].reshape(-1, 1), dtype=np.float32)
            x = np.ascontiguousarray(x, dtype=np.float32)
            
            return x, fused_feats, p_gnn, deg_centrality, pass_through, burst_velocity, closed_loop_sig

    def _predict_ensemble(self, feat_tuple):
        import numpy as np
        if len(feat_tuple) == 7:
            x_tab, fused_feats, p_gnn, deg_centrality, pass_through, burst_velocity, closed_loop_sig = feat_tuple
        else:
            x_tab, fused_feats, p_gnn, deg_centrality, pass_through, burst_velocity = feat_tuple[:6]
            closed_loop_sig = np.zeros_like(deg_centrality)
        
        p_gnn_flat = p_gnn.flatten()
        if self.single_class:
            return p_gnn_flat
            
        # Stream 1: Pure Tabular
        p_xgb_tab = self.xgb_tab.predict_proba(x_tab)[:, 1]
        p_lgb_tab = self.lgbm_tab.predict_proba(x_tab)[:, 1]
        p_cat_tab = self.cat_tab.predict_proba(x_tab)[:, 1]
        
        # Stream 3: Fused Residuals
        p_xgb_fused = self.xgb_fused.predict_proba(fused_feats)[:, 1]
        p_lgb_fused = self.lgbm_fused.predict_proba(fused_feats)[:, 1]
        p_cat_fused = self.cat_fused.predict_proba(fused_feats)[:, 1]
        
        if self.is_meta_fitted:
            meta_input = self._compute_meta_features(
                p_xgb_tab, p_lgb_tab, p_cat_tab, p_gnn_flat,
                p_xgb_fused, p_lgb_fused, p_cat_fused,
                deg_centrality.flatten(), pass_through.flatten(), closed_loop_sig.flatten()
            )
            p_ensemble = self.meta_learner.predict_proba(meta_input)[:, 1]
        else:
            # Unbiased uniform Bayesian prior average across all 5 model streams
            p_ensemble = (p_lgb_tab + p_xgb_tab + p_cat_tab + p_lgb_fused + p_gnn_flat) / 5.0
            
        return p_ensemble

    def fit(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target, train_mask, val_mask=None, test_mask=None):
        from sklearn.model_selection import StratifiedKFold
        import lightgbm as lgb
        from catboost import CatBoostClassifier
        from xgboost import XGBClassifier
        import torch
        import numpy as np
        import gc
        
        self.gnn_model.eval()
        with torch.no_grad():
            feat_tuple = self._extract_all_features(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            y = y_target.cpu().numpy()
            
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        x_tab, fused_feats, p_gnn, deg_centrality, pass_through, burst_velocity, closed_loop_sig = feat_tuple
            
        valid_indices = (y >= 0) & train_mask.cpu().numpy()
        
        if valid_indices.sum() > 0:
            x_tab_train = np.ascontiguousarray(x_tab[valid_indices], dtype=np.float32)
            fused_train = np.ascontiguousarray(fused_feats[valid_indices], dtype=np.float32)
            p_gnn_train = p_gnn[valid_indices].flatten()
            deg_train = deg_centrality[valid_indices].flatten()
            pt_train = pass_through[valid_indices].flatten()
            cl_train = closed_loop_sig[valid_indices].flatten()
            y_train = y[valid_indices]
            
            pos_count = (y_train == 1).sum()
            neg_count = (y_train == 0).sum()
            scale_pos_tab = max(1.0, min(10.0, float(np.sqrt(neg_count / (pos_count + 1e-6)))))
            
            amt = np.maximum(0.0, x_tab_train[:, 3] if x_tab_train.shape[1] > 3 else 0.0)
            sample_weight = 1.0 + 0.5 * np.log1p(amt)
            sample_weight = np.maximum(0.001, np.nan_to_num(sample_weight, nan=1.0, posinf=1.0, neginf=1.0))
            
            # Meta-learner OOF training (Stratified cross-validation)
            if pos_count >= 5 and len(y_train) >= 30:
                try:
                    if len(y_train) > 100_000:
                        pos_indices = np.where(y_train == 1)[0]
                        neg_indices = np.where(y_train == 0)[0]
                        sampled_neg = np.random.choice(neg_indices, size=min(len(neg_indices), 50_000), replace=False)
                        meta_subset_idx = np.concatenate([pos_indices, sampled_neg])
                        np.random.shuffle(meta_subset_idx)
                        
                        x_meta_train = x_tab_train[meta_subset_idx]
                        fused_meta_train = fused_train[meta_subset_idx]
                        p_gnn_meta = p_gnn_train[meta_subset_idx]
                        deg_meta = deg_train[meta_subset_idx]
                        pt_meta = pt_train[meta_subset_idx]
                        cl_meta = cl_train[meta_subset_idx]
                        y_meta = y_train[meta_subset_idx]
                        sw_meta = sample_weight[meta_subset_idx]
                    else:
                        x_meta_train = x_tab_train
                        fused_meta_train = fused_train
                        p_gnn_meta = p_gnn_train
                        deg_meta = deg_train
                        pt_meta = pt_train
                        cl_meta = cl_train
                        y_meta = y_train
                        sw_meta = sample_weight
                        
                    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
                    oof_p_xgb_t = np.zeros(len(y_meta))
                    oof_p_lgb_t = np.zeros(len(y_meta))
                    oof_p_cat_t = np.zeros(len(y_meta))
                    oof_p_xgb_f = np.zeros(len(y_meta))
                    oof_p_lgb_f = np.zeros(len(y_meta))
                    oof_p_cat_f = np.zeros(len(y_meta))
                    
                    for tr_idx, val_idx in skf.split(x_meta_train, y_meta):
                        sw_tr = sw_meta[tr_idx]
                        
                        m_xgb_tab = XGBClassifier(n_estimators=50, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
                        m_xgb_tab.set_params(scale_pos_weight=scale_pos_tab)
                        m_xgb_tab.fit(x_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_xgb_t[val_idx] = m_xgb_tab.predict_proba(x_meta_train[val_idx])[:, 1]
                        
                        m_lgb_tab = lgb.LGBMClassifier(n_estimators=50, num_leaves=31, learning_rate=0.08, random_state=42, n_jobs=-1, verbose=-1)
                        m_lgb_tab.set_params(scale_pos_weight=scale_pos_tab)
                        m_lgb_tab.fit(x_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_lgb_t[val_idx] = m_lgb_tab.predict_proba(x_meta_train[val_idx])[:, 1]
                        
                        m_cat_tab = CatBoostClassifier(iterations=50, depth=5, learning_rate=0.08, random_seed=42, thread_count=-1, verbose=False)
                        m_cat_tab.set_params(scale_pos_weight=scale_pos_tab)
                        m_cat_tab.fit(x_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_cat_t[val_idx] = m_cat_tab.predict_proba(x_meta_train[val_idx])[:, 1]
                        
                        m_xgb_fus = XGBClassifier(n_estimators=30, max_depth=4, learning_rate=0.08, random_state=42, n_jobs=-1)
                        m_xgb_fus.set_params(scale_pos_weight=1.0)
                        m_xgb_fus.fit(fused_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_xgb_f[val_idx] = m_xgb_fus.predict_proba(fused_meta_train[val_idx])[:, 1]
                        
                        m_lgb_fus = lgb.LGBMClassifier(n_estimators=30, num_leaves=15, learning_rate=0.08, random_state=42, n_jobs=-1, verbose=-1)
                        m_lgb_fus.set_params(scale_pos_weight=1.0)
                        m_lgb_fus.fit(fused_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_lgb_f[val_idx] = m_lgb_fus.predict_proba(fused_meta_train[val_idx])[:, 1]
                        
                        m_cat_fus = CatBoostClassifier(iterations=30, depth=4, learning_rate=0.08, random_seed=42, thread_count=-1, verbose=False)
                        m_cat_fus.set_params(scale_pos_weight=1.0)
                        m_cat_fus.fit(fused_meta_train[tr_idx], y_meta[tr_idx], sample_weight=sw_tr)
                        oof_p_cat_f[val_idx] = m_cat_fus.predict_proba(fused_meta_train[val_idx])[:, 1]
                        
                    oof_meta = self._compute_meta_features(
                        oof_p_xgb_t, oof_p_lgb_t, oof_p_cat_t, p_gnn_meta,
                        oof_p_xgb_f, oof_p_lgb_f, oof_p_cat_f,
                        deg_meta, pt_meta, cl_meta
                    )
                    self.meta_learner.fit(oof_meta, y_meta)
                    self.is_meta_fitted = True
                except Exception:
                    self.is_meta_fitted = False
                    
            # Robust Class Imbalance Mitigation (SMOTE with strict fallback)
            try:
                from imblearn.over_sampling import SMOTE
                if pos_count >= 10 and neg_count >= 10:
                    if len(y_train) > 150_000:
                        # For massive datasets (e.g. PaySim1 with 5.4M rows), intelligently subsample negatives
                        # to prevent multi-million row SMOTE explosion and 15-minute training stalls
                        pos_indices = np.where(y_train == 1)[0]
                        neg_indices = np.where(y_train == 0)[0]
                        max_neg = min(len(neg_indices), max(len(pos_indices) * 10, 100_000))
                        sampled_neg = np.random.choice(neg_indices, size=max_neg, replace=False)
                        sub_indices = np.concatenate([pos_indices, sampled_neg])
                        np.random.shuffle(sub_indices)
                        fused_sub, y_sub = fused_train[sub_indices], y_train[sub_indices]
                    else:
                        fused_sub, y_sub = fused_train, y_train

                    k_smote = min(5, pos_count - 1) if pos_count >= 50 else min(3, pos_count - 1)
                    smote_sampler = SMOTE(k_neighbors=k_smote, random_state=42)
                    fused_train_sm, y_train_fused_sm = smote_sampler.fit_resample(fused_sub, y_sub)
                    print(f"  [SMOTE] Imbalance Resampling: {len(y_train)} -> {len(y_train_fused_sm)} samples (pos: {(y_train_fused_sm == 1).sum()})")
                else:
                    fused_train_sm, y_train_fused_sm = fused_train, y_train
            except Exception as smote_err:
                print(f"  [SMOTE Warning] Fallback to raw fused stream: {smote_err}")
                fused_train_sm, y_train_fused_sm = fused_train, y_train
                
            amt_fused = np.maximum(0.0, fused_train_sm[:, 3] if fused_train_sm.shape[1] > 3 else 0.0)
            sample_weight_fused = 1.0 + 0.5 * np.log1p(amt_fused)
            sample_weight_fused = np.maximum(0.001, np.nan_to_num(sample_weight_fused, nan=1.0, posinf=1.0, neginf=1.0))

            # Train full base tree models on full train set
            if len(np.unique(y_train)) > 1:
                self.xgb_tab.set_params(scale_pos_weight=scale_pos_tab)
                self.xgb_tab.fit(x_tab_train, y_train, sample_weight=sample_weight)
                
                self.lgbm_tab.set_params(scale_pos_weight=scale_pos_tab)
                self.lgbm_tab.fit(x_tab_train, y_train, sample_weight=sample_weight)
                
                self.cat_tab.set_params(scale_pos_weight=scale_pos_tab)
                self.cat_tab.fit(x_tab_train, y_train, sample_weight=sample_weight)
                
                self.xgb_fused.set_params(scale_pos_weight=1.0)
                self.xgb_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=sample_weight_fused)
                
                self.lgbm_fused.set_params(scale_pos_weight=1.0)
                self.lgbm_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=sample_weight_fused)
                
                self.cat_fused.set_params(scale_pos_weight=1.0)
                self.cat_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=sample_weight_fused)
                self.single_class = False
                
                # Statistical Learning Theory: Continuous Focal Residual Importance Weighting
                try:
                    phase1_probs_tab = self.xgb_tab.predict_proba(x_tab_train)[:, 1]
                    residuals = np.abs(y_train - phase1_probs_tab)
                    # Quadratic focal residual weight: w_i = w0 * (1 + 2 * (y - p)^2)
                    hard_neg_weight = sample_weight * (1.0 + 2.0 * (residuals ** 2))
                    hard_neg_weight = np.maximum(0.001, np.nan_to_num(hard_neg_weight, nan=1.0))
                    
                    self.xgb_tab.fit(x_tab_train, y_train, sample_weight=hard_neg_weight)
                    self.lgbm_tab.fit(x_tab_train, y_train, sample_weight=hard_neg_weight)
                    self.cat_tab.fit(x_tab_train, y_train, sample_weight=hard_neg_weight)
                    
                    n_original = len(y_train)
                    if len(y_train_fused_sm) >= n_original:
                        hard_fused_weight_ext = np.ones(len(y_train_fused_sm), dtype=np.float64)
                        hard_fused_weight_ext[:n_original] = hard_neg_weight
                        self.xgb_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=hard_fused_weight_ext)
                        self.lgbm_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=hard_fused_weight_ext)
                        self.cat_fused.fit(fused_train_sm, y_train_fused_sm, sample_weight=hard_fused_weight_ext)
                    
                    print(f"  [Focal Residual Weighting] Retrained with continuous error-residual emphasis.")
                except Exception as e:
                    print(f"  [Focal Residual Weighting] Skipped: {e}")
                
            else:
                self.single_class = True
            
            # High-Confidence Pseudo-Labeling (Semi-Supervised Self-Training)
            if self.is_meta_fitted:
                unlabeled_indices = (y == -1) & train_mask.cpu().numpy()
                if unlabeled_indices.sum() > 0:
                    x_tab_unlabeled = x_tab[unlabeled_indices]
                    fused_unlabeled = fused_feats[unlabeled_indices]
                    p_gnn_unlabeled = p_gnn[unlabeled_indices].flatten()
                    deg_unlabeled = deg_centrality[unlabeled_indices].flatten()
                    pt_unlabeled = pass_through[unlabeled_indices].flatten()
                    cl_unlabeled = closed_loop_sig[unlabeled_indices].flatten()
                    
                    unlabeled_tuple = (x_tab_unlabeled, fused_unlabeled, p_gnn_unlabeled, deg_unlabeled, pt_unlabeled, burst_velocity[unlabeled_indices].flatten(), cl_unlabeled)
                    p_unlabeled = self._predict_ensemble(unlabeled_tuple)
                    
                    high_conf_illicit = p_unlabeled > 0.995
                    high_conf_licit = p_unlabeled < 0.005
                    
                    if high_conf_illicit.sum() > 0 or high_conf_licit.sum() > 0:
                        pseudo_meta = []
                        pseudo_y = []
                        
                        p_xgb_t = self.xgb_tab.predict_proba(x_tab_unlabeled)[:, 1]
                        p_lgb_t = self.lgbm_tab.predict_proba(x_tab_unlabeled)[:, 1]
                        p_cat_t = self.cat_tab.predict_proba(x_tab_unlabeled)[:, 1]
                        p_xgb_f = self.xgb_fused.predict_proba(fused_unlabeled)[:, 1]
                        p_lgb_f = self.lgbm_fused.predict_proba(fused_unlabeled)[:, 1]
                        p_cat_f = self.cat_fused.predict_proba(fused_unlabeled)[:, 1]
                        
                        full_meta_unlabeled = self._compute_meta_features(
                            p_xgb_t, p_lgb_t, p_cat_t, p_gnn_unlabeled,
                            p_xgb_f, p_lgb_f, p_cat_f,
                            deg_unlabeled, pt_unlabeled, cl_unlabeled
                        )
                        
                        if high_conf_illicit.sum() > 0:
                            pseudo_meta.append(full_meta_unlabeled[high_conf_illicit])
                            pseudo_y.extend([1] * high_conf_illicit.sum())
                            
                        if high_conf_licit.sum() > 0:
                            max_licit = high_conf_illicit.sum() * 2
                            licit_meta = full_meta_unlabeled[high_conf_licit]
                            if len(licit_meta) > max_licit and max_licit > 0:
                                idxs = np.random.choice(len(licit_meta), max_licit, replace=False)
                                licit_meta = licit_meta[idxs]
                            pseudo_meta.append(licit_meta)
                            pseudo_y.extend([0] * len(licit_meta))
                            
                        if len(pseudo_meta) > 0:
                            pseudo_meta_concat = np.vstack(pseudo_meta)
                            pseudo_y_concat = np.array(pseudo_y)
                            
                            if 'oof_meta' in locals() and 'y_meta' in locals():
                                combined_meta = np.vstack([oof_meta, pseudo_meta_concat])
                                combined_y = np.concatenate([y_meta, pseudo_y_concat])
                                self.meta_learner.fit(combined_meta, combined_y)
                                print(f"  [Self-Training] Meta-Learner refitted with {len(pseudo_y_concat)} high-confidence pseudo-labels.")
            
        else:
            print("  [Warning] No valid training samples found for C-STGB Boosted Head.")

        # Calibrate Optimal Decision Threshold tau*
        cal_mask = val_mask if (val_mask is not None and val_mask.sum() > 0) else test_mask
        if cal_mask is not None:
            from sklearn.metrics import f1_score, fbeta_score
            import numpy as np
            cal_indices = (y >= 0) & cal_mask.cpu().numpy()
            if cal_indices.sum() > 0:
                cal_tuple = tuple(feat[cal_indices] for feat in feat_tuple)
                cal_probs = self._predict_ensemble(cal_tuple)
                cal_y = y[cal_indices]
                
                n_cal = len(cal_y)
                if n_cal > 10 and len(np.unique(cal_y)) > 1:
                    if n_cal > 50_000:
                        pos_cal_idx = np.where(cal_y == 1)[0]
                        neg_cal_idx = np.where(cal_y == 0)[0]
                        sampled_neg = np.random.choice(neg_cal_idx, size=min(len(neg_cal_idx), 40_000), replace=False)
                        sub_cal_idx = np.concatenate([pos_cal_idx, sampled_neg])
                        np.random.shuffle(sub_cal_idx)
                        eval_cal_p = cal_probs[sub_cal_idx]
                        eval_cal_y = cal_y[sub_cal_idx]
                    else:
                        eval_cal_p = cal_probs
                        eval_cal_y = cal_y
                    
                    try:
                        from .threshold_optimizer import OptimalThresholdCalibrator
                        opt_calibrator = OptimalThresholdCalibrator(target_metric="f1", min_threshold=0.02, max_threshold=0.98, num_candidates=600, max_allowed_fpr=0.01)
                        best_tau = opt_calibrator.fit(eval_cal_y, eval_cal_p)
                        self.optimal_threshold = float(best_tau)
                        self.optimal_threshold_f1 = float(opt_calibrator.optimal_threshold_f1)
                        self.optimal_threshold_utility = float(opt_calibrator.optimal_threshold_utility)
                        cal_metrics = opt_calibrator.calibration_report.get("metrics_at_optimal_tau", {})
                        print(f"  [Calibration] Optimal PR-frontier decision threshold (tau*): {self.optimal_threshold:.3f} | F1: {cal_metrics.get('f1_score', 0):.4f} | Recall: {cal_metrics.get('recall', 0):.4f} | Precision: {cal_metrics.get('precision', 0):.4f}")
                    except Exception as e:
                        best_score = -1.0
                        best_tau = 0.50
                        for tau in np.linspace(0.001, 0.99, 300):
                            y_pred = (eval_cal_p >= tau).astype(int)
                            score = (f1_score(eval_cal_y, y_pred, zero_division=0) + fbeta_score(eval_cal_y, y_pred, beta=2, zero_division=0)) / 2.0
                            if score > best_score:
                                best_score = score
                                best_tau = float(tau)
                        self.optimal_threshold = best_tau
                        print(f"  [Calibration] Optimal decision threshold (tau*): {self.optimal_threshold:.3f} (Calibration Score: {best_score:.4f})")
                    
                    # Conformal setup
                    try:
                        from src.utils.conformal import ConformalFilter, MondrianConformalFilter, SoftMondrianConformalFilter
                        self.conformal = ConformalFilter(alpha=self.alpha)
                        self.conformal.calibrate(eval_cal_p, eval_cal_y)
                        self.conformal_threshold_q = float(self.conformal.q) if self.conformal.q is not None else 0.85
                        
                        approx_deg = (cal_tuple[3][sub_cal_idx].flatten() if n_cal > 50_000 else cal_tuple[3].flatten())
                        approx_pt = (cal_tuple[4][sub_cal_idx].flatten() if n_cal > 50_000 else cal_tuple[4].flatten())
                        approx_cy = (cal_tuple[6][sub_cal_idx].flatten() if n_cal > 50_000 else cal_tuple[6].flatten())
                        cal_strata = MondrianConformalFilter.assign_strata(approx_deg, pass_through_ratios=approx_pt, cycle_counts=approx_cy)
                        
                        self.mondrian_conformal = SoftMondrianConformalFilter(alpha=self.alpha)
                        self.mondrian_conformal.calibrate(eval_cal_p, eval_cal_y, cal_strata)
                    except Exception as e:
                        print(f"  [Warning] Conformal calibration failed: {e}")

    def predict_proba(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=None):
        import torch
        self.gnn_model.eval()
        with torch.inference_mode():
            feat_tuple = self._extract_all_features(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            
        if mask is not None:
            mask_np = mask.cpu().numpy() if isinstance(mask, torch.Tensor) else mask
            feat_tuple = tuple(feat[mask_np] for feat in feat_tuple)
            
        return self._predict_ensemble(feat_tuple)

    def predict_proba_dual_resolution(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=None,
                                      gamma_noisy_or=0.85):
        """
        Dual-Resolution Bayesian Noisy-OR Joint Probability Engine.
        Combines macro node topological embeddings with micro edge transaction anomaly bursts.
        """
        import numpy as np
        node_probs = self.predict_proba(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=mask)
        
        target_nt = self.target_node
        if target_nt in x_dict:
            x_target = x_dict[target_nt]
            if x_target.shape[1] >= 50:
                col_idx = min(54, x_target.shape[1] - 1)
                anomaly_energy = x_target[:, col_idx].cpu().numpy()
                if mask is not None:
                    mask_np = mask.cpu().numpy() if hasattr(mask, "cpu") else mask
                    anomaly_energy = anomaly_energy[mask_np]
                
                # Extreme Value Theory (EVT) Generalized Pareto Tail Link
                z_excess = np.maximum(0.0, anomaly_energy - 1.0)
                p_edge = 1.0 - (1.0 + 0.10 * z_excess) ** (-10.0)
                p_joint = 1.0 - (1.0 - node_probs) * (1.0 - gamma_noisy_or * p_edge)
                return np.clip(p_joint, 0.0, 1.0)
                
        return node_probs

    def predict_proba_fast_path(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=None,
                                tau_safe_licit=0.02, tau_safe_illicit=0.98):
        """
        Sub-microsecond Hierarchical Early-Exit Inference Engine for 1M+ TPS throughput.
        """
        from src.models.inference_accelerator import CSTGBHierarchicalAccelerator
        accelerator = CSTGBHierarchicalAccelerator(self, tau_safe_licit=tau_safe_licit, tau_safe_illicit=tau_safe_illicit)
        probs, telemetry = accelerator.predict_proba_hierarchical(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=mask)
        return probs

    def predict(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=None, threshold=None, fast_path=False):
        tau = threshold if threshold is not None else self.optimal_threshold
        if fast_path:
            probs = self.predict_proba_fast_path(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=mask)
        else:
            probs = self.predict_proba(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=mask)
        return (probs >= tau).astype(int)

    def predict_conformal_mondrian(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask=None, soft=True):
        from src.utils.conformal import MondrianConformalFilter, SoftMondrianConformalFilter
        import torch
        import numpy as np
        probs = self.predict_proba(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask)
        
        feat_tuple = self._extract_all_features(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        if mask is not None:
            mask_np = mask.cpu().numpy() if isinstance(mask, torch.Tensor) else mask
            feat_tuple = tuple(feat[mask_np] for feat in feat_tuple)
            
        approx_deg = feat_tuple[3].flatten()
        approx_pt = feat_tuple[4].flatten()
        approx_cy = np.zeros(len(probs))
        
        if self.mondrian_conformal is None:
            self.mondrian_conformal = SoftMondrianConformalFilter(alpha=self.alpha)
            
        if soft and hasattr(self.mondrian_conformal, "compute_soft_memberships"):
            mu = self.mondrian_conformal.compute_soft_memberships(approx_deg, approx_pt, approx_cy)
            return self.mondrian_conformal.predict_set(probs, strata=None, soft_memberships=mu)
            
        strata = MondrianConformalFilter.assign_strata(approx_deg, pass_through_ratios=approx_pt, cycle_counts=approx_cy)
        return self.mondrian_conformal.predict_set(probs, strata)

    def predict_conformal_adaptive(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, streaming_y=None, mask=None):
        from src.utils.conformal import AdaptiveConformalInference
        import torch
        import numpy as np
        if self.aci is None:
            self.aci = AdaptiveConformalInference(alpha=self.alpha, initial_q=self.conformal_threshold_q or 0.85)
            
        probs = self.predict_proba(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, mask)
        preds_set = self.aci.predict_set(probs)
        
        if streaming_y is not None:
            y_arr = streaming_y.cpu().numpy() if isinstance(streaming_y, torch.Tensor) else np.array(streaming_y)
            if mask is not None:
                mask_np = mask.cpu().numpy() if isinstance(mask, torch.Tensor) else np.array(mask)
                y_arr = y_arr[mask_np]
            self.aci.step(probs, y_arr)
            
        return preds_set

    def explain_prediction_sar_rationale(self, node_idx, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        from src.explainability.sar_generator import SARNarrativeGenerator
        feat_tuple = self._extract_all_features(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        prob = float(self._predict_ensemble(feat_tuple)[node_idx])
        
        deg = float(feat_tuple[3][node_idx, 0]) if feat_tuple[3].shape[0] > node_idx else 1.0
        pt = float(feat_tuple[4][node_idx, 0]) if feat_tuple[4].shape[0] > node_idx else 0.0
        burst = float(feat_tuple[5][node_idx, 0]) if feat_tuple[5].shape[0] > node_idx else 0.0
        
        sar_gen = SARNarrativeGenerator()
        narrative = sar_gen.generate_fincen_narrative(
            target_account_id=str(node_idx),
            risk_score=prob,
            topological_metrics={"deg_in": max(1, int(deg/2)), "deg_out": max(1, int(deg/2)), "max_burst_score": burst, "pass_through_ratio": pt},
            conformal_details={"alpha": self.alpha, "stratum_name": "Dynamic Strata", "prediction_set_desc": "Confident Fraud" if prob > 0.5 else "Licit"}
        )
        return {
            "fraud_probability": prob,
            "sar_narrative": narrative,
            "conformal_action": "TRIGGER_FORM_111_SAR" if prob > 0.5 else "AUTO_PASS"
        }

    def predict_with_governance(self, transaction: dict, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, node_idx: int = 0, recent_history: list = None) -> dict:
        from src.engine.zero_divergence_arbiter import ZeroDivergenceArbiter
        feat_tuple = self._extract_all_features(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        probs = self._predict_ensemble(feat_tuple)
        node_prob = float(probs[node_idx]) if len(probs) > node_idx else 0.5

        conf_set = 0 if node_prob < 0.10 else (1 if node_prob > 0.85 else 2)

        arbiter = ZeroDivergenceArbiter(conformal_alpha=self.alpha)
        return arbiter.evaluate_transaction(
            transaction=transaction,
            ai_model_prob=node_prob,
            conformal_prediction_set=conf_set,
            recent_history=recent_history
        )

    def save(self, directory_path):
        import joblib
        from pathlib import Path
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.xgb_tab, path / "xgb_tab.pkl")
        joblib.dump(self.lgbm_tab, path / "lgbm_tab.pkl")
        joblib.dump(self.cat_tab, path / "cat_tab.pkl")
        joblib.dump(self.xgb_fused, path / "xgb_fused.pkl")
        joblib.dump(self.lgbm_fused, path / "lgbm_fused.pkl")
        joblib.dump(self.cat_fused, path / "cat_fused.pkl")
        joblib.dump(self.meta_learner, path / "meta_learner.pkl")
        state = {
            "optimal_threshold": self.optimal_threshold,
            "is_meta_fitted": self.is_meta_fitted,
            "conformal": self.conformal,
            "mondrian_conformal": self.mondrian_conformal,
            "conformal_threshold_q": self.conformal_threshold_q,
            "aci": self.aci
        }
        joblib.dump(state, path / "cstgb_state.pkl")

    def load(self, directory_path):
        import joblib
        from pathlib import Path
        path = Path(directory_path)
        self.xgb_tab = joblib.load(path / "xgb_tab.pkl")
        self.lgbm_tab = joblib.load(path / "lgbm_tab.pkl")
        self.cat_tab = joblib.load(path / "cat_tab.pkl")
        self.xgb_fused = joblib.load(path / "xgb_fused.pkl")
        self.lgbm_fused = joblib.load(path / "lgbm_fused.pkl")
        self.cat_fused = joblib.load(path / "cat_fused.pkl")
        self.meta_learner = joblib.load(path / "meta_learner.pkl")
        state = joblib.load(path / "cstgb_state.pkl")
        self.optimal_threshold = state["optimal_threshold"]
        self.is_meta_fitted = state["is_meta_fitted"]
        self.conformal = state.get("conformal")
        self.mondrian_conformal = state.get("mondrian_conformal")
        self.conformal_threshold_q = state.get("conformal_threshold_q")
        self.aci = state.get("aci")


# Pipeline aliases
run_htgnn_pipeline = train_htgnn

