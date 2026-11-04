"""
scripts/patch_thesis.py
Automates visual, structural, and typographical enhancements across all thesis chapters:
1. Injects Chapter Executive Takeaway boxes (\begin{takeawaybox}) for Chapters 1-9.
2. Injects short titles [Short Title] into all \caption{...} instances to compress LoF and LoT.
3. Injects visual figures into Chapter 2 (Adversarial Camouflage) and Chapter 8 (K8s Architecture).
"""

import os
import re

THESIS_DIR = r"papers\University_CSE_Thesis"
CHAPTERS_DIR = os.path.join(THESIS_DIR, "chapters")

# -----------------------------------------------------------------------------
# 1. Takeaway Boxes per Chapter
# -----------------------------------------------------------------------------
TAKEAWAYS = {
    "ch1_introduction.tex": r'''\begin{takeawaybox}{Chapter 1: Key Contributions \& Defense Highlights}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{The Global Challenge:} Transnational financial crime launders \$800B--\$2T annually (2\%--5\% of global GDP), while legacy static rule engines trigger crippling $>98\%$ false positive rates.
  \item \textbf{Theoretical Failure Modes:} Identifies the five structural failure modes of standard GNNs: long-dwell hibernation evasion, adversarial camouflage, extreme class imbalance ($<0.05\%$), topological cold-start blindness, and uncalibrated black-box alert flooding.
  \item \textbf{Proposed Solution (C-STGB):} Introduces Conformal Spatio-Temporal GraphBoost, uniting continuous harmonic temporal attention, context-aware edge-trust gating, latent GraphSMOTE, canonical physical mass-flow invariants, and distribution-free conformal risk control.
  \item \textbf{Empirical Milestones:} 91.42\% F1 on Elliptic-v1, 99.10\% on Elliptic-v2, 0.45\,ms Fast-Path P99 latency, and a 99.51\% reduction in human analyst compliance queues.
\end{itemize}
\end{takeawaybox}
''',

    "ch2_literature_review.tex": r'''\begin{takeawaybox}{Chapter 2: Theoretical Foundations \& Literature Taxonomy}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Methodological Taxonomy:} Synthesizes 25 foundational publications across tabular gradient boosters, spatial GNNs, continuous dynamic GNNs, and adversarial camouflage filters.
  \item \textbf{Theoretical Expressiveness Bounds:} Analyzes Weisfeiler-Lehman (1-WL) graph expressiveness, Dirichlet energy over-smoothing under commercial merchant hubs, and marked Hawkes self-exciting point processes.
  \item \textbf{Distribution-Free Uncertainty:} Formalizes split conformal prediction and class-conditional non-conformity quantiles under non-stationary distribution drift.
  \item \textbf{Architectural Voids Resolved:} Identifies why no single existing framework simultaneously resolves multi-scale temporal decay, topological camouflage, extreme class imbalance, and strict regulatory auditability.
\end{itemize}
\end{takeawaybox}
''',

    "ch3_system_architecture.tex": r'''\begin{takeawaybox}{Chapter 3: Architectural Innovations \& Mathematical Formulations}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{12-D Canonical Invariants ($\mathbf{z}_{\text{inv}}$):} Formulates physical mass-flow conservation ($\Phi_{\text{flow}}$), marked Hawkes burst rates ($\lambda_u$), pass-through layering ratios, and directed taint exposure.
  \item \textbf{Tri-Band Temporal Attention Kernel:} Synthesizes multi-scale exponential decay spanning burst ($\tau_1=2.4\text{h}$), operational ($\tau_2=24\text{h}$), and dormancy ($\tau_3=168\text{h}$) regimes with continuous Fourier encodings.
  \item \textbf{Context-Aware Edge Gating:} Learnable MLP filter $\hat{g}_{ij} \ge \delta_{\text{floor}}$ prunes 65.9\% of spurious merchant camouflage noise prior to message passing.
  \item \textbf{Typology GraphSMOTE:} Discovers latent topological clusters via GMM and generates synthetic illicit nodes with localized bilinear edge synthesis preserving mass conservation.
  \item \textbf{Evidence-Adaptive Fusion:} Gating scalar $\alpha_u$ dynamically balances graph structural signals against tabular invariants, achieving 89.60\% F1 on zero-degree cold-start nodes.
\end{itemize}
\end{takeawaybox}
''',

    "ch4_data_pipeline.tex": r'''\begin{takeawaybox}{Chapter 4: Vectorized Streaming Systems \& Data Engineering}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Embedded Analytical Kernel:} DuckDB embedded relational OLAP engine executes zero-lookahead time-causal ego-graph analytical queries in $0.11\,\text{ms}$.
  \item \textbf{Zero-Copy Memory Management:} Apache Arrow columnar IPC streaming eliminates serialization overhead between streaming ingestion and PyTorch tensor buffers.
  \item \textbf{Causal Index Architecture:} Composite $(u, t_{\text{timestamp}})$ and $(v, t_{\text{timestamp}})$ indexing strictly enforces causal non-leakage ($t_e \le t_{\text{eval}}$).
  \item \textbf{LRU Ego-Graph Caching:} In-memory 2-hop topological cache achieves an 88.4\% hit rate, serving single-entity subgraphs in $0.18\,\text{ms}$.
\end{itemize}
\end{takeawaybox}
''',

    "ch5_conformal_ethics.tex": r'''\begin{takeawaybox}{Chapter 5: Conformal Risk Control \& Statutory Compliance}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Finite-Sample Risk Guarantees:} Class-Conditional Conformal Risk Control (CRC) guarantees minority class coverage $\mathbb{P}(Y \in \Gamma(X) \mid Y=1) \ge 1 - \alpha$ without distributional assumptions.
  \item \textbf{DKW TV-Drift Bound:} Formulates Dvoretzky-Kiefer-Wolfowitz coverage bounds under non-stationary total variation temporal drift.
  \item \textbf{3-Tier Operational Triage:} Routes streams into Tier 1 (Quarantine Hold, 0.18\%), Tier 2 (Human Four-Eyes Review Desk, 0.49\%), and Tier 3 (Automated Straight-Through Clear, 99.33\%).
  \item \textbf{Queue Compression \& Fairness:} Cuts manual compliance queues by 99.51\% while maintaining zero demographic parity disparity ($\Delta \le 0.008$) across customer tiers.
\end{itemize}
\end{takeawaybox}
''',

    "ch6_xai_agentic_sar.tex": r'''\begin{takeawaybox}{Chapter 6: Explainable AI \& Multi-Agent Forensic Swarms}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Mutual Information Attribution:} GNNExplainer extracts compact, connected subgraphs maximizing mutual information with model risk predictions.
  \item \textbf{Multi-Agent Swarm:} Coordinates four specialized forensic roles: Invariant Analyst, Typology Profiler, Compliance Officer, and Statutory Auditor.
  \item \textbf{Deterministic Anti-Hallucination:} AST grammar compiler enforces strict Extended Backus-Naur Form ($\mathcal{G}_{\text{SAR}}$) and Pydantic schemas over LLM outputs with 0.00\% hallucination rate.
  \item \textbf{Cryptographic Merkle Receipts:} Every SAR filing is anchored to a SHA-256 Merkle root stored in a WORM-compliant audit ledger meeting Federal Reserve SR 11-7 / SR 21-8 standards.
\end{itemize}
\end{takeawaybox}
''',

    "ch7_experiments.tex": r'''\begin{takeawaybox}{Chapter 7: Master Benchmark Campaigns \& Empirical Verification}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Master Benchmark Suite:} 14 financial transaction networks, 9,534,980 entities, 9,528,355 transactions, and 13 published baselines across public crypto and commercial banking rails.
  \item \textbf{SOTA Superiority:} Achieves 91.42\% F1 on Elliptic-v1, 99.10\% on Elliptic-v2, and 68.05\% macro F1 globally ($p < 0.001$ via Wilcoxon signed-rank tests with Holm-Bonferroni correction).
  \item \textbf{Factorial Ablations:} Stepwise progression and leave-one-out ablations isolate the precise marginal gain of each module, with GraphSMOTE and Edge-Gating contributing $+32.1\%$ and $+18.4\%$ F1.
  \item \textbf{Camouflage \& Cold-Start Robustness:} Retains 86.4\% F1 under 50\% injected camouflage links; evidence-adaptive fusion yields 89.60\% F1 on zero-degree cold-start entities.
  \item \textbf{Production SLAs:} Delivers 0.45\,ms Fast-Path P99 latency and 31,200 tx/sec throughput, meeting Tier-1 core-banking clearance requirements.
\end{itemize}
\end{takeawaybox}
''',

    "ch8_software_engineering.tex": r'''\begin{takeawaybox}{Chapter 8: Enterprise Architecture \& Production Engineering}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Asynchronous Serving Tier:} FastAPI / Uvicorn asynchronous streaming endpoints supporting ISO 20022 webhooks with sub-millisecond response SLAs.
  \item \textbf{Cloud-Native Orchestration:} Multi-stage Docker containerization and Kubernetes manifests with Horizontal Pod Autoscaling (HPA) from 4 to 32 worker replicas.
  \item \textbf{Production Telemetry:} Prometheus metrics tracking P50/P90/P99 latency, conformal triage distributions, edge-pruning ratios, and streaming drift statistics.
  \item \textbf{Verification Suite:} 158 automated unit, integration, and regression tests achieving 100\% pass verification across 25 dedicated test modules.
\end{itemize}
\end{takeawaybox}
''',

    "ch9_conclusion.tex": r'''\begin{takeawaybox}{Chapter 9: Synthesis, Limitations \& Enterprise Roadmap}
\begin{itemize}\setlength{\itemsep}{1pt}
  \item \textbf{Scientific Synthesis:} Establishes C-STGB as the first mathematically guaranteed, real-time, explainable graph learning system for high-velocity financial crime surveillance.
  \item \textbf{26-Week Deployment Roadmap:} Details a phased production integration for Tier-1 banks (Shadow Ingestion $\rightarrow$ Dual-Run Conformal Pilot $\rightarrow$ Straight-Through Autonomous Surveillance).
  \item \textbf{Threats to Validity:} Methodically documents five structural boundaries: cross-institutional banking gaps, unobserved dark liquidity, cross-chain bridging, cold-start latency, and adversarial adaptation.
  \item \textbf{Open Science:} Fully reproducible codebase with open-source benchmarks, container recipes, and pre-trained model weights.
\end{itemize}
\end{takeawaybox}
'''
}

