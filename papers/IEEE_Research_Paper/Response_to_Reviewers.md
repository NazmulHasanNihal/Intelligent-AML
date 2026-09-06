# Response to Peer Reviewers

**Manuscript Title:** *Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage*  
**Authors:** Md. Nazmul, Musrat Jahan Gungun, Maheli Ahmed  
**Target Journal:** IEEE Transactions on Information Forensics and Security (TIFS)  
**Tracking Number:** TIFS-2026-AR-0828  
**Revision Round:** First Revision (Post-Reviewer Critique)

---

## Executive Response & Overview of Revisions

We express our sincere appreciation to the Senior Reviewer for their unsparing, deeply technical, and exceptionally constructive peer review. The reviewer's 20+ years of domain expertise in financial forensics, graph machine learning, and regulatory model governance provided invaluable guidance that significantly elevated the theoretical rigor, empirical fairness, and operational framing of this manuscript.

In response to the reviewer's critique, we have executed an exhaustive revision across the main text, mathematical proofs, and supplementary material:
1. **Repaired Conformal Non-Exchangeability Theory (Section IV-F, Supplementary Section D.1):** We decoupled environmental Total Variation drift ($d_{\mathrm{TV}}$) from the Dvoretzky-Kiefer-Wolfowitz (DKW) empirical process concentration bound. The finite-sample coverage bound is now formulated rigorously via maximal coupling and DKW concentration, backed by Adaptive Conformal Inference (ACI) and Martingale guarantees for dynamic tracking.
2. **Established Causal Purity in Latent GraphSMOTE (Section IV-C, Supplementary Section D.2):** We updated Equation (117) with the causal temporal indicator $\mathbb{I}(t_w \le t_{\text{syn}})$ and formulated Lemma~S2, proving zero acausal lookahead into future graph snapshots.
3. **Dissected Cold-Start Performance ($d \le 2$) & Framed Gating as an Intentional Safety Valve (Section IV-E, Section V-E, Supplementary Table S9):** We transparently addressed the reviewer's query regarding cold-start mules, providing head-to-head empirical ablations showing that the degree gate adaptively attenuates GNN weights ($\bar{\alpha}_u \approx 0.08$) to fall back to physical conservation laws, preventing catastrophic GNN collapse.
4. **Leveled Baseline Comparisons with Invariant Augmentation & Parameter Calibration (Section V-C, Supplementary Table S12):** We benchmarked all baselines under dual protocols (raw attributes vs. invariant-augmented features) and parameter-matched architectures ($1.8 \times 10^6$ parameters) to demonstrate that architectural innovations—not feature engineering alone—drive our empirical superiority.
5. **Reframed Regulatory Filing as Human-in-the-Loop Assisted Decision Support (Section VI-C, Appendix, Supplementary Fig. S20):** We explicitly rebranded the multi-agent LLM pipeline from autonomous filing to an **Assisted Compliance Decision Support System (CDSS)**, formalizing mandatory Bank Secrecy Act (BSA) Officer review and cryptographic sign-off under Federal Reserve SR 11-7 / SR 26-2.
6. **Resolved Numerical Stabilities (Section IV-A, Section IV-E):** Added explicit logarithmic clamping for Hawkes intensity $\tilde{\lambda}_u(t)$ and documented a 5-epoch Focal Loss warmup curriculum for the Soft-F1 / Asymmetric Tversky loss.

Below, we address each of the reviewer's major and minor comments point-by-point.

---

## Detailed Point-by-Point Rebuttal & Action Log

### Critique 1: Exchangeability Violations in Streaming Conformal Risk Control
> **Reviewer's Remark:** *"Standard Split Conformal Prediction assumes exchangeability between calibration and test data points... The authors invoke a Total Variation drift correction via the DKW inequality... This application is mathematically invalid as stated. The classical DKW inequality bounds the supremum deviation between an empirical distribution function and its underlying true distribution under i.i.d. draws. DKW does not bound the distribution shift ($d_{\mathrm{TV}}$) between two distinct distributions $\mathcal{P}_{\text{cal}}$ and $\mathcal{P}_{\text{test}}$... The stated theoretical coverage guarantee is either tautological or theoretically unsupported."*

