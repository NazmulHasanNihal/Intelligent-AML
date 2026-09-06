# Intelligent-AML Paper Empirical Scorecard

Generated: `2026-09-04 08:37:34 UTC`  
Total Evaluated Model Runs: `182` across `14` Datasets

---

## Statistical Significance Summary (Wilcoxon Signed-Rank Tests)
| Baseline Architecture | Baseline Mean F1 | C-STGB Mean F1 | Uplift | p-value | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| XGBoost (Tabular) | 67.92% | 67.26% | +-0.66% | `0.6196` | p < 0.05 |
| GCN (Spatial) | 23.78% | 67.26% | +43.49% | `6.10e-05` | **p < 0.001 (***)** |
| EvolveGCN (Dynamic) | 18.94% | 67.26% | +48.32% | `6.10e-05` | **p < 0.001 (***)** |
| GraphSAGE (Inductive) | 24.31% | 67.26% | +42.95% | `6.10e-05` | **p < 0.001 (***)** |
| CatBoost (Industrial) | 67.14% | 67.26% | +0.13% | `0.1727` | p < 0.05 |

---

## LaTeX Source Files Available for Paper:
- `papers/IEEE_Research_Paper/tables/tab2_baseline_scorecard.tex`
- `papers/IEEE_Research_Paper/tables/tab_statistical_tests.tex`
