import pytest
import numpy as np
import torch

from src.models.graph_smote import BilinearEdgeGenerator, LatentGraphSMOTE, DynamicThresholdCalibrator


def test_bilinear_edge_generator():
    """Verifies that BilinearEdgeGenerator computes pairwise edge probabilities and backprops."""
    generator = BilinearEdgeGenerator(hidden_dim=32)
    
    h_u = torch.randn(10, 32)
    h_v = torch.randn(15, 32)
    
    probs = generator(h_u, h_v)
    assert probs.shape == (10, 15)
    assert (probs >= 0.0).all() and (probs <= 1.0).all()
    
    # Loss and gradient test
    real_edge_index = torch.tensor([[0, 1, 2, 3], [4, 5, 6, 7]], dtype=torch.long)
    h_all = torch.randn(20, 32)
    loss = generator.edge_loss(h_all, real_edge_index)
    assert loss.item() > 0.0
    loss.backward()
    assert generator.relation_matrix.grad is not None


def test_latent_graph_smote_synthesis():
    """Verifies that LatentGraphSMOTE synthesizes minority nodes and connects them to the graph."""
    smote = LatentGraphSMOTE(hidden_dim=32, k_neighbors=3, oversample_ratio=0.50)
    
    n_nodes = 50
    h = torch.randn(n_nodes, 32)
    # 40 benign (0), 10 illicit (1)
    y = torch.zeros(n_nodes, dtype=torch.long)
    y[:10] = 1
    
    edge_index = torch.randint(0, n_nodes, (2, 100))
    
    h_aug, y_aug, edge_aug = smote.synthesize_latent_nodes(h, y, edge_index)
    
    # 10 positive nodes * 0.5 ratio = 5 virtual nodes synthesized
    expected_new_nodes = int(10 * 0.50)
    assert h_aug.shape == (n_nodes + expected_new_nodes, 32)
    assert y_aug.shape == (n_nodes + expected_new_nodes,)
    assert (y_aug[n_nodes:] == 1).all(), "Synthesized nodes must have positive illicit label (1)"
    assert edge_aug.shape[1] > edge_index.shape[1], "Edge generator must construct links for virtual nodes"


def test_dynamic_threshold_calibrator():
    """Verifies that DynamicThresholdCalibrator recovers high Recall on imbalanced predictions."""
    np.random.seed(42)
    n = 2000
    y_true = np.zeros(n, dtype=int)
    y_true[:50] = 1  # 2.5% positive
    
    # Model assigns moderate probabilities to positive class under high imbalance
    probs = np.random.beta(0.5, 30.0, size=n)
    probs[:50] = np.random.beta(2.0, 5.0, size=50)  # Average ~0.28
    
    calibrator = DynamicThresholdCalibrator(beta=2.0)
    tau_star = calibrator.calibrate(probs, y_true)
    
    # Default 0.50 threshold would have near 0 recall
    default_rec = np.sum((probs >= 0.50) & (y_true == 1)) / 50.0
    calibrated_rec = np.sum((probs >= tau_star) & (y_true == 1)) / 50.0
    
    assert tau_star < 0.40, f"Calibrated threshold should be < 0.40, got {tau_star}"
    assert calibrated_rec > default_rec, "Calibrated threshold must yield higher Recall than default 0.50"
    assert calibrated_rec >= 0.70, f"Calibrated recall should be >= 70%, got {calibrated_rec*100:.1f}%"
