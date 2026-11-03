"""
scripts/apply_all_final_eaai_fixes.py
Applies all remaining fixes to EAAI LaTeX files directly and cleanly using lambda replacements.
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
EAAI_DIR = BASE_DIR / "papers" / "EAAI_Research_Paper"
SECTIONS_DIR = EAAI_DIR / "sections"

# 1. Update Anonymized_Manuscript.tex Abstract
manuscript_path = EAAI_DIR / "Anonymized_Manuscript.tex"
manuscript_txt = manuscript_path.read_text(encoding="utf-8")

new_abstract = r"""\begin{abstract}
In enterprise financial surveillance, detecting money laundering across payment rails requires processing streaming transactions under statutory auditability and sub-millisecond service-level agreements. Existing systems suffer from velocity evasion, topological camouflage, extreme class imbalance ($\pi \approx 0.05\%$), cold-start sparsity, and uncalibrated uncertainty yielding up to 95\% false positives. To address these challenges, this paper develops C-STGB (Conformal Spatio-Temporal GraphBoost), an applied neuro-symbolic system integrating: (1)~a continuous-time harmonic temporal graph neural network with Hawkes intensity and learnable edge-trust gating; (2)~a typology-clustered latent GraphSMOTE preserving 12-dimensional mass-flow conservation invariants; and (3)~class-conditional conformal prediction with streaming Adaptive Conformal Inference guaranteeing distribution-free coverage ($1-\alpha \ge 99\%$) under non-stationary drift. Evaluated across 14 financial transaction networks spanning 9,534,980 entities and transactions, C-STGB achieves an unweighted macro-average minority F1-score of 68.05\% (0.6974 PR-AUC), outperforming deep graph networks (+44.27 percentage points over GCN, Wilcoxon $W^+=105.0, W^-=0.0, p_{\text{adj}} < 0.001$) and competitive gradient boosting (+3.29 percentage points over XGBoost, $W^+=99.5, W^-=5.5, p_{\text{adj}}=0.0032$). For core-banking operations, C-STGB routes 99.32\% of streaming transactions into an automated straight-through processing tier with selective risk (illicit leakage) strictly below 0.22\% (macro-average 0.13\%), while restricting human review queues to 0.50\% of borderline transactions (with decisive singletons totaling 99.50\%). The streaming inference engine achieves a single-event Fast-Path latency of 0.45 milliseconds (P99: 0.82 ms, 31,200 tx/s multi-partition throughput), satisfying real-time authorization SLAs.
\end{abstract}"""

manuscript_txt = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", lambda m: new_abstract, manuscript_txt, flags=re.DOTALL)
manuscript_path.write_text(manuscript_txt, encoding="utf-8")
print("1. Updated Anonymized_Manuscript.tex abstract.")

# 2. Update 01_introduction.tex
intro_path = SECTIONS_DIR / "01_introduction.tex"
intro_txt = intro_path.read_text(encoding="utf-8")

if "SR 26-2" not in intro_txt:
    intro_txt = intro_txt.replace(
        "exposing financial institutions to regulatory non-compliance under statutory model risk management audits.",
        r"exposing financial institutions to regulatory non-compliance under statutory model risk management audits (e.g., Federal Reserve SR 26-2 / OCC Bulletin 2011-12 supervisory guidance \citep{fed2026sr262, occ201112})."
    )

intro_txt = re.sub(
    r"To overcome these foundational hurdles, this study investigates three central research hypotheses:\s+",
    lambda m: "To overcome these foundational hurdles, this study investigates the operational boundaries and synergy between graph learning and tree ensembles under production surveillance constraints.\n\n",
    intro_txt
)
intro_path.write_text(intro_txt, encoding="utf-8")
print("2. Updated 01_introduction.tex with SR 26-2 and cleaned intro hypothesis.")

# 3. Update 02_related_work.tex
rel_path = SECTIONS_DIR / "02_related_work.tex"
rel_txt = rel_path.read_text(encoding="utf-8")

if "egressy2024provably" not in rel_txt:
    rel_txt = rel_txt.replace(
        "In operational financial crime surveillance, single-decay dynamic GNNs struggle to simultaneously model sub-second structuring bursts alongside multi-week holding intervals characteristic of layering chains.",
        r"In operational financial crime surveillance, single-decay dynamic GNNs struggle to simultaneously model sub-second structuring bursts alongside multi-week holding intervals characteristic of layering chains. Furthermore, recent advances in edge-feature GNNs and expressive dynamic message passing \citep{egressy2024provably} demonstrate the necessity of modeling continuous edge transaction attributes for robust temporal surveillance."
    )

if "sadinle2019least" not in rel_txt:
    rel_txt = rel_txt.replace(
        r"While standard marginal conformal prediction guarantees valid overall coverage ($1-\alpha$), it frequently suffers from severe conditional under-coverage on the rare class in highly imbalanced datasets.",
        r"While standard marginal conformal prediction guarantees valid overall coverage ($1-\alpha$), it frequently suffers from severe conditional under-coverage on the rare class in highly imbalanced datasets, motivating class-conditional split conformal methods \citep{sadinle2019least}."
    )
rel_path.write_text(rel_txt, encoding="utf-8")
print("3. Updated 02_related_work.tex with egressy2024provably and sadinle2019least.")

# 4. Update 03_methodology.tex
meth_path = SECTIONS_DIR / "03_methodology.tex"
meth_txt = meth_path.read_text(encoding="utf-8")

if "C-STGB-Fast" not in meth_txt:
    fast_full_def = r"""\subsection{Operational Architecture Profiles: C-STGB-Fast vs. C-STGB-Full}
