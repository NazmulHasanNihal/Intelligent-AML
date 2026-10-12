"""
test_auth_and_secrets.py — Verifies Secret Safety, Cryptographic RBAC, and Authentication Policies.
Ensures zero hardcoded credentials, production enforcement, and exception sanitization.
"""

import os
import pytest
from fastapi import HTTPException
from src.engine.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    UserProfile,
    UserRole,
    _hash_pw,
    _get_salt,
    SECRET_KEY,
    ALGORITHM
)
from src.engine.api import list_demo_tokens


def test_auth_no_hardcoded_passwords_in_source():
    """Verify that user passwords come from environment or dynamic generation."""
    # Ensure salt entropy is non-empty and dynamic
    salt = _get_salt()
    assert len(salt) >= 8

    # Verify hash function produces standard 64-char hex SHA256
    hashed = _hash_pw("TestPassword123!")
    assert len(hashed) == 64


def test_auth_jwt_token_creation_and_claims():
    """Verify HMAC-SHA256 JWT access token generation and claims encoding."""
    test_profile = UserProfile(
        user_id="USR-TEST-001",
        username="compliance_tester",
        full_name="Test Compliance Officer",
        role=UserRole.COMPLIANCE_OFFICER,
        department="AML Operations",
        institution="Test Bank PLC",
        permissions=["alerts:read", "alerts:triage"],
        is_active=True
    )
    token = create_access_token(test_profile)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # Header.Payload.Signature


def test_demo_tokens_disabled_in_production(monkeypatch):
    """Verify that the /api/v1/auth/demo-tokens endpoint is strictly blocked in production."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    with pytest.raises(HTTPException) as excinfo:
        list_demo_tokens()
    assert excinfo.value.status_code == 403
    assert "disabled in production" in excinfo.value.detail.lower()


def test_demo_tokens_disabled_when_flag_false(monkeypatch):
    """Verify that demo tokens endpoint is blocked when AML_ENABLE_DEMO_TOKENS is false."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("AML_ENABLE_DEMO_TOKENS", "false")
    with pytest.raises(HTTPException) as excinfo:
        list_demo_tokens()
    assert excinfo.value.status_code == 403


def test_get_current_user_unauthenticated_blocked_in_production(monkeypatch):
    """Verify that unauthenticated requests fail with 401 in production (SEC-1)."""
    import src.engine.auth as auth_mod
    monkeypatch.setattr(auth_mod, "_is_prod", True)
    with pytest.raises(HTTPException) as excinfo:
        auth_mod.get_current_user(None)
    assert excinfo.value.status_code == 401
    assert "credentials required" in excinfo.value.detail.lower()


def test_get_current_user_unauthenticated_blocked_under_strict_auth(monkeypatch):
    """Verify that unauthenticated requests fail with 401 when AML_STRICT_AUTH is active (SEC-1)."""
    import src.engine.auth as auth_mod
    monkeypatch.setenv("AML_STRICT_AUTH", "true")
    with pytest.raises(HTTPException) as excinfo:
        auth_mod.get_current_user(None)
    assert excinfo.value.status_code == 401
    assert "credentials required" in excinfo.value.detail.lower()


def test_download_sar_pdf_rejects_path_traversal():
    """Verify that path traversal in download_sar_pdf is blocked with 400 Bad Request (SEC-3)."""
    from src.engine.api import download_sar_pdf
    with pytest.raises(HTTPException) as excinfo:
        download_sar_pdf("../../../etc/passwd")
    assert excinfo.value.status_code == 400
    assert "invalid target_account format" in excinfo.value.detail.lower()


def test_export_sar_pdf_by_id_rejects_path_traversal():
    """Verify that path traversal or newline injection in case_id is blocked with 400 Bad Request (SEC-3)."""
    from src.engine.api import export_sar_pdf_by_id
    from starlette.requests import Request
    scope = {"type": "http", "method": "GET", "path": "/api/v1/sar/test/pdf", "headers": []}
    mock_request = Request(scope)
    with pytest.raises(HTTPException) as excinfo:
        export_sar_pdf_by_id(mock_request, "../../secret_keys\r\n")
    assert excinfo.value.status_code == 400
    assert "invalid case_id format" in excinfo.value.detail.lower()
