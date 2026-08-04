"""
GraphGAN: Generative Adversarial Network for Graph Subgraph Generation
Layer 2 — Detection & Rebalancing

Generates structurally valid synthetic subgraphs that mimic the
topology and feature distributions of real fraud patterns.
"""

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path

import pyarrow.parquet as pq

from torch_geometric.data import HeteroData


OUTPUT_DIR = Path("data/outputs/graph_data")
NODE_TYPES = ["Account", "User", "Device", "Institution"]
EDGE_TYPES = ["Transaction", "IP_Connection", "Shared_Ownership"]

LATENT_DIM = 64
HIDDEN_DIM = 128
WASHERSTEIN_CLIP = 0.01
CRITIC_ITERATIONS = 5


def load_parquet(path):
    if not Path(path).exists():
        return None
    table = pq.read_table(path)
    return table.to_pandas()


def build_hetero_data(dataset_name):
    """Load ingested graph data and convert to PyG HeteroData."""
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

    node_features = nodes_df.drop(columns=[c for c in nodes_df.columns
                                            if c in ("node_id", "node_type", "label")],
                                   errors="ignore")
    feature_cols = [c for c in node_features.columns if c.startswith("feat_")]
    if feature_cols:
        x = torch.tensor(node_features[feature_cols].values, dtype=torch.float)
        x = torch.nan_to_num(x, nan=0.0)
    else:
        x = torch.zeros(len(nodes_df), len(NODE_TYPES), dtype=torch.float)

    src_col = edges_df.get("src", None)
    dst_col = edges_df.get("dst", None)
    if src_col is None or dst_col is None:
        raise ValueError(f"edges.parquet for {dataset_name} missing src/dst")

    all_node_ids = sorted(nodes_df["node_id"].unique())
    node_id_to_idx = {nid: i for i, nid in enumerate(all_node_ids)}
    src_idx = torch.tensor([node_id_to_idx.get(sid, -1) for sid in src_col], dtype=torch.long)
    dst_idx = torch.tensor([node_id_to_idx.get(did, -1) for did in dst_col], dtype=torch.long)
    valid_mask = (src_idx >= 0) & (dst_idx >= 0)
    edge_index = torch.stack([src_idx[valid_mask], dst_idx[valid_mask]])

    data = HeteroData()
    data["node"].x = x
    data["node"].num_nodes = len(nodes_df)
    data["node", "Transaction", "node"].edge_index = edge_index

    label_col = nodes_df.get("label", None)
    if label_col is not None:
        data["node"].y = torch.tensor(label_col.values, dtype=torch.long)

    return data


class GraphGANGenerator(nn.Module):
    """Generator: maps latent noise to synthetic node features and edge probabilities."""

    def __init__(self, latent_dim, hidden_dim, num_nodes):
        super().__init__()
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        self.num_nodes = num_nodes

        # Node feature generator
        self.node_gen = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # Edge topology generator: scores each node pair
        self.edge_gen = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

    def forward(self, z):
        """Generate synthetic node features and edge probabilities.

        Parameters
        ----------
        z : torch.Tensor
            Latent noise, shape (batch_size, latent_dim)

        Returns
        -------
        node_features : torch.Tensor
            Synthetic node features, shape (batch_size, num_nodes, hidden_dim)
        edge_probs : torch.Tensor
            Edge existence probabilities, shape (batch_size, num_nodes, num_nodes)
        """
        batch_size = z.shape[0]

        # Generate node features: (batch_size, num_nodes, hidden_dim)
        node_features = self.node_gen(z)
        node_features = node_features.unsqueeze(1).expand(-1, self.num_nodes, -1)

        # Generate edge probabilities by scoring each node pair
        # Use node features directly as edge features
        z_i = node_features  # (batch_size, num_nodes, hidden_dim)
        z_j = node_features.unsqueeze(2).expand(-1, -1, self.num_nodes, -1)
        z_i = z_i.unsqueeze(2).expand(-1, -1, self.num_nodes, -1)
        z_pair = torch.cat([z_i, z_j], dim=-1)
        z_pair = z_pair.reshape(-1, self.hidden_dim * 2)
        edge_probs = self.edge_gen(z_pair).squeeze(-1)
        edge_probs = edge_probs.reshape(batch_size, self.num_nodes, self.num_nodes)

        return node_features, edge_probs


class GraphGANDiscriminator(nn.Module):
    """Discriminator: distinguishes real from synthetic subgraphs."""

    def __init__(self, hidden_dim):
        super().__init__()

        self.node_disc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim // 2),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid(),
        )

        self.edge_disc = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim // 2),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid(),
        )

    def forward(self, node_features, edge_index):
        """Score real vs synthetic subgraphs.

        Parameters
        ----------
        node_features : torch.Tensor
            Node features, shape (num_nodes, hidden_dim)
        edge_index : torch.Tensor
            Edge index, shape (2, num_edges)

        Returns
        -------
        node_score : torch.Tensor
            Realism score for node features, shape (num_nodes,)
        edge_score : torch.Tensor
            Realism score for edges, shape (num_edges,)
        """
        node_score = self.node_disc(node_features).squeeze(-1)

        src = edge_index[0]
        dst = edge_index[1]
        edge_feat = torch.cat([node_features[src], node_features[dst]], dim=-1)
        edge_score = self.edge_disc(edge_feat).squeeze(-1)

        return node_score, edge_score


