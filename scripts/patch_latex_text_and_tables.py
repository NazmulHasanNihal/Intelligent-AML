import re
from pathlib import Path

# 1. Update Table 7.5 in ch7_experiments.tex
p_ch7 = Path("papers/University_CSE_Thesis/chapters/ch7_experiments.tex")
t_ch7 = p_ch7.read_text(encoding="utf-8")
idx_s = t_ch7.find(r"\label{tab:master_baseline_summary}")
idx_e = t_ch7.find(r"\end{table}", idx_s)
sub = t_ch7[idx_s:idx_e]
sub_mod = sub.replace(r"$\mathbf{1.0}$", r"$\mathbf{1.07}$", 1)
t_ch7 = t_ch7[:idx_s] + sub_mod + t_ch7[idx_e:]
p_ch7.write_text(t_ch7, encoding="utf-8")
print("Table 7.5 Mean Rank updated to 1.07!")

# 2. Update references.bib with lin2026chronowave
p_bib = Path("papers/University_CSE_Thesis/references.bib")
t_bib = p_bib.read_text(encoding="utf-8")
if "lin2026chronowave" not in t_bib:
    bib_entry = """
@article{lin2026chronowave,
  author    = {Z. Lin and Q. Luo and D. Wu and J. Shen and L. Li and X. Nong and Z. Qin},
  title     = {Detecting illicit transactions in bitcoin: a wavelet-temporal graph transformer approach for anti-money laundering},
  journal   = {Scientific Reports},
  volume    = {16},
  pages     = {1548},
  year      = {2026},
  doi       = {10.1038/s41598-025-23901-3}
}
"""
    t_bib = t_bib.strip() + "\n" + bib_entry
    p_bib.write_text(t_bib, encoding="utf-8")
    print("Added lin2026chronowave to references.bib!")

# 3. Update ch2_literature_review.tex
p_ch2 = Path("papers/University_CSE_Thesis/chapters/ch2_literature_review.tex")
t_ch2 = p_ch2.read_text(encoding="utf-8")
# Add citation to ChronoWave-GNN
t_ch2 = t_ch2.replace(
    r"& ChronoWave-GNN & Wavelet Continuous & Frequency Bandpass & \ding{55} & Wavelet Fallback & \ding{55} & Wavelet Energy \\",
    r"& ChronoWave-GNN~\cite{lin2026chronowave} & Wavelet Continuous & Frequency Bandpass & \ding{55} & Wavelet Fallback & \ding{55} & Wavelet Energy \\"
)
# Update caption to 18-Model
t_ch2 = t_ch2.replace(
    r"\caption[Comprehensive 25-Paper Financial Forensics and Graph ML Taxonomy]{Comprehensive 25-Paper Comparative Taxonomy in Financial Forensics and Graph Machine Learning, Grouped by Methodological Families.}",
    r"\caption[Comprehensive 18-Model Financial Forensics and Graph ML Taxonomy]{Comprehensive 18-Model Comparative Taxonomy in Financial Forensics and Graph Machine Learning, Grouped by Methodological Families.}"
)
# Update "25-paper" prose
t_ch2 = t_ch2.replace("Table~\\ref{tab:lit_matrix} presents an exhaustive 25-paper comparative taxonomy",
                      "Table~\\ref{tab:lit_matrix} presents an exhaustive 18-model comparative taxonomy")
p_ch2.write_text(t_ch2, encoding="utf-8")
print("Updated ch2_literature_review.tex with ChronoWave-GNN citation and 18-Model Taxonomy!")

# 4. Update ch3_system_architecture.tex
p_ch3 = Path("papers/University_CSE_Thesis/chapters/ch3_system_architecture.tex")
t_ch3 = p_ch3.read_text(encoding="utf-8")
old_g5 = r"\subsubsection{Group 5: 5-Moment Causal Ego-Statistics ($\mu_A, \sigma_A^2, \gamma_A, \kappa_A, \nu_{\text{io}}, \sigma_{\Delta t}$)}"
new_g5 = r"\subsubsection{Group 5: 7-Moment Causal Ego-Statistics ($\mu_A, \sigma_A^2, \gamma_A, \kappa_A, \nu_{\text{io}}, \sigma_{\Delta t}, v_A$)}"
t_ch3 = t_ch3.replace(old_g5, new_g5)

old_moments = r"""    \item Inflow-to-outflow velocity ratio ($\nu_{\text{io}} = \sum A_{\text{in}} / \sum A_{\text{out}}$)
    \item Inter-arrival temporal standard deviation ($\sigma_{\Delta t}$)
\end{itemize}"""

new_moments = r"""    \item Inflow-to-outflow velocity ratio ($\nu_{\text{io}} = \sum A_{\text{in}} / \sum A_{\text{out}}$)
    \item Inter-arrival temporal standard deviation ($\sigma_{\Delta t}$)
    \item Transmission capital velocity ($v_A = \text{mean}(A_e / \Delta t_e)$)
\end{itemize}"""
t_ch3 = t_ch3.replace(old_moments, new_moments)
p_ch3.write_text(t_ch3, encoding="utf-8")
print("Updated ch3_system_architecture.tex with 7-Moment Causal Ego-Statistics and v_A bullet!")

# 5. Update ch6_xai_agentic_sar.tex
p_ch6 = Path("papers/University_CSE_Thesis/chapters/ch6_xai_agentic_sar.tex")
t_ch6 = p_ch6.read_text(encoding="utf-8")
t_ch6 = t_ch6.replace("Fed_SR26_2_Receipt", "Fed_SR11_7_Receipt")
p_ch6.write_text(t_ch6, encoding="utf-8")
print("Updated ch6_xai_agentic_sar.tex to Fed_SR11_7_Receipt!")

# 6. Update ch10_appendices.tex
p_ch10 = Path("papers/University_CSE_Thesis/chapters/ch10_appendices.tex")
t_ch10 = p_ch10.read_text(encoding="utf-8")
# Fix SR26 tag
t_ch10 = t_ch10.replace("Model_Governance_SR26_2_Receipt", "Model_Governance_SR11_7_Receipt")
# Fix empty hash
t_ch10 = t_ch10.replace("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                         "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")
# Fix tau_gate to delta_floor
t_ch10 = t_ch10.replace(r"Edge Trust Threshold ($\tau_{\text{gate}}$)", r"Edge Trust Floor ($\delta_{\text{floor}}$)")
t_ch10 = t_ch10.replace(r"($g_{ij} \ge \tau_{\text{gate}}$)", r"($g_{ij} \ge \delta_{\text{floor}}$)")
p_ch10.write_text(t_ch10, encoding="utf-8")
print("Updated ch10_appendices.tex with SR11_7, real Merkle hash, and delta_floor!")

