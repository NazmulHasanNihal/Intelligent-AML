"""
test_model_enhancements.py — Unit tests for AML Precision/Recall Enhancements:
1. CostSensitiveFocalTverskyLoss
2. OptimalThresholdCalibrator
3. Hard-Example Priority Mining in TopologicalReservoirBuffer
"""

import unittest
import torch
import numpy as np

from src.models.focal_tversky_loss import CostSensitiveFocalTverskyLoss
from src.models.threshold_optimizer import OptimalThresholdCalibrator
from src.models.continual_learning import TopologicalReservoirBuffer


class TestModelEnhancements(unittest.TestCase):
    
    def test_01_focal_tversky_loss_forward_and_backward(self):
        """Tests Focal Tversky loss computation, gradient propagation, and amount weighting."""
        criterion = CostSensitiveFocalTverskyLoss(alpha=0.30, beta=0.70, gamma=1.33)
        
        # 10 samples, 2 classes
        logits = torch.randn(10, 2, requires_grad=True)
        targets = torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], dtype=torch.long)
        amounts = torch.tensor([100.0, 50.0, 20.0, 500.0, 10.0, 30.0, 200.0, 50.0, 50000.0, 100000.0])
        
        loss = criterion(logits, targets, amounts=amounts)
        self.assertTrue(torch.is_tensor(loss))
        self.assertGreater(loss.item(), 0.0)
        self.assertLessEqual(loss.item(), 1.0)
        
        # Check backward differentiability
        loss.backward()
        self.assertIsNotNone(logits.grad)
        self.assertFalse(torch.isnan(logits.grad).any())

    def test_02_focal_tversky_asymmetric_recall_penalty(self):
        """Verifies that False Negatives are penalized more heavily than False Positives when beta > alpha."""
        criterion = CostSensitiveFocalTverskyLoss(alpha=0.20, beta=0.80, gamma=1.0)
        
        # Case A: False Negative (Target is 1, Model predicts 0 with high confidence)
        logits_fn = torch.tensor([[5.0, -5.0]]) # predicts class 0
        targets_fn = torch.tensor([1], dtype=torch.long)
        loss_fn = criterion(logits_fn, targets_fn)
        
        # Case B: False Positive (Target is 0, Model predicts 1 with high confidence)
        logits_fp = torch.tensor([[-5.0, 5.0]]) # predicts class 1
        targets_fp = torch.tensor([0], dtype=torch.long)
        loss_fp = criterion(logits_fp, targets_fp)
        
        # False Negative must result in a strictly higher penalty
        self.assertGreater(loss_fn.item(), loss_fp.item())

    def test_03_optimal_threshold_calibrator_fit_and_predict(self):
        """Tests that OptimalThresholdCalibrator finds a superior threshold on imbalanced scores."""
        calibrator = OptimalThresholdCalibrator(target_metric="f1_f2_harmonic", num_candidates=200)
        
        np.random.seed(42)
        # 1000 licit scores centered around 0.15, 20 illicit scores centered around 0.35
        licit_scores = np.random.beta(1.5, 8.0, size=1000)
        illicit_scores = np.random.beta(3.5, 5.0, size=20)
        
        y_probs = np.concatenate([licit_scores, illicit_scores])
        y_true = np.array([0] * 1000 + [1] * 20)
        
        best_tau = calibrator.fit(y_true, y_probs)
        self.assertGreaterEqual(best_tau, 0.01)
        self.assertLess(best_tau, 0.95)
        
        preds = calibrator.predict(y_probs)
        self.assertEqual(len(preds), len(y_true))
        
        # Report must contain metrics at optimal tau
        report = calibrator.calibration_report
        self.assertIn("metrics_at_optimal_tau", report)
        self.assertIn("f1_score", report["metrics_at_optimal_tau"])

    def test_04_hard_negative_reservoir_priority_admission(self):
        """Tests priority admission of high-error boundary cases into TopologicalReservoirBuffer."""
        buffer = TopologicalReservoirBuffer(capacity=50, minority_ratio=0.5)
        
        # Add 100 easy samples (error = 0.0) vs 100 hard samples (error = 1.0)
        np.random.seed(42)
        for i in range(100):
            buffer.add_with_priority((f"easy_{i}", torch.randn(5)), y_label=0, prediction_error=0.0)
            buffer.add_with_priority((f"hard_{i}", torch.randn(5)), y_label=1, prediction_error=1.0)
            
        total_samples = len(buffer.buffer_licit) + len(buffer.buffer_illicit)
        self.assertLessEqual(total_samples, 50)
        
        samples_x, samples_y = buffer.sample(n=10)
        self.assertEqual(len(samples_x), 10)
        self.assertEqual(len(samples_y), 10)


    def test_05_cstgb_classifier_init_and_fallback(self):
        """Tests that CSTGBClassifier initializes properly with GPU/CPU auto-detection."""
        from src.models.htgnn import CSTGBClassifier, BurstAwareHGT
        metadata = (["Account"], [("Account", "transfers_to", "Account")])
        gnn = BurstAwareHGT(in_channels_dict={"Account": 8}, hidden_channels=16, num_heads=2, num_layers=1, metadata=metadata)
        
        clf = CSTGBClassifier(gnn, target_node="Account", hidden_channels=16)
        self.assertIsNotNone(clf.xgb_tab)
        self.assertIsNotNone(clf.lgbm_tab)
        self.assertIsNotNone(clf.cat_tab)
        self.assertIsNotNone(clf.xgb_fused)
        self.assertIsNotNone(clf.lgbm_fused)

    def test_06_1cycle_lr_scheduler_dynamics(self):
        """Tests that OneCycleLR steps smoothly across warmup and annealing phases."""
        from torch.optim.lr_scheduler import OneCycleLR
        dummy_model = torch.nn.Linear(10, 2)
        optimizer = torch.optim.AdamW(dummy_model.parameters(), lr=1e-3)
        
        total_epochs = 10
        scheduler = OneCycleLR(optimizer, max_lr=3e-3, total_steps=total_epochs, pct_start=0.2, anneal_strategy="cos")
        
        lrs = []
        for epoch in range(total_epochs):
            optimizer.step()
            lrs.append(optimizer.param_groups[0]["lr"])
            scheduler.step()
            
        # LR should increase during warmup and decrease during annealing
        self.assertEqual(len(lrs), 10)
        self.assertGreater(max(lrs), lrs[0])
        self.assertLess(lrs[-1], max(lrs))

    def test_07_vanilla_hgt_baseline_forward(self):
        """Tests VanillaHGTBaseline forward pass on heterogeneous graph structures."""
        from comparing_models.base_models import VanillaHGTBaseline
        metadata = (["Account", "Merchant"], [("Account", "transfers_to", "Merchant")])
        in_channels = {"Account": 16, "Merchant": 8}
        
        hgt = VanillaHGTBaseline(in_channels, hidden_channels=32, num_layers=2, metadata=metadata, num_heads=2)
        x_dict = {
            "Account": torch.randn(10, 16),
            "Merchant": torch.randn(5, 8)
        }
        edge_index_dict = {
            ("Account", "transfers_to", "Merchant"): torch.tensor([[0, 1, 2, 3], [0, 1, 2, 0]], dtype=torch.long)
        }
        out_dict = hgt(x_dict, edge_index_dict)
        self.assertIn("Account", out_dict)
        self.assertIn("Merchant", out_dict)
        self.assertEqual(out_dict["Account"].shape, (10, 2))
        self.assertEqual(out_dict["Merchant"].shape, (5, 2))

    def test_08_care_gnn_baseline_forward(self):
        """Tests CareGNNBaseline camouflage-aware filtering forward pass."""
        from comparing_models.base_models import CareGNNBaseline
        care_gnn = CareGNNBaseline(in_channels=16, hidden_channels=32, out_channels=2)
        
        x = torch.randn(12, 16)
        edge_index = torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 0]], dtype=torch.long)
        
        out = care_gnn(x, edge_index)
        self.assertEqual(out.shape, (12, 2))


if __name__ == "__main__":
    unittest.main()

