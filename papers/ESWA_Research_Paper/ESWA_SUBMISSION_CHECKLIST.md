# 📋 Elsevier ESWA Author Playbook: Complete Compliance Audit & Submission Checklist

**Manuscript Title:** *Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage*  
**Short Running Title:** *Risk-Controlled Spatio-Temporal Graph Learning for AML*  
**Target Journal:** *Expert Systems with Applications* (ESWA), Elsevier  
**Journal Scope:** Intelligent Expert Systems, Financial Forensics, Knowledge Discovery, Anomaly Detection  
**Editorial Manager Portal:** [https://www.editorialmanager.com/eswa/](https://www.editorialmanager.com/eswa/)  

---

## 🏆 Summary of Files in the ESWA Submission Suite (`papers/ESWA_Research_Paper/`)

| File / Directory | Description | Purpose in Elsevier Portal |
|---|---|---|
| `Title_Page.tex` / `Title_Page.pdf` | Unanonymized title page with full author names, affiliations, emails, ORCIDs, corresponding author details, CRediT statement, funding, declarations, and acknowledgments. | **Item Type:** `Title Page` |
| `ORCID_Information.tex` / `ORCID_Information.pdf` | Dedicated standalone author identification and ORCID verification file with direct profile links and metadata table. | **Item Type:** `Supplementary Material` / `Title Page Attachment` |
| `Anonymized_Manuscript.tex` | Blinded manuscript body using Elsevier CAS double-column template (`cas-dc.cls`). Zero author names, zero affiliations, zero acknowledgments, zero author bios, anonymized URLs. | **Item Type:** `Manuscript` |
| `Highlights.tex` / `Highlights.md` | Exactly 5 bullet points, each strictly $\le 85$ characters including spaces. | **Item Type:** `Highlights` |
| `Declaration_of_Generative_AI.tex` | Standalone declaration titled *Declaration of generative AI and AI-assisted technologies in the manuscript preparation process*. | **Item Type:** `Declaration of Generative AI` |
| `Declaration_of_Competing_Interests.tex` | Official conflict of interest declaration. | **Item Type:** `Conflict of Interest` |
| `Cover_Letter_ESWA.tex` | Formal cover letter addressed to the Editor-in-Chief highlighting the intelligent systems mandate, lack of military use, and compliance with double-blind review. | **Item Type:** `Cover Letter` |
| `Anonymized_Supplementary.tex` | Blinded supplementary material using standard `article` class with `natbib` APA 7th citations (`\citep`), containing formal proofs, 14-dataset benchmark matrices, and hyperparameter sensitivity profiles. Converted from `IEEEtran` to ensure formatting consistency with the main manuscript. | **Item Type:** `Supplementary Material` |
| `references.bib` | APA 7th edition bibliography with DOIs, software package entries, and `[dataset]` tags. | **Item Type:** `LaTeX Source Files` |
| `cas-dc.cls`, `cas-sc.cls`, `cas-common.sty`, `cas-model2-names.bst` | Official Elsevier CAS LaTeX template and BibTeX style files. | **Item Type:** `LaTeX Source Files` |
| `sections/` | Numbered sections (`01_introduction.tex` to `08_conclusion.tex`) with APA `\citep` and `\citet` citations. | **Item Type:** `LaTeX Source Files` |
| `tables/` | Tables in editable `booktabs` format without vertical rules. | **Item Type:** `LaTeX Source Files` |
| `figures/` | High-resolution vector PDF, EPS, and PNG figures. | **Item Type:** `Figure` |

---

## ✅ Item-by-Item Verification Against ESWA Author Playbook

### A. Scope & Fit
- [x] **1. Intelligent/Expert System Mandate:** Framed as an end-to-end intelligent decision-support and surveillance expert system (C-STGB) for operational Financial Intelligence Units (FIUs), integrating continuous graph representation learning, conformal risk triage, and human-in-the-loop compliance dossiers (Federal Reserve SR 11-7).
- [x] **2. No Military/Defense Applications:** Confirmed. The domain is strictly financial forensics and civil anti-money laundering.
- [x] **3. Avoid Nature-Inspired Metaphor Algorithms:** Grounded entirely in rigorous mathematics (harmonic Fourier analysis, Hawkes point processes, latent manifold interpolation, and distribution-free conformal inference).
- [x] **4. Substantive Application Depth:** Evaluated on 14 real-world and synthetic financial transaction networks ($9.53\text{M}$ entities, $9.53\text{M}$ transactions across 182 evaluation pairs over five locked seeds), with production-grade $0.45$\,ms single-event streaming latency.

### B. Ethics, Policy & Declarations
- [x] **5. Submission Declaration:** Included in `Title_Page.tex` and `Cover_Letter_ESWA.tex`, confirming originality and absence of concurrent review.
- [x] **6. Declaration of Competing Interests:** Dedicated file `Declaration_of_Competing_Interests.tex` and unnumbered section in `Title_Page.tex`.
- [x] **7. Funding Statement:** Explicitly stated ("This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.") in both `Title_Page.tex` and `Cover_Letter_ESWA.tex`.
- [x] **8. Declaration of Generative AI Use:** Mandatory dedicated section placed right before references in `Anonymized_Manuscript.tex` and standalone file `Declaration_of_Generative_AI.tex`, titled exactly:
  `Declaration of generative AI and AI-assisted technologies in the manuscript preparation process`.
- [x] **9. CRediT Author Contribution Statement:** Formally assigned roles in `Title_Page.tex`:
  - **Md. Nazmul:** Conceptualization, Methodology, Software Architecture, Mathematical Derivations, Empirical Evaluation, Investigation, Writing – Original Draft, Visualization, Project Administration.
  - **Musrat Jahan Gungun:** Data Curation, Validation, Statistical Significance Testing, Baseline Benchmarking, Writing – Review & Editing.
  - **Maheli Ahmed:** Supervision, Resources, Funding Acquisition, Formal Analysis, Model Governance Alignment, Writing – Review & Editing.
- [x] **10. Data Availability Statement:** Dedicated section in `Anonymized_Manuscript.tex` and `Title_Page.tex` meeting ESWA "Option C" requirements.
- [x] **11. Authorship Locked:** Confirmed at initial submission.

### C. Double-Anonymized Peer Review
- [x] **12. Two Separate Files:**
  - File 1: `Title_Page.tex` (Unanonymized with author names, affiliations, emails, ORCIDs, CRediT, and acknowledgments).
  - File 2: `Anonymized_Manuscript.tex` (Zero identifying details).
- [x] **13. Author Bios & Photos Stripped:** Completely eliminated from `Anonymized_Manuscript.tex`.
- [x] **14. Neutral Phrasing & Anonymized Links:**
  - Author GitHub URL `https://github.com/NazmulHasanNihal/Intelligent-AML` replaced with anonymized repository link `https://anonymous.4open.science/r/Intelligent-AML`.
  - Self-citations phrased in neutral third person.

### D. Formatting & File Mechanics
- [x] **15. Editable Source Files:** Provided in full `.tex`, `.bib`, `.cls`, `.sty`, and `.bst`.
- [x] **16. Elsevier Official LaTeX Template:** Converted from `IEEEtran.cls` to Elsevier's official `cas-dc.cls` (`els-cas-templates`).
- [x] **17. Formatting Cleanup:** No strikethrough/underline text.
- [x] **18. Template Integrity:** Native Elsevier CAS document class with `cas-common.sty` and `cas-model2-names.bst`.
- [x] **19. Math Equations:** Editable text in LaTeX `align` and `equation` environments; consecutive arabic numbering.

### E. Title Page & Front Matter
- [x] **20. Concise Informative Title:** *Risk-Controlled Spatio-Temporal Graph Learning for Anti-Money Laundering Under Extreme Imbalance and Topological Camouflage*.
- [x] **21. Author Details:** Full names, affiliations, country (Bangladesh), and corresponding author email (`nazmulhas36@gmail.com`) in `Title_Page.tex`.

### F. Abstract, Keywords, Highlights
- [x] **22. Abstract:** 189 words (strictly $\le 250$ words), completely standalone, no citations, no undefined acronyms, stating purpose, methods, key findings, and conclusions.
- [x] **23. Keywords (1 to 7 terms):**
  1. Anti-money laundering
  2. Expert systems
  3. Graph neural networks
  4. Temporal graph learning
  5. Class imbalance
  6. Conformal prediction
  7. Financial forensics
- [x] **24. Highlights (3 to 5 bullets, each $\le 85$ characters):**
  - Point 1 (72 chars): `Unified C-STGB framework for AML under extreme class imbalance (<0.05%).`
  - Point 2 (72 chars): `Continuous tri-band temporal attention prunes 65.9% of camouflage edges.`
  - Point 3 (70 chars): `Class-conditional conformal risk control guarantees >= 99.0% coverage.`
  - Point 4 (72 chars): `Outperforms deep GNNs by +43.5 pp macro F1 across 14 financial networks.`
  - Point 5 (74 chars): `Fast-Path streaming inference achieves 0.45 ms single-event audit latency.`

### G. Body Structure
- [x] **25. Numbered Sections & Subsections:** Converted from Roman numerals to Arabic numerals (1, 1.1, 1.1.1, etc.).
- [x] **26. Abstract Not Numbered:** Compliant.
- [x] **27. Numbered Footnotes:** Sequential arabic numerals.
- [x] **28. Appendices:** Labeled A, B, C... in supplementary document.

### H. Tables & Figures
- [x] **29. Editable Booktabs Tables:** Captions positioned above tables, no vertical rules, clean horizontal rules (`\toprule`, `\midrule`, `\bottomrule`).
- [x] **30. High-Resolution Vector Figures:** Standalone vector PDFs/EPS provided in `figures/`.
- [x] **31. Multi-Panel Figures Separated:**
  - Figure 1: Comprehensive 6-module architecture blueprint (`fig6_system_architecture.pdf`).
  - Figure 2: Precision-Recall and ROC curves on `elliptic_v1` (`fig1_pr_roc_curves.pdf`).
  - Figure 3: Latent manifold t-SNE projection (`fig2_tsne_manifold_separation.pdf`).
  - Figure 4: Adversarial Camouflage Robustness (`fig9_adversarial_camouflage_robustness.pdf`).
  - Figure 5: 15-node qualitative attribution subgraph (`15_node_subgraph.pdf`).
- [x] **32. AI Tool Disclosure:** Fully disclosed in dedicated section.

### I. Research Data Policy (Option C)
- [x] **33. Formal Data Availability Statement:** Itemized statement in manuscript and Title Page pointing to public benchmark repositories.
- [x] **34. Repository Link:** Anonymized repository link provided for review; permanent Zenodo archive committed upon publication.

### J. References (APA 7th Edition)
- [x] **35. APA 7th Author-Year In-Text Style:** Replaced numeric brackets `[5]` with `\citep{...}` and `\citet{...}` (`(Weber et al., 2019)` and `Weber et al. (2019)`). Alphabetical ordering with DOIs via `cas-model2-names.bst`.
- [x] **36. Software Citations:** PyTorch Geometric and DuckDB cited as distinct software entries.
- [x] **37. Dataset Tagging:** Benchmark datasets tagged with `[dataset]`.

### K. Final Submission Portal Checklist
- [x] **38. Corresponding Author:** Md. Nazmul (`nazmulhas36@gmail.com`) confirmed.
- [x] **39. All Figures/Tables Cited In-Text:** Every figure and table cross-referenced by `\ref{...}`.
- [x] **40. Spelling & Grammar:** Checked.
- [x] **41. Citation 1:1 Reciprocal Match:** Verified with Python: 100% of cited keys exist in `references.bib`.
- [x] **42. Copyright Permissions:** All data and tools are open-source / public domain.
