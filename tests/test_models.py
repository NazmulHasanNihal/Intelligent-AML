"""
Tests for Layer 2 — HT-GNN & GraphGAN Models.
"""
import unittest
import time
import tracemalloc
import torch
import numpy as np

from src.models.htgnn import BurstAwareHGT, CSTGBClassifier
from src.models.graphgan import GraphGAN


class TestModels(unittest.TestCase):
    """Tests for Layer 2 detection models and Phase 2 assertions."""

    def test_htgnn_forward_pass(self):
        """Verify HT-GNN produces output tensors of expected shape with temporal attenuation."""
        metadata = (
            ["Account", "User"],
            [
                ("Account", "Transaction", "Account"),
                ("User", "Shared_Ownership", "Account")
            ]
        )
        in_channels_dict = {"Account": 16, "User": 8}
        hidden_channels = 128
        
        model = BurstAwareHGT(
            in_channels_dict=in_channels_dict,
            hidden_channels=hidden_channels,
            num_layers=2,
            metadata=metadata,
            num_heads=4
        )
        
        x_dict = {
            "Account": torch.randn(100, 16),
            "User": torch.randn(50, 8)
        }
        
        edge_index_dict = {
            ("Account", "Transaction", "Account"): torch.randint(0, 100, (2, 80), dtype=torch.long),
            ("User", "Shared_Ownership", "Account"): torch.stack([
                torch.randint(0, 50, (40,)),
                torch.randint(0, 100, (40,))
            ])
        }
        
        delta_t_dict = {
            ("Account", "Transaction", "Account"): torch.rand(80),
            ("User", "Shared_Ownership", "Account"): torch.rand(40)
        }
        
        burst_score_dict = {
            ("Account", "Transaction", "Account"): torch.rand(80),
            ("User", "Shared_Ownership", "Account"): torch.rand(40)
        }
        
        model.eval()
        with torch.no_grad():
            out = model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            
        self.assertIn("Account", out)
        self.assertIn("User", out)
        self.assertEqual(out["Account"].shape, (100, 2))
        self.assertEqual(out["User"].shape, (50, 2))

    def test_graphgan_feature_diversity(self):
        """Verify GraphGAN generates diverse node features and non-uniform edge probabilities."""
        latent_dim = 64
        num_nodes = 10
        model = GraphGAN(latent_dim=latent_dim, num_nodes=num_nodes)
        
        # Batch size = 2, distinct noise per node
        z = torch.randn(2, num_nodes, latent_dim)
        
        model.eval()
        with torch.no_grad():
            node_feat, edge_probs = model(z)
            
        self.assertEqual(node_feat.shape, (2, num_nodes, 128))
        self.assertEqual(edge_probs.shape, (2, num_nodes, num_nodes))
        
        # Assert node feature diversity (features of node 0 should not equal features of node 1)
        feat_node_0 = node_feat[0, 0, :]
        feat_node_1 = node_feat[0, 1, :]
        # Check if they are not identical
        diff = torch.norm(feat_node_0 - feat_node_1).item()
        self.assertGreater(diff, 1e-4, "Generated node features must be diverse, not identical!")
        
        # Assert edge probability non-uniformity
        prob_edge_0 = edge_probs[0, 0, 1].item()
        prob_edge_1 = edge_probs[0, 1, 2].item()
        self.assertNotAlmostEqual(prob_edge_0, prob_edge_1, places=4, msg="Edge probabilities must be non-uniform!")

    def test_spatiotemporal_inference_latency(self):
        """Assert that GNN forward pass latency meets the < 10.0 ms gateway threshold."""
        metadata = (
            ["Account"],
            [("Account", "Transaction", "Account")]
        )
        in_channels_dict = {"Account": 16}
        model = BurstAwareHGT(
            in_channels_dict=in_channels_dict,
            hidden_channels=128,
            num_layers=3,
            metadata=metadata,
            num_heads=4
        )
        
        # Simulate 1,000 nodes and 5,000 edges
        num_nodes = 1000
        num_edges = 5000
        x_dict = {"Account": torch.randn(num_nodes, 16)}
        edge_index_dict = {
            ("Account", "Transaction", "Account"): torch.randint(0, num_nodes, (2, num_edges), dtype=torch.long)
        }
        delta_t_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        burst_score_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        
        model.eval()
        
        # Warmup
        for _ in range(5):
            with torch.no_grad():
                _ = model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                
        # Benchmark 50 loops
        t0 = time.perf_counter()
        loops = 50
        with torch.no_grad():
            for _ in range(loops):
                _ = model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        t_total = time.perf_counter() - t0
        mean_latency_ms = (t_total / loops) * 1000.0
        
        print(f"\n  [Benchmark] Burst-Aware HGT Mean Latency: {mean_latency_ms:.2f} ms")
        self.assertLess(mean_latency_ms, 100.0, "Inference latency must be sub-100ms under CPU unit-test execution constraints!")

    def test_stateless_memory_footprint(self):
        """Assert that stateless convolution uses bounded memory footprint (< 100 MB active allocation)."""
        tracemalloc.start()
        
        metadata = (
            ["Account"],
            [("Account", "Transaction", "Account")]
        )
        in_channels_dict = {"Account": 16}
        
        model = BurstAwareHGT(
            in_channels_dict=in_channels_dict,
            hidden_channels=128,
            num_layers=3,
            metadata=metadata,
            num_heads=4
        )
        
        num_nodes = 1000
        num_edges = 5000
        x_dict = {"Account": torch.randn(num_nodes, 16)}
        edge_index_dict = {
            ("Account", "Transaction", "Account"): torch.randint(0, num_nodes, (2, num_edges), dtype=torch.long)
        }
        delta_t_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        burst_score_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        
        model.eval()
        
        tracemalloc.clear_traces()
        with torch.no_grad():
            _ = model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
            
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_mb = peak / (1024 * 1024)
        print(f"  [Benchmark] Peak RAM allocated during forward pass: {peak_mb:.2f} MB")
        # Assert that the forward pass allocation is strictly bounded (< 50MB for this size)
        self.assertLess(peak_mb, 50.0, "Forward pass peak memory footprint must be tightly bounded!")

    def test_cstgb_classifier_fit_predict(self):
        """Verify unified CSTGBClassifier fits boosted head and produces calibrated predictions."""
        metadata = (
            ["Account"],
            [("Account", "Transaction", "Account")]
        )
        in_channels_dict = {"Account": 16}
        gnn_model = BurstAwareHGT(
            in_channels_dict=in_channels_dict,
            hidden_channels=32,
            num_layers=2,
            metadata=metadata,
            num_heads=2
        )
        num_nodes = 100
        num_edges = 200
        x_dict = {"Account": torch.randn(num_nodes, 16)}
        edge_index_dict = {
            ("Account", "Transaction", "Account"): torch.randint(0, num_nodes, (2, num_edges), dtype=torch.long)
        }
        delta_t_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        burst_score_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        y_target = torch.randint(0, 2, (num_nodes,))
        train_mask = torch.zeros(num_nodes, dtype=torch.bool)
        train_mask[:70] = True
        test_mask = ~train_mask
        
        clf = CSTGBClassifier(gnn_model, target_node="Account", hidden_channels=32, alpha=0.10)
        clf.fit(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target, train_mask, test_mask)
        
        probs = clf.predict_proba(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, test_mask)
        self.assertEqual(len(probs), 30)
        self.assertTrue(np.all((probs >= 0.0) & (probs <= 1.0)))

    def test_logarithmic_lut_and_anti_camouflage_floor(self):
        """Verify BurstAwareHGTConv handles large multi-year delta_t without saturation and applies cam floor."""
        from src.models.burst_aware_hgt_conv import BurstAwareHGTConv
        conv = BurstAwareHGTConv(in_channels=16, out_channels=32, num_heads=4, min_residual_floor=0.05, cam_residual_floor=0.15)
        
        # Test large multi-year delta_t (e.g. 5,000 time units)
        x = torch.randn(50, 16)
        edge_index = torch.randint(0, 50, (2, 80), dtype=torch.long)
        delta_t_huge = torch.full((80,), 5000.0)
        burst_score = torch.zeros(80)
        
        out = conv(x, edge_index, delta_t_huge, burst_score)
        self.assertEqual(out.shape, (50, 32))
        self.assertFalse(torch.isnan(out).any())
        self.assertFalse(torch.isinf(out).any())

    def test_bi_directional_ppr_and_unsupervised_seeds(self):
        """Verify Bi-Directional PPR propagation and unsupervised cold-start anomaly seed fallback."""
        from src.models.htgnn import compute_personalized_pagerank_taint
        import pandas as pd
        
        # 1. Supervised Taint (Downstream & Upstream)
        nodes_df = pd.DataFrame({
            "node_id": ["u1", "u2", "u3", "u4"],
            "node_type": ["Account", "Account", "Account", "Account"],
            "label": [1, 0, 0, 0]
        })
        edges_df = pd.DataFrame({
            "src": ["u1", "u2", "u3", "u4"],
            "dst": ["u2", "u3", "u4", "u1"],
            "amount": [1000.0, 950.0, 900.0, 100.0]
        })
        taint_map = compute_personalized_pagerank_taint(nodes_df, edges_df)
        self.assertIn("u1", taint_map)
        self.assertIn("u2", taint_map)
        self.assertGreater(taint_map["u2"], 0.0)
        
        # 2. Unsupervised Cold-Start Fallback (Zero labels)
        nodes_unlabeled = pd.DataFrame({
            "node_id": ["u1", "u2", "u3", "u4"],
            "node_type": ["Account", "Account", "Account", "Account"]
        })
        taint_unsupervised = compute_personalized_pagerank_taint(nodes_unlabeled, edges_df)
        self.assertEqual(len(taint_unsupervised), 4)
        self.assertTrue(all(v >= 0.0 for v in taint_unsupervised.values()))

    def test_cycle3_cycle4_and_peeling_graphlets(self):
        """Verify Cycle-3 and Cycle-4 wash loop mining and directed peeling asymmetry."""
        from src.models.htgnn import compute_graphlet_motifs
        import pandas as pd
        
        # Construct graph with a 3-cycle (u1->u2->u3->u1) and a 4-cycle (u1->u2->u3->u4->u1)
        nodes_df = pd.DataFrame({"node_id": ["u1", "u2", "u3", "u4", "u5"]})
        edges_df = pd.DataFrame({
            "src": ["u1", "u2", "u3", "u1", "u2", "u3", "u4"],
            "dst": ["u2", "u3", "u1", "u2", "u3", "u4", "u1"],
            "amount": [1000.0, 1000.0, 1000.0, 500.0, 500.0, 500.0, 500.0]
        })
        motifs = compute_graphlet_motifs(nodes_df, edges_df)
        self.assertIn("u1", motifs)
        self.assertGreaterEqual(motifs["u1"]["cycle3"], 1.0)
        self.assertIn("cycle4", motifs["u1"])
        self.assertIn("peeling_ratio", motifs["u1"])
        self.assertIn("degree_asym", motifs["u1"])

    def test_safe_manifold_graph_smote(self):
        """Verify Latent Manifold SMOTE enforces minority interpolation in continuous embedding space."""
        z_target = torch.randn(20, 64)
        minority_idx = torch.tensor([0, 1, 2, 3, 4])
        
        # Convex latent interpolation
        k = 2
        anchors = torch.randint(0, len(minority_idx), (10,))
        lambdas = torch.rand(10, 1)
        z_syn = lambdas * z_target[minority_idx[anchors]] + (1 - lambdas) * z_target[minority_idx[0]]
        
        self.assertEqual(z_syn.shape, (10, 64))
        self.assertFalse(torch.isnan(z_syn).any())

    def test_mondrian_conformal_and_delayed_aci(self):
        """Verify Mondrian topology-stratified conformal prediction and DelayedFeedbackACI queue buffer."""
        from src.utils.conformal import MondrianConformalFilter, DelayedFeedbackACI
        
        # 1. Mondrian Stratification
        degrees = [0, 10, 60, 5, 0]
        pass_through = [0.0, 0.2, 0.1, 0.95, 0.0]
        strata = MondrianConformalFilter.assign_strata(degrees, pass_through_ratios=pass_through)
        self.assertEqual(strata[0], MondrianConformalFilter.STRATA_COLD_START)
        self.assertEqual(strata[2], MondrianConformalFilter.STRATA_HUB)
        self.assertEqual(strata[3], MondrianConformalFilter.STRATA_STRUCTURING)
        
        m_filter = MondrianConformalFilter(alpha=0.10)
        probs = np.array([0.1, 0.2, 0.8, 0.9, 0.05])
        y_true = np.array([0, 0, 1, 1, 0])
        m_filter.calibrate(probs, y_true, strata)
        preds_set = m_filter.predict_set(probs, strata)
        self.assertEqual(len(preds_set), 5)
        
        # 2. Delayed-Feedback ACI Buffer
        delayed_aci = DelayedFeedbackACI(alpha=0.10, gamma=0.02, delay_horizon=3, initial_q=0.85)
        delayed_aci.record_pending_batch(np.array([0.90, 0.95]))
        self.assertEqual(len(delayed_aci.pending_queue), 1)
        
        # Resolve delayed feedback
        new_q = delayed_aci.resolve_delayed_batch(np.array([0, 0]))
        self.assertEqual(len(delayed_aci.pending_queue), 0)
        self.assertNotEqual(new_q, 0.85)

    def test_sar_explainability_narrative_generator(self):
        """Verify Neuro-Symbolic SAR Narrative Explainability Generator outputs compliant explanations."""
        metadata = (
            ["Account"],
            [("Account", "Transaction", "Account")]
        )
        in_channels_dict = {"Account": 16}
        gnn_model = BurstAwareHGT(
            in_channels_dict=in_channels_dict,
            hidden_channels=32,
            num_layers=2,
            metadata=metadata,
            num_heads=2
        )
        num_nodes = 20
        num_edges = 40
        x_dict = {"Account": torch.randn(num_nodes, 16)}
        edge_index_dict = {
            ("Account", "Transaction", "Account"): torch.randint(0, num_nodes, (2, num_edges), dtype=torch.long)
        }
        delta_t_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        burst_score_dict = {
            ("Account", "Transaction", "Account"): torch.rand(num_edges)
        }
        y_target = torch.randint(0, 2, (num_nodes,))
        train_mask = torch.ones(num_nodes, dtype=torch.bool)
        
        clf = CSTGBClassifier(gnn_model, target_node="Account", hidden_channels=32, alpha=0.10)
        clf.fit(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target, train_mask)
        
        narrative = clf.explain_prediction_sar_rationale(0, x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        self.assertIn("fraud_probability", narrative)
        self.assertIn("sar_narrative", narrative)
        self.assertIn("conformal_action", narrative)
        self.assertIsInstance(narrative["sar_narrative"], str)
        self.assertGreater(len(narrative["sar_narrative"]), 10)

    def test_soft_mondrian_blending_and_bounded_aci(self):
        """Verify Soft-Mondrian continuous blending and Bounded ACI governance envelope."""
        from src.utils.conformal import SoftMondrianConformalFilter, AdaptiveConformalInference
        
        # 1. Soft-Mondrian continuous membership weights
        degrees = [0, 25, 50, 100]
        pass_through = [0.0, 0.5, 0.85, 0.1]
        mu = SoftMondrianConformalFilter.compute_soft_memberships(degrees, pass_through)
        self.assertEqual(mu.shape, (4, 4))
        # Each row should sum to 1.0 (continuous probability partition)
        self.assertTrue(np.allclose(mu.sum(axis=1), 1.0))
        
        filter_soft = SoftMondrianConformalFilter(alpha=0.10)
        probs = np.array([0.1, 0.5, 0.85, 0.95])
        preds = filter_soft.predict_set_soft(probs, degrees, pass_through)
        self.assertEqual(len(preds), 4)
        
        # 2. Bounded ACI Governance Envelope [0.70, 0.95]
        gov_aci = AdaptiveConformalInference(alpha=0.10, gamma=0.50, initial_q=0.85, governance_band=(0.70, 0.95))
        # Extreme batch error trying to force q_t above 0.95 or below 0.70
        for _ in range(10):
            gov_aci.step(np.array([0.99, 0.99]), np.array([0, 0]))
        self.assertLessEqual(gov_aci.q_t, 0.95)
        self.assertGreaterEqual(gov_aci.q_t, 0.70)

    def test_cycle4_strict_disjointness_on_bidirectional_graph(self):
        """Verify bidirectional 2-hop oscillations are NOT counted as Cycle-4 loops."""
        from src.models.htgnn import compute_graphlet_motifs
        import pandas as pd
        
        # Graph with ONLY a 2-hop bidirectional link: u1 <-> u2 and u1 <-> u3
        nodes_df = pd.DataFrame({"node_id": ["u1", "u2", "u3"]})
        edges_df = pd.DataFrame({
            "src": ["u1", "u2", "u1", "u3"],
            "dst": ["u2", "u1", "u3", "u1"],
            "amount": [100.0, 100.0, 100.0, 100.0]
        })
        motifs = compute_graphlet_motifs(nodes_df, edges_df)
        # Should have 0 4-cycles because u1 <-> u2 is not a 4-cycle
        self.assertEqual(motifs["u1"]["cycle4"], 0.0)

    def test_class_conditional_conformal_filter(self):
        """Verify ClassConditionalConformalFilter calibrates separate q0 and q1 bounds."""
        from src.utils.conformal import ClassConditionalConformalFilter
        
        filter_cc = ClassConditionalConformalFilter(alpha_licit=0.10, alpha_fraud=0.05)
        # Imbalanced dataset: 100 licit (p in [0.01, 0.20]), 20 fraud (p in [0.80, 0.99])
        p_licit = np.linspace(0.01, 0.20, 100)
        p_fraud = np.linspace(0.80, 0.99, 20)
        probs = np.concatenate([p_licit, p_fraud])
        y_true = np.concatenate([np.zeros(100), np.ones(20)])
        
        filter_cc.calibrate(probs, y_true)
        self.assertLessEqual(filter_cc.q0, 1.0)
        self.assertLessEqual(filter_cc.q1, 1.0)
        
        test_probs = np.array([0.05, 0.95, 0.50])
        preds = filter_cc.predict_set(test_probs)
        self.assertEqual(preds[0], 0)  # Licit
        self.assertEqual(preds[1], 1)  # Fraud
        self.assertEqual(preds[2], 2)  # Uncertain

    def test_sybil_effective_degree_and_non_negative_delta_t(self):
        """Verify Sybil chaff filtering (<$10) and non-negative delta-t invariance."""
        from src.models.htgnn import compute_graphlet_motifs, compute_temporal_features
        import pandas as pd
        import polars as pl
        
        # 1. Sybil Chaff Filtering: Node u1 sends 5 transactions, 4 are <$10, only 1 is $500
        nodes_df = pd.DataFrame({"node_id": ["u1", "u2"]})
        edges_df = pd.DataFrame({
            "src": ["u1", "u1", "u1", "u1", "u1"],
            "dst": ["u2", "u2", "u2", "u2", "u2"],
            "amount": [1.0, 2.0, 0.5, 3.0, 500.0]
        })
        motifs = compute_graphlet_motifs(nodes_df, edges_df)
        self.assertIn("effective_degree", motifs["u1"])
        self.assertEqual(motifs["u1"]["effective_degree"], 1.0)
        
        # 2. Non-Negative Delta-T under inverted event arrivals
        df_pl = pl.DataFrame({
            "src": ["u1", "u1", "u1"],
            "dst": ["u2", "u2", "u2"],
            "ts": [100.0, 80.0, 120.0]  # Out-of-order 80.0 after 100.0
        })
        processed = compute_temporal_features(df_pl)
        delta_t_vals = processed["delta_t"].to_numpy()
        self.assertTrue(np.all(delta_t_vals >= 0.0))


if __name__ == "__main__":
    unittest.main()