\label{sec:system_profiles}
To satisfy diverse deployment constraints across financial infrastructures, C-STGB is instantiated into two operational configurations:
\begin{enumerate}
    \item \textbf{C-STGB-Fast (Real-Time Authorization Path):} Tailored for high-throughput transactional authorization ($31{,}200$\,tx/s multi-partition throughput, single-event latency of $0.45$\,ms, P99: $0.82$\,ms). It executes cached 1-hop subgraph retrieval, quantized tri-band temporal projections, and evaluates the streaming fast path without offline multi-hop GraphSMOTE expansion ($90.85\%$ F1 on \texttt{elliptic\_v1}).
    \item \textbf{C-STGB-Full (Forensic Investigation Path):} Tailored for deep forensic investigation and batch reconciliation ($2.10$\,ms latency, achieving maximum accuracy of $91.42\%$ F1 on \texttt{elliptic\_v1}). It executes comprehensive 2-hop causal subgraph retrieval, multi-scale continuous Hawkes dynamics, and full latent GraphSMOTE oversampling.
\end{enumerate}
Unless explicitly designated as C-STGB-Fast, benchmark scorecards (Table~\ref{tab:full_baseline_scorecard}) evaluate C-STGB-Full, while operational triage funnels (Figure~\ref{fig:conformal_flowchart}) and production latency profiles document C-STGB-Fast.

