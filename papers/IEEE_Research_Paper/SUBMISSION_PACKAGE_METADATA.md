# 📦 IEEE TKDE Submission Package & Author Declarations

**Manuscript Title:** *Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage*  
**Short Running Title:** *Nazmul et al.: Risk-Controlled Spatio-Temporal Graph Learning for AML*  
**Target Journal:** *IEEE Transactions on Knowledge and Data Engineering (TKDE)*  
**Journal Scope:** Graph Data Mining, Temporal Graph Learning, Anomaly Detection, Financial Forensics  
**Corresponding Author:** Md. Nazmul (`nazmulhas36@gmail.com`)  

---

## 🌟 1. Research Highlights (Portal Ready, Strictly $\le 85$ Characters, Plain Text)

- **Highlight 1:** `Unified C-STGB framework for AML under extreme class imbalance (<0.05%).` *(72 chars)*
- **Highlight 2:** `Continuous tri-band temporal attention prunes 65.9% of camouflage edges.` *(72 chars)*
- **Highlight 3:** `Class-conditional conformal risk control guarantees >= 99.0% coverage.` *(70 chars)*
- **Highlight 4:** `Benchmarked across 14 networks with 0.45 ms fast-path latency.` *(61 chars)*

---

## 👥 2. Suggested Independent Reviewers (Official Institutional Emails)

| # | Nominated Reviewer | Academic Title & Institution | Institutional Email | Department / Location | Area of Expertise | Reason for Nomination |
|---|---|---|---|---|---|---|
| **1** | **Prof. Mark Weber** | Research Scientist, MIT-IBM Watson AI Lab; Fellow, Harvard | `mweber@mit.edu` | Cambridge, MA, USA | Bitcoin Graph Learning & AML | Lead creator of the Elliptic Bitcoin dataset; pioneer of GNNs in financial compliance. |
| **2** | **Prof. Yingtong Dou** | Assistant Professor, University of Illinois Chicago | `ydou5@uic.edu` | Dept. of Computer Science, Chicago, IL, USA | Adversarial Graph Fraud Detection | Author of CARE-GNN (CIKM 2020); principal authority on relation-aware graph camouflage defense. |
| **3** | **Prof. Anastasios N. Angelopoulos** | Postdoctoral Scholar / Faculty, UC Berkeley & Stanford | `angelopoulos@berkeley.edu` | Dept. of EECS, Berkeley, CA, USA | Conformal Risk Control & DFUQ | Principal author of Learnable Conformal Risk Control and distribution-free uncertainty quantification. |
| **4** | **Dr. Claudio Bellei** | Principal Research Scientist, Elliptic Labs | `claudio.bellei@elliptic.co` | London, United Kingdom | Multi-Asset Graph Forensics | Principal investigator and architect of the Elliptic2 multi-asset subgraph benchmark dataset (2024). |

---

## 📜 3. CRediT (Contributor Roles Taxonomy) Author Statement

