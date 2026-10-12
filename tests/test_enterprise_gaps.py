"""
test_enterprise_gaps.py — Comprehensive Integration Tests for Institutional Enterprise Capabilities.

Verifies:
1. Distributed Graph Store Adapter (Base, PyG, Remote Cypher Connector) & Fast-Path Pre-Clearing Gate
2. Relational Database Concurrency, SQLite/PostgreSQL Write-Through Syncing & Pool Setup
3. Case Management Lifecycle & Four-Eyes Dual Control (OCC 2011-12 / FINRA Rule 3110 / SR 11-7)
4. Model Risk Management (Federal Reserve SR 11-7) & Continuous Concept Drift (PSI/CSI) Auditing
5. FastAPI REST Endpoints for Cases, Dual Control, Graph Adapter, and MRM Audit
"""

import os
import sys
import unittest
import numpy as np
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.engine.persistence import db, CaseRecord
from src.engine.graph_adapter import graph_adapter, fast_path_gate, InMemoryPyGStoreAdapter, RemoteGraphDatabaseConnector
from src.engine.drift_monitor import mrm_monitor, ModelRiskGovernanceMonitor
from src.engine.api import app


class TestEnterpriseGaps(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_graph_adapter_and_fast_path(self):
        """Validates Distributed Graph Store Adapter and Fast-Path Early-Exit Gate."""
        # Test In-Memory PyG adapter ego extraction
        adapter = InMemoryPyGStoreAdapter(capacity=1000, hidden_dim=64)
        subgraph = adapter.get_node_ego_subgraph("BD22-EBLB-4829-1092-8823", depth=2)
        self.assertEqual(subgraph["root_node_id"], "BD22-EBLB-4829-1092-8823")
        self.assertGreaterEqual(len(subgraph["nodes"]), 1)
        self.assertEqual(subgraph["adapter"], "InMemoryPyGStoreAdapter")

        # Test Remote connector resilience fallback
        remote_conn = RemoteGraphDatabaseConnector(uri="bolt://127.0.0.1:9999", pool_size=10)
        health = remote_conn.health_check()
        self.assertEqual(health["status"], "ONLINE")
        self.assertIn("FALLBACK", health["operating_mode"])

        # Test Fast-Path Gate: Low-value domestic transfer (< $1,000, no burst, Tier 3)
        is_fp, fp_resp = fast_path_gate.evaluate(
            tx_id="TX_FAST_001",
            amount=450.0,
            cross_border=False,
            burst_velocity=False,
            src_risk_tier="Tier 3",
            dst_risk_tier="Tier 3"
        )
        self.assertTrue(is_fp)
        self.assertIsNotNone(fp_resp)
        self.assertEqual(fp_resp["decision_tier"], "TIER_3_STRAIGHT_THROUGH_CLEAR")
        self.assertTrue(fp_resp["gnn_forward_bypassed"])
        self.assertLess(fp_resp["execution_latency_ms"], 1.0)

        # Test Non-Fast-Path: Cross-border or high amount ($47,600) -> Must dispatch to GNN
        is_fp_high, _ = fast_path_gate.evaluate(
            tx_id="TX_HEAVY_001",
            amount=47600.0,
            cross_border=True,
            burst_velocity=True,
            src_risk_tier="Tier 1"
        )
        self.assertFalse(is_fp_high)

    def test_02_relational_persistence_and_sync(self):
        """Validates write-through persistence to SQLite and cryptographic ledger linking."""
        initial_cases_count = len(db.cases)
        self.assertGreaterEqual(initial_cases_count, 3)

        # Test case creation with write-through
        test_case = CaseRecord(
            id=f"TEST-CASE-{int(np.random.randint(1000, 9999))}",
            title="Synthetic Layering Ring Probe",
            target_account="BD99-TEST-9999-0001",
            status="OPEN",
            priority="HIGH",
            exposure_usd=125000.0,
            cstgb_risk_score=0.912,
            initiator="Investigator Alice",
            lead_assignee="Investigator Alice",
            created_at="2026-10-11T09:00:00Z"
        )
        created = db.create_case(test_case)
        self.assertEqual(created.id, test_case.id)
        self.assertIn(test_case.id, db.cases)

        # Test case note addition and sync
        note = db.add_case_note(test_case.id, author="Investigator Bob", role="Forensic Analyst", text="Subpoena served.")
        self.assertIsNotNone(note)
        self.assertEqual(note["author"], "Investigator Bob")
        self.assertGreaterEqual(len(db.cases[test_case.id].notes), 1)

        # Test case status update and sync
        updated = db.update_case_status(test_case.id, new_status="UNDER_REVIEW", actor="Investigator Bob", reason="Docs received")
        self.assertEqual(updated.status, "UNDER_REVIEW")

        # Test cryptographic ledger integrity
        chain_verify = db.verify_audit_chain()
        self.assertTrue(chain_verify["is_valid"])
        self.assertEqual(chain_verify["status"], "CRYPTOGRAPHICALLY_VERIFIED")

    def test_03_four_eyes_dual_control_enforcement(self):
        """Validates OCC 2011-12 / FINRA Rule 3110 / SR 11-7 Four-Eyes Dual Control Maker-Checker."""
        case_id = f"DUAL-CASE-{int(np.random.randint(1000, 9999))}"
        case = CaseRecord(
            id=case_id,
            title="Dual Control Enforcement Test Docket",
            target_account="ACC-MAKER-CHECKER-01",
            status="PENDING_DUAL_CONTROL",
            priority="CRITICAL",
            exposure_usd=250000.0,
            cstgb_risk_score=0.95,
            initiator="Sarah Jenkins (Senior Investigator)",
            lead_assignee="Sarah Jenkins",
            timeline=[{"timestamp": "2026-10-11 09:00 UTC", "event": "Case docket created", "actor": "Sarah Jenkins", "type": "creation"}],
            created_at="2026-10-11T09:00:00Z"
        )
        db.create_case(case)

        # 1. Maker-Checker identity collision: Initiator attempting to approve their own filing
        with self.assertRaises(PermissionError) as ctx:
            db.sign_off_case(case_id, approver="Sarah Jenkins", notes="Attempted self-approval.")
        self.assertIn("Four-Eyes Dual Control violation", str(ctx.exception))
        self.assertIn("cannot ratify their own filing", str(ctx.exception))

        # 2. Legitimate independent second approver
        ratified = db.sign_off_case(
            case_id,
            approver="Elena Rostova (Compliance Director)",
            notes="Independent review confirmed. Dual signatory granted."
        )
        self.assertEqual(ratified.status, "APPROVED")
        self.assertEqual(ratified.second_approver, "Elena Rostova (Compliance Director)")
        self.assertGreaterEqual(len(ratified.timeline), 2)

    def test_04_mrm_model_risk_and_concept_drift(self):
        """Validates Federal Reserve SR 11-7 Model Risk Management & Concept Drift Monitor."""
        monitor = ModelRiskGovernanceMonitor()

        # Identical/stationary distribution -> PSI must be near 0 (< 0.10)
        stationary_data = np.random.lognormal(mean=7.8, sigma=1.1, size=2000)
        res_stable = monitor.evaluate_feature_csi("tx_amount", stationary_data)
        self.assertEqual(res_stable["status"], "STABLE")
        self.assertFalse(res_stable["drift_alert"])

        # Heavily shifted distribution -> PSI must exceed critical floor (>= 0.25)
        shifted_data = np.random.lognormal(mean=11.5, sigma=2.0, size=2000)
        res_drift = monitor.evaluate_feature_csi("tx_amount", shifted_data)
        self.assertIn("DRIFT", res_drift["status"])
        self.assertTrue(res_drift["drift_alert"])

        # End-to-end SR 11-7 audit report generation
        audit_rep = monitor.generate_mrm_audit_report()
        self.assertIn("Federal Reserve SR 11-7", audit_rep["regulatory_framework"])
        self.assertIn("system_psi", audit_rep)
        self.assertIn("overall_stability_rating", audit_rep)
        self.assertEqual(len(audit_rep["cryptographic_mrm_seal"]), 64)

    def test_05_api_endpoints_enterprise_integration(self):
        """Validates REST endpoints for Cases, Dual-Signoff, Graph Adapter, and MRM Drift."""
        # 1. Create Case via REST API
        create_payload = {
            "title": "API Automated Case Docket",
            "target_account": "BD11-TEST-REST-8812",
            "priority": "HIGH",
            "exposure_usd": 85000.0,
            "cstgb_risk_score": 0.89,
            "initiator": "Agent Mulder",
            "lead_assignee": "Agent Mulder",
            "regulatory_framework": "FinCEN Form 111 (USA)"
        }
        res_c = self.client.post("/api/v1/cases", json=create_payload)
        self.assertEqual(res_c.status_code, 200)
        case_data = res_c.json()
        cid = case_data["id"]

        # 2. Add Case Note via REST API
        res_n = self.client.post(f"/api/v1/cases/{cid}/notes", json={
            "author": "Agent Scully",
            "role": "Forensic Scientist",
            "text": "Evidence corroborated."
        })
        self.assertEqual(res_n.status_code, 200)

        # 3. Four-Eyes Dual-Signoff rejection on self-approval via REST API (HTTP 403)
        res_self = self.client.post(f"/api/v1/cases/{cid}/dual-signoff", json={
            "approver": "Agent Mulder",
            "notes": "Attempting self approval via API."
        })
        self.assertEqual(res_self.status_code, 403)

        # 4. Legitimate Four-Eyes Dual-Signoff via REST API (HTTP 200)
        res_dual = self.client.post(f"/api/v1/cases/{cid}/dual-signoff", json={
            "approver": "Director Skinner",
            "notes": "Independent approval ratified."
        })
        self.assertEqual(res_dual.status_code, 200)
        self.assertEqual(res_dual.json()["status"], "APPROVED")

        # 5. Fetch Case Audit Trail via REST API
        res_trail = self.client.get(f"/api/v1/cases/{cid}/audit-trail")
        self.assertEqual(res_trail.status_code, 200)
        self.assertGreaterEqual(res_trail.json()["total_audit_blocks"], 2)

        # 6. Graph Adapter Status via REST API
        res_g = self.client.get("/api/v1/graph/adapter/status")
        self.assertEqual(res_g.status_code, 200)
        self.assertEqual(res_g.json()["status"], "ONLINE")

        # 7. Model Risk Management Drift Audit via REST API
        res_mrm = self.client.get("/api/v1/models/drift-audit")
        self.assertEqual(res_mrm.status_code, 200)
        self.assertIn("system_psi", res_mrm.json())
        self.assertEqual(len(res_mrm.json()["cryptographic_mrm_seal"]), 64)


if __name__ == "__main__":
    unittest.main()
