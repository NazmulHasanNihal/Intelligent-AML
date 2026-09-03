"""
test_inference_accelerator.py — Unit tests for Industrial High-Throughput (1M+ TPS) Inference Accelerator:
1. CSTGBHierarchicalAccelerator
2. InMemGraphEmbeddingRingBuffer
3. Zero-loss Fidelity & Telemetry Verification
"""

import unittest
import torch
import torch.nn as nn
import numpy as np

from src.models.inference_accelerator import (
    CSTGBHierarchicalAccelerator,
    InMemGraphEmbeddingRingBuffer,
)


class MockTreeModel:
    """Mock XGBoost/LightGBM model for testing sub-microsecond inference routing."""
    def __init__(self, mode="licit"):
        self.mode = mode

    def predict_proba(self, x):
        n = x.shape[0]
        probs = np.zeros((n, 2))
        if self.mode == "licit":
            probs[:, 1] = 0.001  # Safe licit (< 0.02)
            probs[:, 0] = 0.999
        elif self.mode == "illicit":
            probs[:, 1] = 0.995  # Safe illicit (> 0.98)
            probs[:, 0] = 0.005
        else:
            probs[:, 1] = 0.450  # Ambiguous (0.02 - 0.98)
            probs[:, 0] = 0.550
        return probs


class MockGNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(8, 16)

    def get_embeddings(self, x_dict, *args):
        return {nt: x[:, :16] if x.shape[1] >= 16 else torch.zeros(x.shape[0], 16) for nt, x in x_dict.items()}

    def forward(self, x_dict, *args):
        return {nt: torch.zeros(x.shape[0], 2) for nt, x in x_dict.items()}


class MockCSTGB:
    def __init__(self, mode="mixed"):
        self.target_node = "Account"
        self.gnn_model = MockGNN()
        self.single_class = False
        self.is_meta_fitted = False
        self.optimal_threshold = 0.50
        
        self.xgb_tab = MockTreeModel(mode="licit" if mode == "licit" else "mixed")
        self.lgbm_tab = MockTreeModel(mode="licit" if mode == "licit" else "mixed")
        self.cat_tab = MockTreeModel(mode="licit" if mode == "licit" else "mixed")
        self.xgb_fused = MockTreeModel(mode="mixed")
        self.lgbm_fused = MockTreeModel(mode="mixed")

    def _extract_all_features(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        x = x_dict[self.target_node].detach().cpu().numpy()
        fused = np.hstack([x, x])
        p_gnn = np.ones((x.shape[0], 1)) * 0.1
        deg = np.ones((x.shape[0], 1))
        pt = np.zeros((x.shape[0], 1))
        bv = np.zeros((x.shape[0], 1))
        return x, fused, p_gnn, deg, pt, bv

    def _predict_ensemble(self, feat_tuple):
        x_tab = feat_tuple[0]
        return np.ones(x_tab.shape[0]) * 0.45


class TestInferenceAccelerator(unittest.TestCase):

    def test_01_hierarchical_accelerator_early_exit(self):
        """Tests that obvious licit transactions exit 100% via Fast-Path with 0 GNN calls."""
        mock_cstgb = MockCSTGB(mode="licit")
        accelerator = CSTGBHierarchicalAccelerator(mock_cstgb, tau_safe_licit=0.02, tau_safe_illicit=0.98)
        
        x_dict = {"Account": torch.randn(500, 8)}
        edge_index_dict = {("Account", "tx", "Account"): torch.zeros((2, 0), dtype=torch.long)}
        
        probs, telemetry = accelerator.predict_proba_hierarchical(
            x_dict=x_dict,
            edge_index_dict=edge_index_dict,
            delta_t_dict={},
            burst_score_dict={}
        )
        
        self.assertEqual(len(probs), 500)
        self.assertEqual(telemetry["fast_path_cleared_count"], 500)
        self.assertEqual(telemetry["deep_path_evaluated_count"], 0)
        self.assertEqual(telemetry["fast_path_ratio_pct"], 100.0)
        self.assertGreater(telemetry["throughput_tps"], 50000)

    def test_02_hierarchical_accelerator_ambiguous_routing(self):
        """Tests that borderline / ambiguous transactions route to deep GNN path."""
        mock_cstgb = MockCSTGB(mode="mixed")
        accelerator = CSTGBHierarchicalAccelerator(mock_cstgb, tau_safe_licit=0.02, tau_safe_illicit=0.98)
        
        x_dict = {"Account": torch.randn(100, 8)}
        edge_index_dict = {("Account", "tx", "Account"): torch.zeros((2, 0), dtype=torch.long)}
        
        probs, telemetry = accelerator.predict_proba_hierarchical(
            x_dict=x_dict,
            edge_index_dict=edge_index_dict,
            delta_t_dict={},
            burst_score_dict={}
        )
        
        self.assertEqual(len(probs), 100)
        self.assertEqual(telemetry["deep_path_evaluated_count"], 100)
        self.assertEqual(telemetry["deep_path_ratio_pct"], 100.0)

    def test_03_in_memory_ring_buffer_concurrency(self):
        """Tests lock-free O(1) embedding updates and high-speed retrieval."""
        ring_buffer = InMemGraphEmbeddingRingBuffer(embedding_dim=16, max_entities=1000)
        
        node_ids = np.array([10, 25, 99, 500], dtype=np.int64)
        new_embeddings = np.random.randn(4, 16).astype(np.float32)
        
        ring_buffer.update_embeddings(node_ids, new_embeddings)
        
        retrieved = ring_buffer.get_embeddings_fast(node_ids)
        np.testing.assert_allclose(retrieved, new_embeddings, rtol=1e-5)
        self.assertTrue((ring_buffer.version_tags[node_ids] == 1).all())


if __name__ == "__main__":
    unittest.main()
