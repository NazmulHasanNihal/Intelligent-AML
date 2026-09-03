import unittest
import torch
import torch.nn as nn
from src.models.htgnn import BurstAwareHGT
from src.models.continual_learning import (
    ElasticWeightConsolidation,
    TopologicalReservoirBuffer,
    ContinuousLearningEngine,
)


class TestContinualLearning(unittest.TestCase):
    def setUp(self):
        self.metadata = (
            ["Account"],
            [("Account", "transfers_to", "Account")]
        )
        self.in_channels_dict = {"Account": 16}
        self.model = BurstAwareHGT(
            metadata=self.metadata,
            in_channels_dict=self.in_channels_dict,
            hidden_channels=32,
            num_heads=2,
            num_layers=1,
        )

    def _generate_synthetic_batch(self, num_nodes=20):
        x_dict = {"Account": torch.randn(num_nodes, 16)}
        edge_index = torch.randint(0, num_nodes, (2, 40))
        edge_index_dict = {("Account", "transfers_to", "Account"): edge_index}
        delta_t_dict = {("Account", "transfers_to", "Account"): torch.rand(40)}
        burst_score_dict = {("Account", "transfers_to", "Account"): torch.rand(40)}
        y_target = torch.randint(0, 2, (num_nodes,))
        return (x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target)

    def test_elastic_weight_consolidation(self):
        batches = [self._generate_synthetic_batch() for _ in range(3)]
        ewc = ElasticWeightConsolidation(self.model, batches, target_node="Account")
        
        # Initial penalty should be 0 since weights have not changed
        init_penalty = ewc.penalty(self.model)
        self.assertAlmostEqual(init_penalty.item(), 0.0, places=4)
        
        # Perturb weights and verify penalty grows
        with torch.no_grad():
            for p in self.model.parameters():
                p.add_(torch.randn_like(p) * 0.1)
                
        shifted_penalty = ewc.penalty(self.model)
        self.assertGreater(shifted_penalty.item(), 0.0)

    def test_topological_reservoir_buffer(self):
        buffer = TopologicalReservoirBuffer(capacity=100, minority_ratio=0.5)
        for i in range(200):
            sample = (f"node_{i}", torch.randn(10))
            y_label = 1 if i % 5 == 0 else 0
            buffer.add(sample, y_label)
            
        self.assertLessEqual(len(buffer.buffer_illicit) + len(buffer.buffer_licit), 100)
        samples_x, samples_y = buffer.sample(n=20)
        self.assertEqual(len(samples_x), 20)
        self.assertEqual(len(samples_y), 20)

    def test_continuous_learning_engine(self):
        engine = ContinuousLearningEngine(self.model, ewc_lambda=100.0, buffer_capacity=500)
        batches = [self._generate_synthetic_batch() for _ in range(2)]
        engine.snapshot_task_knowledge(batches, target_node="Account")
        
        penalty = engine.get_continual_penalty()
        self.assertAlmostEqual(penalty.item(), 0.0, places=3)


if __name__ == "__main__":
    unittest.main()
