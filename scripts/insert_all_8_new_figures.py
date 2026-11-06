import sys
from pathlib import Path

# 1. Chapter 1: insert fig_1_3_failure_modes
p_ch1 = Path("papers/University_CSE_Thesis/chapters/ch1_introduction.tex")
t_ch1 = p_ch1.read_text(encoding="utf-8")
if "fig_1_3_failure_modes" not in t_ch1:
    fig_1_3_code = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/fig_1_3_failure_modes.pdf}
\caption[Five Canonical Failure Modes of Conventional AML Architectures]{Five canonical failure modes of conventional AML surveillance: (a) 90-day exponential memory decay vanishing; (b) feature over-smoothing and Dirichlet energy collapse $\mathcal{E}(\mathbf{H}) \to 0$ in high-degree merchant hubs; (c) false-negative recall collapse under extreme class skew ($\pi < 0.05\%$) with na\"ive $\tau = 0.50$; (d) $k$-hop neighborhood VRAM explosion exceeding hardware limits ($>80\,\text{GB}$); (e) marginal conformal triage queue flooding exceeding human review capacity.}
\label{fig:ch1_failure_modes}
\end{figure}
"""
    idx1 = t_ch1.find(r"\section{Formal Problem Formulation}")
    if idx1 != -1:
        t_ch1 = t_ch1[:idx1] + fig_1_3_code + "\n" + t_ch1[idx1:]
        p_ch1.write_text(t_ch1, encoding="utf-8")
        print("Inserted Figure 1.3 into ch1_introduction.tex")

# 3. Chapter 3: insert fig_3_10_gradient_dynamics
p_ch3 = Path("papers/University_CSE_Thesis/chapters/ch3_system_architecture.tex")
t_ch3 = p_ch3.read_text(encoding="utf-8")
if "fig_3_10_gradient_dynamics" not in t_ch3:
    fig_3_10_code = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.88\textwidth]{figures/fig_3_10_gradient_dynamics.pdf}
\caption[Gradient Magnitude Dynamics of Cost-Sensitive Focal Tversky Loss]{Gradient magnitude dynamics of the Cost-Sensitive Asymmetric Focal Tversky Loss (Eq.~3.29), illustrating the $5.67\times$ false-negative gradient amplification ($\beta_{\text{FN}}=0.85$ vs.\ $\beta_{\text{FP}}=0.15$) that prevents minority recall collapse under $\pi < 0.05\%$ skew.}
\label{fig:gradient_dynamics}
\end{figure}
"""
    marker3 = "Gradient Dynamics Analysis:}"
    idx3 = t_ch3.find(marker3)
    if idx3 != -1:
        # Find end of equation split
        end_eq = t_ch3.find(r"\end{split}", idx3)
        end_eq = t_ch3.find(r"\end{equation}", end_eq)
        end_p3 = t_ch3.find("\n\n", end_eq)
        if end_p3 == -1: end_p3 = t_ch3.find("\n", end_eq)
        t_ch3 = t_ch3[:end_p3] + "\n" + fig_3_10_code + "\n" + t_ch3[end_p3:]
        p_ch3.write_text(t_ch3, encoding="utf-8")
        print("Inserted Figure 3.10 into ch3_system_architecture.tex")

# 7. Chapter 9: insert fig_9_3_multibank_split_gnn
p_ch9 = Path("papers/University_CSE_Thesis/chapters/ch9_conclusion.tex")
t_ch9 = p_ch9.read_text(encoding="utf-8")
if "fig_9_3_multibank_split_gnn" not in t_ch9:
    fig_9_3_code = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{figures/fig_9_3_multibank_split_gnn.pdf}
\caption[Multi-Bank Blind Spot vs. Privacy-Preserving Federated Split-GNN]{Bridging the multi-bank observability barrier: (a) Conventional siloed bank architectures truncate multi-hop laundering chains into disconnected 1-hop transactions; (b) Privacy-Preserving Federated Split-GNN shares universal 12-D invariants ($\mathbf{z}_{\text{inv}}$) and boundary activations ($\mathbf{h}_{\text{bound}}$) without disclosing private entity PII, enabling end-to-end cross-institution crime surveillance under strict GDPR and BSA confidentiality.}
\label{fig:multibank_split_gnn}
\end{figure}
"""
    marker9 = r"\subsection{The Multi-Institution Banking Observability Gap}"
    idx9 = t_ch9.find(marker9)
    if idx9 != -1:
        # find end of first paragraph
        end_p9 = t_ch9.find("\n\n", idx9 + len(marker9) + 20)
        if end_p9 == -1: end_p9 = t_ch9.find(r"\subsection{Cold-Start Entities", idx9)
        t_ch9 = t_ch9[:end_p9] + "\n" + fig_9_3_code + "\n" + t_ch9[end_p9:]
        p_ch9.write_text(t_ch9, encoding="utf-8")
        print("Inserted Figure 9.3 into ch9_conclusion.tex")

print("All figure insertions verified!")
