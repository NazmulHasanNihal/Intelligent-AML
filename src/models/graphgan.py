"""
GraphGAN: Generative Adversarial Network for Graph Subgraph Generation
Layer 2 — Detection & Rebalancing

Generates structurally valid synthetic subgraphs that mimic the
topology and feature distributions of real fraud patterns.
"""

import os
import random
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

    # Standardize nodes columns case-insensitively
    nodes_df = nodes_df.rename(columns={c: c.strip() for c in nodes_df.columns})
    edges_df = edges_df.rename(columns={c: c.strip() for c in edges_df.columns})

    # Normalize ID columns: txId/nodeId to node_id
    for col in ["txId", "nodeId", "txid", "nodeid"]:
        if col in nodes_df.columns and "node_id" not in nodes_df.columns:
            nodes_df = nodes_df.rename(columns={col: "node_id"})
        if col in edges_df.columns and "node_id" not in edges_df.columns:
            edges_df = edges_df.rename(columns={col: "node_id"})

    node_features = nodes_df.drop(columns=[c for c in nodes_df.columns
                                            if c in ("node_id", "node_type", "label", "time_step")],
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
        # Convert class string labels to integer labels if applicable
        labels = nodes_df["label"]
        if labels.dtype == object:
            labels = labels.map({"1": 1, "2": 0, 1: 1, 0: 0}).fillna(-1)
        data["node"].y = torch.tensor(labels.values, dtype=torch.long)

    return data


def extract_fraud_subgraph(data, num_nodes=50):
    """
    Extracts a subgraph centered around fraud nodes (label == 1)
    to train GraphGAN without memory exhaustion.
    """
    x = data["node"].x
    edge_index = data["node", "Transaction", "node"].edge_index
    y = data["node"].y if hasattr(data["node"], "y") else None

    num_total_nodes = x.shape[0]

    # Find fraud seeds
    if y is not None and (y == 1).sum() > 0:
        fraud_indices = torch.where(y == 1)[0].tolist()
    else:
        # Fallback to random seeds if no labels exist
        fraud_indices = torch.randperm(num_total_nodes)[:10].tolist()

    # Expand neighborhood starting from seeds until we reach num_nodes
    selected_nodes = set()
    random.shuffle(fraud_indices)
    
    for seed in fraud_indices:
        if len(selected_nodes) >= num_nodes:
            break
        selected_nodes.add(seed)
        
        # 1-hop neighbors
        neighbors = edge_index[1, edge_index[0] == seed].tolist()
        neighbors_rev = edge_index[0, edge_index[1] == seed].tolist()
        for n in neighbors + neighbors_rev:
            if len(selected_nodes) >= num_nodes:
                break
            selected_nodes.add(n)

    # If we still need more nodes, fill with random nodes
    if len(selected_nodes) < num_nodes:
        all_nodes = list(range(num_total_nodes))
        random.shuffle(all_nodes)
        for n in all_nodes:
            if len(selected_nodes) >= num_nodes:
                break
            selected_nodes.add(n)

    # Create subgraph mapping
    sub_nodes = sorted(list(selected_nodes))
    node_map = {old: new for new, old in enumerate(sub_nodes)}

    # Filter features
    sub_x = x[sub_nodes]
    if y is not None:
        sub_y = y[sub_nodes]
    else:
        sub_y = None

    # Filter edges
    mask = torch.isin(edge_index[0], torch.tensor(sub_nodes)) & torch.isin(edge_index[1], torch.tensor(sub_nodes))
    sub_edges_old = edge_index[:, mask]
    
    # Map edges to relative indices
    src_mapped = torch.tensor([node_map[nid.item()] for nid in sub_edges_old[0]], dtype=torch.long)
    dst_mapped = torch.tensor([node_map[nid.item()] for nid in sub_edges_old[1]], dtype=torch.long)
    sub_edge_index = torch.stack([src_mapped, dst_mapped])

    return sub_x, sub_edge_index, sub_y


class GraphGANGenerator(nn.Module):
    """Generator: maps latent noise to synthetic node features and edge probabilities."""

    def __init__(self, latent_dim, hidden_dim, num_nodes):
        super().__init__()
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        self.num_nodes = num_nodes

        # Node feature generator: maps latent noise to individual node features
        self.node_gen = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, z):
        """Generate synthetic node features and edge probabilities.

        Parameters
        ----------
        z : torch.Tensor
            Latent noise, shape (batch_size, num_nodes, latent_dim)

        Returns
        -------
        node_features : torch.Tensor
            Synthetic node features, shape (batch_size, num_nodes, hidden_dim)
        edge_probs : torch.Tensor
            Edge existence probabilities, shape (batch_size, num_nodes, num_nodes)
        """
        batch_size = z.shape[0]
        
        # Flatten batch and node dimensions to project noise independently
        z_flat = z.view(-1, self.latent_dim)
        node_features_flat = self.node_gen(z_flat)
        node_features = node_features_flat.view(batch_size, self.num_nodes, self.hidden_dim)

        # Bilinear dot product edge decoder: scores each node pair (i, j)
        # Scaled dot product to prevent gradient saturation before sigmoid
        scores = torch.matmul(node_features, node_features.transpose(1, 2)) / (self.hidden_dim ** 0.5)
        edge_probs = torch.sigmoid(scores)

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

        if edge_index.numel() > 0:
            src = edge_index[0]
            dst = edge_index[1]
            edge_feat = torch.cat([node_features[src], node_features[dst]], dim=-1)
            edge_score = self.edge_disc(edge_feat).squeeze(-1)
        else:
            edge_score = torch.zeros(0, device=node_features.device)

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
    """Train GraphGAN on a single extracted fraud subgraph."""
    print(f"\n{'='*70}")
    print(f" GraphGAN Training: {dataset_name}")
    print(f"{'='*70}")

    data = build_hetero_data(dataset_name)
    
    # Extract tight fraud subgraph to avoid OOM memory issues
    real_x, real_edge_index, _ = extract_fraud_subgraph(data, num_nodes=num_nodes)
    actual_nodes = real_x.shape[0]
    print(f"  Extracted Subgraph size: {actual_nodes} nodes, {real_edge_index.shape[1]} edges")

    device = torch.device("cpu")
    model = GraphGAN(latent_dim=latent_dim, hidden_dim=HIDDEN_DIM, num_nodes=actual_nodes).to(device)
    
    # Feature dimension project to map real_x to GAN's HIDDEN_DIM
    in_dim = real_x.shape[1]
    feature_proj = nn.Linear(in_dim, HIDDEN_DIM).to(device)
    
    optimizer_G = torch.optim.Adam(list(model.generator.parameters()) + list(feature_proj.parameters()), lr=lr, betas=(0.5, 0.999))
    optimizer_D = torch.optim.Adam(model.discriminator.parameters(), lr=lr, betas=(0.5, 0.999))

    real_edge_index = real_edge_index.to(device)
    
    # Build target dense adjacency matrix for supervised topology alignment
    real_adj = torch.zeros(actual_nodes, actual_nodes, device=device)
    if real_edge_index.numel() > 0:
        real_adj[real_edge_index[0], real_edge_index[1]] = 1.0

    model.train()
    for epoch in range(1, num_epochs + 1):
        real_node_features = feature_proj(real_x.to(device))
        
        # Train discriminator
        for _ in range(CRITIC_ITERATIONS):
            optimizer_D.zero_grad()

            # Generate batch size = 1 synthetic graph matching real size
            noise = torch.randn(1, actual_nodes, latent_dim, device=device)
            fake_node_features_batch, fake_edge_probs_batch = model.generator(noise)
            fake_node_features = fake_node_features_batch.squeeze(0)

            # Sample fake edge indices from highest probabilities
            flat_probs = fake_edge_probs_batch.squeeze(0).view(-1)
            num_edges = real_edge_index.shape[1]
            topk_vals, topk_indices = torch.topk(flat_probs, k=min(num_edges, flat_probs.numel()))
            fake_src = topk_indices // actual_nodes
            fake_dst = topk_indices % actual_nodes
            fake_edge_index = torch.stack([fake_src, fake_dst])

            real_node_score, real_edge_score = model.discriminator(real_node_features, real_edge_index)
            fake_node_score, fake_edge_score = model.discriminator(fake_node_features.detach(), fake_edge_index)

            d_loss = -(real_node_score.mean() + real_edge_score.mean() -
                       fake_node_score.mean() - fake_edge_score.mean())
            d_loss.backward()
            optimizer_D.step()

            # Soft clamp critic parameters (WGAN constraint)
            for p in model.discriminator.parameters():
                p.data.clamp_(-WASHERSTEIN_CLIP, WASHERSTEIN_CLIP)

        # Train generator
        optimizer_G.zero_grad()
        noise = torch.randn(1, actual_nodes, latent_dim, device=device)
        fake_node_features_batch, fake_edge_probs_batch = model.generator(noise)
        fake_node_features = fake_node_features_batch.squeeze(0)
        fake_edge_probs = fake_edge_probs_batch.squeeze(0)

        # Sample fake edges
        flat_probs = fake_edge_probs.view(-1)
        topk_vals, topk_indices = torch.topk(flat_probs, k=min(num_edges, flat_probs.numel()))
        fake_src = topk_indices // actual_nodes
        fake_dst = topk_indices % actual_nodes
        fake_edge_index = torch.stack([fake_src, fake_dst])

        fake_node_score, fake_edge_score = model.discriminator(fake_node_features, fake_edge_index)

        # Joint loss: adversarial + reconstruction topology loss
        adv_loss = -(fake_node_score.mean() + fake_edge_score.mean())
        topo_loss = F.binary_cross_entropy(fake_edge_probs, real_adj)
        g_loss = adv_loss + 10.0 * topo_loss
        
        g_loss.backward()
        optimizer_G.step()

        if epoch % 20 == 0 or epoch == 1:
            print(f"  Epoch {epoch:3d}/{num_epochs} | D loss: {d_loss.item():.4f} | G loss: {g_loss.item():.4f} | Topology Loss: {topo_loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        noise = torch.randn(1, actual_nodes, latent_dim, device=device)
        synth_node_features, synth_edge_probs = model.generator(noise)
        synth_node_features = synth_node_features.squeeze(0)
        synth_edge_probs = synth_edge_probs.squeeze(0)
        
        # Evaluate feature distribution fidelity using Maximum Mean Discrepancy (MMD)
        mmd_score = compute_maximum_mean_discrepancy(real_features, synth_node_features)
        print(f"  Synthetic subgraph generated: {actual_nodes} nodes")
        print(f"  Edge probability range: [{synth_edge_probs.min():.4f}, {synth_edge_probs.max():.4f}]")
        print(f"  Node Feature MMD Discrepancy: {mmd_score:.4f} (Target < 0.05)")

    return model, synth_node_features, synth_edge_probs


def compute_maximum_mean_discrepancy(x: torch.Tensor, y: torch.Tensor, gamma: float = 1.0) -> float:
    """
    Computes Maximum Mean Discrepancy (MMD) between empirical and synthetic feature distributions
    using a multi-scale Gaussian RBF kernel.
    Target: MMD < 0.05 indicates high feature fidelity.
    """
    x = x.view(x.size(0), -1)
    y = y.view(y.size(0), -1)
    
    # Pairwise squared Euclidean distances
    xx = torch.cdist(x, x, p=2) ** 2
    yy = torch.cdist(y, y, p=2) ** 2
    xy = torch.cdist(x, y, p=2) ** 2
    
    # Multi-scale bandwidths
    gammas = [gamma * 0.1, gamma * 0.5, gamma * 1.0, gamma * 2.0, gamma * 5.0]
    mmd2 = 0.0
    for g in gammas:
        k_xx = torch.exp(-g * xx)
        k_yy = torch.exp(-g * yy)
        k_xy = torch.exp(-g * xy)
        mmd2 += k_xx.mean() + k_yy.mean() - 2.0 * k_xy.mean()
        
    mmd2 = mmd2 / len(gammas)
    return float(torch.sqrt(torch.clamp(mmd2, min=0.0)).item())



def run_graphgan_pipeline():
    """Run GraphGAN training on all ingested datasets."""
    if not OUTPUT_DIR.exists():
        print("No graph_data directory found. Run Layer 1 Ingestion first.")
        return

    datasets = sorted([d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()])
    print(f"Found {len(datasets)} dataset(s) in {OUTPUT_DIR}")

    results = {}
    for dataset_name in datasets:
        if dataset_name not in ["elliptic_v1", "paysim1"]:
            continue
        try:
            model, node_feat, edge_prob = train_graphgan(dataset_name, num_nodes=50)
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