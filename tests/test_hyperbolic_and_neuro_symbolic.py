"""
Unit and Integration Tests for Master Research Innovations:
1. Hyperbolic Lorentz Space GNN Layers
2. Causal Counterfactual Forensic Explainer
3. Differentiable Neuro-Symbolic First-Order Logic (FOL)
4. Zero-Knowledge Sanctions & Compliance Proof Protocol
"""

import pytest
import torch
import torch.nn as nn
from src.models.hyperbolic import LorentzManifold, HyperbolicLorentzConv
from src.utils.counterfactual import CounterfactualForensicExplainer
from src.models.neuro_symbolic_logic import LukasiewiczTNorm, DifferentiableAMLRules, NeuroSymbolicLogicLoss
from src.utils.zk_compliance import MerkleSanctionsTree, ZKComplianceProofSystem


class TestHyperbolicLorentzSpace:
    """Test suite for Lorentz Hyperbolic Manifold and Convolutional Layers."""

    def test_01_lorentz_manifold_projections(self):
        manifold = LorentzManifold(curvature=1.0)
        # Create random Euclidean vectors in R^4
        x = torch.randn(10, 4)
        x_lorentz = manifold.project_to_manifold(x)
        
        # Verify Lorentz constraint: -x_0^2 + sum(x_i^2) = -1/c
        time_part = x_lorentz[:, 0]
        space_part = x_lorentz[:, 1:]
        lorentz_sq = -time_part ** 2 + torch.sum(space_part ** 2, dim=-1)
        
        expected = -torch.ones_like(lorentz_sq)
        assert torch.allclose(lorentz_sq, expected, atol=1e-4)

    def test_02_exp_log_map_invertibility(self):
        manifold = LorentzManifold(curvature=1.0)
        # Tangent vector at origin
        v_tangent = torch.randn(8, 5) * 0.5
        
        # Exp map to manifold, then log map back to tangent space
        x_lorentz = manifold.exp_map_zero(v_tangent)
        v_recovered = manifold.log_map_zero(x_lorentz)
        
        assert torch.allclose(v_tangent, v_recovered, atol=1e-4)

    def test_03_hyperbolic_distance_positivity(self):
        manifold = LorentzManifold(curvature=1.0)
        u_tangent = torch.randn(5, 4)
        v_tangent = torch.randn(5, 4)
        
        u = manifold.exp_map_zero(u_tangent)
        v = manifold.exp_map_zero(v_tangent)
        
        dist = manifold.hyperbolic_distance(u, v)
        assert torch.all(dist >= 0.0)
        # Distance from self is zero within float32 numerical tolerance
        dist_self = manifold.hyperbolic_distance(u, u)
        assert torch.allclose(dist_self, torch.zeros_like(dist_self), atol=1e-2)

    def test_04_hyperbolic_lorentz_conv_forward_and_backward(self):
        in_dim, out_dim = 16, 8
        conv = HyperbolicLorentzConv(in_channels=in_dim, out_channels=out_dim, curvature=1.0)
        
        num_nodes = 20
        x = torch.randn(num_nodes, in_dim, requires_grad=True)
        # Random edge index
        edge_index = torch.randint(0, num_nodes, (2, 40))
        
        out = conv(x, edge_index)
        assert out.shape == (num_nodes, out_dim + 1)
        
        loss = out.sum()
        loss.backward()
        assert x.grad is not None


class TestCounterfactualExplainer:
    """Test suite for Causal Counterfactual Explanations."""

    def test_01_structuring_counterfactual_generation(self):
        explainer = CounterfactualForensicExplainer(safe_threshold=0.40)
        
        result = explainer.explain_transaction(
            target_account="ACC_42",
            counterparty="ACC_105",
            transfer_amount=9850.0,
            initial_risk_score=0.945,
            burst_score=0.88,
            triggered_rules=["RULE_BSA_STRUCTURING_SINGLE"],
            temporal_delta_hours=0.25
        )
        
        assert result["status"] == "COUNTERFACTUAL_GENERATED"
        assert result["is_counterfactual_found"] is True
        assert result["counterfactual_risk_score"] < result["initial_risk_score"]
        assert len(result["causal_deltas"]) >= 1
        assert "31 U.S.C. 5324" in result["forensic_narrative"]

    def test_02_cleared_account_no_perturbation(self):
        explainer = CounterfactualForensicExplainer(safe_threshold=0.40)
        result = explainer.explain_transaction(
            target_account="ACC_LEGIT",
            counterparty="ACC_MERCHANT",
            transfer_amount=120.0,
            initial_risk_score=0.08,
            burst_score=0.10,
            triggered_rules=[],
            temporal_delta_hours=48.0
        )
        assert result["status"] == "CLEARED"
        assert len(result["causal_deltas"]) == 0


