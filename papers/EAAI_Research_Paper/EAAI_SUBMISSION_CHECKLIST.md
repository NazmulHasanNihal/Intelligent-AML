# 📋 Elsevier EAAI Author Playbook: Complete Compliance Audit & Submission Checklist

**Manuscript Title:** *Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage*  
**Short Running Title:** *Risk-Controlled Spatio-Temporal Graph Learning for AML*  
**Target Journal:** *Engineering Applications of Artificial Intelligence* (EAAI), Elsevier  
**Journal Scope:** Applied Artificial Intelligence, Financial Engineering, Graph Deep Learning, Statistical Risk Control  
**Editorial Manager Portal:** [https://www.editorialmanager.com/eaai/](https://www.editorialmanager.com/eaai/)  
**Publishing Model:** **Subscription Track ($0 Open Access APC / Free Publishing)**

---

## 🏆 Summary of Files in the EAAI Submission Suite (`papers/EAAI_Research_Paper/`)

| File | Description | Purpose in Elsevier Portal |
|---|---|---|
| `Title_Page.pdf` (`Title_Page.tex`) | Unanonymized title page with full author names, affiliations, emails, ORCIDs, corresponding author details, CRediT statement, funding, declarations, and acknowledgments. | **Item Type:** `Title Page` |
| `Anonymized_Manuscript.pdf` (`Anonymized_Manuscript.tex`) | Blinded manuscript body using Elsevier CAS double-column template (`cas-dc.cls`). Zero author names, zero affiliations, zero acknowledgments, zero author bios, anonymized URLs. | **Item Type:** `Manuscript` |
| `Anonymized_Supplementary.pdf` (`Anonymized_Supplementary.tex`) | Blinded supplementary material using standard `article` class with `natbib` APA 7th citations (`\citep`), containing formal proofs, 14-dataset benchmark matrices, and hyperparameter sensitivity profiles. | **Item Type:** `Supplementary Material` |
| `Highlights.pdf` (`Highlights.tex` / `Highlights.md`) | Exactly 5 bullet points, each strictly $\le 85$ characters including spaces. | **Item Type:** `Highlights` |
| `Cover_Letter_EAAI.pdf` (`Cover_Letter_EAAI.tex`) | Formal cover letter addressed to the Editor-in-Chief highlighting the applied artificial intelligence mandate, 0.45 ms SLA compliance, lack of military use, and double-blind review. | **Item Type:** `Cover Letter` |
| `Declaration_of_Competing_Interests.pdf` (`Declaration_of_Competing_Interests.tex`) | Official conflict of interest declaration. | **Item Type:** `Conflict of Interest` |
| `Declaration_of_Generative_AI.pdf` (`Declaration_of_Generative_AI.tex`) | Standalone declaration titled *Declaration of generative AI and AI-assisted technologies in the manuscript preparation process*. | **Item Type:** `Declaration of Generative AI` |
| `ORCID_Information.tex` | Standalone author identification and ORCID verification file with direct profile links and metadata table. | **Item Type:** `Supplementary Material` / `Title Page Attachment` |

---

## ✅ Item-by-Item Verification Against EAAI Author Playbook

### A. Scope & Fit
- [x] **1. Applied AI Mandate:** Framed as an end-to-end applied artificial intelligence and decision-support surveillance system (C-STGB) for operational Financial Intelligence Units (FIUs), integrating continuous temporal graph representation learning, conformal risk triage, and human-in-the-loop compliance dossiers (Federal Reserve SR 11-7).
- [x] **2. No Military/Defense Applications:** Confirmed. The domain is strictly civilian financial forensics and anti-money laundering compliance.
- [x] **3. Avoid Nature-Inspired Metaphor Algorithms:** Grounded entirely in rigorous mathematics (harmonic Fourier analysis, Hawkes point processes, latent manifold interpolation, and distribution-free conformal inference).
- [x] **4. Substantive Application Depth:** Evaluated on 14 real-world and synthetic financial transaction networks ($8.81\text{M}$ entities, $11.42\text{M}$ transactions across 182 evaluation pairs over five locked seeds), with production-grade $0.45$\,ms single-event streaming latency.

### B. Ethics, Policy & Declarations
- [x] **5. Submission Declaration:** Included in `Title_Page.tex` and `Cover_Letter_EAAI.tex`, confirming originality and absence of concurrent review.
- [x] **6. Declaration of Competing Interests:** Dedicated file `Declaration_of_Competing_Interests.tex` and unnumbered section in `Title_Page.tex`.
- [x] **7. Funding Statement:** Explicitly stated ("This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.") in both `Title_Page.tex` and `Cover_Letter_EAAI.tex`.
- [x] **8. Declaration of Generative AI Use:** Mandatory dedicated section placed right before references in `Anonymized_Manuscript.tex` and standalone file `Declaration_of_Generative_AI.tex`, titled exactly:  
  `Declaration of generative AI and AI-assisted technologies in the manuscript preparation process`.
- [x] **9. CRediT Author Contribution Statement:** Formally assigned roles in `Title_Page.tex`:
  - **Md. Nazmul:** Conceptualization, Methodology, Software Architecture, Mathematical Derivations, Empirical Evaluation, Investigation, Writing – Original Draft, Visualization, Project Administration.
  - **Musrat Jahan Gungun:** Data Curation, Validation, Statistical Significance Testing, Baseline Benchmarking, Writing – Review & Editing.
  - **Maheli Ahmed:** Supervision, Resources, Funding Acquisition, Formal Analysis, Model Governance Alignment, Writing – Review & Editing.
- [x] **10. Data Availability Statement:** Dedicated section in `Anonymized_Manuscript.tex` and `Title_Page.tex` meeting Elsevier requirements with persistent blinded repository link: `https://anonymous.4open.science/r/Intelligent-AML`.
- [x] **11. Authorship Locked:** Confirmed at initial submission.

### C. Double-Blind Review Compliance
- [x] **12. Completely Blinded Manuscript:** `Anonymized_Manuscript.tex` contains NO author names, affiliations, or institutional identifiers.
- [x] **13. Separate Unblinded Title Page:** Provided in `Title_Page.tex` / `Title_Page.pdf`.
- [x] **14. Self-Citations Neutral:** Refers to prior literature in third person.
- [x] **15. Anonymized Code Repository:** Blinded URL used throughout: `https://anonymous.4open.science/r/Intelligent-AML`.

### D. Formatting & Technical Standards
- [x] **16. Highlights:** Exactly 5 bullets, each $\le 85$ characters including spaces.
- [x] **17. Abstract:** Self-contained, under 250 words, summarizing context, methodology, quantitative results ($68.05\%$ Macro F1, $0.6974$ PR-AUC, $+3.29\text{ pp}$ over XGBoost, $+43.49\text{ pp}$ over GCN), and production latency ($0.45\text{ ms}$).
- [x] **18. Keywords:** 7 keywords: Anti-money laundering, Applied artificial intelligence, Graph neural networks, Temporal graph learning, Class imbalance, Conformal prediction, Financial forensics.
- [x] **19. Line Numbers:** Continuous line numbering enabled via `\linenumbers`.
- [x] **20. High-Resolution Figures:** Vector PDFs in `figures/` directory.

---

## 🚀 Stage 7: EAAI Editorial Manager Portal Step-by-Step Submission Guide

### Step 1: Login & Select Article Type
1. Navigate to: **[https://www.editorialmanager.com/eaai/](https://www.editorialmanager.com/eaai/)**
2. Log in using your Elsevier / ORCID account credentials.
3. Click **"Submit New Manuscript"**.
4. **Select Article Type:** Choose **`Full Length Article`** (or **`Research Paper`**).

### Step 2: Attach Files
Upload the generated PDF documents in the specified order with the exact item types:
1. **Item Type:** `Cover Letter` $\to$ Upload `Cover_Letter_EAAI.pdf`
2. **Item Type:** `Highlights` $\to$ Upload `Highlights.pdf`
3. **Item Type:** `Title Page` $\to$ Upload `Title_Page.pdf`
4. **Item Type:** `Manuscript` $\to$ Upload `Anonymized_Manuscript.pdf`
5. **Item Type:** `Supplementary Material` $\to$ Upload `Anonymized_Supplementary.pdf`
6. **Item Type:** `Conflict of Interest` $\to$ Upload `Declaration_of_Competing_Interests.pdf`
7. **Item Type:** `Declaration of Generative AI` $\to$ Upload `Declaration_of_Generative_AI.pdf`

### Step 3: Classifications & Research Areas
Select 3–5 classifications in the portal:
- *Artificial Intelligence in Finance / Economics*
- *Graph Neural Networks / Relational Learning*
- *Machine Learning Applications*
- *Pattern Recognition and Anomaly Detection*
- *Risk Analysis and Decision Support Systems*

### Step 4: Enter Manuscript Details
- **Full Title:** `Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage`
- **Short Title:** `Risk-Controlled Spatio-Temporal Graph Learning for AML`
- **Abstract:** Copy-paste the exact abstract from `Anonymized_Manuscript.tex`.
- **Keywords:** `Anti-money laundering`, `Applied artificial intelligence`, `Graph neural networks`, `Temporal graph learning`, `Class imbalance`, `Conformal prediction`, `Financial forensics`.

### Step 5: Author Information
Verify that all 3 authors are entered in the system matching `Title_Page.pdf`:
1. **First Author & Corresponding Author:**
   - Name: **Md. Nazmul**
   - Email: `nazmulhas36@gmail.com`
   - Institution: National University, Gazipur, Bangladesh
   - ORCID: `0009-0001-6115-7023`
2. **Co-Author:**
   - Name: **Musrat Jahan Gungun**
   - Email: `gungunjahan84@gmail.com`
   - Institution: National University, Gazipur, Bangladesh
   - ORCID: `0009-0006-4249-9198`
3. **Co-Author & Supervisor:**
   - Name: **Maheli Ahmed**
   - Email: `maheli.ahmed.cse.cot@gmail.com`
   - Institution: National University, Gazipur, Bangladesh
   - ORCID: `0000-0002-5183-7498`

### Step 6: Suggested Reviewers
Provide 3–4 non-conflicted international experts in graph learning and AML:
1. **Prof. Mark Weber** (MIT-IBM Watson AI Lab) - *Expert in Bitcoin Elliptic graph benchmarking and AML graph architectures.*
2. **Prof. Jianfei Gao / Prof. Xiao-Ming Wu** - *Experts in temporal graph neural networks and structural camouflage detection.*
3. **Prof. Anastasios N. Angelopoulos** (UC Berkeley) - *Expert in distribution-free conformal prediction and risk control.*
4. **Prof. Toyotaro Suzumura** (The University of Tokyo / IBM Research) - *Creator of IBM-AMLSim benchmark and large-scale financial graph computing.*

### Step 7: Publishing Model Selection ($0 Subscription Track)
When prompted by the Elsevier portal regarding Open Access vs. Subscription:
- **Choose the Subscription Publishing Track:** Select **`Subscription`** (also labeled as **`Publish Under Subscription`** or **`Standard Publishing / No Open Access Fee`**).
- **Cost:** **$0 (Zero USD)**. There are NO submission fees, NO page charges, and NO APC fees for subscription publication in EAAI.
- If asked about Open Access mandates, decline immediate gold open access unless sponsored by external institutional open access agreements.

### Step 8: Build and Approve the Combined PDF
1. Click **"Build PDF for Approval"**.
2. Wait 1–3 minutes for Elsevier's server to assemble the proof PDF.
3. Download and inspect the PDF:
   - Ensure the blinded manuscript contains NO author names.
   - Verify all figures and tables render sharply.
   - Check that line numbering appears in the margins.
4. Click **"I accept"** and **"Submit Manuscript to Journal"**.

