"""
test_audit_ledger.py - Automated Verification of Tamper-Evident Hash Chain & Ed25519 Checkpointing
Validates:
1. Pristine hash-chained audit ledger passes verification.
2. Modifying any historical row content makes verification fail and pinpoints exact first_broken_row.
3. Modifying prev_hash pointer makes verification fail and pinpoints exact first_broken_row.
4. Tampering genesis block #0 makes verification fail at row 0.
5. Ed25519 asymmetric signatures and Merkle tree roots verify cryptographically.
"""

import pytest
import os
import shutil
import tempfile
from src.engine.persistence import IntelligentAMLDatabase
from src.engine.audit_checkpointer import AuditCheckpointer


@pytest.fixture
def temp_db():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_aml.db")
    db = IntelligentAMLDatabase(db_path=db_path)
    # Add a few distinct audit events
    db.append_audit_event("ALERT_TRIAGE", "BNK-001", {"alert_id": "ALT-101", "action": "QUARANTINE"})
    db.append_audit_event("CASE_ESCALATION", "BNK-002", {"case_id": "CASE-201", "priority": "HIGH"})
    db.append_audit_event("SAR_SUBMISSION", "BNK-003", {"sar_id": "SAR-301", "goaml_status": "PENDING"})
    yield db
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_pristine_audit_chain_passes_verification(temp_db):
    """A clean, untampered audit chain must return is_valid=True and first_broken_row=None."""
    res = temp_db.verify_audit_chain()
    assert res["is_valid"] is True
    assert res["first_broken_row"] is None
    assert res["status"] == "TAMPER_EVIDENT_VERIFIED"
    assert res["total_blocks"] >= 4  # genesis + 3 events
    assert "latest_checkpoint" in res
    assert res["latest_checkpoint"]["signature_algorithm"] == "Ed25519 (RFC 8032)"


def test_payload_tampering_fails_verification_and_reports_first_broken_row(temp_db):
    """Modifying historical payload in row 1 must fail verification and pinpoint first_broken_row == 1."""
    # Tamper with row 1 payload
    temp_db.audit_chain[1].payload["alert_id"] = "ALT-TAMPERED-999"

    res = temp_db.verify_audit_chain()
    assert res["is_valid"] is False
    assert res["first_broken_row"] == 1
    assert res["broken_block_index"] == temp_db.audit_chain[1].index
    assert res["status"] == "TAMPER_DETECTED"
    assert "Payload tampering at row #1" in res["error"]


def test_pointer_tampering_fails_verification_and_reports_first_broken_row(temp_db):
    """Modifying prev_hash pointer in row 2 must fail verification and pinpoint first_broken_row == 2."""
    temp_db.audit_chain[2].prev_hash = "0" * 64

    res = temp_db.verify_audit_chain()
    assert res["is_valid"] is False
    assert res["first_broken_row"] == 2
    assert res["broken_block_index"] == temp_db.audit_chain[2].index
    assert res["status"] == "TAMPER_DETECTED"
    assert "Pointer mismatch at row #2" in res["error"]


def test_genesis_tampering_fails_verification_and_reports_row_0(temp_db):
    """Modifying genesis block payload must fail verification and report row 0."""
    temp_db.audit_chain[0].payload["genesis_note"] = "FORGED_GENESIS"

    res = temp_db.verify_audit_chain()
    assert res["is_valid"] is False
    assert res["first_broken_row"] == 0
    assert res["status"] == "TAMPER_DETECTED"
    assert "Genesis block #0 payload altered" in res["error"]


def test_ed25519_checkpoint_signature_and_verification(temp_db):
    """AuditCheckpointer must verify authentic checkpoints and reject forged signatures or Merkle roots."""
    checkpointer = temp_db.checkpointer
    checkpoint = checkpointer.create_checkpoint(temp_db.audit_chain)

    # 1. Valid checkpoint passes
    assert checkpointer.verify_checkpoint(checkpoint, temp_db.audit_chain) is True

    # 2. Forged Merkle root fails verification
    corrupted_data = checkpoint.to_dict()
    from src.engine.audit_checkpointer import AuditCheckpoint
    corrupted_obj = AuditCheckpoint(
        checkpoint_id=corrupted_data["checkpoint_id"],
        start_index=corrupted_data["block_range"][0],
        end_index=corrupted_data["block_range"][1],
        root_hash=corrupted_data["root_hash"],
        head_hash=corrupted_data["head_hash"],
        merkle_root="0" * 64,  # Corrupted Merkle root
        timestamp=corrupted_data["timestamp"],
        ed25519_signature=corrupted_data["ed25519_signature"],
        public_key_hex=corrupted_data["public_key_hex"],
        object_lock_uri=corrupted_data["anchored_object_lock_uri"]
    )
    assert checkpointer.verify_checkpoint(corrupted_obj, temp_db.audit_chain) is False
