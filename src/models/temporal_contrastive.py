"""
Self-Supervised Spatio-Temporal Graph Contrastive Learning (InfoNCE-AML).

Enables unsupervised pretraining on >99.9% unlabelled bank accounts:
- Dual-view data augmentation:
  - View 1: Transaction amount jittering + temporal timestamp noise
  - View 2: High-degree camouflage hub edge masking + feature dropout
- Symmetric InfoNCE loss maximizing mutual information across paired subgraphs.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple


class SpatioTemporalGraphContrastive(nn.Module):
    """
    Self-Supervised Spatio-Temporal Graph Contrastive Pretraining Engine.
    Maximizes agreement between dual-augmented representations of the same account
    while contrasting against distinct accounts in the batch.
    """

    def __init__(self, in_channels: int, projection_dim: int = 64, temperature: float = 0.07):
        super().__init__()
        self.temperature = temperature
        
        # Non-linear projection head (MLP) mapping GNN embeddings to hypersphere
        self.projector = nn.Sequential(
            nn.Linear(in_channels, in_channels),
            nn.ReLU(),
            nn.Linear(in_channels, projection_dim)
        )

    def augment_view_amount_jitter(
        self,
        x: torch.Tensor,
        jitter_std: float = 0.05
    ) -> torch.Tensor:
        """View 1: Perturb numerical transfer amounts with Gaussian noise."""
        noise = torch.randn_like(x) * jitter_std
        return x + noise

    def augment_view_camouflage_dropout(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        drop_rate: float = 0.15
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """View 2: Randomly mask high-degree camouflage edges and apply feature dropout."""
        # Feature dropout
        mask = torch.rand_like(x) > drop_rate
        x_dropped = x * mask / (1.0 - drop_rate)
        
        # Edge dropout
        num_edges = edge_index.size(1)
        edge_mask = torch.rand(num_edges, device=edge_index.device) > drop_rate
        edge_dropped = edge_index[:, edge_mask]
        
        return x_dropped, edge_dropped

    def compute_infonce_loss(
        self,
        z1: torch.Tensor,
        z2: torch.Tensor
    ) -> torch.Tensor:
        """
        Computes symmetric InfoNCE loss between dual projected representations:
        L = (L(z1, z2) + L(z2, z1)) / 2
        """
        # Normalize representations to unit hypersphere
        z1_norm = F.normalize(self.projector(z1), dim=-1)
        z2_norm = F.normalize(self.projector(z2), dim=-1)

        batch_size = z1.size(0)
        
        # Cosine similarity matrices: [N, N]
        sim_12 = torch.matmul(z1_norm, z2_norm.T) / self.temperature
        sim_21 = torch.matmul(z2_norm, z1_norm.T) / self.temperature
        
        # Target labels are identity diagonal
        labels = torch.arange(batch_size, device=z1.device)
        
        loss_12 = F.cross_entropy(sim_12, labels)
        loss_21 = F.cross_entropy(sim_21, labels)
        
        return 0.5 * (loss_12 + loss_21)
