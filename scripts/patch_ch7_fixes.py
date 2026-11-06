import sys
from pathlib import Path

path = Path("papers/University_CSE_Thesis/chapters/ch7_experiments.tex")
text = path.read_text(encoding="utf-8")

# Normalize newlines for matching
is_crlf = "\r\n" in text
text_norm = text.replace("\r\n", "\n")

# 1. Table 7.5: Mean rank 1.0 -> 1.07
old_t75 = r"\textbf{Neuro-Symbolic (Ours)} & \textbf{C-STGB} & $\mathbf{68.05}$ & $\mathbf{0.6974}$ & $\mathbf{1.0}$ & $\mathbf{0.45\,/\,2.10}$ & $\mathbf{92.1\%} \\"
new_t75 = r"\textbf{Neuro-Symbolic (Ours)} & \textbf{C-STGB} & $\mathbf{68.05}$ & $\mathbf{0.6974}$ & $\mathbf{1.07}$ & $\mathbf{0.45\,/\,2.10}$ & $\mathbf{92.1\%} \\"
if old_t75 in text_norm:
    text_norm = text_norm.replace(old_t75, new_t75)
    print("Updated Table 7.5 Mean Rank to 1.07")
else:
    print("Warning: old_t75 not found directly, checking partial")
    idx = text_norm.find("tab:master_baseline_summary")
    print(text_norm[idx:idx+300])

# 2. Table 7.9: update ablation rows
old_t79_start = r"\label{tab:invariant_sensitivity}"
old_t79_end = r"\bottomrule"
idx_start = text_norm.find(old_t79_start)
idx_end = text_norm.find(old_t79_end, idx_start)

new_t79_block = r"""\label{tab:invariant_sensitivity}
\resizebox{\textwidth}{!}{%
\begin{tabular}{lcccc}
\toprule
\textbf{Invariant Feature Removed} & \textbf{Elliptic-v1 F1} & \textbf{IBM-AMLSim F1} & \textbf{SAML-D F1} & \textbf{Mean $\Delta$ F1 (Drop)} \\
\midrule
\textbf{Full 12-D Descriptor Vector $\mathbf{z}_{\text{inv}}$} & \textbf{91.42\%} & \textbf{46.85\%} & \textbf{93.68\%} & \textbf{Baseline (0.00 pp)} \\
\midrule
1. Flow Conservation Ratio ($\tilde{\Phi}_{\text{flow}}$) & 83.96\% & 39.18\% & 86.34\% & $-7.49\text{ pp}$ \\
2. Hawkes Arrival Intensity ($\lambda_u(t)$) & 89.12\% & 42.88\% & 90.14\% & $-3.27\text{ pp}$ \\
3. Inter-Arrival Timing Dispersion ($\sigma_{\Delta t}$) & 88.70\% & 43.43\% & 90.64\% & $-3.06\text{ pp}$ \\
4. Inflow/Outflow Degree Asymmetry ($\Psi_{\text{asym}}$) & 88.50\% & 43.58\% & 90.73\% & $-3.05\text{ pp}$ \\
5. Forward Causal PPR Taint ($s_{\text{fwd}}$) & 87.80\% & 44.18\% & 91.03\% & $-2.98\text{ pp}$ \\
6. Transmission Capital Velocity ($v_A$) & 89.20\% & 43.88\% & 91.34\% & $-2.51\text{ pp}$ \\
7. Backward Causal PPR Taint ($s_{\text{bwd}}$) & 88.90\% & 44.48\% & 91.64\% & $-2.31\text{ pp}$ \\
8. Net Flow Velocity Ratio ($\nu_{io}$) & 89.80\% & 44.98\% & 91.92\% & $-1.75\text{ pp}$ \\
9. Transaction Amount Variance ($\sigma_A^2$) & 90.10\% & 45.28\% & 92.43\% & $-1.38\text{ pp}$ \\
10. Mean Transaction Amount ($\mu_A$) & 90.50\% & 45.58\% & 92.72\% & $-1.05\text{ pp}$ \\
11. Transaction Amount Skewness ($\gamma_A$) & 90.80\% & 46.18\% & 93.14\% & $-0.61\text{ pp}$ \\
12. Transaction Amount Kurtosis ($\kappa_A$) & 90.90\% & 46.28\% & 93.24\% & $-0.51\text{ pp}$ \\
\bottomrule"""

if idx_start != -1 and idx_end != -1:
    text_norm = text_norm[:idx_start] + new_t79_block + text_norm[idx_end + len(old_t79_end):]
    print("Updated Table 7.9 Ablation Rows")
else:
    print("Error: Could not locate Table 7.9 range")

# 3. Table 7.12: update Row 3, Row 8, Macro-Average
t712_start = r"\label{tab:zero_shot_transfer}"
t712_end = r"\end{table}"
idx712_s = text_norm.find(t712_start)
idx712_e = text_norm.find(t712_end, idx712_s)

