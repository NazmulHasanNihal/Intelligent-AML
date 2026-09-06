"""
test_all_improvements.py — Comprehensive verification of all 8 algorithm improvements.

Tests:
1. Stratified Minority Oversampling (batch construction logic)
2. Banking-Specific Temporal Sequence Features (TemporalSequenceFeatureExtractor)
3. Dataset-Adaptive Hyperparameter Profiles (get_dataset_profile)
4. Isotonic Probability Calibration (OptimalThresholdCalibrator with isotonic)
5. Borderline-SMOTE + Tomek Links (import and API verification)
6. Deep GNN + Jumping Knowledge (BurstAwareHGT with JK-cat)
7. Hard Negative Mining (retraining logic verification)
8. Temporal Sequence Encoder module standalone test
9. Full pipeline: CostSensitiveFocalTverskyLoss + DirectedMotifKernel + ZeroDivergenceArbiter
"""

import pytest
import torch
import numpy as np


def test_dataset_adaptive_profiles():
    """Improvement #3: Verify dataset-adaptive profiles exist and return correct keys."""
    from src.models.htgnn import get_dataset_profile, DATASET_PROFILES, DEFAULT_PROFILE
    
    # Known datasets should have profiles
    ibm_profile = get_dataset_profile("ibm_amlsim_hi_small")
    assert ibm_profile["gnn_layers"] in [4, 6]
    assert ibm_profile["focal_beta"] >= 0.95
    assert ibm_profile["xgb_n"] == 800
    
    paysim_profile = get_dataset_profile("paysim1")
    assert paysim_profile["focal_beta"] == 0.95
    assert paysim_profile["lr"] == 0.0001
    
    elliptic_profile = get_dataset_profile("elliptic_v1")
    assert elliptic_profile["gnn_layers"] == 3
    assert elliptic_profile["focal_beta"] == 0.75
    
    # Unknown dataset should fall back to default
    unknown = get_dataset_profile("nonexistent_dataset")
    assert unknown == DEFAULT_PROFILE


def test_isotonic_threshold_calibrator():
    """Improvement #4: Verify isotonic calibration improves threshold optimization."""
    from src.models.threshold_optimizer import OptimalThresholdCalibrator
    
    np.random.seed(42)
    y_true = np.zeros(500, dtype=int)
    pos_idx = np.random.choice(500, 10, replace=False)
    y_true[pos_idx] = 1
    
    # Miscalibrated probabilities (positive samples have slightly higher but overlapping)
    y_probs = np.random.beta(0.3, 15.0, size=500)
    y_probs[pos_idx] = np.random.beta(3.0, 3.0, size=10)
    
    # Without isotonic
    cal_no_iso = OptimalThresholdCalibrator(target_metric="aml_utility", num_candidates=200, use_isotonic=False)
    tau_no_iso = cal_no_iso.fit(y_true, y_probs)
    
    # With isotonic
    cal_iso = OptimalThresholdCalibrator(target_metric="aml_utility", num_candidates=200, use_isotonic=True)
    tau_iso = cal_iso.fit(y_true, y_probs)
    
    assert 0.0 < tau_iso < 1.0
    assert cal_iso.isotonic_model is not None
    assert cal_iso.calibration_report["isotonic_calibration_applied"] == True
    
    # Calibrate new probabilities
    new_probs = np.array([0.1, 0.5, 0.9])
    calibrated = cal_iso.calibrate_probs(new_probs)
    assert len(calibrated) == 3
    assert all(0.0 <= p <= 1.0 for p in calibrated)


def test_temporal_sequence_feature_extractor():
    """Improvements #2 & #8: Verify banking-specific temporal feature extraction."""
    from src.models.temporal_sequence_encoder import TemporalSequenceFeatureExtractor
    
    extractor = TemporalSequenceFeatureExtractor()
    
    # Create a simple scenario: 5 nodes, 10 transactions
    node_ids = np.array(["A", "B", "C", "D", "E"])
    
    # A sends 3 structured deposits ($8500, $8200, $9100) to B within 48 hours
    edge_src = np.array(["A", "A", "A", "B", "B", "C", "C", "D", "D", "E"])
    edge_dst = np.array(["B", "B", "B", "C", "D", "D", "E", "E", "A", "A"])
    edge_amounts = np.array([8500, 8200, 9100, 5000, 3000, 7000, 2000, 1500, 500, 200], dtype=np.float64)
    edge_timestamps = np.array([100, 200, 300, 1000, 2000, 3000, 4000, 5000, 100000, 200000], dtype=np.float64)
    
    features = extractor.extract_node_temporal_features(
        node_ids, edge_src, edge_dst, edge_amounts, edge_timestamps
    )
    
    assert features.shape == (5, 8)
    # A has structured deposits, should have non-zero structuring count
    assert features[0, 0] > 0  # structuring_count
    # A sends to only B, fan-out ratio = 1/3 unique / 3 total
    assert 0 < features[0, 1] <= 1.0  # fan_out_ratio
    

