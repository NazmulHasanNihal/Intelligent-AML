"""
soft_f1_loss.py — Differentiable Soft-F1 and Supervised Contrastive Graph Losses.

Provides direct gradient optimization of the non-differentiable F1 score and
class-conditioned latent manifold clustering under severe class imbalance (<1% minority).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class DifferentiableSoftF1Loss(nn.Module):
    """
    Direct Differentiable F-Beta Optimization Loss.
    
    Instead of approximating cross-entropy surrogates which fail under 99.8% benign imbalance,
    this computes continuous soft approximations of True Positives, False Positives,
    and False Negatives directly through softmax/sigmoid activations:
    
      TP_soft = sum(p_i * y_i)
      FP_soft = sum(p_i * (1 - y_i))
      FN_soft = sum((1 - p_i) * y_i)
      
      Soft_F_beta = (1 + beta^2) * TP_soft / ((1 + beta^2) * TP_soft + beta^2 * FN_soft + FP_soft + eps)
      Loss = 1.0 - Soft_F_beta
    """
    def __init__(self, beta: float = 1.0, eps: float = 1e-6, cost_fp_penalty: float = 1.0):
        super().__init__()
        self.beta = float(beta)
        self.beta_sq = self.beta ** 2
        self.eps = float(eps)
        self.cost_fp_penalty = float(cost_fp_penalty)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Args:
            logits: Predicted logits of shape [N, 2] or [N]
            targets: Binary labels of shape [N] with values in {0, 1}
        """
        if logits.dim() == 2 and logits.shape[1] == 2:
            probs = F.softmax(logits, dim=1)[:, 1]
        elif logits.dim() == 2 and logits.shape[1] == 1:
            probs = torch.sigmoid(logits.squeeze(1))
        else:
            probs = torch.sigmoid(logits)

        # Filter valid targets (y >= 0)
        valid_mask = targets >= 0
        if not valid_mask.any():
            return torch.tensor(0.0, device=logits.device, requires_grad=True)

        p = probs[valid_mask]
        y = targets[valid_mask].float()

        # Continuous soft confusion matrix components
        tp = torch.sum(p * y)
        fp = torch.sum(p * (1.0 - y)) * self.cost_fp_penalty
        fn = torch.sum((1.0 - p) * y)

        # Soft Precision and Recall
        soft_fbeta = ((1.0 + self.beta_sq) * tp + self.eps) / (
            (1.0 + self.beta_sq) * tp + self.beta_sq * fn + fp + self.eps
        )

        return 1.0 - soft_fbeta


class SupConGraphLoss(nn.Module):
    """
    Supervised Contrastive Loss for Graph Node Representations.
    
    Prevents representation collapse in graph neural networks when minority
    money laundering nodes are surrounded by millions of benign neighbors.
    Pulls illicit nodes together in embedding space while repelling licit nodes.
    """
    def __init__(self, temperature: float = 0.07, base_temperature: float = 0.07):
        super().__init__()
        self.temperature = float(temperature)
        self.base_temperature = float(base_temperature)

    def forward(self, features: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """
        Args:
            features: Normalized embeddings of shape [N, hidden_dim]
            labels: Ground truth labels of shape [N]
        """
        device = features.device
        valid_mask = labels >= 0
        if not valid_mask.any():
            return torch.tensor(0.0, device=device, requires_grad=True)

        features = features[valid_mask]
        labels = labels[valid_mask]
        
        # Require at least two samples with positive labels
        pos_mask = labels == 1
        if pos_mask.sum() < 2:
            return torch.tensor(0.0, device=device, requires_grad=True)

        # Normalize features to unit sphere
        features = F.normalize(features, dim=1)
        batch_size = features.shape[0]

        # Anchor subsampling to prevent O(N^2) quadratic VRAM explosion on large graphs (>2000 nodes)
        # Keeps memory under 16 MB while preserving contrastive clustering gradients for fraud rings
        if batch_size > 2048:
            pos_idx = torch.where(labels == 1)[0]
            neg_idx = torch.where(labels == 0)[0]
            
            n_pos = min(len(pos_idx), 1024)
            n_neg = min(len(neg_idx), 2048 - n_pos)
            
            p_sub = pos_idx[torch.randperm(len(pos_idx), device=device)[:n_pos]]
            n_sub = neg_idx[torch.randperm(len(neg_idx), device=device)[:n_neg]]
            sub_idx = torch.cat([p_sub, n_sub])
            
            features = features[sub_idx]
            labels = labels[sub_idx]
            batch_size = features.shape[0]

        # Pairwise mask: 1 if labels[i] == labels[j], 0 otherwise
        labels_mat = labels.contiguous().view(-1, 1)
        mask = torch.eq(labels_mat, labels_mat.T).float().to(device)

        # Compute cosine similarity logits
        anchor_dot_contrast = torch.div(
            torch.matmul(features, features.T),
            self.temperature
        )
        
        # Numerical stability: subtract max per row
        logits_max, _ = torch.max(anchor_dot_contrast, dim=1, keepdim=True)
        logits = anchor_dot_contrast - logits_max.detach()

        # Mask out self-contrast
        logits_mask = torch.scatter(
            torch.ones_like(mask),
            1,
            torch.arange(batch_size, device=device).view(-1, 1),
            0
        )
        mask = mask * logits_mask

        # Compute log-probabilities
        exp_logits = torch.exp(logits) * logits_mask
        log_prob = logits - torch.log(exp_logits.sum(1, keepdim=True) + 1e-6)

        # Compute mean of log-likelihood over positive pairs
        mean_log_prob_pos = (mask * log_prob).sum(1) / (mask.sum(1) + 1e-6)

        # Loss
        loss = - (self.temperature / self.base_temperature) * mean_log_prob_pos
        loss = loss.view(1, batch_size).mean()

        return loss


class CompositeAMLObjective(nn.Module):
    """
    Unified Multi-Objective Loss for Asymmetric Class-Imbalanced Graph Learning:
      L_total = L_focal_tversky + lambda_f1 * L_soft_f1 + lambda_con * L_supcon
    """
    def __init__(self, focal_tversky_loss, soft_f1_weight: float = 0.50, supcon_weight: float = 0.10):
        super().__init__()
        self.focal_tversky = focal_tversky_loss
        self.soft_f1 = DifferentiableSoftF1Loss(beta=1.0)
        self.supcon = SupConGraphLoss(temperature=0.07)
        self.soft_f1_weight = float(soft_f1_weight)
        self.supcon_weight = float(supcon_weight)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor, embeddings: torch.Tensor = None) -> torch.Tensor:
        l_base = self.focal_tversky(logits, targets) if self.focal_tversky is not None else F.cross_entropy(logits, targets)
        l_f1 = self.soft_f1(logits, targets)
        
        total_loss = l_base + self.soft_f1_weight * l_f1
        
        if embeddings is not None and self.supcon_weight > 0.0:
            l_con = self.supcon(embeddings, targets)
            total_loss = total_loss + self.supcon_weight * l_con
            
        return total_loss
