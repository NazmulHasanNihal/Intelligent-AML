# Master Live Multi-Dataset Multi-Split AML Benchmark Report
**Generated / Updated:** `2026-08-21 16:34:19 UTC`  
**Standard:** IEEE Transactions on Information Forensics and Security (TIFS) / Fed SR 11-7 / Basel III  
**Total Model Trials Completed:** `43 runs` across `4 datasets`

---

## 1. Master Benchmark Scorecard (All Recorded Trials)

| Timestamp | Dataset | Model | Split | Epochs | F1-Score | Recall | Precision | F2-Score | PR-AUC | ROC-AUC | TPR@0.1%FPR | Accuracy | Train Time (s) | Latency (ms) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2026-08-21 16:01:23 | `elliptic_v1` | Proposed C-STGB | `70_30` | 10 | **0.9881** | 0.9766 | 1.0000 | 0.9812 | 0.9990 | 0.9999 | 0.9967 | 0.9986 | 136.09s | 0.0231ms |
| 2026-08-21 16:01:25 | `elliptic_v1` | Tabular XGBoost | `70_30` | 10 | 0.9983 | 1.0000 | 0.9967 | 0.9993 | 0.9999 | 1.0000 | 1.0000 | 0.9998 | 0.73s | 0.0007ms |
| 2026-08-21 16:01:26 | `elliptic_v1` | Industrial LightGBM | `70_30` | 10 | 0.9961 | 0.9989 | 0.9933 | 0.9978 | 0.9999 | 1.0000 | 1.0000 | 0.9995 | 0.73s | 0.0010ms |
| 2026-08-21 16:01:30 | `elliptic_v1` | Industrial CatBoost | `70_30` | 10 | 0.9961 | 1.0000 | 0.9922 | 0.9984 | 0.9999 | 1.0000 | 1.0000 | 0.9995 | 3.06s | 0.0009ms |
| 2026-08-21 16:01:33 | `elliptic_v1` | Balanced Random Forest | `70_30` | 10 | 0.9867 | 0.9900 | 0.9834 | 0.9886 | 0.9972 | 0.9997 | 0.9888 | 0.9984 | 2.07s | 0.0035ms |
| 2026-08-21 16:01:35 | `elliptic_v1` | Topological Logistic Reg | `70_30` | 10 | 0.4982 | 0.4676 | 0.5331 | 0.4794 | 0.3647 | 0.8966 | 0.0112 | 0.9439 | 0.92s | 0.0005ms |
| 2026-08-21 16:01:37 | `elliptic_v1` | Isolation Forest (Unsupervised) | `70_30` | 10 | 0.1119 | 0.9955 | 0.0593 | 0.2394 | 0.0333 | 0.1786 | 0.0000 | 0.0595 | 1.76s | 0.0066ms |
| 2026-08-21 16:01:48 | `elliptic_v1` | Deep Autoencoder (Reconstruction) | `70_30` | 10 | 0.0022 | 0.0011 | 0.0526 | 0.0014 | 0.0354 | 0.2195 | 0.0000 | 0.9394 | 10.56s | 0.0009ms |
| 2026-08-21 16:02:02 | `elliptic_v1` | Homogeneous GCN | `70_30` | 10 | 0.3872 | 0.5112 | 0.3116 | 0.4531 | 0.2283 | 0.7906 | 0.0011 | 0.9037 | 12.68s | 0.0046ms |
| 2026-08-21 16:02:16 | `elliptic_v1` | Inductive GraphSAGE | `70_30` | 10 | 0.3978 | 0.4866 | 0.3364 | 0.4467 | 0.3182 | 0.8135 | 0.0424 | 0.9123 | 12.63s | 0.0039ms |
| 2026-08-21 16:02:28 | `elliptic_v1` | Standard GAT | `70_30` | 10 | 0.3167 | 0.6373 | 0.2107 | 0.4536 | 0.1739 | 0.8240 | 0.0045 | 0.8363 | 10.69s | 0.0055ms |
| 2026-08-21 16:02:43 | `elliptic_v1` | GIN (Graph Isomorphism) | `70_30` | 10 | 0.5748 | 0.5212 | 0.6406 | 0.5414 | 0.5741 | 0.8606 | 0.2054 | 0.9541 | 14.72s | 0.0046ms |
| 2026-08-21 16:03:00 | `elliptic_v1` | EvolveGCN (Dynamic GNN) | `70_30` | 10 | 0.3253 | 0.4766 | 0.2470 | 0.4018 | 0.1679 | 0.7868 | 0.0000 | 0.8824 | 15.99s | 0.0043ms |
| 2026-08-21 16:10:29 | `elliptic_v2` | Proposed C-STGB | `70_30` | 10 | **0.9997** | 1.0000 | 0.9994 | 0.9999 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 423.20s | 0.0207ms |
| 2026-08-21 16:10:33 | `elliptic_v2` | Tabular XGBoost | `70_30` | 10 | 0.9986 | 0.9972 | 1.0000 | 0.9978 | 0.9983 | 0.9995 | 0.9972 | 0.9999 | 1.31s | 0.0004ms |
| 2026-08-21 16:10:36 | `elliptic_v2` | Industrial LightGBM | `70_30` | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.79s | 0.0007ms |
| 2026-08-21 16:10:47 | `elliptic_v2` | Industrial CatBoost | `70_30` | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 9.23s | 0.0003ms |
| 2026-08-21 16:10:57 | `elliptic_v2` | Balanced Random Forest | `70_30` | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 7.49s | 0.0015ms |
| 2026-08-21 16:11:05 | `elliptic_v2` | Topological Logistic Reg | `70_30` | 10 | 0.1373 | 0.1158 | 0.1686 | 0.1236 | 0.0780 | 0.6930 | 0.0206 | 0.9650 | 5.38s | 0.0002ms |
| 2026-08-21 16:11:11 | `elliptic_v2` | Isolation Forest (Unsupervised) | `70_30` | 10 | 0.0852 | 0.4992 | 0.0466 | 0.1695 | 0.0436 | 0.7239 | 0.0012 | 0.7424 | 3.43s | 0.0057ms |
| 2026-08-21 16:12:56 | `elliptic_v2` | Deep Autoencoder (Reconstruction) | `70_30` | 10 | 0.0234 | 0.0240 | 0.0227 | 0.0238 | 0.0262 | 0.5197 | 0.0025 | 0.9517 | 103.15s | 0.0004ms |
| 2026-08-21 16:13:26 | `elliptic_v2` | Homogeneous GCN | `70_30` | 10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0241 | 0.5053 | 0.0000 | 0.9760 | 27.56s | 0.0038ms |
| 2026-08-21 16:13:55 | `elliptic_v2` | Inductive GraphSAGE | `70_30` | 10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0232 | 0.4992 | 0.0003 | 0.9760 | 26.17s | 0.0033ms |
| 2026-08-21 16:14:21 | `elliptic_v2` | Standard GAT | `70_30` | 10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0233 | 0.4949 | 0.0003 | 0.9760 | 23.73s | 0.0054ms |
| 2026-08-21 16:14:55 | `elliptic_v2` | GIN (Graph Isomorphism) | `70_30` | 10 | 0.0489 | 0.6150 | 0.0254 | 0.1092 | 0.0247 | 0.5145 | 0.0006 | 0.4251 | 30.56s | 0.0045ms |
| 2026-08-21 16:15:33 | `elliptic_v2` | EvolveGCN (Dynamic GNN) | `70_30` | 10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0241 | 0.5123 | 0.0000 | 0.9760 | 35.93s | 0.0037ms |
| 2026-08-21 16:21:22 | `ibm_amlsim_hi_small` | Proposed C-STGB | `70_30` | 10 | **0.1375** | 0.2814 | 0.0910 | 0.1984 | 0.0854 | 0.8525 | 0.0244 | 0.9560 | 345.00s | 0.0178ms |
| 2026-08-21 16:21:26 | `ibm_amlsim_hi_small` | Tabular XGBoost | `70_30` | 10 | 0.1487 | 0.1952 | 0.1201 | 0.1735 | 0.0978 | 0.8556 | 0.0312 | 0.9721 | 1.27s | 0.0003ms |
| 2026-08-21 16:21:29 | `ibm_amlsim_hi_small` | Industrial LightGBM | `70_30` | 10 | 0.1459 | 0.2939 | 0.0971 | 0.2091 | 0.0952 | 0.8519 | 0.0317 | 0.9571 | 0.69s | 0.0010ms |
| 2026-08-21 16:21:42 | `ibm_amlsim_hi_small` | Industrial CatBoost | `70_30` | 10 | 0.1520 | 0.2804 | 0.1042 | 0.2095 | 0.0919 | 0.8535 | 0.0270 | 0.9610 | 10.15s | 0.0001ms |
| 2026-08-21 16:21:52 | `ibm_amlsim_hi_small` | Balanced Random Forest | `70_30` | 10 | 0.1336 | 0.2040 | 0.0993 | 0.1685 | 0.0786 | 0.8374 | 0.0270 | 0.9670 | 7.92s | 0.0014ms |
| 2026-08-21 16:21:56 | `ibm_amlsim_hi_small` | Topological Logistic Reg | `70_30` | 10 | 0.1102 | 0.1127 | 0.1079 | 0.1117 | 0.0605 | 0.7810 | 0.0187 | 0.9773 | 0.85s | 0.0001ms |
| 2026-08-21 16:22:02 | `ibm_amlsim_hi_small` | Isolation Forest (Unsupervised) | `70_30` | 10 | 0.0463 | 0.3022 | 0.0251 | 0.0942 | 0.0287 | 0.6989 | 0.0104 | 0.8450 | 3.53s | 0.0051ms |
| 2026-08-21 16:24:02 | `ibm_amlsim_hi_small` | Deep Autoencoder (Reconstruction) | `70_30` | 10 | 0.0164 | 0.0083 | 0.7619 | 0.0104 | 0.0375 | 0.7291 | 0.0177 | 0.9876 | 117.90s | 0.0004ms |
| 2026-08-21 16:24:13 | `ibm_amlsim_hi_small` | Homogeneous GCN | `70_30` | 10 | 0.0398 | 0.0670 | 0.0283 | 0.0526 | 0.0148 | 0.4659 | 0.0042 | 0.9597 | 7.77s | 0.0010ms |
| 2026-08-21 16:24:23 | `ibm_amlsim_hi_small` | Inductive GraphSAGE | `70_30` | 10 | 0.0246 | 1.0000 | 0.0125 | 0.0594 | 0.0136 | 0.3120 | 0.0000 | 0.0125 | 7.62s | 0.0011ms |
| 2026-08-21 16:24:30 | `ibm_amlsim_hi_small` | Standard GAT | `70_30` | 10 | 0.0259 | 0.0602 | 0.0165 | 0.0393 | 0.0147 | 0.4326 | 0.0062 | 0.9435 | 4.98s | 0.0009ms |
| 2026-08-21 16:24:42 | `ibm_amlsim_hi_small` | GIN (Graph Isomorphism) | `70_30` | 10 | 0.0365 | 0.6942 | 0.0187 | 0.0845 | 0.0176 | 0.6381 | 0.0026 | 0.5427 | 8.87s | 0.0012ms |
| 2026-08-21 16:24:54 | `ibm_amlsim_hi_small` | EvolveGCN (Dynamic GNN) | `70_30` | 10 | 0.0347 | 0.7918 | 0.0177 | 0.0813 | 0.0207 | 0.6211 | 0.0047 | 0.4502 | 9.45s | 0.0013ms |
| 2026-08-21 16:33:52 | `ibm_amlsim_li_small` | Proposed C-STGB | `70_30` | 10 | **0.0758** | 0.2829 | 0.0438 | 0.1352 | 0.0342 | 0.8287 | 0.0106 | 0.9477 | 456.57s | 0.0193ms |
| 2026-08-21 16:33:58 | `ibm_amlsim_li_small` | Tabular XGBoost | `70_30` | 10 | 0.0996 | 0.2062 | 0.0657 | 0.1444 | 0.0469 | 0.8375 | 0.0199 | 0.9717 | 1.90s | 0.0003ms |
| 2026-08-21 16:34:02 | `ibm_amlsim_li_small` | Industrial LightGBM | `70_30` | 10 | 0.0935 | 0.1931 | 0.0617 | 0.1354 | 0.0419 | 0.8313 | 0.0174 | 0.9716 | 0.91s | 0.0013ms |
| 2026-08-21 16:34:19 | `ibm_amlsim_li_small` | Industrial CatBoost | `70_30` | 10 | 0.0969 | 0.1713 | 0.0676 | 0.1311 | 0.0475 | 0.8405 | 0.0162 | 0.9758 | 13.90s | 0.0001ms |

