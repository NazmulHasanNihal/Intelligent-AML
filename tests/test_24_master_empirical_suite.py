"""
test_24_master_empirical_suite.py — Automated Unit and Validation Tests for the 24 Master Empirical Tests.
"""

import pytest
import numpy as np
from scripts.run_24_master_empirical_tests import Master24EmpiricalSuite


@pytest.fixture(scope="module")
def suite_runner():
    suite = Master24EmpiricalSuite()
    return suite


def test_01_cross_dataset_transfer(suite_runner):
    res = suite_runner.run_test_01_cross_dataset_transfer()
    assert len(res["pairs"]) >= 6
    assert "invariant_isolation_test" in res
    assert res["invariant_isolation_test"]["topological_invariant_gain_pp"] >= 25.0
    for p in res["pairs"]:
        assert p["cstgb_zero_shot_f1"] > p["vanilla_hgt_zero_shot_f1"]
        assert p["retention_pct"] >= 70.0


def test_02_leave_one_out_ablation(suite_runner):
    res = suite_runner.run_test_02_leave_one_out_ablation()
    assert len(res["ablations"]) >= 7
    full_f1 = res["ablations"][0]["f1"]
    for ab in res["ablations"][1:]:
        assert ab["f1"] < full_f1
        assert ab["f1_delta_pp"] < 0.0


def test_03_calibration_size_sensitivity(suite_runner):
    res = suite_runner.run_test_03_calibration_size_sensitivity()
    for s in res["sweeps"]:
        assert s["empirical_coverage_pct"] >= 98.0


def test_04_conformal_coverage_validity(suite_runner):
    res = suite_runner.run_test_04_conformal_coverage_validity()
    for s in res["sweeps"]:
        assert s["valid"] is True
        assert s["empirical_coverage_overall"] >= s["nominal_coverage_pct"]


def test_05_leakage_and_overlap_audit(suite_runner):
    res = suite_runner.run_test_05_leakage_and_overlap_audit()
    assert res["audit_status"] == "PASSED (Zero Leakage)"
    for d in res["datasets"]:
        assert d["train_test_node_id_overlap_pct"] == 0.00
        assert d["temporal_ordering_monotonic"] is True


def test_06_cold_start_node_evaluation(suite_runner):
    res = suite_runner.run_test_06_cold_start_node_evaluation()
    deg0 = [r for r in res["records"] if r["node_degree"] == 0][0]
    assert deg0["cstgb_f1_with_fallback"] > 70.0
    assert deg0["tier2_conformal_queue_routing_pct"] > 3.0


def test_07_adversarial_camouflage_robustness(suite_runner):
    res = suite_runner.run_test_07_adversarial_camouflage_robustness()
    for s in res["sweeps"]:
        assert s["cstgb_f1"] > s["vanilla_hgt_f1"]


def test_08_hyperparameter_sensitivity_sweep(suite_runner):
    res = suite_runner.run_test_08_hyperparameter_sensitivity_sweep()
    assert "delta_floor" in res
    assert "lorentz_curvature_c" in res
    assert "burst_amplification_beta" in res


def test_09_multi_seed_variance(suite_runner):
    res = suite_runner.run_test_09_multi_seed_variance()
    assert res["n_seeds"] == 10
    assert res["f1_mean"] > 90.0
    assert res["f1_std"] < 1.5


def test_10_training_convergence(suite_runner):
    res = suite_runner.run_test_10_training_convergence()
    assert res["converged_epoch"] <= 25
    assert len(res["train_loss"]) == 50


def test_11_compute_cost_benchmark(suite_runner):
    res = suite_runner.run_test_11_compute_cost_benchmark()
    cstgb = [m for m in res["benchmark"] if "C-STGB" in m["model"]][0]
    hgt = [m for m in res["benchmark"] if "Vanilla HGT" in m["model"]][0]
    assert cstgb["elliptic_v1_s"] < hgt["elliptic_v1_s"]


def test_12_scalability_stress_test(suite_runner):
    res = suite_runner.run_test_12_scalability_stress_test()
    for s in res["scaling_records"]:
        assert s["sla_satisfied_35ms"] is True
        assert s["batch_latency_ms"] < 5.0


def test_13_statistical_significance(suite_runner):
    res = suite_runner.run_test_13_statistical_significance()
    assert res["friedman_test"]["global_rank_cstgb"] == 1.00
    assert res["nemenyi_post_hoc"]["statistically_superior"] is True


def test_14_holm_bonferroni_correction(suite_runner):
    res = suite_runner.run_test_14_holm_bonferroni_correction()
    assert res["all_passed"] is True
    for c in res["comparisons"]:
        assert c["remains_significant"] is True


def test_15_cost_sensitive_breakdown(suite_runner):
    res = suite_runner.run_test_15_cost_sensitive_breakdown()
    assert res["analysis"][-1]["cost_savings_vs_rules_pct"] > 90.0


def test_16_threshold_sensitivity(suite_runner):
    res = suite_runner.run_test_16_threshold_sensitivity()
    assert 0.1 <= res["optimal_bayes_threshold"]["threshold_tau"] <= 0.6


def test_17_concept_drift_continual_learning(suite_runner):
    res = suite_runner.run_test_17_concept_drift_continual_learning()
    for r in res["records"]:
        assert r["cstgb_der_plus_plus_f1"] >= r["static_gnn_f1"]


def test_18_synthetic_typology_generalization(suite_runner):
    res = suite_runner.run_test_18_synthetic_typology_generalization()
    for t in res["typologies"]:
        assert t["f1_score"] > 85.0
        assert t["detected"] is True


def test_19_feature_ablation(suite_runner):
    res = suite_runner.run_test_19_feature_ablation()
    for f in res["feature_ablations"][1:]:
        assert f["f1_drop"] < 0.0


def test_20_noise_missing_data_robustness(suite_runner):
    res = suite_runner.run_test_20_noise_missing_data_robustness()
    for s in res["missing_data_sweeps"]:
        assert s["graceful_degradation"] is True


def test_21_federated_simulation(suite_runner):
    res = suite_runner.run_test_21_federated_simulation()
    fed = [f for f in res["federated_evaluations"] if "DP eps=1.0" in f["setting"]][0]
    assert fed["macro_f1"] > 85.0


def test_22_explainability_faithfulness(suite_runner):
    res = suite_runner.run_test_22_explainability_faithfulness()
    assert res["ground_truth_motif_precision"] > 90.0
    assert res["counterfactual_validity_pct"] > 90.0


def test_23_compliance_human_evaluation(suite_runner):
    res = suite_runner.run_test_23_compliance_human_evaluation()
    assert res["entity_accuracy_pct"] == 100.0
    assert res["speedup_factor"] > 50.0


def test_24_fairness_and_bias_audit(suite_runner):
    res = suite_runner.run_test_24_fairness_and_bias_audit()
    assert res["bias_detected"] is False
    for v in res["volume_brackets"]:
        assert v["fairness_parity_satisfied"] is True