**Author Response:**
We thank the reviewer for this crucial theoretical correction. The reviewer is completely correct: the classical DKW inequality applies strictly to the finite-sample concentration of an empirical CDF toward its *own* parent distribution and cannot bound external environmental distribution shift ($d_{\mathrm{TV}}$).

**Revisions Made:**
1. **Decoupled Formulation in Main Text (Section IV-F, Equations 178–181):** We decomposed the class-conditional coverage error into an external environmental drift term and an internal finite-sample concentration term via the triangle inequality:
   $$\big| \mathbb{P}_t(Y \in \Gamma(X) \mid Y=y) - (1 - \alpha) \big| \le d_{\mathrm{TV}}(\mathcal{P}_t, \mathcal{P}_{t - W_{\text{cal}}}) + \sup_{s} \big| F_{\text{cal}}^{(y)}(s) - \hat{F}_{\text{cal}}^{(y)}(s) \big|$$
2. **Applied DKW Strictly to Calibration Concentration (Equation 182):** With probability at least $1 - \delta$:
   $$\sup_{s} \big| F_{\text{cal}}^{(y)}(s) - \hat{F}_{\text{cal}}^{(y)}(s) \big| \le \sqrt{\frac{\ln(2/\delta)}{2 |\mathcal{D}_{\text{cal}}^{(y)}(t)|}}$$
   This clarifies that sampling estimation error vanishes at $\mathcal{O}(1/\sqrt{n(y)})$, while environmental drift $d_{\mathrm{TV}}$ is an external parameter governed by temporal stability within the 4-week window.
3. **Rigorous Proof in Supplementary Material (Section D.1):** We provided a comprehensive proof utilizing the maximal coupling characterization of total variation distance ($|\mathbb{P}_t(S^{(y)} \in A) - \mathbb{P}_{\text{cal}}(S^{(y)} \in A)| \le d_{\mathrm{TV}}$) and the Massart (1990) tight constant for DKW.
4. **Adaptive Conformal Inference (ACI) Online Guarantee:** We formalized the ACI dynamical update $\alpha_t \leftarrow \alpha_{t-1} + \gamma (\alpha - \text{err}_t)$ (Gibbs & Candès, 2021; Barber et al., 2023), proving that Martingale concentration ensures long-run marginal coverage $\lim_{T \to \infty} \frac{1}{T} \sum_{t=1}^T \text{err}_t = \alpha$ almost surely, even under arbitrary bounded non-stationary drift.

---

### Critique 2: Latent GraphSMOTE Bilinear Link Leakage Across Temporal Splits
> **Reviewer's Remark:** *"In dynamic graphs, synthetic edge interpolation is prone to subtle data leakage... When synthetic illicit nodes $\tilde{v}$ are created at time step $t_k$, does the decoder allow synthetic edges to form with nodes $u$ that only appeared at $t_{k+1}$ or later? Provide explicit mathematical proof that the bilinear edge generator is strictly masked by a causal temporal matrix $\mathbf{M}_{ij} = \mathbb{I}(t_j \le t_i)$."*

**Author Response:**
We appreciate this sharp insight. In dynamic graph benchmark evaluation, acausal link generation is a insidious source of lookahead bias. We have made the causal temporal constraints explicit both mathematically and programmatically.

**Revisions Made:**
1. **Causal Temporal Indicator in Equation (117) (Section IV-C):**
   $$\hat{\mathbf{A}}_{\text{syn}, w} = \sigma\left( \mathbf{h}_{\text{syn}}^T \mathbf{W}_{\text{edge}} \mathbf{h}_w \right) \cdot \mathbb{I}(t_w \le t_{\text{syn}}) > \tau_{\text{edge}}, \quad w \in \mathcal{C}_{\text{cand}}(\mathbf{h}_{\text{syn}}) \cap \mathcal{V}_{\text{train}}^{\le t_{\text{syn}}}$$
   where $t_{\text{syn}} = \max(t_u, t_v)$ defines the causal birth timestamp inherited from parent seed nodes $u, v \in \mathcal{C}_k$.
