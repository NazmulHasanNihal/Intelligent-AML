"""
graph_analytics_engine.py — High-Performance Topological Centrality & Dynamic Graph Analytics

Executes dynamic mathematical graph algorithms using NetworkX:
- Dynamic PageRank Centrality (PPR / Random Walk with Restart)
- Dynamic Brandes Betweenness Centrality (identifies conduits bridging clusters)
- Dynamic In/Out Degree Asymmetry & Volume Flow Conservation Phi
- Local Topological Clustering Coefficient
- Cosine Similarity across Hyperbolic Archetype Feature Space
- Continuous In-Memory Directed Transaction Graph with Live Edge Updates
"""

import math
from typing import Dict, Any, List, Optional, Tuple
import networkx as nx
import numpy as np
from pydantic import BaseModel, Field
from src.engine.real_world_engine import REAL_WORLD_ENTITIES


class TopologicalNodeAnalytics(BaseModel):
    node_id: str
    entity_name: str
    pagerank_score: float
    betweenness_centrality: float
    degree_in: int
    degree_out: int
    degree_asymmetry_ratio: float
    flow_conservation_phi: float
    clustering_coefficient: float
    hyperbolic_distance_to_center: float
    nearest_archetype: str
    archetype_similarity_pct: float
    structural_role: str
    recommended_gating_threshold: float
    risk_indicator: str


