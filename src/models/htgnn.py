"""
HT-GNN: Heterogeneous Temporal Graph Neural Network
Layer 2 — Detection & Rebalancing

Reads ingested graph data from data/outputs/graph_data/ and produces
fraud risk scores using a heterogeneous temporal GNN with attention
over node types, edge types, and time.
"""

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path

import pyarrow.parquet as pq

from torch_geometric.data import HeteroData
from torch_geometric.nn import GATConv, SAGEConv, Linear


OUTPUT_DIR = Path("data/outputs/graph_data")
NODE_TYPES = ["Account", "User", "Device", "Institution"]
EDGE_TYPES = ["Transaction", "IP_Connection", "Shared_Ownership"]

HIDDEN_CHANNELS = 128
NUM_LAYERS = 3
DROPOUT = 0.3
ACTIVATION = "relu"


def load_parquet(path):
    if not Path(path).exists():
        return None
    table = pq.read_table(path)
    return table.to_pandas()


def build_hetero_data(dataset_name):
    """Load ingested nodes.parquet and edges.parquet for a dataset
    and convert to PyG HeteroData format."""
    dataset_dir = OUTPUT_DIR / dataset_name
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_dir}")

    nodes_path = dataset_dir / "nodes.parquet"
    edges_path = dataset_dir / "edges.parquet"

    if not nodes_path.exists():
        raise FileNotFoundError(f"nodes.parquet not found for {dataset_name}")
    if not edges_path.exists():
        raise FileNotFoundError(f"edges.parquet not found for {dataset_name}")

    nodes_df = load_parquet(nodes_path)
    edges_df = load_parquet(edges_path)

    # Build node feature matrix
    node_features = nodes_df.drop(columns=[c for c in nodes_df.columns
                                            if c in ("node_id", "node_type", "label")],
                                   errors="ignore")
    feature_cols = [c for c in node_features.columns if c.startswith("feat_")]
    if not feature_cols:
        x = torch.zeros(len(nodes_df), len(NODE_TYPES), dtype=torch.float)
        for i, nt in enumerate(nodes_df.get("node_type", [NODE_TYPES[0]] * len(nodes_df))):
            if nt in NODE_TYPES:
                x[i, NODE_TYPES.index(nt)] = 1.0
    else:
        x = torch.tensor(node_features[feature_cols].values, dtype=torch.float)
        x = torch.nan_to_num(x, nan=0.0)

    # Node type mapping
    node_type_col = nodes_df.get("node_type", [NODE_TYPES[0]] * len(nodes_df))
    node_type_to_idx = {nt: i for i, nt in enumerate(NODE_TYPES)}
    node_type_tensor = torch.tensor(
        [node_type_to_idx.get(nt, 0) for nt in node_type_col],
        dtype=torch.long
    )

    # Build edge index and edge type
    src_col = edges_df.get("src", None)
    dst_col = edges_df.get("dst", None)
    edge_type_col = edges_df.get("edge_type", ["Transaction"] * len(edges_df))

    if src_col is None or dst_col is None:
        raise ValueError(f"edges.parquet for {dataset_name} missing src/dst columns")

    all_node_ids = set(nodes_df["node_id"].unique())
    node_id_to_idx = {nid: i for i, nid in enumerate(sorted(all_node_ids))}

    src_idx = torch.tensor([node_id_to_idx.get(sid, -1) for sid in src_col], dtype=torch.long)
    dst_idx = torch.tensor([node_id_to_idx.get(did, -1) for did in dst_col], dtype=torch.long)
    valid_mask = (src_idx >= 0) & (dst_idx >= 0)
    src_idx = src_idx[valid_mask]
    dst_idx = dst_idx[valid_mask]
    edge_type_col = [edge_type_col[i] for i in range(len(edge_type_col)) if valid_mask[i]]

    edge_type_to_idx = {et: i for i, et in enumerate(EDGE_TYPES)}
    edge_type_tensor = torch.tensor(
        [edge_type_to_idx.get(et, 0) for et in edge_type_col],
        dtype=torch.long
    )

    # Temporal features
    ts_col = edges_df.get("ts", None)
    if ts_col is not None:
        ts_values = torch.tensor(ts_col.values[valid_mask], dtype=torch.float)
        if ts_values.max() > ts_values.min():
            ts_values = (ts_values - ts_values.min()) / (ts_values.max() - ts_values.min())
    else:
        ts_values = torch.zeros(src_idx.shape[0], dtype=torch.float)

    # Build HeteroData
    data = HeteroData()
    data["node"].x = x
    data["node"].node_type = node_type_tensor
    data["node"].num_nodes = len(nodes_df)

    for et in EDGE_TYPES:
        mask = edge_type_tensor == edge_type_to_idx.get(et, -1)
        if mask.sum() > 0:
            data["node", et, "node"].edge_index = torch.stack([src_idx[mask], dst_idx[mask]])
            data["node", et, "node"].ts = ts_values[mask]
            data["node", et, "node"].edge_attr = torch.ones(mask.sum(), 1, dtype=torch.float)

    label_col = nodes_df.get("label", None)
    if label_col is not None:
        data["node"].y = torch.tensor(label_col.values, dtype=torch.long)

    return data


