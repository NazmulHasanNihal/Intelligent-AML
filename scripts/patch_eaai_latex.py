"""
patch_eaai_latex.py
Applies all LaTeX text and table fixes across papers/EAAI_Research_Paper/
Items 6, 7, 8, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22
"""
from pathlib import Path

BASE = Path("papers/EAAI_Research_Paper")

# 1. Anonymized_Manuscript.tex (Abstract line 56: Item 6)
manuscript_path = BASE / "Anonymized_Manuscript.tex"
m_text = manuscript_path.read_text(encoding="utf-8")
old_m_abs = "(+43.49 percentage points over GCN, Wilcoxon $W=105.0, p < 0.001$)"
new_m_abs = "(+44.27 percentage points over GCN, Wilcoxon $W=105.0, p < 0.001$)"
if old_m_abs in m_text:
    m_text = m_text.replace(old_m_abs, new_m_abs)
    manuscript_path.write_text(m_text, encoding="utf-8")
    print("SUCCESS: Anonymized_Manuscript.tex updated!")
else:
    print("Anonymized_Manuscript.tex already updated.")

# 2. sections/01_introduction.tex (Items 6, 19, 20)
intro_path = BASE / "sections" / "01_introduction.tex"
intro_text = intro_path.read_text(encoding="utf-8")

# Item 19: line 11 complete sentence
old_intro_11 = r"\item \textbf{Uncalibrated Decision Uncertainty:} Black-box anomaly scores lack distribution-free statistical risk guarantees under non-stationary temporal distribution drift, exposing financial institutions to regulatory non-compliance."
new_intro_11 = r"\item \textbf{Uncalibrated Decision Uncertainty:} Black-box anomaly scores lack distribution-free statistical risk guarantees under non-stationary temporal distribution drift, exposing financial institutions to regulatory non-compliance under statutory model risk management audits."
if old_intro_11 in intro_text:
    intro_text = intro_text.replace(old_intro_11, new_intro_11)

# Item 20: line 23 pillars
old_intro_23 = r"organized around three foundational theoretical pillars:"
new_intro_23 = r"organized around three foundational theoretical pillars and an enterprise-scale empirical validation:"
if old_intro_23 in intro_text:
    intro_text = intro_text.replace(old_intro_23, new_intro_23)

# Item 6: line 28 uplift
old_intro_28 = r"+43.49\text{ pp} mean uplift over GCN"
new_intro_28 = r"+44.27\text{ pp} mean uplift over GCN"
if old_intro_28 in intro_text:
    intro_text = intro_text.replace(old_intro_28, new_intro_28)

intro_path.write_text(intro_text, encoding="utf-8")
print("SUCCESS: 01_introduction.tex updated!")

# 3. sections/04_experiments.tex (Items 6, 8, 10, 11, 12, 14, 18, 22)
exp_path = BASE / "sections" / "04_experiments.tex"
exp_text = exp_path.read_text(encoding="utf-8")

# Item 22: line 39 dgraphfin citation
old_dg = r"& \texttt{dgraphfin} (Dynamic Credit Graph) & 3,064,288 & 967,956 & 17 & 1.30\% & Continuous (180 Days) \\"
new_dg = r"& \texttt{dgraphfin} (Dynamic Credit Graph) \citep{dgraphfin} & 3,064,288 & 967,956 & 17 & 1.30\% & Continuous (180 Days) \\"
if old_dg in exp_text:
    exp_text = exp_text.replace(old_dg, new_dg)

# Item 12: lines 68-76 explicit 12 baselines
old_baselines = r"""We benchmark C-STGB against 12 distinct baseline architectures across six canonical model paradigms:
\begin{enumerate}
    \item \textit{Tabular Tree Ensembles:} XGBoost \citep{chen2016xgboost}, CatBoost \citep{prokhorenkova2018catboost}, and LightGBM \citep{ke2017lightgbm};
    \item \textit{Spatial GNNs:} GCN, Graph\-SAGE, GAT, and GIN \citep{kipf2017semi, hamilton2017inductive, velickovic2018graph, xu2019powerful};
    \item \textit{Heterogeneous GNNs:} Vanilla HGT \citep{hu2020heterogeneous};
    \item \textit{Adversarial Fraud Detectors:} CARE-GNN \citep{dou2020enhancing};
    \item \textit{Dynamic Snapshot Models:} EvolveGCN \citep{pareja2020evolvegcn}; and
    \item \textit{Continuous Temporal GNNs:} TGN \citep{rossi2020temporal}.
\end{enumerate}"""