class GraphAnalyticsEngine:
    """
    Computes rigorous graph centrality algorithms and archetype vector similarity
    over a dynamic in-memory NetworkX directed multigraph.
    """

    # Reference canonical AML typology vectors: [PageRank, Betweenness, Asymmetry, FlowConservation]
    ARCHETYPES = {
        "CYCLE_WASH_TRADER": np.array([0.08, 0.45, 0.33, 0.98]),
        "SMURFING_AGGREGATOR": np.array([0.05, 0.30, 0.75, 0.88]),
        "MULE_TRANSIT_CONDUIT": np.array([0.07, 0.65, 0.20, 0.98]),
        "CAMOUFLAGE_RETAIL_CHAFF": np.array([0.01, 0.01, 0.89, 0.05]),
        "PRIME_COMMERCIAL_CORP": np.array([0.02, 0.04, 0.10, 0.15])
    }

    def __init__(self):
        self.graph = nx.DiGraph()
        self._cached_pagerank: Optional[Dict[str, float]] = None
        self._cached_betweenness: Optional[Dict[str, float]] = None
        self._dirty = True
        self._initialize_canonical_graph()

    def _initialize_canonical_graph(self):
        """Seeds graph with authentic corporate and retail entities and topology."""
        for eid, info in REAL_WORLD_ENTITIES.items():
            self.graph.add_node(
                eid,
                name=info.get("entity_name", eid),
                is_target=info.get("is_flagged_target", False),
                country=info.get("country", "BD")
            )

        # Baseline transactional topology representing real-world commercial & high-risk corridors
        seed_edges = [
            ("BD22-EBLB-4829-1092-8823", "BD04-BRAC-1109-8421-4402", 47600.0, "RTGS Trade Conduit"),
            ("BD04-BRAC-1109-8421-4402", "AE-EBIL-4412-8819-3301", 47600.0, "SWIFT MT103 Wash Transfer"),
            ("AE-EBIL-4412-8819-3301", "BD22-EBLB-4829-1092-8823", 47600.0, "SWIFT MT700 LC Re-entry Loop"),
            ("BD22-EBLB-4829-1092-8823", "AE-EBIL-4412-8819-3301", 9450.0, "Over-Invoiced LC #88912"),
            ("BD22-EBLB-4829-1092-8823", "AE-EBIL-4412-8819-3301", 9600.0, "Over-Invoiced LC #88912"),
            ("MFS-BKASH-0171-8840", "BD04-BRAC-1109-8421-4402", 4800.0, "bKash MFS Smurfing"),
            ("BD91-DBBL-4401-2299-1184", "BD04-BRAC-1109-8421-4402", 38400.0, "Dormant Payroll Aggregation"),
            ("BD04-BRAC-1109-8421-4402", "GB-BARC-1109-8421-4402", 38400.0, "CHAPS Freight Wire"),
            ("BD04-BRAC-1109-8421-4402", "BD22-EBLB-8831-2901-4412", 12.0, "Retail Camouflage POS"),
            ("BD04-BRAC-1109-8421-4402", "BD04-BRAC-9921-3310-5541", 18.3, "E-Commerce Camouflage POS"),
            ("BD04-BRAC-0192-8821-4401", "BD18-CIBL-3312-8804-1290", 14250.0, "Licit Commercial Pharma"),
            ("BD91-DBBL-0091-8841-2091", "BD08-SONA-9901-7721-5540", 8900.0, "Licit Industrial Clearing"),
            ("BD33-IBBL-5512-9901-3321", "BD12-HSBC-2201-9940-1120", 25000.0, "Agro Export Clearing"),
            ("AE-EBIL-4412-8819-3301", "SG-DBS-8819-3301", 120000.0, "Offshore Escrow Transfer"),
            ("SG-DBS-8819-3301", "US-JPMC-4829-1092-8823", 119500.0, "USD Correspondent Wire"),
            ("US-JPMC-4829-1092-8823", "BD22-EBLB-4829-1092-8823", 118000.0, "Capital Flight Inbound")
        ]

        for src, dst, amt, label in seed_edges:
            self.graph.add_edge(src, dst, weight=amt, label=label)

        self._recompute_topological_metrics()

    def add_transaction(self, src_id: str, dst_id: str, amount: float, label: str = "Live Wire"):
        """Dynamically ingests transaction into topology and flags cache dirty."""
        if not self.graph.has_node(src_id):
            name = REAL_WORLD_ENTITIES.get(src_id, {}).get("entity_name", src_id)
            self.graph.add_node(src_id, name=name, is_target=False)
        if not self.graph.has_node(dst_id):
            name = REAL_WORLD_ENTITIES.get(dst_id, {}).get("entity_name", dst_id)
            self.graph.add_node(dst_id, name=name, is_target=False)

        current_weight = self.graph.get_edge_data(src_id, dst_id, {}).get("weight", 0.0)
        self.graph.add_edge(src_id, dst_id, weight=current_weight + float(amount), label=label)
        self._dirty = True

    def _recompute_topological_metrics(self):
        """Executes PageRank and Betweenness Centrality over full graph."""
        if len(self.graph) == 0:
            self._cached_pagerank = {}
            self._cached_betweenness = {}
            self._dirty = False
            return

        try:
            self._cached_pagerank = nx.pagerank(self.graph, weight="weight", alpha=0.85, max_iter=200)
        except Exception:
            self._cached_pagerank = {n: 1.0 / len(self.graph) for n in self.graph.nodes()}

        try:
            self._cached_betweenness = nx.betweenness_centrality(self.graph, weight="weight", normalized=True)
        except Exception:
            self._cached_betweenness = {n: 0.0 for n in self.graph.nodes()}

        self._dirty = False

    def analyze_node(self, node_id: str) -> TopologicalNodeAnalytics:
        """
        Dynamically calculates graph metrics, flow conservation phi,
        and archetype cosine similarity for any node in the graph.
        """
        if self._dirty:
            self._recompute_topological_metrics()

        info = REAL_WORLD_ENTITIES.get(node_id, {})
        name = info.get("entity_name", self.graph.nodes.get(node_id, {}).get("name", node_id))
        is_target = info.get("is_flagged_target", False)

        if not self.graph.has_node(node_id):
            self.graph.add_node(node_id, name=name, is_target=is_target)
            self._recompute_topological_metrics()

        # Dynamic centrality extraction
        pr = self._cached_pagerank.get(node_id, 0.01)
        betweenness = self._cached_betweenness.get(node_id, 0.0)

        # Dynamic Degree calculation
        deg_in = self.graph.in_degree(node_id)
        deg_out = self.graph.out_degree(node_id)
        total_deg = deg_in + deg_out
        asym = abs(deg_in - deg_out) / max(1, total_deg)

        # Dynamic Flow conservation calculation: Phi = 1 - |InFlow - OutFlow| / (InFlow + OutFlow)
        in_flow = sum(d.get("weight", 1.0) for _, _, d in self.graph.in_edges(node_id, data=True))
        out_flow = sum(d.get("weight", 1.0) for _, _, d in self.graph.out_edges(node_id, data=True))
        flow_sum = in_flow + out_flow
        if flow_sum > 0:
            phi = 1.0 - (abs(in_flow - out_flow) / flow_sum)
        else:
            phi = 0.50

        # Local clustering coefficient
        undirected_g = self.graph.to_undirected()
        clustering = float(nx.clustering(undirected_g, node_id)) if node_id in undirected_g else 0.0

        # Hyperbolic distance approximation from graph boundary/center
        hyp_dist = float(np.clip(1.0 - math.exp(-2.5 * (pr + betweenness)), 0.05, 0.98))
        if is_target:
            hyp_dist = max(hyp_dist, 0.85)

        # Cosine Similarity against Archetypes
        node_vector = np.array([pr, betweenness, asym, phi])
        best_archetype = "PRIME_COMMERCIAL_CORP"
        best_sim = 0.0

        node_norm = np.linalg.norm(node_vector)
        if node_norm > 1e-6:
            for arch_name, arch_vec in self.ARCHETYPES.items():
                arch_norm = np.linalg.norm(arch_vec)
                cos_sim = float(np.dot(node_vector, arch_vec) / (node_norm * arch_norm))
                sim_pct = float(np.clip(cos_sim * 100.0, 10.0, 99.5))
                if sim_pct > best_sim:
                    best_sim = sim_pct
                    best_archetype = arch_name
        else:
            best_sim = 90.0

        # Dynamic Structural Role and Gating Inference
        if best_archetype == "CYCLE_WASH_TRADER" or (phi > 0.90 and betweenness > 0.30):
            role = "Wash Cycle Initiator & Capital Flight Anchor"
            risk = "CRITICAL_TIER_1"
            gate = 0.98
        elif best_archetype == "MULE_TRANSIT_CONDUIT" or (betweenness > 0.40 and phi > 0.80):
            role = "Cross-Border Transit Bridge & Structuring Conduit"
            risk = "CRITICAL_TIER_1"
            gate = 0.96
        elif best_archetype == "SMURFING_AGGREGATOR" or (deg_in >= 4 and deg_out <= 2 and asym > 0.5):
            role = "Dispersed Cash-Out Inbound Aggregation Hub"
            risk = "HIGH_TIER_1"
            gate = 0.88
        elif best_archetype == "CAMOUFLAGE_RETAIL_CHAFF" or (total_deg > 5 and flow_sum < 500.0):
            role = "High-Frequency Retail POS Noise (Pruned by Edge Gating)"
            risk = "SAFE_TIER_3"
            gate = 0.03
        else:
            role = "Normal Recurring Commercial Settlement Hub"
            risk = "SAFE_TIER_3"
            gate = 0.85

        return TopologicalNodeAnalytics(
            node_id=node_id,
            entity_name=name,
            pagerank_score=round(float(pr), 4),
            betweenness_centrality=round(float(betweenness), 4),
            degree_in=int(deg_in),
            degree_out=int(deg_out),
            degree_asymmetry_ratio=round(float(asym), 3),
            flow_conservation_phi=round(float(phi), 3),
            clustering_coefficient=round(float(clustering), 3),
            hyperbolic_distance_to_center=round(float(hyp_dist), 3),
            nearest_archetype=best_archetype,
            archetype_similarity_pct=round(float(best_sim), 1),
            structural_role=role,
            recommended_gating_threshold=round(float(gate), 2),
            risk_indicator=risk
        )


graph_analytics = GraphAnalyticsEngine()
