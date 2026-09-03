import torch
from torch.nn import Parameter
import torch.nn.functional as F
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.utils import softmax
import numpy as np


class BurstAwareHGTConv(MessagePassing):
    def __init__(self, in_channels, out_channels, num_heads, lambda_decay=0.1, beta_scale=1.5,
                 min_residual_floor=0.05, cam_residual_floor=0.10):
        """
        Enterprise Multi-Scale Spatiotemporal GNN Convolution Layer with:
        1. Tri-Band Multi-Scale Temporal Attention Bank (Burst, Diurnal, Seasonal/Hibernation).
        2. Learnable MLP Edge-Gated Anti-Camouflage Denoising Gate.
        3. Logarithmic Harmonic Sinusoidal Temporal Projection.
        4. Brody Dynamic GATv2 Attention Weight Parameterization.
        
        Args:
            in_channels (int): Dimensionality of input node features.
            out_channels (int): Dimensionality of output node embeddings.
            num_heads (int): Number of multi-head attention weights.
            lambda_decay (float): Base exponential decay parameter (λ).
            beta_scale (float): Sensitivity multiplier for high-velocity burst anomalies (β).
            min_residual_floor (float): Minimum baseline decay weight to preserve multi-year topology.
            cam_residual_floor (float): Minimum attention floor for anti-camouflage gate to prevent over-pruning.
        """
        super(BurstAwareHGTConv, self).__init__(aggr='add', node_dim=0)
        
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_heads = num_heads
        self.d_k = out_channels // num_heads
        self.min_residual_floor = float(min_residual_floor)
        self.cam_residual_floor = float(cam_residual_floor)
        
        # 1. Multi-Scale Temporal Attention Bank (Tri-Band Decay Parameters)
        # Band 1: High-frequency bursts (seconds to 24h mixer bursts)
        self.raw_lambda_burst = Parameter(torch.tensor(float(lambda_decay)))
        self.raw_beta_burst = Parameter(torch.tensor(float(beta_scale)))
        
        # Band 2: Diurnal / Weekly business cycles (1 to 7 days)
        self.raw_lambda_diurnal = Parameter(torch.tensor(0.01))
        self.raw_beta_diurnal = Parameter(torch.tensor(0.5))
        
        # Band 3: Seasonal / Long-Dwell Hibernation Layering (30 to 90+ days)
        self.raw_lambda_seasonal = Parameter(torch.tensor(0.0001))
        self.raw_beta_seasonal = Parameter(torch.tensor(0.1))
        
        # Learnable temporal band mixing logits
        self.temporal_band_weights = Parameter(torch.tensor([0.4, 0.35, 0.25]))
        
        # 2. Learnable MLP Edge-Gated Anti-Camouflage Gate
        # Denoises synthetic linkages and prevents camouflage dilution from high-degree utility nodes
        self.cam_gate_mlp = torch.nn.Sequential(
            torch.nn.Linear(self.d_k * 3, self.d_k),
            torch.nn.LeakyReLU(0.2),
            torch.nn.Linear(self.d_k, self.num_heads),
            torch.nn.Sigmoid()
        )
        
        self.cam_gamma = Parameter(torch.tensor(2.0))
        self.raw_temp = Parameter(torch.tensor(float(np.log(np.exp(self.d_k ** 0.5) - 1.0))))
        
        # 3. Sinusoidal temporal encoding projections
        self.time_emb_dim = 16
        self.time_proj = torch.nn.Linear(self.time_emb_dim, self.d_k)
        
        # Register Logarithmic Harmonic Look-Up Table (LUT) buffer
        self.lut_size = 4000
        self.max_log_t = 12.0  # log(1 + 160,000+) ~ 12.0
        self.lut_step = self.max_log_t / self.lut_size
        self.register_buffer("time_lut", torch.zeros(self.lut_size, self.time_emb_dim))
        
        # Precompute logarithmic sinusoidal representations
        half_dim = self.time_emb_dim // 2
        emb_scale = torch.exp(torch.arange(0, half_dim, dtype=torch.float) * -(np.log(10000.0) / (half_dim - 1)))
        log_t_vals = torch.arange(0.0, self.lut_size * self.lut_step, self.lut_step)
        emb = log_t_vals.unsqueeze(-1) * emb_scale.unsqueeze(0)
        self.time_lut.copy_(torch.cat([torch.sin(emb), torch.cos(emb)], dim=-1))
        
        # Type-specific linear projections
        self.q_linear = torch.nn.Linear(in_channels, out_channels)
        self.k_linear = torch.nn.Linear(in_channels, out_channels)
        self.v_linear = torch.nn.Linear(in_channels, out_channels)
        self.out_linear = torch.nn.Linear(out_channels, out_channels)
        
        # Brody Dynamic GATv2 Attention Weight Vector
        self.att_vec = Parameter(torch.empty(1, self.num_heads, self.d_k))
        torch.nn.init.xavier_normal_(self.att_vec)
        
    def forward(self, x, edge_index, delta_t, burst_score):
        """
        Executes the Enterprise Spatiotemporal Message Passing Forward Pass.
        """
        if isinstance(x, tuple):
            x_src, x_dst = x
            query = self.q_linear(x_dst).view(-1, self.num_heads, self.d_k)
            key = self.k_linear(x_src).view(-1, self.num_heads, self.d_k)
            value = self.v_linear(x_src).view(-1, self.num_heads, self.d_k)
        else:
            query = self.q_linear(x).view(-1, self.num_heads, self.d_k)
            key = self.k_linear(x).view(-1, self.num_heads, self.d_k)
            value = self.v_linear(x).view(-1, self.num_heads, self.d_k)
        
        # Propagate spatial messages across edges
        out = self.propagate(edge_index, query=query, key=key, value=value, 
                             delta_t=delta_t, burst_score=burst_score, size=None)
        
        # Final structural linear reconstruction
        out = out.view(-1, self.out_channels)
        return self.out_linear(out)

    def message(self, query_i, key_j, value_j, delta_t, burst_score, index, ptr, size_i):
        """
        Constructs and attenuates spatiotemporal messages using Multi-Scale Temporal Banks
        and Learnable Anti-Camouflage Edge Gating.
        """
        # Logarithmic Time Look-Up Table (LUT) query
        log_dt = torch.log1p(torch.clamp(delta_t, min=0.0))
        lut_idx = torch.clamp((log_dt / self.lut_step).long(), 0, self.lut_size - 1)
        time_emb = self.time_lut[lut_idx]
        time_feat = self.time_proj(time_emb)  # Shape: [num_edges, d_k]
        
        # Modulate keys with sinusoidal temporal encoding
        key_j_time = key_j + time_feat.unsqueeze(1)  # Broadcast across num_heads
        
        # A. Calculate dynamic GATv2 attention coefficient
        dyn_act = F.leaky_relu(query_i + key_j_time, negative_slope=0.2)
        temp = F.softplus(self.raw_temp) + 1e-4
        alpha = (dyn_act * self.att_vec).sum(dim=-1) / temp
        
        # B. Learnable MLP Edge-Gated Anti-Camouflage Filter
        # Measures relational affinity across query, time-modulated key, and time embedding
        time_feat_expanded = time_feat.unsqueeze(1).repeat(1, self.num_heads, 1)
        gate_input = torch.cat([query_i, key_j_time, time_feat_expanded], dim=-1)  # [num_edges, num_heads, d_k * 3]
        cam_gate = self.cam_gate_mlp(gate_input.mean(dim=1))  # [num_edges, num_heads]
        
        # Anti-Camouflage Residual Floor Guarantee
        cam_gate_guarded = self.cam_residual_floor + (1.0 - self.cam_residual_floor) * cam_gate
        alpha = alpha * cam_gate_guarded
        
        # Softmax normalization over destination neighborhood
        alpha = softmax(alpha, index, ptr, num_nodes=size_i)
        
        # C. Multi-Scale Temporal Attention Bank (Tri-Band Continuous-Time Synthesis)
        w_min = self.min_residual_floor
        mixing_weights = F.softmax(self.temporal_band_weights, dim=0)
        
        # Band 1: Burst Decay
        lambda_b = F.softplus(self.raw_lambda_burst)
        beta_b = F.softplus(self.raw_beta_burst)
        decay_b = (w_min + (1.0 - w_min) * torch.exp(-lambda_b * delta_t)).unsqueeze(-1)
        burst_b = (1.0 + beta_b * torch.tanh(burst_score)).unsqueeze(-1)
        w_burst = decay_b * burst_b
        
        # Band 2: Diurnal Decay
        lambda_d = F.softplus(self.raw_lambda_diurnal)
        beta_d = F.softplus(self.raw_beta_diurnal)
        decay_d = (w_min + (1.0 - w_min) * torch.exp(-lambda_d * delta_t)).unsqueeze(-1)
        burst_d = (1.0 + beta_d * torch.tanh(burst_score)).unsqueeze(-1)
        w_diurnal = decay_d * burst_d
        
        # Band 3: Seasonal / Hibernation Decay
        lambda_s = F.softplus(self.raw_lambda_seasonal)
        beta_s = F.softplus(self.raw_beta_seasonal)
        decay_s = (w_min + (1.0 - w_min) * torch.exp(-lambda_s * delta_t)).unsqueeze(-1)
        burst_s = (1.0 + beta_s * torch.tanh(burst_score)).unsqueeze(-1)
        w_seasonal = decay_s * burst_s
        
        # Synthesized Multi-Scale Continuous-Time Weight
        w_multi = (mixing_weights[0] * w_burst + 
                   mixing_weights[1] * w_diurnal + 
                   mixing_weights[2] * w_seasonal)  # [num_edges, 1]
                   
        w_t = w_multi.repeat(1, self.num_heads)  # [num_edges, num_heads]
        
        # D. Attenuate value messages across all multi-scale heads
        msg = value_j * alpha.unsqueeze(-1)
        msg = msg * w_t.unsqueeze(-1)  # [num_edges, num_heads, d_k]
        
        return msg