# -----------------------------------------------------------------------------
# 2. Short Captions Mapping (Target prefix -> Short Title)
# -----------------------------------------------------------------------------
SHORT_CAPTIONS = {
    # Chapter 1
    "Topological contrast between legitimate commercial": "Topological Contrast Between Legitimate Flows and Smurfing Syndicates",
    "Operational architecture and real-time triage dataflow": "C-STGB Operational Architecture and Real-Time Conformal Triage Dataflow",

    # Chapter 2
    "Comprehensive 25-Paper Comparative Taxonomy in Financial Forensics": "Comprehensive 25-Paper Financial Forensics & Graph ML Taxonomy",

    # Chapter 3
    "Reader's Architectural Roadmap: Mapping Operational AML Bottlenecks": "Mapping Operational AML Bottlenecks to C-STGB Innovations",
    "Summary of Universal Mathematical Notations, Tensor Dimensions": "Summary of Universal Mathematical Notations and Tensor Shapes",
    "End-to-End Architectural Dataflow of C-STGB v2": "End-to-End Architectural Dataflow of C-STGB",
    "Universal 12-dimensional canonical invariant representation space": "Universal 12-Dimensional Canonical Invariant Space",
    "Compact Formal Specification of the 12-Dimensional Canonical": "Formal Specification of the 12-Dimensional Canonical Invariants",
    "Multi-scale tri-band continuous harmonic temporal attention": "Tri-Band Continuous Harmonic Temporal Decay Comparison",
    "Three-step Typology-Clustered Latent GraphSMOTE synthesis": "Three-Step Typology-Clustered Latent GraphSMOTE Pipeline",
    "C-STGB Unified Multi-Stage Training Pipeline": "C-STGB Unified Multi-Stage Training Pipeline",
    "Streaming Online Inference & Risk-Controlled Selective Triage": "Streaming Online Inference and Selective Triage",
    "Dual-lane execution lifecycle of C-STGB: Lane 1": "C-STGB Dual-Lane Execution Lifecycle: Training and Inference",
    "Empirical separability distributions of the 12 canonical physical": "Empirical Separability Distributions of Canonical Invariants",
    "Evidence-adaptive gating dynamics $\\alpha_u": "Evidence-Adaptive Gating and Spectral Cold-Start Convergence",

    # Chapter 4
    "Vectorized streaming data engineering architecture, illustrating zero-copy": "Vectorized Streaming Data Engineering Architecture",
    "Relational Database Schema (ERD), time-causal composite indexing": "Relational Database Schema and Causal Index Architecture",
    "Dynamic Heterogeneous Schema Discovery and Canonical Invariant Mapping": "Dynamic Heterogeneous Schema Discovery and Invariant Mapping",

    # Chapter 5
    "Operational workflow. Phases~1--2: LRU subgraph cache": "Fast-Path Latency Workflow and Selective Triage",
    "Class-conditional conformal calibration mechanism under extreme class": "Class-Conditional Conformal Calibration Mechanism",
    "Empirical verification of 3-Tier Conformal Risk Control": "Empirical Verification of 3-Tier Conformal Risk Control",
    "Comparative Evaluation of Conformal Risk Control against Calibration": "Comparative Evaluation of Conformal Risk Control Baselines",
    "Operational compliance triage funnel: comparative workload reduction": "Operational Compliance Triage Funnel and Workload Reduction",

    # Chapter 6
    "Multi-agent forensic reasoning and dual-governance pipeline": "Multi-Agent Forensic Reasoning and Dual-Governance Pipeline",
    "Operational Cost, Token Budget, and Latency Comparison: Multi-Agent": "Operational Cost, Token Budget, and Latency: Swarm vs. Manual",
    "Worked 3-stage forensic progression of a 15-node smurfing": "Worked 3-Stage Forensic Progression of a 15-Node Incident",
    "Chronological forensic timeline of the 15-node incident": "Chronological Forensic Timeline of the 15-Node Laundering Case",

    # Chapter 7
    "Comprehensive Structural Profiles and Extreme Class Skew": "Comprehensive Structural Profiles across 14 Financial Networks",
    "Extreme class skew distribution (Illicit Ratio $\\pi$, $\\log_{10}$ scale)": "Extreme Class Skew Distribution across 14 Benchmarks",
    "Dataset Provenance, Open Academic Licenses, and Permanent": "Dataset Provenance and Open Academic Licenses",
    "Comprehensive Compute Budget, Hardware Specifications, and Environmental": "Comprehensive Compute Budget and Hardware Specifications",
    "Zero-leakage 4-way chronological dataset partitioning timeline": "Zero-Leakage 4-Way Chronological Dataset Split Timeline",
    "Comparative Performance on Elliptic-v1 against Reported Literature": "Comparative Performance on Elliptic-v1 vs. Literature Baselines",
    "Overall Benchmark Performance Summary and Mean Rank across All 14": "Overall Performance Summary and Mean Rank across 14 Networks",
    "Grouped Performance Matrix: Public Crypto Ledgers vs.": "Grouped Performance Matrix: Crypto Ledgers vs. Multi-Bank Rails",
    "Statistical significance and archetype-level performance synthesis": "Statistical Significance and Archetype Performance Synthesis",
    "Multi-criteria radar benchmark contrasting C-STGB against competitive": "Multi-Criteria Radar Benchmark contrasting C-STGB vs. Baselines",
    "Comparative Precision-Recall (PR) and Receiver Operating Characteristic": "Comparative PR and ROC Frontiers on Elliptic-v1",
    "Cumulative Stepwise Architectural Ablation Progression across Three": "Cumulative Stepwise Architectural Ablation Progression",
    "Stepwise architectural ablation progression across Elliptic-v1": "Stepwise Architectural Ablation across Three Benchmark Datasets",
    "Stepwise cumulative ablation waterfall progression, quantifying": "Stepwise Cumulative Ablation Waterfall Progression",
    "Leave-One-Out Component Removal Ablation on Elliptic-v1": "Leave-One-Out Component Removal Ablation on Elliptic-v1",
    "Leave-one-out component ablation impact on Elliptic-v1": "Leave-One-Out Component Ablation Impact Waterfall",
    "Leave-One-Feature-Out Sensitivity Analysis on 12-D Invariants": "Leave-One-Feature-Out Sensitivity Analysis on 12-D Invariants",
    "Factorial importance tornado ranking of the 12 canonical invariants": "Factorial Importance Tornado Ranking of 12-D Invariants",
    "Class-Conditional Conformal Risk Control (CRC) Triage Performance": "Class-Conditional Conformal Risk Control Performance",
    "Adversarial Topological Robustness and Relative F1-Score Retention": "Adversarial Topological Robustness under Camouflage Attacks",
    "Adversarial camouflage link robustness on Elliptic-v1": "Adversarial Camouflage Link Robustness on Elliptic-v1",
    "Empirical distribution of learnable edge-trust gating weights": "Empirical Distribution of Learnable Edge-Trust Gating Weights",
    "t-SNE latent manifold visualization: (a) Baseline GNN": "t-SNE Latent Manifold Visualization: Baseline vs. C-STGB",
    "Zero-shot cross-domain generalization under completely frozen neural": "Zero-Shot Cross-Domain Generalization on Frozen Weights",
    "Expanded 8-Pair Zero-Shot Cross-Domain Transfer Matrix": "Expanded 8-Pair Zero-Shot Cross-Domain Transfer Matrix",
    "Empirical streaming latency distribution (P50, P90, P99) for Fast-Path": "Empirical Streaming Latency Distribution for Fast-Path Inference",
    "Comparative latency profile contrasting C-STGB Fast-Path cached": "Comparative Latency Profile: Fast-Path vs. SOTA Dynamic GNNs",
    "Compute Hardware Specifications, Training Wall-Clock Times": "Hardware Specifications, Training Times, and Streaming Latency",
    "Comprehensive 14-dataset small-multiples Precision-Recall (PR) curves": "Comprehensive 14-Dataset Precision-Recall Curves",

    # Chapter 8
    "System architecture of Intelligent-AML. Payment rails stream": "System Architecture of Intelligent-AML Production Serving",
    "Enterprise RESTful and WebSocket API Endpoint Specifications": "Enterprise RESTful and WebSocket API Endpoint Specifications",
    "Real-Time Operational UML Sequence Lifeline diagram detailing": "Real-Time Operational UML Sequence Lifeline",
    "Algorithmic Complexity, Single-Event Latency, and Memory Footprint": "Algorithmic Complexity, Latency, and Memory Footprint",

    # Chapter 9
    "26-Week Enterprise Integration Roadmap for Tier-1 Banking": "26-Week Enterprise Integration Roadmap for Tier-1 Banking",
    "Global Regulatory Compliance Matrix across Major Statutory Frameworks": "Global Regulatory Compliance Matrix across Statutory Frameworks",
    "Systematic Taxonomy of Architectural Limitations, Operational Threats": "Systematic Taxonomy of Architectural Limitations and Mitigations",
    "Consolidated Methodological Threats to Validity and Architectural": "Consolidated Methodological Threats to Validity and Mitigations",

    # Chapter 10 (Appendices)
    "Comprehensive Cross-Disciplinary Glossary of Financial Crime": "Cross-Disciplinary Financial Crime and Graph ML Glossary",
    "Comprehensive Ingestion Schema Mappings across All 14 Evaluated": "Universal Ingestion Schema Mappings across 14 Financial Networks",
    "Comprehensive Open-Science Empirical Reproducibility Checklist": "Open-Science Empirical Reproducibility Checklist",
    "Four-panel hyperparameter sensitivity analysis of the C-STGB": "Four-Panel Hyperparameter Sensitivity Analysis",
    "Hyperparameter Search Space and Best Configurations for C-STGB": "Hyperparameter Search Space and Optimal Configurations",
    "Comprehensive Multi-Baseline Performance Matrix across All 14": "Comprehensive Multi-Baseline Benchmark Matrix across 14 Networks",
    "Real-Time Surveillance Desk and Alert Triage Queue, displaying": "Real-Time Surveillance Desk and Live Alert Triage Queue Console",
    "3D Multi-Hop Counterparty Forensic Graph Studio (Three.js WebGL": "3D Multi-Hop Counterparty Forensic Graph Studio Console",
    "Autonomous Multi-Agent Case Management Desk, illustrating autonomous": "Autonomous Multi-Agent Case Management Desk Console",
    "Tier-2 Epistemic Uncertainty Four-Eyes Adjudication Console": "Tier-2 Epistemic Uncertainty Four-Eyes Adjudication Console",
    "Multi-Agent SAR Narrative Generation Console: displaying real-time": "Multi-Agent SAR Narrative Generation Console",
    "Model Governance and Drift Monitoring Console: real-time streaming": "Model Governance and Drift Monitoring Console",
    "End-to-end operator investigation lifecycle enforced by the Intelligent": "End-to-End Enterprise Operator Investigation Lifecycle"
}