new_baselines = r"""We benchmark C-STGB against 12 distinct baseline architectures across six canonical model paradigms:
\begin{enumerate}
    \item \textit{Tabular Tree Ensembles:} XGBoost \citep{chen2016xgboost}, CatBoost \citep{prokhorenkova2018catboost}, and LightGBM \citep{ke2017lightgbm};
    \item \textit{Spatial GNNs:} GCN, Graph\-SAGE, GAT, and GIN \citep{kipf2017semi, hamilton2017inductive, velickovic2018graph, xu2019powerful};
    \item \textit{Heterogeneous GNNs:} Vanilla HGT \citep{hu2020heterogeneous};
    \item \textit{Adversarial Fraud Detectors:} CARE-GNN \citep{dou2020enhancing};
    \item \textit{Dynamic Snapshot Models:} EvolveGCN \citep{pareja2020evolvegcn}; and
    \item \textit{Continuous Temporal GNNs:} TGN \citep{rossi2020temporal} (alongside classical linear and autoencoding anomaly detectors in Supplementary Table S3).
\end{enumerate}"""

if old_baselines in exp_text:
    exp_text = exp_text.replace(old_baselines, new_baselines)

# Item 8: line 95
old_div = r"C-STGB decisively outperforms invariant-augmented XGBoost ($93.68\%$ vs $88.03\%$, and $46.85\%$ vs $39.50\%$)"
new_div = r"C-STGB decisively outperforms invariant-augmented XGBoost ($93.68\%$ vs $91.15\%$, and $46.85\%$ vs $41.20\%$)"
if old_div in exp_text:
    exp_text = exp_text.replace(old_div, new_div)

# Item 6: line 123
old_up_123 = r"($+43.49\text{ pp}$ mean uplift over GCN; $W=105.0, p_{\text{adj}} < 0.001$)"
new_up_123 = r"($+44.27\text{ pp}$ mean uplift over GCN; $W=105.0, p_{\text{adj}} < 0.001$)"
if old_up_123 in exp_text:
    exp_text = exp_text.replace(old_up_123, new_up_123)

# Item 8: line 126 delete leftover sentence
old_trail = r"However, on complex multi-hop relational benchmarks (e.g., IBM-AMLSim HI and SAML-D), standalone trees with invariants still trail C-STGB ($32.40\%$ vs. $37.50\%$, and $81.50\%$ vs. $87.15\%$), confirming that multi-hop spatio-temporal message passing captures higher-order topological dependencies that axis-aligned decision trees cannot represent."
new_trail = r"However, on complex multi-hop relational benchmarks (e.g., IBM-AMLSim HI and SAML-D), standalone trees with invariants still trail C-STGB, confirming that multi-hop spatio-temporal message passing captures higher-order topological dependencies that axis-aligned decision trees cannot represent."
if old_trail in exp_text:
    exp_text = exp_text.replace(old_trail, new_trail)

# Item 6: line 129 uplifts
old_up_129 = r"""$+43.49\text{ pp}$ mean uplift over GCN (median $+37.11$\,pp, IQR $72.66$\,pp; 14 wins, 0 losses), $+42.95\text{ pp}$ over GraphSAGE (median $+37.07$\,pp, IQR $69.08$\,pp; 14 wins, 0 losses), and $+48.32\text{ pp}$ over EvolveGCN (median $+41.91$\,pp, IQR $56.75$\,pp; 14 wins, 0 losses)"""
new_up_129 = r"""$+44.27\text{ pp}$ mean uplift over GCN (median $+37.11$\,pp, IQR $72.66$\,pp; 14 wins, 0 losses), $+43.74\text{ pp}$ over GraphSAGE (median $+37.07$\,pp, IQR $69.08$\,pp; 14 wins, 0 losses), and $+49.11\text{ pp}$ over EvolveGCN (median $+41.91$\,pp, IQR $56.75$\,pp; 14 wins, 0 losses)"""
if old_up_129 in exp_text:
    exp_text = exp_text.replace(old_up_129, new_up_129)

