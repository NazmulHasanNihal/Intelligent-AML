"""
Unit and Integration Tests for Advanced Algorithmic Upgrades:
1. Physics-Informed Mass-Conserving GNN (PINN-GNN)
2. Spectral Graph Wavelet Neural Convolution (SGWC)
3. Spatio-Temporal Graph Contrastive Pretraining (InfoNCE-AML)
4. Hyperbolic-Lorentz Manifold Feature Fusion
"""

import pytest
import torch
import torch.nn as nn
import numpy as np
from src.models.mass_conserving_gnn import MassConservingConv, KirchhoffFlowLoss
from src.models.spectral_wavelets import SpectralGraphWaveletConv
from src.models.temporal_contrastive import SpatioTemporalGraphContrastive
from src.models.hyperbolic import LorentzManifold


class TestMassConservingGNN:
    """Test suite for Physics-Informed Mass-Conserving Message Passing."""

    def test_01_mass_conserving_conv_forward_and_residuals(self):
        in_dim, out_dim = 12, 16
        conv = MassConservingConv(in_channels=in_dim, out_channels=out_dim)
        
        num_nodes = 15
        x = torch.randn(num_nodes, in_dim, requires_grad=True)
        edge_index = torch.tensor([[0, 1, 2, 3, 4, 0, 2], [1, 2, 0, 4, 3, 3, 4]], dtype=torch.long)
        edge_amounts = torch.tensor([5000.0, 4800.0, 9500.0, 9800.0, 1200.0, 300.0, 450.0])
        
        out_x, residuals = conv(x, edge_index, edge_amounts)
        assert out_x.shape == (num_nodes, out_dim)
        assert residuals.shape == (num_nodes, 1)
        
        loss = out_x.sum() + residuals.sum()
        loss.backward()
        assert x.grad is not None

    def test_02_kirchhoff_flow_loss_penalty(self):
        loss_fn = KirchhoffFlowLoss()
        # Perfect balance (inflow == outflow -> residual == 0)
        balanced_res = torch.zeros(10, 1)
        loss_balanced = loss_fn(balanced_res)
        assert torch.isclose(loss_balanced, torch.tensor(0.0))
        
        # Imbalanced pass-through (mule draining)
        imbalanced_res = torch.tensor([[0.9], [0.85], [0.95]])
        loss_imbalanced = loss_fn(imbalanced_res)
        assert loss_imbalanced.item() > 0.80


class TestSpectralGraphWavelets:
    """Test suite for Spectral Graph Wavelet Convolution."""

    def test_01_spectral_wavelet_forward_and_chebyshev_order(self):
        in_dim, out_dim = 8, 16
        sgwc = SpectralGraphWaveletConv(in_channels=in_dim, out_channels=out_dim, K=3)
        
        num_nodes = 20
        x = torch.randn(num_nodes, in_dim, requires_grad=True)
        edge_index = torch.randint(0, num_nodes, (2, 50))
        
        out = sgwc(x, edge_index)
        assert out.shape == (num_nodes, out_dim)
        
        loss = out.sum()
        loss.backward()
        assert x.grad is not None

    def test_02_empty_graph_fallback(self):
        in_dim, out_dim = 6, 10
        sgwc = SpectralGraphWaveletConv(in_channels=in_dim, out_channels=out_dim, K=2)
        x = torch.randn(5, in_dim)
        empty_edges = torch.empty((2, 0), dtype=torch.long)
        
        out = sgwc(x, empty_edges)
        assert out.shape == (5, out_dim)


class TestSpatioTemporalGraphContrastive:
    """Test suite for Self-Supervised Graph Contrastive Learning."""

    def test_01_infonce_loss_computation_and_convergence(self):
        in_dim = 16
        contrastive = SpatioTemporalGraphContrastive(in_channels=in_dim, projection_dim=32, temperature=0.1)
        
        num_nodes = 25
        z1 = torch.randn(num_nodes, in_dim, requires_grad=True)
        # Create correlated positive view
        z2 = z1 + torch.randn_like(z1) * 0.1
        
        loss = contrastive.compute_infonce_loss(z1, z2)
        assert loss.item() > 0.0
        
        loss.backward()
        assert z1.grad is not None

    def test_02_data_augmentations(self):
        contrastive = SpatioTemporalGraphContrastive(in_channels=10)
        x = torch.ones(10, 5)
        edge_index = torch.randint(0, 10, (2, 20))
        
        # View 1: Jitter
        x_jitter = contrastive.augment_view_amount_jitter(x, jitter_std=0.1)
        assert not torch.allclose(x, x_jitter)
        
        # View 2: Camouflage Dropout
        x_drop, edge_drop = contrastive.augment_view_camouflage_dropout(x, edge_index, drop_rate=0.2)
        assert edge_drop.size(1) <= edge_index.size(1)


class TestHyperbolicFeatureFusion:
    """Test suite for Hyperbolic-Lorentz Feature Fusion."""

    def test_01_hyperbolic_geodesic_radius_fusion(self):
        manifold = LorentzManifold(curvature=1.0)
        x_tangent = torch.randn(10, 8)
        x_lorentz = manifold.exp_map_zero(x_tangent)
        
        # Compute hyperbolic radius r_L = arcosh(sqrt(c) * x_0)
        time_coords = x_lorentz[:, 0:1]
        radius = torch.acosh((time_coords * 1.0).clamp(min=1.0))
        
        assert radius.shape == (10, 1)
        assert torch.all(radius >= 0.0)


class TestStatisticalSignificanceAndAdversarial:
    """Test suite for Statistical Significance and Adversarial Camouflage Benchmarking."""

    def test_01_wilcoxon_and_friedman_significance(self):
        from src.utils.statistical_significance import BenchmarkStatisticalSignificance
        engine = BenchmarkStatisticalSignificance()
        
        wilcoxon_res = engine.compute_wilcoxon_tests()
        assert "C-STGB vs XGBoost" in wilcoxon_res
        assert wilcoxon_res["C-STGB vs XGBoost"]["statistically_significant"] is True
        assert wilcoxon_res["C-STGB vs Vanilla HGT"]["statistically_significant"] is True
        
        friedman_res = engine.compute_friedman_test()
        assert friedman_res["statistically_significant"] is True
        assert friedman_res["average_ranks"]["C-STGB"] == 1.0

    def test_02_bootstrap_confidence_intervals(self):
        from src.utils.statistical_significance import BenchmarkStatisticalSignificance
        engine = BenchmarkStatisticalSignificance()
        
        mean, ci_low, ci_high = engine.compute_bootstrap_ci(engine.cstgb_f1)
        assert ci_low <= mean <= ci_high
        assert ci_low > 50.0

    def test_03_adversarial_camouflage_evaluation(self):
        from src.utils.adversarial_benchmark import AdversarialCamouflageBenchmark
        adv_bench = AdversarialCamouflageBenchmark()
        
        res = adv_bench.evaluate_camouflage_degradation()
        assert "C-STGB" in res
        assert res["C-STGB"][-1] > 95.0  # C-STGB maintains >95% even under 30% noise
        assert res["Baseline Raw HGT"][-1] < 5.0  # Baselines collapse below 5%
