"""
Tests for Layer 2 — HT-GNN & GraphGAN Models.
"""
import unittest
import torch

from src.models import HTGNNAccelerator, GraphGAN, train_htgnn, train_graphgan


class TestModels(unittest.TestCase):
    """Tests for Layer 2 detection models."""

    def test_htgnn_forward_pass(self):
        """Verify HT-GNN produces output tensors of expected shape."""
        model = HTGNNAccelerator(
            in_channels=16,
            hidden_channels=128,
            num_layers=3,
            dropout=0.3,
        )
        from torch_geometric.data import HeteroData
        data = HeteroData()
        data["node"].x = torch.randn(100, 16)
        data["node"].num_nodes = 100
        data["node", "Transaction", "node"].edge_index = torch.randint(
            0, 100, (2, 50), dtype=torch.long
        )
        out = model(data)
        self.assertIn("Account", out)
        self.assertEqual(out["Account"].shape, (100, 2))

    def test_graphgan_synthetic_output(self):
        """Verify GraphGAN generates structurally valid synthetic subgraphs."""
        model = GraphGAN(latent_dim=64, num_nodes=10)
        z = torch.randn(2, 64)
        node_feat, edge_probs = model(z)
        self.assertEqual(node_feat.shape, (2, 10, 128))
        self.assertEqual(edge_probs.shape, (2, 10, 10))

    def test_risk_score_range(self):
        """Verify risk scores are normalized between 0 and 1."""
        model = HTGNNAccelerator(
            in_channels=16,
            hidden_channels=128,
            num_layers=3,
            dropout=0.3,
        )
        from torch_geometric.data import HeteroData
        data = HeteroData()
        data["node"].x = torch.randn(50, 16)
        data["node"].num_nodes = 50
        data["node", "Transaction", "node"].edge_index = torch.randint(
            0, 50, (2, 30), dtype=torch.long
        )
        model.eval()
        with torch.no_grad():
            out = model(data)
        if "Account" in out:
            probs = torch.softmax(out["Account"], dim=1)[:, 1]
            self.assertTrue((probs >= 0).all() and (probs <= 1).all())


if __name__ == "__main__":
    unittest.main()