def patch_chapter(fname):
    fpath = os.path.join(CHAPTERS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject takeaway box if present
    if fname in TAKEAWAYS:
        box = TAKEAWAYS[fname]
        if "\\begin{takeawaybox}" not in content:
            # find chapter label
            m = re.search(r"(\\chapter\{[^\}]+\}\s*\\label\{[^\}]+\})", content)
            if m:
                target = m.group(1)
                replacement = target + "\n\n" + box
                content = content.replace(target, replacement, 1)
                print(f"  [+] Injected takeawaybox in {fname}")
            else:
                print(f"  [!] Warning: chapter label not found in {fname}")

    # 2. Inject short captions
    for prefix, short_title in SHORT_CAPTIONS.items():
        # Match \caption{prefix...
        pattern = r"\\caption\{(" + re.escape(prefix) + r"[^\}]*)\}"
        # We need balanced braces replacement or re.sub
        # Since regex [^\}]* stops at first }, let's find instances where \caption{ appears without [
        pos = 0
        while True:
            idx = content.find(r"\caption{", pos)
            if idx == -1:
                break
            # check if starts with prefix
            sub = content[idx+9:idx+9+len(prefix)+20]
            if prefix in sub:
                # Find matching brace for \caption{
                depth = 0
                end_idx = idx + 8
                for i in range(idx + 8, len(content)):
                    if content[i] == '{':
                        depth += 1
                    elif content[i] == '}':
                        depth -= 1
                        if depth == 0:
                            end_idx = i
                            break
                orig_caption = content[idx:end_idx+1]
                # Replace with \caption[short_title]{orig_text}
                caption_body = content[idx+9:end_idx]
                new_caption = f"\\caption[{short_title}]{{{caption_body}}}"
                content = content[:idx] + new_caption + content[end_idx+1:]
                print(f"  [+] Injected short caption: [{short_title}]")
                pos = idx + len(new_caption)
            else:
                pos = idx + 9

    # 3. Chapter-specific additions
    if fname == "ch2_literature_review.tex":
        # Add Figure 2.1 under section 2.5
        sec_marker = r"\subsection{Adversarial Camouflage and Robust Fraud Detection}"
        fig2_code = r'''\subsection{Adversarial Camouflage and Robust Fraud Detection}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{figures/fig21_adversarial_camouflage_topology.pdf}
\caption[Adversarial Camouflage Topology and Edge-Trust Filter Pruning]{Topological impact of adversarial camouflage and edge-trust pruning in financial networks: (a) Raw camouflaged transaction graph where an illicit laundering cycle (C4) deliberately injects over 50 spurious edges to high-degree legitimate merchant hubs to induce feature over-smoothing; (b) C-STGB context-aware edge-trust gating ($\hat{g}_{ij} \ge 0.92$), successfully filtering out 65.9\% of adversarial camouflage chaff to isolate the true laundering wash cycle.}
\label{fig:ch2_camouflage_topology}
\end{figure}
'''
        if "\\label{fig:ch2_camouflage_topology}" not in content:
            if sec_marker in content:
                content = content.replace(sec_marker, fig2_code, 1)
                print("  [+] Added Figure 2.1 to Chapter 2")

    if fname == "ch8_software_engineering.tex":
        # Add Figure 8.2 under Section 8.4 Containerization
        sec_marker = r"\subsection{Containerization \& Cloud-Native Orchestration Strategy}"
        fig8_code = r'''\subsection{Containerization \& Cloud-Native Orchestration Strategy}

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/fig8_1_fastapi_k8s_topology.pdf}
\caption[Enterprise Cloud-Native Deployment Topology and Kubernetes Orchestration]{Enterprise cloud-native deployment topology of C-STGB: mTLS 1.3 ingress API Gateway, containerized FastAPI scoring workers orchestrated with Kubernetes Horizontal Pod Autoscaling (HPA), zero-copy Apache Arrow shared memory buffers, DuckDB embedded analytics, and WORM-vault tamper-proof Merkle audit ledger.}
\label{fig:ch8_k8s_topology}
\end{figure}
'''
        if "\\label{fig:ch8_k8s_topology}" not in content:
            if sec_marker in content:
                content = content.replace(sec_marker, fig8_code, 1)
                print("  [+] Added Figure 8.2 to Chapter 8")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Done processing {fname}\n")

if __name__ == "__main__":
    for fname in sorted(os.listdir(CHAPTERS_DIR)):
        if fname.endswith(".tex"):
            print(f"Processing {fname}...")
            patch_chapter(fname)
    print("All chapters successfully patched!")
