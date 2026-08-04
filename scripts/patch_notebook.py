import json
import os

nb_path = 'notebooks/Layer1_Ingestion/01_Layer1_Data_Ingestion_v4_COMPLETE.ipynb'

if not os.path.exists(nb_path):
    print("ERROR: Notebook not found at " + nb_path)
    exit(1)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

patched = False

for c in nb['cells']:
    if c['cell_type'] == 'code':
        source = "".join(c['source'])

        # Patch Cell 5 (imports and directories) — make OUTPUT_DIR local-only
        # ONLY for local execution. Do NOT apply this patch before pushing to Kaggle.
        if "import polars as pl" in source and "duckdb" in source:
            # replace kaggle/working with local data/outputs
            if "OUTPUT_DIR = Path(\"/kaggle/working/graph_data\")" in source:
                source = source.replace(
                    "if getattr(_sys, \"platform\", \"\") == \"linux\" and Path(\"/kaggle/working\").exists():\n    OUTPUT_DIR = Path(\"/kaggle/working/graph_data\")\n    TEMP_DIR = Path(\"/kaggle/temp\")\nelse:\n    OUTPUT_DIR = _repo_root() / 'data' / 'outputs' / 'graph_data'\n    TEMP_DIR = _repo_root() / 'data' / 'outputs' / '.duckdb_spill'",
                    "OUTPUT_DIR = Path(\"data/outputs\")\nTEMP_DIR = Path(\"data/temp\")"
                )
                patched = True

            c['source'] = [line + ('\n' if not line.endswith('\n') else '') for line in source.split('\n')][:-1]

        # Patch Cell 6 (dataset paths) — replace /kaggle/input/ with kagglehub
        # ONLY for local execution. Do NOT apply this patch before pushing to Kaggle.
        if "BASE_AML  = Path(" in source and "/kaggle/input/" in source:
            source = source.replace(
                "BASE_AML  = Path(\"/kaggle/input/datasets/nazmulhasannihal/aml-dataset/Dataset Collection for AML/Dataset Collection for AML\")",
                "BASE_AML  = Path(kagglehub.dataset_download(\"nazmulhasannihal/aml-dataset\")) / \"Dataset Collection for AML\" / \"Dataset Collection for AML\""
            )
            source = source.replace(
                "BASE_ROOT = Path(\"/kaggle/input/datasets/nazmulhasannihal/aml-dataset\")",
                "BASE_ROOT = Path(kagglehub.dataset_download(\"nazmulhasannihal/aml-dataset\"))"
            )
            source = source.replace(
                "Path(\"/kaggle/input/datasets/berkanoztas/synthetic-transaction-monitoring-dataset-aml/SAML-D.csv\")",
                "Path(kagglehub.dataset_download(\"berkanoztas/synthetic-transaction-monitoring-dataset-aml\")) / \"SAML-D.csv\""
            )
            source = source.replace(
                "Path(\"/kaggle/input/datasets/organizations/ellipticco/elliptic2-data-set\")",
                "Path(kagglehub.dataset_download(\"organizations/ellipticco/elliptic2-data-set\"))"
            )
            source = source.replace(
                "Path(\"/kaggle/input/datasets/tczplv/xblocketh\")",
                "Path(kagglehub.dataset_download(\"tczplv/xblocketh\"))"
            )
            source = source.replace(
                "IBM_AML_BASE = Path(\"/kaggle/input/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml\")",
                "IBM_AML_BASE = Path(kagglehub.dataset_download(\"ealtman2019/ibm-transactions-for-anti-money-laundering-aml\"))"
            )
            patched = True
            c['source'] = [line + ('\n' if not line.endswith('\n') else '') for line in source.split('\n')][:-1]

        # Patch Cell 2 (pip install) — add kagglehub
        if "!pip install" in source and "kagglehub" not in source:
            source = source.replace("fastexcel", "fastexcel kagglehub")
            patched = True
            c['source'] = [line + ('\n' if not line.endswith('\n') else '') for line in source.split('\n')][:-1]

        # Patch download instructions
        if "Look at the 'Output' section" in source:
            source = source.replace(
                "print(\"\\n\\U0001f4e5 HOW TO DOWNLOAD:\")\nprint(\"1. Look at the 'Output' section in the right-hand panel of your Kaggle notebook.\")\nprint(\"2. You will see a folder named 'graph_data'.\")\nprint(\"3. Click the Download icon next to it.\")\nprint(\"4. Extract into your local 'data' folder for Layer 2.\")",
                "print(\"\\n\\U0001f4e5 HOW TO USE:\")\nprint(\"1. The output files have been saved to data/outputs\")\nprint(\"2. You can use these files directly for Layer 2.\")"
            )
            patched = True
            c['source'] = [line + ('\n' if not line.endswith('\n') else '') for line in source.split('\n')][:-1]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

if patched:
    print("WARNING: Notebook has been patched for LOCAL execution only.")
    print("  - OUTPUT_DIR changed to data/outputs (local path)")
    print("  - Dataset paths changed to use kagglehub downloads")
    print("  - kagglehub added to pip install")
    print("")
    print("DO NOT push this patched notebook to Kaggle.")
    print("To push to Kaggle, revert with: git checkout HEAD -- " + nb_path)
    print("To run locally, place datasets in data/raw/ first.")
else:
    print("No patches applied (notebook already patched or not matching expected patterns).")

print("Notebook patched successfully!")