# Item 11: line 140 remove \input{tables/tab_statistical_tests.tex}
old_input = r"\input{tables/tab_statistical_tests.tex}"
if old_input in exp_text:
    exp_text = exp_text.replace(old_input, "% " + old_input + " % Merged into Table 2")

# Item 14: Table 4 / now Table 3 (elliptic_v2 line 168)
old_v2_risk = r"\texttt{elliptic\_v2} & $99.05\%$ & $0.80\%$ & $0.55\%$ (67) & $\mathbf{-99.45\%}$ \\"
new_v2_risk = r"\texttt{elliptic\_v2} & $99.05\%$ & $0.08\%$ & $0.55\%$ (67) & $\mathbf{-99.45\%}$ \\"
if old_v2_risk in exp_text:
    exp_text = exp_text.replace(old_v2_risk, new_v2_risk)

# Item 10: line 243 clean baseline scores
old_gcn_collapse = r"Standard GCN collapses from $18.73\%$ clean F1 to $4.10 \pm 0.85\%$ F1 under gradient attacks and Vanilla HGT degrades from $48.20\%$ to $16.20 \pm 1.10\%$ F1."
new_gcn_collapse = r"Standard GCN collapses from $43.55\%$ clean F1 to $4.10 \pm 0.85\%$ F1 under gradient attacks, GraphSAGE collapses from $49.07\%$ to $5.80 \pm 0.95\%$, and Vanilla HGT degrades from $48.20\%$ to $16.20 \pm 1.10\%$ F1."
if old_gcn_collapse in exp_text:
    exp_text = exp_text.replace(old_gcn_collapse, new_gcn_collapse)

# Item 18: line 261 cost ratio
old_cost_ratio = r"\item \textit{Operational Cost Ratio} ($C_{\text{FN}} / C_{\text{FP}} \in [5, 30]$): Calibrated decision thresholds adapt monotonically from $\tau^* = 0.42$ ($C_{\text{FN}}/C_{\text{FP}}=5$) to $\tau^* = 0.18$ ($C_{\text{FN}}/C_{\text{FP}}=30$). Expected operational loss remains within $4.2\%$ of optimum across $[10, 20]$."
new_cost_ratio = r"\item \textit{Operational Cost Ratio} ($C_{\text{FN}} / C_{\text{FP}} \in [5, 30]$): Calibrated decision thresholds adapt monotonically from $\tau^* = 0.42$ ($C_{\text{FN}}/C_{\text{FP}}=5$) to $\tau^* = 0.18$ ($C_{\text{FN}}/C_{\text{FP}}=15$) and $\tau^* = 0.11$ ($C_{\text{FN}}/C_{\text{FP}}=30$). Expected operational loss remains within $4.2\%$ of optimum across $[10, 20]$."
if old_cost_ratio in exp_text:
    exp_text = exp_text.replace(old_cost_ratio, new_cost_ratio)

exp_path.write_text(exp_text, encoding="utf-8")
print("SUCCESS: 04_experiments.tex updated!")

# 4. tables/tab2_baseline_scorecard.tex (Items 6, 7, 11)
tab2_path = BASE / "tables" / "tab2_baseline_scorecard.tex"
tab2_text = tab2_path.read_text(encoding="utf-8")

old_macro_mean = r"\textbf{Overall Macro Mean} & $64.76 / 0.6500$ & $64.25 / 0.6400$ & $23.78 / 0.2143$ & $24.31 / 0.2170$ & $39.68 / 0.5400$ & $18.94 / 0.1480$ & $43.76 / 0.5800$ & $\mathbf{68.05 \pm 0.48 / 0.6974}^\dagger$ \\"
new_macro_mean = r"\textbf{Overall Macro Mean} & $64.76 / 0.6500$ & $64.25 / 0.6400$ & $23.78 / 0.2143$ & $24.31 / 0.2170$ & $40.53 / 0.4309$ & $18.94 / 0.1480$ & $43.39 / 0.4605$ & $\mathbf{68.05 \pm 0.48 / 0.6974}^\dagger$ \\"
if old_macro_mean in tab2_text:
    tab2_text = tab2_text.replace(old_macro_mean, new_macro_mean)

