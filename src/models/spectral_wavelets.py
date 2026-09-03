"""
Spectral Graph Wavelet Neural Convolution (SGWC) for Intelligent-AML.

Decomposes graph signals into multiscale spatial-frequency domains:
- Computes normalized graph Laplacian: L = I - D^(-1/2) A D^(-1/2)
- Fast Chebyshev polynomial recurrence: T_0(x)=1, T_1(x)=x, T_k(x)=2x T_{k-1}(x) - T_{k-2}(x)
- High-frequency wavelets isolate micro-smurfing wash cycles
- Low-frequency scaling functions isolate macro commercial cash flows.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List


class SpectralGraphWaveletConv(nn.Module):
    """
    Multiscale Spectral Graph Wavelet Convolution Layer.
    Uses K-th order Chebyshev polynomial expansions to filter localized spatial frequencies.
    """

    def __init__(self, in_channels: int, out_channels: int, K: int = 3, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.K = K
        
        # Chebyshev filter coefficients: K filters for multiscale frequency bands
        self.chebyshev_weights = nn.Parameter(torch.Tensor(K, in_channels, out_channels))
        self.bias = nn.Parameter(torch.Tensor(out_channels))
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(out_channels)
        
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.chebyshev_weights)
        nn.init.zeros_(self.bias)

    def _compute_scaled_laplacian(
        self,
        edge_index: torch.Tensor,
        num_nodes: int,
        device: torch.device
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the symmetrically normalized Graph Laplacian:
        L = I - D^(-1/2) A D^(-1/2), scaled to [-1, 1] for stable Chebyshev recurrence:
        L_tilde = (2/lambda_max) * L - I (with lambda_max ≈ 2.0 -> L_tilde = L - I = -D^(-1/2) A D^(-1/2))
        """
        src, dst = edge_index[0], edge_index[1]
        deg = torch.zeros(num_nodes, device=device).scatter_add_(0, src, torch.ones_like(src, dtype=torch.float32))
        deg_inv_sqrt = torch.pow(deg.clamp(min=1.0), -0.5)
        
        # Normalized adjacency values: D^(-1/2) A D^(-1/2)
        norm_values = deg_inv_sqrt[src] * deg_inv_sqrt[dst]
        return edge_index, norm_values

    def _laplacian_spmm(
        self,
        edge_index: torch.Tensor,
        norm_values: torch.Tensor,
        x: torch.Tensor,
        num_nodes: int
    ) -> torch.Tensor:
        """Sparse Matrix-Dense Matrix multiplication for Normalized Adjacency."""
        src, dst = edge_index[0], edge_index[1]
        weighted_x = x[src] * norm_values.unsqueeze(-1)
        out = torch.zeros(num_nodes, x.size(1), device=x.device)
        out.index_add_(0, dst, weighted_x)
        return out

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Node feature matrix [N, in_channels]
            edge_index: Graph connectivity tensor [2, E]
        Returns:
            Multiscale spectral wavelet representations [N, out_channels]
        """
        num_nodes = x.size(0)
        
        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            out = torch.matmul(x, self.chebyshev_weights[0]) + self.bias
            return self.norm(F.relu(out))

        edge_index, norm_values = self._compute_scaled_laplacian(edge_index, num_nodes, x.device)

        # Chebyshev Polynomial Recurrence:
        # T_0(x) = x
        # T_1(x) = L_tilde * x
        # T_k(x) = 2 * L_tilde * T_{k-1}(x) - T_{k-2}(x)
        
        # T_0: Identity pass (Low-frequency scaling)
        T_0 = x
        out = torch.matmul(T_0, self.chebyshev_weights[0])

        if self.K > 1:
            # T_1: 1-hop normalized spatial difference (Mid-frequency wavelets)
            # L_tilde * x = norm_A * x - x
            A_norm_x = self._laplacian_spmm(edge_index, norm_values, x, num_nodes)
            T_1 = A_norm_x - x
            out = out + torch.matmul(T_1, self.chebyshev_weights[1])

            T_prev2 = T_0
            T_prev1 = T_1

            for k in range(2, self.K):
                # T_k = 2 * L_tilde * T_{k-1} - T_{k-2}
                A_norm_prev = self._laplacian_spmm(edge_index, norm_values, T_prev1, num_nodes)
                L_tilde_prev = A_norm_prev - T_prev1
                T_k = 2.0 * L_tilde_prev - T_prev2
                
                out = out + torch.matmul(T_k, self.chebyshev_weights[k])
                T_prev2 = T_prev1
                T_prev1 = T_k

        out = out + self.bias
        out = self.norm(self.dropout(F.relu(out)))
        return out


class ChebyshevSpectralWaveletEngine:
    """
    High-Throughput Non-Parametric Chebyshev Graph Wavelet Feature Extractor.
    Extracts 4 multiscale spectral diffusion bands directly from graph topology:
    - Band 0: Low-Frequency Scaling Signal (x)
    - Band 1: Band-Pass Local Gradient (L_tilde x)
    - Band 2: High-Frequency Ring Harmonic ((2 L_tilde^2 - I) x)
    - Band 3: Multi-Hop Macro Cartel Wavelet ((4 L_tilde^3 - 3 L_tilde) x)
    """
    def __init__(self, K: int = 4):
        self.K = K

    def extract_wavelet_bands(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor
    ) -> torch.Tensor:
        """
        Computes multiscale spectral wavelet bands in O(|E|) sparse matrix operations.
        Returns: [N, in_channels * K]
        """
        num_nodes = x.size(0)
        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            return x.repeat(1, self.K)

        src, dst = edge_index[0], edge_index[1]
        deg = torch.zeros(num_nodes, device=x.device).scatter_add_(0, src, torch.ones_like(src, dtype=torch.float32))
        deg_inv_sqrt = torch.pow(deg.clamp(min=1.0), -0.5)
        norm_values = deg_inv_sqrt[src] * deg_inv_sqrt[dst]

        def spmm(in_x: torch.Tensor) -> torch.Tensor:
            weighted = in_x[src] * norm_values.unsqueeze(-1)
            res = torch.zeros(num_nodes, in_x.size(1), device=in_x.device)
            res.index_add_(0, dst, weighted)
            return res

        bands = [x]  # T_0
        if self.K > 1:
            # T_1 = A_norm * x - x
            T_1 = spmm(x) - x
            bands.append(T_1)
            
            T_prev2 = x
            T_prev1 = T_1
            
            for k in range(2, self.K):
                T_k = 2.0 * (spmm(T_prev1) - T_prev1) - T_prev2
                bands.append(T_k)
                T_prev2 = T_prev1
                T_prev1 = T_k

        return torch.cat(bands, dim=-1)

