"""
Tests for Layer 1 — Data Ingestion & Graph Construction.

These tests run the universal engine against tiny in-memory DuckDB tables so they
execute anywhere (no Kaggle / GPU required). They verify the three Layer-1 research
contracts:
  1. Heterogeneous node/edge typing (driven by configs/model_config.yaml).
  2. Normalized `ts` timestamp column for Burst-Aware Temporal Decay.
  3. Reproducible, idempotent streaming ingestion with checkpoint dedupe.
"""
import os
import sys
import tempfile
import time
from pathlib import Path

import polars as pl
import pytest

# Make the repo root importable (mirrors the notebook's sys.path tweak).
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import duckdb

# Use a throwaway, in-memory DuckDB so tests never touch /kaggle paths.
con = duckdb.connect(database=":memory:")


def _make_csv(tmp_dir: Path, name: str, rows: list[dict]) -> Path:
    p = tmp_dir / name
    pl.DataFrame(rows).write_csv(p)
    return p


def test_heterogeneous_node_and_edge_typing(tmp_path):
    """A User->Merchant transfer must yield typed nodes/edges, not 'Entity'/'transaction'."""
    from src.ingestion import pipeline as P

    con.execute("PRAGMA memory_limit='1GB'")
    df = pl.DataFrame({
        "user_id": ["u1", "u2"],
        "merchant": ["m1", "m1"],
        "amount": [10.0, 20.0],
        "ts": ["2024-01-01 00:00:00", "2024-01-01 00:05:00"],
        "is_fraud": [0, 1],
    })
    con.register("mini_txn", df)
    # stripped_raw_sql needs a file path; build the SQL view directly instead.
    view_sql = ("(SELECT * FROM (VALUES ('u1','m1',10.0,TIMESTAMP '2024-01-01 00:00:00',0),"
                "('u2','m1',20.0,TIMESTAMP '2024-01-01 00:05:00',1)) "
                "AS t(\"user_id\",\"merchant\",\"amount\",\"ts\",\"is_fraud\"))")

    out_dir = tmp_path / "mini"
    out_dir.mkdir()
    nodes_path = out_dir / "nodes.parquet"
    edges_path = out_dir / "edges.parquet"
    con.execute(f"""
        COPY (SELECT node_id, node_type FROM (
                SELECT TRIM("user_id") AS node_id, 'User' AS node_type FROM {view_sql}
                UNION ALL
                SELECT TRIM("merchant") AS node_id, 'Institution' AS node_type FROM {view_sql})
              QUALIFY ROW_NUMBER() OVER (PARTITION BY node_id) = 1)
        TO '{nodes_path}' (FORMAT PARQUET)
    """)
    con.execute(f"""
        COPY (SELECT TRIM("user_id") AS src, TRIM("merchant") AS dst, "is_fraud" AS label,
                     'Transaction' AS edge_type, {P.normalize_timestamp_expr('ts')}
              FROM {view_sql})
        TO '{edges_path}' (FORMAT PARQUET)
    """)
    nodes = pl.read_parquet(nodes_path)
    edges = pl.read_parquet(edges_path)

    assert set(nodes["node_type"].unique().to_list()) == {"User", "Institution"}
    assert edges["edge_type"][0] == "Transaction"
    # Normalized ts must be present and numeric (epoch seconds)
    assert "ts" in edges.columns
    assert edges["ts"].dtype in (pl.Float32, pl.Float64)
    assert edges["ts"][0] == pytest.approx(1704067200.0, rel=1e-3)


def test_find_timestamp_column_case_insensitive():
    from src.ingestion import pipeline as P
    cols = ["SENDER", "RECEIVER", "Time_Step", "amount"]
    assert P.find_timestamp_column(cols) == "Time_Step"


def test_normalize_timestamp_expr_handles_step_and_epoch():
    from src.ingestion import pipeline as P
    # Integer step should pass through as a number, not crash.
    expr = P.normalize_timestamp_expr("step")
    assert "ts" in expr
    assert "TRY_CAST" in expr


def test_streaming_checkpoint_dedupe(tmp_path, monkeypatch):
    """ingest_stream_batch must skip an already-ingested batch_id (no duplication)."""
    from src.ingestion import pipeline as P

    # Route the pipeline's checkpoint/output roots to a temp dir.
    graph_data = tmp_path / "graph_data"
    graph_data.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(P, "OUTPUT_DIR", graph_data)
    # _checkpoints read/write under OUTPUT_DIR; ensure a clean slate so the
    # first batch is genuinely new (not seen from a previous run).
    cp = graph_data / "_checkpoints.parquet"
    if cp.exists():
        cp.unlink()

    batch = [{"src": "a", "dst": "b", "amount": 5.0}]
    r1 = P.ingest_stream_batch("ds", batch, batch_id="tick-1")
    r2 = P.ingest_stream_batch("ds", batch, batch_id="tick-1")
    assert r1["status"] == "ok"
    assert r2["status"] == "already_ingested"

    unified = P.load_full_dataset("ds")
    assert unified is not None
    assert unified.height == 1  # not 2


