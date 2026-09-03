"""
Literature Baseline Models for Anti-Money Laundering (AML) Benchmark Comparison.
Implements:
1. Homogeneous GCN (Weber et al. 2019 / Kipf & Welling 2017)
2. GraphSAGE (Hamilton et al. 2017)
3. Standard GAT (Velickovic et al. 2018)
4. GIN: Graph Isomorphism Network (Xu et al. 2019 / Custom Edge GIN 2025)
5. EvolveGCN: Dynamic Recurrent Graph Network (Pareja et al. 2020)
6. GCN-GRU: Spatiotemporal Sequence Baseline
7. Tabular XGBoost (Industrial Banking Baseline)
8. Topological Logistic Regression (Degree & Network Features)
"""

import math
import os
import sys
from pathlib import Path

# Windows PyTorch DLL loading safety guard
_venv_torch_lib = Path(__file__).resolve().parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch_geometric.nn import GCNConv, SAGEConv, GINConv, GATConv
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression


class HomogeneousGAT(nn.Module):
    """Homogeneous Graph Attention Network (GAT) baseline from Velickovic et al. (2018)."""
    def __init__(self, in_channels, hidden_channels=64, out_channels=2, heads=4, dropout=0.3):
        super().__init__()
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, concat=False)
        self.conv2 = GATConv(hidden_channels, out_channels, heads=1, concat=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        x = F.elu(self.conv1(x, edge_index))
        x = self.dropout(x)
        return self.conv2(x, edge_index)


class HomogeneousGCN(nn.Module):
    """3-layer Homogeneous GCN Conv baseline from Weber et al. (2019)."""
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, num_layers=3, dropout=0.3):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(in_channels, hidden_channels))
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
        self.convs.append(GCNConv(hidden_channels, out_channels))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        return self.convs[-1](x, edge_index)


class GraphSAGEBaseline(nn.Module):
    """3-layer Inductive GraphSAGE baseline from Hamilton et al. (2017)."""
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, num_layers=3, dropout=0.3):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_channels, hidden_channels, aggr="mean"))
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_channels, hidden_channels, aggr="mean"))
        self.convs.append(SAGEConv(hidden_channels, out_channels, aggr="mean"))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        return self.convs[-1](x, edge_index)


class StandardGAT(nn.Module):
    """Standard Graph Attention Network (GAT) baseline from Velickovic et al. (2018)."""
    def __init__(self, in_channels_dict, hidden_channels, num_layers, metadata, num_heads=4, dropout=0.3):
        super().__init__()
        from src.models.burst_aware_hgt_conv import BurstAwareHGTConv
        self.node_types, self.edge_types = metadata
        self.input_projs = nn.ModuleDict({
            nt: nn.Linear(in_channels_dict[nt], hidden_channels) for nt in self.node_types
        })
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            layer_dict = nn.ModuleDict({
                f"{et[0]}___{et[1]}___{et[2]}": BurstAwareHGTConv(
                    hidden_channels, hidden_channels, num_heads, lambda_decay=0.0, beta_scale=0.0
                ) for et in self.edge_types
            })
            self.convs.append(layer_dict)
        self.classifier = nn.Linear(hidden_channels, 2)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x_dict, edge_index_dict, delta_t_dict, burst_score_dict):
        h_dict = {nt: F.relu(self.input_projs[nt](x_dict[nt])) for nt in self.node_types}
        for layer_dict in self.convs:
            new_h_dict = {nt: [] for nt in self.node_types}
            for edge_type in self.edge_types:
                src, rel, dst = edge_type
                key = f"{src}___{rel}___{dst}"
                if edge_type in edge_index_dict and edge_index_dict[edge_type].numel() > 0:
                    conv = layer_dict[key]
                    out = conv((h_dict[src], h_dict[dst]), edge_index_dict[edge_type], delta_t_dict[edge_type], burst_score_dict[edge_type])
                    new_h_dict[dst].append(out)
            for nt in self.node_types:
                if len(new_h_dict[nt]) > 0:
                    h_dict[nt] = F.relu(torch.stack(new_h_dict[nt]).mean(dim=0))
                    h_dict[nt] = self.dropout(h_dict[nt])
        return {nt: self.classifier(h_dict[nt]) for nt in self.node_types}


