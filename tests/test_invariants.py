"""
test_invariants.py — Enterprise Mathematical Invariants & Compliance Verification.

Rigorously enforces:
1. Mathematical single source of truth (148,312 total, 1,280 Tier 1, 748 Tier 2, 146,284 Tier 3 -> 98.6% STP).
2. Straight-through rate consistency (98.6% derived, eliminating the 99.4% inconsistency).
3. Four-Eyes Dual Control server-side enforcement (SR 11-7 / OCC 2011-12 / FINRA Rule 3110).
4. Cryptographic audit chain SHA-256 integrity verification (FRE 902(11) / SEC 17a-4).
5. Anti-Tipping-Off statutory compliance in RFI documents (31 U.S.C. § 5318(g)(2)).
6. Grounded evidence attribution for SAR generation ({claim, evidence_ids}).
"""

import pytest
from src.engine.persistence import (
    TOTAL_TRANSACTIONS,
    TIER_1_QUARANTINE,
    TIER_2_REVIEW,
    TIER_3_CLEARED,
    STRAIGHT_THROUGH_RATE,
    IntelligentAMLDatabase,
    AuditBlock
)


def test_mathematical_volume_and_tier_invariants():
    """
    Asserts mathematical consistency across all volume and tier metrics:
    Tier 1 (1,280) + Tier 2 (748) + Tier 3 (146,284) MUST equal 148,312.
    """
    assert TIER_1_QUARANTINE + TIER_2_REVIEW + TIER_3_CLEARED == TOTAL_TRANSACTIONS
    assert TOTAL_TRANSACTIONS == 148_312
    assert TIER_1_QUARANTINE == 1_280
    assert TIER_2_REVIEW == 748
    assert TIER_3_CLEARED == 146_284


def test_straight_through_processing_rate_accuracy():
    """
    Asserts STP rate is precisely derived as 98.63% (displayed as 98.6%),
    verifying elimination of the erroneous 99.4% figure.
    """
    calculated_stp = TIER_3_CLEARED / TOTAL_TRANSACTIONS
    assert round(calculated_stp * 100, 1) == 98.6
    assert round(STRAIGHT_THROUGH_RATE * 100, 1) == 98.6
    # Strictly ensure it is NOT the hallucinated 99.4%
    assert round(calculated_stp * 100, 1) != 99.4


def test_tier_percentage_invariants():
    """
    Asserts tier distribution percentages sum to exactly 100%.
    """
    p_tier1 = (TIER_1_QUARANTINE / TOTAL_TRANSACTIONS) * 100  # ~0.86%
    p_tier2 = (TIER_2_REVIEW / TOTAL_TRANSACTIONS) * 100       # ~0.50%
    p_tier3 = (TIER_3_CLEARED / TOTAL_TRANSACTIONS) * 100      # ~98.63%

    assert round(p_tier1, 2) == 0.86
    assert round(p_tier2, 2) == 0.50
    assert round(p_tier3, 2) == 98.63
    assert round(p_tier1 + p_tier2 + p_tier3, 2) == 100.00


def test_four_eyes_dual_control_rejection():
    """
    Four-Eyes Dual Control: Server MUST reject a sign-off if the approver
    is identical to the case initiator (OCC 2011-12 / FINRA Rule 3110).
    """
    test_db = IntelligentAMLDatabase()
    case_id = "CASE-2026-0881"
    case = test_db.cases[case_id]
    initiator = case.initiator

    # Attempt self-approval -> Must raise PermissionError
    with pytest.raises(PermissionError) as exc_info:
        test_db.sign_off_case(case_id, approver=initiator, notes="Self-approval attempt")

    assert "Four-Eyes Dual Control violation" in str(exc_info.value)
    assert case.status != "APPROVED"


def test_four_eyes_dual_control_approval():
    """
    Four-Eyes Dual Control: Approvals from an independent second compliance officer
    must succeed and append a cryptographically hashed audit entry.
    """
    test_db = IntelligentAMLDatabase()
    case_id = "CASE-2026-0881"
    approver = "Elena Rostova (Compliance Director)"

    initial_blocks = len(test_db.audit_chain)
    updated_case = test_db.sign_off_case(case_id, approver=approver, notes="Independent review complete. Approved.")

    assert updated_case.status == "APPROVED"
    assert updated_case.second_approver == approver
    assert len(test_db.audit_chain) == initial_blocks + 1

    last_block = test_db.audit_chain[-1]
    assert last_block.event_type == "FOUR_EYES_DUAL_SIGNOFF"
    assert last_block.actor == approver
    assert last_block.payload["case_id"] == case_id