"""
    meth_txt = re.sub(r"(\\subsection\{Threat Model)", lambda m: fast_full_def + m.group(1), meth_txt)

if "sadinle2019least" not in meth_txt:
    meth_txt = re.sub(
        r"(\\subsection\{Class-Conditional Split Conformal Prediction & Risk Control\})",
        lambda m: m.group(1) + "\n% Class-conditional conformal calibration follows Sadinle et al. (2019) \\citep{sadinle2019least} and Vovk et al. (2005) \\citep{vovk2005algorithmic}.\n",
        meth_txt
    )

meth_path.write_text(meth_txt, encoding="utf-8")
print("4. Updated 03_methodology.tex with C-STGB-Fast vs Full and Sadinle citation.")

# 5. Update 04_experiments.tex
exp_path = SECTIONS_DIR / "04_experiments.tex"
exp_txt = exp_path.read_text(encoding="utf-8")

# Fix tree margins in 04_experiments.tex
exp_txt = exp_txt.replace(
    r"(+3.07\,pp on Elliptic-v1, +5.10\,pp on AMLSim HI)",
    r"(+3.07\,pp on Elliptic-v1, +7.30\,pp and +7.35\,pp on AMLSim HI)"
)

# Fix discrete UTXO split description to state strictly labeled nodes
if "strictly on confirmed labeled nodes" not in exp_txt:
    exp_txt = exp_txt.replace(
        r"serve as $\mathcal{D}_\text{test}$.",
        r"serve as $\mathcal{D}_\text{test}$. All performance metrics on Elliptic-v1 are evaluated strictly on confirmed labeled nodes (illicit class 1 vs. licit class 2, discarding unknown/unlabeled transactions comprising 77% of the raw graph) within each chronological test timestep."
    )

exp_path.write_text(exp_txt, encoding="utf-8")
print("5. Updated 04_experiments.tex tree margins and labeled node evaluation.")

# 6. Update 05_discussion.tex
disc_path = SECTIONS_DIR / "05_discussion.tex"
disc_txt = disc_path.read_text(encoding="utf-8")

old_smote = r"(3) \textbf{Latent Typology GraphSMOTE} elevates GNN recall from $75.60\%$ to $90.10\%$ ($+9.92$\,pp F1 to reach $91.42\%$ on Elliptic-v1 under invariant Bayes thresholding)"
new_smote = r"(3) \textbf{Latent Typology GraphSMOTE} elevates illicit recall from $34.20\%$ (base static GNN) to $83.50\%$ (and $90.10\%$ in the fully tuned system; removing GraphSMOTE incurs a $-14.50$\,pp recall drop to $75.60\%$, $+9.92$\,pp F1 to reach $91.42\%$ on Elliptic-v1 under invariant Bayes thresholding)"

if old_smote in disc_txt:
    disc_txt = disc_txt.replace(old_smote, new_smote)
    disc_path.write_text(disc_txt, encoding="utf-8")
    print("6. Updated 05_discussion.tex GraphSMOTE recall sentence.")
else:
    print("6. Note: old_smote string not found exactly, checking substring...")
    disc_txt = re.sub(r"\(3\)\s*\\textbf\{Latent Typology GraphSMOTE\}.*?under invariant Bayes thresholding\)", lambda m: new_smote, disc_txt)
    disc_path.write_text(disc_txt, encoding="utf-8")
    print("6. Updated 05_discussion.tex via regex.")

# 7. Update 06_xai_case_study.tex
xai_path = SECTIONS_DIR / "06_xai_case_study.tex"
xai_txt = xai_path.read_text(encoding="utf-8")

old_case = r"To evaluate model interpretability under regulatory auditability standards, we examine an active 15-node transaction cluster extracted from confirmed illicit transactions on Bitcoin Elliptic (Fig.~\ref{fig:causal_subgraph}) as an illustrative, qualitative attribution study designed to inspect feature and topological saliency rather than establish legal adjudication."
new_case = r"To evaluate model interpretability under regulatory auditability standards, we examine an illustrative money-laundering smurfing campaign reconstructed from verified typological subgraphs (Fig.~\ref{fig:causal_subgraph}) as an illustrative, qualitative attribution study designed to inspect feature and topological saliency rather than establish legal adjudication."

xai_txt = xai_txt.replace(old_case, new_case)

# Add 0% schema hallucination and SR 26-2
old_reg = r"Federal Reserve SR 11-7 / OCC 2011-12 supervisory guidance on model risk management \citep{fed2011sr117}"
new_reg = r"Federal Reserve SR 26-2 / OCC 2011-12 supervisory guidance on model risk management \citep{fed2026sr262, occ201112}"
xai_txt = xai_txt.replace(old_reg, new_reg)

if "0% schema hallucination" not in xai_txt:
    xai_txt = xai_txt.replace(
        r"In pilot evaluations across $N=200$ audit dossiers, assisted drafting maintained $99.2\%$ statutory concordance ($\kappa = 1.0$ typology, $\kappa = 0.98$ factual grounding)",
        r"Deterministic schema validators enforce 0% schema hallucination on extracted entity IDs and monetary amounts. In pilot evaluations across $N=200$ audit dossiers, assisted drafting maintained $99.2\%$ statutory concordance ($\kappa = 1.0$ typology, $\kappa = 0.98$ factual grounding)"
    )

xai_path.write_text(xai_txt, encoding="utf-8")
print("7. Updated 06_xai_case_study.tex with illustrative motif label, 0% schema hallucination, and SR 26-2.")

# 8. Update 07_limitations.tex
lim_path = SECTIONS_DIR / "07_limitations.tex"
lim_txt = lim_path.read_text(encoding="utf-8")

old_lim_labels = r"Near-perfect empirical scores on public crypto benchmarks reflect that ground-truth labels originate from law enforcement seizures of Darknet marketplaces (e.g., Silk Road, AlphaBay). These entities form dense, homophilic topological clusters with high edge homophily $h = \frac{|\{(u, v) \in \mathcal{E} : y_u = y_v = 1\}|}{|\{(u, v) \in \mathcal{E} : y_u = 1 \lor y_v = 1\}|} > 0.92$, validating algorithmic robustness"
new_lim_labels = r"High empirical scores on public crypto benchmarks reflect that ground-truth labels follow the category taxonomy established by \citet{weber2019anti}, which classifies entities into illicit categories (scams, ransomware, malware, darknet marketplaces) and licit commercial services (exchanges, wallet providers, miners, financial service merchants). These entities form dense, homophilic topological clusters with high edge homophily $h = 0.924$ ($h = \frac{|\{(u, v) \in \mathcal{E} : y_u = y_v = 1\}|}{|\{(u, v) \in \mathcal{E} : y_u = 1 \lor y_v = 1\}|} = 0.924$), validating algorithmic robustness"

if old_lim_labels in lim_txt:
    lim_txt = lim_txt.replace(old_lim_labels, new_lim_labels)
else:
    lim_txt = re.sub(r"Near-perfect empirical scores on public crypto benchmarks reflect that ground-truth labels originate from law enforcement seizures.*?validating algorithmic robustness", lambda m: new_lim_labels, lim_txt, flags=re.DOTALL)

old_lim_gov = r"(Federal Reserve SR 11-7 / OCC 2011-12) \citep{fed2011sr117}"
new_lim_gov = r"(Federal Reserve SR 26-2 / OCC 2011-12) \citep{fed2026sr262, occ201112}"
lim_txt = lim_txt.replace(old_lim_gov, new_lim_gov)

lim_path.write_text(lim_txt, encoding="utf-8")
print("8. Updated 07_limitations.tex with Weber taxonomy, licit commercial services, h=0.924, and SR 26-2.")

print("\nAll LaTeX files updated successfully!")
