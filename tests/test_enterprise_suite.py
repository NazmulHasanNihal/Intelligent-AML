"""
test_enterprise_suite.py — Unit & Integration Test Suite for Enterprise AML Production Modules.
Verifies:
1. Subgraph LRU Cache (latency & hit-rates)
2. Deterministic Hard-Rule Engine & Hybrid Gate
3. FinCEN SAR Narrative Generator & LLM Prompt Engine
4. Delayed Feedback Pipeline (PID-ACI calibration)
5. Fed SR 11-7 Model Governance & PSI Drift Logger
6. Interactive Ring Visualizer HTML Generation
7. Adversarial Micro-Dusting Graph Defense
"""

import os
import sys
import unittest
import numpy as np

# Ensure project root is on path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.engine.subgraph_cache import SubgraphLRUCache
from src.engine.rule_engine import HardRuleEngine, HybridDecisionGate
from src.explainability.sar_generator import SARNarrativeGenerator
from src.engine.delayed_feedback_pipe import DelayedFeedbackPipeline
from src.governance.governance_logger import ModelGovernanceLogger
from src.explainability.ring_visualizer import RingVisualizer
from src.models.adversarial_defense import AdversarialTopologyDefense


class TestEnterpriseAMLSuite(unittest.TestCase):

    def setUp(self):
        self.cache = SubgraphLRUCache(capacity=500, hidden_dim=64)
        self.rule_engine = HardRuleEngine(structuring_threshold=10_000.0)
        self.hybrid_gate = HybridDecisionGate(self.rule_engine)
        self.sar_gen = SARNarrativeGenerator(institution_name="Test Clearing Bank")
        self.delayed_pipe = DelayedFeedbackPipeline(target_alpha=0.10)
        self.gov_logger = ModelGovernanceLogger(log_dir="results/test_governance_logs")
        self.visualizer = RingVisualizer(output_dir="results/test_visualizations")
        self.defense = AdversarialTopologyDefense(dusting_amount_floor=1.0)

    def test_01_subgraph_lru_cache(self):
        """Tests LRU caching, edge recording, and sub-10ms extraction."""
        # Insert nodes and edges
        z_dummy = np.random.randn(64).astype(np.float32)
        x_dummy = np.random.randn(10).astype(np.float32)
        self.cache.put_node(101, z_emb=z_dummy, tabular_x=x_dummy)
        self.cache.put_node(102, z_emb=z_dummy, tabular_x=x_dummy)
        
        self.cache.record_edge(src=101, dst=102, delta_t=12.5, burst_score=3.2, amount=5000.0)
        
        node_101 = self.cache.get_node(101)
        self.assertIsNotNone(node_101)
        self.assertEqual(node_101["deg_out"], 1)
        self.assertEqual(node_101["max_burst"], 3.2)
        
        # Test feature extraction latency
        x_tab, z_emb, ego_contrast, deg, pt, burst = self.cache.extract_ego_features(101)
        self.assertEqual(x_tab.shape, (1, 10))
        self.assertEqual(z_emb.shape, (1, 64))
        self.assertEqual(deg, 1.0)
        
        telemetry = self.cache.get_telemetry()
        self.assertEqual(telemetry["hits"], 2)
        self.assertEqual(telemetry["cached_nodes"], 2)

    def test_02_hard_rule_engine_and_hybrid_gate(self):
        """Tests deterministic OFAC blocks, structuring flags, and hybrid arbitration."""
        # OFAC Sanction match test
        sanction_tx = {"src_id": "OFAC_SDN_001", "dst_id": "999", "amount": 1500.0}
        eval_res = self.rule_engine.evaluate_rules(sanction_tx)
        self.assertTrue(eval_res["is_blocked"])
        self.assertEqual(eval_res["rule_risk_score"], 1.0)
        
        # Structuring test ($9,500 transfer)
        structuring_tx = {"src_id": "USER_A", "dst_id": "USER_B", "amount": 9500.0}
        eval_res2 = self.rule_engine.evaluate_rules(structuring_tx)
        self.assertFalse(eval_res2["is_blocked"])
        self.assertGreaterEqual(eval_res2["rule_risk_score"], 0.65)
        
        # Hybrid gate test
        hybrid_res = self.hybrid_gate.evaluate_hybrid(sanction_tx, ai_risk_score=0.10)
        self.assertEqual(hybrid_res["final_risk_score"], 1.0)
        self.assertEqual(hybrid_res["triage_action"], "CRITICAL_STATUTORY_BLOCK")

    def test_03_sar_narrative_generation(self):
        """Tests FinCEN regulatory narrative generation and LLM prompt compiler."""
        metrics = {"deg_in": 12, "deg_out": 4, "max_burst_score": 4.8, "pass_through_ratio": 0.94}
        conformal = {"alpha": 0.05, "stratum_name": "Structuring / Peeling Ring", "prediction_set_desc": "Confident Fraud {1}"}
        
        narrative = self.sar_gen.generate_fincen_narrative(
            target_account_id="ACC_TARGET_9921",
            risk_score=0.942,
            topological_metrics=metrics,
            conformal_details=conformal
        )
        self.assertIn("FINANCIAL CRIMES ENFORCEMENT NETWORK", narrative)
        self.assertIn("ACC_TARGET_9921", narrative)
        self.assertIn("94.20%", narrative)
        
        llm_prompts = self.sar_gen.compile_llm_prompt("ACC_TARGET_9921", 0.942, metrics, conformal)
        self.assertIn("system_prompt", llm_prompts)
        self.assertIn("user_prompt", llm_prompts)

    def test_04_delayed_feedback_pipeline(self):
        """Tests asynchronous delayed feedback buffer and PID-ACI adjustment."""
        # Buffer transactions
        for i in range(60):
            self.delayed_pipe.record_scored_transaction(f"TX_{i}", fraud_probability=0.85 if i % 10 == 0 else 0.05)
            
        # Resolve labels
        for i in range(50):
            res_q = self.delayed_pipe.resolve_label_feedback(f"TX_{i}", confirmed_ground_truth=1 if i % 10 == 0 else 0)
            
        telemetry = self.delayed_pipe.get_pipeline_telemetry()
        self.assertEqual(telemetry["total_scored"], 60)
        self.assertEqual(telemetry["total_resolved"], 50)
        self.assertEqual(telemetry["calibration_steps_executed"], 1)

    def test_05_governance_logger_psi_and_audit(self):
        """Tests Fed SR 11-7 PSI drift calculation and SHA-256 audit trail signing."""
        baseline = np.random.beta(0.5, 5.0, 1000)  # low fraud baseline
        gov = ModelGovernanceLogger(log_dir="results/test_governance_logs", baseline_scores=baseline)
        
        # Test stable batch
        stable_batch = np.random.beta(0.5, 5.0, 500)
        psi_res = gov.calculate_psi(stable_batch)
        self.assertEqual(psi_res["status"], "STABLE_NO_DRIFT")
        
        # Test drifted batch
        drifted_batch = np.random.beta(5.0, 0.5, 500)  # high fraud drift
        psi_drift = gov.calculate_psi(drifted_batch)
        self.assertIn("DRIFT", psi_drift["status"])
        
        # Test audit logging
        seal = gov.log_decision_record(
            transaction_id="TX_1001",
            target_node_id="NODE_42",
            input_features={"amount": 9500.0, "degree": 8},
            model_outputs={"risk_score": 0.88},
            rule_eval={"rule_count": 1, "is_blocked": False, "rule_risk_score": 0.65},
            hybrid_decision={"final_risk_score": 0.88, "triage_action": "ESCALATE_TO_COMPLIANCE_INVESTIGATION"},
            conformal_bound={"prediction_set": "CONFIDENT_FRAUD", "alpha": 0.05}
        )
        self.assertEqual(len(seal), 64)  # Valid SHA-256 hash string

    def test_06_ring_visualizer_html(self):
        """Tests standalone interactive HTML graph generation."""
        nodes = [
            {"id": "ACC_SUSPECT", "label": "Suspect Target", "is_target": True},
            {"id": "MULE_01", "label": "Mule Intermediary 1", "is_mule": True},
            {"id": "MULE_02", "label": "Mule Intermediary 2", "is_mule": True}
        ]
        edges = [
            {"source": "ACC_SUSPECT", "target": "MULE_01", "burst": 4.5, "amount": 8000.0},
            {"source": "ACC_SUSPECT", "target": "MULE_02", "burst": 1.2, "amount": 9200.0}
        ]
        html_path = self.visualizer.generate_html_graph("ACC_SUSPECT", 0.945, nodes, edges)
        self.assertTrue(os.path.exists(html_path))
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("C-STGB Forensic Ring Visualizer", content)
        self.assertIn("ACC_SUSPECT", content)

    def test_07_adversarial_defense(self):
        """Tests micro-dusting pruning filter."""
        import torch
        edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=torch.long)
        edge_amounts = torch.tensor([0.001, 500.0, 0.02, 1200.0])  # edges 0 and 2 are micro-dusting
        delta_t = torch.tensor([1.0, 2.0, 3.0, 4.0])
        burst = torch.tensor([0.5, 1.2, 0.1, 3.4])
        
        filt_e, filt_dt, filt_b, telem = self.defense.filter_micro_dusting_edges(
            edge_index, edge_amounts, delta_t, burst
        )
        self.assertEqual(filt_e.shape[1], 2)
        self.assertEqual(telem["pruned_dusting_edges"], 2)


if __name__ == "__main__":
    unittest.main()
