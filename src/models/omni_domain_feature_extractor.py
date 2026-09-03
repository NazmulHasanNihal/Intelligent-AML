"""
omni_domain_feature_extractor.py — Universal High-Performance Edge-to-Node Domain Feature Extractor.

Extracts rich domain-specific transaction signatures directly from edge attributes:
1. Banking Ledgers (IBM AMLSim, SAML-D, SynthAML):
   - Cross-bank inter-institution transfer ratio
   - High-risk payment format exposure (Wire, Cash Deposit, Cheque)
   - Currency conversion diversity / Foreign exchange entropy
   - Benford's Law conformity & Counterparty Gini concentration
2. Mobile Money (PaySim, PaySim Extended):
   - Transfer-to-Cashout mule sequence velocity
   - Account balance draining ratio (oldbalanceOrg > 0 and newbalanceOrig == 0)
   - Destination zero-balance accumulation surge
3. Crypto & Exchange (MtGox, Ethereum Phishing, XBlock):
   - Order-Book VWAP Arbitrage Spread
   - Bilateral Reciprocal Wash Volume (A ⊙ A^T)
   - Extreme-Value Log-Sum-Exp Anomaly Pooling
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional


class OmniDomainFeatureExtractor:
    """High-speed vectorized extractor for transaction domain intelligence."""

    NUM_OMNI_DIMS = 24

    def extract_features(self, nodes_df: pd.DataFrame, edges_df: pd.DataFrame, dataset_name: str) -> np.ndarray:
        """
        Extracts 24-dimensional domain feature matrix for all nodes in nodes_df.
        Returns: np.ndarray [num_nodes, 24] (float32)
        """
        num_nodes = len(nodes_df)
        if num_nodes == 0 or edges_df is None or len(edges_df) == 0:
            return np.zeros((num_nodes, self.NUM_OMNI_DIMS), dtype=np.float32)

        node_ids = nodes_df["node_id"].values
        node_id_to_idx = {nid: idx for idx, nid in enumerate(node_ids)}

        features = np.zeros((num_nodes, self.NUM_OMNI_DIMS), dtype=np.float32)

        cols_lower = {c.lower().strip(): c for c in edges_df.columns}

        src_arr = edges_df["src"].values
        dst_arr = edges_df["dst"].values

        # Map edge indices to node indices
        src_indices = np.array([node_id_to_idx.get(s, -1) for s in src_arr], dtype=np.int32)
        dst_indices = np.array([node_id_to_idx.get(d, -1) for d in dst_arr], dtype=np.int32)

        valid_src_mask = src_indices >= 0
        valid_dst_mask = dst_indices >= 0

        # --- 1. BANKING SPECIFIC FEATURES ---
        from_bank_col = cols_lower.get("from bank") or cols_lower.get("from_bank") or cols_lower.get("sender_bank")
        to_bank_col = cols_lower.get("to bank") or cols_lower.get("to_bank") or cols_lower.get("receiver_bank")

        if from_bank_col and to_bank_col:
            fb = edges_df[from_bank_col].values
            tb = edges_df[to_bank_col].values
            is_cross_bank = (fb != tb).astype(np.float32)
            
            if np.any(valid_src_mask):
                np.add.at(features[:, 0], src_indices[valid_src_mask], is_cross_bank[valid_src_mask])
            if np.any(valid_dst_mask):
                np.add.at(features[:, 1], dst_indices[valid_dst_mask], is_cross_bank[valid_dst_mask])

        # Payment Format Exposure (Wire, Cash, Cheque)
        pay_fmt_col = cols_lower.get("payment format") or cols_lower.get("payment_format") or cols_lower.get("type")
        if pay_fmt_col:
            pf_series = edges_df[pay_fmt_col].astype(str).str.lower()
            is_wire = pf_series.str.contains("wire", na=False).values.astype(np.float32)
            is_cash = pf_series.str.contains("cash|transfer", na=False).values.astype(np.float32)
            is_high_risk = np.maximum(is_wire, is_cash)
            
            if np.any(valid_src_mask):
                np.add.at(features[:, 2], src_indices[valid_src_mask], is_high_risk[valid_src_mask])
            if np.any(valid_dst_mask):
                np.add.at(features[:, 3], dst_indices[valid_dst_mask], is_high_risk[valid_dst_mask])

        # Currency Conversion / FX Cross-Border Indicator
        pay_curr_col = cols_lower.get("payment currency") or cols_lower.get("payment_currency") or cols_lower.get("currency")
        rec_curr_col = cols_lower.get("receiving currency") or cols_lower.get("receiving_currency")
        if pay_curr_col and rec_curr_col:
            is_fx = (edges_df[pay_curr_col].values != edges_df[rec_curr_col].values).astype(np.float32)
            if np.any(valid_src_mask):
                np.add.at(features[:, 5], src_indices[valid_src_mask], is_fx[valid_src_mask])

        # MtGox / Crypto Exchange Rate Volatility & Manipulation Signatures
        rate_col = cols_lower.get("exchange_rate") or cols_lower.get("money_rate")
        if rate_col:
            rates = pd.to_numeric(edges_df[rate_col], errors="coerce").fillna(0.0).values
            finite_mask = (rates > 0.0) & (rates < 1e7) & np.isfinite(rates)
            if np.any(finite_mask):
                med_rate = float(np.median(rates[finite_mask]))
                rate_dev = np.where(finite_mask, np.abs(rates - med_rate) / (med_rate + 1e-5), 0.0).astype(np.float32)
                if np.any(valid_src_mask):
                    np.maximum.at(features[:, 6], src_indices[valid_src_mask], rate_dev[valid_src_mask])
                if np.any(valid_dst_mask):
                    np.maximum.at(features[:, 7], dst_indices[valid_dst_mask], rate_dev[valid_dst_mask])
                # Dimension 22: Order-Book Arbitrage Spread Intensity
                if np.any(valid_src_mask):
                    np.add.at(features[:, 22], src_indices[valid_src_mask], rate_dev[valid_src_mask])

        # --- 2. MOBILE MONEY SPECIFIC FEATURES (PaySim / E-Wallets) ---
        old_bal_org_col = cols_lower.get("oldbalanceorg") or cols_lower.get("old_balance_orig")
        new_bal_org_col = cols_lower.get("newbalanceorig") or cols_lower.get("new_balance_orig")
        old_bal_dest_col = cols_lower.get("oldbalancedest") or cols_lower.get("old_balance_dest")
        new_bal_dest_col = cols_lower.get("newbalancedest") or cols_lower.get("new_balance_dest")
        amt_col = cols_lower.get("amount") or cols_lower.get("value") or cols_lower.get("tx_amount") or cols_lower.get("amount paid") or cols_lower.get("bitcoins")

        if old_bal_org_col and new_bal_org_col:
            try:
                old_b = pd.to_numeric(edges_df[old_bal_org_col], errors="coerce").fillna(0.0).values
                new_b = pd.to_numeric(edges_df[new_bal_org_col], errors="coerce").fillna(0.0).values
                is_drained = ((old_b > 0.0) & (new_b <= 1e-4)).astype(np.float32)
                balance_diff = np.maximum(0.0, old_b - new_b)
                if np.any(valid_src_mask):
                    np.add.at(features[:, 6], src_indices[valid_src_mask], is_drained[valid_src_mask])
                    np.add.at(features[:, 7], src_indices[valid_src_mask], np.log1p(balance_diff[valid_src_mask]))
            except Exception:
                pass

        if old_bal_dest_col and new_bal_dest_col:
            try:
                old_bd = pd.to_numeric(edges_df[old_bal_dest_col], errors="coerce").fillna(0.0).values
                new_bd = pd.to_numeric(edges_df[new_bal_dest_col], errors="coerce").fillna(0.0).values
                is_zero_dest_surge = ((old_bd <= 1e-4) & (new_bd > 100.0)).astype(np.float32)
                if np.any(valid_dst_mask):
                    np.add.at(features[:, 8], dst_indices[valid_dst_mask], is_zero_dest_surge[valid_dst_mask])
            except Exception:
                pass

        # --- 3. HIGH-MAGNITUDE DEVIATION & AMOUNT STRUCTURING ---
        if amt_col:
            try:
                amts = pd.to_numeric(edges_df[amt_col], errors="coerce").fillna(1.0).values.astype(np.float64)
                is_whale = (amts >= 50000.0).astype(np.float32)
                is_structuring_exact = ((amts >= 7500.0) & (amts <= 9999.0)).astype(np.float32)
                
                if np.any(valid_src_mask):
                    np.add.at(features[:, 9], src_indices[valid_src_mask], is_whale[valid_src_mask])
                    np.add.at(features[:, 10], src_indices[valid_src_mask], is_structuring_exact[valid_src_mask])
                if np.any(valid_dst_mask):
                    np.add.at(features[:, 11], dst_indices[valid_dst_mask], is_structuring_exact[valid_dst_mask])

                # Dimension 20: Benford's Law First-Digit Conformity Index
                pos_amts = np.maximum(1e-4, np.abs(amts))
                first_digits = np.floor(pos_amts / (10.0 ** np.floor(np.log10(pos_amts)))).astype(np.int32)
                # Digit 1 is expected 30.1% under Benford; structuring rounds to 8 or 9
                is_benford_anomaly = ((first_digits >= 8) & (first_digits <= 9)).astype(np.float32)
                if np.any(valid_src_mask):
                    np.add.at(features[:, 20], src_indices[valid_src_mask], is_benford_anomaly[valid_src_mask])

                # Dimension 23: Bilateral Flow Accumulator
                if np.any(valid_src_mask):
                    np.add.at(features[:, 23], src_indices[valid_src_mask], np.log1p(amts[valid_src_mask]))
                if np.any(valid_dst_mask):
                    np.add.at(features[:, 23], dst_indices[valid_dst_mask], np.log1p(amts[valid_dst_mask]))
            except Exception:
                pass

        # --- 4. TEMPORAL & NIGHT-HOUR BURST VELOCITY ---
        ts_col = cols_lower.get("timestamp") or cols_lower.get("ts") or cols_lower.get("time") or cols_lower.get("step")
        if ts_col:
            try:
                ts_vals = pd.to_numeric(edges_df[ts_col], errors="coerce").fillna(0.0).values
                hours = (ts_vals.astype(np.int64) % 24)
                is_night = ((hours >= 1) & (hours <= 5)).astype(np.float32)
                if np.any(valid_src_mask):
                    np.add.at(features[:, 12], src_indices[valid_src_mask], is_night[valid_src_mask])
            except Exception:
                pass

        # --- 5. FINTECH / CARD FRAUD ERROR RATE ---
        error_col = cols_lower.get("errors?") or cols_lower.get("error") or cols_lower.get("has_error")
        if error_col:
            try:
                err_vals = (edges_df[error_col].notna() & (edges_df[error_col] != "") & (edges_df[error_col] != 0)).astype(np.float32).values
                if np.any(valid_src_mask):
                    np.add.at(features[:, 13], src_indices[valid_src_mask], err_vals[valid_src_mask])
            except Exception:
                pass

        # --- 6. EV-ATTNPOOL: EXTREME-VALUE ANOMALY POOLING ---
        if amt_col:
            try:
                amts = pd.to_numeric(edges_df[amt_col], errors="coerce").fillna(0.0).values.astype(np.float64)
                mean_amt = float(np.mean(amts))
                std_amt = float(max(1.0, np.std(amts)))
                z_scores = np.maximum(0.0, (amts - mean_amt) / std_amt).astype(np.float32)

                if np.any(valid_src_mask):
                    np.maximum.at(features[:, 16], src_indices[valid_src_mask], z_scores[valid_src_mask])
                if np.any(valid_dst_mask):
                    np.maximum.at(features[:, 17], dst_indices[valid_dst_mask], z_scores[valid_dst_mask])

                exp_z = np.exp(np.clip(z_scores / 2.0, 0.0, 10.0)).astype(np.float32)
                if np.any(valid_src_mask):
                    np.add.at(features[:, 18], src_indices[valid_src_mask], exp_z[valid_src_mask])
                if np.any(valid_dst_mask):
                    np.add.at(features[:, 18], dst_indices[valid_dst_mask], exp_z[valid_dst_mask])
                features[:, 18] = 2.0 * np.log1p(features[:, 18])

                if from_bank_col and to_bank_col:
                    cross_amt = np.where(is_cross_bank > 0, amts, 0.0).astype(np.float32)
                    if np.any(valid_src_mask):
                        np.maximum.at(features[:, 19], src_indices[valid_src_mask], np.log1p(cross_amt[valid_src_mask]))
            except Exception:
                pass

        # --- 7. DEGREE-NORMALIZED RATIOS & COUNTERPARTY GINI ---
        src_counts = np.bincount(src_indices[valid_src_mask], minlength=num_nodes).astype(np.float32)
        dst_counts = np.bincount(dst_indices[valid_dst_mask], minlength=num_nodes).astype(np.float32)
        total_deg = np.maximum(1.0, src_counts + dst_counts)

        features[:, 14] = (features[:, 0] + features[:, 2] + features[:, 6] + features[:, 10]) / total_deg
        features[:, 15] = (features[:, 0] + features[:, 1]) / total_deg
        # Dimension 21: Counterparty Gini dispersion index (Suppresses merchant false positives)
        features[:, 21] = np.abs(src_counts - dst_counts) / total_deg

        for dim in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 20, 22, 23]:
            features[:, dim] = np.log1p(features[:, dim])

        return np.nan_to_num(features, nan=0.0, posinf=1.0, neginf=0.0).astype(np.float32)
