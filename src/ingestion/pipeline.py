"""
Omni-Channel Data Ingestion Pipeline (v4)

This module contains the DuckDB-based data ingestion logic.
"""

# --- CELL BREAK ---

import polars as pl
import numpy as np
import duckdb
import os
import sys
import time
import json
import hashlib
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# `resource` is Unix-only (used for peak-RAM reporting). Guard it so the pipeline
# also imports on Windows (local control plane / CI), where it is unavailable.
try:
    import resource  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - Windows
    resource = None  # type: ignore
from pathlib import Path

print(f"Polars version: {pl.__version__}")
print(f"DuckDB version: {duckdb.__version__}")

# ─────────────────────────────────────────────────────────────────────────────
# Reproducibility (L0) — locked seed + config-anchored typing.
# ETH Zurich / IEEE TIFS reviewers expect exact reproducibility; SEED is the
# single global knob. We set it here so every Layer-1 run is deterministic.
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
os.environ.setdefault("PYTHONHASHSEED", str(SEED))
np.random.seed(SEED)

# Heterogeneous typing is driven by model_config.yaml so Layer 1 and Layer 2
# agree on the node/edge vocabulary. This is what makes the HT-GNN *heterogeneous*.
# NOTE: __file__ is NOT defined inside a Jupyter/Kaggle notebook cell, so we resolve
# the repo root without relying on it (falls back through CWD / common parents).
def _repo_root():
    """Locate the project root containing configs/, robust to running as a module
    OR inside a notebook cell where __file__ is undefined."""
    candidates = []
    try:
        if "__file__" in globals():
            candidates.append(Path(globals()["__file__"]).resolve().parent.parent.parent)
    except Exception:
        pass
    candidates.append(Path.cwd())
    candidates.append(Path("/kaggle/working"))  # Kaggle notebook working dir
    for c in candidates:
        if (c / "configs" / "model_config.yaml").exists():
            return c
    # Fallback: walk up from CWD looking for configs/
    cur = Path.cwd()
    for _ in range(6):
        if (cur / "configs").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return candidates[0]

_CONFIG_PATH = _repo_root() / "configs" / "model_config.yaml"

def _load_graph_types():
    """Load node/edge types from configs/model_config.yaml.

    Falls back to the canonical v4 vocabulary if the config is missing, so the
    pipeline never hard-codes a single 'Entity'/'transaction' type.
    """
    default_node_types = ["Account", "User", "Device", "Institution"]
    default_edge_types = ["Transaction", "IP_Connection", "Shared_Ownership"]
    if not _CONFIG_PATH.exists():
        return default_node_types, default_edge_types
    try:
        import yaml  # PyYAML
        with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        graph = cfg.get("graph", {}) or {}
        node_types = graph.get("node_types") or default_node_types
        edge_types = graph.get("edge_types") or default_edge_types
        return list(node_types), list(edge_types)
    except Exception:
        return default_node_types, default_edge_types

NODE_TYPES, EDGE_TYPES = _load_graph_types()
DEFAULT_NODE_TYPE = NODE_TYPES[0] if NODE_TYPES else "Entity"
DEFAULT_EDGE_TYPE = EDGE_TYPES[0] if EDGE_TYPES else "transaction"

# --- Output vs. scratch space (see markdown above for why these are different) ---
# On Kaggle the working dir is /kaggle/working; elsewhere (local control plane /
# CI / Windows) fall back to a project-local data/outputs path so the module
# imports and runs anywhere without a Kaggle session.
import sys as _sys
if getattr(_sys, "platform", "") == "linux" and Path("/kaggle/working").exists():
    OUTPUT_DIR = Path("/kaggle/working/graph_data")
    TEMP_DIR = Path("/kaggle/temp")
else:
    OUTPUT_DIR = _repo_root() / "data" / "outputs" / "graph_data"
    TEMP_DIR = _repo_root() / "data" / "outputs" / ".duckdb_spill"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# --- DuckDB engine: memory-bounded, spills to TEMP_DIR, uses all available cores ---
# Tune DUCKDB_MEMORY_LIMIT_GB down if your Kaggle instance shows less RAM available
# (check the resource panel on the right side of the Kaggle notebook UI).
DUCKDB_MEMORY_LIMIT_GB = 8

# Lazy DuckDB connection: importing pipeline.py is instant and lightweight.
# `con` is a thin proxy that spins up the real in-memory engine on first
# .execute()/.register() call, so importing for helpers/tests costs ~nothing.
class _LazyDuckDB:
    def __init__(self):
        self._conn = None

    def _ensure(self):
        if self._conn is None:
            self._conn = duckdb.connect(database=":memory:")
            self._conn.execute(f"PRAGMA memory_limit='{DUCKDB_MEMORY_LIMIT_GB}GB'")
            self._conn.execute(f"PRAGMA temp_directory='{TEMP_DIR}'")
            # Let DuckDB auto-use available cores (omit threads pragma rather than
            # risk an invalid value on some versions).
        return self._conn

    def execute(self, *a, **k):
        return self._ensure().execute(*a, **k)

    def register(self, *a, **k):
        return self._ensure().register(*a, **k)

    def cursor(self, *a, **k):
        return self._ensure().cursor(*a, **k)


con = _LazyDuckDB()

def report_resources(tag=""):
    """Prints free disk space (both dirs) and peak RAM used so far in this process."""
    out_du = shutil.disk_usage(OUTPUT_DIR)
    tmp_du = shutil.disk_usage(TEMP_DIR)
    if resource is not None:
        ram_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB -> MB on Linux
        ram_str = f"| peak RAM so far {ram_mb:,.0f} MB"
    else:  # Windows / non-POSIX: RAM peak unavailable, report disk only
        ram_str = ""
    label = f" [{tag}]" if tag else ""
    print(f"  \U0001f4ca resources{label}: output disk free {out_du.free/1e9:.1f} GB | "
          f"temp disk free {tmp_du.free/1e9:.1f} GB {ram_str}")

def check_disk_space(path=None, required_mb=None):
    """Pre-flight check before attempting a large write - lets a loader skip itself gracefully
    (e.g. IBM AML's Large tiers, Elliptic v2's background) instead of crashing mid-write and
    taking other datasets down with it."""
    du = shutil.disk_usage(path or OUTPUT_DIR)
    free_mb = du.free / (1024 * 1024)
    return {"free_mb": free_mb, "required_mb": required_mb,
            "insufficient": (required_mb is not None and free_mb < required_mb)}

def run_safely(step_name, func, *args, **kwargs):
    """
    Runs one dataset's ingestion and NEVER lets its failure kill the rest of the notebook.
    This is the direct fix for the v3 bug where Elliptic v2's disk-full error silently
    prevented every dataset after it from running at all.
    """
    print(f"\n{'='*70}\n\U0001f504 {step_name}\n{'='*70}")
    t0 = time.time()
    try:
        func(*args, **kwargs)
        RESULTS[step_name] = "SUCCESS"
        print(f"  \u2705 {step_name} completed in {time.time()-t0:.1f}s")
    except Exception as e:
        RESULTS[step_name] = f"FAILED: {type(e).__name__}: {e}"
        print(f"  \u274c {step_name} FAILED after {time.time()-t0:.1f}s: {type(e).__name__}: {e}")
        print(f"  \u2192 Continuing to the next dataset — this dataset's output may be missing or partial.")
    report_resources(step_name)

RESULTS = {}  # dataset_name -> "SUCCESS" | "FAILED: ..."

# --- CELL BREAK ---

def is_kaggle():
    """Returns True when running on Kaggle's Execution Plane (datasets mounted
    at /kaggle/input/), so the pipeline can skip all download logic and use
    the already-available paths directly."""
    return Path("/kaggle/input").exists()


def _resolve_raw_dir(kaggle_path, relative_subpath="", auto_download=False):
    """Returns kaggle_path if it exists; otherwise probes local project folders.
    If auto_download=True and the dataset is a known Kaggle dataset, attempts
    to download it via kagglehub before giving up. Skips all download logic
    when running on Kaggle (datasets are already mounted)."""
    kp = Path(kaggle_path)
    if kp.exists():
        return kp
    if is_kaggle():
        return kp
    local_candidates = [
        _repo_root() / "data" / "raw" / relative_subpath,
        _repo_root() / "data" / "inputs" / relative_subpath,
        _repo_root() / "data" / relative_subpath,
        _repo_root() / relative_subpath,
    ]
    for loc in local_candidates:
        if loc.exists():
            return loc
    # Try kagglehub auto-download for known datasets (local only)
    if auto_download:
        kaggle_slug = _kaggle_path_to_slug(kaggle_path)
        if kaggle_slug:
            try:
                import kagglehub
                print(f"  [kagglehub] Downloading {kaggle_slug} ...")
                path = kagglehub.dataset_download(kaggle_slug)
                print(f"  [kagglehub] Downloaded to: {path}")
                # If the kaggle_path points to a subfolder inside the dataset,
                # try to resolve it relative to the downloaded path
                if relative_subpath:
                    resolved = Path(path) / relative_subpath
                    if resolved.exists():
                        return resolved
                return Path(path)
            except Exception as e:
                print(f"  [kagglehub] Download failed for {kaggle_slug}: {e}")
    return kp


def _kaggle_path_to_slug(kaggle_path):
    """Convert a /kaggle/input/... path to a kagglehub slug.
    e.g. /kaggle/input/datasets/nazmulhasannihal/aml-dataset -> nazmulhasannihal/aml-dataset"""
    p = str(kaggle_path)
    # Match /kaggle/input/datasets/<owner>/<dataset> or /kaggle/input/<owner>/<dataset>
    import re
    m = re.search(r'/kaggle/input/(?:datasets/)?([^/]+/[^/]+)', p)
    if m:
        return m.group(1)
    return None

BASE_AML  = _resolve_raw_dir("/kaggle/input/datasets/nazmulhasannihal/aml-dataset/Dataset Collection for AML/Dataset Collection for AML", "Dataset Collection for AML")
BASE_ROOT = _resolve_raw_dir("/kaggle/input/datasets/nazmulhasannihal/aml-dataset", "aml-dataset")

