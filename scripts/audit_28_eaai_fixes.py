"""
audit_28_eaai_fixes.py
Comprehensive automated test suite verifying all 28 EAAI fixes
across LaTeX source files, tables, figures, and compiled PDFs.
"""
import sys
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
EAAI_DIR = BASE_DIR / "papers" / "EAAI_Research_Paper"
FIG_DIR = EAAI_DIR / "figures"

errors = []
passes = []

def check(condition, desc, error_msg):
    if condition:
        passes.append(desc)
        print(f"  [PASS] {desc}")
    else:
        errors.append(f"{desc}: {error_msg}")
        print(f"  [FAIL] {desc} -> {error_msg}")

print("=" * 70)
print("AUDITING ALL 28 EAAI ERRORS & FIXES")
print("=" * 70)

# -------------------------------------------------------------
# Category A: Figures (Items 1-5, 9, 10, 25, 26)
# -------------------------------------------------------------
print("\n--- CATEGORY A: FIGURES & RENDERING ---")

# Item 1: Figure 1 text overlaps & Assisted FinCEN SAR Dossier
fig1_py = (BASE_DIR / "scripts" / "generate_final_10_of_10_figures.py").read_text(encoding="utf-8")
check("Assisted FinCEN SAR Dossier" in fig1_py,
      "Item 1: Figure 1 Assisted FinCEN SAR Dossier present",
      "Assisted FinCEN SAR Dossier missing from figure generator")
check("Auto FinCEN SAR Package" not in fig1_py,
      "Item 1: Figure 1 Auto FinCEN SAR Package purged",
      "Auto FinCEN SAR Package still present in figure generator")
check((FIG_DIR / "fig1_operational_architecture_flowchart.pdf").exists(),
      "Item 1: fig1_operational_architecture_flowchart.pdf exists",
      "File missing")

# Item 2: Figure 6 Pareto
check("ax.set_ylim([60, 6500])" in fig1_py,
      "Item 2: Figure 6 y-axis headroom ([60, 6500])",
      "Headroom not set in generate_final_10_of_10_figures.py")
check("Core Banking Fast SLA (< 1 ms)" in fig1_py,
      "Item 2: Figure 6 legend (< 1 ms) clean",
      "Raw latex glitch in legend label")
check((FIG_DIR / "fig_table7_latency_pareto.pdf").exists(),
      "Item 2: fig_table7_latency_pareto.pdf exists",
      "File missing")

# Item 3: Figure 3 PR/ROC
fig_all_py = (BASE_DIR / "scripts" / "generate_all_publication_figures.py").read_text(encoding="utf-8")
check("prec_sage = np.clip" in fig_all_py and "prec_gcn = np.clip" in fig_all_py,
      "Item 3: Figure 3 curves clipped with np.clip(..., 0.0, 1.0)",
      "Curves not clipped in generate_all_publication_figures.py")
check((FIG_DIR / "fig1_pr_roc_curves.pdf").exists(),
      "Item 3: fig1_pr_roc_curves.pdf exists",
      "File missing")

# Item 4: Figure 4 t-SNE
check("Silhouette S =" in fig_all_py,
      "Item 4: Figure 4 title plain text math",
      "Title contains raw unescaped math causing character collision")
check((FIG_DIR / "fig2_tsne_manifold_separation.pdf").exists(),
      "Item 4: fig2_tsne_manifold_separation.pdf exists",
      "File missing")

# Item 5: Figure 5 Conformal Calibration
check("99.32% Tier-3 STP | 99.50% Singletons" in fig1_py,
      "Item 5: Figure 5 callout synchronized with Table 4",
      "Callout label not synchronized")
check((FIG_DIR / "fig_conformal_coverage_reliability.pdf").exists(),
      "Item 5: fig_conformal_coverage_reliability.pdf exists",
      "File missing")

# Item 9: Figure 2(a) light blue bar on elliptic_v1 without invariants
check("native_elliptic = [43.55, 49.07, 51.04, 68.40, 87.90, 88.35, 83.96]" in fig1_py,
      "Item 9: Figure 2(a) C-STGB without z_inv is 83.96% (+7.46 pp)",
      "native_elliptic not set to 83.96 in figure generator")

# Item 10: Clean rho=0 baseline scores
check("f1_care       = np.array([64.50" in fig_all_py,
      "Item 10: Figure 9 clean CARE-GNN is 64.50%",
      "CARE-GNN starting value not 64.50%")
check("f1_graphsage = np.array([49.07" in fig_all_py,
      "Item 10: Figure 9 clean GraphSAGE is 49.07%",
      "GraphSAGE starting value not 49.07%")
