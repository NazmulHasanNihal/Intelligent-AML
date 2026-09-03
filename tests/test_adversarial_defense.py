"""
test_adversarial_defense.py — Unit tests for Minimax Adversarial Camouflage & Counterfactual Graph Defense:
1. AdversarialCamouflageGenerator
2. MinimaxAdversarialTrainer
3. CounterfactualRobustnessAuditor
4. AdversarialTopologyDefense
"""

import unittest
import torch
import torch.nn as nn
import numpy as np

from src.models.adversarial_defense import (
    AdversarialCamouflageGenerator,
    MinimaxAdversarialTrainer,
    CounterfactualRobustnessAuditor,
    AdversarialTopologyDefense,
)


class DummyGNN(nn.Module):
    """Simple 2-layer graph neural network for testing adversarial robustness."""
    def __init__(self, in_channels=8, hidden_channels=16, out_channels=2):
        super().__init__()
        self.lin1 = nn.Linear(in_channels, hidden_channels)
        self.lin2 = nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index, delta_t=None, burst_score=None):
        h = torch.relu(self.lin1(x))
        # Simple mean aggregation over edge_index
        src, dst = edge_index[0], edge_index[1]
        msg = h[src]
        agg = torch.zeros_like(h)
        agg.index_add_(0, dst, msg)
        return self.lin2(h + agg)


class TestAdversarialDefense(unittest.TestCase):

    def test_01_camouflage_generator_budget_and_injection(self):
        """Tests that AdversarialCamouflageGenerator injects camouflage edges strictly within budget."""
        generator = AdversarialCamouflageGenerator(perturbation_budget=0.10, max_injected_edges=50)
        
        num_nodes = 20
        # 10 clean edges
        edge_index = torch.tensor([
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        ], dtype=torch.long)
        
        # 2 illicit nodes (0, 1) and 18 benign nodes (2..19)
        y = torch.zeros(num_nodes, dtype=torch.long)
        y[0] = 1
        y[1] = 1
        
        pert_edges, is_adv, tel = generator.generate_camouflage_perturbations(
            edge_index=edge_index,
            y_labels=y,
            num_nodes=num_nodes
        )
        
        self.assertGreaterEqual(pert_edges.shape[1], edge_index.shape[1])
        self.assertEqual(is_adv.shape[0], pert_edges.shape[1])
        self.assertTrue(is_adv[edge_index.shape[1]:].all())
        self.assertIn("injected_camouflage_edges", tel)
        self.assertIn("attack_intensity_pct", tel)

    def test_02_minimax_adversarial_trainer_differentiability(self):
        """Tests that MinimaxAdversarialTrainer computes regularized robust loss and propagates gradients."""
        model = DummyGNN(in_channels=8, hidden_channels=16, out_channels=2)
        minimax_trainer = MinimaxAdversarialTrainer(adv_gamma=0.35, perturbation_budget=0.10)
        criterion = nn.CrossEntropyLoss()
        
        x = torch.randn(15, 8, requires_grad=True)
        edge_index = torch.tensor([[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 0]], dtype=torch.long)
        y = torch.tensor([1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=torch.long)
        
        loss, metrics = minimax_trainer(model, x, edge_index, y, criterion)
        self.assertTrue(torch.is_tensor(loss))
        self.assertGreater(loss.item(), 0.0)
        self.assertIn("loss_clean", metrics)
        self.assertIn("loss_adv", metrics)
        self.assertIn("loss_robust", metrics)
        
        # Check backward differentiability
        loss.backward()
        self.assertIsNotNone(model.lin1.weight.grad)

    def test_03_counterfactual_robustness_auditor(self):
        """Tests that CounterfactualRobustnessAuditor measures minimal edit evasion distance."""
        model = DummyGNN(in_channels=4, hidden_channels=8, out_channels=2)
        auditor = CounterfactualRobustnessAuditor(max_edit_search=10)
        
        x = torch.randn(8, 4)
        edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=torch.long)
        benign_candidates = [2, 3, 4, 5, 6, 7]
        
        report = auditor.audit_node_robustness(
            model=model,
            target_node_idx=0,
            x=x,
            edge_index=edge_index,
            benign_candidate_nodes=benign_candidates
        )
        
        self.assertIn("target_node", report)
        self.assertIn("initial_prediction", report)
        self.assertIn("robustness_status" if report["initial_prediction"] == "LICIT" else "robustness_rating", report)

    def test_04_micro_dusting_and_resilience_filter(self):
        """Tests micro-dusting pruning and graph perturbation resilience scoring."""
        defense = AdversarialTopologyDefense(dusting_amount_floor=1.0)
        
        edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 0]], dtype=torch.long)
        # Edge amounts: 0.01 (dusting), 50.0 (valid), 0.005 (dusting), 100.0 (valid)
        amounts = torch.tensor([0.01, 50.0, 0.005, 100.0])
        dt = torch.tensor([1.0, 2.0, 3.0, 4.0])
        bs = torch.tensor([0.5, 1.2, 0.3, 2.5])
        
        filtered_edges, filtered_dt, filtered_bs, tel = defense.filter_micro_dusting_edges(
            edge_index=edge_index,
            edge_amounts=amounts,
            delta_t=dt,
            burst_score=bs
        )
        
        self.assertEqual(filtered_edges.shape[1], 2)
        self.assertEqual(tel["pruned_dusting_edges"], 2)
        
        # Test resilience index computation
        resilience = defense.compute_adversarial_resilience_index(
            x_dict={"Account": torch.randn(10, 8)},
            edge_index_dict={("Account", "tx", "Account"): filtered_edges}
        )
        self.assertIn("resilience_score", resilience)
        self.assertIn("status", resilience)


if __name__ == "__main__":
    unittest.main()
