"""
scripts/embed_intuitive_visuals.py
Embeds the 7 newly generated intuitive visual figures into their respective thesis chapters:
1. ch2_literature_review.tex -> fig_lit_evolution_frontier.pdf
2. ch3_system_architecture.tex -> fig_12d_toy_model_schematic.pdf
3. ch3_system_architecture.tex -> fig_triband_waveform_spectrum.pdf
4. ch5_conformal_ethics.tex -> fig_conformal_conveyor_funnel.pdf
5. ch6_xai_agentic_sar.tex -> fig_ast_grammar_pipeline.pdf
6. ch7_experiments.tex -> fig_champion_vs_runnerup_delta.pdf
7. ch9_conclusion.tex -> fig_regulatory_shields.pdf
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
chapters_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "chapters"

def insert_before(filepath, target_str, block_to_insert, label_to_check):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if label_to_check in content:
        print(f"[-] Already embedded in {filepath.name}: {label_to_check}")
        return
    if target_str not in content:
        print(f"[!] Target string not found in {filepath.name} for {label_to_check}")
        return
    content = content.replace(target_str, block_to_insert + "\n\n" + target_str, 1)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Successfully embedded in {filepath.name}: {label_to_check}")

# 1. Chapter 2
fig2_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{figures/fig_lit_evolution_frontier.pdf}
\caption[2D Financial Crime Graph Learning Evolution Frontier]{2D financial crime graph learning evolution frontier positioning C-STGB against 18 SOTA baselines across Temporal Expressiveness (x-axis) and Imbalance, Camouflage \& Conformal Safety (y-axis). C-STGB uniquely defines the upper-right Pareto frontier.}
\label{fig:ch2_lit_evolution}
\end{figure}'''
insert_before(
    chapters_dir / "ch2_literature_review.tex",
    r"\begin{sidewaystable}[htbp]",
    fig2_tex,
    r"\label{fig:ch2_lit_evolution}"
)

# 2. Chapter 3: 12-D Toy Model
fig3_12d_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_12d_toy_model_schematic.pdf}
\caption[12-Dimensional Canonical Invariant Physical Toy-Model Schematic]{Physical toy-model and flow anatomy of the 12-dimensional canonical invariants: (a) Hydrodynamic mass-flow invariant ($\Phi_{\text{flow}}$) identifying near-zero retention pass-through conduits; (b) Marked Hawkes self-exciting point process intensity ($\lambda_u(t)$) isolating micro-burst smurfing spikes; (c) Directed causal taint exposure and reverse PageRank ($\pi_u^{\text{fwd}}, \pi_u^{\text{rev}}$); (d) Spectral Dirichlet energy preservation ($\mathcal{E}(\mathbf{H})$) preventing camouflage over-smoothing.}
\label{fig:ch3_12d_toy_schematic}
\end{figure}'''
insert_before(
    chapters_dir / "ch3_system_architecture.tex",
    r"\subsection{Mathematical Invariant Definitions}",
    fig3_12d_tex,
    r"\label{fig:ch3_12d_toy_schematic}"
)

# 3. Chapter 3: Tri-Band Waveform Spectrum
fig3_triband_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_triband_waveform_spectrum.pdf}
\caption[Tri-Band Multi-Scale Harmonic Attention Spectrum]{Tri-band continuous harmonic temporal attention spectrum: Band 1 ($2.4\text{ h}$) captures sub-second smurfing bursts; Band 2 ($24\text{ h}$) captures circadian business hours; Band 3 ($168\text{ h}$) captures 90-day dormant hibernation holding chains, resolving the temporal decay failure mode of conventional GNNs.}
\label{fig:ch3_triband_spectrum}
\end{figure}'''
insert_before(
    chapters_dir / "ch3_system_architecture.tex",
    r"\section{Module 2: Context-Aware Adaptive Edge-Trust Filter}",
    fig3_triband_tex,
    r"\label{fig:ch3_triband_spectrum}"
)

# 4. Chapter 5: Conformal Conveyor Funnel
fig5_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_conformal_conveyor_funnel.pdf}
\caption[3-Tier Conformal Risk Control Triage Conveyor Funnel]{3-tier class-conditional Conformal Risk Control (CRC) triage conveyor funnel: streaming transactions evaluate dual non-conformity quantiles ($1-\alpha \ge 99.0\%$), routing into Tier 1 (Quarantine Hold, 0.18\%), Tier 2 (Human 4-Eyes Compliance Review, 0.49\%, achieving a -99.51\% queue cut), and Tier 3 (Automated Straight-Through Clearing, 99.33\%, at 0.45\,ms latency).}
\label{fig:ch5_conformal_conveyor}
\end{figure}'''
insert_before(
    chapters_dir / "ch5_conformal_ethics.tex",
    r"\section{The 3-Tier Selective Abstention Triage Architecture}",
    fig5_tex,
    r"\label{fig:ch5_conformal_conveyor}"
)

# 5. Chapter 6: AST Grammar Pipeline
fig6_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_ast_grammar_pipeline.pdf}
\caption[AST Grammar Compiler and Anti-Hallucination SAR Pipeline]{AST grammar compiler and schema verification pipeline: multi-agent forensic reasoning text is parsed via Extended Backus-Naur Form ($\mathcal{G}_{\text{SAR}}$) recursive descent rules and validated against strict Pydantic schemas, guaranteeing a 0.00\% hallucination rate in compiled FinCEN Form 111 XML filings.}
\label{fig:ch6_ast_pipeline}
\end{figure}'''
insert_before(
    chapters_dir / "ch6_xai_agentic_sar.tex",
    r"\subsection{Extended Backus-Naur Form (EBNF) Grammar (GSAR)}",
    fig6_tex,
    r"\label{fig:ch6_ast_pipeline}"
)

# 6. Chapter 7: Champion Delta Chart
fig7_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_champion_vs_runnerup_delta.pdf}
\caption[C-STGB Benchmark Superiority and F1 Lead across 14 Networks]{C-STGB benchmark superiority across 14 financial transaction networks: (Left) Executive performance badges confirming Global Mean Rank 1.07, +21.8\% average F1 lead, -99.51\% workload cut, and 0.45\,ms Fast-Path latency; (Right) Horizontal delta bar chart illustrating decisive F1 gains over the closest published baseline per network ($p < 0.001$).}
\label{fig:ch7_champion_delta}
\end{figure}'''
insert_before(
    chapters_dir / "ch7_experiments.tex",
    r"\subsection{Comparative Analysis against Published SOTA Architectures}",
    fig7_tex,
    r"\label{fig:ch7_champion_delta}"
)

# 7. Chapter 9: Regulatory Shields
fig9_tex = r'''\begin{figure}[htbp]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig_regulatory_shields.pdf}
\caption[5-Pillar Global Regulatory Compliance Shield Infographic]{5-pillar global regulatory compliance shield infographic: formal alignment of C-STGB architectural capabilities with statutory mandates across FATF 40 Recommendations, FinCEN BSA, Federal Reserve SR 11-7 / SR 21-8, EU 6AMLD, and Bangladesh Bank BFIU MFS guidelines.}
\label{fig:ch9_regulatory_shields}
\end{figure}'''
insert_before(
    chapters_dir / "ch9_conclusion.tex",
    r"\section{Global Regulatory Compliance Matrix}",
    fig9_tex,
    r"\label{fig:ch9_regulatory_shields}"
)

print("\nEmbedding completed!")