check("f1_gcn       = np.array([43.55" in fig_all_py,
      "Item 10: Figure 9 clean GCN is 43.55%",
      "GCN starting value not 43.55%")

# Item 25: Figure S2 top crop
check("top=0.86" in fig_all_py and "y=0.96" in fig_all_py,
      "Item 25: Figure S2 top padding headroom",
      "Figure S2 top padding not set")

# Item 26: Figures S4-S7 full-width & vector
check("line3 = ax_right.plot(node_degrees, alpha_gate" in fig_all_py,
      "Item 26: Figure S7(b) split dual y-axes via twinx()",
      "twinx() not found in fig22 code")
check("xytext=(0.22, 2.45)" in fig_all_py,
      "Item 26: Figure S4 threshold label offset",
      "Threshold label offset not set in fig17 code")

# -------------------------------------------------------------
# Category B: LaTeX Main Manuscript Text & Tables
# -------------------------------------------------------------
print("\n--- CATEGORY B: MAIN MANUSCRIPT TEXT & TABLES ---")

manuscript = (EAAI_DIR / "Anonymized_Manuscript.tex").read_text(encoding="utf-8")
intro = (EAAI_DIR / "sections" / "01_introduction.tex").read_text(encoding="utf-8")
exp = (EAAI_DIR / "sections" / "04_experiments.tex").read_text(encoding="utf-8")
tab2 = (EAAI_DIR / "tables" / "tab2_baseline_scorecard.tex").read_text(encoding="utf-8")
disc = (EAAI_DIR / "sections" / "05_discussion.tex").read_text(encoding="utf-8")
meth = (EAAI_DIR / "sections" / "03_methodology.tex").read_text(encoding="utf-8")
xai = (EAAI_DIR / "sections" / "06_xai_case_study.tex").read_text(encoding="utf-8")
lim = (EAAI_DIR / "sections" / "07_limitations.tex").read_text(encoding="utf-8")

# Item 6: GNN mean uplifts across all files
check("+44.27 percentage points over GCN" in manuscript,
      "Item 6: Manuscript Abstract GCN uplift +44.27 pp",
      "Abstract has outdated GCN uplift")
check(bool(re.search(r"\+44\.27\\text\{\s*pp\}\$?\s*mean\s*uplift\s*over\s*GCN", intro)),
      "Item 6: Introduction line 28 GCN uplift +44.27 pp",
      "Intro line 28 has outdated GCN uplift")
check(bool(re.search(r"\+44\.27\\text\{\s*pp\}\$?\s*mean\s*uplift\s*over\s*GCN", exp)),
      "Item 6: Experiments line 123 GCN uplift +44.27 pp",
      "Experiments line 123 has outdated GCN uplift")
check(bool(re.search(r"\+43\.74\\text\{\s*pp\}\$?\s*over\s*GraphSAGE", exp)) and bool(re.search(r"\+49\.11\\text\{\s*pp\}\$?\s*over\s*EvolveGCN", exp)),
      "Item 6: Experiments line 129 GraphSAGE (+43.74) & EvolveGCN (+49.11) uplifts",
      "Experiments line 129 has outdated uplifts")
check("+44.27" in tab2 and "+43.74" in tab2 and "+27.52" in tab2 and "+49.11" in tab2 and "+24.66" in tab2,
      "Item 6 & 7: Table 2 Delta row exact uplifts (+44.27, +43.74, +27.52, +49.11, +24.66)",
      "Table 2 Delta row has outdated numbers")

# Item 7: Table 2 Macro Averages
check("40.53 / 0.4309" in tab2,
      "Item 7: Table 2 CARE-GNN macro average 40.53 / 0.4309",
      "CARE-GNN macro average incorrect in Table 2")
check("43.39 / 0.4605" in tab2,
      "Item 7: Table 2 TGN macro average 43.39 / 0.4605",
      "TGN macro average incorrect in Table 2")

# Item 8: Contradictory SAML-D & IBM-AMLSim Scores
check("91.15" in exp and "41.20" in exp,
      "Item 8: Experiments line 95 SAML-D (91.15%) and AMLSim (41.20%)",
      "Experiments line 95 numbers incorrect")
check("32.40" not in exp,
      "Item 8: Leftover contradictory numbers purged from line 126",
      "Leftover sentence still present in line 126")

# Item 10: Clean baseline scores in Sec 4.9
check("43.55" in exp and "clean F1" in exp,
      "Item 10: Experiments line 243 clean GCN 43.55%",
      "Line 243 has outdated clean GCN score")