class HTGNNAccelerator(nn.Module):
    """Heterogeneous Temporal Graph Attention Network for fraud detection.

    Uses GATConv layers with temporal attention over the ts column.
    Processes each edge type separately and aggregates results.
    """

    def __init__(self, in_channels, hidden_channels, num_layers,
                 dropout=0.3, activation="relu"):
        super().__init__()
        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.num_layers = num_layers

        # Input projection per node type
        self.node_proj = nn.ModuleDict()
        for nt in NODE_TYPES:
            self.node_proj[nt] = Linear(in_channels, hidden_channels)

        # GATConv layers per edge type
        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            layer_convs = nn.ModuleDict()
            for et in EDGE_TYPES:
                layer_convs[et] = GATConv(
                    hidden_channels, hidden_channels // 4,
                    heads=4, dropout=dropout, add_self_loops=False
                )
            self.convs.append(layer_convs)

        # Temporal decay gate
        self.temporal_gate = nn.Sequential(
            nn.Linear(1, hidden_channels),
            nn.Sigmoid()
        )

        # Activation
        if activation == "relu":
            self.activation = F.relu
        elif activation == "gelu":
            self.activation = F.gelu
        else:
            self.activation = F.relu

        self.dropout = nn.Dropout(dropout)

        # Output projection per node type
        self.out_proj = nn.ModuleDict()
        for nt in NODE_TYPES:
            self.out_proj[nt] = Linear(hidden_channels, 2)

    def forward(self, data):
        # Get node features per type
        x_dict = {}
        for nt in NODE_TYPES:
            if nt in data:
                x_dict[nt] = data[nt].x
            else:
                x_dict[nt] = torch.zeros(data["node"].num_nodes, self.in_channels)

        # Project node features
        for nt in NODE_TYPES:
            x_dict[nt] = self.node_proj[nt](x_dict[nt])
            x_dict[nt] = self.activation(x_dict[nt])
            x_dict[nt] = self.dropout(x_dict[nt])

        # GAT propagation per edge type with temporal gating
        for i in range(self.num_layers):
            new_x_dict = {nt: x_dict[nt] for nt in NODE_TYPES}

            for et in EDGE_TYPES:
                edge_key = ("node", et, "node")
                if edge_key in data and data[edge_key].edge_index is not None:
                    edge_index = data[edge_key].edge_index
                    ts = data[edge_key].ts if hasattr(data[edge_key], "ts") else None

                    # Apply temporal gating
                    if ts is not None and ts.numel() > 0:
                        temporal_weight = self.temporal_gate(ts.unsqueeze(-1))
                        # Use temporal weight as edge attribute
                        edge_attr = temporal_weight
                    else:
                        edge_attr = None

                    # Get source node features for this edge type
                    src_nodes = edge_index[0]
                    h_src = x_dict["Account"]

                    # Apply GAT convolution
                    h_updated = self.convs[i][et](
                        x_dict["Account"], edge_index,
                        edge_attr=edge_attr
                    )

                    # Aggregate: add to existing features
                    new_x_dict["Account"] = new_x_dict["Account"] + h_updated

            # Apply activation and dropout
            for nt in NODE_TYPES:
                new_x_dict[nt] = self.activation(new_x_dict[nt])
                new_x_dict[nt] = self.dropout(new_x_dict[nt])

            x_dict = new_x_dict

        # Classification head per node type
        out_dict = {}
        for nt in NODE_TYPES:
            if nt in x_dict:
                out_dict[nt] = self.out_proj[nt](x_dict[nt])

        return out_dict


