"""
test_physics_hawkes_sam.py — Unit tests for the Top 3 Algorithmic Innovations:
1. Physics-Informed Financial Mass Conservation Loss (Kirchhoff Law)
2. Sharpness-Aware Minimization (SAM) Optimizer Wrapper
3. Continuous-Time Multivariate Hawkes Process Arrival Intensity Module
"""

import unittest
import math
import torch
import torch.nn as nn
import numpy as np
import polars as pl
import pandas as pd

from src.models.neuro_symbolic_loss import (
    KirchhoffMassConservationLoss,
    NeuroSymbolicAMLLoss,
    PhysicsInformedAMLLoss,
)
from src.models.sam_optimizer import SAMOptimizer
from src.models.hawkes_process import HawkesIntensityEngine, HawkesTemporalEncoder


class TestPhysicsHawkesSAM(unittest.TestCase):
    
    # -------------------------------------------------------------------------
    # 1. Physics-Informed Financial Mass Conservation Tests
    # -------------------------------------------------------------------------
    def test_01_kirchhoff_mass_conservation_loss(self):
        """Tests that Kirchhoff mass conservation loss computes properly and differentiates."""
        criterion = KirchhoffMassConservationLoss(lambda_flow=0.5, tolerance=0.05)
        
        # 4 accounts
        logits = torch.randn(4, 2, requires_grad=True)
        # Account 0: Pass-through mule ($10,000 in, $9,950 out -> pt = 0.995)
        # Account 1: Normal saver ($5,000 in, $500 out -> pt = 0.10)
        # Account 2: High roller ($50,000 in, $49,800 out -> pt = 0.996)
        # Account 3: Normal retail ($200 in, $180 out -> pt = 0.90)
        in_flows = torch.tensor([10000.0, 5000.0, 50000.0, 200.0])
        out_flows = torch.tensor([9950.0, 500.0, 49800.0, 180.0])
        burst_scores = torch.tensor([3.5, 0.2, 4.1, 0.8])
        
        loss, metrics = criterion(logits, in_flows, out_flows, burst_scores)
        self.assertTrue(torch.is_tensor(loss))
        self.assertGreaterEqual(loss.item(), 0.0)
        self.assertIn("kirchhoff_flow_penalty", metrics)
        self.assertIn("mule_conduit_loss", metrics)
        
        # Differentiability check
        loss.backward()
        self.assertIsNotNone(logits.grad)
        self.assertFalse(torch.isnan(logits.grad).any())

    def test_02_physics_informed_master_loss(self):
        """Tests the unified PhysicsInformedAMLLoss module combining FOL logic + Kirchhoff flow."""
        master_loss = PhysicsInformedAMLLoss(lambda_logic=0.4, lambda_kirchhoff=0.3)
        
        logits = torch.randn(6, 2, requires_grad=True)
        base_loss = torch.tensor(0.45, requires_grad=True)
        
        in_flows = torch.tensor([1000.0, 200.0, 5000.0, 100.0, 8000.0, 300.0])
        out_flows = torch.tensor([990.0, 10.0, 4950.0, 20.0, 7920.0, 50.0])
        burst_scores = torch.tensor([2.8, 0.1, 3.2, 0.4, 3.9, 0.5])
        pass_through = torch.tensor([0.99, 0.05, 0.99, 0.20, 0.99, 0.16])
        cycle_scores = torch.tensor([0.8, 0.0, 0.9, 0.0, 0.7, 0.0])
        
        total_loss, metrics = master_loss(
            base_loss=base_loss,
            logits=logits,
            in_flows=in_flows,
            out_flows=out_flows,
            burst_scores=burst_scores,
            pass_through_ratios=pass_through,
            cycle_scores=cycle_scores
        )
        
        self.assertTrue(torch.is_tensor(total_loss))
        self.assertGreater(total_loss.item(), base_loss.item())
        self.assertIn("logic_penalty", metrics)
        self.assertIn("kirchhoff_penalty", metrics)
        self.assertIn("total_physics_loss", metrics)

    # -------------------------------------------------------------------------
    # 2. Sharpness-Aware Minimization (SAM) Optimizer Tests
    # -------------------------------------------------------------------------
    def test_03_sam_optimizer_two_step_update(self):
        """Verifies that SAM optimizer executes first_step perturbation and second_step weight restore/update."""
        linear = nn.Linear(4, 2)
        initial_weight = linear.weight.clone().detach()
        
        optimizer = SAMOptimizer(linear.parameters(), base_optimizer=torch.optim.AdamW, rho=0.05, lr=0.01)
        x = torch.randn(5, 4)
        y = torch.tensor([0, 1, 0, 1, 0], dtype=torch.long)
        criterion = nn.CrossEntropyLoss()
        
        # Step 1: Forward & backward at original weights
        loss1 = criterion(linear(x), y)
        loss1.backward()
        
        # First step climbs to perturbed weights (theta + epsilon)
        optimizer.first_step(zero_grad=True)
        perturbed_weight = linear.weight.clone().detach()
        self.assertFalse(torch.allclose(initial_weight, perturbed_weight))
        
        # Step 2: Forward & backward at perturbed weights
        loss2 = criterion(linear(x), y)
        loss2.backward()
        
        # Second step restores theta and applies optimizer step
        optimizer.second_step(zero_grad=True)
        final_weight = linear.weight.clone().detach()
        
        # Final weights should have moved in the descent direction
        self.assertFalse(torch.allclose(initial_weight, final_weight))

    def test_04_sam_optimizer_closure_step(self):
        """Verifies that SAM optimizer single step() with closure functions correctly."""
        linear = nn.Linear(3, 1)
        optimizer = SAMOptimizer(linear.parameters(), base_optimizer=torch.optim.SGD, rho=0.05, lr=0.1)
        x = torch.randn(4, 3)
        y = torch.randn(4, 1)
        criterion = nn.MSELoss()
        
        def closure():
            optimizer.zero_grad()
            output = linear(x)
            loss = criterion(output, y)
            loss.backward()
            return loss
            
        initial_loss = closure().item()
        optimizer.step(closure)
        post_loss = criterion(linear(x), y).item()
        
        # After optimization step, loss should change
        self.assertNotEqual(initial_loss, post_loss)

    # -------------------------------------------------------------------------
    # 3. Continuous-Time Hawkes Arrival Intensity Tests
    # -------------------------------------------------------------------------
    def test_05_hawkes_intensity_engine(self):
        """Verifies that Hawkes process calculates exact recursive exponential self-excitation on bursts."""
        engine = HawkesIntensityEngine(base_mu=0.01, alpha_self=1.0, beta_decay=0.1)
        
        # Create a burst sequence of transactions for account A
        # Transactions at t=0, t=1, t=2 (rapid burst) vs t=100 (isolated)
        df = pl.DataFrame({
            "src": ["A", "A", "A", "A", "B"],
            "dst": ["M1", "M2", "M3", "M4", "N1"],
            "ts": [0.0, 1.0, 2.0, 100.0, 5.0],
            "amount": [100.0, 200.0, 150.0, 50.0, 300.0]
        })
        
        res = engine.compute_edge_hawkes_intensity(df, time_col="ts", src_col="src", dst_col="dst")
        self.assertIn("hawkes_intensity", res.columns)
        self.assertIn("log_hawkes_intensity", res.columns)
        
        intensities = res["hawkes_intensity"].to_list()
        # During the rapid burst (t=0 -> 1 -> 2), intensity for A must strictly increase
        self.assertGreater(intensities[1], intensities[0])
        self.assertGreater(intensities[2], intensities[1])
        # After 98 seconds of silence at t=100, intensity must decay back down
        self.assertLess(intensities[3], intensities[2])

    def test_06_hawkes_temporal_encoder(self):
        """Verifies that HawkesTemporalEncoder projects intensities into continuous differentiable embeddings."""
        encoder = HawkesTemporalEncoder(out_dim=16, num_components=4)
        
        hawkes_intensity = torch.tensor([0.01, 1.5, 3.8, 0.05])
        delta_t = torch.tensor([0.0, 1.0, 0.5, 95.0])
        
        out = encoder(hawkes_intensity, delta_t)
        self.assertEqual(out.shape, (4, 16))
        
        # Test backward pass
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(encoder.projection[0].weight.grad)


if __name__ == "__main__":
    unittest.main()
