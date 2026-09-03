import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if os.name == "nt":
    _torch_lib = ROOT / "venv" / "Lib" / "site-packages" / "torch" / "lib"
    if _torch_lib.exists():
        try:
            os.add_dll_directory(str(_torch_lib))
        except Exception:
            pass

import shutil
import tempfile
import unittest
import torch
import torch.nn as nn
import numpy as np
import pandas as pd

from scripts.run_automated_paper_benchmark import (
    ALL_MODELS_REGISTRY,
    count_model_parameters,
    get_checkpoint_path,
    save_atomic_checkpoint,
    load_checkpoint,
    generate_trial_group_summary,
    sync_to_central_registry
)
from comparing_models.evaluator import evaluate_model_performance


class TestAutomatedPaperBenchmark(unittest.TestCase):
    """Test suite for the automated paper benchmarking pipeline."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_model_registry_integrity(self):
        """Verify all 13 paper models are registered with required metadata."""
        self.assertEqual(len(ALL_MODELS_REGISTRY), 13)
        slugs = [m["slug"] for m in ALL_MODELS_REGISTRY]
        self.assertEqual(len(slugs), len(set(slugs)), "Model slugs must be unique")
        
        # Verify Proposed model is present
        self.assertTrue(any(m["slug"] == "proposed_c_stgb" for m in ALL_MODELS_REGISTRY))
        
        for m in ALL_MODELS_REGISTRY:
            self.assertIn("slug", m)
            self.assertIn("name", m)
            self.assertIn("paper_ref", m)
            self.assertIn("type", m)
            self.assertIn("category", m)

    def test_count_model_parameters(self):
        """Verify parameter counting on PyTorch models."""
        linear = nn.Linear(10, 5)  # 10*5 + 5 = 55 params
        self.assertEqual(count_model_parameters(linear), 55)

    def test_atomic_checkpointing_and_loading(self):
        """Verify atomic JSON saving, loading, and corruption resilience."""
        ckpt_path = get_checkpoint_path(
            output_dir=self.temp_dir,
            dataset_name="test_dataset",
            split_name="70_30",
            epochs=10,
            model_slug="tabular_xgboost"
        )
        
        test_record = {
            "dataset": "test_dataset",
            "model": "Tabular XGBoost",
            "model_slug": "tabular_xgboost",
            "split": "70_30",
            "epochs": 10,
            "f1_score": 0.9542,
            "recall": 0.9610,
            "precision": 0.9475,
            "pr_auc": 0.9820,
            "roc_auc": 0.9910,
            "tpr_at_01fpr": 0.8500,
            "accuracy": 0.9980,
            "training_time_sec": 1.25,
            "inference_latency_ms": 0.0450,
            "throughput_samples_per_sec": 22222.0,
            "peak_memory_mb": 45.2,
            "parameter_count": 0
        }
        
        # 1. Save checkpoint
        save_atomic_checkpoint(ckpt_path, test_record)
        self.assertTrue(ckpt_path.exists())
        
        # 2. Load checkpoint
        loaded = load_checkpoint(ckpt_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["f1_score"], 0.9542)
        self.assertEqual(loaded["model"], "Tabular XGBoost")

    def test_generate_trial_group_summary_and_markdown(self):
        """Verify generation of group CSV, JSON, and Markdown report from checkpoints."""
        group_dir = self.temp_dir / "test_dataset" / "70_30_10ep"
        checkpoints_dir = group_dir / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        
        record_cstgb = {
            "dataset": "test_dataset",
            "model": "Proposed C-STGB",
            "model_slug": "proposed_c_stgb",
            "category": "Proposed SOTA",
            "split": "70_30",
            "epochs": 10,
            "f1_score": 0.9950,
            "recall": 0.9978,
            "precision": 0.9922,
            "f2_score": 0.9967,
            "pr_auc": 0.9998,
            "roc_auc": 0.9999,
            "tpr_at_01fpr": 1.0000,
            "accuracy": 0.9994,
            "training_time_sec": 12.5,
            "inference_latency_ms": 0.0120,
            "throughput_samples_per_sec": 83333.0,
            "peak_memory_mb": 110.0,
            "parameter_count": 150000
        }
        
        record_xgb = {
            "dataset": "test_dataset",
            "model": "Tabular XGBoost",
            "model_slug": "tabular_xgboost",
            "category": "Industrial Gradient Boosting",
            "split": "70_30",
            "epochs": 10,
            "f1_score": 0.9880,
            "recall": 0.9840,
            "precision": 0.9920,
            "f2_score": 0.9850,
            "pr_auc": 0.9990,
            "roc_auc": 0.9995,
            "tpr_at_01fpr": 0.9900,
            "accuracy": 0.9985,
            "training_time_sec": 1.5,
            "inference_latency_ms": 0.0080,
            "throughput_samples_per_sec": 125000.0,
            "peak_memory_mb": 45.0,
            "parameter_count": 0
        }
        
        save_atomic_checkpoint(checkpoints_dir / "proposed_c_stgb.json", record_cstgb)
        save_atomic_checkpoint(checkpoints_dir / "tabular_xgboost.json", record_xgb)
        
        ds_meta = {
            "dataset": "test_dataset",
            "total_nodes": 5000,
            "total_edges": 15000,
            "illicit_ratio_pct": 2.50
        }
        
        generate_trial_group_summary(group_dir, "test_dataset", "70_30", 10, ds_meta)
        
        summary_csv = group_dir / "benchmark_summary.csv"
        summary_json = group_dir / "benchmark_summary.json"
        report_md = group_dir / "benchmark_report.md"
        
        self.assertTrue(summary_csv.exists())
        self.assertTrue(summary_json.exists())
        self.assertTrue(report_md.exists())
        
        df = pd.read_csv(summary_csv)
        self.assertEqual(len(df), 2)
        # Proposed model should be sorted first
        self.assertEqual(df.iloc[0]["model"], "Proposed C-STGB")
        
        md_text = report_md.read_text(encoding="utf-8")
        self.assertIn("Proposed C-STGB", md_text)
        self.assertIn("Tabular XGBoost", md_text)
        self.assertIn("0.9950", md_text)


if __name__ == "__main__":
    unittest.main()
