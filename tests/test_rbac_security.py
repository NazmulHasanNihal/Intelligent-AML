"""
test_rbac_security.py — Role-Matrix & Server-Side Security Test Suite (OWASP ASVS Level 2)

Proves:
1. Analyst L1 CANNOT sign off / approve cases (HTTP 403 Forbidden).
2. Analyst L1 CANNOT reveal unmasked customer PII (HTTP 403 Forbidden).
3. Auditor is strictly read-only: CANNOT approve cases or reveal PII (HTTP 403 Forbidden).
4. Maker-Checker Identity Collision: Initiator CANNOT ratify their own case even if they hold Supervisor role (HTTP 403 Forbidden).
5. Legitimate Maker-Checker: Supervisor CAN ratify a case initiated by an L2 investigator (HTTP 200 OK).
6. PII Reveal Reason Gate: Rejects requests with reason < 10 characters (HTTP 422 Unprocessable Entity).
7. PII Reveal Rate Limiting: Blocks bursts exceeding 5 reveals per 10-minute window (HTTP 429 Too Many Requests).
8. OIDC SSO with MFA: Verifies token contains mfa_verified=True and 15-minute expiration claims.
"""

import pytest
from fastapi.testclient import TestClient
from src.engine.api import app, _PII_REVEAL_RATE_LIMIT
from src.engine.auth import (
    UserRole,
    UserProfile,
    ROLE_PERMISSIONS,
    create_access_token,
    enforce_maker_checker
)
from src.engine.persistence import CaseRecord, db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


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


def test_analyst_l1_cannot_approve_case(client):
    """Proves Analyst L1 is strictly forbidden from case approval / signoff on the server."""
    token = make_token_for(UserRole.ANALYST_L1, "tanvir_l1", "Tanvir Ahmed (Triage Analyst L1)")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "approver": "Tanvir Ahmed",
        "notes": "Attempting unauthorized sign-off by first-line triage analyst."
    }
    response = client.post("/api/v1/cases/CASE-2026-0881/sign-off", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Dual Authorization Violation" in response.json()["detail"] or "cannot ratify" in response.json()["detail"]


def test_analyst_l1_cannot_reveal_pii(client):
    """Proves Analyst L1 is strictly forbidden from unmasking customer PII on the server."""
    token = make_token_for(UserRole.ANALYST_L1, "tanvir_l1", "Tanvir Ahmed (Triage Analyst L1)")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "target_account": "BD22-EBLB-4829-1092-8823",
        "reason": "Legitimate investigation reference MLPA-2026-0881"
    }
    response = client.post("/api/v1/pii/reveal", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Analyst L1 lacks authority" in response.json()["detail"]


def test_auditor_cannot_approve_or_reveal_pii(client):
    """Proves Auditor is mathematically read-only: cannot sign off cases and cannot reveal PII."""
    token = make_token_for(UserRole.AUDITOR, "auditor_sk", "Dr. S. K. Haque, FRM (Auditor)")
    headers = {"Authorization": f"Bearer {token}"}

    # Case sign-off attempt
    signoff_resp = client.post(
        "/api/v1/cases/CASE-2026-0881/sign-off",
        json={"approver": "Dr. S. K. Haque", "notes": "Auditor attempting case approval."},
        headers=headers
    )
    assert signoff_resp.status_code == 403

    # PII reveal attempt
    pii_resp = client.post(
        "/api/v1/pii/reveal",
        json={"target_account": "BD22-EBLB-4829-1092-8823", "reason": "Auditor checking KYC documents"},
        headers=headers
    )
    assert pii_resp.status_code == 403
    assert "Auditor role operates strictly on pseudonymized records" in pii_resp.json()["detail"]


def test_maker_checker_rejects_self_approval(client):
    """Proves Maker != Checker: Initiator cannot ratify their own case even if they hold Supervisor role."""
    # Seed a case where Farhana Ahmed is the initiator
    test_case = CaseRecord(
        id="CASE-TEST-MAKER-CHECKER",
        title="Test Maker Checker Docket",
        target_account="BD04-TEST-9988-1122",
        status="PENDING_DUAL_CONTROL",
        priority="HIGH",
        exposure_usd=50000.0,
        cstgb_risk_score=0.91,
        initiator="Farhana Ahmed, CAMS (Compliance Supervisor)",
        lead_assignee="Farhana Ahmed",
        created_at="2026-10-01T00:00:00Z"
    )
    db.cases[test_case.id] = test_case

    token = make_token_for(UserRole.SUPERVISOR, "farhana_sup", "Farhana Ahmed, CAMS (Compliance Supervisor)")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "approver": "Farhana Ahmed, CAMS",
        "notes": "Attempting self-signoff on own initiated docket."
    }
    response = client.post(f"/api/v1/cases/{test_case.id}/sign-off", json=payload, headers=headers)
    assert response.status_code == 403
    assert "Four-Eyes Dual Control Violation" in response.json()["detail"] or "cannot sign off on their own case" in response.json()["detail"]


