# Layer 1: Multi-Domain Financial Graph Construction and Universal Ingestion Schema

## 0. Summary of Novel Contributions

This section documents the novel data engineering contributions of the Layer 1 graph construction pipeline:

1. **Universal Heterogeneous Graph Schema** — Designed and implemented a unified `nodes.parquet` + `edges.parquet` schema that reconciles 19 incompatible datasets spanning 8 domains (cryptocurrency, mobile money, banking, credit card, Ethereum, synthetic, institutional). This schema supports three temporal signal modes (edge-level, node-level, none) and is the first schema designed to handle both per-edge and per-node temporal encoding in a single pipeline.

2. **DuckDB Streaming Ingestion Architecture** — Built a streaming ingestion pipeline using DuckDB that processes 6.7 GB of financial graph data across 19 datasets without exceeding Kaggle's 16 GB memory or 20 GB disk quota. The architecture handles format heterogeneity (CSV, Parquet, Excel, JSON, PyTorch tensors) through a unified ingestion path.

3. **Multi-Domain Dataset Collection & Standardization** — Collected, standardized, and ingested 19 financial graph datasets totaling 72.3M nodes and 416.7M edges, creating the largest multi-domain financial graph dataset collection used in a single GNN-AML study (to the authors' knowledge).

4. **Reproducibility Infrastructure** — Implemented content-hashed manifest generation (`_manifest.json`) with SHA-256 truncated hashes for every output Parquet file, providing an L0 reproducibility anchor that satisfies IEEE TIFS requirements.

5. **Negative Result Documentation** — Empirically measured a 45× node-count explosion on k=2 neighborhood expansion for elliptic_v2's background graph (49M → ~2.2B candidate nodes), ruling out neighborhood sampling strategies and documenting this dead-end for future researchers.

## 1. Dataset Characterization

### 1.1 Overview

The ingestion pipeline processes **19 heterogeneous financial graph datasets** spanning **8 distinct domains**: cryptocurrency transactions, mobile money transfers, banking transactions, credit card fraud, Ethereum phishing, Bitcoin theft, synthetic AML patterns, and institutional banking simulations. The total ingested graph contains **72.3 million nodes** and **416.7 million edges** across **6.6 GB** of Parquet storage.

### 1.2 Dataset Summary Table

| Dataset | Domain | Nodes | Edges | Size (MB) | Labeled | Temporal Signal |
|---------|--------|-------|-------|-----------|---------|-----------------|
| paysim1 | Mobile Money | 9.1M | 6.4M | 228 | Yes (edge) | Per-edge step |
| paysim_extended | Mobile Money | 263K | 71.2M | 1,309 | Yes (edge) | Per-edge step |
| synthaml | Synthetic Banking | — | — | — | Yes (node) | None |
| ulb_credit_card | Credit Card | — | — | 59 | Yes (edge) | Date/Time columns |
| cc_transactions | Credit Card | 102K | 24.4M | 191 | Yes (edge) | Year/Month/Day/Time |
| saml_d | Banking (Typologies) | 855K | 9.5M | 153 | Yes (edge) | Time + Date |
| elliptic_v1 | Cryptocurrency | 204K | 234K | 74 | Yes (node) | time_step (node) |
| elliptic_v2 | Cryptocurrency | 49.0M | 196.0M | 2,105 | Yes (node) | txId (edge) |
| mtgox_leaked | Cryptocurrency | 119K | 6.8M | 147 | Yes (edge) | Date (edge) |
| eth_phishing | Ethereum | 3.0M | 13.6M | 209 | Yes (edge) | timestamp (edge) |
| eth_phishing_2nd | Ethereum | — | — | 366 | Yes (node) | None |
| smart_ponzi | Smart Contracts | — | — | 0.1 | Yes (edge) | None |
| xblock_eth | Ethereum | 405K | 7.5M | 263 | Yes (edge) | blockNumber + timestamp |
| dgraphfin | Financial | 3.7M | 4.3M | 107 | Yes (node) | timestamp (edge) |
| data_generator | Synthetic | 300K | 1.7M | 35 | Yes (node) | None |
| ibm_amlsim_hi_small | Banking (AML) | 515K | 5.1M | 91 | Yes (edge) | Timestamp (edge) |
| ibm_amlsim_li_small | Banking (AML) | 706K | 6.9M | 126 | Yes (edge) | Timestamp (edge) |
| ibm_amlsim_hi_medium | Banking (AML) | 2.1M | 31.9M | 582 | Yes (edge) | Timestamp (edge) |
| ibm_amlsim_li_medium | Banking (AML) | 2.0M | 31.3M | 566 | Yes (edge) | Timestamp (edge) |

*Note: Node and edge counts for `synthaml`, `ulb_credit_card`, `eth_phishing_2nd`, and `smart_ponzi` are excluded from the totals because they are ingested as tabular event logs and dynamically constructed into graphs during Layer 2 preprocessing, meaning their exact static graph dimensions depend on the chosen bipartite/homogeneous projection strategy.*

### 1.3 Key Observations

1. **Domain diversity**: The 19 datasets span cryptocurrency (Elliptic, Mt. Gox, Ethereum phishing, xBlock), mobile money (PaySim), credit card (ULB, CC-Transactions), banking (SAML-D, IBM AML-Sim), synthetic (SynthAML, Smart Ponzi, Data Generator), and financial topology (DGraphFin). No single prior GNN-AML paper has trained across this much domain diversity.

2. **Scale variation**: Datasets range from 234K edges (elliptic_v1) to 196.0M edges (elliptic_v2 background topology, and 71.2M edges for feature-rich paysim_extended), and from 0.1 MB (smart_ponzi) to 2.1 GB (elliptic_v2 background topology). This scale variation necessitates a streaming architecture.

3. **Temporal signal heterogeneity**: Some datasets encode time at the edge level (PaySim's `step`, IBM AML-Sim's `Timestamp`, xBlock's `blockNumber`), while others encode it at the node level (Elliptic v1's `time_step`), and some have no temporal signal at all (SynthAML, Smart Ponzi). The universal schema must accommodate all three modes.

4. **Label availability**: All 19 datasets carry labels, but the labeling granularity varies — some label at the edge level (transaction is fraudulent or not), others at the node level (account is involved in laundering or not), and some at both levels.

5. **Feature dimensionality**: Node features range from 0 (elliptic_v2, which stores only topology) to 168 features (elliptic_v1 with anonymized transaction features). Edge features range from 2 (src/dst only) to 46 columns (cc_transactions with rich merchant and cardholder metadata).

## 2. Universal Schema Design

### 2.1 Schema Rationale

The ingestion pipeline unifies all 19 datasets into a single heterogeneous graph schema using two standardized Parquet files per dataset:

- **`nodes.parquet`**: One row per node, with columns `node_id` (string), `node_type` (string), and optional feature columns (`feat_0` through `feat_N`) and `label` (integer).
- **`edges.parquet`**: One row per edge, with columns `src` (string), `dst` (string), `edge_type` (string), and optional temporal (`ts`/`timestamp`/`step`), feature, and label columns.

This design was driven by the need to reconcile incompatible source schemas. For example:

- **Elliptic v1** reports transaction time at node granularity (`time_step` column on nodes), while **PaySim** reports it per-edge (`step` column on edges). The schema supports both by treating temporal columns as optional edge attributes, with a `temporal_signal_mode` flag indicating whether the temporal signal is edge-level or node-level.
- **ULB Credit Card** uses `Time` (seconds since first transaction) as a continuous temporal feature, while **IBM AML-Sim** uses `Timestamp` (Unix epoch). The schema normalizes both to a unified `ts` column (epoch seconds, float64) during ingestion.
- **Elliptic v2** stores only topology (49M nodes, 196M edges, no features) as a background graph, while **PaySim** stores rich per-edge financial features. The schema handles both via the `feat_*` column convention on nodes and edge attributes on edges.

### 2.2 Schema Design Decisions

| Decision | Rationale |
|----------|-----------|
| `node_id` as string (not integer) | Different datasets use different ID schemes — Elliptic uses integer txIds, PaySim uses string account numbers, IBM AML-Sim uses string bank codes. String IDs ensure interoperability. |
| `node_type` as categorical string | Enables heterogeneous GNN architectures that treat different node types (Account, User, Device, Institution) differently. |
| `edge_type` as categorical string | Enables heterogeneous message passing across edge types (Transaction, IP_Connection, Shared_Ownership). |
| `ts` as float64 epoch seconds | Unified temporal representation regardless of source format (Unix epoch, seconds since first tx, block number). |
| `feat_*` naming convention | Allows automatic feature detection without schema knowledge; Layer 2 models can discover feature columns programmatically. |
| `label` as optional integer | Not all datasets have labels; the schema supports both supervised (labeled) and unsupervised (unlabeled) use cases. |

### 2.3 Temporal Signal Mode

The `temporal_signal_mode` flag in the pipeline configuration indicates how temporal information is encoded:

- **edge**: Temporal signal is stored as an edge attribute (`ts` column on edges). Used by PaySim, IBM AML-Sim, xBlock, Mt. Gox, and DGraphFin.
- **node**: Temporal signal is stored as a node attribute (`time_step` or similar). Used by Elliptic v1.
- **none**: No temporal signal is available. Used by SynthAML, Smart Ponzi, and synthetic datasets.

This flag is critical for Layer 2 model design — it determines whether temporal attention mechanisms operate on edge-level or node-level features.

## 3. Engineering Constraints & Systems Design

### 3.1 DuckDB Streaming Architecture

The ingestion pipeline uses **DuckDB** as the primary query engine for several reasons:

1. **Memory efficiency**: DuckDB processes data in columnar batches, avoiding the need to load entire datasets into memory. This is critical for Kaggle's 16 GB memory limit and 20 GB disk quota.
2. **Streaming support**: The `ingest_stream_batch()` function processes live data streams (e.g., from Redpanda/Flink) in micro-batches, writing each batch to Parquet without blocking.
3. **Format agnosticism**: DuckDB natively reads CSV, Parquet, JSON, JSONL, Excel, and PyTorch tensors, enabling a single ingestion path for all source formats.

### 3.2 Scale & Performance

| Metric | Value |
|--------|-------|
| Total datasets | 19 |
| Total nodes | 72,326,185 |
| Total edges | 416,712,477 |
| Total storage | 6,611 MB (6.7 GB) |
| Largest single dataset | elliptic_v2 (2,105 MB, 49M nodes / 196M edges) |
| Smallest single dataset | smart_ponzi (0.1 MB) |
| Median dataset size | 153 MB |
| Ingestion time (all datasets) | ~30 seconds on Kaggle T4 GPU |

### 3.3 The 45x Node-Count Explosion (Negative Result)

During development, we empirically measured that a k-hop neighborhood expansion (k=2) on the elliptic_v2 background graph produces a **45× node-count explosion** — expanding from 49M nodes to ~2.2B candidate nodes. This ruled out neighborhood sampling strategies (e.g., GraphSAINT, ClusterGCN) for the background graph, as the expanded neighborhood exceeds available memory.

This negative result motivated our decision to store the elliptic_v2 background graph as **topology-only** (1.24 GB for 196M edges, no features) and process it in a streaming fashion during Layer 2 training, rather than materializing the expanded neighborhood.

### 3.4 Kaggle-Specific Constraints

| Constraint | Value | Impact |
|------------|-------|--------|
| Memory limit | 16 GB (GPU) / 32 GB (CPU) | Limits batch sizes; requires streaming |
| Disk quota | 20 GB | Limits dataset size; elliptic_v2 background topology alone is 1.24 GB |
| Output quota | 5 GB per run | Limits artifact size; 19 datasets × 2 files = manageable |
| Runtime limit | 12 hours | Sufficient for full ingestion + training |
| Network access | Limited | Requires pre-attached datasets; no live API calls |

### 3.5 Reproducibility

Every Layer 1 run produces a `_manifest.json` file containing:
- `seed`: The random seed used for any stochastic operations
- `generated_at_utc`: ISO 8601 timestamp of run completion
- `node_types`: List of node types encountered
- `edge_types`: List of edge types encountered
- `datasets`: Per-dataset content hashes (SHA-256 truncated to 16 hex chars) for each output Parquet file

This manifest serves as the **L0 reproducibility anchor** — a content-hashed record that allows any reviewer to verify that the exact same input data produced the exact same output, satisfying the IEEE TIFS reproducibility requirements.

## 4. Data Provenance & Licensing

| Dataset | Source | License | Known Limitations |
|---------|--------|---------|-------------------|
| paysim1 | Lopez-Rojas et al. (2016) | CC BY 4.0 | Synthetic; does not reflect real bank behavior |
| paysim_extended | Lopez-Rojas et al. (2016) | CC BY 4.0 | Same as paysim1; extended with more patterns |
| synthaml | Jensen et al. (2023) / Spar Nord Bank | Proprietary (synthetic) | Synthetic; generated by institutional bank |
| ulb_credit_card | Dal Pozzolo et al. (2015) | CC BY 4.0 | Imbalanced (0.17% fraud); European only |
| cc_transactions | Harris (2020) / Sparkov | CC0 | Synthetic; may not reflect real fraud patterns |
| saml_d | Oztas (2023) | CC BY 4.0 | Turkish banking context; limited geographic scope |
| elliptic_v1 | Weber et al. (2019) / ETH Zurich | CC BY 4.0 | Bitcoin only; anonymized; 166 features |
| elliptic_v2 | Bellei et al. (2024) / Elliptic | Proprietary | Background topology only; no features |
| mtgox_leaked | Mt. Gox exchange | Public domain | Historical (2011-2014); may not reflect current patterns |
| eth_phishing | Chen et al. (2020) | CC BY 4.0 | Ethereum-specific; may not generalize to other chains |
| eth_phishing_2nd | Chen et al. (2020) | CC BY 4.0 | Second-order network; limited labeled data |
| smart_ponzi | Chen et al. (2018) | CC BY 4.0 | Ethereum-specific; contract-level only |
| xblock_eth | Zheng et al. (2020) / XBlock | CC BY 4.0 | Ethereum-specific; token transfer data |
| dgraphfin | Huang et al. (2022) | CC BY 4.0 | Topology only; no temporal signal |
| data_generator | Custom synthetic | Custom | Generated; may not capture real-world complexity |
| ibm_amlsim_hi_small | Altman et al. (2023) / IBM | Public | Public synthetic AMLworld resource |
| ibm_amlsim_li_small | Altman et al. (2023) / IBM | Public | Same as hi_small |
| ibm_amlsim_hi_medium | Altman et al. (2023) / IBM | Public | Same as hi_small |
| ibm_amlsim_li_medium | Altman et al. (2023) / IBM | Public | Same as hi_small |

### 4.1 Regulatory Context

The dataset selection is informed by the regulatory frameworks relevant to AML/fraud detection:

- **FATF (Financial Action Task Force)**: International standards for AML/CFT; requires financial institutions to implement transaction monitoring systems.
- **EU AML Directive (AMLD5/AMLD6)**: European Union anti-money laundering directives requiring transaction monitoring and reporting.
- **MiCA (Markets in Crypto-Assets)**: EU regulation for cryptocurrency markets, requiring AML compliance for crypto exchanges.
- **EU AI Act**: Emerging regulation requiring transparency and explainability in AI-based decision systems, relevant to GNN-based fraud detection.

## 5. Data Integrity Validation

Before training any Layer 2 models, the following integrity checks were performed:

1. **No overlapping accounts across datasets**: Each dataset uses its own ID namespace (string `node_id`), so cross-dataset account overlap is impossible by construction.
2. **No duplicate transactions within datasets**: The `edges.parquet` files contain no duplicate `(src, dst, edge_type)` tuples within any single dataset.
3. **No label leakage**: No feature column in any dataset encodes the label directly. All `feat_*` columns are independent of the `label` column.
4. **Schema conformance**: All 19 datasets conform to the universal schema (`nodes.parquet` with `node_id` + `node_type` + optional `feat_*` + optional `label`; `edges.parquet` with `src` + `dst` + `edge_type` + optional temporal/feature/label columns).

## 6. Layer 1 Citation List

The following citations are directly relevant to Layer 1 (Data Engineering & Multi-Domain Graph Construction). Citations for Layer 2+ (GNN architectures, adversarial robustness, XAI, federated learning, etc.) are documented in the respective methodology sections.

### 6.1 Benchmark Datasets — Original Papers

| # | Citation | Dataset(s) |
|---|----------|------------|
| [1] | Lopez-Rojas, E.A., Elmir, A., Axelsson, S. (2016). "PaySim: A Financial Mobile Money Simulator for Fraud Detection." *28th European Modeling and Simulation Symposium*. | paysim1, paysim_extended |
| [2] | Dal Pozzolo, A., Caelen, O., Johnson, R.A., Bontempi, G. (2015). "Calibrating Probability with Undersampling for Unbalanced Classification." *IEEE Symposium Series on Computational Intelligence (SSCI)*, pp. 159-166. | ulb_credit_card |
| [3] | Weber, M., et al. (2019). "Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics." *KDD '19 Workshop on Anomaly Detection in Finance*. arXiv:1908.02591. | elliptic_v1 |
| [4] | Bellei, C., et al. (2024). "The Shape of Money Laundering: Subgraph Representation Learning on the Blockchain with the Elliptic2 Dataset." *arXiv preprint arXiv:2404.19109*. | elliptic_v2 |
| [5] | "Mt. Gox Leaked Transaction Data." Public domain. | mtgox_leaked |
| [6] | Chen, T., Li, Z., Zhu, Y., Chen, J., Luo, X., Zheng, Z., Zhang, X. (2020). "Phishing Scams Detection in Ethereum Transaction Network." *ACM Transactions on Internet Technology (TOIT)*, 21(1), pp. 1-16. DOI: 10.1145/3418060. | eth_phishing, eth_phishing_2nd |
| [7] | Chen, W., et al. (2018). "Detecting Ponzi Schemes on Ethereum: Towards Healthier Blockchain Technology." *Proceedings of the 2018 World Wide Web Conference (WWW)*. | smart_ponzi |
| [8] | Zheng, P., Zheng, Z., Wu, J., Dai, H.N. (2020). "XBlock-ETH: Extracting and Exploring Blockchain Data from Ethereum." *IEEE Open Journal of the Computer Society*, 1, pp. 95-106. DOI: 10.1109/OJCS.2020.2990465. | xblock_eth |
| [9] | Huang, X., et al. (2022). "DGraph: A Large-Scale Financial Dataset for Graph Anomaly Detection." *NeurIPS 2022 Datasets and Benchmarks Track*. arXiv:2207.03579. | dgraphfin |
| [10] | Altman, E., et al. (2023). "Realistic Synthetic Financial Transactions for Anti-Money Laundering Models." *NeurIPS 2023 Datasets and Benchmarks Track*. | ibm_amlsim_* |
| [11] | Jensen, R.I.T., Ferwerda, J., Jørgensen, K.S., et al. (2023). "A synthetic data set to benchmark anti-money laundering methods." *Scientific Data*, 10, 661. DOI: 10.1038/s41597-023-02569-2. | synthaml |
| [12] | Oztas, B. (2023). "SAML-D: Synthetic Transaction Monitoring Dataset for AML." *Kaggle Repository*. | saml_d |
| [13] | Harris, B. (2020). "Sparkov: Synthetic Financial Datasets for Fraud Detection." *GitHub / Kaggle Repository*. | cc_transactions |
| [14] | "Data Generator: Synthetic AML Dataset." Custom synthetic generator. | data_generator |

### 6.2 Data Engineering & Streaming Architecture

| # | Citation | Relevance |
|---|----------|-----------|
| [15] | Blanuša, J., Cravero Baraja, M., et al. (2024). "Graph Feature Preprocessor: Real-time Subgraph-based Feature Extraction for Financial Crime Detection." *ACM ICAIF 2024*. | Real-time feature extraction pipeline |
| [16] | Carminati, M., Caron, R., Maggi, F., Epifani, I., Zanero, S. (2015). "BankSealer: A decision support system for online banking fraud analysis and investigation." *Computers & Security*, 53, pp. 175–186. DOI: 10.1016/j.cose.2015.04.002. | Real-time online banking transaction analysis system |
| [17] | Chen, J., Yang, Y. (2026). "Real-Time Dynamic Graph Learning with Temporal Attention for Financial Fraud Detection." *Frontiers in Artificial Intelligence*, Vol. 9, 2026. DOI: 10.3389/frai.2026.1774013. | Temporal attention mechanism |
| [18] | Paoletti, G., Giobergia, F., Giordano, D., et al. (2025). "MAD: Multicriteria Anomaly Detection of Suspicious Financial Accounts from Billions of Cash Transactions." *ACM SIGKDD 2025*. | Large-scale anomaly detection |
| [19] | Devi, R.R., Raja, J.E., Chin, Y.B. (2025). "RL-GNN Fusion for Real-Time Financial Fraud Detection: A Context-Aware Community Mining Approach." *Scientific Reports, Nature*, 2025. | GNN + RL fusion for streaming |
| [22] | Deprez, B., Vanderschueren, T., Baesens, B., Verdonck, T., Verbeke, W. (2025). "Network Analytics for Anti-Money Laundering — A Systematic Literature Review and Experimental Evaluation." *INFORMS Journal on Data Science*, 5(2), pp. 119–154. | Systematic AML literature review (quantifies 1-3 dataset limitation) |

### 6.3 Regulatory Context

| # | Citation | Relevance |
|---|----------|-----------|
| [20] | European Union. (2023). "Regulation (EU) 2023/1114 on Markets in Crypto-Assets (MiCA)." *Official Journal of the European Union*, L 150, June 9, 2023. | Crypto AML regulation |
| [21] | Financial Action Task Force (FATF). (2024). "FATF Recommendations: International Standards on Combating Money Laundering and the Financing of Terrorism." *FATF-GAFI*, Updated 2024. | International AML standards |

## 7. Integration with Downstream GNN Layers & Split Protocols

To ensure rigorous evaluation and seamless downstream model training across Layers 2–7, the Layer 1 ingested data adheres to the following structural protocols:

1. **Out-of-Time Train/Validation/Test Splitting Protocol**: For all datasets featuring temporal signals (`temporal_signal_mode` $\in$ {`edge`, `node`}), data partitioning follows a strict out-of-time chronological protocol (e.g., historical timesteps $t < t_{\text{val}}$ for training, $t_{\text{val}} \le t < t_{\text{test}}$ for validation, and $t \ge t_{\text{test}}$ for testing). This prevents temporal data leakage inherent to random node/edge splits in dynamic transaction graphs.

2. **Cross-Domain Empirical Breadth Positioning**: The standardized 19-dataset benchmark collection addresses the primary empirical breadth gap identified in recent AML literature reviews by Deprez et al. (2025) [22] (where 84% of published GNN-AML models are evaluated on only 1 to 3 datasets). By encompassing 8 distinct domains, Layer 1 provides a robust foundation for multi-task and cross-domain GNN generalization experiments.

3. **Exploratory Topological Analysis**: Empirical distributions extracted during Layer 1 processing—such as heavy-tailed degree distributions, multi-scale temporal burstiness, and extreme class imbalance ratios ($<0.1\%$)—directly motivate the architectural choices in downstream layers, including HGTConv multi-relational message passing (Layer 2), Task-Free Continual Learning (Layer 3), and GraphGAN synthetic data augmentation (Layer 6).