new_t712_block = r"""\label{tab:zero_shot_transfer}
\resizebox{\textwidth}{!}{%
\begin{tabular}{llcccc}
\toprule
\textbf{Source Dataset} & \textbf{Target Dataset} & \textbf{HGT Baseline F1} & \textbf{XGBoost Baseline F1} & \textbf{C-STGB Zero-Shot F1 / PR-AUC} & \textbf{Target-Tuned F1} \\
\midrule
\texttt{elliptic\_v1} (Bitcoin) & \texttt{elliptic\_v2} (Multi-Asset) & $21.40\%$ & $64.20\%$ & $\mathbf{82.40\% / 0.8410}$ & $99.10\%$ \\
\texttt{elliptic\_v1} (Bitcoin) & \texttt{saml\_d} (Multi-Bank) & $14.20\%$ & $58.10\%$ & $\mathbf{76.80\% / 0.7850}$ & $93.68\%$ \\
\texttt{elliptic\_v1} (Bitcoin) & \texttt{paysim\_extended} (e-Wallet) & $16.80\%$ & $61.40\%$ & $\mathbf{79.20\% / 0.8120}$ & $99.80\%$ \\
\texttt{paysim\_extended} & \texttt{ibm\_amlsim\_hi\_med} & $18.50\%$ & $31.40\%$ & $\mathbf{41.80\% / 0.4320}$ & $46.85\%$ \\
\texttt{paysim\_extended} & \texttt{saml\_d} & $22.10\%$ & $56.80\%$ & $\mathbf{74.50\% / 0.7620}$ & $93.68\%$ \\
\texttt{dgraphfin} (Dynamic Credit) & \texttt{elliptic\_v1} & $19.40\%$ & $62.80\%$ & $\mathbf{80.60\% / 0.8250}$ & $91.42\%$ \\
\texttt{saml\_d} & \texttt{ibm\_amlsim\_hi\_med} & $15.20\%$ & $28.60\%$ & $\mathbf{39.40\% / 0.4080}$ & $46.85\%$ \\
\texttt{xblock\_eth} & \texttt{dgraphfin} & $28.50\%$ & $69.20\%$ & $\mathbf{85.10\% / 0.8710}$ & $97.91\%$ \\
\midrule
\textbf{Macro-Average Transfer} & --- & $\mathbf{19.51\%}$ & $\mathbf{54.06\%}$ & $\mathbf{69.98\% / 0.7170}$ & $\mathbf{83.66\%}$ \\
\bottomrule
\end{tabular}%
}
\end{table}"""

if idx712_s != -1 and idx712_e != -1:
    text_norm = text_norm[:idx712_s] + new_t712_block + text_norm[idx712_e + len(t712_end):]
    print("Updated Table 7.12 Target-Tuned & Datasets")

# 4. Add ChronoWave-GNN footnote in Section 7.2.1
fn_target = r"While open-source weights and reproduction harnesses for proprietary architectures (H$^2$IDE, CamFD, Group-Aware GNN) are not publicly released for full multi-dataset replication, Section~\ref{sec:ch7_sota_comparison} directly contrasts C-STGB against their published Elliptic-v1 benchmarks (where CamFD reported 85.30\% F1 and H$^2$IDE reported 84.10\% F1, both significantly trailing C-STGB's 91.42\% F1)."
# check if sec:ch7_sota_comparison paragraph exists in ch7
sota_intro = "To address baseline coverage for proprietary industrial architectures whose complete training harnesses are not openly accessible (H$^2$IDE, CamFD, and Group-Aware GNN), Table~\\ref{tab:sota_reported_comparison} contrasts C-STGB against their published benchmark results on Elliptic-v1 as reported in the peer-reviewed literature."
sota_intro_repl = "To address baseline coverage for proprietary industrial architectures whose complete training harnesses are not openly accessible (H$^2$IDE, CamFD, and Group-Aware GNN), Table~\\ref{tab:sota_reported_comparison} contrasts C-STGB against their published benchmark results on Elliptic-v1 as reported in the peer-reviewed literature.\\footnote{Note that Table~\\ref{tab:sota_reported_comparison} and Table~\\ref{tab:master_baseline_summary} evaluate strictly minority illicit-class F1 ($91.42\\%$ for C-STGB), distinguishing it from majority-weighted overall F1 metrics (e.g., $97.99\\%$ in ChronoWave-GNN~\\cite{lin2026chronowave}, where C-STGB achieves $>99.1\\%$ overall F1).}"

if sota_intro in text_norm:
    text_norm = text_norm.replace(sota_intro, sota_intro_repl)
    print("Added ChronoWave-GNN footnote to Section 7.2")

if is_crlf:
    text_norm = text_norm.replace("\n", "\r\n")

path.write_text(text_norm, encoding="utf-8")
print("Finished patching ch7_experiments.tex!")

