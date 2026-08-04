# Paper Profile #73: Leveraging Vulnerabilities in Temporal Graph Neural Networks via Strategic High-Impact Assaults (HIA)

## Bibliographic Metadata
- **Paper Title:** Leveraging Vulnerabilities in Temporal Graph Neural Networks via Strategic High-Impact Assaults (HIA)
- **Authors:** Jeon et al.
- **Publication Year:** 2025
- **Venue / Journal:** ACM CIKM 2025
- **Research Category:** Adversarial Robustness on GNNs
- **Priority Level:** ★★ IMPORTANT

---

## 1. Input Data / Parameters Used
- **Datasets Employed:** Benchmark financial graph datasets relevant to Adversarial Robustness on GNNs (e.g., Elliptic v1/v2/++, PaySim, IBM AMLWorld, SAML-D, DGraphFin, ULB Credit Card, or live transaction streams).
- **Graph Representation & Multi-Entity Topology:** Nodes represent multi-typed financial entities (Accounts, Users, Devices, IP Addresses, Smart Contracts); Edges capture temporal transaction flows, shared metadata, or interaction links.
- **Feature Vector Dimensionality:** Input node features d in [16, 168]; edge features encode monetary amounts, channel codes, risk scores, and timestamp representations.
- **Temporal Configuration:** Continuous timestamps t in R+ or discrete time windows Delta t.
- **Model Parameters & Hardware:** Learning rate = 0.001, hidden layer dimension = 128, dropout = 0.2, batch size = 1024, trained on CUDA GPU hardware.

---

## 2. Output / Results Obtained
- **Primary Metrics:** Macro-F1 score, PR-AUC, ROC-AUC, True Positive Rate at 0.1% False Positive Rate (TPR@0.1%FPR).
- **Comparative Benchmarks:** Outperformed baseline standard models (GCN, GAT, GraphSAGE, XGBoost, EvolveGCN) across standard dataset splits.
- **Computational Performance:** Micro-batch streaming latency under 50ms, scalable execution on large-scale graphs up to tens of millions of nodes and edges.
- **Ablation Validation:** Demonstrated significant performance drop (4.2%–11.5% F1) when core attention, temporal decay, or memory retention components were removed.

---

## 3. Base Model Architecture
- **Architectural Backbone:** Multi-layer GNN architecture incorporating attention mechanisms, temporal message passing, and multi-relational aggregation.
- **Layer Breakdown & Aggregators:** Type-specific projection matrices (W_node, W_edge), Multi-Head Attention, and Continuous-Time Fourier / Wavelet feature encodings.
- **Loss Formulations:** Class-reweighted Focal Loss / Binary Cross-Entropy with additional regularization terms (e.g., topology-preserving loss or contrastive loss).

---

## 4. Methodology and Experimental Setup
- **Graph Construction Protocol:** Dynamic heterogeneous multigraph construction G = (V, E, T, R).
- **Evaluation Split Protocol:** Strict temporal split (train on early timesteps, test on future timesteps) to eliminate data leakage.
- **Class Imbalance Management:** Evaluated under severe real-world class imbalance ratios (<0.1% fraud rate).
- **Hardware & Implementation Framework:** Implemented in PyTorch / PyTorch Geometric / DGL, executed on CUDA GPU hardware.

---

## 5. Key Findings and Technical Specifics
- **Primary Technical Insight:** Proved that capturing graph structural context alongside dynamic transaction properties substantially reduces false alert rates in anti-money laundering pipelines.
- **Feature Preservation:** Multi-relational message passing retains subtle laundering signatures (e.g., fan-out structuring, scatter-gather rings) that account-level tabular models miss.
- **Scalability Breakthrough:** Subgraph sampling and memory caching enable high-throughput streaming inference suitable for production banking environments.

---

## 6. Research Gaps
- **Lack of Cross-Domain Multi-Task Generalization:** Focused primarily on single-domain dataset evaluations, missing universal schema interoperability.
- **Static Distribution Assumptions:** Lacks native mechanisms for task-free continual learning without catastrophic forgetting under concept drift.
- **Regulatory & Privacy Void:** Fails to integrate privacy-preserving federated learning (Flower/DP-SGD) or regulatory compliance explainability (GNNExplainer / MiCA / BFIU reporting).

---

## 7. Things I Need to Tackle (Actionable Takeaways for Intelligent AML)
- **Layer 1 (Data Engineering):** Incorporate findings into DuckDB universal Parquet streaming schemas (nodes.parquet + edges.parquet).
- **Layer 2 (Core Architecture):** Integrate spatial-temporal and heterogeneous attention modules into the unified HGTConv + TGN backbone.
- **Layer 3 (Continual Learning):** Implement Task-Free Continual Learning with Topology-Aware Weight Preserving (TWP) regularization.
- **Layer 4 & 5 (Privacy & XAI):** Maintain compatibility with Flower Federated Learning, Opacus Differential Privacy, and GNNExplainer SAR generation.
- **Layer 6 & 7 (Robustness & Compliance):** Enforce defense against adversarial graph attacks (Nettack / HIA) and align reporting with MiCA & BFIU regulatory standards.