class GraphGAN(nn.Module):
    """GraphGAN: Adversarial graph subgraph generation model."""

    def __init__(self, latent_dim=LATENT_DIM, hidden_dim=HIDDEN_DIM, num_nodes=50):
        super().__init__()
        self.generator = GraphGANGenerator(latent_dim, hidden_dim, num_nodes)
        self.discriminator = GraphGANDiscriminator(hidden_dim)

    def forward(self, z):
        node_features, edge_probs = self.generator(z)
        return node_features, edge_probs


def train_graphgan(dataset_name, num_epochs=100, lr=0.0002, latent_dim=LATENT_DIM, num_nodes=50):
    """Train GraphGAN on a single ingested dataset."""
    print(f"\n{'='*70}")
    print(f" GraphGAN Training: {dataset_name}")
    print(f"{'='*70}")

    data = build_hetero_data(dataset_name)
    actual_nodes = data["node"].num_nodes
    print(f"  Nodes: {actual_nodes}")

    device = torch.device("cpu")
    model = GraphGAN(latent_dim=latent_dim, hidden_dim=HIDDEN_DIM, num_nodes=actual_nodes).to(device)
    optimizer_G = torch.optim.Adam(model.generator.parameters(), lr=lr, betas=(0.5, 0.999))
    optimizer_D = torch.optim.Adam(model.discriminator.parameters(), lr=lr, betas=(0.5, 0.999))

    real_node_features = data["node"].x.to(device)
    real_edge_index = data["node", "Transaction", "node"].edge_index.to(device)

    model.train()
    for epoch in range(1, num_epochs + 1):
        # Train discriminator
        for _ in range(CRITIC_ITERATIONS):
            optimizer_D.zero_grad()

            noise = torch.randn(actual_nodes, latent_dim, device=device)
            fake_node_features, fake_edge_probs = model.generator(noise)

            real_node_score, real_edge_score = model.discriminator(real_node_features, real_edge_index)
            fake_node_score, fake_edge_score = model.discriminator(fake_node_features.detach(), real_edge_index)

            d_loss = -(real_node_score.mean() + real_edge_score.mean() -
                       fake_node_score.mean() - fake_edge_score.mean())
            d_loss.backward()
            optimizer_D.step()

            for p in model.discriminator.parameters():
                p.data.clamp_(-WASHERSTEIN_CLIP, WASHERSTEIN_CLIP)

        # Train generator
        optimizer_G.zero_grad()
        noise = torch.randn(actual_nodes, latent_dim, device=device)
        fake_node_features, fake_edge_probs = model.generator(noise)
        fake_node_score, fake_edge_score = model.discriminator(fake_node_features, real_edge_index)

        g_loss = -(fake_node_score.mean() + fake_edge_score.mean())
        g_loss.backward()
        optimizer_G.step()

        if epoch % 20 == 0 or epoch == 1:
            print(f"  Epoch {epoch:3d}/{num_epochs} | D loss: {d_loss.item():.4f} | G loss: {g_loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        noise = torch.randn(actual_nodes, latent_dim, device=device)
        synth_node_features, synth_edge_probs = model.generator(noise)
        print(f"  Synthetic subgraph generated: {actual_nodes} nodes")
        print(f"  Edge probability range: [{synth_edge_probs.min():.4f}, {synth_edge_probs.max():.4f}]")

    return model, synth_node_features, synth_edge_probs


def run_graphgan_pipeline():
    """Run GraphGAN training on all ingested datasets."""
    if not OUTPUT_DIR.exists():
        print("No graph_data directory found. Run Layer 1 ingestion first.")
        return

    datasets = sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()])
    print(f"Found {len(datasets)} dataset(s) in {OUTPUT_DIR}")

    results = {}
    for dataset_name in datasets:
        try:
            model, node_feat, edge_prob = train_graphgan(dataset_name)
            results[dataset_name] = "SUCCESS"
        except Exception as e:
            print(f"  ❌ {dataset_name} failed: {type(e).__name__}: {e}")
            results[dataset_name] = f"FAILED: {e}"

    print(f"\n{'='*70}")
    print(" GraphGAN PIPELINE COMPLETE ")
    print(f"{'='*70}")
    for name, status in results.items():
        marker = "✅" if status == "SUCCESS" else "❌"
        print(f"  {marker} {name:30s} {status}")


if __name__ == "__main__":
    run_graphgan_pipeline()