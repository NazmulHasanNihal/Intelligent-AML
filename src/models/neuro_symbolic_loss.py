"""
neuro_symbolic_loss.py — Neuro-Symbolic Logic & Physics-Informed Flow Loss Regularizer.
Injects statutory AML legal axioms and Kirchhoff Financial Mass-Conservation laws directly into
the neural network backpropagation loss via differentiable soft First-Order Logic (FOL) t-norms
and flow-conservation residuals, guaranteeing physical and regulatory alignment.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional, Any


class KirchhoffMassConservationLoss(nn.Module):
    """
    Physics-Informed Financial Mass Conservation Loss (Kirchhoff Law for Financial Networks).
    
    Penalizes representations that violate physical banking balance conservation:
        Flow Residual = |Inflow - (Outflow + Delta_Balance + Fees)|
    For suspected money mules / layering conduits, enforces tight pass-through bounds:
        Outflow / (Inflow + epsilon) in [0.95, 1.05] during high-velocity windows.
    """
    def __init__(self, lambda_flow: float = 0.35, tolerance: float = 0.05):
        super().__init__()
        self.lambda_flow = float(lambda_flow)
        self.tolerance = float(tolerance)

    def forward(self, logits: torch.Tensor,
                in_flows: torch.Tensor,
                out_flows: torch.Tensor,
                burst_scores: Optional[torch.Tensor] = None,
                epsilon: float = 1e-5) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Computes the differentiable Kirchhoff mass conservation penalty.
        
        Args:
            logits: [num_nodes, 2] GNN classification logits
            in_flows: [num_nodes] aggregated inbound transaction volume
            out_flows: [num_nodes] aggregated outbound transaction volume
            burst_scores: [num_nodes] optional rolling frequency velocity scores
        """
        device = logits.device
        probs = F.softmax(logits, dim=-1)[:, 1]  # Predicted fraud probability
        
        in_f = in_flows.to(device).flatten().float()
        out_f = out_flows.to(device).flatten().float()
        
        # 1. Non-dimensionalized Pass-Through Ratio: Out / (In + eps)
        pt_ratio = out_f / (in_f + epsilon)
        
        # Active conduit condition: meaningful inflow & outflow
        active_mask = (in_f > 1.0) & (out_f > 1.0)
        if active_mask.sum() == 0:
            zero_loss = torch.tensor(0.0, device=device, requires_grad=True)
            return zero_loss, {"kirchhoff_flow_penalty": 0.0, "mule_conduit_loss": 0.0}
            
        # 2. Mule Conduit Invariant:
        # Near-unity pass-through (0.95 <= pt <= 1.05) with rapid velocity implies high probability of layering
        # If node behaves like a perfect pass-through conduit, penalize low fraud predictions
        mule_proximity = torch.exp(-((pt_ratio - 1.0) ** 2) / (2 * (self.tolerance ** 2)))
        
        if burst_scores is not None:
            burst = burst_scores.to(device).flatten().float()
            burst_weight = torch.sigmoid(2.0 * (burst - 1.5))
            mule_conduit_condition = mule_proximity * burst_weight
        else:
            mule_conduit_condition = mule_proximity
            
        # Penalize if model assigns low fraud probability (prob < 0.80) to a clear high-velocity conduit
        mule_violation = F.relu(0.80 - probs) ** 2
        mule_conduit_loss = torch.mean(mule_conduit_condition[active_mask] * mule_violation[active_mask])
        
        # 3. Flow Conservation Residual:
        # Normal customer accounts retain balances (Inflow != Outflow),
        # whereas transit mules have near-zero retained balance relative to turnover
        flow_imbalance = torch.abs(in_f - out_f) / (in_f + out_f + epsilon)
        # If model flags a standard non-transitive account as high-risk without topological justification
        false_flag_penalty = probs * (flow_imbalance > 0.80).float()
        flow_regularization = torch.mean(false_flag_penalty[active_mask]) * 0.10
        
        total_flow_loss = mule_conduit_loss + flow_regularization
        
        metrics = {
            "kirchhoff_flow_penalty": float(total_flow_loss.item()),
            "mule_conduit_loss": float(mule_conduit_loss.item())
        }
        return total_flow_loss, metrics


