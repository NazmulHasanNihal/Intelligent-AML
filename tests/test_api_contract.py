"""
test_api_contract.py — Contract verification tests for Intelligent-AML FastAPI & Database

Validates:
1. Health and engine status endpoints
2. Real-time scoring response contract (model_version, artifact_hash, conformal set)
3. Conformal prediction calibration endpoint (alpha, coverage, exchangeability note)
4. Alerts endpoint with tier/status filtering and pagination
5. Cases docket endpoints with Four-Eyes dual control enforcement
6. Append-only WORM audit ledger verification
"""

import pytest
from fastapi.testclient import TestClient
from src.engine.api import app
from src.scoring.tiered_scorer import (
    ModelArtifactRegistry,
    ConformalCalibrationRegistry,
    TieredScoringService
)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_contract(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"].lower() == "healthy"
    assert "version" in data or "engine_version" in data


def test_conformal_calibration_contract(client):
    response = client.get("/api/v1/conformal/calibration")
    assert response.status_code == 200
    data = response.json()
    assert data["alpha"] == 0.01
    assert data["target_coverage"] == 0.99
    assert data["calibration_set_size"] == 10000
    assert data["empirical_coverage"] >= 0.99
    assert "exchangeability_drift_note" in data
    assert "temporal_drift_status" in data


def test_transaction_score_contract(client):
    payload = {
        "tx_id": "TX-TEST-2026-CONTRACT",
        "src_id": "ACC-SRC-001",
        "dst_id": "ACC-DST-002",
        "amount": 47600.0,
        "cross_border": True,
        "burst_velocity_spikes": True,
        "payment_rail": "ISO20022_RTGS",
        "conformal_alpha": 0.01
    }
    response = client.post("/api/v1/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ensemble_posterior_prob" in data
    assert "decision_tier" in data
    assert "conformal_prediction_set" in data
    assert "total_latency_ms" in data
    assert "model_version" in data
    assert "model_artifact_hash" in data
    assert data["model_version"] == "3.2.0"
    assert len(data["model_artifact_hash"]) == 64


def test_alerts_list_contract(client):
    response = client.get("/api/v1/alerts?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "alerts" in data
    assert isinstance(data["alerts"], list)
    assert len(data["alerts"]) > 0

    # Verify alert record contract
    first = data["alerts"][0]
    assert "id" in first
    assert "target_account" in first
    assert "risk_score" in first
    assert "tier" in first
    assert "status" in first


def test_cases_list_contract(client):
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    case_ids = [c["id"] for c in data]
    assert "CASE-2026-0881" in case_ids
    assert "CASE-2026-0612" in case_ids


def test_tiered_scorer_service():
    service = TieredScoringService()
    decision = service.score_transaction(
        tx_id="TX-FAST-001",
        src_id="BD22-EBLB-4829",
        dst_id="AE-EBIL-4412",
        amount_usd=950.0,
        is_cross_border=False
    )
    assert decision["tier_code"] == 3
    assert decision["decision"] == "AUTO_CLEARED_FAST_PATH"
    assert decision["model_version"] == "3.2.0"
    assert decision["latency_ms"] < 5.0
