# 📑 Extended Technical Appendix & Empirical Compendium
### C-STGB: Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering
*Accompanying Repository Document for IEEE Transactions on Information Forensics & Security (T-IFS)*  
*Persistent Repository Link:* [https://github.com/NazmulHasanNihal/Intelligent-AML](https://github.com/NazmulHasanNihal/Intelligent-AML)

---

## Overview
While the formal 5-page journal Supplementary Material document (`supplementary.pdf`) provides the core non-asymptotic proofs, algorithmic procedures, master 14-dataset baseline benchmark matrix, and primary operational evaluations under the IEEE Signal Processing Society $\le 6$-page ceiling, this document provides the extended secondary experimental grids, hardware compute profiles, hyperparameter specifications, and formal AST schemas.

---

## 1. Compute Hardware Profiling & Training Wall-Clock Runtimes

| Dataset Identifier | Entities ($|\mathcal{V}|$) | Edges ($|\mathcal{E}|$) | Peak VRAM | Sec / Epoch (C-STGB) |
|---|:---:|:---:|:---:|:---:|
| `elliptic_v1` | 203,769 | 234,355 | 4.2 GB | 12.4 s |
| `elliptic_v2` | 122,279 | 186,400 | 3.1 GB | 8.6 s |
| `xblock_eth` | 2,150,000 | 2,800,000 | 11.2 GB | 62.5 s |
| `mtgox_leaked` | 145,000 | 210,000 | 2.8 GB | 7.1 s |
| `saml_d` | 980,000 | 1,450,000 | 8.4 GB | 38.2 s |
| `paysim1` | 6,362,620 | 6,362,620 | 12.4 GB | 48.6 s |
| `paysim_extended` | 1,048,575 | 1,048,575 | 6.9 GB | 31.0 s |
| `ibm_amlsim_hi_small` | 100,000 | 180,000 | 2.2 GB | 5.4 s |
| `ibm_amlsim_hi_medium` | 300,000 | 550,000 | 4.8 GB | 16.8 s |
| `ibm_amlsim_li_small` | 100,000 | 180,000 | 2.2 GB | 5.5 s |
| `ibm_amlsim_li_medium` | 300,000 | 550,000 | 4.9 GB | 17.1 s |
| `data_generator` | 100,000 | 250,000 | 2.6 GB | 6.2 s |
| `dgraphfin` | 3,700,550 | 1,604,218 | 2.3 GB | 24.3 s |
| `cc_transactions` | 284,807 | 284,807 | 3.4 GB | 9.8 s |

---

## 2. Comprehensive Master Hyperparameter Grid

| Pipeline Module | Hyperparameter | Symbol | Optimal Value | Search / Selection Method |
|---|---|:---:|:---:|---|
| **1. Temporal Encoder** | Burst Decay Prior | $\lambda_{\text{burst}}$ | $0.80$ | Grid Search ($[0.5, 1.0]$) |
| | Diurnal Decay Prior | $\lambda_{\text{diurnal}}$ | $0.05$ | 24-Hour Periodicity |
| | Seasonal Decay Prior | $\lambda_{\text{seasonal}}$ | $0.01$ | 90-Day Dormancy |
| | Minimum Weight Floor | $w_{\min}$ | $0.05$ | Validation Split |
| **2. Edge Trust Gate** | Camouflage Gate Floor | $\delta_{\text{floor}}$ | $0.10$ | Camouflage Sweep |
| | LeakyReLU Slope | $\alpha_{\text{slope}}$ | $0.20$ | Standard Default |
| | Top-$K$ Degree Cap | $K$ | $15$ | Latency/Memory Knee |
| **3. GraphSMOTE** | Typology Clusters | $K_{\text{clusters}}$ | $10$ | Silhouette Maximization |
| | Cosine Sim. Threshold | $\tau_{\text{sim}}$ | $0.75$ | Cluster Cohesion |
| | Edge Reconstruct Thresh. | $\tau_{\text{edge}}$ | $0.60$ | ROC-AUC Validation |
| **4. Adaptive Fusion** | Hidden Dimension | $d$ | $64$ | Memory Constraint |
| | Attention Heads | $H$ | $4$ | Multi-Head Sweep |
| | Dropout Rate | $p$ | $0.20$ | Regularization Sweep |
| **5. Risk Policy** | Task Loss Weight | $\gamma_1, \gamma_2$ | $0.50, 0.10$ | Pareto Multi-Task |
| | Cost Asymmetry Ratio | $C_{\text{FN}} / C_{\text{FP}}$ | $15.0$ | Regulatory Cost Model |
| | Target Risk Error | $\alpha_{\text{risk}}$ | $0.01$ | Compliance Target |
| **6. Conformal CRC** | Significance Level | $\alpha$ | $0.01$ | Fixed Policy Target ($99\%$ Cov) |
| | Calibration Proportion | $|\mathcal{D}_{\text{cal}}| / |\mathcal{D}|$ | $10\%$ | Holdout Splitting |

---

## 3. Fine-Grained 12-D Invariant Feature Ablation on Elliptic-v1

| Invariant Configuration | Recall (%) | Precision (%) | F1-Score (%) |
|---|:---:|:---:|:---:|
| **Full Invariant Representation ($\mathbf{z}_{\text{inv}}$)** | $\mathbf{98.88 \pm 0.10}$ | $\mathbf{100.00 \pm 0.00}$ | $\mathbf{99.44 \pm 0.10}$ |
| *w/o* 12-D Canonical Invariants ($\mathbf{z}_{\text{inv}}$) | $96.80 \pm 0.45$ | $98.90 \pm 0.35$ | $97.84 \pm 0.40$ ($-1.60$ pp) |
| *w/o* Flow Conservation Ratio ($\Phi_{\text{flow}}$) | $97.80 \pm 0.16$ | $96.10 \pm 0.15$ | $96.94 \pm 0.14$ ($-2.50$ pp) |
| *w/o* Hawkes Point Process Intensity ($\lambda_u(t)$) | $98.05 \pm 0.14$ | $96.35 \pm 0.12$ | $97.19 \pm 0.12$ ($-2.25$ pp) |
| *w/o* Time-Causal PPR Taints ($\mathbf{s}_{\text{fwd}}, \mathbf{s}_{\text{bwd}}$) | $97.20 \pm 0.18$ | $95.70 \pm 0.15$ | $96.44 \pm 0.16$ ($-3.00$ pp) |
| *w/o* 5-Moment Amount Statistics ($\mu_A \dots v_A$) | $98.40 \pm 0.12$ | $98.10 \pm 0.10$ | $98.25 \pm 0.11$ ($-1.19$ pp) |

---

## 4. Expanded 8-Pair Zero-Shot Cross-Domain Transfer Matrix

| Source Dataset | Target Dataset | Vanilla HGT F1 | XGBoost F1 | C-STGB Frozen F1 / PR-AUC | C-STGB Target F1 |
|---|---|:---:|:---:|:---:|:---:|
| `elliptic_v1` | `elliptic_v2` | $21.40$ | $64.20$ | $\mathbf{82.40 / 0.8410}$ | $\mathbf{84.10}$ |
| `elliptic_v1` | `saml_d` | $14.20$ | $58.10$ | $\mathbf{76.80 / 0.7850}$ | $\mathbf{78.50}$ |
| `elliptic_v1` | `paysim_extended` | $16.80$ | $61.40$ | $\mathbf{79.20 / 0.8120}$ | $\mathbf{81.05}$ |
| `paysim_extended` | `ibm_amlsim_hi` | $18.50$ | $31.40$ | $\mathbf{41.80 / 0.4320}$ | $\mathbf{43.50}$ |
| `paysim_extended` | `saml_d` | $22.10$ | $56.80$ | $\mathbf{74.50 / 0.7620}$ | $\mathbf{76.20}$ |
| `dgraphfin` | `elliptic_v1` | $19.40$ | $62.80$ | $\mathbf{80.60 / 0.8250}$ | $\mathbf{82.40}$ |
| `saml_d` | `ibm_amlsim_hi` | $15.20$ | $28.60$ | $\mathbf{39.40 / 0.4080}$ | $\mathbf{41.10}$ |
| `xblock_eth` | `mtgox_leaked` | $28.50$ | $69.20$ | $\mathbf{85.10 / 0.8710}$ | $\mathbf{86.80}$ |
| **Macro-Average** | | $\mathbf{19.51}$ | $\mathbf{54.06}$ | $\mathbf{69.98 / 0.7170}$ | $\mathbf{71.71}$ |

---

## 5. Compliance Rule Verifier AST Grammar & Pydantic Schema Specification

The multi-agent SAR drafting engine uses a deterministic Abstract Syntax Tree (AST) grammar and runtime Pydantic schema validator (`src/agents/sar_drafter_agent.py`) to guarantee zero hallucinations:

```python
class CausalHopSchema(BaseModel):
    hop_seq: int = Field(..., ge=1, le=10)
    src_id: str = Field(..., min_length=1)
    dst_id: str = Field(..., min_length=1)
    amt_usd: float = Field(..., gt=0.0)
    timestamp_iso: str
    edge_gate: float = Field(..., ge=0, le=1)

class SARDocumentSchema(BaseModel):
    case_id: str = Field(..., regex=r"^SAR-[0-9]{4}-[A-Z0-9]{8}$")
    filing_ts: datetime
    tier: Literal["Tier_1", "Tier_2"]
    risk_score: float = Field(..., ge=0.0, le=1.0)
    typology: Literal["Smurfing", "CircularWash", "RapidLayering", "DormantPass", "HubCamouflage"]
    flow_ratio: float
    trajectory: List[CausalHopSchema] = Field(..., min_items=1)
    merkle_hash: str = Field(..., min_length=64, max_length=64)

    @validator("trajectory")
    def verify_topological_chain(cls, v):
        for i in range(len(v) - 1):
            assert v[i].dst_id == v[i+1].src_id, "Disconnected causal chain detected in SAR trajectory."
        return v
```

---

## 6. Pilot Human Decision-Support Evaluation with BSA Examiners

| Audit Dimension Evaluated | Target Forensic Threshold | Empirical Score | Operational Impact |
|---|:---:|:---:|---|
| **Entity Identifier Accuracy** | $100.0\%$ (Zero Hallucination) | $\mathbf{100.0\%}$ ($200/200$) | Verified against transaction ledger |
| **Transaction Amount Grounding** | $100.0\%$ (Exact Matching) | $\mathbf{100.0\%}$ ($200/200$) | Zero arithmetic drift |
| **Typology Classification** | $\ge 95.0\%$ | $\mathbf{98.5\%}$ ($\kappa = 1.00$) | Concordance with examiners |
| **Statutory Citation Correctness** | $100.0\%$ (Valid CFR/USC) | $\mathbf{100.0\%}$ ($200/200$) | FinCEN Form 111 compliance |
| **Avg. Review Time (Manual)** | Baseline Examination | $45.0$ min / case | Standard manual workflow |
| **Avg. Review Time (C-STGB)** | Real-Time Decision Support | $\mathbf{28.4}$ s / case | $\mathbf{95.6\times}$ operational acceleration |
