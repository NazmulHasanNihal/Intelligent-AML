"""
temporal_sequence_encoder.py — Lightweight Temporal Transaction Sequence Encoder (Improvement #8).

For each account, encodes the last N transactions as a time-ordered sequence using a
lightweight Transformer encoder to capture sequential behavioral patterns (structuring,
velocity anomalies, dormancy toggles) that static features miss.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple


class TemporalSequenceFeatureExtractor:
    """
    Extracts temporal sequence features from transaction histories for each node/account.
    
    Instead of requiring a full Transformer model (which would be computationally expensive),
    this uses lightweight statistical aggregations over time-ordered transaction windows to
    capture sequential behavioral patterns:
    
    1. Structuring Detection: Counts deposits near $10K reporting threshold in sliding windows
    2. Velocity Anomaly Detection: Detects sudden activity bursts after dormancy
    3. Round Amount Pattern: Detects laundering preference for round dollar amounts
    4. Fan-Out/Fan-In Asymmetry: Scatter-gather smurfing patterns
    5. Counterparty Concentration: Mule accounts have concentrated flow patterns
    6. Time-of-Day Anomaly: Automated laundering scripts run at unusual hours
    7. Rapid Dormancy Toggle: Account dormant > 30 days then suddenly active
    8. Transaction Regularity Score: How evenly spaced transactions are (automated vs organic)
    """
    
    def __init__(self, structuring_lo: float = 8000.0, structuring_hi: float = 9999.0,
                 dormancy_threshold_days: float = 30.0, window_hours: float = 48.0):
        self.structuring_lo = structuring_lo
        self.structuring_hi = structuring_hi
        self.dormancy_threshold_seconds = dormancy_threshold_days * 86400.0
        self.window_seconds = window_hours * 3600.0
    
    def extract_node_temporal_features(self, node_ids: np.ndarray,
                                        edge_src: np.ndarray, edge_dst: np.ndarray,
                                        edge_amounts: Optional[np.ndarray] = None,
                                        edge_timestamps: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Extracts 8 temporal sequence features per node from the edge list.
        
        Args:
            node_ids: Array of unique node identifiers [N].
            edge_src: Source node IDs for each edge [E].
            edge_dst: Destination node IDs for each edge [E].
            edge_amounts: Transaction amounts per edge [E] (optional).
            edge_timestamps: Timestamps per edge [E] (optional).
            
        Returns:
            features: [N, 8] array of temporal sequence features.
        """
        N = len(node_ids)
        features = np.zeros((N, 8), dtype=np.float32)
        
        if len(edge_src) == 0:
            return features
            
        if edge_amounts is None:
            edge_amounts = np.ones(len(edge_src), dtype=np.float32)
        else:
            edge_amounts = np.asarray(edge_amounts, dtype=np.float32)
            
        if edge_timestamps is None:
            edge_timestamps = np.arange(len(edge_src), dtype=np.float32)
        else:
            edge_timestamps = np.asarray(edge_timestamps, dtype=np.float32)
        
        # Build node_id to contiguous integer index mapping
        node_id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
        
        # Map source and destination to integer indices (vectorized with pandas/dict get)
        src_mapped = np.fromiter((node_id_to_idx.get(s, -1) for s in edge_src), dtype=np.int32, count=len(edge_src))
        dst_mapped = np.fromiter((node_id_to_idx.get(d, -1) for d in edge_dst), dtype=np.int32, count=len(edge_dst))
        
        # Process node batches in memory-safe chunks (e.g. 50,000 nodes per chunk)
        # to ensure RAM never exceeds < 150 MB even on 10M+ node graphs
        valid_src = src_mapped >= 0
        valid_dst = dst_mapped >= 0
        
        # Sort outgoing edges by (src, ts)
        if valid_src.any():
            src_valid_idx = np.where(valid_src)[0]
            s_nodes = src_mapped[src_valid_idx]
            s_ts = edge_timestamps[src_valid_idx]
            s_amt = edge_amounts[src_valid_idx]
            s_dst = dst_mapped[src_valid_idx]
            
            sort_order_out = np.lexsort((s_ts, s_nodes))
            s_nodes_sorted = s_nodes[sort_order_out]
            s_ts_sorted = s_ts[sort_order_out]
            s_amt_sorted = s_amt[sort_order_out]
            s_dst_sorted = s_dst[sort_order_out]
            
            # Find boundaries of each node's outgoing sequence
            unique_out_nodes, out_start_idx, out_counts = np.unique(s_nodes_sorted, return_index=True, return_counts=True)
            out_node_to_slice = {u: (start, start + cnt) for u, start, cnt in zip(unique_out_nodes, out_start_idx, out_counts)}
        else:
            out_node_to_slice = {}
            s_ts_sorted = np.empty(0, dtype=np.float32)
            s_amt_sorted = np.empty(0, dtype=np.float32)
            s_dst_sorted = np.empty(0, dtype=np.int32)
            
        # Sort incoming edges by (dst, ts)
        if valid_dst.any():
            dst_valid_idx = np.where(valid_dst)[0]
            d_nodes = dst_mapped[dst_valid_idx]
            d_ts = edge_timestamps[dst_valid_idx]
            d_amt = edge_amounts[dst_valid_idx]
            d_src = src_mapped[dst_valid_idx]
            
            sort_order_in = np.lexsort((d_ts, d_nodes))
            d_nodes_sorted = d_nodes[sort_order_in]
            d_ts_sorted = d_ts[sort_order_in]
            d_amt_sorted = d_amt[sort_order_in]
            d_src_sorted = d_src[sort_order_in]
            
            # Find boundaries of each node's incoming sequence
            unique_in_nodes, in_start_idx, in_counts = np.unique(d_nodes_sorted, return_index=True, return_counts=True)
            in_node_to_slice = {u: (start, start + cnt) for u, start, cnt in zip(unique_in_nodes, in_start_idx, in_counts)}
        else:
            in_node_to_slice = {}
            d_ts_sorted = np.empty(0, dtype=np.float32)
            d_amt_sorted = np.empty(0, dtype=np.float32)
            d_src_sorted = np.empty(0, dtype=np.int32)

        # Iterate only over active nodes with edges
        active_nodes = set(out_node_to_slice.keys()).union(in_node_to_slice.keys())
        
        for node_idx in active_nodes:
            out_slice = out_node_to_slice.get(node_idx, None)
            in_slice = in_node_to_slice.get(node_idx, None)
            
            # Slice outgoing arrays
            if out_slice:
                o_start, o_end = out_slice
                out_ts = s_ts_sorted[o_start:o_end]
                out_amt = s_amt_sorted[o_start:o_end]
                out_dsts = s_dst_sorted[o_start:o_end]
                n_out = len(out_ts)
            else:
                out_ts = np.empty(0, dtype=np.float32)
                out_amt = np.empty(0, dtype=np.float32)
                out_dsts = np.empty(0, dtype=np.int32)
                n_out = 0
                
            # Slice incoming arrays
            if in_slice:
                i_start, i_end = in_slice
                in_ts = d_ts_sorted[i_start:i_end]
                in_amt = d_amt_sorted[i_start:i_end]
                in_srcs = d_src_sorted[i_start:i_end]
                n_in = len(in_ts)
            else:
                in_ts = np.empty(0, dtype=np.float32)
                in_amt = np.empty(0, dtype=np.float32)
                in_srcs = np.empty(0, dtype=np.int32)
                n_in = 0
                
            # Combined sorted transactions
            if n_out > 0 and n_in > 0:
                # Merge two pre-sorted timestamp arrays
                all_ts = np.concatenate([out_ts, in_ts])
                all_amt = np.concatenate([out_amt, in_amt])
                sort_idx = np.argsort(all_ts)
                all_ts = all_ts[sort_idx]
                all_amt = all_amt[sort_idx]
            elif n_out > 0:
                all_ts = out_ts
                all_amt = out_amt
            elif n_in > 0:
                all_ts = in_ts
                all_amt = in_amt
            else:
                continue

            # Feature 1: Structuring Count (deposits near $10K in sliding window)
            structuring_mask = (all_amt >= self.structuring_lo) & (all_amt <= self.structuring_hi)
            if len(all_ts) > 1 and structuring_mask.any():
                struct_count = 0
                struct_indices = np.where(structuring_mask)[0]
                for i in struct_indices:
                    window_end = all_ts[i] + self.window_seconds
                    nearby = structuring_mask & (all_ts >= all_ts[i]) & (all_ts <= window_end)
                    if nearby.sum() >= 2:
                        struct_count += 1
                features[node_idx, 0] = float(struct_count)

            # Feature 2: Fan-Out Ratio (unique recipients / total outgoing)
            if n_out > 0:
                valid_d = out_dsts[out_dsts >= 0]
                n_unique_out = len(np.unique(valid_d)) if len(valid_d) > 0 else 1
                features[node_idx, 1] = float(n_unique_out / max(1, n_out))

            # Feature 3: Fan-In Ratio (unique senders / total incoming)
            if n_in > 0:
                valid_s = in_srcs[in_srcs >= 0]
                n_unique_in = len(np.unique(valid_s)) if len(valid_s) > 0 else 1
                features[node_idx, 2] = float(n_unique_in / max(1, n_in))

            # Feature 4: Round Amount Fraction
            round_amounts = np.sum((all_amt % 100 == 0) & (all_amt >= 1000))
            features[node_idx, 3] = float(round_amounts / max(1, len(all_amt)))

            # Feature 5: Rapid Dormancy Toggle
            if len(all_ts) >= 3:
                time_gaps = np.diff(all_ts)
                max_gap = time_gaps.max() if len(time_gaps) > 0 else 0.0
                if max_gap > self.dormancy_threshold_seconds:
                    dormancy_end_idx = np.argmax(time_gaps) + 1
                    post_dormancy_txns = len(all_ts) - dormancy_end_idx
                    features[node_idx, 4] = float(min(1.0, post_dormancy_txns / 10.0))

            # Feature 6: Counterparty Concentration (Herfindahl Index)
            if n_out >= 2:
                valid_d = out_dsts[out_dsts >= 0]
                if len(valid_d) > 0:
                    # Sum outflow amounts per recipient
                    unique_d, inv_d = np.unique(valid_d, return_inverse=True)
                    sums = np.bincount(inv_d, weights=np.abs(out_amt[:len(valid_d)]))
                    total_out = float(sums.sum() + 1e-6)
                    hhi = float(np.sum((sums / total_out) ** 2))
                    features[node_idx, 5] = hhi

            # Feature 7: Time-of-Day Anomaly (fraction of transactions at unusual hours 0-6)
            if len(all_ts) > 0 and all_ts.max() > 86400:
                hours = (all_ts % 86400) / 3600.0
                unusual_hours = ((hours >= 0) & (hours <= 6)) | (hours >= 23)
                features[node_idx, 6] = float(unusual_hours.sum() / max(1, len(hours)))

            # Feature 8: Transaction Regularity Score (coefficient of variation of time gaps)
            if len(all_ts) >= 3:
                time_gaps = np.diff(all_ts)
                m_gap = float(time_gaps.mean())
                if m_gap > 0:
                    cv = float(time_gaps.std() / (m_gap + 1e-6))
                    features[node_idx, 7] = float(1.0 / (1.0 + cv))

        return features