DATASETS = {
    # --- Module A: Traditional Fiat & Fraud ---
    "paysim1":           BASE_AML / "PaySim1 (Standard Baseline)",
    "paysim_extended":   BASE_AML / "PaySim Dataset (Generated Data)",
    "synthaml":          BASE_AML / "SynthAML (Spar Nord Bank)" / "synthetic_alerts.csv",
    "ulb_credit_card":   BASE_AML / "Credit Card Fraud Detection" / "creditcard.csv",
    "cc_transactions":   BASE_AML / "credit-card-transactions",
    "saml_d":            _resolve_raw_dir("/kaggle/input/datasets/berkanoztas/synthetic-transaction-monitoring-dataset-aml/SAML-D.csv", "SAML-D.csv"),

    # --- Module B: Crypto & Web3 ---
    "elliptic_v1":       BASE_AML / "Elliptic Bitcoin (Original)" / "elliptic_bitcoin_dataset",
    "elliptic_v2":       _resolve_raw_dir("/kaggle/input/datasets/organizations/ellipticco/elliptic2-data-set", "elliptic2-data-set"),
    "mtgox_leaked":      BASE_AML / "Mt.Gox Leaked Transaction" / "Mt.Gox Leaked Transaction" / "complete_edge_v2.csv",
    "eth_phishing":      BASE_AML / "Ethereum Phishing Transaction Network" / "Ethereum Phishing Transaction Network" / "MulDiGraph.pkl",
    "eth_phishing_2nd":  BASE_AML / "Second-order Transaction Network of Phishing Nodes",
    "smart_ponzi":       BASE_AML / "Smart Ponzi Scheme Labels" / "Smart Ponzi Scheme Labels",
    "xblock_eth":        _resolve_raw_dir("/kaggle/input/datasets/tczplv/xblocketh", "xblocketh"),

    # --- Module C: Specialized ---
    "dgraphfin":         BASE_ROOT / "DGraphFin" / "dgraphfin.npz",
    "data_generator":    BASE_AML / "Data Generator" / "generated_dataset" / "aml_dataset.pt",
}

# --- IBM AML dataset (the real one, replacing the previous missing-file placeholder) ---
# This is a DIFFERENT Kaggle dataset than the old "AML-Data-Public" folder (which only ever
# had documentation, confirmed earlier) - this is "IBM Transactions for Anti Money Laundering
# (AML)" by ealtman2019, matching the URL from your original 16-dataset list. It ships 6 tiers
# (HI/LI illicit-ratio x Small/Medium/Large scale), each with a transaction graph, an account
# lookup table, and a Patterns.txt file listing exactly which transactions form which specific
# laundering scheme - genuinely valuable typology-validation data, parsed with a dedicated
# parser below (it's a structured text format, not CSV).
#
# PATH IS A BEST-GUESS, following the same mount convention as your other individual-account
# Kaggle datasets (saml_d/berkanoztas, xblock_eth/tczplv): /kaggle/input/datasets/<username>/
# <dataset-slug>/. Verify via the Path Check output below - if it shows [!!], the diagnostic
# message will tell you what's actually there, same as every other path issue resolved so far.
IBM_AML_BASE = _resolve_raw_dir("/kaggle/input/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml", "ibm-transactions-for-anti-money-laundering-aml")

# tier_key -> file prefix (e.g. "HI-Small" -> HI-Small_Trans.csv, HI-Small_accounts.csv, HI-Small_Patterns.txt)
# Ordered small-to-large deliberately - if disk runs tight, earlier (smaller) tiers still succeed.
IBM_AML_TIERS = {
    "ibm_amlsim_hi_small":  "HI-Small",
    "ibm_amlsim_li_small":  "LI-Small",
    "ibm_amlsim_hi_medium": "HI-Medium",
    "ibm_amlsim_li_medium": "LI-Medium",
    "ibm_amlsim_hi_large":  "HI-Large",
    "ibm_amlsim_li_large":  "LI-Large",
}
# The Data Explorer showed 41.61 GB total across all 18 files (6 tiers x 3 files) - the Large
# tiers are almost certainly the dominant contributors (matches the known scale of this public
# dataset: Large tiers run to hundreds of millions of transactions). Defaults to False so Small
# + Medium (4 tiers) run safely first; flip to True only once you've confirmed there's room.
IBM_AML_INCLUDE_LARGE = False

# Registered here too so the Path Check below reports their status individually.
for _tier_key, _prefix in IBM_AML_TIERS.items():
    DATASETS[_tier_key] = IBM_AML_BASE / f"{_prefix}_Trans.csv"

# Elliptic v2 background config (see the Elliptic v2 section below). Confirmed by direct
# measurement: this graph has hub nodes with enormous degree - a K-hop BFS from the labeled
# subgraph exploded 45x in a single hop (737,870 -> 33,788,526 nodes), so neighborhood sampling
# is NOT done here. Background is written in full (nodes with features, edges as topology only -
# see the Elliptic v2 section for why). Set to False only if disk is still tight even for that.
ELLIPTIC2_INCLUDE_BACKGROUND = True


def _startup_diagnostics():
    """Print resource + dataset-path status. Called by run_all_datasets()/CLI,
    NOT at import time, so importing the module stays instant and quiet."""
    report_resources("startup")
    print("Path Check:")
    for name, path in DATASETS.items():
        marker = "[OK]" if path.exists() else "[!!]"
        kind = "file" if (path.exists() and path.is_file()) else "folder" if path.exists() else "?"
        print(f"  {marker} {name:20s} [{kind:6s}] -> {path}")


# --- CELL BREAK ---

# Master hint lists — matched case-insensitively against stripped column names.
# The more complete this list, the more new/unfamiliar datasets auto-detect correctly
# without needing hand-written hints — this is what makes the engine "universal."
SRC_HINTS = [
    "Sender_account", "nameOrig", "From", "from", "SENDER_ACCOUNT_ID",
    "from_address", "src", "source", "User", "sender", "payer", "Account",
]
DST_HINTS = [
    "Receiver_account", "nameDest", "To", "to", "RECEIVER_ACCOUNT_ID",
    "to_address", "dst", "target", "Merchant Name", "Merchant", "receiver", "payee", "Account_1",
]
LABEL_HINTS = [
    "Is_laundering", "isFraud", "is_fraud", "Is Fraud?", "IS_LAUNDERING",
    "label", "class", "Label", "Errors?", "Is Laundering",
]

# Temporal signal hints — Burst-Aware Temporal Decay (Innovation 1) needs a real
# time-order column. Dataset column names vary wildly across 18+ sources, so we
# probe for any of these case-insensitively and normalize to a single `ts` column.
TS_HINTS = [
    "timestamp", "time_stamp", "datetime", "date_time", "created_at", "tx_time",
    "time", "date", "step", "time_step", "timestep", "block_number", "blocknumber",
    "blocktimestamp", "block_timestamp", "transactiontime", "event_time", "ts",
]


def find_timestamp_column(cols):
    """Case-insensitive hint match for a temporal column among real column names."""
    lower_map = {c.lower(): c for c in cols}
    for h in TS_HINTS:
        if h in lower_map:
            return lower_map[h]
    return None


def normalize_timestamp_expr(ts_col):
    """Returns a DuckDB SQL expression that casts any supported timestamp column
    to a normalized epoch (DOUBLE, seconds since 1970-01-01) named `ts`.

    Handles: epoch strings, ISO datetimes, integer 'step'/block heights, and
    already-numeric timestamps. Non-parseable values become NULL (not a crash),
    so a missing/odd temporal column never aborts ingestion.
    """
    return (
        f"TRY_CAST({ts_col} AS TIMESTAMP) AS _ts_tmp, "
        f"CASE WHEN _ts_tmp IS NOT NULL THEN CAST(EXTRACT(EPOCH FROM _ts_tmp) AS DOUBLE) "
        f"     WHEN TRY_CAST({ts_col} AS DOUBLE) IS NOT NULL THEN TRY_CAST({ts_col} AS DOUBLE) "
        f"     ELSE NULL END AS ts"
    )


def build_files_sql(files):
    """['a.csv', 'b.csv', ...] literal for DuckDB read_csv_auto()."""
    return "[" + ", ".join(f"'{str(f)}'" for f in files) + "]"


def stripped_raw_sql(files):
    """
    Returns (sql_subquery, stripped_column_names).

    Uses DuckDB's own type sniffer (NOT all_varchar=true) so numeric columns come out of
    Layer 1 as actual Float64/Int64 in the parquet, not strings Layer 2 has to remember to
    cast on every load. Tested directly against the exact failure that crashed v3
    (`'1e+05'` deep inside a column DuckDB samples as BIGINT from earlier clean rows):
    with `ignore_errors=true`, DuckDB parses it correctly as 100000 rather than throwing —
    its sniffer/caster is meaningfully more capable here than Polars' early-row heuristic
    was. `ignore_errors=true` is kept as the safety net for any row DuckDB genuinely can't
    parse (it becomes NULL instead of aborting the whole file), so a single bad row can
    never take down the read.
    Also renames every column to its whitespace-stripped form so hint-matching doesn't
    silently fail on datasets like XBlock-ETH whose real headers are ' from', ' to', etc.

    Defensive fix: any column whose name matches a known src/dst ID hint is forced to VARCHAR
    at read time. Verified this matters — DuckDB's sniffer treats short hex-looking strings like
    '0xaaa' as integer literals (0xaaa == 2730 in decimal) and silently corrupts them. Real
    Ethereum addresses (42 chars) are long enough to overflow any integer type and stay safe by
    accident, but there's no guarantee every dataset's IDs are that long, so this is forced
    explicitly rather than relied upon.
    """
    files_sql = build_files_sql(files)
    probe = f"read_csv_auto({files_sql}, union_by_name=true, ignore_errors=true)"
    cur = con.execute(f"SELECT * FROM {probe} LIMIT 0")
    raw_cols = [d[0] for d in cur.description]

    id_hint_names = {h.lower() for h in (SRC_HINTS + DST_HINTS)}
    force_varchar = [c for c in raw_cols if c.strip().lower() in id_hint_names]
    types_sql = ""
    if force_varchar:
        types_dict = "{" + ", ".join(f"'{c}': 'VARCHAR'" for c in force_varchar) + "}"
        types_sql = f", types={types_dict}"

    base = f"read_csv_auto({files_sql}, union_by_name=true, ignore_errors=true{types_sql})"
    select_list = ", ".join(f'"{c}" AS "{c.strip()}"' for c in raw_cols)
    sql = f"(SELECT {select_list} FROM {base})"
    return sql, [c.strip() for c in raw_cols]


def find_column(hints, cols):
    """Case-insensitive, exact-match-first search of hints against real column names."""
    lower_map = {c.lower(): c for c in cols}
    for h in hints:
        if h in cols:
            return h
        if h.lower() in lower_map:
            return lower_map[h.lower()]
    return None


def discover_csv_files(path):
    """Handles a direct .csv/.txt file OR a folder containing one or more CSVs (multi-shard aware).
    .txt is included because IBM's AML transaction data ships as trans_3000p2_list.txt - a
    delimited text file DuckDB's CSV reader handles fine once pointed at it directly."""
    if not path.exists():
        return []
    if path.is_file() and path.suffix.lower() in (".csv", ".csv.gz", ".tsv", ".txt"):
        return [path]
    found = sorted(path.rglob("*.csv")) + sorted(path.rglob("*.csv.gz")) + sorted(path.rglob("*.tsv"))
    return sorted(set(found))