2. **Formal Proof of Zero-Leakage (Supplementary Lemma S2):** We added Lemma~S2 (*Causal Isolation of Latent Topological Oversampling*), proving that:
   $$\mathcal{V}(\tilde{\mathcal{G}}_{\text{train}}) \cap \big(\mathcal{V}_{\text{val}} \cup \mathcal{V}_{\text{cal}} \cup \mathcal{V}_{\text{test}}\big) = \emptyset, \quad \text{and} \quad \forall (i, j) \in \mathcal{E}(\tilde{\mathcal{G}}_{\text{train}}), \; \max(t_i, t_j) \le t_{\text{train}}$$
   establishing that the mutual information $I(\tilde{\mathcal{G}}_{\text{train}}; \mathcal{D}_{\text{test}} \mid \mathcal{D}_{\text{train}}) = 0$.

---

### Critique 3: Realism of Adversarial Camouflage Modeling
> **Reviewer's Remark:** *"While injecting edges to top-degree hubs tests degree bias, it is a simplified proxy for actual financial camouflage... Real-world laundering utilizes nested layering chains, smurfing (<$10k), dormant accounts, and round-trip shell invoicing... Rephrase claims from 'universal camouflage immunity' to 'synthetic hub-association camouflage'."*

**Author Response:**
The reviewer's point is well-taken. High-degree commercial hub injection tests an architecture's immunity to degree over-smoothing, but does not capture the full behavioral diversity of multi-tier professional money laundering.

**Revisions Made:**
1. **Reframed Camouflage Claims (Section V-G):** We added explicit context clarifying that degree-matched and white-box gradient attacks serve as mathematical stress tests of edge-filtration bounds, whereas real-world laundering utilizes structured multi-tier layering (smurfing fan-out, circular wash trades, and peeling chains).
2. **Complementary Protective Coverage:** We clarified that while the Edge Trust Gate ($\hat{g}_{ij}$) suppresses commercial hub chaff, the Tri-Band Temporal Attention and Kirchhoff Flow Invariants ($\tilde{\Phi}_{\text{flow}}$) directly target structured peeling chains and rapid pass-through conduits (as demonstrated in the 15-node qualitative case study in Section~VI-A).

---

### Critique 4: The Cold-Start Dilemma: Is the GNN Doing Any Work?
> **Reviewer's Remark:** *"For cold-start nodes ($d_u \le 2$), the authors state that $\alpha_u$ drops to approximately $0.08$–$0.12$... When $\alpha_u = 0.08$, the GNN provides less than 10% of the final classification vector, and prediction is driven almost entirely by the MLP/GBDT over 12-D invariants... Is this a breakthrough in Graph Representation Learning, or is it an ensemble where a tabular invariant model saves a struggling GNN on sparse graphs? The authors must perform an explicit head-to-head ablation on the cold-start subset."*

**Author Response:**
This is an incisive and candid observation. Rather than obscuring this behavior, we now address it head-on as a major architectural virtue: **an intentional topological fail-safe**.

Standard GNNs suffer catastrophic representation failure on isolated entities ($d \le 1$) because isotropic message aggregation degenerates into uninformative self-loops. By contrast, C-STGB incorporates physical conservation laws as a permanent floor.

**Revisions Made:**
1. **Cold-Start Dissection Added to Section V-E & Supplementary Table S9:**
   - On the cold-start subset ($d_u = 1$, comprising $38.4\%$ of mules on Elliptic-v1):
     - **Standalone Hawkes-HGT:** Collapses to $18.40 \pm 1.15\%$ F1 due to structural starvation.
     - **Tabular GBDT on 12-D Invariants:** Delivers $84.60 \pm 0.85\%$ F1.
     - **C-STGB Dynamic Gated Hybrid:** Achieves $\mathbf{89.60 \pm 0.62\%}$ F1 ($\bar{\alpha}_u = 0.08$).
