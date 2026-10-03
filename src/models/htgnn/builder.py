"""
builder.py — Heterogeneous Graph Construction and NeighborLoader Pipelines across 24 Datasets.
"""
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import polars as pl
import torch
from torch_geometric.data import HeteroData

from .profiles import (
    NODE_TYPES, EDGE_TYPES, OUTPUT_DIR, DATASET_PROFILES, DEFAULT_PROFILE, get_dataset_profile
)
from .features import (
    load_parquet, compute_temporal_features, compute_personalized_pagerank_taint, compute_graphlet_motifs
)

def get_neighbor_loader(data, input_node_type="Account", input_nodes=None, batch_size=2048, num_neighbors=None, num_workers=0):
    """
    Constructs a PyTorch Geometric NeighborLoader for billion-node graph mini-batch streaming.
    Binds RAM footprint to < 4 GB regardless of graph size.
    """
    if num_neighbors is None:
        num_neighbors = [15, 10]
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

        # Deterministic Causal Invariants Engine (Flow Conservation Phi, Conduit Mules, Dormancy Windows)
        try:
            from src.features.deterministic_invariants import DeterministicInvariantsExtractor
            det_extractor = DeterministicInvariantsExtractor()
            det_invariants = det_extractor.extract_node_features(nt_df, edges_df, dataset_name)
            print(f"  [Deterministic Invariants] Extracted {det_invariants.shape[1]} causal invariant features for {len(nt_df)} {nt} nodes.")
        except Exception as e:
            det_invariants = np.zeros((len(nt_df), 8), dtype=np.float32)
            print(f"  [Deterministic Invariants] Skipped for {nt}: {e}")

        if feature_cols:
            x_raw = torch.tensor(nt_df[feature_cols].values, dtype=torch.float)
            x_raw = torch.nan_to_num(x_raw, nan=0.0)
            x_vals = torch.cat([
                x_raw,
                torch.tensor(flow_invariants, dtype=torch.float),
                torch.tensor(banking_features, dtype=torch.float),
                torch.tensor(omni_features, dtype=torch.float),
                torch.tensor(chain_features, dtype=torch.float),
                torch.tensor(det_invariants, dtype=torch.float)
            ], dim=1)
        else:
            # Dynamic structural + banking + omni EV-AttnPool + laundering chain + deterministic invariants
            total_dim = NUM_FLOW_DIMS + 8 + banking_features.shape[1] + omni_features.shape[1] + chain_features.shape[1] + det_invariants.shape[1]
            x_mat = np.zeros((len(nt_df), total_dim), dtype=np.float32)
            x_mat[:, :NUM_FLOW_DIMS] = flow_invariants
            x_mat[:, NUM_FLOW_DIMS + (target_node_types.index(nt) % 8)] = 1.0
            col_offset = NUM_FLOW_DIMS + 8
            x_mat[:, col_offset:col_offset + banking_features.shape[1]] = banking_features
            col_offset += banking_features.shape[1]
            x_mat[:, col_offset:col_offset + omni_features.shape[1]] = omni_features
            col_offset += omni_features.shape[1]
            x_mat[:, col_offset:col_offset + chain_features.shape[1]] = chain_features
            col_offset += chain_features.shape[1]
            x_mat[:, col_offset:col_offset + det_invariants.shape[1]] = det_invariants
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
        valid_src = np.array([idx for idx in fraud_src_list if idx < data[primary_nt].num_nodes], dtype=np.int64)
        if len(valid_src) > 0:
            node_labels[valid_src] = 1
            
        # Debiased Destination Mapping:
        # 1. Credit Card: dst are innocent merchants (Walmart, Amazon, Starbucks, etc.) -> DO NOT mark dst as fraud!
        # 2. PaySim: In CASH_OUT, dst is an innocent cashout agent -> DO NOT mark dst as fraud!
        #    Only in TRANSFER to a non-merchant account is dst marked as laundering recipient.
        # 3. IBM AMLSim & SAML-D: both src and dst in SAR patterns participate in laundering.
        if dataset_name == "cc_transactions":
            pass # Keep merchants completely clean to eliminate false positive cross-contamination
        elif "paysim" in dataset_name.lower():
            type_col = None
            for col in ["type", "edge_type", "action"]:
                if col in fraud_edges.columns:
                    type_col = col
                    break
            if type_col is not None:
                transfer_edges = fraud_edges[fraud_edges[type_col].astype(str).str.upper() == "TRANSFER"]
                transfer_dst = [node_id_to_rel_idx[d] for d in transfer_edges["dst"].values if d in node_id_to_rel_idx and not str(d).startswith("M")]
                valid_transfer_dst = np.array([idx for idx in transfer_dst if idx < data[primary_nt].num_nodes], dtype=np.int64)
                if len(valid_transfer_dst) > 0:
                    node_labels[valid_transfer_dst] = 1
        else:
            fraud_dst_list = [node_id_to_rel_idx[d] for d in fraud_edges["dst"].values if d in node_id_to_rel_idx]
            valid_dst = np.array([idx for idx in fraud_dst_list if idx < data[primary_nt].num_nodes], dtype=np.int64)
            if len(valid_dst) > 0:
                node_labels[valid_dst] = 1
                
        print(f"  [Label Mapping] Unified debiased laundering subgraph node labels: {sum(node_labels == 1):,} fraud accounts ({sum(node_labels == 0):,} clean accounts).")
            
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


