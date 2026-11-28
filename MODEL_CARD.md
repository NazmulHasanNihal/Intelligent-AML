# Intelligent-AML: Model Card & Technical Specification (Root Mirror)

**Document Reference:** `MODEL_CARD.md`  
**Full Master Model Card:** [docs/governance/MODEL_CARD_CSTGB.md](file:///c:/Users/SAAD/Documents/GitHub/Intelligent-AML/docs/governance/MODEL_CARD_CSTGB.md)  
**Model Architecture:** Conformal Spatio-Temporal GraphBoost (`C-STGB v3.2`) with `BurstAwareHGTConv`  
**Target Domain:** Anti-Money Laundering (AML), Counter-Terrorist Financing (CTF) & Trade-Based Money Laundering (TBML)  
**Version:** 3.2.0-Production (Platform v3.0)  
**Authors:** Md. Nazmul, Musrat Jahan Gungun, Sagor Chandra  

---

### 1. Model Overview & Purpose

`C-STGB v3.2` is a continuous-time, causal spatio-temporal graph neural network paired with gradient-boosted tabular invariants and Class-Conditional Conformal Risk Control (CRC). It detects complex financial crime typologies (structuring rings, circular wash loops, rapid layering, and trade-based over/under-invoicing) while bounding false-negative risk.

1. **`BurstAwareHGTConv`:** Continuous Tri-Band temporal attention encoding sub-second bursts and 90-day dormant holding chains.
2. **Edge-Trust Camouflage Gating ($\hat{g}_{ij} \ge 0.10$):** Suppresses 65.9% of adversarial utility/POS hub chaff links.
3. **Class-Conditional Conformal Risk Control (CRC):** Guarantees finite-sample coverage $\ge 1 - \alpha$ ($\alpha = 0.01 \Rightarrow \ge 99.0\%$ nominal coverage, $99.04\%$ empirical coverage).

---

### 2. Empirical Benchmarks (Verifiable via `/evals`)

#### 2.1 7-Day Bangladesh Synthetic Bank Shadow Replay (`SHADOW-REPLAY-7D-20261123`)
| Evaluation Metric | Champion (`C-STGB v3.2`) | Baseline (`LightGBM-v2.1`) | Baseline (`Vanilla GCN`) | Target Policy |
| :--- | :---: | :---: | :---: | :---: |
| **Macro F1 Score** | **94.5%** | 88.7% | 74.2% | $\ge 90.0\%$ |
| **Minority Recall** | **94.8%** | 82.4% | 68.2% | $\ge 90.0\%$ |
| **False Positive / Missed Rate** | **0.76%** | 4.82% | 11.40% | $\le 1.00\%$ ($\alpha=0.01$) |
| **Operational Noise Reduction** | **84.2%** | — | — | $> 80.0\%$ |
| **Conformal Coverage ($1-\alpha$)** | **99.04%** | N/A | N/A | $\ge 99.00\%$ |

#### 2.2 14-Dataset Cross-Domain Research Corpus (`MASTER_14_DATASET_EVAL_20260904`)
| Evaluation Metric | C-STGB (Proposed) | XGBoost | TGN | CARE-GNN |
| :--- | :---: | :---: | :---: | :---: |
| **Global Macro F1 (14 Networks)** | **68.05%** | 64.76% | 43.39% | 40.53% |
| **Elliptic-v1 Minority F1 / PR-AUC** | **91.42% / 0.9312** | 88.35% / 0.8900 | 68.40% / 0.7200 | 64.50% / 0.6800 |
| **Fast-Path Inference Latency** | **0.45 ms P50 (0.82 ms P99)** | 0.32 ms | 4.85 ms | 5.10 ms |

#### One-Command Reproduction:
```bash
python evals/reproduce_headlines.py --fast
```

---

### 3. Tiered Scoring Cascade & Governance

- **Tier 1 Hold ($\Gamma = \{1\}$):** High-confidence illicit activity routed to administrative hold & multi-agent SAR drafting.
- **Tier 2 Review ($\Gamma = \{0, 1\}$):** Epistemic uncertainty queue routed to senior analysts with 4-Eyes sign-off.
- **Tier 3 Auto-Clear ($\Gamma = \{0\}$):** Straight-through clearing in $< 0.45\text{ ms}$ with bounded missed-illicit risk ($\le \alpha$).
- **Regulatory Grounding:** Aligned with BFIU Master Circular No. 26, Circular No. 24 (TBML), 2026 Circulars 32 & 02/03/05, MLPA 2012 §§ 6 & 25, Bangladesh Evidence Act (Amended 2022) §§ 65A–65B & 73A, and Federal Reserve SR 11-7.

> **Research prototype. Not legal advice. Not a certified regulated product.**
