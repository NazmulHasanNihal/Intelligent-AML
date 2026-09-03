"""
optimal_transport.py — Neural Optimal Transport & Sinkhorn Domain Alignment Engine.
Enables Zero-Shot and Few-Shot Model Transfer across Banking Institutions & Blockchain Corridors.

References:
1. Cuturi. "Sinkhorn Distances: Lightspeed Computation of Optimal Transport" (NeurIPS).
2. Peyré & Cuturi. "Computational Optimal Transport" (Foundations and Trends in ML).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Optional


class SinkhornDomainAligner(nn.Module):
    """
    Entropic Regularized Optimal Transport Aligner (Sinkhorn-Knopp).
    Computes Wasserstein-2 optimal transport distance between source and target
    latent embedding distributions to eliminate cross-bank domain shift.
    """
    def __init__(self, reg_epsilon: float = 0.05, max_iter: int = 100, stop_thresh: float = 1e-4):
        super().__init__()
        self.reg_epsilon = float(reg_epsilon)
        self.max_iter = int(max_iter)
        self.stop_thresh = float(stop_thresh)

    def compute_cost_matrix(self, z_source: torch.Tensor, z_target: torch.Tensor) -> torch.Tensor:
        """
        Computes pairwise squared Euclidean cost matrix:
        C_{ij} = ||z_i^s - z_j^t||_2^2
        """
        # z_source: [Ns, D], z_target: [Nt, D]
        return torch.cdist(z_source, z_target, p=2).pow(2)

    def forward(
        self,
        z_source: torch.Tensor,
        z_target: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes entropic Wasserstein distance and optimal transport plan T*.
        
        Args:
            z_source: Source domain node embeddings [Ns, D]
            z_target: Target domain node embeddings [Nt, D]
        Returns:
            wasserstein_dist: Scalar optimal transport distance
            T: Optimal coupling transport plan matrix [Ns, Nt]
        """
        device = z_source.device
        ns = z_source.size(0)
        nt = z_target.size(0)

        if ns == 0 or nt == 0:
            return torch.tensor(0.0, device=device, requires_grad=True), torch.empty(0, 0, device=device)

        # Uniform empirical probability distributions
        mu = torch.full((ns,), 1.0 / ns, dtype=torch.float32, device=device)
        nu = torch.full((nt,), 1.0 / nt, dtype=torch.float32, device=device)

        # Cost matrix C
        C = self.compute_cost_matrix(z_source, z_target)

        # Kernel matrix K = exp(-C / epsilon) in log space
        log_K = -C / self.reg_epsilon

        # Log-space stabilized Sinkhorn iterations
        u = torch.zeros(ns, dtype=torch.float32, device=device)
        v = torch.zeros(nt, dtype=torch.float32, device=device)

        for _ in range(self.max_iter):
            u_prev = u.clone()
            # u = log(mu) - logsumexp(log_K + v.unsqueeze(0), dim=1)
            u = torch.log(mu + 1e-12) - torch.logsumexp(log_K + v.unsqueeze(0), dim=1)
            # v = log(nu) - logsumexp(log_K + u.unsqueeze(1), dim=0)
            v = torch.log(nu + 1e-12) - torch.logsumexp(log_K + u.unsqueeze(1), dim=0)

            if torch.max(torch.abs(u - u_prev)) < self.stop_thresh:
                break

        # Reconstruct optimal transport coupling: T = exp(u / eps) * K * exp(v / eps)
        log_T = log_K + u.unsqueeze(1) + v.unsqueeze(0)
        T = torch.exp(log_T)

        # Optimal transport distance: <T, C>
        wasserstein_dist = (T * C).sum()

        return wasserstein_dist, T


class EntropicWassersteinLoss(nn.Module):
    """
    Differentiable Neural Optimal Transport Loss for Cross-Institution Domain Alignment.
    Minimizes Wasserstein divergence between two banking jurisdictions or crypto ledgers.
    """
    def __init__(self, reg_epsilon: float = 0.05, loss_weight: float = 0.10):
        super().__init__()
        self.aligner = SinkhornDomainAligner(reg_epsilon=reg_epsilon)
        self.loss_weight = float(loss_weight)

    def forward(self, z_source: torch.Tensor, z_target: torch.Tensor) -> torch.Tensor:
        """Computes weighted Sinkhorn Wasserstein divergence loss."""
        # Subsample for memory efficiency on mega-graphs
        if z_source.size(0) > 1000:
            idx_s = torch.randperm(z_source.size(0))[:1000]
            z_source = z_source[idx_s]
        if z_target.size(0) > 1000:
            idx_t = torch.randperm(z_target.size(0))[:1000]
            z_target = z_target[idx_t]

        w_dist, _ = self.aligner(z_source, z_target)
        return self.loss_weight * w_dist