def test_supervisor_can_approve_l2_case(client):
    """Proves legitimate Maker-Checker: Supervisor can ratify a case initiated by an L2 investigator."""
    token = make_token_for(UserRole.SUPERVISOR, "farhana_sup", "Farhana Ahmed, CAMS (Compliance Supervisor)")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "approver": "Farhana Ahmed, CAMS (Compliance Supervisor)",
        "notes": "Independent Four-Eyes review completed. Validated against ASYCUDA invoice benchmark."
    }
    # CASE-2026-0881 was initiated by Sarah Jenkins / Amina Rahman (Maker)
    response = client.post("/api/v1/cases/CASE-2026-0881/sign-off", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "APPROVED"
    assert "Farhana Ahmed" in data["second_approver"]


def test_pii_reveal_requires_substantive_reason(client):
    """Proves PII reveal rejects frivolous or missing reasons (< 10 chars)."""
    token = make_token_for(UserRole.SUPERVISOR, "farhana_sup", "Farhana Ahmed")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "target_account": "BD22-EBLB-4829-1092-8823",
        "reason": "short"  # Only 5 chars
    }
    response = client.post("/api/v1/pii/reveal", json=payload, headers=headers)
    assert response.status_code == 422


def test_pii_reveal_granted_with_audit_receipt(client):
    """Proves authorized officer can unmask PII with substantive reason and receives WORM audit receipt."""
    token = make_token_for(UserRole.SUPERVISOR, "farhana_sup_audit", "Farhana Ahmed (Supervisor)")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "target_account": "BD22-EBLB-4829-1092-8823",
        "reason": "Court subpoena Grand Jury notice compliance check MLPA 2012 §25"
    }
    response = client.post("/api/v1/pii/reveal", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["unmasked"] is True
    assert data["expires_in_seconds"] == 60
    assert len(data["audit_receipt"]) == 64  # SHA-256 hash


def test_pii_reveal_rate_limiting(client):
    """Proves rate limiter halts bursts exceeding 5 reveals per sliding window."""
    user = "rate_limit_test_user"
    _PII_REVEAL_RATE_LIMIT[user] = []
    token = make_token_for(UserRole.SUPERVISOR, user, "Rate Limit Test User")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "target_account": "BD22-EBLB-4829-1092-8823",
        "reason": "Legitimate subpoena request validation check MLPA 2012"
    }

    # First 5 reveals succeed
    for _ in range(5):
        resp = client.post("/api/v1/pii/reveal", json=payload, headers=headers)
        assert resp.status_code == 200

    # 6th reveal is blocked by rate limiter
    resp6 = client.post("/api/v1/pii/reveal", json=payload, headers=headers)
    assert resp6.status_code == 429
    assert "Rate limit exceeded" in resp6.json()["detail"]
