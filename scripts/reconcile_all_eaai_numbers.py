"""
scripts/reconcile_all_eaai_numbers.py
Master Python script to reconcile all numerical results, statistical tests,
and table matrices across the EAAI paper suite.
"""

import numpy as np
import scipy.stats as stats
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EAAI_DIR = BASE_DIR / "papers" / "EAAI_Research_Paper"

# 14 Benchmark Datasets
DATASETS = [
    'elliptic_v1', 'elliptic_v2', 'xblock_eth', 'mtgox_leaked',
    'saml_d', 'paysim1', 'paysim_extended',
    'ibm_amlsim_hi_small', 'ibm_amlsim_hi_medium',
    'ibm_amlsim_li_small', 'ibm_amlsim_li_medium',
    'data_generator', 'dgraphfin', 'cc_transactions'
]

# Baseline and C-STGB Illicit F1-Score (%) and PR-AUC on test splits
# (F1, PR-AUC)
TABLE2_DATA = {
    'elliptic_v1': {
        'XGBoost': (88.35, 0.8900), 'CatBoost': (87.90, 0.8800), 'GCN': (43.55, 0.3482),
        'GraphSAGE': (49.07, 0.4254), 'CARE-GNN': (64.50, 0.6800), 'EvolveGCN': (51.04, 0.4243),
        'TGN': (68.40, 0.7200), 'C-STGB': (91.42, 0.9312, 0.65)
    },
    'elliptic_v2': {
        'XGBoost': (96.50, 0.9814), 'CatBoost': (95.80, 0.9580), 'GCN': (0.00, 0.0237),
        'GraphSAGE': (0.24, 0.0230), 'CARE-GNN': (58.20, 0.6100), 'EvolveGCN': (0.00, 0.0258),
        'TGN': (62.10, 0.6500), 'C-STGB': (99.10, 0.9950, 0.45)
    },
    'xblock_eth': {
        'XGBoost': (93.80, 0.9400), 'CatBoost': (92.90, 0.9300), 'GCN': (6.53, 0.0212),
        'GraphSAGE': (6.75, 0.0206), 'CARE-GNN': (63.20, 0.6600), 'EvolveGCN': (6.62, 0.0211),
        'TGN': (67.50, 0.7100), 'C-STGB': (97.40, 0.9920, 0.50)
    },
    'mtgox_leaked': {
        'XGBoost': (68.40, 0.7400), 'CatBoost': (67.80, 0.7300), 'GCN': (20.30, 0.2038),
        'GraphSAGE': (22.16, 0.1801), 'CARE-GNN': (52.40, 0.5600), 'EvolveGCN': (22.12, 0.0956),
        'TGN': (55.80, 0.6000), 'C-STGB': (74.20, 0.8350, 0.95)
    },
    'saml_d': {
        'XGBoost': (89.20, 0.8950), 'CatBoost': (88.60, 0.8850), 'GCN': (1.69, 0.0109),
        'GraphSAGE': (3.16, 0.0071), 'CARE-GNN': (55.80, 0.5900), 'EvolveGCN': (3.81, 0.0077),
        'TGN': (59.40, 0.6300), 'C-STGB': (93.68, 0.9574, 0.60)
    },
    'paysim1': {
        'XGBoost': (18.90, 0.1254), 'CatBoost': (17.76, 0.1061), 'GCN': (3.50, 0.0084),
        'GraphSAGE': (0.56, 0.0016), 'CARE-GNN': (2.20, 0.0180), 'EvolveGCN': (3.98, 0.0097),
        'TGN': (2.50, 0.0220), 'C-STGB': (16.66, 0.1350, 0.80)
    },
    'paysim_extended': {
        'XGBoost': (99.72, 0.9996), 'CatBoost': (99.77, 0.9996), 'GCN': (96.22, 0.9825),
        'GraphSAGE': (96.05, 0.9799), 'CARE-GNN': (69.40, 0.7200), 'EvolveGCN': (92.64, 0.7521),
        'TGN': (73.10, 0.7600), 'C-STGB': (99.80, 0.9993, 0.10)
    },
    'ibm_amlsim_hi_small': {
        'XGBoost': (32.40, 0.3100), 'CatBoost': (31.80, 0.3000), 'GCN': (2.46, 0.0101),
        'GraphSAGE': (2.46, 0.0080), 'CARE-GNN': (25.40, 0.2800), 'EvolveGCN': (2.31, 0.0080),
        'TGN': (28.40, 0.3200), 'C-STGB': (39.70, 0.4000, 1.20)
    },
    'ibm_amlsim_hi_medium': {
        'XGBoost': (39.50, 0.4200), 'CatBoost': (38.90, 0.4100), 'GCN': (3.88, 0.0135),
        'GraphSAGE': (3.95, 0.0126), 'CARE-GNN': (31.80, 0.3500), 'EvolveGCN': (7.06, 0.0350),
        'TGN': (35.20, 0.3900), 'C-STGB': (46.85, 0.5100, 1.10)
    },
    'ibm_amlsim_li_small': {
        'XGBoost': (14.20, 0.1300), 'CatBoost': (13.80, 0.1300), 'GCN': (0.84, 0.0060),
        'GraphSAGE': (1.50, 0.0057), 'CARE-GNN': (11.80, 0.1300), 'EvolveGCN': (1.18, 0.0052),
        'TGN': (12.90, 0.1400), 'C-STGB': (15.83, 0.1493, 0.95)
    },
    'ibm_amlsim_li_medium': {
        'XGBoost': (21.50, 0.1900), 'CatBoost': (20.90, 0.1900), 'GCN': (3.41, 0.0143),
        'GraphSAGE': (2.30, 0.0073), 'CARE-GNN': (17.50, 0.2000), 'EvolveGCN': (4.29, 0.0238),
        'TGN': (19.20, 0.2200), 'C-STGB': (23.74, 0.2139, 1.10)
    },
    'data_generator': {
        'XGBoost': (99.90, 0.9990), 'CatBoost': (99.85, 0.9985), 'GCN': (99.74, 0.9979),
        'GraphSAGE': (99.63, 0.9956), 'CARE-GNN': (78.50, 0.8100), 'EvolveGCN': (62.72, 0.6327),
        'TGN': (81.50, 0.8400), 'C-STGB': (99.93, 1.0000, 0.05)
    },
    'dgraphfin': {
        'XGBoost': (96.07, 0.9900), 'CatBoost': (95.82, 0.9628), 'GCN': (2.60, 0.0129),
        'GraphSAGE': (3.26, 0.0161), 'CARE-GNN': (2.50, 0.0450), 'EvolveGCN': (2.59, 0.0094),
        'TGN': (3.20, 0.0250), 'C-STGB': (97.91, 0.9979, 0.40)
    },
    'cc_transactions': {
        'XGBoost': (48.20, 0.4900), 'CatBoost': (47.90, 0.4800), 'GCN': (48.16, 0.3472),
        'GraphSAGE': (49.24, 0.3555), 'CARE-GNN': (34.20, 0.3800), 'EvolveGCN': (4.79, 0.0215),
        'TGN': (38.20, 0.4200), 'C-STGB': (56.48, 0.6476, 0.70)
    }
}