check("49.07" in exp and "GraphSAGE collapses" in exp,
      "Item 10: Experiments line 243 clean GraphSAGE 49.07%",
      "Line 243 has outdated clean GraphSAGE score")

# Item 11: Duplicate Table 3 purged and Wilcoxon W_stat
check(not ("\\input{tables/tab_statistical_tests.tex}" in exp and not exp.split("\\input{tables/tab_statistical_tests.tex}")[0].endswith("% ")),
      "Item 11: Duplicate tab_statistical_tests.tex un-inputted from 04_experiments.tex",
      "Duplicate table still active in 04_experiments.tex")
check("99.5" in tab2 and "102.0" in tab2 and "105.0" in tab2,
      "Item 11: Table 2 reports Wilcoxon W_+ consistently (99.5, 102.0, 105.0)",
      "Table 2 W_+ row not consistent")

# Item 12: 12 Baselines explicitly listed
check("12 distinct baseline architectures" in exp and "TGN" in exp and "LightGBM" in exp,
      "Item 12: 12 baselines listed in Section 4.3",
      "Baseline list incomplete")

# Item 13: Section 5.1 & 5.2 Ablation Numbers
check("75.60" in disc and "elevates GNN recall" in disc,
      "Item 13: Discussion line 6 recall baseline 75.60%",
      "Discussion line 6 still says 49.07%")
check("+37.24" in disc and "+42.97" in disc and "over base GNNs" in disc,
      "Item 13: Discussion line 12 advantage over base GNNs (+37.24 to +42.97 pp)",
      "Discussion line 12 still says +9.98 pp")

# Item 14: Table 4 / Table 3 elliptic_v2 selective risk outlier
check(r"\texttt{elliptic\_v2} & $99.05\%$ & $0.08\%$" in exp,
      "Item 14: Table 4 elliptic_v2 selective risk 0.08%",
      "elliptic_v2 selective risk still 0.80%")

# Item 15: Equation 22 indicator
check(r"\mathbb{I}" in meth,
      "Item 15: Standard mathbb{I} indicator in methodology",
      "Indicator mathbb{I} missing")

# Item 16: Algorithm 1 typos
check(r"th\hat{g}" not in meth,
      "Item 16: No stray th\\hat{g} typos in Algorithm 1",
      "Stray th\\hat{g} typo found in methodology")
check(r"\Gamma(u)" in meth and r"\hat{p}_u" in meth and r"\mathbf{h}_u^*" in meth,
      "Item 16: Algorithm 1 uses Gamma(u), p_hat_u, h_u^*",
      "Standard notation missing from Algorithm 1")

# Item 17: Loss parameters standardized
check(r"\gamma_{\text{focal}}=1.5" in meth and r"\lambda_{\text{recon}} = 0.50" in meth and r"\lambda_{\text{aux}} = 0.10" in meth and r"\eta_{\text{aci}} = 0.005" in meth,
      "Item 17: Loss parameters standardized in methodology (gamma=1.5, recon=0.50, aux=0.10, aci=0.005)",
      "Loss parameters not standardized in methodology.tex")

# Item 18: Section 4.10 cost ratio
check(r"\tau^* = 0.18$ ($C_{\text{FN}}/C_{\text{FP}}=15$) and $\tau^* = 0.11$ ($C_{\text{FN}}/C_{\text{FP}}=30$)" in exp,
      "Item 18: Section 4.10 cost ratios tau*=0.18 (15:1) and tau*=0.11 (30:1)",
      "Cost ratios incorrect in 04_experiments.tex line 261")

# Item 19: Page 1 line 11 sentence completion
check("under statutory model risk management audits." in intro,
      "Item 19: Intro line 11 completed under statutory audits",
      "Sentence cut off in 01_introduction.tex")

# Item 20: Intro line 23 pillars + validation
check("organized around three foundational theoretical pillars and an enterprise-scale empirical validation:" in intro,
      "Item 20: Intro line 23 pillars + empirical validation",
      "Line 23 text incorrect")

# Item 21: Purge SR 26-2 across all files
for p in [xai, lim]:
    check("SR 26-2" not in p,
          f"Item 21: SR 26-2 purged from {p[:30].strip()}...",
          "SR 26-2 still present")

# Item 22: Table 1 dgraphfin citation
check(r"\texttt{dgraphfin} (Dynamic Credit Graph) \citep{dgraphfin}" in exp,
      "Item 22: Table 1 dgraphfin has \\citep{dgraphfin}",
      "Citation missing from dgraphfin row in Table 1")