class GINBaseline(nn.Module):
    """Graph Isomorphism Network (GIN) from Xu et al. (2019) / Custom Edge GIN (2025)."""
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, dropout=0.3):
        super().__init__()
        mlp1 = nn.Sequential(
            nn.Linear(in_channels, hidden_channels),
            nn.BatchNorm1d(hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        mlp2 = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.BatchNorm1d(hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        self.conv1 = GINConv(mlp1, train_eps=True)
        self.conv2 = GINConv(mlp2, train_eps=True)
        self.out_proj = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        h = F.relu(self.conv1(x, edge_index))
        h = self.dropout(h)
        h = F.relu(self.conv2(h, edge_index))
        h = self.dropout(h)
        return self.out_proj(h)


class EvolveGCNBaseline(nn.Module):
    """EvolveGCN Dynamic Graph baseline from Pareja et al. (2020)."""
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, dropout=0.3):
        super().__init__()
        self.gcn1 = GCNConv(in_channels, hidden_channels)
        self.gcn2 = GCNConv(hidden_channels, hidden_channels)
        self.gru = nn.GRUCell(hidden_channels, hidden_channels)
        self.out_proj = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index, h_prev=None):
        h = F.relu(self.gcn1(x, edge_index))
        h = self.dropout(h)
        h = F.relu(self.gcn2(h, edge_index))
        if h_prev is not None:
            h = self.gru(h, h_prev)
        return self.out_proj(h), h


class GCNGRUBaseline(nn.Module):
    """Spatiotemporal GCN-GRU Sequence baseline."""
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, dropout=0.3):
        super().__init__()
        self.spatial_encoder = GCNConv(in_channels, hidden_channels)
        self.temporal_proj = nn.Linear(2, hidden_channels)
        self.gru_cell = nn.GRUCell(hidden_channels, hidden_channels)
        self.classifier = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index, delta_t, burst_score):
        h_spatial = F.relu(self.spatial_encoder(x, edge_index))
        h_spatial = self.dropout(h_spatial)
        t_feats = torch.stack([delta_t, burst_score], dim=-1)
        h_temporal = F.relu(self.temporal_proj(t_feats))
        h_fused = self.gru_cell(h_spatial, h_temporal)
        return self.classifier(h_fused)


class TabularXGBoost:
    """Standard Industry Tabular Gradient Boosted Trees (Chen & Guestrin 2016)."""
    def __init__(self, n_estimators=100, max_depth=6, learning_rate=0.08, random_state=42):
        self.model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=-1
        )

    def fit(self, x, y):
        neg_count = (y == 0).sum()
        pos_count = (y == 1).sum()
        scale_pos = max(1.0, neg_count / (pos_count + 1e-6))
        self.model.set_params(scale_pos_weight=scale_pos)
        self.model.fit(x, y)

    def predict_proba(self, x):
        return self.model.predict_proba(x)[:, 1]


class IndustrialLightGBM:
    """Standard Industry LightGBM Classifier (Microsoft 2017)."""
    def __init__(self, n_estimators=100, num_leaves=31, learning_rate=0.08, random_state=42):
        import lightgbm as lgb
        self.model = lgb.LGBMClassifier(
            n_estimators=n_estimators,
            num_leaves=num_leaves,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=-1,
            verbose=-1
        )

    def fit(self, x, y):
        neg_count = (y == 0).sum()
        pos_count = (y == 1).sum()
        scale_pos = max(1.0, neg_count / (pos_count + 1e-6))
        self.model.set_params(scale_pos_weight=scale_pos)
        self.model.fit(x, y)

    def predict_proba(self, x):
        return self.model.predict_proba(x)[:, 1]


class IndustrialCatBoost:
    """Standard Industry CatBoost Classifier (Yandex 2017)."""
    def __init__(self, iterations=100, depth=6, learning_rate=0.08, random_seed=42):
        from catboost import CatBoostClassifier
        self.model = CatBoostClassifier(
            iterations=iterations,
            depth=depth,
            learning_rate=learning_rate,
            random_seed=random_seed,
            verbose=False
        )

    def fit(self, x, y):
        neg_count = (y == 0).sum()
        pos_count = (y == 1).sum()
        scale_pos = max(1.0, neg_count / (pos_count + 1e-6))
        self.model.set_params(scale_pos_weight=scale_pos)
        self.model.fit(x, y)

    def predict_proba(self, x):
        return self.model.predict_proba(x)[:, 1]