def test_cryptographic_audit_chain_verification():
    """
    Validates append-only SHA-256 hash chaining integrity.
    """
    test_db = IntelligentAMLDatabase()
    receipt = test_db.verify_audit_chain()

    assert receipt["is_valid"] is True
    assert receipt["status"] == "CRYPTOGRAPHICALLY_VERIFIED"
    assert receipt["total_blocks"] >= 3
    assert len(receipt["root_hash"]) == 64
    assert len(receipt["head_hash"]) == 64


def test_cryptographic_audit_chain_tamper_detection():
    """
    Tampering with any historical block in the audit ledger MUST break chain verification
    and flag the exact index of the compromised block.
    """
    test_db = IntelligentAMLDatabase()
    assert test_db.verify_audit_chain()["is_valid"] is True

    # Tamper with historical block payload
    compromised_block = test_db.audit_chain[1]
    compromised_block.payload["tampered_field"] = "MALICIOUS_INJECTION"

    tamper_receipt = test_db.verify_audit_chain()
    assert tamper_receipt["is_valid"] is False
    assert tamper_receipt["broken_block_index"] == 1
    assert "Payload tampering" in tamper_receipt["error"]


def test_anti_tipping_off_compliance():
    """
    Verifies adherence to 31 U.S.C. § 5318(g)(2) (Anti-Tipping-Off):
    Customer RFI templates and workflows must NEVER advise targets on AML detection thresholds,
    structuring amounts, or transfer splitting strategies.
    """
    test_db = IntelligentAMLDatabase()
    forbidden_terms = [
        "split your transfer",
        "under $10,000",
        "avoid reporting",
        "smurfing threshold",
        "below the reporting limit"
    ]

    for rfi in test_db.rfi_requests.values():
        text_content = f"{rfi.request_type} {' '.join(rfi.document_checklist)} {rfi.statutory_warning}".lower()
        for term in forbidden_terms:
            assert term not in text_content, f"Anti-Tipping-Off violation detected: '{term}' found in {rfi.id}"
        # Assert statutory confidentiality warning is present
        assert "31 u.s.c. § 5318(g)(2)" in rfi.statutory_warning.lower()


def test_grounded_evidence_sources_in_cases():
    """
    Every compliance case must substantiate its claims with explicit evidence IDs
    ({claim, evidence_ids}), replacing ungrounded agent confidence scores.
    """
    test_db = IntelligentAMLDatabase()
    for case in test_db.cases.values():
        if case.grounded_evidence:
            for evidence in case.grounded_evidence:
                assert "claim" in evidence
                assert "evidence_ids" in evidence
                assert len(evidence["evidence_ids"]) >= 1


def test_case_attachments_and_audit_provenance():
    """
    Verifies evidentiary file attachments are appended to cases and sealed into
    the cryptographic audit ledger with immutable provenance.
    """
    test_db = IntelligentAMLDatabase()
    case_id = "CASE-2026-0881"
    initial_chain_length = len(test_db.audit_chain)

    att = test_db.add_case_attachment(
        case_id=case_id,
        filename="subpoena_grand_jury_sdny.pdf",
        file_type="application/pdf",
        file_size="450 KB",
        uploaded_by="Sarah Jenkins"
    )

    assert att["id"].startswith("ATT_")
    assert att["filename"] == "subpoena_grand_jury_sdny.pdf"
    assert len(test_db.cases[case_id].attachments) >= 1
    assert len(test_db.audit_chain) == initial_chain_length + 1

    last_event = test_db.audit_chain[-1]
    assert last_event.event_type == "CASE_ATTACHMENT_UPLOADED"
    assert last_event.actor == "Sarah Jenkins"
    assert last_event.payload["attachment_id"] == att["id"]

    # Ensure chain verification passes with the new block
    assert test_db.verify_audit_chain()["is_valid"] is True

