# 🔬 Comparing Models: AML Benchmark Suite & Model Evaluation

This directory contains modular implementations of standard research literature baselines for Anti-Money Laundering (AML) transaction and account classification, designed to benchmark against our master proposed algorithm: **`C-STGB` (Conformal Spatio-Temporal GraphBoost Classifier)**.

---

## 📚 Literature Models Implemented

| Model Name | Paper Reference & Source | Core Mechanism |
| :--- | :--- | :--- |
| **`Proposed C-STGB`** | **Our Thesis Master Model** | Continuous-Time Burst-Aware HGT + Ego-Neighborhood Pooling ($\bar{z}_{\mathcal{N}(u)}, \Delta z_u$) + Class-Balanced XGBoost + Conformal Risk Gate ($\alpha=0.10, \tau^*$). |
| **`Tabular XGBoost`** | Industry Standard Baseline | Gradient boosted decision trees on raw node/transaction tabular features. |
| **`Network + LR`** | Classical Graph Baseline | Logistic regression on tabular node features combined with in/out degree topological properties. |
| **`Homogeneous GCN`** | Weber et al. (2019) / Kipf & Welling (2017) | 3-layer spectral graph convolution over flattened homogeneous topology. |
| **`GraphSAGE`** | Hamilton et al. (2017) | Inductive spatial neighborhood aggregation with mean pooling. |
| **`Standard GAT`** | Velickovic et al. (2018) | Multi-head attention over heterogeneous edge relations without continuous decay. |
| **`GIN`** | Xu et al. (2019) / Custom Edge GIN (2025) | Graph Isomorphism Network with MLP multi-layer sum aggregation. |
| **`EvolveGCN`** | Pareja et al. (2020) | Dynamic recurrent graph neural network combining GCN convolutions with GRU weight evolution. |
| **`GCN-GRU`** | Spatiotemporal Baseline | Spatial GCN encoder concatenated with delta-t/burst-score projections and fused via GRU. |

---

## 🚀 How to Run Comparisons Locally on Your PC

### 1. Run Complete Comparison Suite on Elliptic:
```bash
python -m comparing_models.compare_all --dataset elliptic_v1 --epochs 30
```

### 2. Run Comparison on Other Ingested Datasets:
```bash
# High-Imbalance Synthetic IBM Dataset
python -m comparing_models.compare_all --dataset ibm_amlsim_hi_small --epochs 30

# Multi-Million Node PaySim Dataset
python -m comparing_models.compare_all --dataset paysim1 --epochs 15
```

### 3. Generated Artifacts & Visualizations:
Running the comparison generates the following in `data/outputs/comparisons/`:
* `[dataset]_metrics.csv` — Full quantitative metrics table (Accuracy, Precision, Recall, F1, F2, PR-AUC, TPR@0.1%FPR, Latency, Peak Memory).
* `[dataset]_pr_roc.png` — High-resolution Precision-Recall and ROC curves comparing all models.
* `[dataset]_metric_bars.html` — Interactive Plotly comparison bar chart across F1, F2, Precision, and Recall.

---

## 🛠️ Python API Integration

You can easily import and compare any baseline in Python:

```python
from comparing_models.base_models import HomogeneousGCN, GraphSAGEBaseline, TabularXGBoost
from comparing_models.evaluator import evaluate_model_performance
from comparing_models.visualizer import plot_pr_roc_curves

# Evaluate predictions
metrics = evaluate_model_performance(y_true, y_probs, threshold=0.70)
print(f"F1-Score: {metrics['f1_score']:.4f} | Recall: {metrics['recall']:.4f}")
```