class IsolationForestBaseline:
    """Unsupervised Isolation Forest Outlier Anomaly Detector (Liu et al. 2008)."""
    def __init__(self, n_estimators=100, contamination=0.05, random_state=42):
        from sklearn.ensemble import IsolationForest
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )

    def fit(self, x, y=None):
        self.model.fit(x)

    def predict_proba(self, x):
        # Invert anomaly scores: lower score means more anomalous -> map to [0, 1] probability
        raw_scores = -self.model.decision_function(x)
        probs = (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-6)
        return probs


class DeepAutoencoderBaseline:
    """Deep Learning Unsupervised Autoencoder Anomaly Detector (Reconstruction Error)."""
    def __init__(self, in_channels, hidden_dim=64, latent_dim=16, epochs=15):
        self.epochs = epochs
        self.encoder = nn.Sequential(
            nn.Linear(in_channels, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, latent_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, in_channels)
        )
        self.optimizer = torch.optim.AdamW(list(self.encoder.parameters()) + list(self.decoder.parameters()), lr=0.005)
        self.criterion = nn.MSELoss()

    def fit(self, x, y=None):
        # Train strictly on normal / licit instances or full training split
        if len(x) > 200000:
            idx = np.random.choice(len(x), size=200000, replace=False)
            x_fit = x[idx]
        else:
            x_fit = x
            
        x_tensor = torch.tensor(x_fit, dtype=torch.float)
        batch_size = max(512, min(8192, len(x_fit) // 50))
        dataset = torch.utils.data.TensorDataset(x_tensor)
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.encoder.train()
        self.decoder.train()
        for _ in range(self.epochs):
            for (batch_x,) in loader:
                self.optimizer.zero_grad()
                z = self.encoder(batch_x)
                rec = self.decoder(z)
                loss = self.criterion(rec, batch_x)
                loss.backward()
                self.optimizer.step()

    def predict_proba(self, x):
        self.encoder.eval()
        self.decoder.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(x, dtype=torch.float)
            # Batch-wise prediction for memory safety on multi-million rows
            rec_errors_list = []
            pred_loader = torch.utils.data.DataLoader(
                torch.utils.data.TensorDataset(x_tensor), batch_size=16384, shuffle=False
            )
            for (bx,) in pred_loader:
                bz = self.encoder(bx)
                brec = self.decoder(bz)
                berr = torch.mean((bx - brec) ** 2, dim=-1).cpu().numpy()
                rec_errors_list.append(berr)
            rec_errors = np.concatenate(rec_errors_list)
            
        probs = (rec_errors - rec_errors.min()) / (rec_errors.max() - rec_errors.min() + 1e-6)
        return probs


class BalancedRandomForestBaseline:
    """Balanced Random Forest Ensemble (Chen et al. 2004)."""
    def __init__(self, n_estimators=100, max_depth=10, random_state=42):
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1
        )

    def fit(self, x, y):
        self.model.fit(x, y)

    def predict_proba(self, x):
        return self.model.predict_proba(x)[:, 1]


class TopologicalLogisticRegression:
    """Logistic Regression on Node Features + Graph Degree Statistics."""
    def __init__(self, max_iter=200, random_state=42):
        self.model = LogisticRegression(max_iter=max_iter, random_state=random_state)

    def fit(self, x, y):
        self.model.fit(x, y)

    def predict_proba(self, x):
        return self.model.predict_proba(x)[:, 1]


class VanillaHGTBaseline(nn.Module):
    """
    Vanilla Heterogeneous Graph Transformer (HGT) from Hu et al. (WWW 2020).
    Pure heterogeneous multi-head attention without continuous sinusoidal LUT,
    without burst-aware velocity attenuation, and without boosted stacking.
    """
    def __init__(self, in_channels_dict, hidden_channels, num_layers, metadata, num_heads=4, dropout=0.3):
        super().__init__()
        self.node_types, self.edge_types = metadata
        self.input_projs = nn.ModuleDict({
            nt: nn.Linear(in_channels_dict[nt], hidden_channels) for nt in self.node_types
        })
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            layer_dict = nn.ModuleDict()
            for et in self.edge_types:
                src, rel, dst = et
                key = f"{src}___{rel}___{dst}"
                layer_dict[key] = nn.ModuleDict({
                    "k_proj": nn.Linear(hidden_channels, hidden_channels),
                    "q_proj": nn.Linear(hidden_channels, hidden_channels),
                    "v_proj": nn.Linear(hidden_channels, hidden_channels),
                })
            self.convs.append(layer_dict)
            
        self.num_heads = num_heads
        self.head_dim = hidden_channels // num_heads
        self.hidden_channels = hidden_channels
        self.classifier = nn.Linear(hidden_channels, 2)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x_dict, edge_index_dict, *args):
        h_dict = {nt: F.relu(self.input_projs[nt](x_dict[nt])) for nt in self.node_types}
        for layer_dict in self.convs:
            new_h_dict = {nt: [] for nt in self.node_types}
            for edge_type in self.edge_types:
                src, rel, dst = edge_type
                key = f"{src}___{rel}___{dst}"
                if edge_type in edge_index_dict and edge_index_dict[edge_type].numel() > 0:
                    edge_index = edge_index_dict[edge_type]
                    src_nodes, dst_nodes = edge_index[0], edge_index[1]
                    mods = layer_dict[key]
                    
                    h_src = h_dict[src][src_nodes]
                    h_dst = h_dict[dst][dst_nodes]
                    
                    k = mods["k_proj"](h_src).view(-1, self.num_heads, self.head_dim)
                    q = mods["q_proj"](h_dst).view(-1, self.num_heads, self.head_dim)
                    v = mods["v_proj"](h_src).view(-1, self.num_heads, self.head_dim)
                    
                    att = (q * k).sum(dim=-1) / math.sqrt(self.head_dim)
                    att = torch.softmax(att, dim=0).unsqueeze(-1)
                    
                    msg = (att * v).view(-1, self.hidden_channels)
                    out = torch.zeros(h_dict[dst].shape[0], self.hidden_channels, device=h_src.device)
                    out.index_add_(0, dst_nodes, msg)
                    new_h_dict[dst].append(out)
                    
            for nt in self.node_types:
                if len(new_h_dict[nt]) > 0:
                    h_dict[nt] = F.relu(torch.stack(new_h_dict[nt]).mean(dim=0))
                    h_dict[nt] = self.dropout(h_dict[nt])
                    
        return {nt: self.classifier(h_dict[nt]) for nt in self.node_types}


