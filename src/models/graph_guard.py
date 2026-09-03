"""
graph_guard.py — Adversarial Graph Purifier & Dynamic Homophily Denoising Engine.
Defends against Adversarial Camouflage, Smurfing Chaff Injection, and Homophily Dilution.

Reference:
1. Zhu et al. "GraphGuard: Defending Graph Neural Networks against Adversarial Attacks via Purifying Disturbed Homophily" (IEEE TKDE).
2. Chen et al. "Understanding Structural Vulnerability in GNNs" (KDD).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import scipy.sparse as sp
from typing import Tuple, Dict, Optional, Union


class HomophilyDenoisingGate(nn.Module):
    """
    Parametric Neural Gate for Dynamic Adversarial Edge Pruning.
    Predicts the authenticity score of graph edges:
    s_{uv} = sigmoid(W [h_u * h_v || |h_u - h_v| || cos_sim(h_u, h_v)] + b)
    """
    def __init__(self, in_channels: int, hidden_dim: int = 32):
        super().__init__()
        self.proj = nn.Sequential(
            nn.Linear(in_channels * 2 + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        self.threshold = 0.50

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Node feature/embedding matrix [N, in_channels]
            edge_index: Graph linkages [2, E]
        Returns:
            edge_scores: Probability that each edge is a legitimate structural link [E]
        """
        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            return torch.empty(0, device=x.device)

        src, dst = edge_index[0], edge_index[1]
        h_src, h_dst = x[src], x[dst]

        # 1. Hadamard product interaction
        hadamard = h_src * h_dst

        # 2. Absolute difference
        diff = torch.abs(h_src - h_dst)

        # 3. Normalized Cosine similarity
        h_src_norm = F.normalize(h_src, p=2, dim=-1)
        h_dst_norm = F.normalize(h_dst, p=2, dim=-1)
        cos_sim = (h_src_norm * h_dst_norm).sum(dim=-1, keepdim=True)

        # Concatenate edge representation
        edge_feats = torch.cat([hadamard, diff, cos_sim], dim=-1)
        logits = self.proj(edge_feats).view(-1)
        return torch.sigmoid(logits)


class AdversarialGraphGuard(nn.Module):
    """
    Master Adversarial Graph Purification & Denoising Engine.
    Detects and purges synthetic camouflage edges injected by sophisticated money launderers
    to avoid detection by Graph Attention and message passing layers.
    """
    def __init__(self, in_channels: int, prune_threshold: float = 0.35, max_drop_ratio: float = 0.40):
        super().__init__()
        self.in_channels = in_channels
        self.prune_threshold = float(prune_threshold)
        self.max_drop_ratio = float(max_drop_ratio)
        self.gate = HomophilyDenoisingGate(in_channels)

    def compute_jaccard_homophily(self, edge_index: torch.Tensor, num_nodes: int) -> torch.Tensor:
        """
        Computes the 1-hop topological Jaccard neighbor overlap for every edge:
        J(u, v) = |N(u) ∩ N(v)| / (|N(u) ∪ N(v)| + eps)
        """
        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            return torch.empty(0, device=edge_index.device)

        src_np = edge_index[0].detach().cpu().numpy()
        dst_np = edge_index[1].detach().cpu().numpy()
        
        # Build binary symmetric adjacency
        data = np.ones(len(src_np), dtype=np.float32)
        adj = sp.csr_matrix((data, (src_np, dst_np)), shape=(num_nodes, num_nodes))
        adj_sym = (adj + adj.T).astype(bool).astype(np.float32)

        # Common neighbors: (A * A)_{uv}
        adj2 = adj_sym.dot(adj_sym)
        
        deg = np.asarray(adj_sym.sum(axis=1)).flatten()
        
        jaccard_scores = []
        for u, v in zip(src_np, dst_np):
            common = adj2[u, v]
            union = deg[u] + deg[v] - common
            jaccard = common / max(1.0, union)
            jaccard_scores.append(jaccard)
            
        return torch.tensor(jaccard_scores, dtype=torch.float32, device=edge_index.device)

    def purify_graph(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        edge_attr: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Dict[str, float]]:
        """
        Filters adversarial camouflage edges, returning purified graph connectivity.
        
        Args:
            x: Node feature matrix [N, D]
            edge_index: Original edge index [2, E]
            edge_attr: Optional edge attributes [E, ...]
        Returns:
            purified_edge_index: Denoised edge index [2, E_clean]
            purified_edge_attr: Filtered edge attributes [E_clean, ...]
            stats: Denoising statistics dictionary
        """
        num_edges = edge_index.size(1) if (edge_index is not None and edge_index.numel() > 0) else 0
        if num_edges == 0:
            return edge_index, edge_attr, {"original_edges": 0, "pruned_edges": 0, "drop_rate": 0.0}

        with torch.no_grad():
            edge_scores = self.gate(x, edge_index)  # [E]
            
            # Keep edges with score >= prune_threshold
            keep_mask = edge_scores >= self.prune_threshold
            
            num_kept = keep_mask.sum().item()
            drop_ratio = 1.0 - (num_kept / num_edges)
            
            # Safety clamp: do not drop more than max_drop_ratio to prevent graph fragmentation
            if drop_ratio > self.max_drop_ratio:
                k = int(num_edges * (1.0 - self.max_drop_ratio))
                top_indices = torch.topk(edge_scores, k=k).indices
                keep_mask = torch.zeros(num_edges, dtype=torch.bool, device=edge_index.device)
                keep_mask[top_indices] = True
                num_kept = k

        purified_edge_index = edge_index[:, keep_mask]
        purified_edge_attr = edge_attr[keep_mask] if edge_attr is not None else None

        stats = {
            "original_edges": num_edges,
            "purified_edges": num_kept,
            "pruned_edges": num_edges - num_kept,
            "drop_rate": float(1.0 - (num_kept / max(1, num_edges)))
        }

        return purified_edge_index, purified_edge_attr, stats