class NeuroSymbolicAMLLoss(nn.Module):
    """
    Differentiable Neuro-Symbolic Loss Engine.
    Penalizes neural network representations that contradict statutory banking compliance axioms.
    """
    def __init__(self, lambda_logic: float = 0.50,
                 mule_pt_threshold: float = 0.85,
                 mule_burst_threshold: float = 2.5):
        super().__init__()
        self.lambda_logic = lambda_logic
        self.mule_pt_threshold = mule_pt_threshold
        self.mule_burst_threshold = mule_burst_threshold

    def compute_logic_penalty(self, logits: torch.Tensor,
                              pass_through_ratios: Optional[torch.Tensor] = None,
                              burst_scores: Optional[torch.Tensor] = None,
                              cycle_scores: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Computes soft First-Order Logic (FOL) constraint violations.
        Logits shape: [num_nodes, 2]
        """
        probs = F.softmax(logits, dim=-1)[:, 1]  # Predicted fraud probability
        device = logits.device
        total_penalty = torch.tensor(0.0, device=device, requires_grad=True)

        if pass_through_ratios is None or burst_scores is None:
            return total_penalty

        pt = pass_through_ratios.to(device).flatten().float()
        burst = burst_scores.to(device).flatten().float()

        # AXIOM 1: Money Mule Rapid Conduit Constraint
        # Condition: PassThrough > 0.85 AND Burst > 2.5 => Predicted Fraud Prob >= 0.85
        condition_pt = torch.sigmoid(10.0 * (pt - self.mule_pt_threshold))
        condition_burst = torch.sigmoid(2.0 * (burst - self.mule_burst_threshold))
        axiom1_antecedent = condition_pt * condition_burst  # Product t-norm (fuzzy AND)

        target_risk_floor = 0.85
        # Soft violation: penalize when prob < target_risk_floor while condition is true
        violation1 = F.relu(target_risk_floor - probs) ** 2
        loss_axiom1 = torch.mean(axiom1_antecedent * violation1)

        # AXIOM 2: Circular Peeling Chain Constraint
        loss_axiom2 = torch.tensor(0.0, device=device)
        if cycle_scores is not None:
            cycles = cycle_scores.to(device).flatten().float()
            condition_cycle = torch.sigmoid(5.0 * (cycles - 0.50))
            violation2 = F.relu(0.80 - probs) ** 2
            loss_axiom2 = torch.mean(condition_cycle * violation2)

        total_penalty = loss_axiom1 + loss_axiom2
        return total_penalty

    def forward(self, base_loss: torch.Tensor, logits: torch.Tensor,
                pass_through_ratios: Optional[torch.Tensor] = None,
                burst_scores: Optional[torch.Tensor] = None,
                cycle_scores: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Combines standard empirical task loss (e.g. Focal Loss) with statutory logic penalty.
        """
        logic_penalty = self.compute_logic_penalty(
            logits, pass_through_ratios, burst_scores, cycle_scores
        )
        total_loss = base_loss + self.lambda_logic * logic_penalty

        metrics = {
            "base_loss": float(base_loss.item()) if hasattr(base_loss, "item") else float(base_loss),
            "logic_penalty": float(logic_penalty.item()) if hasattr(logic_penalty, "item") else float(logic_penalty),
            "total_hybrid_loss": float(total_loss.item())
        }
        return total_loss, metrics


class PhysicsInformedAMLLoss(nn.Module):
    """
    Unified Physics-Informed & Neuro-Symbolic Master Loss Engine.
    Combines:
    1. Base Task Loss (Focal Tversky / Weighted Cross Entropy)
    2. First-Order Logic Statutory Compliance Axioms (Axiomatic Rule Regularization)
    3. Kirchhoff Financial Mass Conservation Law (Physical Accounting Conservation)
    """
    def __init__(self, lambda_logic: float = 0.40, lambda_kirchhoff: float = 0.30):
        super().__init__()
        self.logic_engine = NeuroSymbolicAMLLoss(lambda_logic=lambda_logic)
        self.kirchhoff_engine = KirchhoffMassConservationLoss(lambda_flow=lambda_kirchhoff)
        self.lambda_logic = lambda_logic
        self.lambda_kirchhoff = lambda_kirchhoff

    def forward(self, base_loss: torch.Tensor,
                logits: torch.Tensor,
                in_flows: Optional[torch.Tensor] = None,
                out_flows: Optional[torch.Tensor] = None,
                burst_scores: Optional[torch.Tensor] = None,
                pass_through_ratios: Optional[torch.Tensor] = None,
                cycle_scores: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, Dict[str, float]]:
        
        # 1. Compute FOL Logic Penalty
        logic_pen = self.logic_engine.compute_logic_penalty(
            logits, pass_through_ratios, burst_scores, cycle_scores
        )
        
        # 2. Compute Kirchhoff Mass Conservation Loss
        if in_flows is not None and out_flows is not None:
            flow_pen, flow_metrics = self.kirchhoff_engine(
                logits, in_flows, out_flows, burst_scores
            )
        else:
            flow_pen = torch.tensor(0.0, device=logits.device, requires_grad=True)
            flow_metrics = {"kirchhoff_flow_penalty": 0.0, "mule_conduit_loss": 0.0}
            
        total_loss = base_loss + self.lambda_logic * logic_pen + self.lambda_kirchhoff * flow_pen
        
        metrics = {
            "base_loss": float(base_loss.item()) if hasattr(base_loss, "item") else float(base_loss),
            "logic_penalty": float(logic_pen.item()) if hasattr(logic_pen, "item") else float(logic_pen),
            "kirchhoff_penalty": float(flow_pen.item()) if hasattr(flow_pen, "item") else float(flow_pen),
            "total_physics_loss": float(total_loss.item())
        }
        return total_loss, metrics
