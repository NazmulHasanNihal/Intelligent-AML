"""
Hyperbolic Lorentz Space Neural Network Module for Intelligent-AML.

Implements the Lorentz (Hyperboloid) model of hyperbolic space:
- Lorentzian inner product and distance
- Exponential and logarithmic maps at origin
- Parallel transport and tangent space projections
- HyperbolicLorentzConv: GNN layer operating in constant negative curvature (c < 0)
  for distortion-free embedding of scale-free hierarchical laundering trees.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, Dict, List


class LorentzManifold:
    """Mathematical operations on the Lorentz (Hyperboloid) Manifold L^d."""

    def __init__(self, curvature: float = 1.0, eps: float = 1e-6):
        self.c = curvature
        self.eps = eps

    def lorentzian_inner_product(self, u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """Computes Lorentzian inner product: <u, v>_L = -u_0*v_0 + sum_{i=1}^d u_i*v_i."""
        uv = u * v
        time_part = -uv[..., 0:1]
        space_part = torch.sum(uv[..., 1:], dim=-1, keepdim=True)
        return time_part + space_part

    def project_to_manifold(self, x: torch.Tensor) -> torch.Tensor:
        """Projects Euclidean vectors (x_0, x_1..d) onto the Lorentz hyperboloid L^d."""
        space = x[..., 1:]
        sq_norm = torch.sum(space ** 2, dim=-1, keepdim=True)
        time = torch.sqrt(sq_norm + (1.0 / self.c) + self.eps)
        return torch.cat([time, space], dim=-1)

    def exp_map_zero(self, v: torch.Tensor) -> torch.Tensor:
        """Exponential map from tangent space at origin T_0 L^d onto the Lorentz manifold."""
        # v is in R^d (space components). Tangent at origin has v_0 = 0.
        v_norm = torch.norm(v, p=2, dim=-1, keepdim=True).clamp(min=self.eps)
        sqrt_c = math.sqrt(self.c)
        sinh_part = torch.sinh(sqrt_c * v_norm) * (v / (v_norm * sqrt_c))
        # Exact time component derived from space to guarantee -x_0^2 + sum(x_i^2) == -1/c
        sq_norm = torch.sum(sinh_part ** 2, dim=-1, keepdim=True)
        time_part = torch.sqrt(sq_norm + (1.0 / self.c))
        return torch.cat([time_part, sinh_part], dim=-1)

    def log_map_zero(self, x: torch.Tensor) -> torch.Tensor:
        """Logarithmic map from Lorentz manifold L^d to tangent space T_0 L^d (space components)."""
        time = x[..., 0:1]
        space = x[..., 1:]
        dist_origin = torch.acosh((time * math.sqrt(self.c)).clamp(min=1.0 + self.eps))
        sinh_term = torch.sinh(dist_origin).clamp(min=self.eps)
        return (dist_origin / sinh_term) * space

    def hyperbolic_distance(self, u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """Computes geodesic distance between two points on the Lorentz manifold."""
        inner = self.lorentzian_inner_product(u, v)
        c_inner = (-self.c * inner).clamp(min=1.0)
        return (1.0 / math.sqrt(self.c)) * torch.acosh(c_inner)


class HyperbolicLorentzConv(nn.Module):
    """
    Hyperbolic Lorentz Graph Convolutional Layer.
    Aggregates neighborhood messages in tangent space at origin T_0 L^d,
    applies curvature-aware feature transformations, and projects back onto L^d.
    """

    def __init__(self, in_channels: int, out_channels: int, curvature: float = 1.0, dropout: float = 0.1):
        super().__init__()
        self.manifold = LorentzManifold(curvature=curvature)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.curvature = curvature
        
        # Euclidean weights for linear transformation in tangent space (out_channels x in_channels for F.linear)
        self.weight = nn.Parameter(torch.Tensor(out_channels, in_channels))
        self.bias = nn.Parameter(torch.Tensor(out_channels))
        self.dropout = nn.Dropout(dropout)
        
        # Attention scoring parameters for hyperbolic graph aggregation
        self.att_src = nn.Parameter(torch.Tensor(out_channels, 1))
        self.att_dst = nn.Parameter(torch.Tensor(out_channels, 1))
        
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)
        nn.init.xavier_uniform_(self.att_src)
        nn.init.xavier_uniform_(self.att_dst)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Euclidean node features [N, in_channels] or Lorentz embeddings [N, in_channels + 1]
            edge_index: Graph connectivity tensor [2, E]
        Returns:
            Hyperbolic embeddings on Lorentz manifold L^d of shape [N, out_channels + 1]
        """
        # If input is Euclidean, map to tangent space, then project to manifold
        if x.size(-1) == self.in_channels:
            # Transform in Euclidean space first
            x_tangent = F.linear(x, self.weight, self.bias)
            x_tangent = self.dropout(F.relu(x_tangent))
            x_lorentz = self.manifold.exp_map_zero(x_tangent)
        else:
            # Project existing Lorentz features to tangent space at origin
            x_tangent = self.manifold.log_map_zero(x)
            x_tangent = F.linear(x_tangent, self.weight, self.bias)
            x_tangent = self.dropout(F.relu(x_tangent))
            x_lorentz = self.manifold.exp_map_zero(x_tangent)

        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            return x_lorentz

        src, dst = edge_index[0], edge_index[1]
        num_nodes = x_lorentz.size(0)

        # Compute Lorentz-aware hyperbolic attention scores
        # Tangent space representations for linear attention
        h_tangent = self.manifold.log_map_zero(x_lorentz)
        alpha_src = (h_tangent @ self.att_src)[src]
        alpha_dst = (h_tangent @ self.att_dst)[dst]
        edge_att = F.leaky_relu(alpha_src + alpha_dst, negative_slope=0.2)
        
        # Softmax normalization per target node
        edge_att_exp = torch.exp(edge_att - edge_att.max())
        denom = torch.zeros(num_nodes, 1, device=x.device).scatter_add_(0, dst.unsqueeze(1), edge_att_exp) + 1e-6
        edge_weights = edge_att_exp / denom[dst]

        # Aggregate in Tangent Space T_0 L^d (preserving Euclidean vector addition validity)
        weighted_tangent = h_tangent[src] * edge_weights
        agg_tangent = torch.zeros(num_nodes, self.out_channels, device=x.device)
        agg_tangent.index_add_(0, dst, weighted_tangent)

        # Exponential map back onto Lorentz Manifold
        out_lorentz = self.manifold.exp_map_zero(agg_tangent + h_tangent)
        return out_lorentz