- **Md. Nazmul** (ORCID: [0009-0001-6115-7023](https://orcid.org/0009-0001-6115-7023)): Conceptualization, Methodology, Software Architecture, Mathematical Derivations, Empirical Evaluation, Investigation, Writing – Original Draft, Visualization, Project Administration.
- **Musrat Jahan Gungun** (ORCID: [0009-0006-4249-9198](https://orcid.org/0009-0006-4249-9198)): Data Curation, Validation, Statistical Significance Testing, Baseline Benchmarking, Writing – Review & Editing.
- **Maheli Ahmed (Supervisor)** (ORCID: [0000-0002-5183-7498](https://orcid.org/0000-0002-5183-7498)): Supervision, Resources, Funding Acquisition, Formal Analysis, Model Governance Alignment, Writing – Review & Editing.

---

## 🔒 4. Mandatory Ethical & Regulatory Declarations

- **Funding Statement:** This research received no specific external grant from any funding agency in the public, commercial, or not-for-profit sectors.
- **Conflict of Interest:** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
- **Data Availability:** All public benchmark datasets (Elliptic-v1, Elliptic-v2, Ethereum Phishing, XBlock-ETH, PaySim, SAML-D, Mt. Gox, IBM-AMLSim, DGraphFin) are openly accessible from their respective repositories. Complete preprocessing scripts and synthetic dataset generators are provided in the repository.
- **Code & Reproducibility:** The complete, fully reproducible source code, trained model checkpoints, and configuration pipelines are publicly maintained at: [https://github.com/NazmulHasanNihal/Intelligent-AML](https://github.com/NazmulHasanNihal/Intelligent-AML).
- **Ethics & Privacy:** All evaluations were performed on publicly released, cryptographically anonymized, or synthetic benchmark datasets. No non-public personal customer identifying information (PII) was collected or processed.

---

## 📑 5. ScholarOne Portal Quick Entry & Disclosures Guide (IEEE TKDE)

### Portal URL:
Log into IEEE Computer Society ScholarOne Manuscripts:
**`https://mc.manuscriptcentral.com/tkde-cs`**

### Step 1: Type, Title, Running Head, & Abstract
- **Manuscript Type:** Regular Paper (13.0 Pages)
- **Full Title:** `Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage`
- **Running Head:** `Nazmul et al.: Risk-Controlled Spatio-Temporal Graph Learning for AML`
- **Plain-Text Abstract (Portal Ready):**
  > Financial money laundering moves an estimated $800B–$2T annually across global financial rails. While Graph Neural Networks (GNNs) capture relational topologies, practical Anti-Money Laundering (AML) surveillance is hindered by velocity evasion, topological camouflage, extreme class imbalance (pi < 0.05%), cold-start isolation, and uncalibrated uncertainty. We propose C-STGB (Conformal Spatio-Temporal GraphBoost), an integrated risk-controlled temporal graph learning framework combining continuous harmonic temporal attention, learnable edge-trust gating, typology-clustered latent GraphSMOTE, evidence-adaptive graph-tabular fusion, and Class-Conditional Conformal Risk Control (CRC). Benchmarked across 14 financial transaction networks (9.53M entities, 9.53M transactions, 182 evaluation pairs over five locked seeds), C-STGB achieves an unweighted macro F1 of 67.26% (0.6848 PR-AUC). This establishes parity with tuned gradient-boosted decision trees (XGBoost 67.92%, p=0.8077; CatBoost 67.14%, p=0.4318) which excel on flat transaction streams, alongside statistically significant outperformance over evaluated deep GNNs (+43.49 pp mean uplift over GCN; W=105.0, p_adj < 0.001), with advantages concentrated in graph-rich relational regimes. Furthermore, C-STGB provides finite-sample coverage (>= 99.0%) under within-class exchangeability with Adaptive Conformal Inference (ACI) drift tracking, routing >99.4% of volume into decisive singleton prediction sets while achieving a streaming Fast-Path inference latency of 0.45 ms per event.

### Step 2: File Upload
1. **Main Document:** `papers/IEEE_Research_Paper/main.pdf` *(File Designation: Main Document / Manuscript)* — strictly 13.0 pages.
2. **Supplementary Material:** `papers/IEEE_Research_Paper/supplementary.pdf` *(File Designation: Supplementary Material for Review)* — strictly 6.0 pages.
3. **Cover Letter:** `papers/IEEE_Research_Paper/Cover_Letter_IEEE_TKDE.pdf` *(File Designation: Cover Letter)* — strictly 1.0 page.

### Step 3: Keywords & Categories
- Primary Keywords:
  - `Anti-Money Laundering`
  - `Graph Neural Networks`
  - `Temporal Graph Learning`
  - `Conformal Prediction`
  - `Financial Forensics`
  - `Anomaly Detection`

### Step 4: Author Details & ORCIDs
- **Author 1 (Corresponding):** Md. Nazmul (`nazmulhas36@gmail.com`) | ORCID: `0009-0001-6115-7023`
- **Author 2:** Musrat Jahan Gungun (`gungunjahan84@gmail.com`) | ORCID: `0009-0006-4249-9198`
- **Author 3 (Supervisor):** Maheli Ahmed (`maheli.ahmed.cse.cot@gmail.com`) | ORCID: `0000-0002-5183-7498`
- **Institution:** Department of Computer Science and Engineering, College of Technology, National University, Gazipur 1704, Bangladesh

---

## 🛠️ 6. Step-by-Step Portal Disclosures Checklist

1. **Question: "Has this manuscript or substantial portions of it been published, accepted, or submitted for publication elsewhere?"**
   - **Action:** Select **`No`**.
   - **Explanation text (if box appears):**  
     `"This manuscript is an entirely original work that has not been submitted, accepted, or published in any conference, workshop, or journal."`

2. **Question: "Has this manuscript (or an earlier version) been deposited on a preprint server (e.g., arXiv)?"**
   - **Action:** Select **`No`** (unless you already posted it on arXiv; if posted, select `Yes` and input the arXiv link).

3. **Question: "Does this submission include Supplemental Material?"**
   - **Action:** Select **`Yes`**.
   - **Explanation text:**  
     `"The accompanying Supplementary Material document is strictly formatted to 6 double-column pages using IEEEtran, in full compliance with IEEE TKDE supplemental guidelines."`

4. **Question: "Funding Disclosure / Research Grant Information"**
   - **Action:** Paste:  
     `"This research received no specific external grant from any funding agency in the public, commercial, or not-for-profit sectors."`

5. **Question: "Conflict of Interest Declaration"**
   - **Action:** Paste:  
     `"The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."`

6. **Question: "Data Availability Statement"**
   - **Action:** Paste:  
     `"All 14 benchmark datasets evaluated in this study are publicly accessible. Complete pipelines, scripts, and checkpoints are open-sourced at https://github.com/NazmulHasanNihal/Intelligent-AML."`

7. **Question: "Confirm Author Review and Approval"**
   - **Action:** Check **`Yes`** *(All authors have reviewed and approved the manuscript submission).*
