"""
focal_tversky_loss.py — Adaptive Cost-Sensitive Focal Tversky Loss with Financial Exposure Reweighting
and Curriculum Focal Scheduling (Upgrade F).

Provides dynamic, adaptive asymmetric control over False Positives (alpha) vs. False Negatives (beta)
to boost Recall and F1-Score under extreme class imbalance (<0.5% fraud rate),
with logarithmic financial volume penalty weighting, PolyLoss gradient injection, and Curriculum Annealing.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional


class CostSensitiveFocalTverskyLoss(nn.Module):
    """
    Adaptive Cost-Sensitive Poly-Focal Tversky Loss with Dynamic Curriculum Scheduling.
    
    Formula:
        TI = (TP + eps) / (TP + alpha * FP + beta * FN + eps)
        Loss = (1 - TI) ^ gamma_curriculum + eps_poly * (1 - pt) * class_weight
        
    Args:
        alpha: Baseline penalty weight on False Positives (Precision control, default: 0.25).
        beta: Baseline penalty weight on False Negatives (Recall booster, default: 0.75).
        gamma: Focal focusing parameter (default: 1.33).
        gamma_init: Initial focal focusing parameter for curriculum scheduling (default: 2.5).
        label_smoothing: Smoothing factor for target labels (default: 0.02).
        adaptive_imbalance: Automatically scale beta higher if positive ratio < 5% (default: True).
        epsilon_poly: PolyLoss first-order gradient coefficient (default: 0.35).
        eps: Small constant to avoid division by zero (default: 1e-6).
    """
    def __init__(self, alpha: float = 0.25, beta: float = 0.75, gamma: float = 1.33,
                 gamma_init: float = 2.50, label_smoothing: float = 0.02,
                 adaptive_imbalance: bool = True, epsilon_poly: float = 0.35, eps: float = 1e-6):
        super().__init__()
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.gamma_target = float(gamma)
        self.gamma_init = float(gamma_init)
        self.gamma = float(gamma_init)
        self.label_smoothing = float(label_smoothing)
        self.adaptive_imbalance = bool(adaptive_imbalance)
        self.epsilon_poly = float(epsilon_poly)
        self.eps = float(eps)
        self.current_epoch = 1
        self.max_epochs = 50

    def step_curriculum(self, epoch: int, max_epochs: int = 50):
        """
        Curriculum Focal Scheduling:
        Anneals gamma from gamma_init (aggressive recall booster on hard examples)
        down to gamma_target (precision stabilization) over the course of training.
        """
        self.current_epoch = max(1, int(epoch))
        self.max_epochs = max(1, int(max_epochs))
        progress = min(1.0, (self.current_epoch - 1) / max(1, self.max_epochs - 1))
        # Cosine annealing from gamma_init to gamma_target
        cos_decay = 0.5 * (1.0 + torch.cos(torch.tensor(progress * 3.14159265)))
        self.gamma = float(self.gamma_target + (self.gamma_init - self.gamma_target) * cos_decay.item())

    def forward(self, logits: torch.Tensor, targets: torch.Tensor,
                amounts: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward computation of Base-Rate Prior-Adjusted Poly-Focal Tversky Loss.
        
        Args:
            logits: Predicted raw logits [N, 2] or [N].
            targets: Ground truth binary labels [N] (0 = licit, 1 = illicit).
            amounts: Optional financial transaction amounts [N] for dollar-weighted exposure.
            
        Returns:
            Scalar loss tensor.
        """
        targets_raw = targets.float()
        total_samples = float(max(1, targets_raw.numel()))
        pos_samples = float(targets_raw.sum().item())
        pos_ratio = max(1e-5, pos_samples / total_samples)

        if logits.dim() == 2:
            probs = F.softmax(logits, dim=1)[:, 1]
        else:
            probs = torch.sigmoid(logits)

        # Dynamic Imbalance Adaptation: Calibrated beta/alpha balancing
        if self.adaptive_imbalance and pos_ratio < 0.05:
            rarity_factor = float(1.0 - (pos_ratio / 0.05))
            effective_beta = min(0.85, self.beta + 0.10 * rarity_factor)
            effective_alpha = max(0.15, 1.0 - effective_beta)
        else:
            effective_alpha = self.alpha
            effective_beta = self.beta

        # Apply soft label smoothing
        targets_f = targets_raw
        if self.label_smoothing > 0:
            targets_f = targets_f * (1.0 - self.label_smoothing) + 0.5 * self.label_smoothing

        # Financial exposure weighting: higher amount -> higher penalty for misclassification
        if amounts is not None:
            amt_clamped = torch.clamp(amounts.float(), min=0.0)
            weights = 1.0 + torch.log1p(amt_clamped / 1000.0)
            tp = (probs * targets_f * weights).sum()
            fp = (probs * (1.0 - targets_f) * weights).sum()
            fn = ((1.0 - probs) * targets_f * weights).sum()
        else:
            tp = (probs * targets_f).sum()
            fp = (probs * (1.0 - targets_f)).sum()
            fn = ((1.0 - probs) * targets_f).sum()

        tversky_index = (tp + self.eps) / (tp + effective_alpha * fp + effective_beta * fn + self.eps)
        tversky_index = torch.clamp(tversky_index, min=0.0, max=1.0)
        
        focal_tversky = torch.pow(1.0 - tversky_index, self.gamma)

        # Class-Weighted PolyLoss First-Order Gradient Injector:
        # L_poly = L_focal + eps_poly * (1 - pt) * class_weight
        # Guarantees active non-zero gradients even when probabilities saturate
        pt = probs * targets_raw + (1.0 - probs) * (1.0 - targets_raw)
        class_weights = targets_raw * (1.0 / pos_ratio) + (1.0 - targets_raw) * 1.0
        class_weights = torch.clamp(class_weights, max=50.0)
        poly_term = self.epsilon_poly * torch.mean((1.0 - pt) * (class_weights / class_weights.mean()))

        return focal_tversky + poly_term


# Alias for backward and forward compatibility
AdaptiveFocalTverskyLoss = CostSensitiveFocalTverskyLoss