def diagnose_empty_folder(path, max_items=25):
    """When no CSVs are found, list what's actually there (any extension, one level of
    subfolders) so the resulting error message is self-diagnosing - no extra round-trip needed
    to find out this dataset actually ships .txt/.json/.parquet or is nested one level deeper."""
    if not path.exists():
        return f"path does not exist: {path}"
    if path.is_file():
        return f"is a file, not a folder: {path.name}"
    entries = list(path.iterdir())
    if not entries:
        return "folder exists but is completely empty"
    names = [f"{e.name}{'/' if e.is_dir() else ''}" for e in entries[:max_items]]
    more = f" (+{len(entries) - max_items} more)" if len(entries) > max_items else ""
    return f"folder contains {len(entries)} item(s), e.g.: {names}{more}"


def ingest_transaction_csv(dataset_name, path, out_name=None, edge_type_name=None,
                            src_hints=None, dst_hints=None, label_hints=None,
                            node_type=None, src_node_type=None, dst_node_type=None):
    """Universal graph loader: streams CSV -> nodes.parquet + edges.parquet via DuckDB.

    Heterogeneous typing (v4 fix):
      - `node_type` forces every node to one type (e.g. Account), or
      - `src_node_type`/`dst_node_type` assign different types to the two endpoints
        (e.g. User -> Merchant), enabling a truly heterogeneous HT-GNN.
      - `edge_type_name` defaults to the first configured edge type.
    A normalized `ts` (epoch seconds, DOUBLE) column is emitted when a temporal
    column is auto-detected, so Burst-Aware Temporal Decay has a uniform input.
    """
    out_name = out_name or dataset_name
    edge_type_name = edge_type_name or DEFAULT_EDGE_TYPE
    files = discover_csv_files(path)
    if not files:
        # Raise (rather than silently returning) so run_safely correctly logs this as a
        # FAILED/missing dataset in the final report, instead of a misleading "SUCCESS"
        # for a dataset that never actually produced any output. Include a live directory
        # listing so the error is actionable immediately, without a second round-trip.
        raise FileNotFoundError(f"no CSV/TSV files found under {path} -- {diagnose_empty_folder(path)}")
    print(f"  Found {len(files)} file(s): {[f.name for f in files]}")

    raw_sql, cols = stripped_raw_sql(files)
    print(f"  Columns: {cols}")

    src_col = find_column(src_hints or SRC_HINTS, cols)
    dst_col = find_column(dst_hints or DST_HINTS, cols)
    label_col = find_column(label_hints or LABEL_HINTS, cols)
    ts_col = find_timestamp_column(cols)

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)

    if not src_col or not dst_col:
        print(f"  [INFO] No src/dst pair detected — not a transaction graph. Saving as raw table.")
        ingest_tabular_csv(dataset_name, path, out_name=out_name, _prefetched=(raw_sql, cols))
        return

    print(f"  Auto-Detected: SRC='{src_col}' | DST='{dst_col}' | LABEL='{label_col}' | TS='{ts_col}'")

    label_expr = f'"{label_col}"' if label_col else "-1"
    exclude_set = {src_col, dst_col} | ({label_col} if label_col else set())
    exclude_sql = ", ".join(f'"{c}"' for c in exclude_set)

    # Heterogeneous node typing
    s_type = src_node_type or node_type or DEFAULT_NODE_TYPE
    d_type = dst_node_type or node_type or DEFAULT_NODE_TYPE

    nodes_path = out_dir / "nodes.parquet"
    edges_path = out_dir / "edges.parquet"

    nodes_sql = f"""
        COPY (
            SELECT node_id, node_type FROM (
                SELECT TRIM("{src_col}") AS node_id, '{s_type}' AS node_type FROM {raw_sql}
                UNION ALL
                SELECT TRIM("{dst_col}") AS node_id, '{d_type}' AS node_type FROM {raw_sql}
            ) t
            WHERE node_id IS NOT NULL AND node_id != ''
            QUALIFY ROW_NUMBER() OVER (PARTITION BY node_id) = 1
        ) TO '{nodes_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """
    ts_select = normalize_timestamp_expr(ts_col) if ts_col else "NULL AS ts"
    edges_sql = f"""
        COPY (
            SELECT
                TRIM("{src_col}") AS src,
                TRIM("{dst_col}") AS dst,
                {label_expr} AS label,
                '{edge_type_name}' AS edge_type,
                {ts_select},
                * EXCLUDE ({exclude_sql}{", " + ts_col if ts_col else ""})
            FROM {raw_sql}
            WHERE "{src_col}" IS NOT NULL AND "{dst_col}" IS NOT NULL
        ) TO '{edges_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """
    con.execute(nodes_sql)
    con.execute(edges_sql)

    n_nodes = con.execute(f"SELECT COUNT(*) FROM '{nodes_path}'").fetchone()[0]
    n_edges = con.execute(f"SELECT COUNT(*) FROM '{edges_path}'").fetchone()[0]
    ts_note = f" | ts from '{ts_col}'" if ts_col else " | NO temporal signal"
    print(f"  Saved Graph: {n_nodes:,} nodes ({s_type}/{d_type}) | {n_edges:,} edges "
          f"({edge_type_name}){ts_note} "
          f"| {len(cols) - len(exclude_set)} extra edge feature cols preserved")


def diagnose_multi_file_dataset(dataset_name, path, src_hints=None, dst_hints=None):
    """
    For a folder with multiple CSVs, checks whether they're genuinely shards of the same table
    or actually different logical tables (e.g. a transaction log + a user lookup table) that
    the shard-detection heuristic incorrectly merged just because they're similar file sizes.

    Reports, per SOURCE FILE: row count, and what fraction of its rows are NULL on the
    dataset's auto-detected src/dst columns. A file with 100% null src/dst almost certainly
    doesn't belong merged in - it's a different table (e.g. a card/user metadata file with no
    transaction columns at all), not a shard.
    """
    files = discover_csv_files(path)
    if not files:
        print(f"  No files found for {dataset_name}")
        return

    src_hints = src_hints or SRC_HINTS
    dst_hints = dst_hints or DST_HINTS

    print("")
    print("=" * 70)
    print(f"DIAGNOSTIC: {dataset_name} ({len(files)} file(s))")
    print("=" * 70)
    for f in files:
        print(f"  - {f.name}")

    raw_sql, cols = stripped_raw_sql(files)
    src_col = next((c for c in src_hints if c in cols), None)
    dst_col = next((c for c in dst_hints if c in cols), None)
    print("")
    print(f"Auto-detected across the MERGED schema: SRC='{src_col}' DST='{dst_col}'")

    if not src_col or not dst_col:
        print("  No src/dst detected at all across any file - nothing to check per-file.")
        return

    files_sql = build_files_sql(files)
    q = f"""
        SELECT filename,
               COUNT(*) AS total_rows,
               COUNT(*) FILTER (WHERE "{src_col}" IS NULL OR "{dst_col}" IS NULL) AS null_src_or_dst,
               ROUND(100.0 * COUNT(*) FILTER (WHERE "{src_col}" IS NULL OR "{dst_col}" IS NULL)
                     / COUNT(*), 1) AS pct_null
        FROM read_csv_auto({files_sql}, union_by_name=true, ignore_errors=true, filename=true)
        GROUP BY filename
        ORDER BY pct_null DESC
    """
    result = con.execute(q).fetchall()
    print("")
    header = f"{'file':<60} {'rows':>10} {'null src/dst':>13} {'%':>7}"
    print(header)
    print("-" * 92)
    for filename, total, nulls, pct in result:
        short_name = Path(filename).name
        flag = "  <-- LIKELY NOT A REAL SHARD, check before using" if pct >= 90 else ""
        print(f"{short_name:<60} {total:>10,} {nulls:>13,} {pct:>6.1f}%{flag}")
    print()


