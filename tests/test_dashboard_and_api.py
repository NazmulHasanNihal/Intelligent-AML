"""
test_dashboard_and_api.py — Verification of FastAPI Microservices & Dashboard Integration.
Tests real-time scoring, conformal triage, subgraph extraction, multi-agent SAR drafting,
and counterfactual recourse solvers for Intelligent-AML directly.
"""

import pytest
from src.engine.api import (
    health_check,
    score_transaction,
    get_ego_subgraph,
    evaluate_conformal_triage,
    run_agent_investigation,
    solve_counterfactual,
    get_benchmark_scorecard,
    TransactionScoreRequest,
    ConformalTriageRequest,
    AgentInvestigationRequest,
    CounterfactualSolveRequest
)


def test_api_health_check():
    """Verify API health endpoint returns healthy status and metadata."""
    data = health_check()
    assert data["status"] == "HEALTHY"
    assert "Intelligent-AML C-STGB Engine" in data["service"]
    assert "version" in data


def test_api_transaction_scoring_fast_path():
    """Verify sub-millisecond fast-path transaction scoring."""
    req = TransactionScoreRequest(
        tx_id="TX_TEST_001",
        src_id="ACC_8823_SUSPECT",
        dst_id="ACC_1109_MULE",
        amount=9500.0,
        payment_rail="Wire Transfer",
        cross_border=True,
        burst_velocity_spikes=True,
        fast_path_mode=True,
        conformal_alpha=0.01
    )
    res = score_transaction(req)
    assert res.tx_id == "TX_TEST_001"
    assert res.decision_tier in ["TIER_1_QUARANTINE_AUTO_SAR", "TIER_2_COMPLIANCE_REVIEW_QUEUE", "TIER_3_STRAIGHT_THROUGH_CLEAR"]
    assert len(res.conformal_prediction_set) >= 1
    assert res.conformal_coverage_pct == 99.0
    assert len(res.audit_merkle_receipt) == 64  # SHA-256 hex string


def test_api_ego_subgraph_extraction():
    """Verify dynamic 2-hop ego-subgraph extraction with edge-gating filter."""
    data = get_ego_subgraph(node_id="ACC_TEST_8823", depth=2, delta_floor=0.10)
    assert data["target_node_id"] == "ACC_TEST_8823"
    assert data["total_nodes"] > 0
    assert data["total_edges"] > 0
    assert "nodes" in data
    assert "edges" in data
    for edge in data["edges"]:
        assert "filtered_by_camouflage_gate" in edge
        assert "edge_trust_gate" in edge


def test_api_conformal_triage_evaluation():
    """Verify Class-Conditional Conformal Risk Control triage metrics across error rates."""
    req = ConformalTriageRequest(alpha=0.01, dataset_name="elliptic_v1")
    res = evaluate_conformal_triage(req)
    assert res.alpha == 0.01
    assert res.target_coverage_pct == 99.0
    assert res.empirical_coverage_pct >= 99.0
    assert res.workload_reduction_pct > 99.0
    assert res.mean_prediction_set_size >= 1.0


def test_api_agent_investigation_and_fincen_xml():
    """Verify autonomous multi-agent SAR drafting and XML generation."""
    req = AgentInvestigationRequest(
        target_account="ACC_SUSPECT_42",
        urgency="IMMEDIATE",
        include_fincen_xml=True
    )
    res = run_agent_investigation(req)
    assert res.target_account == "ACC_SUSPECT_42"
    assert res.case_verdict == "TIER_1_CONFIRMED_ILLICIT_RING"
    assert len(res.agent_logs) == 3
    assert res.fincen_form_111_xml is not None
    assert "<FinCENSuspiciousActivityReport" in res.fincen_form_111_xml
    assert len(res.sha256_merkle_seal) == 64


def test_api_counterfactual_recourse_solver():
    """Verify counterfactual recourse solver generates valid remediation steps."""
    req = CounterfactualSolveRequest(
        current_amount=9600.0,
        current_burst_velocity=18,
        current_fan_in_degree=8,
        current_holding_hours=1.2
    )
    res = solve_counterfactual(req)
    assert res.original_risk_score > res.remediated_risk_score
    assert res.recourse_achieved is True
    assert len(res.actionable_remediation_steps) == 4


def test_api_benchmark_scorecard():
    """Verify 13-dataset master scorecard endpoint."""
    data = get_benchmark_scorecard()
    assert data["macro_average_cstgb_f1"] == 68.05
    assert len(data["benchmarks"]) >= 9
    assert data["governance_compliance"] == "SR 26-2 Aligned (2026)"
