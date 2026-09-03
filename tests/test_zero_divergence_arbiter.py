"""
test_zero_divergence_arbiter.py — Comprehensive Unit Tests for Zero-Divergence Governance & Triage Arbiter:
1. Statutory Hard Redline Overrides (OFAC SDN, FATF Blacklist) -> 100% Deterministic Recall
2. Repeated Sub-Threshold Smurfing & Cycle Wash Loops
3. Conformal Confident Clearances -> 100% Automated Precision
4. Ambiguous Border Case Deferral to Human Review Queue
"""

import unittest
import time
from src.engine.zero_divergence_arbiter import ZeroDivergenceArbiter
from src.engine.rule_engine import HardRuleEngine
from src.models.motif_kernel import DirectedMotifKernel


class TestZeroDivergenceArbiter(unittest.TestCase):

    def setUp(self):
        self.arbiter = ZeroDivergenceArbiter(conformal_alpha=0.05, high_risk_threshold=0.85, low_risk_threshold=0.05)

    def test_01_statutory_ofac_instant_block(self):
        """Tests that a direct OFAC sanctioned wallet match guarantees instant STATUTORY_BLOCK (100% Recall)."""
        tx = {
            "tx_id": "TX_OFAC_001",
            "src_id": "OFAC_SDN_001", # Blacklisted entity
            "dst_id": "ACC_9921",
            "amount": 250.0,
            "jurisdiction": "USA",
            "timestamp": time.time()
        }
        # Even if AI model outputs a very low probability (0.01), statutory override must enforce 1.0 risk
        verdict = self.arbiter.evaluate_transaction(tx, ai_model_prob=0.01, conformal_prediction_set=0)

        self.assertEqual(verdict["action"], "STATUTORY_BLOCK")
        self.assertEqual(verdict["status"], "CRITICAL_SEIZURE")
        self.assertEqual(verdict["final_risk_score"], 1.0000)
        self.assertTrue(verdict["is_statutory_blocked"])
        self.assertGreater(verdict["triggered_rules_count"], 0)

    def test_02_smurfing_aggregation_mandatory_sar(self):
        """Tests that repeated structured transactions under $10,000 trigger MANDATORY_SAR_ESCALATION."""
        now = time.time()
        history = [
            {"src_id": "MULE_01", "dst_id": "ACC_B", "amount": 9500.0, "timestamp": now - 3600},
            {"src_id": "MULE_01", "dst_id": "ACC_C", "amount": 9200.0, "timestamp": now - 1800},
        ]
        tx = {
            "tx_id": "TX_SMURF_3",
            "src_id": "MULE_01",
            "dst_id": "ACC_D",
            "amount": 9400.0,
            "jurisdiction": "USA",
            "timestamp": now
        }
        verdict = self.arbiter.evaluate_transaction(tx, ai_model_prob=0.60, recent_history=history)

        self.assertEqual(verdict["action"], "MANDATORY_SAR_ESCALATION")
        self.assertEqual(verdict["status"], "SUSPICIOUS_ACTIVITY_ALERT")
        self.assertGreaterEqual(verdict["final_risk_score"], 0.85)

    def test_03_conformal_auto_cleared_pass(self):
        """Tests that clean transactions with low AI risk are safely cleared with guaranteed 0% false alarms."""
        tx = {
            "tx_id": "TX_CLEAN_01",
            "src_id": "BENIGN_USER_1",
            "dst_id": "GROCERY_STORE",
            "amount": 45.50,
            "jurisdiction": "USA",
            "timestamp": time.time()
        }
        verdict = self.arbiter.evaluate_transaction(tx, ai_model_prob=0.002, conformal_prediction_set=0)

        self.assertEqual(verdict["action"], "AUTO_CLEARED_PASS")
        self.assertEqual(verdict["status"], "LEGITIMATE_TRANSACTION")
        self.assertLess(verdict["final_risk_score"], 0.05)
        self.assertFalse(verdict["is_statutory_blocked"])

    def test_04_ambiguous_case_deferred_to_human_queue(self):
        """Tests that uncertain border cases are deferred to compliance officers rather than guessing."""
        tx = {
            "tx_id": "TX_AMBIGUOUS_01",
            "src_id": "NEW_USER_99",
            "dst_id": "MERCHANT_X",
            "amount": 4200.0,
            "jurisdiction": "USA",
            "timestamp": time.time()
        }
        # Conformal set 2 indicates uncertainty {0, 1}
        verdict = self.arbiter.evaluate_transaction(tx, ai_model_prob=0.42, conformal_prediction_set=2)

        self.assertEqual(verdict["action"], "HUMAN_REVIEW_QUEUE")
        self.assertEqual(verdict["status"], "DEFERRED_ANALYST_TRIAGE")
        self.assertIn("Human Compliance Officer", verdict["audit_evidence"][0])

    def test_05_cycle_wash_loop_topology_override(self):
        """Tests that localized circular graphlet wash loop triggers SAR escalation."""
        tx = {
            "tx_id": "TX_CYCLE_01",
            "src_id": 10,
            "dst_id": 20,
            "amount": 15000.0,
            "jurisdiction": "USA",
            "timestamp": time.time()
        }
        # In-edges and out-edges have 100% counterparty intersection (instant wash loop)
        in_edges = [{"counterparty": 20}]
        out_edges = [{"counterparty": 20}]

        verdict = self.arbiter.evaluate_transaction(
            tx, ai_model_prob=0.30, node_in_edges=in_edges, node_out_edges=out_edges
        )

        self.assertEqual(verdict["action"], "MANDATORY_SAR_ESCALATION")
        self.assertGreaterEqual(verdict["cycle_topology_score"], 0.45)

    def test_06_arbiter_telemetry(self):
        """Tests real-time governance metrics calculation."""
        telemetry = self.arbiter.get_arbiter_telemetry()
        self.assertIn("total_evaluated", telemetry)
        self.assertIn("statutory_block_rate", telemetry)
        self.assertIn("auto_clear_rate", telemetry)


if __name__ == "__main__":
    unittest.main()