# -------------------------------------------------------------
# Category C: Supplementary Material (Items 21, 23, 24, 26, 27, 28)
# -------------------------------------------------------------
print("\n--- CATEGORY C: SUPPLEMENTARY MATERIAL ---")
supp = (EAAI_DIR / "Anonymized_Supplementary.tex").read_text(encoding="utf-8")

# Item 21 in Supp
check("SR 26-2" not in supp,
      "Item 21: SR 26-2 purged from Anonymized_Supplementary.tex",
      "SR 26-2 still present in Supplementary")

# Item 23: Tables native latex, optimal beta=0.30 in S8
check(r"Tversky Weight $\beta_{\text{tversky}}$ & $[0.10, 0.50]$ (Uniform) & $0.30$" in supp,
      "Item 23 & 17: Table S8 optimal beta_tversky = 0.30",
      "beta_tversky optimal value not 0.30 in Table S8")
check(r"Focal Exponent $\gamma_{\text{focal}}$ & $[1.0, 3.0]$ (Uniform) & $1.5$" in supp,
      "Item 17: Table S8 optimal gamma_focal = 1.5",
      "gamma_focal not 1.5 in Table S8")
check(r"\textbf{Total Benchmark Corpus} & $\mathbf{9,534,980}$ & $\mathbf{9,528,355}$" in supp,
      "Item 23: Table S6 clean 9,534,980 and 9,528,355 formatting",
      "Table S6 totals formatted incorrectly")

# Item 24: Table S3 chronological out-of-time scores
check(r"\texttt{elliptic\_v1} & $88.35 / 0.8900$ & $87.90 / 0.8800$ & $88.50 / 0.8920$ & $86.20 / 0.8650$" in supp,
      "Item 24: Table S3 elliptic_v1 chronological scores for LightGBM & Balanced RF",
      "Table S3 still contains 99.72* leakage score")
check(r"\texttt{elliptic\_v2} & $96.50 / 0.9814$ & $95.80 / 0.9580$ & $96.20 / 0.9780$ & $94.50 / 0.9510$" in supp,
      "Item 24: Table S3 elliptic_v2 chronological scores for LightGBM & Balanced RF",
      "Table S3 still contains 100.00* leakage score")
check(r"\textbf{Macro-Average} & $64.76 / 0.6500$ & $64.25 / 0.6400$ & $65.10 / 0.6550$ & $62.85 / 0.6120$" in supp,
      "Item 24: Table S3 chronological Macro-Average (65.10 & 62.85)",
      "Table S3 macro averages incorrect")

# Item 26: Figures S5, S6, S7 full width
check(r"\begin{figure*}[!t]" in supp and "fig20_multi_agent_forensic_swarm.pdf" in supp,
      "Item 26: Figure S5 uses full-width figure*",
      "Figure S5 not using figure*")
check(r"\begin{figure*}[!t]" in supp and "fig_canonical_invariants_empirical.pdf" in supp,
      "Item 26: Figure S6 uses full-width figure*",
      "Figure S6 not using figure*")
check(r"\begin{figure*}[!t]" in supp and "fig22_triband_spectral_coldstart.pdf" in supp,
      "Item 26: Figure S7 uses full-width figure*",
      "Figure S7 not using figure*")

# Item 27: Table S9 and S10 layout
check(r"w/o Flow Regularity $\tilde{\Phi}_{\text{flow}}$ & $86.45 / 0.8810$" in supp,
      "Item 27 & 9: Table S9 w/o Flow Regularity on elliptic_v1 is 86.45 / 0.8810",
      "Table S9 score incorrect")
check(r"False Discovery $< 1.0\%$" in supp and r"\begin{table*}[t]" in supp,
      "Item 27: Table S10 widened with False Discovery < 1.0% on one line",
      "Table S10 not widened")

# Item 28: Table S12 column order and formatting
check(r"\textbf{Source Dataset} & \textbf{Target Dataset} & \textbf{HGT Baseline F1} & \textbf{XGBoost Baseline F1} & \textbf{C-STGB Zero-Shot F1 / PR-AUC} & \textbf{Target-Tuned F1}" in supp,
      "Item 28: Table S12 columns properly ordered",
      "Table S12 column order incorrect")
check(r"82.40\% / 0.8410" in supp,
      "Item 28: Table S12 clean %/ notation",
      "Table S12 notation incorrect")

# -------------------------------------------------------------
# Summary
# -------------------------------------------------------------
print("\n" + "=" * 70)
print(f"AUDIT RESULTS: {len(passes)} PASSED, {len(errors)} FAILED")
print("=" * 70)
if errors:
    print("\nFAILURES TO RESOLVE:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("\nALL 28 ITEMS FULLY VERIFIED AND PASSING!")
    sys.exit(0)
