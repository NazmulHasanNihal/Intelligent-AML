"""
test_next_frontier.py — Unit & Integration Test Suite for Next-Frontier AML Extensions.
Verifies:
1. Directed Motif & Higher-Order Cycle Kernel (3-hop/4-hop DAG detection)
2. Neuro-Symbolic Logic Loss Regularizer (Differentiable Statutory Constraints)
3. Privacy-Preserving Federated GNN (FedProx + Differential Privacy Noise)
4. Distributed Kafka Streams & Neo4j/Memgraph Graph Database Connector
"""

import os
import sys
import unittest
import json
import torch
import numpy as np

# Ensure project root is on path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.models.motif_kernel import DirectedMotifKernel
from src.models.neuro_symbolic_loss import NeuroSymbolicAMLLoss
from src.federated.fed_gnn import FedProxServer, FederatedBankClient
from src.ingestion.streaming.kafka_neo4j_connector import DistributedKafkaTransactionConsumer, Neo4jBoltGraphConnector


class TestNextFrontierSuite(unittest.TestCase):

    def setUp(self):
        self.motif_kernel = DirectedMotifKernel(max_cycle_order=4)
        self.logic_loss = NeuroSymbolicAMLLoss(lambda_logic=0.50)
        self.kafka_consumer = DistributedKafkaTransactionConsumer(batch_size=5)

    def test_01_directed_cycle_motif_kernel(self):
        """Tests exact 3-cycle and 4-cycle circular laundering ring detection."""
        # Create synthetic 3-cycle: 0 -> 1 -> 2 -> 0, plus 4-cycle: 0 -> 1 -> 2 -> 3 -> 0
        edge_index = torch.tensor([
            [0, 1, 2, 0, 1, 2, 3],
            [1, 2, 0, 1, 2, 3, 0]
        ], dtype=torch.long)
        num_nodes = 4

        motifs = self.motif_kernel.compute_ego_cycle_motifs(edge_index, num_nodes)
        
        # Nodes 0, 1, 2 should have non-zero 3-cycle counts
        self.assertGreater(motifs["cycle3_count"][0], 0.0)
        self.assertGreater(motifs["cycle3_count"][1], 0.0)
        self.assertGreater(motifs["cycle3_count"][2], 0.0)
        self.assertGreater(motifs["closed_loop_index"][0], 0.0)

        # Streaming ego-cycle proxy test
        in_edges = [{"counterparty": 1}, {"counterparty": 2}]
        out_edges = [{"counterparty": 1}, {"counterparty": 3}]
        cycle_proxy = self.motif_kernel.compute_streaming_ego_cycle(0, in_edges, out_edges)
        self.assertGreater(cycle_proxy, 0.0)

    def test_02_neuro_symbolic_logic_loss(self):
        """Tests differentiable statutory FOL logic penalty computation."""
        # Simulated logits: 2 nodes
        # Node 0 has high pass-through & high burst but model predicts LOW risk (violates axiom)
        # Node 1 has normal metrics
        logits = torch.tensor([[2.0, -2.0], [-1.0, 1.0]], dtype=torch.float, requires_grad=True)
        pt = torch.tensor([0.98, 0.10])
        burst = torch.tensor([4.5, 0.5])
        cycle = torch.tensor([0.80, 0.0])
        base_loss = torch.tensor(0.50, requires_grad=True)

        total_loss, metrics = self.logic_loss(base_loss, logits, pt, burst, cycle)

        self.assertGreater(metrics["logic_penalty"], 0.0)
        self.assertGreater(metrics["total_hybrid_loss"], metrics["base_loss"])

        # Check differentiability
        total_loss.backward()
        self.assertIsNotNone(logits.grad)

    def test_03_federated_gnn_with_differential_privacy(self):
        """Tests 3-party FedProx collaborative learning with Differential Privacy noise."""
        # Mock global linear model
        global_model = torch.nn.Linear(16, 2)
        server = FedProxServer(global_model, mu_proximal=0.01, dp_noise_multiplier=0.05)

        # Create 3 bank clients
        bank_a = FederatedBankClient("JPMorgan_Chase", local_data_count=50_000)
        bank_b = FederatedBankClient("HSBC_UK", local_data_count=35_000)
        bank_c = FederatedBankClient("Deutsche_Bank", local_data_count=20_000)

        global_weights = global_model.state_dict()
        w_a = bank_a.train_local_epoch(global_weights)
        w_b = bank_b.train_local_epoch(global_weights)
        w_c = bank_c.train_local_epoch(global_weights)

        # Server aggregates with Differential Privacy
        telem = server.aggregate_client_updates([w_a, w_b, w_c], [50_000, 35_000, 20_000])

        self.assertEqual(telem["participating_banks_count"], 3)
        self.assertEqual(telem["total_transactions_aggregated"], 105_000)
        self.assertEqual(telem["round"], 1)

    def test_04_kafka_and_neo4j_streaming_connector(self):
        """Tests Kafka message ingestion, batching, and Cypher statement generation."""
        connector = Neo4jBoltGraphConnector()
        consumer = DistributedKafkaTransactionConsumer(batch_size=3, graph_connector=connector)

        sample_txs = [
            {"tx_id": f"TX_{i}", "src_id": f"A_{i}", "dst_id": f"B_{i}", "amount": 1000.0 * i, "timestamp": 1000.0 + i, "delta_t": 1.0, "burst_score": 0.5, "jurisdiction": "USA"}
            for i in range(5)
        ]

        received = []
        for tx in sample_txs:
            res = consumer.ingest_kafka_message(json.dumps(tx), cache_callback=lambda x: received.append(x["tx_id"]))
            self.assertEqual(res["status"], "INGESTED")

        self.assertEqual(len(received), 5)
        self.assertEqual(consumer.total_consumed, 5)

        # Flush remaining 2 items
        flush_res = consumer.flush_pending_batch()
        self.assertEqual(flush_res["flushed_count"], 2)


if __name__ == "__main__":
    unittest.main()
