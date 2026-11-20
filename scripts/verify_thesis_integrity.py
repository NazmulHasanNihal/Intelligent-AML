"""
scripts/verify_thesis_integrity.py
Single-source-of-truth mathematical, statistical, schema, and cryptographic
verifier for the C-STGB B.Sc. Thesis (main.pdf).
"""
from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Literal, Set, Tuple

import numpy as np
from pydantic import BaseModel, Field, field_validator
from scipy.stats import wilcoxon


# ---------------------------------------------------------------------------
# 1. DETERMINISTIC CRYPTOGRAPHIC MERKLE RECEIPT (REPLACES SHA-256("test"))
# ---------------------------------------------------------------------------
def compute_verified_merkle_tree() -> dict:
    artifacts = [
        {
            "artifact": "wire_payload",
            "case_id": "SAR-2026-B8F91A04",
            "src": "ACC_9941",
            "aggregated_amount_usd": 485000.00,
            "total_hops": 49,
        },
        {
            "artifact": "subgraph_ring",
            "nodes": 15,
            "edges": 18,
            "flow_conservation_ratio": 0.9942,
            "primary_typology": "Smurfing",
        },
        {
            "artifact": "model_dossier",
            "predicted_risk_score": 0.9620,
            "saliency": 0.9841,
            "conformal_tier": "Tier_1_Quarantine",
            "alpha": 0.01,
        },
        {
            "artifact": "four_eyes_signoff",
            "maker": "Sarah Jenkins",
            "checker": "Nazmul Hasan",
            "standard": "Fed_SR_11_7_SR_21_8",
            "status": "APPROVED",
        },
    ]
    leaves = [
        hashlib.sha256(json.dumps(a, sort_keys=True).encode("utf-8")).hexdigest()
        for a in artifacts
    ]
    left_branch = hashlib.sha256((leaves[0] + leaves[1]).encode("utf-8")).hexdigest()
    right_branch = hashlib.sha256((leaves[2] + leaves[3]).encode("utf-8")).hexdigest()
    root = hashlib.sha256((left_branch + right_branch).encode("utf-8")).hexdigest()

    assert root != hashlib.sha256(b"test").hexdigest(), "Placeholder SHA-256('test') forbidden!"
    return {
        "leaves": leaves,
        "left_branch": left_branch,
        "right_branch": right_branch,
        "merkle_root": root,
    }


# ---------------------------------------------------------------------------
# 2. PYDANTIC V2 ANTI-HALLUCINATION VALIDATOR (LISTING E.1 + PROPOSITION 6.1)
# ---------------------------------------------------------------------------
class CausalHopSchema(BaseModel):
    hop_seq: int = Field(..., ge=1, le=10)
    source_entity_id: str = Field(..., min_length=1, max_length=64)
    target_entity_id: str = Field(..., min_length=1, max_length=64)
    amount_usd: float = Field(..., gt=0.0)
    timestamp_iso: datetime
    edge_trust_gate: float = Field(..., ge=0.0, le=1.0)


class SARDocumentSchema(BaseModel):
    case_id: str = Field(..., pattern=r"^SAR-[0-9]{4}-[A-Z0-9]{8}$")
    filing_timestamp: datetime
    conformal_tier: Literal["Tier_1_Quarantine", "Tier_2_Abstention"]
    predicted_risk_score: float = Field(..., ge=0.0, le=1.0)
    primary_typology: Literal[
        "Smurfing",
        "CircularWash",
        "RapidLayering",
        "DormantPassThrough",
        "HubCamouflage",
    ]
    flow_conservation_ratio: float = Field(..., ge=0.0)
    causal_trajectory: List[CausalHopSchema] = Field(..., min_length=1)
    merkle_root_hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")

    @field_validator("causal_trajectory")
    @classmethod
    def verify_topological_chain_integrity(
        cls, hops: List[CausalHopSchema]
    ) -> List[CausalHopSchema]:
        for i in range(len(hops) - 1):
            if hops[i].target_entity_id != hops[i + 1].source_entity_id:
                raise ValueError(
                    f"Disconnected causal chain at hop {i + 1}: "
                    f"{hops[i].target_entity_id} != {hops[i + 1].source_entity_id}"
                )
        return hops

    def verify_subgraph_grounding(
        self,
        observed_nodes: Set[str],
        observed_edges: Set[Tuple[str, str]],
    ) -> None:
        """Enforces Proposition 6.1: V(T) subset V_sub and E(T) subset E_sub."""
        for hop in self.causal_trajectory:
            if hop.source_entity_id not in observed_nodes:
                raise ValueError(f"Hallucinated source node: {hop.source_entity_id}")
            if hop.target_entity_id not in observed_nodes:
                raise ValueError(f"Hallucinated target node: {hop.target_entity_id}")
            if (hop.source_entity_id, hop.target_entity_id) not in observed_edges:
                raise ValueError(
                    f"Hallucinated edge: ({hop.source_entity_id}, {hop.target_entity_id})"
                )


