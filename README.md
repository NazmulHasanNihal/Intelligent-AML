# Intelligent AML

A Neuro-Symbolic Framework for Omni-Channel Financial Fraud Detection via Temporal Graph Networks & Agentic AI.

## Project Architecture (Hybrid Execution)
- **Control Plane (Local):** Handles UI, Agentic Automation, and Orchestration.
- **Execution Plane (Kaggle/Cloud):** Handles massive data ingestion and PyTorch Geometric GPU training.

## Layers
1. **Layer 1:** Data Ingestion & Graph Construction (Polars / DuckDB). Heterogeneous node/edge typing is driven by `configs/model_config.yaml` (Account/User/Device/Institution × Transaction/IP_Connection/Shared_Ownership); every ingested edge carries a normalized `ts` (epoch seconds) column for the Burst-Aware Temporal Decay component, and a `_manifest.json` (SEED + content hashes) is written for reproducibility.
2. **Layer 2:** Detection & Rebalancing (HT-GNN / GraphGAN)
3. **Layer 3:** Federated Privacy (Flower / Opacus)
4. **Layer 4:** Causal Auditing (GNNExplainer / PyVis)
5. **Layer 5:** Agentic Automation (CrewAI / LangChain)
6. **Layer 6:** UI Verification (Streamlit)

## Getting Started
1. Install requirements: `pip install -r requirements.txt`
2. Configure `.env` based on `.env.example`.
3. **Run on Kaggle from your IDE (no Kaggle website needed):**
   - Download your API token from https://www.kaggle.com/settings → "Create New Token"
     and save it to `C:\Users\<you>\.kaggle\kaggle.json` (already git-ignored).
   - Verify: `python src/utils/run_remote.py setup`
   - Run any notebook/script on Kaggle's GPU and pull the output back to this PC:
     `python src/utils/run_remote.py run --target notebooks/Layer1_Ingestion/01_Layer1_Data_Ingestion_v4.ipynb`
     (or `make remote TARGET=notebooks/.../01_Layer1_Data_Ingestion_v4.ipynb`).
     This pushes your code, executes it on a free T4/P100, then downloads
     `graph_data/` + `_manifest.json` into `data/outputs/` automatically.
