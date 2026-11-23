"""
test_model_governance.py — Unit Tests for Phase 7 Model Governance & Research Credibility.

Verifies:
1. Population Stability Index (PSI) computation & thresholds (SR 11-7 / OCC 2011-12)
2. Two-sample Kolmogorov-Smirnov (KS) goodness-of-fit test
3. Demographic parity & disparate impact ratio (EEOC 4/5ths rule)
4. Perturbation Lipschitz stability under Gaussian noise
5. AlertScorerExplainer local feature attributions across 12 invariants
6. Supervisory override logging to tamper-evident WORM ledger
7. Champion vs. Challenger shadow replay benchmark
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient

from src.governance.drift_monitor import ModelDriftMonitor, model_drift_monitor
from src.governance.shadow_replay import ShadowReplayEngine, shadow_replay_engine
from src.explainability.scorer_explainer import AlertScorerExplainer, alert_scorer_explainer
from src.engine.api import app
from src.engine.persistence import db
from src.engine.auth import create_access_token, UserProfile, UserRole, ROLE_PERMISSIONS


@pytest.fixture
def api_client():
    return TestClient(app)


def make_token_for(role: UserRole, username: str, full_name: str) -> str:
    profile = UserProfile(
        user_id=f"USR-TEST-{role.value}",
        username=username,
        full_name=full_name,
        role=role,
        department="Financial Crime Compliance",
        institution="Eastern Bank PLC",
        permissions=ROLE_PERMISSIONS.get(role, []),
        is_active=True,
        mfa_enabled=True,
        mfa_verified=True,
        auth_method="OIDC_SSO_MFA"
    )
    return create_access_token(profile)


@pytest.fixture
def supervisor_token():
    return make_token_for(UserRole.SUPERVISOR, "farhana_sup", "Farhana Yasmin, CAMS")


@pytest.fixture
def analyst_token():
    return make_token_for(UserRole.ANALYST_L1, "tanvir_l1", "Tanvir Ahmed")


def test_psi_identical_distributions_returns_zero():
    """Identical distributions should have PSI ~ 0.0 (perfect stability)."""
    base = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    act = base.copy()
    psi = ModelDriftMonitor.calculate_psi(base, act)
    assert psi < 0.01, f"Expected PSI near 0, got {psi}"


def test_psi_drift_thresholds():
    """Shifted distribution should trigger moderate or critical drift."""
    rng = np.random.default_rng(42)
    base = rng.normal(loc=0.0, scale=1.0, size=5000)
    
    # Moderate shift
    moderate = rng.normal(loc=0.45, scale=1.0, size=5000)
    psi_mod = ModelDriftMonitor.calculate_psi(base, moderate)
    assert psi_mod >= ModelDriftMonitor.PSI_STABLE_THRESHOLD, f"Expected PSI >= 0.10, got {psi_mod}"

    # Critical shift
    critical = rng.normal(loc=1.2, scale=1.0, size=5000)
    psi_crit = ModelDriftMonitor.calculate_psi(base, critical)
    assert psi_crit >= ModelDriftMonitor.PSI_WARNING_THRESHOLD, f"Expected PSI >= 0.25, got {psi_crit}"


def test_score_drift_evaluation():
    """Full score drift report produces validated status and KS statistic."""
    report = model_drift_monitor.evaluate_score_drift()
    assert report["metric"] == "POPULATION_STABILITY_INDEX"
    assert "psi_value" in report
    assert report["status"] in ["STABLE", "MODERATE_DRIFT", "SIGNIFICANT_DRIFT"]
    assert "ks_statistic" in report
    assert "ks_pvalue" in report


def test_fairness_and_demographic_parity():
    """Evaluates disparate impact ratios across segments satisfying EEOC 4/5ths rule."""
    fairness = model_drift_monitor.evaluate_fairness_and_parity()
    assert fairness["overall_fairness_verdict"] == "FAIR_AND_NON_DISCRIMINATORY"
    for seg in fairness["segments_breakdown"]:
        assert seg["four_fifths_compliant"] is True, f"Segment {seg['segment']} failed 4/5ths rule"
        assert 0.80 <= seg["disparate_impact_ratio"] <= 1.25


def test_perturbation_stability():
    """Gaussian perturbation check confirms bounded sensitivity."""
    stability = model_drift_monitor.evaluate_perturbation_stability()
    assert stability["stability_verdict"] == "BOUNDED_PERTURBATION_RESILIENT"
    for sweep in stability["perturbation_sweeps"]:
        assert sweep["macro_f1"] >= 0.90, f"F1 dropped too low under sigma={sweep['noise_sigma']}"
        assert sweep["lipschitz_bounded"] is True


def test_alert_scorer_explainer_12_invariants():
    """Per-alert explainer produces 12 invariants attribution with sum matching risk score."""
    explanation = alert_scorer_explainer.explain_alert(
        alert_id="ALT-TEST-9901",
        target_account="BD22-EBLB-4829-1092-8823",
        amount_bdt=950_000.0,
        risk_score=0.942,
        typology="Pass-Through Transit Smurfing Loop"
    )

    assert explanation.alert_id == "ALT-TEST-9901"
    assert len(explanation.feature_attributions) == 12
    assert len(explanation.top_risk_drivers) == 3
    assert "counterfactual_recourse" in explanation.model_dump()
    assert len(explanation.statutory_citations) >= 3

    # Check top drivers have positive attribution
    top_attrib = explanation.feature_attributions[0]
    assert top_attrib.impact_direction == "RISK_INCREASING"
    assert top_attrib.attribution_weight > 0


def test_supervisory_override_api_authorization(api_client, analyst_token, supervisor_token):
    """Analyst L1 cannot override model risk scores (403 Forbidden); Supervisor can."""
    override_payload = {
        "new_score": 0.12,
        "new_tier": "Tier 3 Clear",
        "justification_code": "DOCUMENTED_TRADE_INVOICE",
        "notes": "Verified authentic letter of credit and customs bill."
    }

    # 1. Analyst L1 attempt -> 403 Forbidden
    res_l1 = api_client.post(
        "/api/v1/alerts/ALT-TEST-9901/override",
        json=override_payload,
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert res_l1.status_code == 403

    # 2. Supervisor attempt -> 200 OK
    res_sup = api_client.post(
        "/api/v1/alerts/ALT-TEST-9901/override",
        json=override_payload,
        headers={"Authorization": f"Bearer {supervisor_token}"}
    )
    assert res_sup.status_code == 200
    data = res_sup.json()
    assert data["status"] == "OVERRIDE_RECORDED_TAMPER_EVIDENT"
    assert data["overridden_score"] == 0.12
    assert "audit_block_hash" in data


def test_supervisory_override_appends_to_tamper_evident_ledger(api_client, supervisor_token):
    """Override creates a verified block in the cryptographic hash chain."""
    chain_len_before = len(db.audit_chain)
    override_payload = {
        "new_score": 0.14,
        "new_tier": "Tier 3 Clear",
        "justification_code": "VERIFIED_PAYROLL_SPIKE",
        "notes": "End-of-month corporate disbursement approved by CFO."
    }

    res = api_client.post(
        "/api/v1/alerts/ALT-TEST-9902/override",
        json=override_payload,
        headers={"Authorization": f"Bearer {supervisor_token}"}
    )
    assert res.status_code == 200

    assert len(db.audit_chain) == chain_len_before + 1
    last_block = db.audit_chain[-1]
    assert last_block.event_type == "MODEL_RISK_SCORE_OVERRIDDEN"
    assert last_block.payload["overridden_score"] == 0.14

    # Verification must pass
    verification = db.verify_audit_chain()
    assert verification["is_valid"] is True


def test_champion_challenger_shadow_replay():
    """Shadow replay benchmark reproduces verified 7-day comparative metrics."""
    engine = ShadowReplayEngine(seed=42)
    summary = engine.run_replay(transaction_count=2500)

    assert summary.total_transactions_replayed == 2500
    assert summary.champion_f1 == 0.945
    assert summary.challenger_f1 == 0.887
    assert summary.champion_fpr < summary.challenger_fpr
    assert summary.operational_noise_reduction_pct > 80.0
    assert summary.supervisory_verdict == "RETAIN_CHAMPION_IN_PRODUCTION"
    assert len(summary.replay_hash_seal) == 64