2. **Framing as a Continuous Safety Valve (Section IV-E, Section VII-A):** We clarified in the text that the gating parameter $\alpha_u$ acts as a continuous topological confidence estimator. It gracefully shifts reliance to physical mass-balance invariants when relational topology is sparse ($d \le 2$), while ramping up to $\alpha_u = 0.91$ to capture complex multi-hop cycles when dense relational topology ($d > 20$) is present.

---

### Critique 5: Baseline Fairness and Parameter Budget Discrepancies
> **Reviewer's Remark:** *"Did baselines receive the 12-D deterministic invariants? If XGBoost and TGN were only provided raw attributes while the proposed model had 12 hand-engineered invariants, the comparison is confounded... What is the total parameter count compared to baseline E-GCN or GAT? Report parameter-matched architectures."*

**Author Response:**
We agree completely that baseline comparisons must eliminate both feature unfairness and capacity confounding.

**Revisions Made:**
1. **Dual-Track Evaluation Protocol Documented in Section V-C:**
   - *Canonical Feature Protocol:* Baselines evaluated on raw benchmark features.
   - *Invariant-Augmented Protocol:* Baselines receive the identical concatenated feature matrix $[\mathbf{x}_u \,\|\, \mathbf{z}_{\text{inv}}(u, t)] \in \mathbb{R}^{d_v + 12}$.
   - We report that baseline XGBoost achieves $99.89\%$ on Elliptic-v1, and C-STGB achieves $99.44\%$ with perfect PR-AUC ($1.0000$), while decisively outperforming deep GNN baselines by $+43.49$ to $+48.32$ pp and outperforming tree models under severe banking imbalance ($37.70\%$ vs. $36.66\%$ on IBM-AMLSim HI).
2. **Parameter Budget Matching (Section V-C, Supplementary Table S12):** We report calibrated parameter counts: C-STGB ($1.84 \times 10^6$ parameters), scaled Vanilla HGT ($1.80 \times 10^6$), and scaled TGN ($2.12 \times 10^6$), confirming that C-STGB's lead is not an artifact of parameter over-parameterization.

---

### Critique 6: Regulatory Compliance Overreach (LLM Hallucinations & Fed SR 11-7)
> **Reviewer's Remark:** *"Regulators do not permit unconstrained, generative LLM narratives to file automated Suspicious Activity Reports without deterministic human validation... LLMs are non-deterministic and prone to hallucination... Tone down claims of 'fully autonomous filing'. Reframe as an 'Assisted Compliance Decision Support System' with mandatory BSA Officer sign-off."*

**Author Response:**
We thank the reviewer for this essential compliance grounding. Automated submission of legal filings without human review is legally unviable under the Bank Secrecy Act (BSA) and Federal Reserve SR 11-7 / SR 26-2.

**Revisions Made:**
1. **Rebranded as Assisted Decision Support System (Section VI-C, Appendix):** We reframed the multi-agent LLM module from autonomous filing to an **"Assisted Compliance Decision Support System (CDSS)"**.
2. **Mandatory Human-in-the-Loop Sign-Off Node:** We explicitly articulated that the multi-agent swarm serves solely to accelerate investigative dossier compilation (reducing drafting time from 45.0 min to 28.4 s). Final submission authority resides exclusively with a human certified Bank Secrecy Act (BSA) Officer who must inspect the dossier and execute a digital cryptographic signature.
3. **Deterministic Compiler Exception Fallback:** Documented that any AST schema or graph-membership validation failure triggers a local greedy retry ($T=0.0$); if validation fails twice, machine drafting aborts, and the case is routed to the compliance officer's manual workbench with an anomaly trace log.

---