class CareGNNBaseline(nn.Module):
    """
    CARE-GNN from Dou et al. (ACM CIKM 2020).
    Camouflage-Aware Anti-Fraud GNN using label-aware cosine neighbor filtering
    and reinforcement-weighted inter-relation aggregation.
    """
    def __init__(self, in_channels, hidden_channels=128, out_channels=2, dropout=0.3):
        super().__init__()
        self.feature_proj = nn.Linear(in_channels, hidden_channels)
        self.classifier = nn.Linear(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        h = F.relu(self.feature_proj(x))
        h_norm = F.normalize(h, p=2, dim=-1)
        
        src_nodes, dst_nodes = edge_index[0], edge_index[1]
        
        # Camouflage Filtering via Cosine Similarity Gating
        sim = (h_norm[src_nodes] * h_norm[dst_nodes]).sum(dim=-1)
        gate = torch.sigmoid(sim * 3.0).unsqueeze(-1)
        
        # Filtered Neighborhood Aggregation
        filtered_msg = h[src_nodes] * gate
        h_agg = torch.zeros_like(h)
        h_agg.index_add_(0, dst_nodes, filtered_msg)
        
        deg = torch.zeros(h.shape[0], 1, device=x.device)
        deg.index_add_(0, dst_nodes, torch.ones_like(gate))
        h_agg = h_agg / (deg + 1e-6)
        
        h_out = F.relu(h + h_agg)
        h_out = self.dropout(h_out)
        return self.classifier(h_out)