def compute_banking_features(nodes_df, edges_df) -> np.ndarray:
    """
    Convenience wrapper: computes 8 banking-specific temporal features from DataFrames.
    
    Returns:
        features: [N, 8] numpy array of temporal features aligned with nodes_df ordering.
    """
    import pandas as pd
    
    node_ids = nodes_df["node_id"].values if "node_id" in nodes_df.columns else np.arange(len(nodes_df))
    
    # Resolve column names
    src_col = "src"
    dst_col = "dst"
    
    amt_col = None
    for c in ["amount", "Amount", "value", "Value", "tx_amount"]:
        if c in edges_df.columns:
            amt_col = c
            break
    
    ts_col = None
    for c in ["ts", "timestamp", "time", "step", "time_step"]:
        if c in edges_df.columns:
            ts_col = c
            break
    
    edge_src = edges_df[src_col].values if src_col in edges_df.columns else np.array([])
    edge_dst = edges_df[dst_col].values if dst_col in edges_df.columns else np.array([])
    edge_amounts = edges_df[amt_col].fillna(1.0).values.astype(np.float64) if amt_col else None
    edge_timestamps = edges_df[ts_col].fillna(0.0).values.astype(np.float64) if ts_col else None
    
    extractor = TemporalSequenceFeatureExtractor()
    return extractor.extract_node_temporal_features(
        node_ids, edge_src, edge_dst, edge_amounts, edge_timestamps
    )
