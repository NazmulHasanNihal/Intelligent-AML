"""
model.py — BurstAwareHGT Neural Network, FocalLoss, and Elastic Weight Consolidation (EWC).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import Linear
from ..burst_aware_hgt_conv import BurstAwareHGTConv
from ..graph_smote import LatentGraphSMOTE, DynamicThresholdCalibrator, BilinearEdgeGenerator
from .profiles import NODE_TYPES, EDGE_TYPES, HIDDEN_CHANNELS, NUM_LAYERS, DROPOUT, ACTIVATION, JK_MODE

class BurstAwareHGT(nn.Module):
    """
    Heterogeneous Graph Transformer with Burst-Aware Edge Attenuation,
    Gated Residual Skip Connections, Jumping Knowledge (JK) Aggregation,
    and Stabilizing Layer Normalization.
    
    Improvement #6: Supports deeper architectures (5-6 layers) with JK-cat
    aggregation to prevent over-smoothing and capture multi-hop laundering rings.
    """
    def __init__(self, in_channels_dict, hidden_channels, num_layers, metadata,
                 num_heads=4, lambda_decay=0.1, beta_scale=1.5, dropout=0.3,
                 jk_mode=None):
        super().__init__()
        self.metadata = metadata
        self.num_layers = num_layers
        self.hidden_channels = hidden_channels
        self.jk_mode = jk_mode  # "cat", "max", "last", or None
        
        # 1. Projection layer per node type
        self.node_proj = nn.ModuleDict()
        for nt in metadata[0]:
            in_dim = in_channels_dict.get(nt, hidden_channels)
            self.node_proj[nt] = Linear(in_dim, hidden_channels)
            
        # 2. Convolutions, LayerNorms, and Gated Residuals per layer
        self.convs = nn.ModuleList()
        self.layer_norms = nn.ModuleList()
        self.res_gates = nn.ModuleList()
        
        for _ in range(num_layers):
            layer_convs = nn.ModuleDict()
            for relation in metadata[1]:
                rel_key = "__".join(relation)
                layer_convs[rel_key] = BurstAwareHGTConv(
                    hidden_channels, hidden_channels, num_heads,
                    lambda_decay=lambda_decay, beta_scale=beta_scale
                )
            self.convs.append(layer_convs)
            
            # Layer normalization and learnable gating per node type
            self.layer_norms.append(nn.ModuleDict({
                nt: nn.LayerNorm(hidden_channels) for nt in metadata[0]
            }))
            self.res_gates.append(nn.ModuleDict({
                nt: nn.Linear(hidden_channels * 2, hidden_channels) for nt in metadata[0]
            }))
            
        self.dropout = nn.Dropout(dropout)
        
        # 3. Jumping Knowledge projection (reduces concatenated multi-layer repr back to hidden_channels)
        if self.jk_mode == "cat":
            self.jk_proj = nn.ModuleDict({
                nt: Linear(hidden_channels * num_layers, hidden_channels) for nt in metadata[0]
            })
        
        # 4. Final classification head per node type
        self.out_proj = nn.ModuleDict()
        for nt in metadata[0]:
            self.out_proj[nt] = Linear(hidden_channels, 2)

    def get_embeddings(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        # Project all node features into uniform hidden dimension
        h_dict = {}
        for nt, x in x_dict.items():
            if x.shape[0] > 0:
                h_dict[nt] = F.relu(self.node_proj[nt](x))
                h_dict[nt] = self.dropout(h_dict[nt])
            else:
                h_dict[nt] = x
        
        # Collect per-layer representations for Jumping Knowledge
        jk_layers = {nt: [] for nt in h_dict.keys()} if self.jk_mode == "cat" else None
                
        # Propagation loop with LayerNorm and Gated Skip Connections
        for i in range(self.num_layers):
            new_h_dict = {}
            counts = {nt: 0 for nt in h_dict.keys()}
            
            for relation in self.metadata[1]:
                rel_key = "__".join(relation)
                src_type, edge_type, dst_type = relation
                
                if relation in edge_index_dict and edge_index_dict[relation].numel() > 0:
                    edge_index = edge_index_dict[relation]
                    delta_t = delta_t_dict[relation]
                    burst_score = burst_score_dict[relation]
                    
                    x_src = h_dict[src_type]
                    x_dst = h_dict[dst_type]
                    
                    # Run convolution message passing
                    h_out = self.convs[i][rel_key](
                        (x_src, x_dst), edge_index, delta_t, burst_score
                    )
                    
                    if dst_type not in new_h_dict:
                        new_h_dict[dst_type] = h_out
                    else:
                        new_h_dict[dst_type] = new_h_dict[dst_type] + h_out
                    counts[dst_type] += 1
            
            # Apply activations, gated residuals, and layer normalization
            for nt in h_dict.keys():
                if counts[nt] > 0 and nt in new_h_dict and h_dict[nt].shape[0] > 0:
                    agg = new_h_dict[nt] / counts[nt]
                    gate = torch.sigmoid(self.res_gates[i][nt](torch.cat([h_dict[nt], agg], dim=-1)))
                    fused = gate * h_dict[nt] + (1.0 - gate) * F.relu(agg)
                    h_dict[nt] = self.layer_norms[i][nt](fused)
                    h_dict[nt] = self.dropout(h_dict[nt])
            
            del new_h_dict
            
            # Store layer output for Jumping Knowledge aggregation
            if jk_layers is not None:
                for nt in h_dict.keys():
                    jk_layers[nt].append(h_dict[nt])
        
        # Apply Jumping Knowledge aggregation (concatenate all layer representations)
        if self.jk_mode == "cat" and jk_layers is not None:
            for nt in h_dict.keys():
                if len(jk_layers[nt]) > 0 and h_dict[nt].shape[0] > 0:
                    jk_concat = torch.cat(jk_layers[nt], dim=-1)
                    h_dict[nt] = self.jk_proj[nt](jk_concat)
                    
        return h_dict

    def forward(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        h_dict = self.get_embeddings(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                
        # Classify nodes
        out_dict = {}
        for nt, h in h_dict.items():
            if h.shape[0] > 0:
                out_dict[nt] = self.out_proj[nt](h)
            else:
                out_dict[nt] = torch.zeros(0, 2, device=h.device)
                
        return out_dict


class FocalLoss(nn.Module):
    """
    Focal Loss with Label Smoothing to address extreme class imbalance by down-weighting
    easy examples and preventing overconfident probability estimates on noisy fraudulent patterns.
    """
    def __init__(self, alpha=None, gamma=2.0, reduction='mean', label_smoothing=0.05):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
        self.label_smoothing = label_smoothing

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', label_smoothing=self.label_smoothing)
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        
        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            focal_loss = alpha_t * focal_loss
            
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss


class EWC:
    """
    Elastic Weight Consolidation (EWC) class to compute parameter importance (Fisher Matrix)
    and calculate quadratic regularization loss during continuous incremental learning.
    """
    def __init__(self, model, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, target_node, y_target):
        self.model = model
        self.target_node = target_node
        self.params = {n: p.clone().detach() for n, p in model.named_parameters() if p.requires_grad}
        self.fisher = self._compute_fisher(x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target)

    def _compute_fisher(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict, y_target):
        fisher = {}
        for n, p in self.model.named_parameters():
            if p.requires_grad:
                fisher[n] = torch.zeros_like(p)
                
        self.model.eval()
        self.model.zero_grad()
        
        # Run forward pass and compute backward gradients
        out_dict = self.model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
        logits = out_dict[self.target_node]
        valid_mask = y_target >= 0
        
        if valid_mask.sum() > 0:
            loss = F.cross_entropy(logits[valid_mask], y_target[valid_mask])
            loss.backward()
            
            for n, p in self.model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    fisher[n] = p.grad.data.pow(2)
                    
        return fisher

    def penalty(self, model):
        loss = 0.0
        for n, p in model.named_parameters():
            if p.requires_grad and n in self.fisher:
                loss += (self.fisher[n] * (p - self.params[n]).pow(2)).sum()
        return loss


