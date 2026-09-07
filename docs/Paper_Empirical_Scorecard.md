# Intelligent-AML Paper Empirical Scorecard

Generated: `2026-09-04 08:37:34 UTC`  
Total Evaluated Model Runs: `182` across `14` Datasets

---

## Statistical Significance Summary (Wilcoxon Signed-Rank Tests)
| Baseline Architecture | Baseline Mean F1 | C-STGB Mean F1 | Uplift | p-value (adj) | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: |
| XGBoost (Tabular) | 67.92% | 67.26% | -0.66% | `0.8077` | $p \ge 0.05$ (Parity / Not Significant) |
| GCN (Spatial) | 23.78% | 67.26% | +43.49% | `6.10e-04` | **$p < 0.001$ (***)** |
| EvolveGCN (Dynamic) | 18.94% | 67.26% | +48.32% | `6.10e-04` | **$p < 0.001$ (***)** |
| GraphSAGE (Inductive) | 24.31% | 67.26% | +42.95% | `6.10e-04` | **$p < 0.001$ (***)** |
| CatBoost (Industrial) | 67.14% | 67.26% | +0.13% | `0.4318` | $p \ge 0.05$ (Parity / Not Significant) |

---

## LaTeX Source Files Available for Paper:
- `papers/IEEE_Research_Paper/tables/tab2_baseline_scorecard.tex`
- `papers/IEEE_Research_Paper/tables/tab_statistical_tests.tex`
