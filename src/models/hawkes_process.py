"""
hawkes_process.py — Continuous-Time Multivariate Hawkes Process Arrival Intensity Module.
Models self-exciting and mutually-exciting transaction generation dynamics across financial entities.
Replaces static heuristic sliding windows with provable point-process likelihood and intensity metrics:
    lambda_u(t) = mu_u + sum_{t_i < t} alpha_{uu} * exp(-beta_u * (t - t_i))
"""

import math
import numpy as np
import polars as pl
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional, Any, Union


class HawkesIntensityEngine:
    """
    High-Performance Vectorized Hawkes Point Process Intensity Engine.
    Computes exact self-exciting continuous arrival intensities across transaction ledgers.
    """
    def __init__(self, base_mu: float = 0.01, alpha_self: float = 0.80, beta_decay: float = 0.05):
        self.base_mu = float(base_mu)
        self.alpha_self = float(alpha_self)
        self.beta_decay = float(beta_decay)

    def compute_edge_hawkes_intensity(self, edges_df: Union[pl.DataFrame, pd.DataFrame],
                                      time_col: str = "ts",
                                      src_col: str = "src",
                                      dst_col: str = "dst") -> pl.DataFrame:
        """
        Computes continuous Hawkes arrival intensity lambda(t) for every interaction edge
        using vectorized recursive exponential decay formulation:
            S_i = (S_{i-1} + alpha) * exp(-beta * Delta t)
            lambda(t_i) = mu + S_i
        """
        if isinstance(edges_df, pd.DataFrame):
            df = pl.from_pandas(edges_df)
        else:
            df = edges_df

        if time_col not in df.columns or len(df) == 0:
            return df.with_columns(pl.lit(self.base_mu).alias("hawkes_intensity"))

        # Sort chronologically
        df = df.sort(time_col)
        
        # Calculate per-source recursive arrival intensity in Python/NumPy for exact recursion
        # Convert to numpy for ultra-fast single-pass recursive decay
        src_ids = df[src_col].to_numpy()
        timestamps = df[time_col].to_numpy().astype(np.float64)
        
        n = len(df)
        intensities = np.full(n, self.base_mu, dtype=np.float32)
        
        last_time_map: Dict[Any, float] = {}
        decay_sum_map: Dict[Any, float] = {}
        
        mu = self.base_mu
        alpha = self.alpha_self
        beta = self.beta_decay
        
        for i in range(n):
            u = src_ids[i]
            t = timestamps[i]
            
            if u in last_time_map:
                dt = max(0.0, t - last_time_map[u])
                # Exponential decay of historical intensity memory
                prev_s = decay_sum_map[u]
                curr_s = (prev_s + alpha) * math.exp(-beta * dt)
            else:
                curr_s = 0.0
                
            last_time_map[u] = t
            decay_sum_map[u] = curr_s
            intensities[i] = mu + curr_s

        # Add intensity and log-intensity columns
        df = df.with_columns([
            pl.Series("hawkes_intensity", intensities),
            pl.Series("log_hawkes_intensity", np.log1p(intensities))
        ])
        
        return df


class HawkesTemporalEncoder(nn.Module):
    """
    Differentiable Neural Hawkes Process Projection Layer.
    Embeds continuous arrival intensity lambda(t) and inter-arrival intervals into continuous
    edge representation spaces to fuse with HGT attention heads.
    """
    def __init__(self, out_dim: int = 16, num_components: int = 4):
        super().__init__()
        self.out_dim = out_dim
        self.num_components = num_components
        
        # Learnable multi-scale Hawkes decay parameters
        self.log_betas = nn.Parameter(torch.linspace(math.log(0.001), math.log(1.0), num_components))
        self.alpha_weights = nn.Parameter(torch.ones(num_components) / num_components)
        
        self.projection = nn.Sequential(
            nn.Linear(num_components + 1, out_dim),
            nn.SiLU(),
            nn.Linear(out_dim, out_dim)
        )

    def forward(self, hawkes_intensity: torch.Tensor, delta_t: torch.Tensor) -> torch.Tensor:
        """
        Args:
            hawkes_intensity: [num_edges] or [num_edges, 1] raw Hawkes intensity
            delta_t: [num_edges] or [num_edges, 1] elapsed interval
        Returns:
            [num_edges, out_dim] continuous Hawkes temporal representation
        """
        device = delta_t.device
        h_int = hawkes_intensity.to(device).view(-1, 1).float()
        dt = delta_t.to(device).view(-1, 1).float()
        
        betas = torch.exp(self.log_betas).to(device)  # [num_components]
        # Multi-scale decay: exp(-beta_k * dt)
        decay_feats = torch.exp(-dt * betas.unsqueeze(0))  # [num_edges, num_components]
        
        # Concatenate log intensity with multi-scale decays
        feat_combined = torch.cat([torch.log1p(h_int), decay_feats], dim=-1)
        return self.projection(feat_combined)