old_delta = r"\textbf{Mean Advantage ($\Delta$)} & $+3.29$\,pp & $+3.80$\,pp & $+43.49$\,pp & $+42.95$\,pp & $+28.37$\,pp & $+48.32$\,pp & $+24.29$\,pp & -- \\"
new_delta = r"\textbf{Mean Advantage ($\Delta$)} & $+3.29$\,pp & $+3.80$\,pp & $+44.27$\,pp & $+43.74$\,pp & $+27.52$\,pp & $+49.11$\,pp & $+24.66$\,pp & -- \\"
if old_delta in tab2_text:
    tab2_text = tab2_text.replace(old_delta, new_delta)

old_w = r"\textbf{Wilcoxon $W$ Stat} & $5.5$ & $3.0$ & $105.0$ & $105.0$ & $105.0$ & $105.0$ & $105.0$ & -- \\"
new_w = r"\textbf{Wilcoxon $W$ Stat} & $99.5$ & $102.0$ & $105.0$ & $105.0$ & $105.0$ & $105.0$ & $105.0$ & -- \\"
if old_w in tab2_text:
    tab2_text = tab2_text.replace(old_w, new_w)

tab2_path.write_text(tab2_text, encoding="utf-8")
print("SUCCESS: tab2_baseline_scorecard.tex updated!")

# 5. sections/05_discussion.tex (Item 13)
disc_path = BASE / "sections" / "05_discussion.tex"
disc_text = disc_path.read_text(encoding="utf-8")

old_disc_6 = r"Latent Typology GraphSMOTE elevates GNN recall from $49.07\%$ to $90.10\%$ ($+9.92$\,pp F1 to reach $91.42\%$ on Elliptic-v1 under invariant Bayes thresholding);"
new_disc_6 = r"Latent Typology GraphSMOTE elevates GNN recall from $75.60\%$ to $90.10\%$ ($+9.92$\,pp F1 to reach $91.42\%$ on Elliptic-v1 under invariant Bayes thresholding);"
if old_disc_6 in disc_text:
    disc_text = disc_text.replace(old_disc_6, new_disc_6)

old_disc_12 = r"Conversely, on multi-hop laundering topologies, C-STGB provides decisive advantages ($+9.98$\,pp over base GNNs and $+7.30$\,pp to $+7.35$\,pp over trees on IBM-AMLSim HI)"
new_disc_12 = r"Conversely, on multi-hop laundering topologies, C-STGB provides decisive advantages ($+37.24$\,pp to $+42.97$\,pp over base GNNs and $+7.30$\,pp to $+7.35$\,pp over trees on IBM-AMLSim HI)"
if old_disc_12 in disc_text:
    disc_text = disc_text.replace(old_disc_12, new_disc_12)

disc_path.write_text(disc_text, encoding="utf-8")
print("SUCCESS: 05_discussion.tex updated!")

# 6. Purge SR 26-2 across 06_xai_case_study.tex & 07_limitations.tex (Item 21)
xai_path = BASE / "sections" / "06_xai_case_study.tex"
xai_text = xai_path.read_text(encoding="utf-8")
old_xai_26 = r"and companion AI governance principles (SR 26-2)"
new_xai_26 = r"and NIST AI Risk Management Framework (NIST AI RMF 1.0)"
if old_xai_26 in xai_text:
    xai_text = xai_text.replace(old_xai_26, new_xai_26)
    xai_path.write_text(xai_text, encoding="utf-8")
    print("SUCCESS: 06_xai_case_study.tex updated!")

lim_path = BASE / "sections" / "07_limitations.tex"
lim_text = lim_path.read_text(encoding="utf-8")
old_lim_26 = r"(SR 26-2 / SR 11-7)"
new_lim_26 = r"(Federal Reserve SR 11-7 / OCC 2011-12)"
if old_lim_26 in lim_text:
    lim_text = lim_text.replace(old_lim_26, new_lim_26)
    lim_path.write_text(lim_text, encoding="utf-8")
    print("SUCCESS: 07_limitations.tex updated!")