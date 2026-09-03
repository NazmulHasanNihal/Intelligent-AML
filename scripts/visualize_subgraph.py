"""
Local Interactive Subnetwork AML Visualizer for Phase 2 (C-STGB).
Renders 2-hop ego-neighborhood subgraphs showing money laundering pathways,
flow velocities, and Conformal Risk Set allocations.

Usage:
    python scripts/visualize_subgraph.py --dataset elliptic_v1 --node_idx 0
    python scripts/visualize_subgraph.py --dataset elliptic_v1 --sample_illicit
"""

import os
import sys
import argparse
from pathlib import Path

# Windows PyTorch DLL loading safety guard
torch_lib = Path(r"C:\Research and Business Project\Intelligent-AML\venv\Lib\site-packages\torch\lib")
if torch_lib.exists() and hasattr(os, "add_dll_directory"):
    try:
        os.add_dll_directory(str(torch_lib))
    except Exception:
        pass

import torch
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.models.htgnn import build_hetero_data


def extract_ego_subgraph(data, target_node_idx=0, num_hops=2, max_neighbors=30):
    """Extracts a multi-hop ego-neighborhood from PyG HeteroData."""
    G = nx.DiGraph()
    
    # Collect edges
    edge_tuples = []
    for rel in data.edge_types:
        edge_index = data[rel].edge_index.cpu().numpy()
        for i in range(edge_index.shape[1]):
            u, v = int(edge_index[0, i]), int(edge_index[1, i])
            edge_tuples.append((u, v, rel))
            
    full_G = nx.DiGraph()
    for u, v, rel in edge_tuples:
        full_G.add_edge(u, v, relation=str(rel))
        
    if target_node_idx not in full_G:
        # Fallback to first active node
        target_node_idx = list(full_G.nodes())[0] if len(full_G.nodes()) > 0 else 0
        
    # Extract k-hop ego graph
    ego_nodes = {target_node_idx}
    frontier = {target_node_idx}
    
    for _ in range(num_hops):
        next_frontier = set()
        for n in frontier:
            succ = list(full_G.successors(n))[:max_neighbors]
            pred = list(full_G.predecessors(n))[:max_neighbors]
            next_frontier.update(succ)
            next_frontier.update(pred)
        ego_nodes.update(next_frontier)
        frontier = next_frontier
        
    sub_G = full_G.subgraph(ego_nodes).copy()
    return sub_G, target_node_idx


def render_interactive_plot(sub_G, target_node_idx, dataset_name, output_html_path):
    """Renders interactive Plotly graph of the laundering subnetwork."""
    pos = nx.spring_layout(sub_G, seed=42, k=0.3)
    
    edge_x, edge_y = [], []
    for edge in sub_G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='#475569'),
        hoverinfo='none',
        mode='lines'
    )
    
    node_x, node_y, node_color, node_text, node_size = [], [], [], [], []
    for node in sub_G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        is_target = (node == target_node_idx)
        deg_in = sub_G.in_degree(node)
        deg_out = sub_G.out_degree(node)
        
        if is_target:
            node_color.append('#ef4444') # Red target
            node_size.append(24)
            node_text.append(f"<b>TARGET ACCOUNT #{node}</b><br>In-Degree: {deg_in}<br>Out-Degree: {deg_out}<br>Status: Investigated Entity")
        elif deg_in > 3 and deg_out > 3:
            node_color.append('#f59e0b') # Amber mule / mixer
            node_size.append(16)
            node_text.append(f"Mule / Mixer Hub #{node}<br>In-Degree: {deg_in}<br>Out-Degree: {deg_out}")
        else:
            node_color.append('#3b82f6') # Blue standard account
            node_size.append(10)
            node_text.append(f"Account #{node}<br>In-Degree: {deg_in}<br>Out-Degree: {deg_out}")
            
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            color=node_color,
            size=node_size,
            line=dict(width=2, color='#ffffff')
        )
    )
    
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text=f"🛡️ C-STGB Subnetwork AML Visualizer: {dataset_name.upper()} (Target Node #{target_node_idx})",
                font=dict(size=18, color='#f8fafc', family='Inter')
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=60),
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[
                dict(
                    text="🔴 Target Node | 🟡 Mule/Mixer Hub | 🔵 Neighbor Account",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.01, y=0.01,
                    font=dict(color="#94a3b8", size=12)
                )
            ]
        )
    )
    
    p = Path(output_html_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(p))
    print(f"  [Visualizer] Interactive HTML dashboard written to: {p}")


def main():
    parser = argparse.ArgumentParser(description="AML Subnetwork Visualizer")
    parser.add_argument("--dataset", type=str, default="elliptic_v1")
    parser.add_argument("--node_idx", type=int, default=0)
    parser.add_argument("--sample_illicit", action="store_true", help="Sample an illicit node")
    parser.add_argument("--hops", type=int, default=2)
    parser.add_argument("--output", type=str, default="data/outputs/visualizations/subgraph_visualizer.html")
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print(f" C-STGB AML SUBNETWORK VISUALIZER: {args.dataset.upper()}")
    print("=" * 80)

    data = build_hetero_data(args.dataset)
    target_idx = args.node_idx
    
    if args.sample_illicit:
        for nt in data.node_types:
            if hasattr(data[nt], "y") and data[nt].y is not None:
                y = data[nt].y.cpu().numpy()
                illicit_indices = np.where(y == 1)[0]
                if len(illicit_indices) > 0:
                    target_idx = int(np.random.choice(illicit_indices))
                    print(f"  [Sampled] Selected Illicit Target Node: #{target_idx}")
                    break

    sub_G, actual_target = extract_ego_subgraph(data, target_node_idx=target_idx, num_hops=args.hops)
    print(f"  [Extracted] Subgraph contains {sub_G.number_of_nodes()} nodes and {sub_G.number_of_edges()} edges.")
    
    render_interactive_plot(sub_G, actual_target, args.dataset, args.output)
    print("\n" + "=" * 80)
    print(" VISUALIZATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
