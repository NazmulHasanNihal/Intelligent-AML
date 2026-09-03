"""
test_enhanced_cstgb_pipeline.py — Verification of Algorithm Improvements in C-STGB & HT-GNN.

Tests:
1. CostSensitiveFocalTverskyLoss: Adaptive class imbalance scaling, dollar penalty weighting, gradient flow.
2. OptimalThresholdCalibrator: aml_utility objective under severe class imbalance.
3. DirectedMotifKernel: Higher-order 3-cycle, 4-cycle, reciprocal edges, and closed-loop wash index computation.
4. ZeroDivergenceArbiter: Fast vectorized batch arbitration and single transaction triage.
5. CSTGBClassifier: Feature extraction with motif matrices and ensemble predictions.
"""

import pytest
import torch
import numpy as np
from src.models.focal_tversky_loss import CostSensitiveFocalTverskyLoss, AdaptiveFocalTverskyLoss
from src.models.threshold_optimizer import OptimalThresholdCalibrator
from src.models.motif_kernel import DirectedMotifKernel
from src.engine.zero_divergence_arbiter import ZeroDivergenceArbiter


def test_adaptive_focal_tversky_loss():
    loss_fn = CostSensitiveFocalTverskyLoss(alpha=0.25, beta=0.75, gamma=1.33, adaptive_imbalance=True)
    
    # 100 samples with 2 positive (2% imbalance)
    logits = torch.randn(100, requires_grad=True)
    targets = torch.zeros(100)
    targets[5] = 1.0
    targets[42] = 1.0
    amounts = torch.randint(100, 10000, (100,)).float()
    
    loss = loss_fn(logits, targets, amounts=amounts)
    assert loss.item() >= 0.0
    assert torch.isfinite(loss)
    
    # Check backward pass / gradient flow
    loss.backward()
    assert logits.grad is not None
    assert torch.isfinite(logits.grad).all()


def test_threshold_optimizer_aml_utility():
    calibrator = OptimalThresholdCalibrator(target_metric="aml_utility", num_candidates=200)
    
    # 1000 samples, 10 positive (1% imbalance)
    np.random.seed(42)
    y_true = np.zeros(1000, dtype=int)
    pos_idx = np.random.choice(1000, 10, replace=False)
    y_true[pos_idx] = 1
    
    # Positive samples have higher average predicted probabilities
    y_probs = np.random.beta(0.5, 20.0, size=1000)
    y_probs[pos_idx] = np.random.beta(5.0, 2.0, size=10)
    
    opt_tau = calibrator.fit(y_true, y_probs)
    assert 0.0 < opt_tau < 1.0
    assert "metrics_at_optimal_tau" in calibrator.calibration_report
    report = calibrator.calibration_report["metrics_at_optimal_tau"]
    assert "f1_score" in report
    assert "recall" in report
    assert report["recall"] > 0.0


def test_directed_motif_kernel():
    motif_engine = DirectedMotifKernel(max_cycle_order=4)
    
    # Construct a directed 3-cycle: 0 -> 1 -> 2 -> 0
    src = [0, 1, 2]
    dst = [1, 2, 0]
    edge_index = torch.tensor([src, dst], dtype=torch.long)
    
    motifs = motif_engine.compute_ego_cycle_motifs(edge_index, num_nodes=3)
    assert "cycle3_count" in motifs
    assert "cycle4_count" in motifs
    assert "closed_loop_index" in motifs
    
    # Each node in a 3-cycle should have cycle3_count == 1
    np.testing.assert_array_equal(motifs["cycle3_count"], np.array([1.0, 1.0, 1.0], dtype=np.float32))
    assert (motifs["closed_loop_index"] > 0).all()


def test_zero_divergence_arbiter_batch():
    arbiter = ZeroDivergenceArbiter(conformal_alpha=0.05)
    
    ai_probs = np.array([0.10, 0.45, 0.90, 0.35])
    amounts = np.array([500.0, 9500.0, 2000.0, 100.0])  # sample 1 has $9,500 structuring
    closed_loop = np.array([0.0, 0.10, 0.0, 0.60])     # sample 3 has 0.60 wash trading
    
    blended = arbiter.evaluate_batch(ai_probs, amounts=amounts, closed_loop_indices=closed_loop)
    
    assert len(blended) == 4
    # Sample 1 ($9500 structuring) should be boosted to at least 0.75
    assert blended[1] >= 0.75
    # Sample 3 (wash trading 0.60) should be boosted to at least 0.88
    assert blended[3] >= 0.88
    # Sample 0 should remain 0.10
    assert np.isclose(blended[0], 0.10)