def train_htgnn(dataset_name, num_epochs=50, learning_rate=0.001):
    """Train HT-GNN on a single ingested dataset."""
    print(f"\n{'='*70}")
    print(f" HT-GNN Training: {dataset_name}")
    print(f"{'='*70}")

    data = build_hetero_data(dataset_name)
    print(f"  Nodes: {data['node'].num_nodes}")

    for et in EDGE_TYPES:
        edge_key = ("node", et, "node")
        if edge_key in data and data[edge_key].edge_index is not None:
            n_edges = data[edge_key].edge_index.shape[1]
            print(f"  {et}: {n_edges:,} edges")

    has_labels = hasattr(data["node"], "y") and data["node"].y is not None
    if has_labels:
        n_pos = (data["node"].y == 1).sum().item()
        n_neg = (data["node"].y == 0).sum().item()
        print(f"  Labels: {n_pos:,} positive, {n_neg:,} negative")

    model = HTGNNAccelerator(
        in_channels=data["node"].x.shape[1] if data["node"].x.dim() > 1 else HIDDEN_CHANNELS,
        hidden_channels=HIDDEN_CHANNELS,
        num_layers=NUM_LAYERS,
        dropout=DROPOUT,
        activation=ACTIVATION,
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.0001)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(1, num_epochs + 1):
        optimizer.zero_grad()
        out_dict = model(data)

        if has_labels and "Account" in out_dict:
            logits = out_dict["Account"]
            labels = data["node"].y
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            if epoch % 10 == 0 or epoch == 1:
                pred = logits.argmax(dim=1)
                acc = (pred == labels).float().mean().item()
                print(f"  Epoch {epoch:3d}/{num_epochs} | Loss: {loss.item():.4f} | Acc: {acc:.4f}")
        else:
            loss = sum(torch.norm(x) for x in out_dict.values()) * 0.001
            loss.backward()
            optimizer.step()
            if epoch % 10 == 0 or epoch == 1:
                print(f"  Epoch {epoch:3d}/{num_epochs} | Unsupervised loss: {loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        out_dict = model(data)
        if "Account" in out_dict:
            risk_scores = F.softmax(out_dict["Account"], dim=1)[:, 1]
            print(f"  Risk scores: min={risk_scores.min():.4f}, max={risk_scores.max():.4f}, "
                  f"mean={risk_scores.mean():.4f}")
            print(f"  High-risk nodes (score > 0.5): {(risk_scores > 0.5).sum().item()}")

    return model, risk_scores if "Account" in out_dict else None


def run_htgnn_pipeline():
    """Run HT-GNN training on all ingested datasets."""
    if not OUTPUT_DIR.exists():
        print("No graph_data directory found. Run Layer 1 ingestion first.")
        return

    datasets = sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()])
    print(f"Found {len(datasets)} dataset(s) in {OUTPUT_DIR}")

    results = {}
    for dataset_name in datasets:
        try:
            model, scores = train_htgnn(dataset_name)
            results[dataset_name] = "SUCCESS"
        except Exception as e:
            print(f"  ❌ {dataset_name} failed: {type(e).__name__}: {e}")
            results[dataset_name] = f"FAILED: {e}"

    print(f"\n{'='*70}")
    print(" HT-GNN PIPELINE COMPLETE ")
    print(f"{'='*70}")
    for name, status in results.items():
        marker = "✅" if status == "SUCCESS" else "❌"
        print(f"  {marker} {name:30s} {status}")


if __name__ == "__main__":
    run_htgnn_pipeline()