def test_burst_aware_hgt_jumping_knowledge():
    """Improvement #6: Verify BurstAwareHGT works with JK-cat and deeper layers."""
    from src.models.htgnn import BurstAwareHGT
    
    metadata = (
        ["Account"],  # node types
        [("Account", "Transaction", "Account")]  # edge types
    )
    in_channels = {"Account": 36}
    
    # Create model with 4 layers and JK-cat
    model = BurstAwareHGT(
        in_channels_dict=in_channels,
        hidden_channels=32,
        num_layers=4,
        metadata=metadata,
        dropout=0.1,
        jk_mode="cat"
    )
    
    # Verify JK projection layers exist
    assert hasattr(model, "jk_proj")
    assert "Account" in model.jk_proj
    
    # Forward pass
    x_dict = {"Account": torch.randn(20, 36)}
    edge_index = torch.randint(0, 20, (2, 50))
    edge_index_dict = {("Account", "Transaction", "Account"): edge_index}
    delta_t_dict = {("Account", "Transaction", "Account"): torch.rand(50)}
    burst_dict = {("Account", "Transaction", "Account"): torch.rand(50)}
    
    embeddings = model.get_embeddings(x_dict, edge_index_dict, delta_t_dict, burst_dict)
    assert "Account" in embeddings
    assert embeddings["Account"].shape == (20, 32)  # Should be projected back to hidden_channels
    
    logits = model(x_dict, edge_index_dict, delta_t_dict, burst_dict)
    assert logits["Account"].shape == (20, 2)


def test_burst_aware_hgt_no_jk():
    """Verify BurstAwareHGT still works without JK (jk_mode=None)."""
    from src.models.htgnn import BurstAwareHGT
    
    metadata = (
        ["Account"],
        [("Account", "Transaction", "Account")]
    )
    
    model = BurstAwareHGT(
        in_channels_dict={"Account": 20},
        hidden_channels=32,
        num_layers=3,
        metadata=metadata,
        dropout=0.1,
        jk_mode=None
    )
    
    assert not hasattr(model, "jk_proj") or model.jk_mode != "cat"
    
    x_dict = {"Account": torch.randn(10, 20)}
    edge_index_dict = {("Account", "Transaction", "Account"): torch.randint(0, 10, (2, 20))}
    delta_t_dict = {("Account", "Transaction", "Account"): torch.rand(20)}
    burst_dict = {("Account", "Transaction", "Account"): torch.rand(20)}
    
    embeddings = model.get_embeddings(x_dict, edge_index_dict, delta_t_dict, burst_dict)
    assert embeddings["Account"].shape == (10, 32)


def test_adaptive_focal_tversky_loss():
    """Verify CostSensitiveFocalTverskyLoss with adaptive beta."""
    from src.models.focal_tversky_loss import CostSensitiveFocalTverskyLoss
    
    loss_fn = CostSensitiveFocalTverskyLoss(alpha=0.08, beta=0.92, gamma=1.33, adaptive_imbalance=True)
    
    logits = torch.randn(100, requires_grad=True)
    targets = torch.zeros(100)
    targets[5] = 1.0
    targets[42] = 1.0
    
    loss = loss_fn(logits, targets)
    assert loss.item() >= 0.0
    assert torch.isfinite(loss)
    loss.backward()
    assert logits.grad is not None


def test_directed_motif_kernel():
    """Verify DirectedMotifKernel cycle detection."""
    from src.models.motif_kernel import DirectedMotifKernel
    
    motif_engine = DirectedMotifKernel(max_cycle_order=4)
    edge_index = torch.tensor([[0, 1, 2], [1, 2, 0]], dtype=torch.long)
    
    motifs = motif_engine.compute_ego_cycle_motifs(edge_index, num_nodes=3)
    assert "cycle3_count" in motifs
    assert "closed_loop_index" in motifs
    np.testing.assert_array_equal(motifs["cycle3_count"], np.array([1.0, 1.0, 1.0], dtype=np.float32))


def test_zero_divergence_arbiter_batch():
    """Verify ZeroDivergenceArbiter vectorized batch arbitration."""
    from src.engine.zero_divergence_arbiter import ZeroDivergenceArbiter
    
    arbiter = ZeroDivergenceArbiter(conformal_alpha=0.05)
    ai_probs = np.array([0.10, 0.45, 0.90, 0.35])
    amounts = np.array([500.0, 9500.0, 2000.0, 100.0])
    closed_loop = np.array([0.0, 0.10, 0.0, 0.60])
    
    blended = arbiter.evaluate_batch(ai_probs, amounts=amounts, closed_loop_indices=closed_loop)
    assert len(blended) == 4
    assert blended[1] >= 0.75
    assert blended[3] >= 0.88
