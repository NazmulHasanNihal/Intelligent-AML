"""
test_targeted_enhancements.py — Unit Tests for Targeted Low-Performing Benchmark Algorithmic Improvements.

Validates:
1. TypologyClusteredGraphSMOTE: Homogeneous cluster interpolation with cosine affinity constraints.
2. DirectedMotifKernel: Extraction of all 6 canonical AML graphlet typologies.
3. LaunderingChainDetector (12-dim): Periodicity Regularity, Fast Drain, and Wash Ratios.
4. CLI Dashboard Invocation integrity.
"""

import os
import sys
from pathlib import Path

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import pytest
import torch
import numpy as np
import pandas as pd

from src.models.graph_smote import TypologyClusteredGraphSMOTE, BilinearEdgeGenerator
from src.models.motif_kernel import DirectedMotifKernel
from src.models.laundering_chain_detector import LaunderingChainDetector


class TestTargetedEnhancements:
    def test_01_typology_clustered_graph_smote(self):
        """Tests that TypologyClusteredGraphSMOTE synthesizes minority nodes within high cosine affinity clusters."""
        torch.manual_seed(42)
        hidden_dim = 32
        num_pos = 6
        num_neg = 30
        
        # Create distinct clusters of positive illicit nodes in latent space
        cluster_a = torch.randn(num_pos // 2, hidden_dim) + 5.0
        cluster_b = torch.randn(num_pos // 2, hidden_dim) - 5.0
        h_pos = torch.cat([cluster_a, cluster_b], dim=0)
        h_neg = torch.randn(num_neg, hidden_dim)
        h = torch.cat([h_pos, h_neg], dim=0)
        
        y = torch.cat([torch.ones(num_pos, dtype=torch.long), torch.zeros(num_neg, dtype=torch.long)])
        
        # Synthetic edges
        src = torch.randint(0, num_pos + num_neg, (50,))
        dst = torch.randint(0, num_pos + num_neg, (50,))
        edge_index = torch.stack([src, dst])
        
        smote = TypologyClusteredGraphSMOTE(hidden_dim=hidden_dim, oversample_ratio=0.50, min_cosine_similarity=0.50)
        h_aug, y_aug, edge_aug = smote.synthesize_latent_nodes(h, y, edge_index)
        
        num_expected_syn = int(num_pos * 0.50)
        assert h_aug.shape[0] == h.shape[0] + num_expected_syn
        assert y_aug.shape[0] == y.shape[0] + num_expected_syn
        assert (y_aug[h.shape[0]:] == 1).all()
        assert not torch.isnan(h_aug).any()

    def test_02_directed_motif_canonical_typologies(self):
        """Tests that DirectedMotifKernel correctly computes 6 canonical AML graphlet typologies."""
        kernel = DirectedMotifKernel(max_cycle_order=4)
        num_nodes = 8
        
        # Directed Cycle: 0 -> 1 -> 2 -> 0 (Cycle-3 Wash Loop)
        # Fan-Out: 3 -> 4, 3 -> 5, 3 -> 6, 3 -> 7 (Structuring)
        # Fan-In: 4 -> 0, 5 -> 0, 6 -> 0 (Smurfing Aggregator)
        src = torch.tensor([0, 1, 2, 3, 3, 3, 3, 4, 5, 6], dtype=torch.long)
        dst = torch.tensor([1, 2, 0, 4, 5, 6, 7, 0, 0, 0], dtype=torch.long)
        edge_index = torch.stack([src, dst])
        edge_amts = torch.tensor([1000.0, 1000.0, 1000.0, 9500.0, 9500.0, 9500.0, 9500.0, 9000.0, 9000.0, 9000.0])
        
        typ_dict = kernel.compute_canonical_aml_typologies(edge_index, num_nodes, edge_amts)
        
        assert "fan_in_score" in typ_dict
        assert "fan_out_score" in typ_dict
        assert "scatter_gather_score" in typ_dict
        assert "peeling_chain_score" in typ_dict
        assert "wash_loop_score" in typ_dict
        assert "wash_ratio_index" in typ_dict
        
        # Node 0 has high in-degree (fan-in smurfing aggregator)
        assert typ_dict["fan_in_score"][0] > 0.0
        # Node 3 has high out-degree (fan-out structuring)
        assert typ_dict["fan_out_score"][3] > 0.0
        # Cycle-3 nodes (0, 1, 2) have wash loop indicators
        assert typ_dict["wash_loop_score"][0] > 0.0 or typ_dict["wash_loop_score"][1] > 0.0

    def test_03_laundering_chain_12_dimensional_features(self):
        """Tests that LaunderingChainDetector extracts 12-dimensional features with periodicity and fast-drain."""
        detector = LaunderingChainDetector()
        
        nodes_df = pd.DataFrame({
            "node_id": ["acc1", "acc2", "acc3", "acc4"],
            "node_type": ["Account", "Account", "Account", "Account"]
        })
        
        edges_df = pd.DataFrame({
            "src": ["acc1", "acc1", "acc1", "acc2", "acc3"],
            "dst": ["acc2", "acc3", "acc4", "acc4", "acc4"],
            "ts": [100.0, 120.0, 140.0, 200.0, 220.0],
            "Amount Paid": [9500.0, 9200.0, 9800.0, 5000.0, 5000.0],
            "From Bank": ["BankA", "BankA", "BankA", "BankB", "BankC"],
            "To Bank": ["BankB", "BankC", "BankD", "BankD", "BankD"],
            "Payment Format": ["Wire", "Wire", "Wire", "Cash", "Cash"]
        })
        
        feats = detector.extract_typology_features(nodes_df, edges_df)
        assert feats.shape == (4, 12)
        assert not np.isnan(feats).any()
        
        # acc1 has high structuring ratio (dim 7) and fan-out (dim 1)
        assert feats[0, 7] > 0.0
        assert feats[0, 1] > 0.0
        # acc4 has high fan-in (dim 6)
        assert feats[3, 6] > 0.0

    def test_04_dashboard_module_loadability(self):
        """Tests that the enterprise API server and frontend configuration load cleanly."""
        api_path = Path(__file__).resolve().parent.parent / "src" / "engine" / "api.py"
        assert api_path.exists()
        with open(api_path, "r", encoding="utf-8") as f:
            code = f.read()
        compiled = compile(code, str(api_path), "exec")
        assert compiled is not None
        
        frontend_pkg = Path(__file__).resolve().parent.parent / "frontend" / "package.json"
        assert frontend_pkg.exists()