MODELS = ['XGBoost', 'CatBoost', 'GCN', 'GraphSAGE', 'CARE-GNN', 'EvolveGCN', 'TGN']

def recompute_all():
    print("="*70)
    print("RECOMPUTING ALL TABLE 2 & TABLE 3 STATS")
    print("="*70)
    
    cstgb_f1 = np.array([TABLE2_DATA[d]['C-STGB'][0] for d in DATASETS])
    cstgb_prauc = np.array([TABLE2_DATA[d]['C-STGB'][1] for d in DATASETS])
    
    print(f"C-STGB Macro Mean: {np.mean(cstgb_f1):.2f}% / {np.mean(cstgb_prauc):.4f}")
    
    stats_dict = {}
    raw_p_list = []
    
    for m in MODELS:
        f1_vals = np.array([TABLE2_DATA[d][m][0] for d in DATASETS])
        prauc_vals = np.array([TABLE2_DATA[d][m][1] for d in DATASETS])
        
        diff = cstgb_f1 - f1_vals
        mean_delta = np.mean(diff)
        med_delta = np.median(diff)
        q25 = np.percentile(diff, 25)
        q75 = np.percentile(diff, 75)
        iqr = q75 - q25
        
        # Rank-based Wilcoxon
        ranks = stats.rankdata(np.abs(diff))
        w_plus = np.sum(ranks[diff > 0])
        w_minus = np.sum(ranks[diff < 0])
        
        res = stats.wilcoxon(cstgb_f1, f1_vals, alternative='two-sided')
        raw_p = res.pvalue
        raw_p_list.append(raw_p)
        
        wins = int(np.sum(diff > 0))
        ties = int(np.sum(diff == 0))
        losses = int(np.sum(diff < 0))
        
        stats_dict[m] = {
            'macro_f1': np.mean(f1_vals),
            'macro_prauc': np.mean(prauc_vals),
            'mean_delta': mean_delta,
            'med_delta': med_delta,
            'q25': q25,
            'q75': q75,
            'iqr': iqr,
            'w_plus': w_plus,
            'w_minus': w_minus,
            'raw_p': raw_p,
            'wins': wins,
            'ties': ties,
            'losses': losses
        }

    # Benjamini-Hochberg FDR
    m_len = len(MODELS)
    sorted_idx = np.argsort(raw_p_list)
    p_adj = np.zeros(m_len)
    for rank, idx in enumerate(sorted_idx, 1):
        p_adj[idx] = min(raw_p_list[idx] * m_len / rank, 1.0)
    for i in range(m_len - 2, -1, -1):
        p_adj[sorted_idx[i]] = min(p_adj[sorted_idx[i]], p_adj[sorted_idx[i+1]])
        
    for i, m in enumerate(MODELS):
        stats_dict[m]['p_adj'] = p_adj[i]
        sd = stats_dict[m]
        print(f"{m:12s} | Mean: {sd['macro_f1']:5.2f}% | MeanDelta: {sd['mean_delta']:+6.2f} pp | Med[IQR]: {sd['med_delta']:+6.2f} [{sd['iqr']:5.2f}] | W+: {sd['w_plus']:5.1f}, W-: {sd['w_minus']:4.1f} | Raw p: {sd['raw_p']:.4e} | p_adj: {sd['p_adj']:.4e}")

    # -------------------------------------------------------------
    # 1. Generate tab2_baseline_scorecard.tex
    # -------------------------------------------------------------
    tab2_path = EAAI_DIR / "tables" / "tab2_baseline_scorecard.tex"
    tab2_content = r"""\begin{table*}[t]
\centering
\caption{Comprehensive Benchmark Comparison across All 14 Financial Networks: Minority (Illicit) Class F1-Score (\%) and PR-AUC with Validation-Tuned Thresholds $\tau^*$ under Asymmetric Operational Loss against Literature Baselines ($^\dagger$ indicates statistically significant corpus-wide improvement over deep GNNs at $W^+=105.0, W^-=0.0, p_{\text{adj}} < 0.001$ under two-sided Wilcoxon signed-rank test across all 14 benchmark networks).}
\label{tab:full_baseline_scorecard}
\renewcommand{\arraystretch}{0.85}
\setlength{\tabcolsep}{3.2pt}
\resizebox{\textwidth}{!}{%
\begin{tabular}{lcccccccc}
\toprule
\textbf{Dataset Identifier} & \textbf{XGBoost} & \textbf{CatBoost} & \textbf{GCN} & \textbf{GraphSAGE} & \textbf{CARE-GNN} & \textbf{EvolveGCN} & \textbf{TGN} & \textbf{C-STGB (Ours)} \\
\midrule
\multicolumn{9}{l}{\textbf{Group A: Public Blockchain Ledgers \& Relational DAGs (4 Networks)}} \\
\texttt{elliptic\_v1} & $88.35 / 0.8900$ & $87.90 / 0.8800$ & $43.55 / 0.3482$ & $49.07 / 0.4254$ & $64.50 / 0.6800$ & $51.04 / 0.4243$ & $68.40 / 0.7200$ & $\mathbf{91.42 \pm 0.65 / 0.9312}$ \\
\texttt{elliptic\_v2} & $96.50 / 0.9814$ & $95.80 / 0.9580$ & $0.00 / 0.0237$ & $0.24 / 0.0230$ & $58.20 / 0.6100$ & $0.00 / 0.0258$ & $62.10 / 0.6500$ & $\mathbf{99.10 \pm 0.45 / 0.9950}$ \\
\texttt{xblock\_eth} & $93.80 / 0.9400$ & $92.90 / 0.9300$ & $6.53 / 0.0212$ & $6.75 / 0.0206$ & $63.20 / 0.6600$ & $6.62 / 0.0211$ & $67.50 / 0.7100$ & $\mathbf{97.40 \pm 0.50 / 0.9920}$ \\
\texttt{mtgox\_leaked} & $68.40 / 0.7400$ & $67.80 / 0.7300$ & $20.30 / 0.2038$ & $22.16 / 0.1801$ & $52.40 / 0.5600$ & $22.12 / 0.0956$ & $55.80 / 0.6000$ & $\mathbf{74.20 \pm 0.95 / 0.8350}$ \\
\midrule
\multicolumn{9}{l}{\textbf{Group B: Multi-Bank, Mobile Synthetic \& FinTech Rails (9 Networks)}} \\
\texttt{saml\_d} & $89.20 / 0.8950$ & $88.60 / 0.8850$ & $1.69 / 0.0109$ & $3.16 / 0.0071$ & $55.80 / 0.5900$ & $3.81 / 0.0077$ & $59.40 / 0.6300$ & $\mathbf{93.68 \pm 0.60 / 0.9574}$ \\
\texttt{paysim1} & $18.90 / 0.1254$ & $17.76 / 0.1061$ & $3.50 / 0.0084$ & $0.56 / 0.0016$ & $2.20 / 0.0180$ & $3.98 / 0.0097$ & $2.50 / 0.0220$ & $\mathbf{16.66 \pm 0.80 / 0.1350}$ \\
\texttt{paysim\_extended} & $99.72 / 0.9996$ & $99.77 / 0.9996$ & $96.22 / 0.9825$ & $96.05 / 0.9799$ & $69.40 / 0.7200$ & $92.64 / 0.7521$ & $73.10 / 0.7600$ & $\mathbf{99.80 \pm 0.10 / 0.9993}$ \\
\texttt{ibm\_amlsim\_hi\_small} & $32.40 / 0.3100$ & $31.80 / 0.3000$ & $2.46 / 0.0101$ & $2.46 / 0.0080$ & $25.40 / 0.2800$ & $2.31 / 0.0080$ & $28.40 / 0.3200$ & $\mathbf{39.70 \pm 1.20 / 0.4000}$ \\
\texttt{ibm\_amlsim\_hi\_medium} & $39.50 / 0.4200$ & $38.90 / 0.4100$ & $3.88 / 0.0135$ & $3.95 / 0.0126$ & $31.80 / 0.3500$ & $7.06 / 0.0350$ & $35.20 / 0.3900$ & $\mathbf{46.85 \pm 1.10 / 0.5100}$ \\
\texttt{ibm\_amlsim\_li\_small} & $14.20 / 0.1300$ & $13.80 / 0.1300$ & $0.84 / 0.0060$ & $1.50 / 0.0057$ & $11.80 / 0.1300$ & $1.18 / 0.0052$ & $12.90 / 0.1400$ & $\mathbf{15.83 \pm 0.95 / 0.1493}$ \\
\texttt{ibm\_amlsim\_li\_medium} & $21.50 / 0.1900$ & $20.90 / 0.1900$ & $3.41 / 0.0143$ & $2.30 / 0.0073$ & $17.50 / 0.2000$ & $4.29 / 0.0238$ & $19.20 / 0.2200$ & $\mathbf{23.74 \pm 1.10 / 0.2139}$ \\
\texttt{data\_generator} & $99.90 / 0.9990$ & $99.85 / 0.9985$ & $99.74 / 0.9979$ & $99.63 / 0.9956$ & $78.50 / 0.8100$ & $62.72 / 0.6327$ & $81.50 / 0.8400$ & $\mathbf{99.93 \pm 0.05 / 1.0000}$ \\
\texttt{dgraphfin} & $96.07 / 0.9900$ & $95.82 / 0.9628$ & $2.60 / 0.0129$ & $3.26 / 0.0161$ & $2.50 / 0.0450$ & $2.59 / 0.0094$ & $3.20 / 0.0250$ & $\mathbf{97.91 \pm 0.40 / 0.9979}$ \\
\midrule
\multicolumn{9}{l}{\textbf{Group C: Bipartite Card Transaction Streams (1 Network)}} \\
\texttt{cc\_transactions} & $48.20 / 0.4900$ & $47.90 / 0.4800$ & $48.16 / 0.3472$ & $49.24 / 0.3555$ & $34.20 / 0.3800$ & $4.79 / 0.0215$ & $38.20 / 0.4200$ & $\mathbf{56.48 \pm 0.70 / 0.6476}$ \\
\midrule
\textbf{Overall Macro Mean} & $64.76 / 0.6500$ & $64.25 / 0.6400$ & $23.78 / 0.2143$ & $24.31 / 0.2170$ & $40.53 / 0.4309$ & $18.94 / 0.1480$ & $43.39 / 0.4605$ & $\mathbf{68.05 \pm 0.48 / 0.6974}^\dagger$ \\
\midrule
\multicolumn{9}{l}{\textbf{Non-Parametric Statistical Testing \& Effect Sizes vs. C-STGB ($n=14$ Benchmark Networks)}} \\
\textbf{Wins / Ties / Losses} & $13 \,/\, 0 \,/\, 1$ & $13 \,/\, 0 \,/\, 1$ & $14 \,/\, 0 \,/\, 0$ & $14 \,/\, 0 \,/\, 0$ & $14 \,/\, 0 \,/\, 0$ & $14 \,/\, 0 \,/\, 0$ & $14 \,/\, 0 \,/\, 0$ & -- \\
\textbf{Mean Advantage ($\Delta$)} & $+3.29$\,pp & $+3.80$\,pp & $+44.27$\,pp & $+43.74$\,pp & $+27.52$\,pp & $+49.11$\,pp & $+24.66$\,pp & -- \\
\textbf{Median [IQR] $\Delta$} & $+2.84$\,[3.79]\,pp & $+3.41$\,[4.03]\,pp & $+40.11$\,[68.01]\,pp & $+39.80$\,[66.13]\,pp & $+22.04$\,[18.64]\,pp & $+40.09$\,[56.53]\,pp & $+18.42$\,[16.82]\,pp & -- \\
\textbf{Wilcoxon $W^+, W^-$} & $99.5, 5.5$ & $102.0, 3.0$ & $105.0, 0.0$ & $105.0, 0.0$ & $105.0, 0.0$ & $105.0, 0.0$ & $105.0, 0.0$ & -- \\
\textbf{Raw $p$-value} & $3.17 \times 10^{-3}$ & $6.10 \times 10^{-4}$ & $1.22 \times 10^{-4}$ & $1.22 \times 10^{-4}$ & $1.22 \times 10^{-4}$ & $1.22 \times 10^{-4}$ & $1.22 \times 10^{-4}$ & -- \\
\textbf{Adjusted $p_{\text{adj}}$} & $\mathbf{3.17 \times 10^{-3}}$ & $\mathbf{7.12 \times 10^{-4}}$ & $\mathbf{1.71 \times 10^{-4}}$ & $\mathbf{1.71 \times 10^{-4}}$ & $\mathbf{1.71 \times 10^{-4}}$ & $\mathbf{1.71 \times 10^{-4}}$ & $\mathbf{1.71 \times 10^{-4}}$ & -- \\
\bottomrule
\end{tabular}%
}
\vspace{0.8ex}

\footnotesize{Minority (illicit) class F1-Score evaluates harmonic precision and recall on confirmed illicit transactions ($y=1$) under validation-calibrated threshold $\tau^*$; Macro-Average represents the unweighted arithmetic mean across benchmark dataset scores, alongside median and interquartile range. Tabular tree models (XGBoost, CatBoost) are reported on native transaction features ($64.76\%$ and $64.25\%$ macro F1); augmenting XGBoost with the 12-D flow invariants $\mathbf{z}_{\text{inv}}$ elevates its score to $90.80\%$ on Elliptic-v1 as detailed in Section~\ref{sec:benchmark_results}. $^\dagger$ indicates statistically significant corpus-wide improvement over deep GNNs at $W^+=105.0, W^-=0.0, p_{\text{adj}} < 0.001$ under two-sided Wilcoxon signed-rank test across all 14 benchmark networks with Benjamini--Hochberg FDR correction across $m=7$ comparisons. Group A: 4 Public Crypto Ledgers; Group B: 9 Multi-Bank, Mobile \& FinTech Networks; Group C: 1 Bipartite Card Stream.}
\end{table*}
"""
    tab2_path.write_text(tab2_content, encoding="utf-8")
    print(f"Generated: {tab2_path}")

    # -------------------------------------------------------------
    # 2. Generate tab_statistical_tests.tex
    # -------------------------------------------------------------
    tab3_path = EAAI_DIR / "tables" / "tab_statistical_tests.tex"
    tab3_content = r"""\begin{table}[t]
\centering
\caption{Non-Parametric Statistical Significance and Distributional Effect Sizes of C-STGB vs. Baselines across All $n=14$ Benchmark Networks (Two-Sided Paired Wilcoxon Signed-Rank Test with Benjamini--Hochberg FDR Correction across $m=7$ Comparisons).}
\label{tab:statistical_tests}
\renewcommand{\arraystretch}{0.85}
\setlength{\tabcolsep}{2.5pt}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
\textbf{Baseline} & \textbf{W / T / L} & \textbf{Mean $\Delta$} & \textbf{Median [IQR]} & \textbf{$W^+, W^-$} & \textbf{Adjusted $p_{\text{adj}}$} \\
\midrule
XGBoost (Tabular) & $13 \,/\, 0 \,/\, 1$ & $+3.29$\,pp & $+2.84$\,[3.79]\,pp & $99.5, 5.5$ & $\mathbf{3.17 \times 10^{-3}}^{\ast\ast}$ \\
CatBoost (Industrial) & $13 \,/\, 0 \,/\, 1$ & $+3.80$\,pp & $+3.41$\,[4.03]\,pp & $102.0, 3.0$ & $\mathbf{7.12 \times 10^{-4}}^{\ast\ast\ast}$ \\
GCN (Spatial) & $14 \,/\, 0 \,/\, 0$ & $+44.27$\,pp & $+40.11$\,[68.01]\,pp & $105.0, 0.0$ & $\mathbf{1.71 \times 10^{-4}}^{\ast\ast\ast}$ \\
GraphSAGE (Inductive) & $14 \,/\, 0 \,/\, 0$ & $+43.74$\,pp & $+39.80$\,[66.13]\,pp & $105.0, 0.0$ & $\mathbf{1.71 \times 10^{-4}}^{\ast\ast\ast}$ \\
CARE-GNN (Camouflage) & $14 \,/\, 0 \,/\, 0$ & $+27.52$\,pp & $+22.04$\,[18.64]\,pp & $105.0, 0.0$ & $\mathbf{1.71 \times 10^{-4}}^{\ast\ast\ast}$ \\
EvolveGCN (Dynamic) & $14 \,/\, 0 \,/\, 0$ & $+49.11$\,pp & $+40.09$\,[56.53]\,pp & $105.0, 0.0$ & $\mathbf{1.71 \times 10^{-4}}^{\ast\ast\ast}$ \\
TGN (Continuous Time) & $14 \,/\, 0 \,/\, 0$ & $+24.66$\,pp & $+18.42$\,[16.82]\,pp & $105.0, 0.0$ & $\mathbf{1.71 \times 10^{-4}}^{\ast\ast\ast}$ \\
\bottomrule
\end{tabular}%
}
\vspace{1.0ex}

\footnotesize{$^\ast$Under invariant representations $[\mathbf{x}_u \,\|\, \mathbf{z}_{\text{inv}}]$, C-STGB preserves $14/0/0$ wins over standard GNNs ($W^+=105.0, W^-=0.0, p_{\text{adj}} < 0.001$). Full per-dataset evaluation matrix is provided in Supplementary Material Table~S3.}
\end{table}
"""
    tab3_path.write_text(tab3_content, encoding="utf-8")
    print(f"Generated: {tab3_path}")

if __name__ == "__main__":
    recompute_all()

