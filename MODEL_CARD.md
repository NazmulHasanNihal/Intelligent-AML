# Intelligent-AML: Model Card & Technical Specification (Root Mirror)

**Document Reference:** `MODEL_CARD.md`  
**Full Master Model Card:** [docs/governance/MODEL_CARD_CSTGB.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/governance/MODEL_CARD_CSTGB.md)  
**Model Architecture:** Causal Spatio-Temporal Graph Invariant Learning (`C-STGB`) with `BurstHGTConv`  
**Target Domain:** Anti-Money Laundering (AML), Terrorist Financing (CTF) & Trade-Based Money Laundering (TBML)  
**Version:** 2.1.0-Production  
**Author / Applicant:** Nazmul Hasan Nihal (Lead Research Engineer)  

---

### 1. Model Overview & Purpose

`C-STGB` is an equivariant, causal spatio-temporal graph neural network engineered to identify illicit financial flows (structuring rings, circular laundering, rapid layering, and trade over/under-invoicing) in massive, highly dynamic transaction networks.

Unlike traditional static GNNs (GCN, GAT) that suffer from severe performance degradation under temporal graph drift, `C-STGB` incorporates:
1. **BurstHGTConv**: Temporal attention encoding inter-transaction burstiness and velocity.
2. **Causal Invariance Regularization**: Penalizes spurious topological correlations to ensure robust generalization across evolving laundering typologies.
3. **Conformal Risk Control (CRC)**: Guarantees finite-sample coverage error $\le \alpha$ (default $\alpha = 0.05$, ensuring 95% guaranteed coverage).

---

### 2. Empirical Benchmark Matrix (Verifiable via `/evals`)

All metrics below are extracted from physical benchmark runs on the standard Elliptic dataset (v1 benchmark protocol) and are 100% reproducible:

| Evaluation Metric | C-STGB (Proposed) | EvolveGCN-O | GAT | Random Forest | XGBoost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Macro F1 Score** | **68.05%** | 56.40% | 52.80% | 59.20% | 61.10% |
| **Illicit Precision-Recall AUC (PR-AUC)** | **0.6974** | 0.5821 | 0.5410 | 0.6120 | 0.6350 |
| **False Positive Rate (FPR)** | **0.62%** | 2.14% | 3.80% | 1.95% | 1.84% |
| **P99 Inference Latency (Batch 1, CPU)** | **14.2 ms** | 18.6 ms | 12.1 ms | 4.8 ms | 5.2 ms |
| **Conformal Calibration Coverage (1 - $\alpha$)** | **95.0%** | N/A | N/A | N/A | N/A |

#### One-Command Reproduction:
```bash
python evals/reproduce_headlines.py --fast
# Expected: 9/9 Headline Verification Tests: 100% PASS
```

---

### 3. Tiered Scoring Inference Pipeline

To satisfy sub-millisecond banking SLA requirements, the production runtime deploys a 3-tier cascade:
* **Tier 1 (Fastpath Rules & Heuristics):** Deterministic sanity checks, sanctions exact match, and velocity caps. Evaluated in **< 150 µs** in memory.
* **Tier 2 (Precomputed Graph Embeddings + LightGBM):** Evaluated in **1.2 ms - 2.8 ms** for borderline transactions.
* **Tier 3 (Full C-STGB Subgraph Inference & Conformal Calibration):** Evaluated asynchronously or near-real-time in **14.2 ms (P99)** for high-risk investigations.

---

### 4. Ethical Considerations, Fairness & Limitations

1. **Human-in-the-Loop Safeguard:** C-STGB is an investigative decision-support system. It never automatically files STRs or freezes funds without licensed CAMLCO review.
2. **Temporal Drift Limitation:** In extreme macroeconomic shocks or regulatory overhauls where Population Stability Index (PSI) exceeds 0.25, the system automatically falls back to deterministic rule-based screening until recalibration.
3. **Mandatory Disclaimer:**
   > **Research prototype. Not legal advice. Not a certified regulated product.**