---

## 2. Dataset-by-Dataset SOTA Summary

### Dataset: `elliptic_v1`
- **Total Nodes:** 203,769 | **Total Edges:** 234,355 | **Illicit Ratio:** 9.76%
- **Top Performing Model:** `Tabular XGBoost` on Split `70_30` (Epochs=10)
- **Best F1-Score:** `0.9983` | **Recall:** `1.0000` | **Precision:** `0.9967` | **PR-AUC:** `0.9999`

### Dataset: `elliptic_v2`
- **Total Nodes:** 444,521 | **Total Edges:** 367,137 | **Illicit Ratio:** 2.35%
- **Top Performing Model:** `Industrial LightGBM` on Split `70_30` (Epochs=10)
- **Best F1-Score:** `1.0000` | **Recall:** `1.0000` | **Precision:** `1.0000` | **PR-AUC:** `1.0000`

### Dataset: `ibm_amlsim_hi_small`
- **Total Nodes:** 515,080 | **Total Edges:** 5,078,345 | **Illicit Ratio:** 1.23%
- **Top Performing Model:** `Industrial CatBoost` on Split `70_30` (Epochs=10)
- **Best F1-Score:** `0.1520` | **Recall:** `0.2804` | **Precision:** `0.1042` | **PR-AUC:** `0.0919`

### Dataset: `ibm_amlsim_li_small`
- **Total Nodes:** 705,903 | **Total Edges:** 6,924,049 | **Illicit Ratio:** 0.75%
- **Top Performing Model:** `Tabular XGBoost` on Split `70_30` (Epochs=10)
- **Best F1-Score:** `0.0996` | **Recall:** `0.2062` | **Precision:** `0.0657` | **PR-AUC:** `0.0469`

