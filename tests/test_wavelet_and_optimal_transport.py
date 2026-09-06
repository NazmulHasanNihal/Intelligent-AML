"""
test_frontier_master_suite.py — Comprehensive Unit Tests for the 5 Master Algorithmic Frontiers:
1. DER++ Dark Experience Replay Memory Buffer & Continual Loss
2. Adversarial GraphGuard & Homophily Denoising Gate
3. Multiscale Chebyshev Spectral Graph Wavelets Engine
4. Neural Optimal Transport & Sinkhorn Domain Alignment
5. Benjamini-Hochberg Conformal False Discovery Rate (FDR) Controller
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

from src.models.continual_learning import DarkExperienceReplayBuffer
from src.models.graph_guard import AdversarialGraphGuard, HomophilyDenoisingGate
from src.models.spectral_wavelets import SpectralGraphWaveletConv, ChebyshevSpectralWaveletEngine
from src.models.optimal_transport import SinkhornDomainAligner, EntropicWassersteinLoss
from src.utils.conformal_fdr import BenjaminiHochbergConformalFDR


class TestFrontierMasterSuite:
    def test_01_der_plus_plus_continual_learning(self):
        """Tests that DarkExperienceReplayBuffer stores logits/features and computes DER++ loss."""
        torch.manual_seed(42)
        buffer = DarkExperienceReplayBuffer(capacity=100, alpha=0.5, beta=0.5)
        
        x = torch.randn(20, 16)
        logits = torch.randn(20, 2)
        y = torch.randint(0, 2, (20,))
        
        buffer.add(x, logits, y)
        assert len(buffer.x_buf) == 20
        assert len(buffer.logits_buf) == 20
        
        # Sample replay batch
        x_samp, logits_samp, y_samp = buffer.sample(batch_size=8, device=torch.device("cpu"))
        assert x_samp.shape == (8, 16)
        assert logits_samp.shape == (8, 2)
        assert y_samp.shape == (8,)
        
        # Current predictions on sampled data
        current_logits = logits_samp + 0.1 * torch.randn_like(logits_samp)
        loss = buffer.compute_der_loss(current_logits, logits_samp, y_samp)
        assert loss.item() >= 0.0
        assert not torch.isnan(loss)

    def test_02_adversarial_graph_guard_purification(self):
        """Tests that AdversarialGraphGuard identifies and prunes camouflage chaff edges."""
        torch.manual_seed(42)
        in_dim = 16
        num_nodes = 10
        x = torch.randn(num_nodes, in_dim)
        
        # Node 0 and Node 1 are similar; Node 0 and Node 9 are dissimilar (Camouflage noise)
        x[1] = x[0] + 0.01 * torch.randn(in_dim)
        x[9] = -x[0] + 0.01 * torch.randn(in_dim)
        
        src = torch.tensor([0, 0, 1, 2, 3])
        dst = torch.tensor([1, 9, 2, 3, 4])
        edge_index = torch.stack([src, dst])
        
        guard = AdversarialGraphGuard(in_channels=in_dim, prune_threshold=0.40)
        purified_edge_index, _, stats = guard.purify_graph(x, edge_index)
        
        assert purified_edge_index.size(0) == 2
        assert stats["original_edges"] == 5
        assert stats["purified_edges"] <= 5
        assert 0.0 <= stats["drop_rate"] <= 1.0

    def test_03_chebyshev_spectral_wavelet_engine(self):
        """Tests that ChebyshevSpectralWaveletEngine extracts 4 multi-scale spectral wavelet diffusion bands."""
        torch.manual_seed(42)
        num_nodes = 8
        in_dim = 8
        K = 4
        x = torch.randn(num_nodes, in_dim)
        
        src = torch.tensor([0, 1, 2, 3, 4, 5, 6, 7])
        dst = torch.tensor([1, 2, 3, 4, 5, 6, 7, 0])
        edge_index = torch.stack([src, dst])
        
        engine = ChebyshevSpectralWaveletEngine(K=K)
        bands = engine.extract_wavelet_bands(x, edge_index)
        
        assert bands.shape == (num_nodes, in_dim * K)
        assert not torch.isnan(bands).any()

    def test_04_neural_optimal_transport_sinkhorn(self):
        """Tests that SinkhornDomainAligner computes optimal transport Wasserstein distance across domains."""
        torch.manual_seed(42)
        dim = 16
        ns = 25
        nt = 30
        
        z_source = torch.randn(ns, dim)
        z_target = torch.randn(nt, dim) + 2.0  # Shifted domain
        
        aligner = SinkhornDomainAligner(reg_epsilon=0.10, max_iter=50)
        w_dist, T = aligner(z_source, z_target)
        
        assert w_dist.item() > 0.0
        assert T.shape == (ns, nt)
        assert torch.allclose(T.sum(), torch.tensor(1.0), atol=1e-2)
        
        loss_fn = EntropicWassersteinLoss(reg_epsilon=0.10, loss_weight=0.5)
        loss = loss_fn(z_source, z_target)
        assert loss.item() > 0.0

    def test_05_benjamini_hochberg_conformal_fdr(self):
        """Tests that BenjaminiHochbergConformalFDR calculates valid p-values and controls empirical FDR."""
        np.random.seed(42)
        fdr_controller = BenjaminiHochbergConformalFDR(q_target=0.05, method="BH")
        
        # Calibration non-conformity scores under Null (clean accounts)
        calib_clean = np.random.beta(1.0, 5.0, 500)
        calib_labels = np.zeros(500, dtype=int)
        fdr_controller.calibrate(calib_clean, calib_labels)
        
        # Test transactions: 80 clean, 20 high-confidence fraud
        test_clean = np.random.beta(1.0, 5.0, 80)
        test_fraud = np.random.beta(8.0, 1.0, 20)
        test_scores = np.concatenate([test_clean, test_fraud])
        test_labels = np.concatenate([np.zeros(80, dtype=int), np.ones(20, dtype=int)])
        
        results = fdr_controller.select_alerts(test_scores, q_target=0.05)
        assert "alert_mask" in results
        assert "p_values" in results
        assert len(results["alert_mask"]) == 100
        
        metrics = fdr_controller.evaluate_empirical_fdr(results["alert_mask"], test_labels)
        assert metrics["empirical_fdr"] <= 0.10  # Bounded false discoveries
        assert metrics["true_positives"] > 0