def ingest_tabular_csv(dataset_name, path, out_name=None, _prefetched=None):
    """For datasets with no natural entity graph — streams the whole file to raw_table.parquet."""
    out_name = out_name or dataset_name
    if _prefetched is not None:
        raw_sql, cols = _prefetched
    else:
        files = discover_csv_files(path)
        if not files:
            raise FileNotFoundError(f"no CSV/TSV files found under {path} -- {diagnose_empty_folder(path)}")
        raw_sql, cols = stripped_raw_sql(files)
        print(f"  Columns: {cols}")

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "raw_table.parquet"

    con.execute(f"COPY (SELECT * FROM {raw_sql}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    n_rows = con.execute(f"SELECT COUNT(*) FROM '{out_path}'").fetchone()[0]
    print(f"  Saved: {n_rows:,} rows as raw table (no graph structure)")

# --- CELL BREAK ---

def load_elliptic_v1(folder_path, out_name="elliptic_v1"):
    if not folder_path.exists():
        raise FileNotFoundError(f"folder missing -> {folder_path}")

    feat_file  = next(folder_path.glob("*features*.csv"), None)
    class_file = next(folder_path.glob("*classes*.csv"), None)
    edge_file  = next(folder_path.glob("*edgelist*.csv"), None)
    if not all([feat_file, class_file, edge_file]):
        raise FileNotFoundError(f"missing one of features/classes/edgelist. Found: {list(folder_path.glob('*.csv'))}")

    print(f"  Joining {feat_file.name}, {class_file.name}, {edge_file.name}")

    # Features file has NO header: txId, time_step, then 165 anonymized feature columns
    df_feat = pl.read_csv(feat_file, has_header=False)
    n_feat_cols = df_feat.width - 2
    df_feat.columns = ["txId", "time_step"] + [f"feat_{i}" for i in range(n_feat_cols)]

    df_class = pl.read_csv(class_file)
    df_class = df_class.with_columns(
        pl.when(pl.col("class") == "1").then(1)
          .when(pl.col("class") == "2").then(0)
          .otherwise(-1).alias("label")
    )

    df_edges = pl.read_csv(edge_file).rename({"txId1": "src", "txId2": "dst"})
    df_nodes = df_feat.join(df_class.select(["txId", "label"]), on="txId", how="left")
    # Heterogeneous typing: Elliptic transactions are 'User' nodes (Bitcoin addresses).
    df_nodes = df_nodes.with_columns(pl.lit("User").alias("node_type"))
    # Burst-Aware Temporal Decay needs `ts` on edges; Elliptic's time lives on NODES
    # (txId -> time_step). Join node time_step onto each edge so Layer 2 reads one uniform field.
    ts_lookup = df_nodes.select(["txId", "time_step"]).with_columns(
        (pl.col("time_step").cast(pl.Float64) * 1.0).alias("ts"))
    df_edges = df_edges.join(ts_lookup, left_on="src", right_on="txId", how="left").rename(
        {"ts": "ts_src"}).join(ts_lookup, left_on="dst", right_on="txId", how="left")
    df_edges = df_edges.with_columns(
        pl.when(pl.col("ts_src").is_not_null()).then(pl.col("ts_src"))
         .otherwise(pl.col("ts")).alias("ts")).drop(["ts_src", "ts_right"] if "ts_right" in df_edges.columns else ["ts_src"])
    # ensure a clean `ts` column exists (NULL if absent)
    if "ts" not in df_edges.columns:
        df_edges = df_edges.with_columns(pl.lit(None, dtype=pl.Float64).alias("ts"))

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    df_nodes.write_parquet(out_dir / "nodes.parquet")
    df_edges.write_parquet(out_dir / "edges.parquet")

    print(f"  Saved: {len(df_nodes):,} nodes ({n_feat_cols} features, type=User) | "
          f"{len(df_edges):,} edges (ts joined from node time_step)")

# --- CELL BREAK ---

def load_elliptic_v2(folder_path, out_name="elliptic_v2"):
    if not folder_path.exists():
        raise FileNotFoundError(f"folder missing -> {folder_path}")

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Labeled data FIRST: small, and the part actually needed for supervised training.
    # Written before background is even attempted, so it's safe on disk regardless of what
    # happens below.
    # --- Labeled data FIRST: small, and the part actually needed for supervised training.
    # Written before background is even attempted, so it's safe on disk regardless of what
    # happens below.
    for src_name, out_file in [("nodes.csv", "nodes.parquet"), ("edges.csv", "edges.parquet"),
                                ("connected_components.csv", "connected_components.parquet")]:
        src_path = folder_path / src_name
        if not src_path.exists():
            print(f"  [SKIP] {src_name} not found")
            continue
        raw_sql, cols = stripped_raw_sql([src_path])
        print(f"  {src_name} columns: {cols}")
        out_path = out_dir / out_file
        # Elliptic v2's temporal signal lives on NODES (time_step), not edges — keep it
        # as a normalized `ts` column so the Burst-Aware Temporal Decay component can read
        # from one uniform field across datasets instead of a per-dataset branch.
        if out_file == "nodes.parquet" and "time_step" in cols:
            sql = (f"COPY (SELECT *, {normalize_timestamp_expr('time_step')} "
                   f"FROM {raw_sql}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)")
        else:
            sql = f"COPY (SELECT * FROM {raw_sql}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)"
        con.execute(sql)
        n_rows = con.execute(f"SELECT COUNT(*) FROM '{out_path}'").fetchone()[0]
        print(f"    -> {out_file}: {n_rows:,} rows")

    if not ELLIPTIC2_INCLUDE_BACKGROUND:
        print(f"  [SKIPPED] background - ELLIPTIC2_INCLUDE_BACKGROUND=False")
        return

    bg_nodes_csv = folder_path / "background_nodes.csv"
    bg_edges_csv = folder_path / "background_edges.csv"
    if not bg_nodes_csv.exists() or not bg_edges_csv.exists():
        print(f"  [SKIPPED] background_nodes.csv / background_edges.csv not found")
        return

    bg_nodes_sql, bg_node_cols = stripped_raw_sql([bg_nodes_csv])
    bg_edges_sql, bg_edge_cols = stripped_raw_sql([bg_edges_csv])
    bg_node_id_col = bg_node_cols[0]
    bg_edge_src_col, bg_edge_dst_col = bg_edge_cols[0], bg_edge_cols[1]
    print(f"  background_nodes columns: {bg_node_cols}")
    print(f"  background_edges columns: {bg_edge_cols}")

    # NO graph traversal here on purpose. A K-hop BFS was tried and measured directly: from
    # 444,521 seed nodes, hop 1 reached 737,870 nodes, hop 2 reached 33,788,526 - a 45x blowup
    # in a single hop. That means this background graph has hub nodes with enormous degree
    # (common in transaction graphs - a handful of exchange/mixer-like addresses connected to
    # millions of others), so ANY full-neighborhood BFS is the wrong tool: even a safety cap on
    # total frontier size doesn't help, because the already-exploded frontier from the hop that
    # tripped the cap still gets used to filter the output, which is nearly as expensive as no
    # filtering at all - confirmed directly, this is what caused the repeat disk-full crash.
    #
    # The standard, correct answer for graphs shaped like this: don't pre-compute a neighborhood
    # in Layer 1 at all. Store the full lightweight topology, and let Layer 2's GNN dataloader
    # (e.g. PyTorch Geometric's NeighborLoader) do FIXED-FANOUT sampling live during training -
    # that's what it's built for, and it's already robust to hub nodes because it caps neighbors
    # per node, not per hop. Concretely:
    #   - background_nodes: kept in FULL (all ~49M rows), float32 - already proven to work
    #     fine on its own in an earlier run (~850MB).
    #   - background_edges: kept in FULL (all ~196M rows) but TOPOLOGY ONLY - the ~95 feature
    #     columns are dropped for this unlabeled context graph (95 cols x 196M rows would be
    #     ~75GB before compression even at float32 - bigger than the entire quota regardless of
    #     any sampling scheme). Your labeled edges already keep their features in full; the
    #     background's job here is to supply graph STRUCTURE for message passing, not features.
    print(f"  Writing FULL background (no sampling/traversal - streamed straight through, "
          f"bounded by construction): nodes in full w/ features, edges in full w/ topology only")

    float_cols = bg_node_cols[1:]
    cast_list = ", ".join(f'CAST("{c}" AS FLOAT) AS "{c}"' for c in float_cols)
    con.execute(f"""
        COPY (SELECT "{bg_node_id_col}", {cast_list} FROM {bg_nodes_sql})
        TO '{out_dir / "background_nodes.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    con.execute(f"""
        COPY (
            SELECT CAST("{bg_edge_src_col}" AS VARCHAR) AS src,
                   CAST("{bg_edge_dst_col}" AS VARCHAR) AS dst
            FROM {bg_edges_sql}
        ) TO '{out_dir / "background_edges_topology.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    n_bg_nodes = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'background_nodes.parquet'}'").fetchone()[0]
    n_bg_edges = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'background_edges_topology.parquet'}'").fetchone()[0]
    bg_mb = sum((out_dir / f).stat().st_size for f in
                ["background_nodes.parquet", "background_edges_topology.parquet"]) / (1024 * 1024)
    print(f"  Saved FULL background: {n_bg_nodes:,} nodes (all features) | {n_bg_edges:,} edges "
          f"(topology only) - {bg_mb:,.1f} MB total")
    print(f"  Layer 2: join background_edges_topology against background_nodes/labeled_nodes by "
          f"ID to pull features per-batch; use a fixed-fanout neighbor sampler (e.g. PyG "
          f"NeighborLoader) rather than loading the whole background into one training batch.")

# --- CELL BREAK ---

def load_dgraphfin(npz_path, out_name="dgraphfin"):
    if not npz_path.exists():
        raise FileNotFoundError(f"file missing -> {npz_path}")

    data = np.load(npz_path)
    print(f"  Available keys: {list(data.keys())}")

    x = data["x"].astype(np.float32)   # float64 -> float32: halves this array's RAM for free
    edge_index = data["edge_index"]
    y = data["y"]

    df_nodes = pl.DataFrame(x, schema=[f"feat_{i}" for i in range(x.shape[1])])
    df_nodes = df_nodes.with_columns([
        pl.arange(0, len(df_nodes)).alias("node_id"),
        pl.Series("label", y),
        pl.lit("User").alias("node_type")  # DGraphFin: anonymized financial accounts
    ])

    df_edges = pl.DataFrame(edge_index, schema=["src", "dst"])
    if "edge_type" in data:
        df_edges = df_edges.with_columns(pl.Series("edge_type", data["edge_type"]))
    else:
        df_edges = df_edges.with_columns(pl.lit("Transaction").alias("edge_type"))
    if "edge_timestamp" in data:
        df_edges = df_edges.with_columns(
            pl.Series("ts", data["edge_timestamp"].astype("float64")))
    else:
        df_edges = df_edges.with_columns(pl.lit(None, dtype=pl.Float64).alias("ts"))

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    df_nodes.write_parquet(out_dir / "nodes.parquet")
    df_edges.write_parquet(out_dir / "edges.parquet")

    print(f"  Saved: {len(df_nodes):,} nodes ({x.shape[1]} float32 features, type=User) | "
          f"{len(df_edges):,} edges (ts={'yes' if 'edge_timestamp' in data else 'no'})")

# --- CELL BREAK ---

def load_xblock_eth(folder_path, out_name="xblock_eth"):
    files = discover_csv_files(folder_path)
    if not files:
        raise FileNotFoundError(f"no CSV files found under {folder_path}")
    if len(files) == 1:
        print(f"  [INFO] Only one shard found ({files[0].name}). If XBlock-ETH ships more shards "
              f"(8100to..., etc.), they are not present in this Kaggle dataset version — treat this "
              f"as a partial slice, not the complete set.")
    ingest_transaction_csv("xblock_eth", folder_path, out_name=out_name,
                           src_node_type="Account", dst_node_type="Account",
                           edge_type_name="Transaction")

# --- CELL BREAK ---

import pickle

def load_eth_phishing_pkl(pkl_path, out_name="eth_phishing"):
    if not pkl_path.exists():
        raise FileNotFoundError(f"file missing -> {pkl_path}")

    print(f"  Unpickling {pkl_path.name} ...")
    with open(pkl_path, "rb") as f:
        G = pickle.load(f)

    print(f"  Loaded object type: {type(G)}")
    if not hasattr(G, "edges"):
        raise TypeError(f"Unrecognized object (no .edges method) - inspect manually: {type(G)}")

    edges_data = list(G.edges(data=True))
    print(f"  Graph has {G.number_of_nodes():,} nodes, {len(edges_data):,} edges")

    rows = [{"src": str(u), "dst": str(v), **{k: v2 for k, v2 in data.items()}}
            for u, v, data in edges_data]
    df_edges = pl.DataFrame(rows, infer_schema_length=None)
    df_edges = df_edges.with_columns(pl.lit("eth_transfer").alias("edge_type"))

    senders = df_edges.select(pl.col("src").alias("node_id"))
    receivers = df_edges.select(pl.col("dst").alias("node_id"))
    df_nodes = pl.concat([senders, receivers]).unique().with_columns(pl.lit("Account").alias("node_type"))

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    df_nodes.write_parquet(out_dir / "nodes.parquet", compression="zstd", compression_level=3)
    df_edges.write_parquet(out_dir / "edges.parquet", compression="zstd", compression_level=3)

    print(f"  Saved: {len(df_nodes):,} nodes (type=Account) | {len(df_edges):,} edges")

# --- CELL BREAK ---

def load_data_generator_pt(pt_path, out_name="data_generator"):
    if not pt_path.exists():
        raise FileNotFoundError(f"file missing -> {pt_path}")

    try:
        import torch
    except ImportError:
        raise ImportError("torch is required to read aml_dataset.pt but isn't installed here")

    print(f"  Loading {pt_path.name} with torch.load ...")
    try:
        obj = torch.load(pt_path, map_location="cpu", weights_only=False)
    except ModuleNotFoundError as e:
        if "torch_geometric" in str(e):
            raise ModuleNotFoundError(
                f"{e}. aml_dataset.pt is a PyTorch Geometric object and needs torch_geometric "
                f"installed to unpickle, even just to read it. Add 'torch_geometric' to the "
                f"pip install cell at the top of this notebook and re-run from the top."
            ) from e
        raise
    print(f"  Loaded object type: {type(obj)}")

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Case 1: PyTorch Geometric Data/HeteroData-style object (has .x and .edge_index attributes)
    if hasattr(obj, "x") and hasattr(obj, "edge_index"):
        x = obj.x.numpy() if obj.x is not None else None
        edge_index = obj.edge_index.numpy()
        y = obj.y.numpy() if getattr(obj, "y", None) is not None else None

        if x is not None:
            df_nodes = pl.DataFrame(x.astype("float32"), schema=[f"feat_{i}" for i in range(x.shape[1])])
            node_cols = [pl.arange(0, len(df_nodes), eager=True).alias("node_id")]
            if y is not None:
                node_cols.append(pl.Series("label", y))
            node_cols.append(pl.lit("Account").alias("node_type"))
            df_nodes = df_nodes.with_columns(node_cols)
            df_nodes.write_parquet(out_dir / "nodes.parquet", compression="zstd", compression_level=3)
            print(f"  Saved nodes.parquet: {len(df_nodes):,} nodes, {x.shape[1]} features (type=Account)")
        else:
            print("  [WARN] obj.x is None - no node features to save")

        df_edges = pl.DataFrame(edge_index.T, schema=["src", "dst"])
        if getattr(obj, "edge_attr", None) is not None:
            edge_attr = obj.edge_attr.numpy()
            for i in range(edge_attr.shape[1]):
                df_edges = df_edges.with_columns(pl.Series(f"edge_feat_{i}", edge_attr[:, i].astype("float32")))
        df_edges = df_edges.with_columns(pl.lit("Transaction").alias("edge_type"))
        df_edges = df_edges.with_columns(pl.lit(None, dtype=pl.Float64).alias("ts"))
        df_edges.write_parquet(out_dir / "edges.parquet", compression="zstd", compression_level=3)
        print(f"  Saved edges.parquet: {len(df_edges):,} edges (type=Transaction)")
        return

    # Case 2: a plain dict of tensors/arrays
    if isinstance(obj, dict):
        print(f"  Dict keys found: {list(obj.keys())}")
        print(f"  [ACTION NEEDED] Structure not auto-recognized - inspect the keys above and adjust "
              f"this loader to match (e.g. obj['x'], obj['edge_index'], or dataset-specific names).")
        return

    print(f"  [ACTION NEEDED] Unrecognized object shape for {type(obj)} - "
          f"inspect its attributes (dir(obj)) and extend this loader.")

# --- CELL BREAK ---

def load_eth_phishing_2nd(base_folder, out_name="eth_phishing_2nd"):
    if not base_folder.exists():
        raise FileNotFoundError(f"folder missing -> {base_folder}")

    categories = {
        "Normal first-order nodes":    {"actor_type": "normal",   "hop_order": 1},
        "Normal second-order nodes":   {"actor_type": "normal",   "hop_order": 2},
        "Phishing first-order nodes":  {"actor_type": "phishing", "hop_order": 1},
        "Phishing second-order nodes": {"actor_type": "phishing", "hop_order": 2},
    }

    out_dir = OUTPUT_DIR / out_name
    out_dir.mkdir(parents=True, exist_ok=True)

    category_tables = []
    for subfolder_name, tags in categories.items():
        subfolder = base_folder / subfolder_name
        if not subfolder.exists():
            print(f"  [SKIP] subfolder not found: {subfolder_name}")
            continue
        files = discover_csv_files(subfolder)
        if not files:
            print(f"  [SKIP] no CSVs under {subfolder_name}")
            continue
        print(f"  {subfolder_name}: {len(files):,} per-address files")

        files_sql = build_files_sql(files)

        # Probe real column names first - types= throws a hard error if a key doesn't exist
        # in the file, so build the override dict only from columns that are actually present.
        probe = f"read_csv_auto({files_sql}, union_by_name=true, ignore_errors=true)"
        cur = con.execute(f"SELECT * FROM {probe} LIMIT 0")
        raw_cols = [d[0] for d in cur.description]
        id_hint_names = {h.lower() for h in (SRC_HINTS + DST_HINTS)}
        force_varchar = [c for c in raw_cols if c.strip().lower() in id_hint_names]
        types_sql = ""
        if force_varchar:
            types_dict = "{" + ", ".join(f"'{c}': 'VARCHAR'" for c in force_varchar) + "}"
            types_sql = f", types={types_dict}"

        # filename=true adds a column with the source path -> the address is embedded in it
        q = f"""
            SELECT *, '{tags["actor_type"]}' AS actor_type, {tags["hop_order"]} AS hop_order
            FROM read_csv_auto({files_sql}, union_by_name=true, ignore_errors=true, filename=true{types_sql})
        """
        tmp_view = f"cat_{tags['actor_type']}_{tags['hop_order']}"
        con.execute(f"CREATE OR REPLACE TEMP VIEW {tmp_view} AS {q}")
        category_tables.append(tmp_view)

    if not category_tables:
        raise FileNotFoundError(f"no data found in any of the 4 subfolders under {base_folder}")

    union_sql = " UNION ALL BY NAME ".join(f"SELECT * FROM {t}" for t in category_tables)
    out_path = out_dir / "labeled_transactions.parquet"
    con.execute(f"COPY ({union_sql}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    n_rows = con.execute(f"SELECT COUNT(*) FROM '{out_path}'").fetchone()[0]
    print(f"  Saved labeled_transactions.parquet: {n_rows:,} rows across all 4 categories")
    print(f"  Category counts:")
    counts = con.execute(f"SELECT actor_type, hop_order, COUNT(*) FROM '{out_path}' GROUP BY 1,2 ORDER BY 1,2").fetchall()
    for actor_type, hop_order, cnt in counts:
        print(f"    {actor_type} / hop {hop_order}: {cnt:,} rows")

# --- CELL BREAK ---

import re as _re

def parse_ibm_patterns_txt(path):
    """
    IBM AML's Patterns.txt is a structured but non-CSV format:
        BEGIN LAUNDERING ATTEMPT - STACK
        2022/08/09 05:14,00952,8139F54E0,0111632,8062C56E0,5331.44,US Dollar,5331.44,US Dollar,ACH,1
        ...
        END LAUNDERING ATTEMPT - STACK
    Each data line has the same 11 fields as Trans.csv (timestamp, from bank/account, to
    bank/account, amounts/currencies, format, is_laundering flag). This parses every block into
    one row per flagged transaction, tagged with which specific scheme (pattern_id) and pattern
    type (STACK/CYCLE/etc, plus any qualifier like "Max 12 hops") it belongs to.
    Malformed lines are skipped rather than raising, since this is label metadata, not the core
    graph - one bad line shouldn't lose an entire tier's pattern labels.
    """
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    blocks = _re.split(r"(?=BEGIN LAUNDERING ATTEMPT)", text)
    rows = []
    pattern_id = 0
    for block in blocks:
        block = block.strip()
        if not block.startswith("BEGIN LAUNDERING ATTEMPT"):
            continue
        header_line = block.splitlines()[0]
        m = _re.match(r"BEGIN LAUNDERING ATTEMPT - (\w[\w\- ]*?)(?::\s*(.*))?$", header_line.strip())
        pattern_type = m.group(1).strip() if m else "UNKNOWN"
        qualifier = m.group(2).strip() if (m and m.group(2)) else None
        pattern_id += 1

        data_lines = [l for l in block.splitlines()[1:]
                      if l.strip() and not l.startswith("END LAUNDERING ATTEMPT")]
        for line in data_lines:
            fields = line.split(",")
            if len(fields) != 11:
                continue
            try:
                rows.append({
                    "pattern_id": pattern_id, "pattern_type": pattern_type,
                    "pattern_qualifier": qualifier, "timestamp": fields[0],
                    "from_bank": fields[1], "from_account": fields[2],
                    "to_bank": fields[3], "to_account": fields[4],
                    "amount_received": float(fields[5]), "receiving_currency": fields[6],
                    "amount_paid": float(fields[7]), "payment_currency": fields[8],
                    "payment_format": fields[9], "is_laundering": int(fields[10]),
                })
            except ValueError:
                continue
    return pl.DataFrame(rows) if rows else pl.DataFrame()


def load_ibm_amlsim_tier(tier_key, base_folder, prefix):
    """One tier (e.g. HI-Small) of the real IBM AML dataset: Trans.csv (the graph, via the
    same universal engine as everything else), accounts.csv (small lookup table), and
    Patterns.txt (parsed separately, see parse_ibm_patterns_txt)."""
    trans_path = base_folder / f"{prefix}_Trans.csv"
    accounts_path = base_folder / f"{prefix}_accounts.csv"
    patterns_path = base_folder / f"{prefix}_Patterns.txt"

    if not trans_path.exists():
        raise FileNotFoundError(f"{trans_path} not found")

    src_mb = trans_path.stat().st_size / (1024 * 1024)
    disk = check_disk_space(required_mb=src_mb * 1.5)
    print(f"  {prefix}_Trans.csv is {src_mb:,.0f} MB. Free output disk: {disk['free_mb']:,.0f} MB.")
    if disk["insufficient"]:
        print(f"  [SKIPPED] not enough free disk to safely attempt this tier.")
        return {"status": "skipped_disk"}

    result = ingest_transaction_csv(
        tier_key, trans_path,
        src_hints=["Account"] + SRC_HINTS, dst_hints=["Account_1"] + DST_HINTS,
        label_hints=["Is Laundering"] + LABEL_HINTS, edge_type_name="Transaction",
        src_node_type="Account", dst_node_type="Account",
    )

    if accounts_path.exists():
        try:
            ingest_tabular_csv(f"{tier_key}_accounts", accounts_path)
            print(f"  {prefix}_accounts.csv: ok")
        except Exception as e:
            print(f"  {prefix}_accounts.csv: FAILED ({type(e).__name__}: {e}) - "
                  f"continuing, this doesn't affect the main transaction graph")
    else:
        print(f"  [SKIP] {prefix}_accounts.csv not found")

    if patterns_path.exists():
        patterns_df = parse_ibm_patterns_txt(patterns_path)
        if len(patterns_df) > 0:
            out_dir = OUTPUT_DIR / tier_key
            out_dir.mkdir(parents=True, exist_ok=True)
            patterns_df.write_parquet(out_dir / "patterns.parquet", compression="zstd")
            n_schemes = patterns_df["pattern_id"].n_unique()
            n_types = patterns_df["pattern_type"].n_unique()
            print(f"  {prefix}_Patterns.txt: {len(patterns_df):,} labeled transactions across "
                  f"{n_schemes:,} laundering schemes ({n_types} distinct pattern types)")
        else:
            print(f"  {prefix}_Patterns.txt: parsed but found 0 valid rows - check format manually")
    else:
        print(f"  [SKIP] {prefix}_Patterns.txt not found")

    return result

# --- CELL BREAK ---

def load_ulb_tabular(csv_path, out_name="ulb_credit_card"):
    if not csv_path.exists():
        raise FileNotFoundError(f"file missing -> {csv_path}")
    ingest_tabular_csv("ulb_credit_card", csv_path, out_name=out_name)

# --- CELL BREAK ---

# All lightweight/fast datasets run FIRST inside run_all_datasets() (defined below).
# Elliptic v2 (the one dataset whose background can exceed the Kaggle output quota) is
# deliberately LAST there, so if it fails, every other dataset has already succeeded and
# is safe on disk. This block intentionally runs ONLY when run_all_datasets() is called
# (not at import), keeping the module import instant and side-effect free.

# --- CELL BREAK ---

# Module A: Fiat & Fraud — generic universal engine, auto-detects columns for each.
# Each call passes the heterogeneous node/edge types from the research schema so the
# output is a genuinely typed graph (HT-GNN input), not a single 'Entity'/'transaction'.


def ingest_from_upload(file_path, dataset_name=None, file_format=None,
                        src_hints=None, dst_hints=None, label_hints=None,
                        node_type=None, src_node_type=None, dst_node_type=None):
    """Universal upload handler: accepts any file format (CSV, Parquet, Excel, JSON, JSONL)
    and routes it to the correct loader. Designed for user-uploaded data.

    Parameters
    ----------
    file_path : str or Path
        Path to the uploaded file.
    dataset_name : str, optional
        Name for the output dataset. Defaults to the file stem.
    file_format : str, optional
        'csv', 'parquet', 'excel', 'json', 'jsonl', or 'auto' (detect from extension).
    src_hints / dst_hints / label_hints : list of str, optional
        Column name hints for source, destination, and label columns.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Uploaded file not found: {file_path}")

    dataset_name = dataset_name or file_path.stem
    if file_format is None or file_format == "auto":
        ext = file_path.suffix.lower()
        fmt_map = {".csv": "csv", ".parquet": "parquet", ".xlsx": "excel", ".xls": "excel",
                   ".json": "json", ".jsonl": "jsonl", ".pkl": "pkl", ".pt": "pt"}
        file_format = fmt_map.get(ext, "csv")

    print(f"\n  Uploading: {file_path.name} -> {dataset_name} (format={file_format})")

    if file_format in ("csv", "json", "jsonl"):
        ingest_transaction_csv(dataset_name, file_path, out_name=dataset_name,
                               src_node_type=src_node_type or "Account",
                               dst_node_type=dst_node_type or "Account",
                               edge_type_name="Transaction",
                               src_hints=src_hints, dst_hints=dst_hints,
                               label_hints=label_hints)
    elif file_format == "parquet":
        load_parquet_passthrough(dataset_name, file_path)
    elif file_format == "excel":
        load_excel_file(dataset_name, file_path, src_hints=src_hints, dst_hints=dst_hints,
                        label_hints=label_hints, node_type=node_type,
                        src_node_type=src_node_type, dst_node_type=dst_node_type)
    elif file_format in ("pkl", "pt"):
        if file_format == "pkl":
            load_eth_phishing_pkl(file_path, out_name=dataset_name)
        else:
            load_data_generator_pt(file_path, out_name=dataset_name)
    else:
        # Try CSV as fallback
        ingest_transaction_csv(dataset_name, file_path, out_name=dataset_name,
                               src_node_type=src_node_type or "Account",
                               dst_node_type=dst_node_type or "Account",
                               edge_type_name="Transaction",
                               src_hints=src_hints, dst_hints=dst_hints,
                               label_hints=label_hints)

    print(f"  Upload ingested: {dataset_name}")
    return dataset_name


def ingest_from_live_stream(records, dataset_name="live_stream", batch_id=None):
    """Ingest a live batch of transaction records into the streaming graph.

    Parameters
    ----------
    records : list of dict or Polars DataFrame
        New transaction records to ingest.
    dataset_name : str
        Name of the streaming dataset.
    batch_id : str, optional
        Batch identifier. Auto-generated if not provided.

    Returns
    -------
    dict with ingestion status and row counts.
    """
    return ingest_stream_batch(dataset_name, records, batch_id=batch_id)


def download_missing_datasets():
    """Download all Kaggle datasets that are referenced in DATASETS but not
    found locally. Uses kagglehub to download datasets on demand.

    Skipped entirely when running on Kaggle (datasets are already mounted
    at /kaggle/input/). Only needed for local (Control Plane) execution.
    """
    if is_kaggle():
        print("Running on Kaggle — all datasets are already mounted at /kaggle/input/. No download needed.")
        return
    import kagglehub
    print("Downloading missing datasets via kagglehub ...")
    downloaded = set()
    for name, path in DATASETS.items():
        p_str = str(path).replace("\\", "/")
        has_kaggle = "/kaggle/input/" in p_str
        path_obj = Path(path)
        if has_kaggle and not path_obj.exists():
            slug = _kaggle_path_to_slug(p_str)
            if slug and slug not in downloaded:
                try:
                    print(f"  Downloading {slug} ...")
                    kagglehub.dataset_download(slug)
                    downloaded.add(slug)
                except Exception as e:
                    print(f"  Failed to download {slug}: {e}")
    print(f"Done. Downloaded {len(downloaded)} dataset(s).")


def run_all_datasets():
    global RESULTS
    _startup_diagnostics()
    # Fast/lightweight datasets first so they're safe on disk before the heavy ones.
    run_safely("elliptic_v1", load_elliptic_v1, DATASETS["elliptic_v1"])
    run_safely("dgraphfin", load_dgraphfin, DATASETS["dgraphfin"])
    run_safely("xblock_eth", load_xblock_eth, DATASETS["xblock_eth"])
    run_safely("ulb_credit_card", load_ulb_tabular, DATASETS["ulb_credit_card"])
    # PaySim (MFS): sender Account -> receiver Account, mobile-money transfer
    run_safely("paysim1", ingest_transaction_csv, "paysim1", DATASETS["paysim1"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")
    run_safely("paysim_extended", ingest_transaction_csv, "paysim_extended", DATASETS["paysim_extended"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")

    # SynthAML: institutional alert outcome table (sender/receiver accounts)
    run_safely("synthaml", ingest_transaction_csv, "synthaml", DATASETS["synthaml"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")
    # SAML-D: labeled laundering typologies (account-level)
    run_safely("saml_d", ingest_transaction_csv, "saml_d", DATASETS["saml_d"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")
    # cc_transactions: consumer card graph (cardholder -> merchant)
    run_safely("cc_transactions", ingest_transaction_csv, "cc_transactions", DATASETS["cc_transactions"],
               src_node_type="Account", dst_node_type="Institution", edge_type_name="Transaction")

    # --- CELL BREAK ---

    # Module B: Crypto & Web3
    # Mt.Gox: crypto wallet -> wallet
    run_safely("mtgox_leaked", ingest_transaction_csv, "mtgox_leaked", DATASETS["mtgox_leaked"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")
    run_safely("eth_phishing", load_eth_phishing_pkl, DATASETS["eth_phishing"])
    run_safely("eth_phishing_2nd", load_eth_phishing_2nd, DATASETS["eth_phishing_2nd"])
    # Smart Ponzi: contract-level, treat addresses as accounts
    run_safely("smart_ponzi", ingest_transaction_csv, "smart_ponzi", DATASETS["smart_ponzi"],
               src_node_type="Account", dst_node_type="Account", edge_type_name="Transaction")

    # --- CELL BREAK ---

    run_safely("data_generator", load_data_generator_pt, DATASETS["data_generator"])

    # --- CELL BREAK ---

    for _tier_key, _prefix in IBM_AML_TIERS.items():
        if "large" in _tier_key:
            continue  # Large tiers handled separately below, after Elliptic v2
        run_safely(_tier_key, load_ibm_amlsim_tier, _tier_key, IBM_AML_BASE, _prefix)

    # --- CELL BREAK ---

    run_safely("elliptic_v2", load_elliptic_v2, DATASETS["elliptic_v2"])

    # --- CELL BREAK ---

    if IBM_AML_INCLUDE_LARGE:
        for _tier_key, _prefix in IBM_AML_TIERS.items():
            if "large" not in _tier_key:
                continue
            run_safely(_tier_key, load_ibm_amlsim_tier, _tier_key, IBM_AML_BASE, _prefix)
    else:
        print("IBM AML Large tiers skipped (IBM_AML_INCLUDE_LARGE=False). "
              "Set it to True near the top of the notebook once you've confirmed there's room.")
    
    # --- CELL BREAK ---
    
    print("\n" + "="*70)
    print(" LAYER 1 COMPLETE — RUN REPORT ")
    print("="*70)
    
    print("\nPer-dataset status:")
    for name, status in RESULTS.items():
        marker = "\u2705" if status == "SUCCESS" else "\u274c"
        print(f"  {marker} {name:20s} {status}")
    
    n_success = sum(1 for s in RESULTS.values() if s == "SUCCESS")
    n_failed = len(RESULTS) - n_success
    print(f"\n{n_success}/{len(RESULTS)} datasets ingested successfully.")
    if n_failed > 0:
        if is_kaggle():
            print(f"\n  {n_failed} dataset(s) failed because the data files are not available at /kaggle/input/.")
            print("  Check the Kaggle dataset attachments for this notebook and re-run.")
        else:
            print(f"\n  {n_failed} dataset(s) failed because the data files are not available locally.")
            print("  To download them automatically, run:")
            print("    python -c \"from src.ingestion import pipeline as P; P.download_missing_datasets()\"")
            print("  Or place CSV/Parquet/Excel/JSON files in data/raw/ and re-run.")
    
    print("\n" + "="*70)
    print(" OUTPUT FILES ")

    print("="*70)
    total_size_bytes = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        if not files:
            continue
        folder_name = os.path.basename(root)
        print(f"\n\U0001f4c1 {folder_name}/")
        for file in sorted(files):
            filepath = Path(root) / file
            size_mb = filepath.stat().st_size / (1024 * 1024)
            total_size_bytes += filepath.stat().st_size
            print(f"  |-- {file:35s} {size_mb:>8.2f} MB")
    
    print("\n" + "="*70)
    print(f"\U0001f4be TOTAL OUTPUT SIZE: {total_size_bytes / (1024*1024):.2f} MB")
    print("="*70)
    report_resources("final")

    # Deterministic train/val/test splits per the blueprint split matrix.
    split_all_datasets()

    # Reproducibility anchor (L0): seed-locked, content-hashed manifest of all outputs.
    write_run_manifest(OUTPUT_DIR)

    print("\n\U0001f4e5 HOW TO DOWNLOAD:")
    print("1. Look at the 'Output' section in the right-hand panel of your Kaggle notebook.")
    print("2. You will see a folder named 'graph_data'.")
    print("3. Click the Download icon next to it.")
    print("4. Extract into your local 'data' folder for Layer 2.")
    
    # --- CELL BREAK ---
    

def load_json_records(dataset_name, path, src_hints=None, dst_hints=None, label_hints=None,
                      node_type=None, src_node_type=None, dst_node_type=None):
    """JSON array or JSONL (one record per line) - both read the same way via read_json_auto."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"file missing -> {path}")

    files_sql = build_files_sql([path])
    probe = f"read_json_auto({files_sql})"
    cur = con.execute(f"SELECT * FROM {probe} LIMIT 0")
    raw_cols = [d[0] for d in cur.description]
    stripped_cols = [c.strip() for c in raw_cols]

    src_hints = src_hints or SRC_HINTS
    dst_hints = dst_hints or DST_HINTS
    label_hints = label_hints or LABEL_HINTS
    src_col = next((c for c in stripped_cols if c in src_hints), None)
    dst_col = next((c for c in stripped_cols if c in dst_hints), None)
    label_col = next((c for c in stripped_cols if c in label_hints), None)
    ts_col = find_timestamp_column(stripped_cols)

    out_dir = OUTPUT_DIR / dataset_name
    out_dir.mkdir(parents=True, exist_ok=True)

    if not src_col or not dst_col:
        con.execute(f"COPY (SELECT * FROM {probe}) TO '{out_dir / 'raw_table.parquet'}' (FORMAT PARQUET, COMPRESSION ZSTD)")
        n = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'raw_table.parquet'}'").fetchone()[0]
        print(f"  Saved as flat table (no src/dst detected): {n:,} rows")
        return {"status": "tabular_fallback", "rows": n}

    s_type = src_node_type or node_type or DEFAULT_NODE_TYPE
    d_type = dst_node_type or node_type or DEFAULT_NODE_TYPE
    exclude_set = {src_col, dst_col} | ({label_col} if label_col else set())
    exclude_sql = ", ".join(f'"{c}"' for c in exclude_set)
    label_expr = f'"{label_col}"' if label_col else "-1"
    ts_select = normalize_timestamp_expr(ts_col) if ts_col else "NULL AS ts"

    con.execute(f"""
        COPY (SELECT node_id, node_type FROM (
                SELECT CAST("{src_col}" AS VARCHAR) AS node_id, '{s_type}' AS node_type
                FROM {probe} WHERE "{src_col}" IS NOT NULL
                UNION ALL
                SELECT CAST("{dst_col}" AS VARCHAR) AS node_id, '{d_type}' AS node_type
                FROM {probe} WHERE "{dst_col}" IS NOT NULL)
              QUALIFY ROW_NUMBER() OVER (PARTITION BY node_id) = 1)
        TO '{out_dir / "nodes.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    con.execute(f"""
        COPY (SELECT TRIM("{src_col}") AS src, TRIM("{dst_col}") AS dst, {label_expr} AS label,
                     '{DEFAULT_EDGE_TYPE}' AS edge_type, {ts_select},
                     * EXCLUDE ({exclude_sql}{", " + ts_col if ts_col else ""})
              FROM {probe} WHERE "{src_col}" IS NOT NULL AND "{dst_col}" IS NOT NULL)
        TO '{out_dir / "edges.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    n_nodes = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'nodes.parquet'}'").fetchone()[0]
    n_edges = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'edges.parquet'}'").fetchone()[0]
    ts_note = f" | ts from '{ts_col}'" if ts_col else ""
    print(f"  Saved: {n_nodes:,} nodes ({s_type}/{d_type}) | {n_edges:,} edges{ts_note}")
    return {"status": "ok", "n_nodes": n_nodes, "n_edges": n_edges}


def load_excel_file(dataset_name, path, sheet_name=None, src_hints=None, dst_hints=None,
                    label_hints=None, node_type=None, src_node_type=None, dst_node_type=None):
    """Excel (.xlsx/.xls). DuckDB has no native Excel reader, so this loads via Polars
    (needs the fastexcel package) then hands off to DuckDB for the same standardized
    node/edge construction as every other loader."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"file missing -> {path}")

    df = pl.read_excel(path, sheet_name=sheet_name) if sheet_name else pl.read_excel(path)
    df.columns = [c.strip() for c in df.columns]
    con.register("excel_tmp", df.to_pandas())

    src_hints = src_hints or SRC_HINTS
    dst_hints = dst_hints or DST_HINTS
    label_hints = label_hints or LABEL_HINTS
    src_col = next((c for c in df.columns if c in src_hints), None)
    dst_col = next((c for c in df.columns if c in dst_hints), None)
    label_col = next((c for c in df.columns if c in label_hints), None)
    ts_col = find_timestamp_column(list(df.columns))

    out_dir = OUTPUT_DIR / dataset_name
    out_dir.mkdir(parents=True, exist_ok=True)

    if not src_col or not dst_col:
        con.execute(f"COPY (SELECT * FROM excel_tmp) TO '{out_dir / 'raw_table.parquet'}' (FORMAT PARQUET, COMPRESSION ZSTD)")
        n = len(df)
        print(f"  Saved as flat table (no src/dst detected): {n:,} rows")
        con.unregister("excel_tmp")
        return {"status": "tabular_fallback", "rows": n}

    s_type = src_node_type or node_type or DEFAULT_NODE_TYPE
    d_type = dst_node_type or node_type or DEFAULT_NODE_TYPE
    exclude_set = {src_col, dst_col} | ({label_col} if label_col else set())
    exclude_sql = ", ".join(f'"{c}"' for c in exclude_set)
    label_expr = f'"{label_col}"' if label_col else "-1"
    ts_select = normalize_timestamp_expr(ts_col) if ts_col else "NULL AS ts"

    con.execute(f"""
        COPY (SELECT node_id, node_type FROM (
                SELECT CAST("{src_col}" AS VARCHAR) AS node_id, '{s_type}' AS node_type
                FROM excel_tmp WHERE "{src_col}" IS NOT NULL
                UNION ALL
                SELECT CAST("{dst_col}" AS VARCHAR) AS node_id, '{d_type}' AS node_type
                FROM excel_tmp WHERE "{dst_col}" IS NOT NULL)
              QUALIFY ROW_NUMBER() OVER (PARTITION BY node_id) = 1)
        TO '{out_dir / "nodes.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    con.execute(f"""
        COPY (SELECT TRIM("{src_col}") AS src, TRIM("{dst_col}") AS dst, {label_expr} AS label,
                     '{DEFAULT_EDGE_TYPE}' AS edge_type, {ts_select},
                     * EXCLUDE ({exclude_sql}{", " + ts_col if ts_col else ""})
              FROM excel_tmp WHERE "{src_col}" IS NOT NULL AND "{dst_col}" IS NOT NULL)
        TO '{out_dir / "edges.parquet"}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    n_nodes = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'nodes.parquet'}'").fetchone()[0]
    n_edges = con.execute(f"SELECT COUNT(*) FROM '{out_dir / 'edges.parquet'}'").fetchone()[0]
    ts_note = f" | ts from '{ts_col}'" if ts_col else ""
    print(f"  Saved: {n_nodes:,} nodes ({s_type}/{d_type}) | {n_edges:,} edges{ts_note}")
    con.unregister("excel_tmp")
    return {"status": "ok", "n_nodes": n_nodes, "n_edges": n_edges}


def load_parquet_passthrough(dataset_name, path):
    """Already-Parquet input - just validate and copy into the standard output location
    rather than re-deriving nodes/edges (respects whatever structure it already has)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"file missing -> {path}")
    out_dir = OUTPUT_DIR / dataset_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "raw_table.parquet"
    con.execute(f"COPY (SELECT * FROM read_parquet('{path}')) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    n = con.execute(f"SELECT COUNT(*) FROM '{out_path}'").fetchone()[0]
    print(f"  Copied through: {n:,} rows")
    return {"status": "ok", "rows": n}

# --- CELL BREAK ---

import re, hashlib
from datetime import datetime, timezone

def _checkpoint_path():
    """Checkpoint file lives under the *current* OUTPUT_DIR (not a frozen import-time
    path), so relocating OUTPUT_DIR — e.g. in tests or the remote-runner — keeps
    checkpointing correct and isolated."""
    return OUTPUT_DIR / "_checkpoints.parquet"

def _load_checkpoints():
    cp = _checkpoint_path()
    if cp.exists():
        return pl.read_parquet(cp)
    return pl.DataFrame(schema={"dataset_name": pl.Utf8, "source_id": pl.Utf8,
                                 "ingested_at": pl.Utf8, "rows_ingested": pl.Int64})

def _save_checkpoint(dataset_name, source_id, rows_ingested):
    cp = _checkpoint_path()
    df = _load_checkpoints()
    now = datetime.now(timezone.utc).isoformat()
    df = df.filter(~((pl.col("dataset_name") == dataset_name) & (pl.col("source_id") == source_id)))
    new_row = pl.DataFrame({"dataset_name": [dataset_name], "source_id": [source_id],
                             "ingested_at": [now], "rows_ingested": [rows_ingested]})
    df = pl.concat([df, new_row])
    df.write_parquet(cp)

def _is_already_ingested(dataset_name, source_id):
    df = _load_checkpoints()
    if len(df) == 0:
        return False
    match = df.filter((pl.col("dataset_name") == dataset_name) & (pl.col("source_id") == source_id))
    return len(match) > 0


def _hash_parquet(path):
    """Content hash of an output parquet — used for the run manifest so a reviewer
    can reproduce the exact Layer-1 artifacts referenced in the paper (L0/DVC-equivalent)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def write_run_manifest(output_dir=OUTPUT_DIR):
    """Writes _manifest.json next to the outputs: SEED, config-driven types, and a
    per-dataset content hash. This is the reproducibility anchor for IEEE TIFS / ETH."""
    manifest = {
        "seed": SEED,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "node_types": NODE_TYPES,
        "edge_types": EDGE_TYPES,
        "datasets": {},
    }
    if output_dir.exists():
        for d in sorted(output_dir.iterdir()):
            if not d.is_dir():
                continue
            files = {f.name: _hash_parquet(f) for f in d.glob("*.parquet")}
            if files:
                manifest["datasets"][d.name] = files
    manifest_path = output_dir / "_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"  📝 Reproducibility manifest written: {manifest_path}")
    return manifest_path


# ─────────────────────────────────────────────────────────────────────────────
# Train / Validation / Test splitting (Layer 1 → Layer 2 handoff).
# Mirrors the v4 blueprint split matrix: temporal (time-ordered), stratified
# (preserve positive ratio), or random. Splits are deterministic via SEED so the
# exact same edges land in train/val/test on every run.
# ─────────────────────────────────────────────────────────────────────────────
SPLIT_STRATEGIES = {
    # dataset: (strategy, train_ratio, val_ratio, test_ratio)
    "elliptic_v1":        ("temporal", 0.70, 0.15, 0.15),
    "elliptic_v2":        ("temporal", 0.70, 0.15, 0.15),
    "xblock_eth":         ("temporal", 0.80, 0.10, 0.10),
    "paysim1":            ("temporal", 0.70, 0.15, 0.15),
    "paysim_extended":    ("temporal", 0.70, 0.15, 0.15),
    "dgraphfin":          ("temporal", 0.60, 0.20, 0.20),
    "cc_transactions":    ("temporal", 0.70, 0.15, 0.15),
    "mtgox_leaked":       ("temporal", 0.70, 0.15, 0.15),
    "eth_phishing":       ("temporal", 0.70, 0.15, 0.15),
    "saml_d":             ("stratified", 0.80, 0.10, 0.10),
    "synthaml":           ("stratified", 0.80, 0.10, 0.10),
    "smart_ponzi":        ("stratified", 0.80, 0.10, 0.10),
    "ulb_credit_card":    ("random", 0.80, 0.10, 0.10),
    "ibm_amlsim_hi_small": ("stratified", 0.60, 0.20, 0.20),
    "ibm_amlsim_li_small": ("stratified", 0.60, 0.20, 0.20),
    "ibm_amlsim_hi_medium": ("stratified", 0.60, 0.20, 0.20),
    "ibm_amlsim_li_medium": ("stratified", 0.60, 0.20, 0.20),
}


def split_dataset(dataset_name, out_dir=None, strategy=None, ratios=None):
    """Split a dataset's edges (and any node/edge tables) into train/val/test parquet.

    Writes <out_dir>/{train,val,test}.parquet for the edge table (and copies node
    tables as-is into each split dir is NOT done — nodes are shared). Returns the
    strategy used, or None if there is no edge table to split.
    """
    out_dir = Path(out_dir) if out_dir else (OUTPUT_DIR / dataset_name)
    if not out_dir.exists():
        return None
    edges_pq = out_dir / "edges.parquet"
    if not edges_pq.exists():
        return None

    strat, tr, va, te = SPLIT_STRATEGIES.get(
        dataset_name, (strategy or "random", *(ratios or (0.7, 0.15, 0.15))))
    lf = pl.scan_parquet(edges_pq)
    cols = lf.collect_schema().names()

    # Deterministic assignment column.
    if strat == "temporal" and "ts" in cols:
        # Time-ordered split: sort by ts, then cut by cumulative ratio.
        df = lf.sort("ts").collect()
        n = len(df)
        i1, i2 = int(n * tr), int(n * (tr + va))
        train, val, test = df[:i1], df[i1:i2], df[i2:]
    elif strat == "stratified" and "label" in cols:
        df = lf.collect()
        parts = {}
        for name, sub in [("train", None), ("val", None), ("test", None)]:
            parts[name] = None
        # Split per-label to preserve positive ratio.
        train_frames, val_frames, test_frames = [], [], []
        for lab in df["label"].unique().to_list():
            sub = df.filter(pl.col("label") == lab)
            n = len(sub)
            i1, i2 = int(n * tr), int(n * (tr + va))
            train_frames.append(sub[:i1])
            val_frames.append(sub[i1:i2])
            test_frames.append(sub[i2:])
        train = pl.concat(train_frames) if train_frames else df.head(0)
        val = pl.concat(val_frames) if val_frames else df.head(0)
        test = pl.concat(test_frames) if test_frames else df.head(0)
    else:
        # Random split (default / fallback), deterministic via SEED.
        df = lf.collect().with_columns(
            (pl.col("src").hash(seed=SEED) % 1000).alias("_rnd"))
        train = df.filter(pl.col("_rnd") < tr * 1000)
        val = df.filter((pl.col("_rnd") >= tr * 1000) & (pl.col("_rnd") < (tr + va) * 1000))
        test = df.filter(pl.col("_rnd") >= (tr + va) * 1000)
        train, val, test = train.drop("_rnd"), val.drop("_rnd"), test.drop("_rnd")

    for name, frame in [("train", train), ("val", val), ("test", test)]:
        frame.write_parquet(out_dir / f"{name}.parquet", compression="zstd")
    print(f"  ✂️  {dataset_name}: split ({strat}) -> "
          f"train={len(train):,}, val={len(val):,}, test={len(test):,}")
    return strat


def split_all_datasets():
    """Apply split_dataset() to every ingested graph dataset under OUTPUT_DIR."""
    if not OUTPUT_DIR.exists():
        return
    print("\n" + "="*70)
    print(" LAYER 1 — TRAIN/VAL/TEST SPLITS ")
    print("="*70)
    for d in sorted(OUTPUT_DIR.iterdir()):
        if d.is_dir() and (d / "edges.parquet").exists():
            split_dataset(d.name, out_dir=d)


def ingest_stream_batch(dataset_name, records, batch_id=None):
    """
    Appends a small batch of new records (list of dicts, or a Polars DataFrame) as a new,
    checkpointed part-file under graph_data/<dataset_name>/streaming/. Safe to call repeatedly
    with the same batch_id - already-seen batches are skipped, not duplicated.
    """
    is_df = isinstance(records, pl.DataFrame)
    if (is_df and records.is_empty()) or (not is_df and not records):
        return {"status": "empty_batch"}

    batch_id = batch_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    if _is_already_ingested(dataset_name, batch_id):
        return {"status": "already_ingested", "batch_id": batch_id}

    df = records if is_df else pl.DataFrame(records)
    stream_dir = OUTPUT_DIR / dataset_name / "streaming"
    stream_dir.mkdir(parents=True, exist_ok=True)

    # batch_id might be a full file path, a Kafka "topic:partition:offset" string, etc. -
    # sanitize for use as a filename while keeping the original for checkpoint tracking.
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", batch_id)[:100]
    if safe_id != batch_id:
        safe_id += "_" + hashlib.md5(batch_id.encode()).hexdigest()[:8]
    part_path = stream_dir / f"part-{safe_id}.parquet"

    df.write_parquet(part_path, compression="zstd")
    _save_checkpoint(dataset_name, batch_id, len(df))
    return {"status": "ok", "rows": len(df), "path": str(part_path), "batch_id": batch_id}


def load_full_dataset(dataset_name):
    """Unifies bulk-batch parquet + any streaming part-files into ONE view for Layer 2 -
    it never needs to know whether a row arrived via the original bulk load or a later
    live update."""
    out_dir = OUTPUT_DIR / dataset_name
    if not out_dir.exists():
        return None
    patterns = []
    for fname in ["nodes.parquet", "edges.parquet", "raw_table.parquet", "transactions.parquet"]:
        if (out_dir / fname).exists():
            patterns.append(str(out_dir / fname))
    stream_dir = out_dir / "streaming"
    if stream_dir.exists() and list(stream_dir.glob("*.parquet")):
        patterns.append(str(stream_dir / "*.parquet"))
    if not patterns:
        return None
    return con.execute(f"SELECT * FROM read_parquet({patterns}, union_by_name=true)").pl()


def watch_folder_and_ingest(dataset_name, folder, max_polls=3, poll_interval_s=5):
    """
    Genuine, working near-real-time ingestion for a notebook context: repeatedly checks
    `folder` for files not yet in the checkpoint store and ingests any new ones.

    WHAT THIS CAN AND CANNOT DO: this can run for a bounded number of polls interactively (as
    below), or be wired up via Kaggle's "Schedule notebook to run" feature for genuine periodic
    re-ingestion. It cannot hold an always-on network listener open in this session. To graduate
    to a true always-on stream, replace this function's loop body with a Kafka/websocket
    consumer that calls ingest_stream_batch() per message instead - everything downstream
    (checkpointing, load_full_dataset) stays exactly the same.
    """
    folder = Path(folder)
    poll = 0
    total_new_rows = 0
    while poll < max_polls:
        poll += 1
        current_files = sorted(folder.glob("*.csv")) if folder.exists() else []
        new_files = [f for f in current_files if not _is_already_ingested(dataset_name, str(f))]
        if new_files:
            print(f"  [poll {poll}] {len(new_files)} new file(s): {[f.name for f in new_files]}")
            for f in new_files:
                df = pl.read_csv(f, infer_schema_length=10_000)
                result = ingest_stream_batch(dataset_name, df, batch_id=str(f))
                total_new_rows += result.get("rows", 0)
        else:
            print(f"  [poll {poll}] no new files")
        if poll < max_polls:
            time.sleep(poll_interval_s)
    print(f"  Watch loop ended after {poll} poll(s), {total_new_rows:,} new rows ingested total.")
    return total_new_rows

# --- CELL BREAK ---

def simulate_live_feed(n_batches=5, records_per_batch=3):
    """Stand-in for a real live source (Kafka consumer, websocket handler, API poller).
    Replace this generator with a real one to go from demo to production - ingest_stream_batch
    and everything downstream doesn't change."""
    for i in range(n_batches):
        batch = [{"src": f"user{i}", "dst": f"merchant{i}", "amount": 50.0 + i}
                 for _ in range(records_per_batch)]
        yield f"tick-{i}", batch

def _self_test_demo():
    """Optional smoke demo of the streaming/dedupe path. Only runs when the module
    is executed directly (python pipeline.py), never on import — so importing for
    tests or as a library stays instant and side-effect free."""
    print("=== Simulated live feed: first run ===")
    for batch_id, batch in simulate_live_feed():
        result = ingest_stream_batch("live_demo", batch, batch_id=batch_id)
        print(f"  {batch_id}: {result['status']}, rows={result.get('rows')}")

    unified = load_full_dataset("live_demo")
    print(f"\nUnified view after first run: {len(unified):,} rows")

    print("\n=== Re-running the SAME feed (should all be skipped, not duplicated) ===")
    for batch_id, batch in simulate_live_feed():
        result = ingest_stream_batch("live_demo", batch, batch_id=batch_id)
        print(f"  {batch_id}: {result['status']}")

    unified2 = load_full_dataset("live_demo")
    print(f"\nUnified view after re-run: {len(unified2):,} rows (should be unchanged)")
    assert len(unified2) == len(unified), "BUG: re-run caused duplication"
    print("Confirmed: no duplication on re-run.")


if __name__ == "__main__":
    _self_test_demo()

# --- CELL BREAK ---

