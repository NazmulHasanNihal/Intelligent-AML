"""
Physics-Informed Mass-Conserving Graph Neural Network (PINN-GNN) for Intelligent-AML.

Implements financial physics constraints based on Kirchhoff's Current Law (Mass Balance):
- Inflow vs. Outflow flow conservation: sum(Inflow) = sum(Outflow) + Delta Balance + Fees
- Relative transfer flow ratios: A_uv / (sum_k A_kv + eps)
- MassConservingConv: GNN layer encoding flow conservation residuals directly into message passing.
- KirchhoffFlowLoss: Auxiliary physics-informed loss for unsupervised flow anomaly detection.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple


class MassConservingConv(nn.Module):
    """
    Mass-Conserving Spatio-Temporal Graph Convolution Layer.
    Aggregates messages by weighting them with relative mass flow proportions
    and explicit node-level cash flow conservation balance residuals.
    """

    def __init__(self, in_channels: int, out_channels: int, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        
        # Message transform: node features (in_channels) + relative flow (1) + conservation residual (1)
        self.msg_linear = nn.Linear(in_channels + 2, out_channels)
        self.update_linear = nn.Linear(in_channels + out_channels, out_channels)
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(out_channels)

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        edge_amounts: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Node feature matrix [N, in_channels]
            edge_index: Graph connectivity [2, E] (src -> dst)
            edge_amounts: Dollar transfer amounts [E] or [E, 1]
        Returns:
            out_x: Updated node representations [N, out_channels]
            flow_residuals: Kirchhoff mass conservation residual per node [N, 1]
        """
        num_nodes = x.size(0)
        
        if edge_index.numel() == 0 or edge_index.size(1) == 0:
            dummy_out = self.norm(F.relu(self.update_linear(torch.cat([x, torch.zeros(num_nodes, self.out_channels, device=x.device)], dim=-1))))
            dummy_res = torch.zeros(num_nodes, 1, device=x.device)
            return dummy_out, dummy_res

        src, dst = edge_index[0], edge_index[1]
        
        if edge_amounts is None:
            edge_amounts = torch.ones(edge_index.size(1), 1, device=x.device)
        elif edge_amounts.dim() == 1:
            edge_amounts = edge_amounts.unsqueeze(-1)

        # 1. Compute Total Inflow & Outflow per Node
        inflow = torch.zeros(num_nodes, 1, device=x.device).scatter_add_(0, dst.unsqueeze(-1), edge_amounts)
        outflow = torch.zeros(num_nodes, 1, device=x.device).scatter_add_(0, src.unsqueeze(-1), edge_amounts)

        # 2. Kirchhoff Flow Balance Residual (Inflow - Outflow relative to total volume)
        total_vol = inflow + outflow + 1e-6
        flow_residuals = (inflow - outflow) / total_vol

        # 3. Relative Transfer Flow Ratio per Edge (Proportion of destination's inflow from this specific source)
        dst_inflow = inflow[dst] + 1e-6
        relative_edge_flow = edge_amounts / dst_inflow

        # 4. Formulate Physics-Informed Message Vector
        # [x_src, relative_flow, source_conservation_residual]
        src_residuals = flow_residuals[src]
        raw_msg_input = torch.cat([x[src], relative_edge_flow, src_residuals], dim=-1)
        msg = F.relu(self.msg_linear(raw_msg_input))
        msg = self.dropout(msg)

        # 5. Aggregate Messages at Destination
        agg_msg = torch.zeros(num_nodes, self.out_channels, device=x.device)
        agg_msg.index_add_(0, dst, msg)

        # 6. Node State Update
        combined = torch.cat([x, agg_msg], dim=-1)
        out_x = self.norm(F.relu(self.update_linear(combined)))

        return out_x, flow_residuals


class KirchhoffFlowLoss(nn.Module):
    """
    Auxiliary Physics-Informed Loss Function for Financial Flow Conservation.
    Penalizes intermediate layering nodes (PassThrough > 0.8) that violate mass balance.
    """

    def __init__(self, pass_through_threshold: float = 0.75):
        super().__init__()
        self.pass_through_threshold = pass_through_threshold

    def forward(
        self,
        flow_residuals: torch.Tensor,
        is_intermediate_mule: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Penalizes |Inflow - Outflow| / Volume for nodes expected to be pure pass-through conduits.
        """
        if is_intermediate_mule is not None:
            mask = is_intermediate_mule.float().unsqueeze(-1)
            loss = torch.mean(torch.abs(flow_residuals) * mask)
        else:
            # General L1 flow penalty on conservation deviations
            loss = torch.mean(torch.abs(flow_residuals))
        return loss