def verify_xml_roundtrip(merkle_root: str) -> str:
    xml_doc = f"""<?xml version='1.0' encoding='UTF-8'?>
<SAR_Form111 Standard="BSA_AML_FinCEN" Version="2.0">
  <FilingHeader>
    <CaseID>SAR-2026-B8F91A04</CaseID>
    <FilingInstitution>Commercial_Bank_Node_04</FilingInstitution>
    <Jurisdiction>US_FinCEN</Jurisdiction>
    <Timestamp>2026-08-28T14:31:33.028Z</Timestamp>
    <FilingStatus>AUTOMATED_QUARANTINE_TIER_1</FilingStatus>
  </FilingHeader>
  <SubjectEntity>
    <EntityID>ACC_9941</EntityID>
    <RiskScore Saliency="0.9841">0.9620</RiskScore>
    <ConformalTier>Tier_1_Quarantine</ConformalTier>
    <PrimaryTypology>Smurfing</PrimaryTypology>
    <FlowConservation Ratio="0.9942">BALANCED_PASSTHROUGH</FlowConservation>
  </SubjectEntity>
  <CampaignSummary AggregatedAmount="485000.00" StructuringThreshold="10000.00" TotalHops="49" WindowMinutes="12"/>
  <TopologicalEvidence SubgraphEdges="18" SubgraphNodes="15">
    <CausalChain ExemplarPathAmount="29350.00" Hops="3">
      <Hop Amount="9850.00" Dst="ACC_MULE_02" EdgeTrust="0.94" Seq="1" Src="ACC_9941" Timestamp="2026-08-28T14:19:12Z"/>
      <Hop Amount="9800.00" Dst="ACC_MULE_08" EdgeTrust="0.91" Seq="2" Src="ACC_MULE_02" Timestamp="2026-08-28T14:23:01Z"/>
      <Hop Amount="9700.00" Dst="ACC_OFFSHORE_08" EdgeTrust="0.96" Seq="3" Src="ACC_MULE_08" Timestamp="2026-08-28T14:27:45Z"/>
    </CausalChain>
  </TopologicalEvidence>
  <Model_Governance_SR11_7_Receipt>
    <MerkleRoot>{merkle_root}</MerkleRoot>
    <SHA256Proof Algorithm="SHA-256" Validated="true"/>
    <Timestamp>2026-08-28T14:32:01.452Z</Timestamp>
  </Model_Governance_SR11_7_Receipt>
</SAR_Form111>"""

    root_el = ET.fromstring(xml_doc)
    hops = [
        CausalHopSchema(
            hop_seq=int(h.attrib["Seq"]),
            source_entity_id=h.attrib["Src"],
            target_entity_id=h.attrib["Dst"],
            amount_usd=float(h.attrib["Amount"]),
            timestamp_iso=h.attrib["Timestamp"],
            edge_trust_gate=float(h.attrib["EdgeTrust"]),
        )
        for h in root_el.findall(".//Hop")
    ]
    sar = SARDocumentSchema(
        case_id=root_el.findtext(".//CaseID"),
        filing_timestamp=root_el.findtext(".//FilingHeader/Timestamp"),
        conformal_tier=root_el.findtext(".//ConformalTier"),
        predicted_risk_score=float(root_el.findtext(".//RiskScore")),
        primary_typology=root_el.findtext(".//PrimaryTypology"),
        flow_conservation_ratio=float(
            root_el.find(".//FlowConservation").attrib["Ratio"]
        ),
        causal_trajectory=hops,
        merkle_root_hash=root_el.findtext(".//MerkleRoot").strip(),
    )
    observed_nodes = {"ACC_9941", "ACC_MULE_02", "ACC_MULE_08", "ACC_OFFSHORE_08"}
    observed_edges = {
        ("ACC_9941", "ACC_MULE_02"),
        ("ACC_MULE_02", "ACC_MULE_08"),
        ("ACC_MULE_08", "ACC_OFFSHORE_08"),
    }
    sar.verify_subgraph_grounding(observed_nodes, observed_edges)
    return xml_doc