### Critique 7: Numerical Stabilities (Hawkes Clamping & Soft-F1 Warmup)
> **Reviewer's Remark:** *"When $t - t_i \to 0$, Hawkes intensity $\lambda_r$ spikes abruptly... $\log \lambda_r$ can overflow or dominate attention... In extreme class imbalance, Soft-F1 gradients become unstable early in training... Specify explicit clamping and curriculum warmup."*

**Author Response:**
Both observations identify genuine numerical edge cases under extreme streaming velocity and extreme class skew.

**Revisions Made:**
1. **Hawkes Intensity Clamping (Section IV-A, Invariant 3):** Added explicit bounded logarithmic clamping:
   $$\tilde{\lambda}_u(t) = \log \min\left(\max(\lambda_u(t), 10^{-5}), 10^4\right)$$
   strictly preventing numerical overflow or one-hot degenerate softmax attention collapse.
2. **Curriculum Loss Warmup (Section IV-E):** Documented a 5-epoch warmup curriculum using Cost-Sensitive Focal Loss before engaging the non-convex Soft-F1 / Asymmetric Tversky multi-objective head.
3. **Transaction Fee Absorption in Flow Conservation (Section IV-A, Invariant 1):** Explicitly noted that transaction clearing fees and gas burn ($\le 1.5\%$) are natively absorbed within the empirical tolerance band $\Phi_{\text{flow}} \in [1-\bar{\epsilon}, 1.0]$, preventing false-positive flags on high-fee corridors.

---

## Summary of Revisions by Manuscript Section

| Section in Revised Manuscript | Nature of Revisions |
| :--- | :--- |
| **Section IV-A (Invariants 1 & 3)** | Added fee tolerance band $[1-\bar{\epsilon}, 1.0]$; added bounded numerical clamping $\tilde{\lambda}_u(t)$ for Hawkes intensity. |
| **Section IV-C (Module 3: GraphSMOTE)** | Added causal temporal indicator $\mathbb{I}(t_w \le t_{\text{syn}})$ to Equation (117); added zero future-split leakage statement. |
| **Section IV-E (Module 4: Adaptive Fusion)** | Framed degree gate $\alpha_u$ as a continuous topological confidence estimator and intentional safety valve for cold-start stubs. |
| **Section IV-E (Module 5: Loss Objective)** | Added 5-epoch Focal Loss curriculum warmup to stabilize Soft-F1 optimization. |
| **Section IV-F (Module 6: Conformal Risk Control)** | Rewrote error decomposition, decoupling DKW empirical process concentration from external environmental TV drift; added ACI Martingale guarantees. |
| **Section V-C (Baseline Protocols)** | Added dual-track evaluation protocol (canonical vs. invariant-augmented) and parameter-matched budget calibration ($1.84\times 10^6$ parameters). |
| **Section V-E (Ablation Analysis)** | Added cold-start ($d \le 2$) dissection: Standalone HGT ($18.4\%$), Tabular GBDT ($84.6\%$), C-STGB Hybrid ($89.60\%$). |
| **Section V-G (Adversarial Camouflage)** | Added operational context distinguishing synthetic hub perturbation from structured peeling chains. |
| **Section VI-C (Qualitative Case Study)** | Rebranded to *Assisted Compliance Decision Support System*; added mandatory BSA Officer sign-off and compiler fallback exception handling. |
| **Section VII & VIII (Discussion & Limitations)** | Expanded on division of labor, synthetic simulator boundaries, and macroeconomic shock bounds. |
| **Section IX (Appendix)** | Added BSA Officer cryptographic countersignature requirement to Proposition S1 remark. |
| **Supplementary Section D.1 & D.2** | Rewrote DKW proof via maximal coupling and Massart tight bounds; added Lemma S2 on Causal GraphSMOTE Purity. |

---

We thank the Senior Reviewer again for their rigorous evaluation, which has helped us make this manuscript significantly more robust, precise, and impactful for publication in *IEEE Transactions on Information Forensics and Security*.
