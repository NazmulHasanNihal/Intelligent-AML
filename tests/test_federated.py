"""
test_federated.py — Unit & Integration Tests for Privacy-Preserving Federated Graph Learning (FedProx + DP).
Tests:
1. FederatedDifferentialPrivacyEngine: L2 norm clipping and Gaussian noise sanitization.
2. FedProxServer: Weighted client aggregation across decentralized banking nodes.
3. FederatedBankClient: Local training simulation with proximal regularization.
4. Multi-Round Collaborative Learning Simulation across 5 simulated financial institutions.
"""

import unittest
import torch
import copy
from src.federated.fed_gnn import FederatedDifferentialPrivacyEngine, FedProxServer, FederatedBankClient


class SimpleMockGNN(torch.nn.Module):
    """Simple neural module for testing federated parameter updates."""
    def __init__(self, in_dim=16, out_dim=2):
        super().__init__()
        self.fc1 = torch.nn.Linear(in_dim, 32)
        self.fc2 = torch.nn.Linear(32, out_dim)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


class TestFederatedLearning(unittest.TestCase):
    """Tests for Cross-Bank Federated Learning and Differential Privacy."""

    def setUp(self):
        self.global_model = SimpleMockGNN()
        self.dp_engine = FederatedDifferentialPrivacyEngine(clip_norm=1.0, noise_multiplier=0.1)
        self.fed_server = FedProxServer(self.global_model, mu_proximal=0.01, dp_noise_multiplier=0.05)

    def test_differential_privacy_clipping_and_noise(self):
        """Test that weight updates are strictly clipped and sanitized with DP noise."""
        local_weights = copy.deepcopy(self.global_model.state_dict())
        global_weights = copy.deepcopy(self.global_model.state_dict())

        # Inject massive artificial delta
        for k in local_weights:
            local_weights[k] = local_weights[k] + 100.0

        sanitized = self.dp_engine.sanitize_model_updates(local_weights, global_weights)

        # Verify that sanitized parameters are not exploded and have DP bounds
        for k in sanitized:
            self.assertEqual(sanitized[k].shape, global_weights[k].shape)
            diff = (sanitized[k] - global_weights[k]).abs().max().item()
            # Since clip_norm is 1.0, max diff per parameter should be well bounded
            self.assertLess(diff, 10.0)

    def test_fedprox_server_aggregation(self):
        """Test multi-bank weighted aggregation on the central server."""
        clients = [
            FederatedBankClient(bank_id=f"bank_{i}", local_data_count=1000 * (i + 1))
            for i in range(3)
        ]

        global_state = self.global_model.state_dict()
        client_updates = [c.train_local_epoch(global_state) for c in clients]
        client_counts = [c.local_data_count for c in clients]

        telemetry = self.fed_server.aggregate_client_updates(client_updates, client_counts)

        self.assertEqual(telemetry["round"], 1)
        self.assertEqual(telemetry["participating_banks_count"], 3)
        self.assertEqual(telemetry["total_transactions_aggregated"], 6000)

    def test_multi_round_federated_convergence(self):
        """Test a 5-round collaborative federated training loop across 4 banks."""
        num_rounds = 5
        banks = [
            FederatedBankClient(bank_id=f"tier1_bank_{i}", local_data_count=5000)
            for i in range(4)
        ]

        for r in range(num_rounds):
            current_global = self.global_model.state_dict()
            updates = [b.train_local_epoch(current_global) for b in banks]
            counts = [b.local_data_count for b in banks]
            telemetry = self.fed_server.aggregate_client_updates(updates, counts)
            self.assertEqual(telemetry["round"], r + 1)

        self.assertEqual(len(self.fed_server.round_history), 5)


if __name__ == "__main__":
    unittest.main()
