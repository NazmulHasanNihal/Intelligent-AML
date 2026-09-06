# 📚 Curated Literature Base & Theoretical Foundations

This directory outlines the theoretical and empirical literature underpinning **C-STGB** (*Conformal Spatio-Temporal GraphBoost*). The research corpus spans **75 seminal and state-of-the-art papers** (2017–2026) across graph representation learning, temporal point processes, class imbalance, conformal risk control, adversarial robustness, and regulatory compliance.

> [!NOTE]
> **Copyright & Open-Source Hygiene:**  
> In accordance with IEEE, ACM, Springer Nature, Elsevier copyright policies and GitHub open-science standards, third-party publisher PDF binaries are excluded from version control. Complete mathematical analyses, architectural dissections, and equation extractions for all 75 papers are independently authored and maintained in [`docs/paper_profiles/`](../paper_profiles/). Full BibTeX citations and DOIs are maintained in [`papers/IEEE_Research_Paper/references.bib`](../../papers/IEEE_Research_Paper/references.bib) and [`papers/University_CSE_Thesis/references.bib`](../../papers/University_CSE_Thesis/references.bib).

---

## 🏛️ Taxonomic Categorization of Literature

The literature base is organized across eight core research pillars:

### 1. Spatio-Temporal & Heterogeneous Graph Neural Networks
*Foundations for relational representation of financial transactions across multiple entity types and continuous time.*
- **HGT (WWW 2020):** Heterogeneous Graph Transformer (Hu et al.) — Type-specific parameter parameterization and relative positional encodings. [Profile 01](../paper_profiles/paper_01_Heterogeneous_Graph_Transformer_HGT.md).
- **TGN (ICML 2020):** Temporal Graph Networks for Deep Learning on Dynamic Graphs (Rossi et al.) — Memory modules and continuous-time message passing. [Profile 02](../paper_profiles/paper_02_Temporal_Graph_Networks_for_Deep_Le.md).
- **EvolveGCN (AAAI 2020):** Evolving Graph Convolutional Networks (Pareja et al.) — Weight evolution via RNNs along graph snapshots. [Profile 08](../paper_profiles/paper_08_EvolveGCN_Evolving_Graph_Convolutio.md).
- **ChronoWave-GNN (2026):** Wavelet-Temporal Graph Transformer for Anti-Money Laundering — Multi-scale temporal decomposition. [Profile 05](../paper_profiles/paper_05_ChronoWave_GNN_Wavelet_Temporal_Gra.md).
- **LAS-GNN (2025):** Temporal Money Laundering Motif Detection with Learnable Attention Sparsification. [Profile 06](../paper_profiles/paper_06_LAS_GNN_A_Graph_Neural_Network_for_.md).
- **Provably Powerful Directed GNNs (ICLR 2024):** Multigraph message passing resolving directed flow symmetries. [Profile 03](../paper_profiles/paper_03_Provably_Powerful_Graph_Neural_Netw.md).

### 2. Extreme Class Imbalance & Graph Oversampling
*Techniques for handling severe minority skew ($\pi < 0.05\%$) without synthetic topology corruption.*
- **GraphSMOTE (WSDM 2021):** Imbalanced Node Classification on Graphs (Zhao et al.) — Latent-space minority interpolation with link prediction. [Profile 39](../paper_profiles/paper_39_GraphSMOTE_Imbalanced_Node_Classifi.md).
- **Synthetic Anomaly Generation (KDD 2024):** Generative modeling of minority graph motifs. [Profile 40](../paper_profiles/paper_40_Generating_Synthetic_Anomaly_Graph_.md).
- **HeteroGCL (2024):** Contrastive self-supervised pretraining for skewed heterogeneous topologies. [Profile 41](../paper_profiles/paper_41_HeteroGCL_A_Heterogeneous_Graph_Con.md).
- **LaundroGraph (2025):** Self-supervised representation learning for money laundering paths. [Profile 42](../paper_profiles/paper_42_LaundroGraph_Self_Supervised_Graph_.md).

### 3. Adversarial Robustness & Camouflage Defense
*Mechanisms for detecting and suppressing evasion maneuvers (e.g., dispersion through merchant hubs, smurfing).*
- **CARE-GNN (CIKM 2020):** Camouflage-Aware Anti-Fraud GNN — Label-informed reinforcement filtering of deceptive relations. [Profile 72](../paper_profiles/paper_72_Safeguarding_Fraud_Detection_from_A.md).
- **GNNGuard (NeurIPS 2020):** Defending Graph Neural Networks against Adversarial Attacks via Neighbor Importance Weighting. [Profile 71](../paper_profiles/paper_71_GNNGuard_Defending_Graph_Neural_Net.md).
- **Temporal Evasion Vulnerabilities (2025):** Evaluating evasion attacks against continuous-time dynamic graph learning. [Profile 73](../paper_profiles/paper_73_Leveraging_Vulnerabilities_in_Tempo.md).

