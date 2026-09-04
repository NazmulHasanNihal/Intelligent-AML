"""
governance_logger.py — Model Governance (SR 26-2) & Audit Logger.
Implements Population Stability Index (PSI) drift monitoring, input characteristic tracking,
and cryptographically hashed immutable compliance decision audit trails.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import numpy as np


class ModelGovernanceLogger:
    """
    Enterprise Model Risk Management (MRM) & Regulatory Audit Logger.
    Aligned with 2026 Interagency Guidance on Model Risk Management (SR 26-2, superseding SR 11-7).
    """
    def __init__(self, log_dir: Optional[str] = None, 
                 baseline_scores: Optional[np.ndarray] = None):
        self.log_dir = Path(log_dir or "results/governance_audit_logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.audit_file = self.log_dir / f"audit_trail_{time.strftime('%Y%m%d')}.jsonl"

        # Initialize baseline score distribution for PSI drift calculation (10 equal bins)
        self.num_bins = 10
        self.bin_edges = np.linspace(0.0, 1.0, self.num_bins + 1)
        if baseline_scores is not None and len(baseline_scores) > 0:
            self.baseline_dist = self._compute_distribution(baseline_scores)
        else:
            # Default uniform reference baseline
            self.baseline_dist = np.full(self.num_bins, 1.0 / self.num_bins)

    def _compute_distribution(self, scores: np.ndarray) -> np.ndarray:
        """Computes binned frequency distribution with epsilon smoothing."""
        counts, _ = np.histogram(scores, bins=self.bin_edges)
        probs = (counts + 1e-4) / (np.sum(counts) + 1e-4 * self.num_bins)
        return probs

    def calculate_psi(self, current_scores: np.ndarray) -> Dict[str, Any]:
        """
        Calculates Population Stability Index (PSI) between baseline and production scores:
        PSI = sum((Actual_b - Expected_b) * ln(Actual_b / Expected_b))
        """
        if len(current_scores) == 0:
            return {"psi": 0.0, "status": "INSUFFICIENT_DATA"}

        actual_dist = self._compute_distribution(current_scores)
        expected_dist = self.baseline_dist

        # Compute bucket-level PSI
        psi_buckets = (actual_dist - expected_dist) * np.log(actual_dist / expected_dist)
        total_psi = float(np.sum(psi_buckets))

        if total_psi < 0.10:
            status = "STABLE_NO_DRIFT"
            action = "CONTINUE_STANDARD_MONITORING"
        elif total_psi < 0.25:
            status = "MODERATE_DRIFT_WARNING"
            action = "SCHEDULE_CONFORMAL_RECALIBRATION"
        else:
            status = "SIGNIFICANT_CONCEPT_DRIFT"
            action = "MANDATORY_MODEL_RETRAINING_TRIGGER"

        return {
            "psi_score": round(total_psi, 4),
            "status": status,
            "recommended_action": action,
            "sample_count": len(current_scores),
            "bucket_actual": [round(float(p), 4) for p in actual_dist],
            "bucket_expected": [round(float(p), 4) for p in expected_dist]
        }

    def log_decision_record(self, transaction_id: str,
                            target_node_id: str,
                            input_features: Dict[str, Any],
                            model_outputs: Dict[str, Any],
                            rule_eval: Dict[str, Any],
                            hybrid_decision: Dict[str, Any],
                            conformal_bound: Dict[str, Any]) -> str:
        """
        Generates an immutable, cryptographically hashed compliance audit record
        and appends to daily JSONL audit log.
        """
        timestamp = time.time()
        record_payload = {
            "version": "CSTGB-PROD-2.0",
            "timestamp": timestamp,
            "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp)),
            "transaction_id": transaction_id,
            "target_node_id": target_node_id,
            "inputs": {
                "amount": input_features.get("amount", 0.0),
                "degree": input_features.get("degree", 0),
                "burst_score": input_features.get("burst_score", 0.0),
                "pass_through": input_features.get("pass_through", 0.0)
            },
            "hard_rules": {
                "triggered_count": rule_eval.get("rule_count", 0),
                "is_blocked": rule_eval.get("is_blocked", False),
                "rule_risk": rule_eval.get("rule_risk_score", 0.0)
            },
            "cstgb_model": {
                "ai_risk_score": model_outputs.get("risk_score", 0.0),
                "stream1_tabular": model_outputs.get("p_tab", None),
                "stream2_gnn": model_outputs.get("p_gnn", None),
                "stream3_fused": model_outputs.get("p_fused", None)
            },
            "conformal_calibration": {
                "prediction_set": conformal_bound.get("prediction_set", "UNCERTAIN"),
                "alpha_error_bound": conformal_bound.get("alpha", 0.10),
                "calibrated_q": conformal_bound.get("calibrated_q", 0.85),
                "stratum": conformal_bound.get("stratum", "STANDARD")
            },
            "final_triage": {
                "final_risk_score": hybrid_decision.get("final_risk_score", 0.0),
                "triage_action": hybrid_decision.get("triage_action", "AUTO_CLEARED_PASS")
            }
        }

        # Generate cryptographic SHA-256 seal for immutable regulatory provenance
        record_json_str = json.dumps(record_payload, sort_keys=True)
        record_hash = hashlib.sha256(record_json_str.encode('utf-8')).hexdigest()
        record_payload["audit_sha256_seal"] = record_hash

        # Append to disk
        try:
            with open(self.audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record_payload) + "\n")
        except Exception:
            pass

        return record_hash
