"""
tests/test_phase1_enhancements.py
Validates the new Phase 1 production enhancements:
1. Regulatory SAR PDF Generator & SHA-256 Seal
2. Model Drift Detector (PSI, KS Test, Wasserstein)
3. Accelerated Sanctions Engine (Soundex, Inverted Token Index)
4. AML Forensic Copilot & Statutory Legal Grounding
5. REST API Integration Endpoints
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient
from src.engine.api import app
from src.engine.sar_pdf_exporter import sar_pdf_generator
from src.models.drift_detector import drift_detector
from src.engine.sanctions_engine import sanctions_engine, ScreeningRequest, soundex
from src.engine.aml_copilot import aml_copilot


@pytest.fixture
def client():
    return TestClient(app)


def test_regulatory_sar_pdf_generation():
    """Verifies official PDF creation and byte stream structure."""
    case_payload = {
        "case_id": "SAR-2026-QA-001",
        "target_entity": "ACC-TEST-SUBJECT-99",
        "risk_score": 0.965,
        "conformal_bound": "[0.932, 0.994] (95% Coverage)",
        "jurisdiction": "FinCEN / BFIU Global Tier-1"
    }
    pdf_bytes = sar_pdf_generator.generate_sar_pdf(case_payload)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF")


def test_model_drift_detector_psi_and_ks():
    """Verifies mathematical calculation of PSI and KS 2-sample tests."""
    report = drift_detector.evaluate_system_drift()
    assert "overall_status" in report
    assert "features" in report
    assert report["features_evaluated"] >= 5

    # Check feature-level properties
    for feat in report["features"]:
        assert "psi" in feat
        assert "ks_statistic" in feat
        assert "ks_p_value" in feat
        assert feat["psi"] >= 0.0
        assert 0.0 <= feat["ks_p_value"] <= 1.0


def test_soundex_phonetic_matching():
    """Verifies Soundex phonetic hashing."""
    assert soundex("Robert") == "R163"
    assert soundex("Rupert") == "R163"
    assert soundex("Smith") == soundex("Smyth")


def test_sanctions_engine_indexing_and_screening():
    """Verifies fast candidate indexed screening."""
    req = ScreeningRequest(query="Meghna Industrial", threshold=0.70)
    res = sanctions_engine.screen_entity(req)
    assert res.matches_found >= 1
    assert res.highest_score >= 0.85
    assert res.recommended_action in ["MANDATORY_ASSET_FREEZE_24H", "ENHANCED_DUE_DILIGENCE"]


def test_aml_copilot_case_explanation():
    """Verifies statutory grounding and legal citations."""
    explanation = aml_copilot.explain_case(
        case_id="CASE-AUTO-01",
        entity_id="ACC-SHELL-77",
        risk_score=0.93,
        flow_phi=-0.89
    )
    assert "executive_narrative" in explanation
    assert len(explanation["statutes_cited"]) >= 1
    assert len(explanation["recommended_investigative_actions"]) >= 1


def test_api_sar_pdf_download_endpoint(client):
    """Verifies GET /api/v1/sar/{case_id}/pdf."""
    response = client.get("/api/v1/sar/SAR-TEST-ID-992/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=\"SAR_SAR-TEST-ID-992.pdf\"" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")


def test_api_model_drift_endpoint(client):
    """Verifies GET /api/v1/models/drift-status."""
    response = client.get("/api/v1/models/drift-status")
    assert response.status_code == 200
    data = response.json()
    assert "overall_status" in data
    assert "features" in data


def test_api_copilot_explain_endpoint(client):
    """Verifies POST /api/v1/copilot/explain."""
    payload = {
        "case_id": "CASE-100",
        "entity_id": "ACC-MULE-12",
        "risk_score": 0.94,
        "flow_phi": -0.85
    }
    response = client.post("/api/v1/copilot/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "executive_narrative" in data
    assert "statutes_cited" in data
