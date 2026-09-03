"""
test_agents.py — Comprehensive Unit & Integration Tests for the Autonomous Multi-Agent AML Swarm.
Tests:
1. ForensicInvestigatorAgent: Subgraph traversal, Kirchhoff peeling, wash cycles, dormant delays.
2. SARDrafterAgent: Regulatory FinCEN Form 111 & FATF narrative generation.
3. ComplianceAuditorAgent: Statutory rule evaluation, citation mapping, audit verdicts.
4. AMLSwarmOrchestrator: End-to-end case dossier synthesis and batch alert processing.
"""

import unittest
import time
from src.agents.investigator_agent import ForensicInvestigatorAgent, ForensicEvidence
from src.agents.sar_drafter_agent import SARDrafterAgent
from src.agents.compliance_auditor_agent import ComplianceAuditorAgent, AuditVerdict
from src.agents.swarm_orchestrator import AMLSwarmOrchestrator, InvestigationDossier


class TestMultiAgentAMLSwarm(unittest.TestCase):
    """Test suite for the Autonomous Multi-Agent Compliance Swarm."""

    def setUp(self):
        self.investigator = ForensicInvestigatorAgent()
        self.sar_drafter = SARDrafterAgent(filing_institution="Test Financial Intelligence Bank")
        self.auditor = ComplianceAuditorAgent(approval_threshold=70.0, auto_escalate_volume_usd=50_000.0)
        self.orchestrator = AMLSwarmOrchestrator(filing_institution="Test Financial Intelligence Bank")

    def test_investigator_mule_peeling_conduit(self):
        """Test that the investigator correctly detects a rapid transit mule pass-through conduit."""
        now = time.time()
        in_edges = [
            {"source": "acct_source_1", "amount": 9500.0, "timestamp": now - 3600},
            {"source": "acct_source_2", "amount": 9200.0, "timestamp": now - 3500}
        ]
        out_edges = [
            {"target": "acct_target_1", "amount": 9450.0, "timestamp": now - 1800},
            {"target": "acct_target_2", "amount": 9150.0, "timestamp": now - 1700}
        ]

        evidence = self.investigator.investigate_subgraph(
            alert_entity_id="mule_conduit_account_01",
            risk_score=0.965,
            conformal_tier="Tier 1: Auto-Block",
            in_edges=in_edges,
            out_edges=out_edges
        )

        self.assertIsInstance(evidence, ForensicEvidence)
        self.assertGreaterEqual(evidence.kirchhoff_peeling_ratio, 0.90)
        self.assertIn("Pass-Through Mule Conduit (Rapid Layering)", evidence.detected_typologies)
        self.assertEqual(len(evidence.suspect_counterparties), 4)
        self.assertEqual(evidence.total_inbound_volume, 18700.0)
        self.assertEqual(evidence.total_outbound_volume, 18600.0)

    def test_investigator_circular_cycle_detection(self):
        """Test that the investigator catches circular wash-trading loops (A -> B -> A)."""
        now = time.time()
        in_edges = [{"source": "acct_entity_X", "amount": 5000.0, "timestamp": now - 1000}]
        out_edges = [{"target": "acct_entity_X", "amount": 4900.0, "timestamp": now}]

        evidence = self.investigator.investigate_subgraph(
            alert_entity_id="ring_node_01",
            risk_score=0.92,
            conformal_tier="Tier 1: Auto-Block",
            in_edges=in_edges,
            out_edges=out_edges
        )

        self.assertTrue(evidence.cycle_detected)
        self.assertTrue(any("Circular Wash Trading" in t for t in evidence.detected_typologies))

    def test_investigator_dormant_hibernation_delay(self):
        """Test that long-dwell hibernation (e.g. 45 days dormant) is accurately extracted."""
        t1 = 1700000000.0
        t2 = t1 + (45.0 * 86400.0)  # 45 days later
        in_edges = [{"source": "originator_a", "amount": 10000.0, "timestamp": t1}]
        out_edges = [{"target": "destination_b", "amount": 9900.0, "timestamp": t2}]

        evidence = self.investigator.investigate_subgraph(
            alert_entity_id="dormant_mule_01",
            risk_score=0.88,
            conformal_tier="Tier 2: Manual Review",
            in_edges=in_edges,
            out_edges=out_edges
        )

        self.assertAlmostEqual(evidence.dormant_delay_days, 45.0, delta=0.5)
        self.assertTrue(any("Long-Dwell Hibernation" in t for t in evidence.detected_typologies))

    def test_sar_drafter_output_structure(self):
        """Test that the SAR Drafter produces all mandatory FinCEN/FATF regulatory fields."""
        evidence = ForensicEvidence(
            alert_entity_id="test_subject_99",
            risk_score=0.985,
            conformal_tier="Tier 1: Auto-Block",
            total_inbound_volume=25000.0,
            total_outbound_volume=24800.0,
            kirchhoff_peeling_ratio=0.992,
            max_hop_depth=2,
            dormant_delay_days=30.0,
            detected_typologies=["Pass-Through Mule Conduit (Rapid Layering)", "Smurfing / Structuring"],
            suspect_counterparties=["c1", "c2", "c3"],
            transaction_trail=[{"type": "INBOUND", "counterparty": "c1", "amount": 25000.0, "timestamp": time.time()}],
            smurfing_burst_score=3.5,
            cycle_detected=False,
            sanctions_taint_score=0.95
        )

        sar = self.sar_drafter.draft_sar(evidence)

        self.assertIn("sar_id", sar)
        self.assertTrue(sar["sar_id"].startswith("SAR-INTELAML-"))
        self.assertEqual(sar["subject_entity_id"], "test_subject_99")
        self.assertIn("executive_summary", sar)
        self.assertIn("risk_assessment", sar)
        self.assertIn("financial_summary", sar)
        self.assertIn("part_iii_forensic_narrative", sar)
        self.assertIn("part_v_recommendation", sar)
        self.assertIn("IMMEDIATE ACTION REQUIRED", sar["part_v_recommendation"])

    def test_compliance_auditor_approval_verdict(self):
        """Test that high-confidence evidence earns an APPROVED_FOR_FIU_SUBMISSION verdict with legal citations."""
        evidence = ForensicEvidence(
            alert_entity_id="confirmed_laundering_node",
            risk_score=0.97,
            conformal_tier="Tier 1: Auto-Block",
            total_inbound_volume=15000.0,
            total_outbound_volume=14900.0,
            kirchhoff_peeling_ratio=0.993,
            max_hop_depth=2,
            dormant_delay_days=0.5,
            detected_typologies=["Pass-Through Mule Conduit (Rapid Layering)", "Smurfing / Structuring"],
            suspect_counterparties=["bank_x_1", "bank_x_2"],
            transaction_trail=[],
            smurfing_burst_score=4.0,
            cycle_detected=True,
            sanctions_taint_score=0.98
        )
        sar = self.sar_drafter.draft_sar(evidence)
        verdict = self.auditor.audit_sar(sar)

        self.assertIsInstance(verdict, AuditVerdict)
        self.assertEqual(verdict.verdict, "APPROVED_FOR_FIU_SUBMISSION")
        self.assertGreaterEqual(verdict.compliance_score, 80.0)
        self.assertTrue(len(verdict.regulatory_citations) >= 3)
        self.assertTrue(any("FATF Rec. 20" in c for c in verdict.regulatory_citations))

    def test_compliance_auditor_high_volume_escalation(self):
        """Test that multi-million dollar volume triggers immediate executive escalation."""
        evidence = ForensicEvidence(
            alert_entity_id="mega_whale_mule",
            risk_score=0.85,
            conformal_tier="Tier 1: Auto-Block",
            total_inbound_volume=500_000.0,
            total_outbound_volume=499_000.0,
            kirchhoff_peeling_ratio=0.998,
            max_hop_depth=3,
            dormant_delay_days=5.0,
            detected_typologies=["Pass-Through Mule Conduit"],
            suspect_counterparties=["entity_a", "entity_b"],
            transaction_trail=[],
            smurfing_burst_score=1.0,
            cycle_detected=False,
            sanctions_taint_score=0.80
        )
        sar = self.sar_drafter.draft_sar(evidence)
        verdict = self.auditor.audit_sar(sar)

        self.assertEqual(verdict.verdict, "ESCALATE_TO_CHIEF_OFFICER")

    def test_orchestrator_end_to_end_pipeline(self):
        """Test full swarm orchestration: Alert -> Investigation -> SAR -> Audit -> Dossier & Markdown."""
        now = time.time()
        dossier = self.orchestrator.process_alert(
            alert_entity_id="acct_fraud_target_888",
            risk_score=0.95,
            conformal_tier="Tier 1: Auto-Block",
            in_edges=[
                {"source": "src_1", "amount": 8000.0, "timestamp": now - 3600},
                {"source": "src_2", "amount": 8000.0, "timestamp": now - 3500}
            ],
            out_edges=[
                {"target": "dst_1", "amount": 7950.0, "timestamp": now - 100},
                {"target": "src_1", "amount": 7950.0, "timestamp": now}  # Circular loop + burst
            ]
        )

        self.assertIsInstance(dossier, InvestigationDossier)
        self.assertEqual(dossier.alert_entity_id, "acct_fraud_target_888")
        self.assertIn("APPROVED", dossier.investigation_status)

        # Test Markdown generation
        md_text = dossier.to_markdown()
        self.assertIn("# 🛡️ Autonomous AML Regulatory Dossier", md_text)
        self.assertIn("acct_fraud_target_888", md_text)
        self.assertIn("Forensic Graph Evidence", md_text)
        self.assertIn("Part III — FinCEN / FATF Forensic Narrative", md_text)

    def test_orchestrator_batch_processing(self):
        """Test batch processing of multiple alerts."""
        alerts = [
            {
                "alert_entity_id": f"batch_node_{i}",
                "risk_score": 0.90 + i * 0.02,
                "conformal_tier": "Tier 1: Auto-Block",
                "in_edges": [{"source": f"in_{i}", "amount": 1000.0 * (i + 1), "timestamp": time.time()}],
                "out_edges": [{"target": f"out_{i}", "amount": 990.0 * (i + 1), "timestamp": time.time()}]
            }
            for i in range(3)
        ]

        dossiers = self.orchestrator.batch_process_alerts(alerts)
        self.assertEqual(len(dossiers), 3)
        for i, d in enumerate(dossiers):
            self.assertEqual(d.alert_entity_id, f"batch_node_{i}")


if __name__ == "__main__":
    unittest.main()