class TestNeuroSymbolicLogic:
    """Test suite for Differentiable First-Order Logic & Regulatory Constraints."""

    def test_01_lukasiewicz_t_norm_properties(self):
        logic = LukasiewiczTNorm()
        a = torch.tensor([0.8, 0.2, 1.0, 0.0])
        b = torch.tensor([0.7, 0.9, 0.5, 0.5])
        
        conj = logic.conjunction(a, b)
        disj = logic.disjunction(a, b)
        impl = logic.implication(a, b)
        
        # a=1, b=0.5 -> conj=0.5, disj=1.0, impl=0.5
        assert torch.isclose(conj[2], torch.tensor(0.5))
        assert torch.isclose(disj[2], torch.tensor(1.0))
        assert torch.isclose(impl[2], torch.tensor(0.5))

    def test_02_neuro_symbolic_loss_gradient_flow(self):
        primary_loss = nn.CrossEntropyLoss()
        combined_loss_fn = NeuroSymbolicLogicLoss(primary_loss, logic_weight=0.30)
        
        num_samples = 10
        logits = torch.randn(num_samples, 2, requires_grad=True)
        targets = torch.randint(0, 2, (num_samples,))
        ofac_flags = torch.tensor([1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
        amounts = torch.tensor([9500.0, 200.0, 9900.0, 50.0, 100.0, 9800.0, 500.0, 40.0, 80.0, 90.0])
        burst_scores = torch.tensor([0.9, 0.1, 0.85, 0.05, 0.1, 0.95, 0.2, 0.1, 0.05, 0.1])
        cycle_counts = torch.tensor([1.0, 0.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
        
        loss, breakdown = combined_loss_fn(logits, targets, ofac_flags, amounts, burst_scores, cycle_counts)
        assert loss.item() > 0.0
        assert "logic_loss" in breakdown
        assert "avg_rule_satisfaction" in breakdown
        
        loss.backward()
        assert logits.grad is not None


class TestZKComplianceProtocol:
    """Test suite for Zero-Knowledge Compliance Proofs."""

    def test_01_merkle_tree_root_determinism(self):
        entries = ["OFAC_SANCTION_A", "OFAC_SANCTION_B", "OFAC_SANCTION_C"]
        tree1 = MerkleSanctionsTree(entries)
        tree2 = MerkleSanctionsTree(entries)
        assert tree1.get_root() == tree2.get_root()

    def test_02_zk_proof_generation_and_verification(self):
        zk_system = ZKComplianceProofSystem()
        
        # Generate valid compliant transaction proof
        proof = zk_system.generate_zk_proof(
            sender_account="CLEAN_USER_001",
            recipient_account="CLEAN_USER_002",
            transfer_amount=5400.0,
            structuring_limit=10000.0
        )
        
        is_valid, msg = zk_system.verify_zk_proof(proof)
        assert is_valid is True
        assert msg == "VERIFIED_COMPLIANT_ZERO_KNOWLEDGE"

    def test_03_zk_proof_rejects_sanctioned_entity(self):
        zk_system = ZKComplianceProofSystem()
        # Generate proof with a sanctioned account name
        proof = zk_system.generate_zk_proof(
            sender_account="OFAC_SANCTION_001",
            recipient_account="CLEAN_USER_002",
            transfer_amount=500.0
        )
        
        is_valid, msg = zk_system.verify_zk_proof(proof)
        assert is_valid is False
        assert msg == "STATUTORY_RULE_VIOLATION_DETECTED"