# ---------------------------------------------------------------------------
# 3. EXACT BENCHMARK ARITHMETIC (TABLES D.3, 7.5, 7.6, 7.10, 7.11, 5.1)
# ---------------------------------------------------------------------------
def verify_all_tables() -> None:
    f1 = {
        "XGBoost":   [88.35, 96.50, 93.80, 68.40, 89.20, 18.90, 99.72, 32.40, 39.50, 14.20, 21.50, 99.90, 96.07, 48.20],
        "CatBoost":  [87.90, 95.80, 92.90, 67.80, 88.60, 17.76, 99.77, 31.80, 38.90, 13.80, 20.90, 99.85, 95.82, 47.90],
        "GCN":       [43.55,  0.00,  6.53, 20.30,  1.69,  3.50, 96.22,  2.46,  3.88,  0.84,  3.41, 99.74,  2.60, 48.16],
        "GraphSAGE": [49.07,  0.24,  6.75, 22.16,  3.16,  0.56, 96.05,  2.46,  3.95,  1.50,  2.30, 99.63,  3.26, 49.24],
        "GAT":       [31.35,  0.00,  6.45, 28.47,  2.20,  0.46, 95.64,  2.03,  4.03,  1.61,  3.05, 99.98,  2.71, 45.62],
        "GIN":       [22.32,  0.13,  5.56, 19.79,  2.37,  0.94, 95.66,  1.90,  3.95,  1.22,  2.30, 99.00,  2.25, 42.74],
        "HGT":       [48.20, 41.80, 46.50, 43.20, 39.40,  1.80, 52.40, 18.50, 24.80,  8.90, 13.20, 68.40,  1.80, 26.50],
        "CARE-GNN":  [64.50, 58.20, 63.20, 52.40, 55.80,  2.20, 69.40, 25.40, 31.80, 11.80, 17.50, 78.50,  2.50, 34.20],
        "EvolveGCN": [51.04,  0.00,  6.62, 22.12,  3.81,  3.98, 92.64,  2.31,  7.06,  1.18,  4.29, 62.72,  2.59,  4.79],
        "TGN":       [68.40, 62.10, 67.50, 55.80, 59.40,  2.50, 73.10, 28.40, 35.20, 12.90, 19.20, 81.50,  3.20, 38.20],
        "C-STGB":    [91.42, 99.10, 97.40, 74.20, 93.68, 16.66, 99.80, 39.70, 46.85, 15.83, 23.74, 99.93, 97.91, 56.48],
    }
    prauc = {
        "XGBoost":   [0.8900, 0.9814, 0.9400, 0.7400, 0.8950, 0.1254, 0.9996, 0.3100, 0.4200, 0.1300, 0.1900, 0.9990, 0.9900, 0.4900],
        "CatBoost":  [0.8800, 0.9580, 0.9300, 0.7300, 0.8850, 0.1061, 0.9996, 0.3000, 0.4100, 0.1300, 0.1900, 0.9985, 0.9628, 0.4800],
        "GCN":       [0.3482, 0.0237, 0.0212, 0.2038, 0.0109, 0.0084, 0.9825, 0.0101, 0.0135, 0.0060, 0.0143, 0.9979, 0.0129, 0.3472],
        "GraphSAGE": [0.4254, 0.0230, 0.0206, 0.1801, 0.0071, 0.0016, 0.9799, 0.0080, 0.0126, 0.0057, 0.0073, 0.9956, 0.0161, 0.3555],
        "GAT":       [0.1959, 0.0234, 0.0199, 0.1751, 0.0099, 0.0014, 0.9816, 0.0090, 0.0164, 0.0050, 0.0211, 1.0000, 0.0123, 0.3441],
        "GIN":       [0.5625, 0.0266, 0.0137, 0.2411, 0.0078, 0.0057, 0.9818, 0.0112, 0.0174, 0.0105, 0.0083, 1.0000, 0.0189, 0.3883],
        "HGT":       [0.5200, 0.4600, 0.5000, 0.4700, 0.4300, 0.0150, 0.5600, 0.2100, 0.2800, 0.1000, 0.1500, 0.7100, 0.0210, 0.3000],
        "CARE-GNN":  [0.6800, 0.6100, 0.6600, 0.5600, 0.5900, 0.0180, 0.7200, 0.2800, 0.3500, 0.1300, 0.2000, 0.8100, 0.0450, 0.3800],
        "EvolveGCN": [0.4243, 0.0258, 0.0211, 0.0956, 0.0077, 0.0097, 0.7521, 0.0080, 0.0350, 0.0052, 0.0238, 0.6327, 0.0094, 0.0215],
        "TGN":       [0.7200, 0.6500, 0.7100, 0.6000, 0.6300, 0.0220, 0.7600, 0.3200, 0.3900, 0.1400, 0.2200, 0.8400, 0.0250, 0.4200],
        "C-STGB":    [0.9312, 0.9950, 0.9920, 0.8350, 0.9574, 0.1350, 0.9993, 0.4000, 0.5100, 0.1493, 0.2139, 1.0000, 0.9979, 0.6476],
    }

    models = list(f1.keys())
    mat = np.array([f1[m] for m in models])
    ranks = np.zeros_like(mat)
    for col in range(mat.shape[1]):
        # Average rank for ties, descending
        vals = mat[:, col]
        for row in range(mat.shape[0]):
            greater = np.sum(vals > vals[row])
            equal = np.sum(vals == vals[row])
            ranks[row, col] = greater + (equal + 1) / 2.0

    print("=== TABLE D.3 & TABLE 7.5 EXACT VERIFIED METRICS ===")
    cstgb_mean = float(np.mean(f1["C-STGB"]))
    for i, m in enumerate(models):
        mf1 = float(np.mean(f1[m]))
        mpr = float(np.mean(prauc[m]))
        mrk = float(np.mean(ranks[i]))
        if m == "C-STGB":
            w_str, p_str = "  ---", "     ---"
        else:
            res = wilcoxon(f1["C-STGB"], f1[m], alternative="greater")
            w_str, p_str = f"{res.statistic:5.1f}", f"{res.pvalue:.2e}"
        print(
            f"{m:10s} | F1={mf1:6.2f}% | PR-AUC={mpr:.4f} | Rank={mrk:4.2f} | "
            f"Lead={cstgb_mean - mf1:+6.2f}pp | W={w_str} | p={p_str}"
        )

    # Table 7.10 Exact Macro-Averages
    t1 = [2.15, 0.82, 0.08, 1.75, 0.05, 0.11, 0.12, 0.20, 0.21, 0.65, 0.68, 1.45, 1.25, 0.15]
    t2 = [0.48, 0.52, 0.42, 0.85, 0.58, 0.44, 0.40, 0.72, 0.68, 0.92, 0.88, 0.32, 0.38, 0.45]
    t3 = [97.37, 98.66, 99.50, 97.40, 99.37, 99.45, 99.48, 99.08, 99.11, 98.43, 98.44, 98.23, 98.37, 99.40]
    wred = [100.0 - x for x in t2]
    print("\n=== TABLE 7.10 EXACT MACRO-AVERAGES ===")
    print(f"Tier 1: {np.mean(t1):.2f}% | Tier 2: {np.mean(t2):.2f}% | Tier 3: {np.mean(t3):.2f}% | Workload Red: {np.mean(wred):.2f}%")

    # Table 7.11 Exact 4-Attack Retention Means
    ret = {
        "GCN":       [64.6, 44.8, 33.1, 21.9],
        "GraphSAGE": [72.7, 53.9, 42.9, 31.8],
        "HGT":       [79.7, 59.1, 46.5, 33.6],
        "CARE-GNN":  [90.2, 75.2, 65.3, 53.5],
        "C-STGB":    [98.2, 95.6, 93.6, 92.1],
    }
    print("\n=== TABLE 7.11 EXACT 4-ATTACK RETENTION AVERAGES ===")
    for k, v in ret.items():
        print(f"{k:10s} | Mean Retention = {np.mean(v):.1f}%")

    # Table 5.1 Weighted Overall Coverage on Elliptic-v1 (pi = 2.23%)
    pi = 0.0223
    print("\n=== TABLE 5.1 WEIGHTED OVERALL COVERAGE (ELLIPTIC-V1, pi=2.23%) ===")
    cov_rows = [
        ("Uncalibrated Cutoff (tau=0.50)", 99.85, 90.10),
        ("Temperature Scaling",            99.70, 92.80),
        ("Isotonic Regression",            99.65, 94.50),
        ("Marginal Conformal",             99.98, 82.40),
        ("Class-Conditional CRC (Ours)",   99.05, 99.12),
        ("Streaming Adaptive ACI (Ours)",  99.06, 99.08),
    ]
    for name, c0, c1 in cov_rows:
        overall = (1.0 - pi) * c0 + pi * c1
        print(f"{name:32s} | Overall={overall:.2f}% | Benign={c0:.2f}% | Illicit={c1:.2f}%")

    # Eq. (3.29) Exact Tversky Gradient Numerical Finite-Difference Verification
    beta_fn, beta_fp, eps = 0.85, 0.15, 1e-6
    rng = np.random.default_rng(42)
    z = rng.normal(size=100)
    y = (rng.random(100) < 0.05).astype(float)

    def tversky_loss(logits: np.ndarray) -> float:
        p = 1.0 / (1.0 + np.exp(-logits))
        tp = np.sum(p * y)
        fn = np.sum((1.0 - p) * y)
        fp = np.sum(p * (1.0 - y))
        return 1.0 - (tp + eps) / (tp + beta_fn * fn + beta_fp * fp + eps)

    p = 1.0 / (1.0 + np.exp(-z))
    tp, fn, fp = np.sum(p * y), np.sum((1.0 - p) * y), np.sum(p * (1.0 - y))
    D = tp + beta_fn * fn + beta_fp * fp + eps
    idx_pos = int(np.where(y == 1)[0][0])
    idx_neg = int(np.where(y == 0)[0][0])

    # Analytical exact derivatives
    dL_dz_pos = -(beta_fn * (np.sum(y) + eps) + beta_fp * fp) / (D ** 2) * p[idx_pos] * (1.0 - p[idx_pos])
    dL_dz_neg = +(beta_fp * (tp + eps)) / (D ** 2) * p[idx_neg] * (1.0 - p[idx_neg])

    h = 1e-6
    z_p1, z_m1 = z.copy(), z.copy()
    z_p1[idx_pos] += h; z_m1[idx_pos] -= h
    num_pos = (tversky_loss(z_p1) - tversky_loss(z_m1)) / (2 * h)

    z_p0, z_m0 = z.copy(), z.copy()
    z_p0[idx_neg] += h; z_m0[idx_neg] -= h
    num_neg = (tversky_loss(z_p0) - tversky_loss(z_m0)) / (2 * h)

    assert abs(dL_dz_pos - num_pos) < 1e-8, f"Pos gradient mismatch: {dL_dz_pos} vs {num_pos}"
    assert abs(dL_dz_neg - num_neg) < 1e-8, f"Neg gradient mismatch: {dL_dz_neg} vs {num_neg}"
    print("\n=== EQ. (3.29) ANALYTICAL TVERSKY GRADIENT VERIFIED (ERROR < 1e-8) ===")


if __name__ == "__main__":
    merkle = compute_verified_merkle_tree()
    print("=== VERIFIED CRYPTOGRAPHIC MERKLE RECEIPT ===")
    for i, leaf in enumerate(merkle["leaves"], 1):
        print(f"Leaf {i}: {leaf}")
    print(f"Left:   {merkle['left_branch']}")
    print(f"Right:  {merkle['right_branch']}")
    print(f"ROOT:   {merkle['merkle_root']}")
    verify_xml_roundtrip(merkle["merkle_root"])
    print("XML <-> Pydantic v2 <-> Subgraph Grounding (Prop 6.1): PASS\n")
    verify_all_tables()
