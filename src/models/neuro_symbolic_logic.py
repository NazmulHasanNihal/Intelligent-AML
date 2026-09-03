"""
Differentiable Neuro-Symbolic First-Order Logic (FOL) Engine for Intelligent-AML.

Implements differentiable t-norm logic constraints for financial regulatory rules:
- Differentiable Łukasiewicz and Product t-norms (AND, OR, NOT, IMPLIES)
- Enforces statutory Bank Secrecy Act (BSA) & OFAC sanctions logic directly during backprop
- NeuroSymbolicLogicLoss: Penalizes violation of regulatory rules with continuous gradient flow.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple


class LukasiewiczTNorm:
    """Mathematical operations for differentiable Łukasiewicz First-Order Logic."""

    @staticmethod
    def conjunction(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Differentiable AND: T_Luk(a, b) = max(0, a + b - 1)."""
        return torch.clamp(a + b - 1.0, min=0.0, max=1.0)

    @staticmethod
    def disjunction(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Differentiable OR: S_Luk(a, b) = min(1, a + b)."""
        return torch.clamp(a + b, min=0.0, max=1.0)

    @staticmethod
    def negation(a: torch.Tensor) -> torch.Tensor:
        """Differentiable NOT: N_Luk(a) = 1 - a."""
        return 1.0 - a

    @staticmethod
    def implication(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Differentiable IMPLIES: I_Luk(a, b) = min(1, 1 - a + b)."""
        return torch.clamp(1.0 - a + b, min=0.0, max=1.0)

    @staticmethod
    def equivalence(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Differentiable EQUIVALENCE: E_Luk(a, b) = 1 - |a - b|."""
        return 1.0 - torch.abs(a - b)


class DifferentiableAMLRules(nn.Module):
    """
    Evaluates statutory AML rules as differentiable continuous truth values in [0, 1].
    """

    def __init__(self, structuring_threshold: float = 10000.0, burst_threshold: float = 0.70):
        super().__init__()
        self.structuring_threshold = structuring_threshold
        self.burst_threshold = burst_threshold
        self.logic = LukasiewiczTNorm()

    def rule_ofac_sanctions(self, ofac_flag: torch.Tensor, model_pred_suspicious: torch.Tensor) -> torch.Tensor:
        """
        Rule 1: IF OFAC_Sanctioned(u) == 1 THEN Suspicious(u) == 1
        Formula: OFAC(u) -> Pred(u)
        """
        return self.logic.implication(ofac_flag, model_pred_suspicious)

    def rule_smurfing_structuring(
        self,
        transfer_amounts: torch.Tensor,
        burst_scores: torch.Tensor,
        model_pred_suspicious: torch.Tensor
    ) -> torch.Tensor:
        """
        Rule 2: IF ($8,500 <= Amount < $10,000) AND (BurstScore >= 0.70) THEN Suspicious(u) == 1
        """
        # Soft continuous membership for structuring amount ($8.5k - $10k)
        is_sub_threshold = torch.sigmoid((transfer_amounts - 8500.0) / 300.0) * torch.sigmoid((10000.0 - transfer_amounts) / 300.0)
        is_burst = torch.sigmoid((burst_scores - self.burst_threshold) * 10.0)
        
        antecedent = self.logic.conjunction(is_sub_threshold, is_burst)
        return self.logic.implication(antecedent, model_pred_suspicious)

    def rule_wash_cycle_topology(
        self,
        cycle_count: torch.Tensor,
        model_pred_suspicious: torch.Tensor
    ) -> torch.Tensor:
        """
        Rule 3: IF (DirectedCycleCount >= 1) THEN Suspicious(u) == 1
        """
        has_cycle = torch.sigmoid((cycle_count - 0.5) * 5.0)
        return self.logic.implication(has_cycle, model_pred_suspicious)


class NeuroSymbolicLogicLoss(nn.Module):
    """
    Combined Loss Function incorporating Task Classification + Neuro-Symbolic Logic Penalty:
    Loss = Loss_Task + lambda_logic * Loss_FOL
    """

    def __init__(self, primary_loss_fn: nn.Module, logic_weight: float = 0.25):
        super().__init__()
        self.primary_loss_fn = primary_loss_fn
        self.logic_weight = logic_weight
        self.aml_rules = DifferentiableAMLRules()

    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
        ofac_flags: Optional[torch.Tensor] = None,
        amounts: Optional[torch.Tensor] = None,
        burst_scores: Optional[torch.Tensor] = None,
        cycle_counts: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Computes combined primary + differentiable logic loss.
        """
        primary_loss = self.primary_loss_fn(logits, targets)
        pred_probs = F.softmax(logits, dim=1)[:, 1] if logits.dim() > 1 and logits.size(1) > 1 else torch.sigmoid(logits.squeeze())

        rule_satisfactions = []

        # Evaluate OFAC rule
        if ofac_flags is not None:
            sat_ofac = self.aml_rules.rule_ofac_sanctions(ofac_flags.float(), pred_probs)
            rule_satisfactions.append(sat_ofac)

        # Evaluate Smurfing rule
        if amounts is not None and burst_scores is not None:
            sat_smurf = self.aml_rules.rule_smurfing_structuring(amounts.float(), burst_scores.float(), pred_probs)
            rule_satisfactions.append(sat_smurf)

        # Evaluate Cycle rule
        if cycle_counts is not None:
            sat_cycle = self.aml_rules.rule_wash_cycle_topology(cycle_counts.float(), pred_probs)
            rule_satisfactions.append(sat_cycle)

        if rule_satisfactions:
            all_sats = torch.stack(rule_satisfactions, dim=0)
            # Logic violation loss is 1 - truth_value
            logic_loss = torch.mean(1.0 - all_sats)
        else:
            logic_loss = torch.tensor(0.0, device=logits.device)

        total_loss = primary_loss + self.logic_weight * logic_loss

        loss_breakdown = {
            "primary_loss": float(primary_loss.item()),
            "logic_loss": float(logic_loss.item()),
            "total_loss": float(total_loss.item()),
            "avg_rule_satisfaction": float(1.0 - logic_loss.item())
        }

        return total_loss, loss_breakdown
