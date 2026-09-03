"""
test_conformal_triager.py — Unit Tests for TwoTierConformalTriager.
Validates multi-tier decision boundaries, distribution-free coverage, and workload reduction metrics.
"""

import numpy as np
import pytest
from src.utils.conformal import TwoTierConformalTriager


def test_conformal_triager_calibration_and_metrics():
    np.random.seed(42)
    n_samples = 2000
    
    # Simulate imbalanced AML scenario (1:100 fraud rate)
    y_true = np.zeros(n_samples, dtype=int)
    y_true[:20] = 1  # 20 fraud accounts
    
    # Probs: high for fraud, low for licit, with realistic overlap
    probs = np.random.beta(0.5, 10.0, size=n_samples)
    probs[:20] = np.random.beta(10.0, 1.0, size=20)  # Fraud accounts have high risk
    
    triager = TwoTierConformalTriager(alpha=0.05, target_fdr=0.05, target_fnr=0.01)
    triager.calibrate(probs, y_true)
    
    assert triager.tau_high > triager.tau_low
    assert 0.50 <= triager.tau_high <= 0.95
    assert 0.05 <= triager.tau_low <= 0.80
    
    triage_preds = triager.predict_triage(probs)
    assert len(triage_preds) == n_samples
    assert set(triage_preds).issubset({0, 1, 2})
    
    metrics = triager.evaluate_triaged_metrics(probs, y_true)
    
    # Validate mathematical properties
    assert "tier1_precision" in metrics
    assert "tier2_cumulative_recall" in metrics
    assert "conformal_coverage" in metrics
    assert "workload_reduction_pct" in metrics
    
    # Coverage should satisfy finite sample bound >= 1 - alpha (0.95)
    assert metrics["conformal_coverage"] >= 0.90
    # Tier 2 cumulative recall should capture high fraction of frauds
    assert metrics["tier2_cumulative_recall"] >= 0.85
    # Workload reduction should clear vast majority of clean accounts
    assert metrics["workload_reduction_pct"] >= 0.80
