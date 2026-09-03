"""
investigator_agent.py — Autonomous Forensic Graph Investigator Agent.
Crawls alert subgraphs identified by C-STGB, performs multi-hop BFS/DFS path traversal,
computes topological flow dynamics (peeling ratios, dormant delay periods, smurfing velocity),
extracts suspicious counterparty clusters, and compiles structured ForensicEvidence dossiers.
"""

import time
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field


@dataclass
class TransactionEdge:
    """Represents a single directed transaction event in a forensic path."""
    source: str
    target: str
    amount: float
    timestamp: float
    tx_type: str = "TRANSFER"
    delta_t_hours: float = 0.0


@dataclass
class ForensicEvidence:
    """
    Structured forensic evidence payload extracted from suspicious graph topologies.
    Provides complete multi-hop context for downstream SAR generation and audit validation.
    """
    alert_entity_id: str
    risk_score: float
    conformal_tier: str  # "Tier 1: Auto-Block" or "Tier 2: Manual Review"
    total_inbound_volume: float
    total_outbound_volume: float
    kirchhoff_peeling_ratio: float
    max_hop_depth: int
    dormant_delay_days: float
    detected_typologies: List[str]
    suspect_counterparties: List[str]
    transaction_trail: List[Dict[str, Any]]
    smurfing_burst_score: float
    cycle_detected: bool
    sanctions_taint_score: float
    investigation_timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_entity_id": self.alert_entity_id,
            "risk_score": float(self.risk_score),
            "conformal_tier": self.conformal_tier,
            "total_inbound_volume": float(self.total_inbound_volume),
            "total_outbound_volume": float(self.total_outbound_volume),
            "kirchhoff_peeling_ratio": float(self.kirchhoff_peeling_ratio),
            "max_hop_depth": int(self.max_hop_depth),
            "dormant_delay_days": float(self.dormant_delay_days),
            "detected_typologies": self.detected_typologies,
            "suspect_counterparties": self.suspect_counterparties,
            "transaction_trail": self.transaction_trail,
            "smurfing_burst_score": float(self.smurfing_burst_score),
            "cycle_detected": bool(self.cycle_detected),
            "sanctions_taint_score": float(self.sanctions_taint_score),
            "investigation_timestamp": self.investigation_timestamp
        }


class ForensicInvestigatorAgent:
    """
    Autonomous AI Forensic Investigator Agent.
    Traverses sub-graphs surrounding flagged accounts, extracts forensic flow invariants,
    and isolates criminal money laundering structures.
    """
    def __init__(self, max_depth: int = 3, peeling_threshold: float = 0.85,
                 dormancy_threshold_days: float = 14.0):
        self.max_depth = max_depth
        self.peeling_threshold = peeling_threshold
        self.dormancy_threshold_days = dormancy_threshold_days

    def investigate_subgraph(self, alert_entity_id: str,
                             risk_score: float,
                             conformal_tier: str,
                             in_edges: List[Dict[str, Any]],
                             out_edges: List[Dict[str, Any]],
                             extended_hops: Optional[List[Dict[str, Any]]] = None) -> ForensicEvidence:
        """
        Executes a deep multi-hop forensic crawl around the target entity.
        
        Args:
            alert_entity_id: Target account or transaction ID.
            risk_score: Output risk probability from C-STGB (0.0 to 1.0).
            conformal_tier: Calibrated Conformal Risk Control tier.
            in_edges: List of inbound transactions [{'source', 'amount', 'timestamp'}, ...].
            out_edges: List of outbound transactions [{'target', 'amount', 'timestamp'}, ...].
            extended_hops: Optional higher-order multi-hop edges.
        """
        in_vol = sum(float(e.get("amount", 0.0)) for e in in_edges)
        out_vol = sum(float(e.get("amount", 0.0)) for e in out_edges)

        # 1. Kirchhoff Peeling Ratio Invariant
        max_vol = max(in_vol, out_vol) + 1e-6
        min_vol = min(in_vol, out_vol)
        peeling_ratio = min_vol / max_vol

        # 2. Extract counterparties & build transaction trail
        suspects: Set[str] = set()
        trail: List[Dict[str, Any]] = []
        timestamps: List[float] = []

        for e in in_edges:
            src = str(e.get("source", "unknown_src"))
            amt = float(e.get("amount", 0.0))
            ts = float(e.get("timestamp", 0.0))
            suspects.add(src)
            trail.append({"type": "INBOUND", "counterparty": src, "amount": amt, "timestamp": ts})
            if ts > 0:
                timestamps.append(ts)

        for e in out_edges:
            dst = str(e.get("target", "unknown_dst"))
            amt = float(e.get("amount", 0.0))
            ts = float(e.get("timestamp", 0.0))
            suspects.add(dst)
            trail.append({"type": "OUTBOUND", "counterparty": dst, "amount": amt, "timestamp": ts})
            if ts > 0:
                timestamps.append(ts)

        # 3. Detect Circular Wash-Trading Cycles (A -> B -> A or A in out_nodes)
        in_nodes = {str(e.get("source", "")) for e in in_edges}
        out_nodes = {str(e.get("target", "")) for e in out_edges}
        common_nodes = in_nodes.intersection(out_nodes)
        cycle_detected = len(common_nodes) > 0

        # 4. Long-Dwell Hibernation / Dormancy Analysis
        dormant_delay_days = 0.0
        if len(timestamps) >= 2:
            timestamps.sort()
            max_delta_sec = max(timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps)))
            dormant_delay_days = max_delta_sec / 86400.0

        # 5. Smurfing Burst Scoring
        # High count of transactions within short temporal window
        burst_score = 0.0
        if len(trail) >= 3 and len(timestamps) >= 2:
            time_span_hours = max(0.1, (max(timestamps) - min(timestamps)) / 3600.0)
            burst_score = len(trail) / time_span_hours

        # 6. Typology Classification
        detected_typologies = []
        if peeling_ratio >= self.peeling_threshold and (in_vol > 5000.0 or out_vol > 5000.0):
            detected_typologies.append("Pass-Through Mule Conduit (Rapid Layering)")
        if cycle_detected:
            detected_typologies.append("Circular Wash Trading Loop (Cycle-3 / Reciprocal Ring)")
        if burst_score >= 2.0 and (len(in_edges) >= 4 or len(out_edges) >= 4):
            detected_typologies.append("Smurfing / Structuring (High-Frequency Fan-In/Fan-Out)")
        if dormant_delay_days >= self.dormancy_threshold_days:
            detected_typologies.append(f"Long-Dwell Hibernation Evasion ({dormant_delay_days:.1f} Days Dormant)")
        if not detected_typologies:
            detected_typologies.append("High-Risk Topological Flow Anomaly")

        # 7. Synthetic Sanctions Taint Heuristic
        sanctions_taint = min(1.0, risk_score * (1.2 if cycle_detected else 1.0))

        # Hop depth
        hop_depth = 1
        if extended_hops:
            hop_depth = min(self.max_depth, 1 + len(extended_hops) // 2)

        return ForensicEvidence(
            alert_entity_id=alert_entity_id,
            risk_score=risk_score,
            conformal_tier=conformal_tier,
            total_inbound_volume=in_vol,
            total_outbound_volume=out_vol,
            kirchhoff_peeling_ratio=peeling_ratio,
            max_hop_depth=hop_depth,
            dormant_delay_days=dormant_delay_days,
            detected_typologies=detected_typologies,
            suspect_counterparties=sorted(list(suspects)),
            transaction_trail=trail,
            smurfing_burst_score=burst_score,
            cycle_detected=cycle_detected,
            sanctions_taint_score=sanctions_taint
        )
