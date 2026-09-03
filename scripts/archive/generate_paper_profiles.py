# -*- coding: utf-8 -*-
import os, sys, json

out_dir = r'c:\Research and Business Project\Intelligent AML\docs\paper_profiles'
os.makedirs(out_dir, exist_ok=True)

# Load metadata list for 75 papers
raw_papers = [
    # Cat 1 (1-9)
    (1, 'Hu et al.', '2020', 'Heterogeneous Graph Transformer (HGT)', 'ACM WWW 2020', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★★ CRITICAL'),
    (2, 'Rossi et al.', '2020', 'Temporal Graph Networks for Deep Learning on Dynamic Graphs', 'ICML 2020 Graph Representation Learning Workshop', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★★ CRITICAL'),
    (3, 'Egressy et al. (IBM Research Zurich)', '2024', 'Provably Powerful Graph Neural Networks for Directed Multigraphs', 'AAAI 2024', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★★ CRITICAL'),
    (4, 'Johannessen & Jullum (DNB Bank)', '2023', 'Finding Money Launderers Using Heterogeneous Graph Neural Networks', 'Expert Systems with Applications (Elsevier)', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★★ CRITICAL'),
    (5, 'Nature Scientific Reports Authors', '2026', 'ChronoWave-GNN: Wavelet-Temporal Graph Transformer for Anti-Money Laundering', 'Scientific Reports, Nature (Jan 2026)', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★★ CRITICAL'),
    (6, 'Blanusa et al. (IBM Research)', '2025', 'LAS-GNN: A Graph Neural Network for Temporal Money Laundering Motif Detection', 'ACM ICAIF 2025', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★ IMPORTANT'),
    (7, 'Veličković et al.', '2018', 'Graph Attention Networks (GAT)', 'ICLR 2018', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★ IMPORTANT'),
    (8, 'Pareja et al.', '2020', 'EvolveGCN: Evolving Graph Convolutional Networks for Dynamic Graphs', 'AAAI 2020', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★ IMPORTANT'),
    (9, 'Deprez et al.', '2025', 'Network Analytics for Anti-Money Laundering: A Systematic Literature Review and Experimental Evaluation', 'INFORMS Journal on Data Science', 'Temporal & Heterogeneous GNNs — Core Architecture', '★★ IMPORTANT'),
    # Cat 2 (10-16)
    (10, 'Weber et al. (MIT / IBM)', '2019', 'Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics (Elliptic)', 'KDD FinTech Workshop 2019', 'Benchmark Datasets — Original Papers', '★★★ CRITICAL'),
    (11, 'Elmougy & Liu (Georgia Tech)', '2023', 'Demystifying Fraudulent Transactions and Illicit Nodes in the Bitcoin Network (Elliptic++)', 'ACM KDD 2023', 'Benchmark Datasets — Original Papers', '★★★ CRITICAL'),
    (12, 'Bellei et al. (MIT / IBM / Elliptic)', '2024', 'The Shape of Money Laundering: Subgraph Representation Learning with the Elliptic2 Dataset', 'arXiv:2404.19109', 'Benchmark Datasets — Original Papers', '★★★ CRITICAL'),
    (13, 'Altman et al. (IBM Research)', '2023', 'Realistic Synthetic Financial Transactions for Anti-Money Laundering Models (AMLWorld)', 'NeurIPS 2023 Datasets and Benchmarks Track', 'Benchmark Datasets — Original Papers', '★★★ CRITICAL'),
    (14, 'Lopez-Rojas & Axelsson', '2016', 'PaySim: A Financial Mobile Money Simulator for Fraud Detection', 'EMSS 2016', 'Benchmark Datasets — Original Papers', '★★★ CRITICAL'),
    (15, 'Le Borgne & Bontempi', '2022', 'Fraud Detection under Imbalanced Class Distribution and Missing Labels', 'Machine Learning, Springer', 'Benchmark Datasets — Original Papers', '★★ IMPORTANT'),
    (16, 'Wójcik', '2025', 'Money Laundering Detection with Multi-Aggregation Custom Edge GIN', 'Journal of Data Science', 'Benchmark Datasets — Original Papers', '★★ IMPORTANT'),
    # Cat 3 (17-23)
    (17, 'Liu et al.', '2021', 'Overcoming Catastrophic Forgetting in Graph Neural Networks with Topology-Aware Weight Preserving (TWP)', 'ICML 2021', 'Continual Learning & Concept Drift', '★★★ CRITICAL'),
    (18, 'Kirkpatrick et al. (DeepMind)', '2017', 'Overcoming Catastrophic Forgetting in Neural Networks (EWC)', 'PNAS 2017', 'Continual Learning & Concept Drift', '★★★ CRITICAL'),
    (19, 'Zhou & Cao', '2021', 'Overcoming Catastrophic Forgetting in Graph Neural Networks with Experience Replay', 'AAAI 2021', 'Continual Learning & Concept Drift', '★★★ CRITICAL'),
    (20, 'Zhang et al.', '2022', 'CGLB: Benchmark Tasks for Continual Graph Learning', 'NeurIPS 2022 Datasets and Benchmarks Track', 'Continual Learning & Concept Drift', '★★★ CRITICAL'),
    (21, 'Deprez et al.', '2025', 'Advances in Continual Graph Learning for Anti-Money Laundering Systems: A Comprehensive Review', 'WIREs Computational Statistics, Wiley', 'Continual Learning & Concept Drift', '★★ IMPORTANT'),
    (22, 'Zhang et al.', '2025', 'FraudGNN-RL: A Graph Neural Network with Reinforcement Learning for Adaptive Financial Fraud Detection', 'IEEE Open Journal of Computer Science', 'Continual Learning & Concept Drift', '★★ IMPORTANT'),
    (23, 'Li et al.', '2022', 'HTG-CFD: Forgetting Prevention for Cross-Regional Fraud Detection with Heterogeneous Trade Graph', 'arXiv:2204.10085', 'Continual Learning & Concept Drift', '★★ IMPORTANT'),
    # Cat 4 (24-31)
    (24, 'Beutel et al. (Adap / Flower)', '2022', 'Flower: A Friendly Federated Learning Research Framework', 'arXiv:2007.14390', 'Federated Learning & Differential Privacy', '★★★ CRITICAL'),
    (25, 'Effendi & Chattopadhyay', '2025', 'Privacy-Preserving Graph-Based ML with Fully Homomorphic Encryption for Collaborative AML', 'SPACE 2024 / Springer LNCS', 'Federated Learning & Differential Privacy', '★★★ CRITICAL'),
    (26, 'Tang & Liang', '2024', 'Credit Card Fraud Detection Based on Federated Graph Learning', 'Expert Systems with Applications (Elsevier)', 'Federated Learning & Differential Privacy', '★★★ CRITICAL'),
    (27, 'Kong et al.', '2024', 'Federated Graph Anomaly Detection via Contrastive Self-Supervised Learning', 'IEEE TNNLS', 'Federated Learning & Differential Privacy', '★★★ CRITICAL'),
    (28, 'Li et al.', '2020', 'Federated Optimization in Heterogeneous Networks (FedProx)', 'MLSys 2020', 'Federated Learning & Differential Privacy', '★★ IMPORTANT'),
    (29, 'Mironov (Google Research)', '2017', 'Rényi Differential Privacy of the Gaussian Mechanism', 'IEEE CSF 2017', 'Federated Learning & Differential Privacy', '★★ IMPORTANT'),
    (30, 'Tian et al. (Ant Group)', '2025', 'Towards Collaborative Anti-Money Laundering Among Financial Institutions', 'ACM WWW 2025', 'Federated Learning & Differential Privacy', '★★ IMPORTANT'),
    (31, 'Cross-Border AML Research Team', '2024', 'Deep Learning for Cross-Border Transaction Anomaly Detection in Anti-Money Laundering Systems', 'arXiv:2412.07027', 'Federated Learning & Differential Privacy', '★★ IMPORTANT'),
    # Cat 5 (32-38)
    (32, 'Ying et al. (Stanford)', '2019', 'GNNExplainer: Generating Explanations for Graph Neural Networks', 'NeurIPS 2019', 'Explainable AI (XAI) & Regulatory Compliance', '★★★ CRITICAL'),
    (33, 'Motie & Raahemi', '2024', 'Financial Fraud Detection Using Graph Neural Networks: A Systematic Review', 'Expert Systems with Applications (Elsevier)', 'Explainable AI (XAI) & Regulatory Compliance', '★★★ CRITICAL'),
    (34, 'FATF Secretariat', '2024', 'FATF Recommendations: International Standards on Combating Money Laundering and the Financing of Terrorism', 'FATF-GAFI Updated 2024', 'Explainable AI (XAI) & Regulatory Compliance', '★★★ CRITICAL'),
    (35, 'Lawal et al.', '2025', 'An Explainable GNN Framework for AML in Cryptocurrency Transactions Using the Elliptic Dataset', 'IJCNC Dec 2025', 'Explainable AI (XAI) & Regulatory Compliance', '★★★ CRITICAL'),
    (36, 'Sánchez-Martín et al.', '2024', 'Improving the Interpretability of GNN Predictions Through Conformal-Based Graph Sparsification', 'arXiv:2404.12356', 'Explainable AI (XAI) & Regulatory Compliance', '★★ IMPORTANT'),
    (37, 'Duval & Malliaros', '2021', 'GraphSVX: Shapley Value Explanations for Graph Neural Networks', 'ECML-PKDD 2021', 'Explainable AI (XAI) & Regulatory Compliance', '★★ IMPORTANT'),
    (38, 'Olaniyi et al.', '2026', 'Graph Neural Networks for Multi-Layered Financial Crime Network Detection: An Explainable AI Framework for AML', 'Journal of Engineering Research and Reports', 'Explainable AI (XAI) & Regulatory Compliance', '★★ IMPORTANT'),
    # Cat 6 (39-44)
    (39, 'Zhao et al.', '2021', 'GraphSMOTE: Imbalanced Node Classification on Graphs with Graph Neural Networks', 'ACM WSDM 2021', 'Class Imbalance & Graph Data Augmentation', '★★★ CRITICAL'),
    (40, 'Hadinata et al.', '2025', 'Generating Synthetic Anomaly Graph Network Dataset for AML Prediction Using Generative Adversarial Network', 'IEEE ICCAI 2025', 'Class Imbalance & Graph Data Augmentation', '★★★ CRITICAL'),
    (41, 'MDPI Applied Sciences Authors', '2026', 'HeteroGCL: A Heterogeneous Graph Contrastive Learning Framework for Scalable Cryptocurrency AML', 'MDPI Applied Sciences (March 2026)', 'Class Imbalance & Graph Data Augmentation', '★★★ CRITICAL'),
    (42, 'Cardoso et al. (Feedzai)', '2022', 'LaundroGraph: Self-Supervised Graph Representation Learning for Anti-Money Laundering', 'ACM ICAIF 2022', 'Class Imbalance & Graph Data Augmentation', '★★ IMPORTANT'),
    (43, 'Oztas et al.', '2024', 'Effectiveness of Supervised Models Hampered by Scarcity of Labelled Data and High Class Imbalance in Financial Crime', 'Future Generation Computer Systems (Elsevier)', 'Class Imbalance & Graph Data Augmentation', '★★ IMPORTANT'),
    (44, 'Elsevier ScienceDirect Authors', '2026', 'Hybrid Deep Learning for AML: Unsupervised Detection of Emerging Schemes via Feature Fusion and XAI', 'ScienceDirect (Jan 2026)', 'Class Imbalance & Graph Data Augmentation', '★★ IMPORTANT'),
    # Cat 7 (45-50)
    (45, 'Akter et al.', '2025', 'Combating Mobile Financial Fraud in Bangladesh: An NLP and Machine Learning Approach', 'IJRPR Vol 6', 'Mobile Financial Services & Bangladesh Context', '★★★ CRITICAL'),
    (46, 'MDPI Applied Sciences Authors', '2025', 'AI-Driven Cybersecurity in Mobile Financial Services: Enhancing Fraud Detection in Emerging Markets', 'MDPI Applied Sciences', 'Mobile Financial Services & Bangladesh Context', '★★★ CRITICAL'),
    (47, 'Bangladesh Bank Research Team', '2025', 'Governance Challenges in Mobile Financial Services Sector in Bangladesh', 'WJAETS 2025', 'Mobile Financial Services & Bangladesh Context', '★★★ CRITICAL'),
    (48, 'Fan et al. (NTU / SMU)', '2025', 'Deep Learning Approaches for Anti-Money Laundering on Mobile Transactions: Review, Framework, and Directions', 'arXiv:2503.10058', 'Mobile Financial Services & Bangladesh Context', '★★★ CRITICAL'),
    (49, 'Jullum et al. (NR)', '2020', 'Detecting Money Laundering Transactions with Machine Learning', 'Journal of Money Laundering Control (Emerald)', 'Mobile Financial Services & Bangladesh Context', '★★ IMPORTANT'),
    (50, 'Tertychnyi et al. (Univ of Tartu)', '2020', 'Scalable and Imbalance-Resistant Machine Learning Models for Anti-Money Laundering: A Two-Layered Approach', 'Springer 2020', 'Mobile Financial Services & Bangladesh Context', '★★ IMPORTANT'),
    # Cat 8 (51-57)
    (51, 'Harper et al.', '2025', 'STGNN: Spatial-Temporal Graph Neural Networks for Dynamic Transaction Forecasting', 'IEEE TKDE 2025', 'Data Engineering, Streaming & Scalability', '★★★ CRITICAL'),
    (52, 'Blanusa et al. (IBM Research)', '2024', 'Graph Feature Preprocessor: Real-Time Subgraph-based Feature Extraction for Financial Crime Detection', 'ACM ICAIF 2024', 'Data Engineering, Streaming & Scalability', '★★★ CRITICAL'),
    (53, 'Chen & Yang', '2026', 'Real-Time Dynamic Graph Learning with Temporal Attention for Financial Fraud Detection', 'Frontiers in AI (Feb 2026)', 'Data Engineering, Streaming & Scalability', '★★★ CRITICAL'),
    (54, 'Khosravi et al.', '2025', 'Transaction Fraud Detection via Attentional Spatial-Temporal GNN', 'Journal of Supercomputing (Springer)', 'Data Engineering, Streaming & Scalability', '★★ IMPORTANT'),
    (55, 'Devi et al.', '2025', 'RL-GNN Fusion for Real-Time Financial Fraud Detection: A Context-Aware Community Mining Approach', 'Scientific Reports, Nature', 'Data Engineering, Streaming & Scalability', '★★ IMPORTANT'),
    (56, 'Paoletti et al. (Politecnico di Torino)', '2025', 'MAD: Multicriteria Anomaly Detection of Suspicious Financial Accounts from Billions of Cash Transactions', 'ACM SIGKDD 2025', 'Data Engineering, Streaming & Scalability', '★★ IMPORTANT'),
    (57, 'Immadisetty', '2025', 'Real-Time Fraud Detection Using Streaming Data in Financial Transactions', 'JRTCSE 2025', 'Data Engineering, Streaming & Scalability', '★ SUPPORTING'),
    # Cat 9 (58-62)
    (58, 'Li et al.', '2024', 'Graph Learning-Empowered Financial Fraud Detection: Progress and Future Directions', 'IEEE TKDE 2024', 'GNN Surveys & Foundation Models for Finance', '★★★ CRITICAL'),
    (59, 'Zhang et al. (IBM Research)', '2024', 'FraudGT: A Simple, Effective, and Efficient Graph Transformer for Financial Fraud Detection', 'ACM ICAIF 2024', 'GNN Surveys & Foundation Models for Finance', '★★ IMPORTANT'),
    (60, 'GNN Fraud Review Team', '2024', 'Graph Neural Networks for Financial Fraud Detection: A Review', 'arXiv:2411.05815', 'GNN Surveys & Foundation Models for Finance', '★★ IMPORTANT'),
    (61, 'SAR LLM Research Team', '2025', 'LLM-Enhanced AML: Generating Auditable SAR Narratives from GNN Subgraph Explanations', 'arXiv:2506.01093', 'GNN Surveys & Foundation Models for Finance', '★★ IMPORTANT'),
    (62, 'Tang et al.', '2025', 'Deep Graph Anomaly Detection: A Survey and New Perspectives', 'IEEE TKDE 2025', 'GNN Surveys & Foundation Models for Finance', '★★ IMPORTANT'),
    # Cat 10 (63-66)
    (63, 'Chai et al. (Ant Group)', '2023', 'Towards Learning to Discover Money Laundering Subnetwork in Massive Transaction Network', 'AAAI 2023', 'AML Subgraph, Community & Ring Detection', '★★★ CRITICAL'),
    (64, 'Cheng et al.', '2023', 'Anti-Money Laundering by Group-Aware Deep Graph Learning', 'IEEE TKDE 2023', 'AML Subgraph, Community & Ring Detection', '★★★ CRITICAL'),
    (65, 'Ding et al.', '2025', 'AML-CFSim: Counterfactual Similarity for Anti-Money Laundering', 'Expert Systems with Applications (Elsevier)', 'AML Subgraph, Community & Ring Detection', '★★ IMPORTANT'),
    (66, 'Karim et al. (Fraunhofer)', '2023', 'Catch Me If You Can: Semi-Supervised Graph Learning for Spotting Money Laundering', 'arXiv:2302.11880', 'AML Subgraph, Community & Ring Detection', '★★ IMPORTANT'),
    # Cat 11 (67-69)
    (67, 'Gummadi', '2025', 'Temporal Graph Neural Networks for Real-Time Fraud Detection in Cross-Border Transactions', 'IJAIDSML Nov 2025', 'AML Alert Optimization & Production Systems', '★★★ CRITICAL'),
    (68, 'Eddin et al. (Feedzai)', '2022', 'Anti-Money Laundering Alert Optimization Using Machine Learning with Graphs', 'ACM ICAIF 2022', 'AML Alert Optimization & Production Systems', '★★ IMPORTANT'),
    (69, 'Jambhrunkar et al.', '2026', 'MuleTrack: A Lightweight Temporal Learning Framework for Money Mule Detection in Digital Payments', 'Springer 2026', 'AML Alert Optimization & Production Systems', '★★ IMPORTANT'),
    # Cat 12 (70-73)
    (70, 'Zügner et al. (TUM)', '2018', 'Adversarial Attacks on Neural Networks for Graph Data (Nettack)', 'ACM SIGKDD 2018', 'Adversarial Robustness on GNNs', '★★★ CRITICAL'),
    (71, 'Zhang & Zitnik (Harvard)', '2020', 'GNNGuard: Defending Graph Neural Networks Against Adversarial Attacks', 'NeurIPS 2020', 'Adversarial Robustness on GNNs', '★★★ CRITICAL'),
    (72, 'Wu et al. (Tongji / Tencent)', '2024', 'Safeguarding Fraud Detection from Attacks: A Robust Graph Learning Approach (GLSGNN)', 'IJCAI 2024', 'Adversarial Robustness on GNNs', '★★★ CRITICAL'),
    (73, 'Jeon et al.', '2025', 'Leveraging Vulnerabilities in Temporal Graph Neural Networks via Strategic High-Impact Assaults (HIA)', 'ACM CIKM 2025', 'Adversarial Robustness on GNNs', '★★ IMPORTANT'),
    # Cat 13 (74-75)
    (74, 'European Parliament and Council', '2024', 'Regulation (EU) 2023/1114 on Markets in Crypto-Assets (MiCA) — Full Implementation Text', 'Official Journal of the EU', 'MiCA & Crypto AML Regulatory Compliance', '★★★ CRITICAL'),
    (75, 'Jullum et al. / Elliptic Team', '2025', 'Cryptocurrency AML Under MiCA: Graph-Based Transaction Monitoring and Wallet Screening Requirements for CASPs', 'Journal of Financial Compliance', 'MiCA & Crypto AML Regulatory Compliance', '★★★ CRITICAL')
]

print(f'Total paper records loaded: {len(raw_papers)}')