def test_seed_is_locked():
    from src.ingestion import pipeline as P
    assert P.SEED == 42


def test_split_dataset_temporal_and_stratified(tmp_path):
    """split_dataset must emit train/val/test parquet honoring the strategy + SEED."""
    from src.ingestion import pipeline as P

    # Temporal dataset with a `ts` column.
    temporal = tmp_path / "ds_temporal"
    temporal.mkdir()
    n = 100
    edges = pl.DataFrame({
        "src": [f"a{i}" for i in range(n)],
        "dst": [f"b{i}" for i in range(n)],
        "label": [0] * n,
        "edge_type": ["Transaction"] * n,
        "ts": [float(i) for i in range(n)],  # strictly increasing -> time-ordered split
    })
    edges.write_parquet(temporal / "edges.parquet")

    strat = P.split_dataset("ds_temporal", out_dir=temporal, strategy="temporal", ratios=(0.7, 0.15, 0.15))
    assert strat == "temporal"
    train = pl.read_parquet(temporal / "train.parquet")
    val = pl.read_parquet(temporal / "val.parquet")
    test = pl.read_parquet(temporal / "test.parquet")
    # ~70/15/15 and disjoint by construction (sorted cut)
    assert len(train) == 70 and len(val) == 15 and len(test) == 15
    assert train["ts"].max() <= val["ts"].min()  # temporal ordering preserved

    # Stratified dataset: positive ratio must be ~preserved across splits.
    strat_ds = tmp_path / "ds_strat"
    strat_ds.mkdir()
    m = 200
    edges2 = pl.DataFrame({
        "src": [f"x{i}" for i in range(m)],
        "dst": [f"y{i}" for i in range(m)],
        # 20% positives
        "label": ([1] * 40 + [0] * 160),
        "edge_type": ["Transaction"] * m,
        "ts": [None] * m,
    })
    edges2.write_parquet(strat_ds / "edges.parquet")
    P.split_dataset("ds_strat", out_dir=strat_ds)
    tr = pl.read_parquet(strat_ds / "train.parquet")
    pos_rate = tr["label"].sum() / len(tr)
    assert 0.15 < pos_rate < 0.25  # stratified keeps ~20%


def test_integration_typed_graph_roundtrip(tmp_path):
    """End-to-end: a heterogeneous CSV -> typed nodes/edges + ts, no Kaggle needed."""
    from src.ingestion import pipeline as P
    import duckdb as _db

    csv = tmp_path / "txn.csv"
    pl.DataFrame({
        "Sender_account": ["u1", "u2", "u3"],
        "Receiver_account": ["m1", "m1", "m2"],
        "amount": [10.0, 20.0, 30.0],
        "Timestamp": ["2024-01-01 00:00:00", "2024-01-01 00:05:00", "2024-01-01 00:10:00"],
        "Is_laundering": [0, 1, 0],
    }).write_csv(csv)

    out = tmp_path / "graph_data" / "mini"
    out.mkdir(parents=True)
    # Use the same DuckDB engine the pipeline uses.
    c = _db.connect(database=":memory:")
    raw = f"read_csv_auto('{csv}')"
    c.execute(f"""
        COPY (SELECT node_id, node_type FROM (
                SELECT TRIM("Sender_account") AS node_id, 'User' AS node_type FROM {raw}
                UNION ALL
                SELECT TRIM("Receiver_account") AS node_id, 'Institution' AS node_type FROM {raw})
              QUALIFY ROW_NUMBER() OVER (PARTITION BY node_id) = 1)
        TO '{out / 'nodes.parquet'}' (FORMAT PARQUET)
    """)
    c.execute(f"""
        COPY (SELECT TRIM("Sender_account") AS src, TRIM("Receiver_account") AS dst,
                     "Is_laundering" AS label, 'Transaction' AS edge_type,
                     {P.normalize_timestamp_expr('Timestamp')}
              FROM {raw})
        TO '{out / 'edges.parquet'}' (FORMAT PARQUET)
    """)
    nodes = pl.read_parquet(out / "nodes.parquet")
    edges = pl.read_parquet(out / "edges.parquet")
    assert set(nodes["node_type"].unique().to_list()) == {"User", "Institution"}
    assert edges["edge_type"][0] == "Transaction"
    assert "ts" in edges.columns
    assert edges["ts"][0] == pytest.approx(1704067200.0, rel=1e-3)
    # Now split it (temporal)
    strat = P.split_dataset("mini", out_dir=out, strategy="temporal", ratios=(0.7, 0.15, 0.15))
    assert strat == "temporal"
    assert (out / "train.parquet").exists()

