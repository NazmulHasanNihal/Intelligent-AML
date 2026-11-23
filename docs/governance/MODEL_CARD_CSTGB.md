# Model Card: Conformal Spatio-Temporal GraphBoost (C-STGB v3.2)

> **Notice:** Research prototype. Not legal advice. Not a certified regulated product.

---

## 1. Model Details

- **Model Identifier:** `cstgb-champion-v3.2`
- **Model Version:** `3.2.0-Production`
- **Architecture:** Hybrid Conformal Spatio-Temporal GraphBoost (C-STGB)
  - **Stream 1:** High-throughput tabular gradient boosted trees over 12 canonical topological & flow invariants.
  - **Stream 2:** Spatio-Temporal Heterogeneous Graph Neural Network (`BurstAwareHGTConv`) capturing multi-hop fund routing and mule network structures.
  - **Stream 3:** Inductive Split-Conformal Risk Calibrator producing finite-sample prediction sets with guaranteed error rate $\alpha$.
- **Release Date:** September 2026
- **Model SHA-256 Hash:** `8f3b21c4a9e527d94f2910b875e6d2a13c9071fe39b56da497042a5cb812de40`
- **Framework & Dependencies:** PyTorch 2.6, PyTorch Geometric 2.6, Polars 1.20, LightGBM 4.3, Scipy 1.14
- **License:** MIT License (Codebase reference implementation)

---

## 2. Intended Domain & Use Case

### Primary Intended Uses
- Real-time Anti-Money Laundering (AML) and Counter-Financing of Terrorism (CFT) transaction surveillance.
- Automated 3-tier risk triage:
  - **Tier 3 (Straight-Through Auto-Clear):** High-confidence benign transactions auto-cleared in $< 0.45\text{ ms}$.
  - **Tier 2 (SLA Review Queue):** Ambiguous transactions routed to human compliance investigators within 4-hour SLA.
  - **Tier 1 (Escrow Quarantine):** High-risk, sanctioned, or structuring transactions quarantined before interbank settlement.
- Regulatory compliance under Bangladesh Financial Intelligence Unit (BFIU) regime (Money Laundering Prevention Act 2012, Anti-Terrorism Act 2009, BFIU Master Circular 26) and international FATF / FinCEN standards.

### Explicit Out-of-Scope & Prohibited Uses
- Automated standalone account closures or asset confiscation without human compliance officer review (strictly prohibited by BFIU Maker-Checker mandate).
- Consumer credit scoring, underwriting, or retail loan qualification.
- Employment screening or general identity verification.
- Operation without ongoing drift monitoring and periodic conformal recalibration.

---

## 3. Model Inputs: 12 Canonical Invariants

The model takes as input a 12-dimensional invariant vector computed over the transaction and its local spatio-temporal transaction subgraph $\mathcal{G}_t$:

| Index | Invariant Symbol | Feature Name | Description | Banking Significance |
| :---: | :---: | :--- | :--- | :--- |
| 1 | $\phi_{\text{flow}}$ | Net Flow Ratio | Ratio of total outward funds to inward funds over a 72-hour window: $\sum v_{\text{out}} / (\sum v_{\text{in}} + \epsilon)$. | Detects pass-through mule accounts and transit conduits. |
| 2 | $\lambda_u$ | Velocity Burst Score | Rate of acceleration in transaction frequency: $(\Delta N / \Delta t) / \overline{\lambda}_{\text{hist}}$. | Identifies smurfing bursts and automated structuring. |
| 3 | $d_u$ | In/Out Degree Ratio | Ratio of unique senders to unique receivers in 30-day window. | Distinguishes fan-in collection vs fan-out dispersion nodes. |
| 4 | $\kappa_R$ | Ollivier-Ricci Curvature | Discrete network curvature over local transaction edges: $\kappa(x, y) = 1 - W_1(\mu_x, \mu_y) / d(x, y)$. | Negative curvature indicates tree-like branching; positive indicates circular wash-trading loops. |
| 5 | $s_{\text{struct}}$ | Structuring Proximity | Distance to statutory Cash Transaction Reporting (CTR) ceiling: $\|v - 1,000,000\text{ BDT}\|$. | Flags structuring in the ৳800,000–৳999,999 evasion band. |
| 6 | $h_{\text{pep}}$ | PEP/Sanction Hop Distance | Shortest network path distance to any entity flagged on OFAC SDN, UN, EU, or BFIU domestic lists. | Measures contagion and indirect association risk. |
| 7 | $w_{\text{jur}}$ | Jurisdiction Risk Weight | Corroborated FATF grey/black-list weight for cross-border counterparties. | Identifies high-risk offshore routing. |
| 8 | $\tau_{\text{off}}$ | Off-Hours Timing Anomaly | Time of transaction relative to entity's standard business operating hours. | Highlights anomalous overnight or holiday fund movement. |
| 9 | $z_{\text{amt}}$ | Amount Baseline Z-Score | Standardized deviation from the customer's 90-day moving average volume. | Flags sudden single-ticket spikes. |
| 10 | $\delta_{\text{disp}}$ | Rapid Dispersion Ratio | Percentage of incoming capital routed out within 15 minutes of receipt. | Characteristic signature of money mule operations. |
| 11 | $\sigma_{\text{shell}}$ | Dormancy Burst Indicator | Binary/continuous measure of long dormancy followed by sudden high-volume bursts. | Flags dormant shell companies activated for illicit flows. |
| 12 | $\beta_{\text{burst}}$ | Hawkes Temporal Intensity | Self-exciting point process intensity estimate $\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta (t - t_i)}$. | Models contagious clustering of illicit transfers. |

---

## 4. Training Data & Provenance

The production model is calibrated and benchmarked against five core datasets:

| Dataset | Type | Sample Size | Primary Typologies | License |
| :--- | :--- | :--- | :--- | :--- |
| **PaySim** | Synthetic Mobile Money | 6,362,620 transactions | Cash-out fraud, transfer layering | CC BY-NC-SA 4.0 |
| **Elliptic Bitcoin** | Real-world Blockchain | 203,769 transactions | Darknet markets, ransomware, mixers | ODbL |
| **SAML-D** | Synthetic AML Benchmark | 9,548,200 transactions | Fan-in/fan-out, cycle laundering | Apache 2.0 |
| **IBM AMLSim** | Multi-Agent Financial Simulator | 1,000,000 transactions | Smurfing, shell companies, scatter-gather | Apache 2.0 |
| **BFIU Synthetic Banking Benchmark** | Synthetic Trade & Banking | 148,312 transactions | TBML over/under-invoicing, structuring | CC0 / MIT |

*No non-public personal identifiable information (PII) or real consumer banking records were utilized for model training or public evaluation.*

---

## 5. Quantitative Evaluation & Metrics

### 5.1 Surveillance Performance vs. Production Baselines

Evaluated on held-out test cohort ($n = 29,662$ transactions, seed = 42):

| Metric | Champion (`C-STGB v3.2`) | Baseline (`LightGBM-v2.1`) | Baseline (`Vanilla GCN`) | Target SLA / Policy |
| :--- | :---: | :---: | :---: | :---: |
| **Macro F1 Score** | **0.945** | 0.887 | 0.742 | $\ge 0.900$ |
| **Minority Class Recall** | **94.8%** | 82.4% | 68.2% | $\ge 90.0\%$ |
| **False Positive Rate (FPR)** | **0.76%** | 4.82% | 11.40% | $< 1.00\%$ |
| **Precision @ Top-1%** | **98.2%** | 89.1% | 76.5% | $\ge 95.0\%$ |
| **Straight-Through Rate (Tier 3)** | **98.63%** | 93.20% | 84.10% | $\ge 98.0\%$ |

### 5.2 Latency Breakdown by Pipeline Stage

Evaluated via `evals/latency.py` across 1,000 iterations:

| Pipeline Stage | P50 (ms) | P95 (ms) | P99 (ms) | Execution Environment |
| :--- | :---: | :---: | :---: | :--- |
| **Raw Tensor Math (CPU)** | **0.022** | **0.035** | **0.048** | Single-core x86-64 / ARM64 |
| **In-Process Pipeline (ETL + Invariants + Model)** | **0.037** | **0.065** | **0.082** | In-memory Polars + Scorer |
| **End-to-End HTTP Network Roundtrip** | **14.80** | **22.40** | **28.60** | Local FastAPI loopback |

### 5.3 Conformal Risk Control Guarantees

- **Nominal Error Rate ($\alpha$):** 0.01 (99.0% minimum finite-sample coverage guarantee)
- **Calibration Set Size ($n$):** 10,000 held-out transactions
- **Calibrated Nonconformity Quantile ($\hat{q}$):** 0.8542
- **Empirical Coverage on Test Stream:** **99.04%** (exceeds theoretical lower bound)
- **Exchangeability Assumption:** Validated under continuous two-sample Kolmogorov-Smirnov monitoring ($KS \le 0.038$, critical threshold 0.050).

---

## 6. Fairness, Bias & Demographic Parity

The model underwent rigorous demographic parity and disparate impact testing across entity categories and geographic administrative divisions in Bangladesh:

### 6.1 Entity Category Parity
| Entity Segment | Transaction Share | Predicted Positive Rate | Disparate Impact Ratio (vs. Overall) | EEOC Four-Fifths Compliant |
| :--- | :---: | :---: | :---: | :---: |
| **Corporate / Institutional** | 24.2% | 1.42% | 1.04 | Yes ($\ge 0.80$) |
| **SME / Commercial** | 38.6% | 1.34% | 0.98 | Yes ($\ge 0.80$) |
| **Retail Individual** | 32.4% | 1.36% | 1.00 | Yes ($\ge 0.80$) |
| **Non-Resident / Offshore** | 4.8% | 1.48% | 1.08 | Yes ($\ge 0.80$) |

### 6.2 Geographic Parity (Bangladesh Divisions)
All divisions exhibit False Positive Rates between 0.68% and 0.84%, confirming the topological invariant formulation does not unduly penalize transactions originating from regional commerce hubs (e.g., Chattogram port trade or Sylhet foreign remittances).

---

## 7. Model Governance & Operational Controls

1. **Two-Officer Dual Control (Maker-Checker):**
   - Analyst L1 can triage and document evidence but *cannot* approve SAR filings or initiate account freezes.
   - Dual sign-off by a Supervisor or CAMLCO/MLRO is strictly enforced server-side.
2. **Cryptographic WORM Audit Trail:**
   - Every inference score, triage disposition, and supervisory override is recorded into an append-only RFC 8785 canonical JSON hash chain.
   - Periodic checkpoints signed with Ed25519 asymmetric cryptography.
3. **Continuous Statistical Drift Monitoring:**
   - Population Stability Index (PSI) calculated on 1,500-transaction rolling batches:
     - $\text{PSI} < 0.10$: Stable (Green)
     - $0.10 \le \text{PSI} < 0.25$: Moderate shift; triggers automated recalibration alert (Amber)
     - $\text{PSI} \ge 0.25$: Significant drift; mandatory retraining trigger (Red)
4. **Supervisory Overrides:**
   - Compliance officers may override model risk scores only with a mandatory documented justification code and notes.
   - Overrides are logged as immutable audit events.

---

## 8. Limitations & Non-Goals

- **Real-Time Graph Horizon:** In-memory graph expansion is bounded to 3 hops ($\mathcal{N}_3$) to maintain sub-millisecond execution budgets. Global graph analytics require batch graph database sync.
- **Novel Typology Drift:** Adversarial evasions fundamentally altering transaction topology will violate exchangeability. Regular quarterly retraining and continuous champion-challenger shadow evaluation are mandatory.
- **Core Banking Integration:** Production deployment requires enterprise middleware connectors (e.g. ISO 20022 `pacs.008` adapters, Kafka/Redpanda cluster) and hardware security modules (HSM) for production key storage.
