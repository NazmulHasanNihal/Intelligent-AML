"""
Deterministic Causal Invariant Engines for AML Benchmark Networks.

Implements exact symbolic equations and temporal geometric invariants
for PaySim, IBM-AMLSim, Credit Card Bipartite streams, and MtGox Trade Books.
"""

import numpy as np
import pandas as pd


def extract_paysim_exact_invariants(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the exact algebraic invariants that govern fraudulent transactions in PaySim.
    
    The PaySim synthetic generator produces fraud according to strict balance equations:
    1. Originator balance drain error: oldbalanceOrg - amount - newbalanceOrig == 0
    2. Destination balance deposit error: oldbalanceDest + amount - newbalanceDest == 0
    3. Complete account drainage: oldbalanceOrg > 0 and newbalanceOrig == 0
    4. Exact synthetic fraud signature: type in ('TRANSFER', 'CASH_OUT') and oldbalanceOrg == amount
    """
    df = df.copy()
    
    amount = df["amount"].values.astype(np.float64)
    old_orig = df["oldbalanceOrg"].values.astype(np.float64) if "oldbalanceOrg" in df.columns else df.get("oldbalanceOrig", pd.Series(0, index=df.index)).values.astype(np.float64)
    new_orig = df["newbalanceOrig"].values.astype(np.float64)
    old_dest = df["oldbalanceDest"].values.astype(np.float64)
    new_dest = df["newbalanceDest"].values.astype(np.float64)
    tx_type = df["type"].astype(str).str.upper().values if "type" in df.columns else np.array(["TRANSFER"] * len(df))
    
    # 1. Exact balance conservation residuals (Signed and Absolute)
    err_orig = old_orig - amount - new_orig
    err_dest = old_dest + amount - new_dest
    
    df["inv_err_balance_orig"] = err_orig.astype(np.float32)
    df["inv_err_balance_dest"] = err_dest.astype(np.float32)
    df["inv_abs_err_orig"] = np.abs(err_orig).astype(np.float32)
    df["inv_abs_err_dest"] = np.abs(err_dest).astype(np.float32)
    
    # 2. Conservation ratio: (newbalanceOrig + amount) / (oldbalanceOrg + 1e-5)
    df["inv_orig_conservation_ratio"] = ((new_orig + amount) / (old_orig + 1e-5)).astype(np.float32)
    
    # 3. Liquidation indicators
    df["inv_is_complete_orig_drain"] = ((old_orig > 0) & (new_orig == 0)).astype(np.float32)
    df["inv_is_dest_empty_prior"] = (old_dest == 0).astype(np.float32)
    df["inv_amount_equals_old_orig"] = (np.abs(amount - old_orig) < 1e-4).astype(np.float32)
    
    # 4. Overdraft / Phantom money anomaly
    df["inv_is_phantom_overdraft"] = (amount > (old_orig + 1.0)).astype(np.float32)
    
    # 5. Exact synthetic generator rule signature
    is_high_risk_type = np.isin(tx_type, ["TRANSFER", "CASH_OUT"])
    df["inv_exact_generator_signature"] = (
        is_high_risk_type & 
        (old_orig > 0) & 
        (new_orig == 0) & 
        (np.abs(amount - old_orig) < 1.0)
    ).astype(np.float32)
    
    # 6. Destination balance discrepancy flag
    # In PaySim fraud, cashout destinations often report newbalanceDest == 0 or unchanged
    df["inv_dest_balance_anomaly"] = (
        is_high_risk_type & (old_dest == 0) & (new_dest == 0) & (amount > 0)
    ).astype(np.float32)

    return df


def extract_ibm_amlsim_invariants(edges_df: pd.DataFrame, nodes_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Computes exact physical flow conservation and multi-day temporal delay invariants
    for IBM-AMLSim transaction networks.
    
    Identifies:
    1. Physical mass flow conservation ratio Φflow ≈ 1.0
    2. Smurfing Fan-Out (n_out >= 4, n_in <= 2) and Layering Fan-In (n_in >= 4, n_out <= 2)
    3. Multi-day dormancy conduit windows (t_out - t_in between 1 and 21 days)
    4. Rapid Scatter-Gather wash loops
    """
    edges_df = edges_df.copy()
    
    # Check column names
    src_col = "src" if "src" in edges_df.columns else "source"
    dst_col = "dst" if "dst" in edges_df.columns else "target"
    amt_col = "amount" if "amount" in edges_df.columns else "value"
    ts_col = "ts" if "ts" in edges_df.columns else ("timestamp" if "timestamp" in edges_df.columns else "time")
    
    has_ts = ts_col in edges_df.columns
    
    # Aggregate node volume statistics
    src_nodes = edges_df[src_col].values
    dst_nodes = edges_df[dst_col].values
    amounts = edges_df[amt_col].values.astype(np.float64) if amt_col in edges_df.columns else np.ones(len(edges_df), dtype=np.float64)
    timestamps = edges_df[ts_col].values.astype(np.float64) if has_ts else np.zeros(len(edges_df), dtype=np.float64)
    
    # Fast vectorized aggregation of node-level statistics
    out_df = pd.DataFrame({"node": src_nodes, "out_vol": amounts, "out_cnt": 1, "out_ts_min": timestamps, "out_ts_max": timestamps})
    out_stats = out_df.groupby("node").agg({
        "out_vol": "sum",
        "out_cnt": "sum",
        "out_ts_min": "min",
        "out_ts_max": "max"
    })
    
    in_df = pd.DataFrame({"node": dst_nodes, "in_vol": amounts, "in_cnt": 1, "in_ts_min": timestamps, "in_ts_max": timestamps})
    in_stats = in_df.groupby("node").agg({
        "in_vol": "sum",
        "in_cnt": "sum",
        "in_ts_min": "min",
        "in_ts_max": "max"
    })
    
    node_summary = out_stats.join(in_stats, how="outer").fillna(0.0)
    
    # Calculate Node-Level Invariants
    in_vol = node_summary["in_vol"].values
    out_vol = node_summary["out_vol"].values
    
    # 1. Mass flow conservation ratio Φflow
    min_vol = np.minimum(in_vol, out_vol)
    max_vol = np.maximum(in_vol, out_vol)
    phi_flow = np.where(max_vol > 0, min_vol / max_vol, 0.0)
    
    # Mule hub condition: high flow conservation (Phi > 0.85) with active in and out flows
    is_mule_conduit = (phi_flow >= 0.85) & (in_vol > 0) & (out_vol > 0)
    
    # 2. Fan-In and Fan-Out topology signatures
    in_cnt = node_summary["in_cnt"].values
    out_cnt = node_summary["out_cnt"].values
    is_smurfing_fan_out = (out_cnt >= 4) & (in_cnt <= 2)
    is_layering_fan_in = (in_cnt >= 4) & (out_cnt <= 2)
    is_scatter_gather = (in_cnt >= 3) & (out_cnt >= 3) & (phi_flow >= 0.80)
    
    # 3. Temporal dormancy: funds held for 1 to 21 days before release
    delta_days = (node_summary["out_ts_min"].values - node_summary["in_ts_max"].values) / 86400.0
    is_dormant_holding = (delta_days >= 1.0) & (delta_days <= 21.0) & (phi_flow >= 0.75)
    
    node_summary["node_phi_flow"] = phi_flow.astype(np.float32)
    node_summary["node_is_mule_conduit"] = is_mule_conduit.astype(np.float32)
    node_summary["node_is_smurfing_fan_out"] = is_smurfing_fan_out.astype(np.float32)
    node_summary["node_is_layering_fan_in"] = is_layering_fan_in.astype(np.float32)
    node_summary["node_is_scatter_gather"] = is_scatter_gather.astype(np.float32)
    node_summary["node_is_dormant_holding"] = is_dormant_holding.astype(np.float32)
    
    # Map back to edges
    src_mapped = edges_df[src_col].map(node_summary["node_phi_flow"]).fillna(0.0).values
    dst_mapped = edges_df[dst_col].map(node_summary["node_phi_flow"]).fillna(0.0).values
    edges_df["edge_src_phi_flow"] = src_mapped.astype(np.float32)
    edges_df["edge_dst_phi_flow"] = dst_mapped.astype(np.float32)
    edges_df["edge_is_conduit_chain"] = (
        edges_df[src_col].map(node_summary["node_is_mule_conduit"]).fillna(0.0) |
        edges_df[dst_col].map(node_summary["node_is_mule_conduit"]).fillna(0.0)
    ).astype(np.float32)
    
    edges_df["edge_is_smurfing_flow"] = (
        edges_df[src_col].map(node_summary["node_is_smurfing_fan_out"]).fillna(0.0) |
        edges_df[dst_col].map(node_summary["node_is_layering_fan_in"]).fillna(0.0)
    ).astype(np.float32)
    
    return edges_df, node_summary


def extract_credit_card_invariants(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts high-velocity burst and merchant degree-normalized invariants
    for credit card fraud transaction streams.
    """
    df = df.copy()
    amt_col = "Amount" if "Amount" in df.columns else ("amount" if "amount" in df.columns else None)
    time_col = "Time" if "Time" in df.columns else ("timestamp" if "timestamp" in df.columns else None)
    
    if amt_col is not None:
        amt = df[amt_col].values.astype(np.float64)
        # Log-amount anomaly
        log_amt = np.log1p(np.maximum(0.0, amt))
        df["inv_log_amount"] = log_amt.astype(np.float32)
        mean_log = np.mean(log_amt)
        std_log = np.std(log_amt) + 1e-5
        df["inv_amount_zscore"] = ((log_amt - mean_log) / std_log).astype(np.float32)
        df["inv_is_extreme_amount"] = (df["inv_amount_zscore"] > 3.0).astype(np.float32)
        
    if time_col is not None:
        t = df[time_col].values.astype(np.float64)
        # Inter-transaction arrival interval delta
        delta_t = np.diff(t, prepend=t[0])
        df["inv_delta_t_raw"] = delta_t.astype(np.float32)
        df["inv_is_rapid_burst"] = ((delta_t > 0) & (delta_t < 60.0)).astype(np.float32) # within 1 minute
        
    return df


def extract_mtgox_invariants(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts high-frequency algorithmic trade invariants for MtGox trade book analysis
    (identifying Willy Bot / Markus wash trading bursts).
    """
    df = df.copy()
    price_col = "Price" if "Price" in df.columns else ("price" if "price" in df.columns else None)
    amt_col = "Amount" if "Amount" in df.columns else ("amount" if "amount" in df.columns else None)
    time_col = "Time" if "Time" in df.columns else ("timestamp" if "timestamp" in df.columns else None)
    
    if price_col is not None and amt_col is not None:
        price = df[price_col].values.astype(np.float64)
        amount = df[amt_col].values.astype(np.float64)
        notional = price * amount
        df["inv_notional_volume"] = notional.astype(np.float32)
        
        # Micro-trade bot signature (e.g. constant small repeated volume)
        df["inv_is_micro_bot_order"] = ((amount >= 0.01) & (amount <= 0.05)).astype(np.float32)
        df["inv_is_whale_volume"] = (notional > np.percentile(notional, 99.0)).astype(np.float32)
        
    if time_col is not None:
        t = df[time_col].values.astype(np.float64)
        delta_t = np.diff(t, prepend=t[0])
        # High-frequency trading velocity (< 0.5 sec intervals)
        df["inv_is_hft_burst"] = ((delta_t >= 0) & (delta_t <= 0.5)).astype(np.float32)
        
    return df


class DeterministicInvariantsExtractor:
    """
    Unified Causal & Deterministic Invariants Extraction Engine.
    Maps known physical flow balance, temporal conduit windows, and simulator
    signatures into clean feature matrices for both GNN and Tree streams.
    """
    def __init__(self):
        pass

    def extract_node_features(self, nt_df: pd.DataFrame, edges_df: pd.DataFrame, dataset_name: str) -> np.ndarray:
        """
        Extracts high-precision node-level invariant features.
        Returns a numpy array of shape [num_nodes, K].
        """
        num_nodes = len(nt_df)
        if num_nodes == 0:
            return np.zeros((0, 8), dtype=np.float32)
            
        node_ids = nt_df["node_id"].values if "node_id" in nt_df.columns else nt_df.index.values
        node_to_idx = {nid: i for i, nid in enumerate(node_ids)}
        
        # Output feature buffer: 8 invariant dimensions
        # [0: phi_flow, 1: is_mule_conduit, 2: fan_out_ratio, 3: fan_in_ratio,
        #  4: is_drain_originator, 5: is_phantom_overdraft, 6: dormant_window_flag, 7: generator_exact_flag]
        feats = np.zeros((num_nodes, 8), dtype=np.float32)
        
        src_col = "src" if "src" in edges_df.columns else ("source" if "source" in edges_df.columns else None)
        dst_col = "dst" if "dst" in edges_df.columns else ("target" if "target" in edges_df.columns else None)
        amt_col = "amount" if "amount" in edges_df.columns else ("value" if "value" in edges_df.columns else ("Amount" if "Amount" in edges_df.columns else None))
        ts_col = "ts" if "ts" in edges_df.columns else ("timestamp" if "timestamp" in edges_df.columns else ("Time" if "Time" in edges_df.columns else None))
        
        if src_col is None or dst_col is None:
            return feats
            
        src_vals = edges_df[src_col].values
        dst_vals = edges_df[dst_col].values
        amt_vals = edges_df[amt_col].values.astype(np.float64) if amt_col in edges_df.columns else np.ones(len(edges_df), dtype=np.float64)
        ts_vals = edges_df[ts_col].values.astype(np.float64) if ts_col in edges_df.columns else np.zeros(len(edges_df), dtype=np.float64)
        
        # 1. Flow conservation Φflow and In/Out volumes
        out_agg = pd.DataFrame({"nid": src_vals, "amt": amt_vals, "ts": ts_vals}).groupby("nid").agg(
            out_vol=("amt", "sum"), out_cnt=("amt", "count"), out_ts_min=("ts", "min"), out_ts_max=("ts", "max")
        )
        in_agg = pd.DataFrame({"nid": dst_vals, "amt": amt_vals, "ts": ts_vals}).groupby("nid").agg(
            in_vol=("amt", "sum"), in_cnt=("amt", "count"), in_ts_min=("ts", "min"), in_ts_max=("ts", "max")
        )
        
        combined = out_agg.join(in_agg, how="outer").fillna(0.0)
        c_nids = combined.index.values
        c_in_vol = combined["in_vol"].values
        c_out_vol = combined["out_vol"].values
        c_in_cnt = combined["in_cnt"].values
        c_out_cnt = combined["out_cnt"].values
        
        # Vectorized flow conservation
        max_v = np.maximum(c_in_vol, c_out_vol)
        min_v = np.minimum(c_in_vol, c_out_vol)
        c_phi = np.where(max_v > 0, min_v / max_v, 0.0)
        c_mule = ((c_phi >= 0.85) & (c_in_vol > 0) & (c_out_vol > 0)).astype(np.float32)
        c_fan_out = np.where(c_in_cnt > 0, c_out_cnt / c_in_cnt, c_out_cnt).astype(np.float32)
        c_fan_in = np.where(c_out_cnt > 0, c_in_cnt / c_out_cnt, c_in_cnt).astype(np.float32)
        
        # Dormant holding (1 to 21 days delay)
        c_delay_days = (combined["out_ts_min"].values - combined["in_ts_max"].values) / 86400.0
        c_dormant = ((c_delay_days >= 1.0) & (c_delay_days <= 21.0) & (c_phi >= 0.70)).astype(np.float32)
        
        # Map back to target nodes
        for idx_c, nid in enumerate(c_nids):
            if nid in node_to_idx:
                target_i = node_to_idx[nid]
                feats[target_i, 0] = c_phi[idx_c]
                feats[target_i, 1] = c_mule[idx_c]
                feats[target_i, 2] = np.log1p(min(100.0, c_fan_out[idx_c]))
                feats[target_i, 3] = np.log1p(min(100.0, c_fan_in[idx_c]))
                feats[target_i, 6] = c_dormant[idx_c]
                
        # PaySim specialized invariant extraction
        if "paysim" in dataset_name.lower():
            old_orig_col = "oldbalanceOrg" if "oldbalanceOrg" in edges_df.columns else ("oldbalanceOrig" if "oldbalanceOrig" in edges_df.columns else None)
            new_orig_col = "newbalanceOrig" if "newbalanceOrig" in edges_df.columns else None
            
            if old_orig_col is not None and new_orig_col is not None:
                old_o = edges_df[old_orig_col].values.astype(np.float64)
                new_o = edges_df[new_orig_col].values.astype(np.float64)
                drain_mask = (old_o > 0) & (new_o == 0)
                phantom_mask = amt_vals > (old_o + 1.0)
                
                type_col = "type" if "type" in edges_df.columns else None
                if type_col is not None:
                    tx_t = edges_df[type_col].astype(str).str.upper().values
                    exact_sig = np.isin(tx_t, ["TRANSFER", "CASH_OUT"]) & drain_mask & (np.abs(amt_vals - old_o) < 1.0)
                else:
                    exact_sig = drain_mask & (np.abs(amt_vals - old_o) < 1.0)
                    
                drain_srcs = src_vals[drain_mask]
                for s in drain_srcs:
                    if s in node_to_idx:
                        feats[node_to_idx[s], 4] = 1.0
                        
                phantom_srcs = src_vals[phantom_mask]
                for s in phantom_srcs:
                    if s in node_to_idx:
                        feats[node_to_idx[s], 5] = 1.0
                        
                exact_srcs = src_vals[exact_sig]
                for s in exact_srcs:
                    if s in node_to_idx:
                        feats[node_to_idx[s], 7] = 1.0

        return feats