### 4. Distribution-Free Uncertainty Quantification & Conformal Risk Control
*Finite-sample mathematical safety bounds guaranteeing coverage under arbitrary data distributions.*
- **Conformal Prediction Intro (2023):** Angelopoulos & Bates — Gentle introduction to split conformal prediction and risk control.
- **Conformal Graph Sparsification (2024):** Improving GNN interpretability with conformal non-conformity guarantees. [Profile 36](../paper_profiles/paper_36_Improving_the_Interpretability_of_G.md).
- **Adaptive Conformal Inference (ACI, 2021):** Online threshold adjustment under temporal non-stationarity and concept drift.

### 5. Explainable AI (XAI) & Regulatory Model Governance
*Interpretable subgraph extraction and regulatory narrative generation conforming to FinCEN and supervisory guidance.*
- **GNNExplainer (NeurIPS 2019):** Information-theoretic compact subgraph explanations. [Profile 32](../paper_profiles/paper_32_GNNExplainer_Generating_Explanation.md).
- **GraphSVX (ICML 2021):** Shapley Value Explanations for Graph Neural Networks. [Profile 37](../paper_profiles/paper_37_GraphSVX_Shapley_Value_Explanations.md).
- **LLM-Enhanced AML (2026):** Auditable SAR narrative generation from causal subgraphs. [Profile 61](../paper_profiles/paper_61_LLM_Enhanced_AML_Generating_Auditab.md).
- **FATF Recommendations & Guidance (2024–2026):** International standards on combating money laundering and terrorist financing. [Profile 34](../paper_profiles/paper_34_FATF_Recommendations_International_.md).
- **Federal Reserve SR 26-2 (2026):** Supervisory Letter superseding SR 11-7 and SR 21-8 on Model Risk Management for Complex AI Systems.

### 6. Federated Learning & Differential Privacy
*Collaborative cross-institution model training preserving financial privacy.*
- **Flower Framework (2022):** Friendly Federated Learning Research Framework. [Profile 24](../paper_profiles/paper_24_Flower_A_Friendly_Federated_Learnin.md).
- **FedProx (MLSys 2020):** Federated Optimization in Heterogeneous Networks. [Profile 28](../paper_profiles/paper_28_Federated_Optimization_in_Heterogen.md).
- **Privacy-Preserving Collaborative AML (2025):** Graph-based collaborative detection with homomorphic encryption. [Profile 25](../paper_profiles/paper_25_Privacy_Preserving_Graph_Based_ML_w.md).

### 7. Continual Learning & Concept Drift Adaptation
*Preventing catastrophic forgetting across regulatory epochs and darknet market disruptions.*
- **EWC (PNAS 2017):** Overcoming Catastrophic Forgetting via Fisher Information matrix regularization. [Profile 17](../paper_profiles/paper_17_Overcoming_Catastrophic_Forgetting_.md).
- **Topology-Aware Weight Preserving (TWP, ECCV 2020):** Protecting critical topological representations during incremental graph training. [Profile 18](../paper_profiles/paper_18_Overcoming_Catastrophic_Forgetting_.md).
- **CGLB (NeurIPS 2023):** Continual Graph Learning Benchmark tasks and evaluation protocols. [Profile 20](../paper_profiles/paper_20_CGLB_Benchmark_Tasks_for_Continual_.md).

### 8. Financial Forensics Benchmark Datasets
*Empirical evaluation corpora spanning blockchain, mobile money, and traditional banking.*
- **Elliptic Dataset (2019):** Anti-Money Laundering in Bitcoin (Weber et al., KDD). [Profile 10](../paper_profiles/paper_10_Anti_Money_Laundering_in_Bitcoin_Ex.md).
- **Elliptic2 Dataset (2024):** Subgraph representation learning with multi-entity crypto networks. [Profile 12](../paper_profiles/paper_12_The_Shape_of_Money_Laundering_Subgr.md).
- **PaySim (2016):** Financial mobile money simulator based on real cellular transactions. [Profile 14](../paper_profiles/paper_14_PaySim_A_Financial_Mobile_Money_Sim.md).
- **IBM AMLSim (2019):** Agent-based synthetic financial transaction network with structured laundering typologies. [Profile 13](../paper_profiles/paper_13_Realistic_Synthetic_Financial_Trans.md).
- **XBlock-ETH (2023):** On-chain Ethereum token transfer and phishing transaction networks. [Profile 16](../paper_profiles/paper_16_Money_Laundering_Detection_with_Mul.md).

---

## 🔗 Related Resources in this Repository

| Resource | Location | Description |
| :--- | :--- | :--- |
| **Individual Paper Profiles** | [`docs/paper_profiles/`](../paper_profiles/) | Detailed markdown dossiers for all 75 surveyed works. |
| **Literature Summary Table** | [`docs/paper_profiles/00_summary_table.md`](../paper_profiles/00_summary_table.md) | Compact matrix comparing algorithms, tasks, datasets, and venues. |
| **IEEE Paper Bibliography** | [`papers/IEEE_Research_Paper/references.bib`](../../papers/IEEE_Research_Paper/references.bib) | Camera-ready BibTeX citations used in the IEEE TIFS submission. |
| **Thesis Bibliography** | [`papers/University_CSE_Thesis/references.bib`](../../papers/University_CSE_Thesis/references.bib) | Comprehensive 75+ reference BibTeX database for the University Thesis. |
