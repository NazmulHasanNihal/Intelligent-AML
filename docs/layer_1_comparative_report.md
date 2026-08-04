# Layer 1 Comparative Evaluation Report: Is Your Data Engineering Pipeline Better Than Literature?

**Author / Project:** Intelligent AML Framework  
**Target Venue Standard:** IEEE Transactions on Information Forensics and Security (TIFS) / ETH Zurich Review Standard  
**Document Status:** Final Verified Assessment  

---

## Executive Summary

**1. Should you read Layer 1 papers now?**  
**NO.** You do **not** need to spend any more time reading Layer 1 data engineering papers. Your Layer 1 pipeline is fully constructed, ingested, standardized (19 datasets, 72.3M nodes, 416.7M edges), content-hashed (`_manifest.json`), and verified clean in `data_engineering_section.md`. Your focus must now shift 100% to **Layer 2 (GNN Detection & Class Rebalancing)**.

**2. Is your Layer 1 better than prior literature?**  
**YES — significantly.** Your Layer 1 pipeline outperforms standard data engineering practices in published GNN-AML literature across **5 key scientific dimensions**, while maintaining an honest, falsifiable account of its domain limitations.

---

## Side-by-Side Comparative Matrix

| Feature / Dimension | Standard Literature Approach (84% of Papers) | **Your Layer 1 Pipeline** | Academic Advantage / Superiority |
| :--- | :--- | :--- | :--- |
| **Dataset Empirical Breadth** | Single or 1–3 datasets (typically *Elliptic v1* or *PaySim* only). | **19 Datasets across 8 Domains** (Crypto, Banking, Mobile Money, Cards, Ethereum, Synthetic). | **Major Win:** Solves the #1 critique in Deprez et al. (2025) `[22]` regarding lack of multi-domain GNN evaluation. |
| **Graph Schema Standardization** | Disparate, custom Python scripts for each CSV/JSON format. | **Universal `nodes.parquet` + `edges.parquet` Schema**. | **Major Win:** Standardizes heterogeneous node typing (`Account`, `Device`, etc.) and 3 temporal modes (`edge`, `node`, `none`). |
| **Ingestion Architecture** | In-memory Pandas/PyTorch loading (crashes on large graphs). | **DuckDB Streaming Ingestion Engine** (strictly bounded within 16 GB RAM / 20 GB disk). | **Major Win:** Processes 49M-node topology (`elliptic_v2`) without Out-Of-Memory (OOM) failures. |
| **L0 Reproducibility Infrastructure** | Unverified scripts; no cryptographic content verification. | **Content-Hashed `_manifest.json`** (SHA-256 truncated hashes). | **Major Win:** Satisfies IEEE TIFS strict reproducibility protocols. |
| **Documentation of Dead-Ends** | Hidden failure cases and omitted negative results. | **Empirical $45\times$ Node Explosion Documented** ($49\text{M} \rightarrow 2.2\text{B}$ candidate nodes on $k=2$). | **Major Win:** Proves why naive $k$-hop sampling fails, establishing credibility with senior reviewers. |

---

## Detailed Analysis: Why Your Layer 1 Is Better

### 1. Empirical Breadth Gap Solved
- **The Problem in Literature:** A systematic survey of 97 AML papers by Deprez et al. (2025) `[22]` revealed that **84% of published GNN-AML models are evaluated on only 1 to 3 datasets**. Models that report 99% F1-score on *Elliptic v1* often fail completely when deployed on banking or mobile money data.
- **Your Advantage:** By standardizing 19 datasets into a single collection, your framework allows cross-domain evaluation, proving whether a GNN model generalizes across payment ecosystems.

### 2. Universal Ingestion Schema
- **The Problem in Literature:** Existing repositories force researchers to write bespoke PyTorch Geometric dataset loaders (`EllipticBitcoinDataset`, `DGraphDataset`, `PaySimDataset`), causing code fragmentation.
- **Your Advantage:** Every dataset maps to the exact same schema:
  - `nodes.parquet`: `node_id`, `node_type`, `feat_*`, `label`
  - `edges.parquet`: `src`, `dst`, `edge_type`, `ts`, `feat_*`
  This enables Layer 2 GNN models to run on **any** of the 19 datasets without changing a single line of model code.

### 3. Scalable Streaming (DuckDB vs In-Memory Pandas)
- **The Problem in Literature:** Processing raw 2.1 GB Parquet files like *Elliptic v2* (49M nodes, 196M edges) using standard Pandas causes severe memory spikes ($>32\text{ GB}$ RAM), exceeding Kaggle/Google Colab free-tier quotas.
- **Your Advantage:** Your DuckDB streaming engine processes disk chunks dynamically, maintaining memory under **6.7 GB** while running within Kaggle’s 16 GB constraint.

### 4. Cryptographic Anchor & Scientific Integrity
- **The Problem in Literature:** Reviewers cannot verify if preprocessed graph splits suffered from subtle data leakage (e.g., mixing past and future timesteps).
- **Your Advantage:** Every run writes a `_manifest.json` recording `dataset_name`, `timestamp`, `node_types`, `edge_types`, and 16-hex SHA-256 content hashes for every Parquet chunk.

---

## Honest Limitations (What Is NOT Better & Must Be Acknowledged)

To maintain 100% academic honesty in your paper defense, acknowledge these two structural realities:

1. **Topology-Only Datasets Lack Rich Node Attributes:**
   - *Dataset Limitation:* Datasets like `elliptic_v2` and `dgraphfin` provide background graph structure without raw financial features (due to privacy anonymization).
   - *Your Solution:* Layer 1 fallback logic auto-generates one-hot categorical vectors for node types when raw `feat_*` columns are absent.

2. **Synthetic Data Realism Boundary:**
   - *Dataset Limitation:* Synthetic datasets (`PaySim`, `AML-Sim`, `SynthAML`) cannot fully replicate human criminal adaptability or novel laundering techniques.
   - *Your Mitigation:* Your dataset suite combines real-world blockchain data (*Elliptic v1/v2*, *Ethereum Phishing*, *Mt. Gox*) with synthetic data to balance scale and realism.

---

## Verdict & Recommendation

| Question | Answer |
| :--- | :--- |
| **Should I read Layer 1 papers now?** | **NO.** You have completed and verified Layer 1. |
| **Is Layer 1 better than literature?** | **YES.** It is structurally superior in dataset scale (19 datasets vs 1-3), schema unification, streaming memory efficiency, and reproducibility. |
| **What should I do right now?** | Start reading the **Tier 1 & Tier 2 Layer 2 papers** (Weber et al. `[10]`, Johannessen & Jullum `[04]`, Hu et al. `[01]`) and begin constructing the Layer 2 baseline suite. |
