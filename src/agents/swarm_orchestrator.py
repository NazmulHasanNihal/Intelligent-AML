"""
swarm_orchestrator.py — Autonomous Multi-Agent AML Swarm Orchestrator.
Coordinates the end-to-end pipeline connecting C-STGB alerts with:
1. Forensic Investigator Agent (deep graph traversal)
2. SAR Drafter Agent (regulatory compliance narrative generation)
3. Compliance Auditor Agent (statutory rule validation & approval)
"""

import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .investigator_agent import ForensicInvestigatorAgent, ForensicEvidence
from .sar_drafter_agent import SARDrafterAgent
from .compliance_auditor_agent import ComplianceAuditorAgent, AuditVerdict


@dataclass
class InvestigationDossier:
    """Complete end-to-end regulatory compliance case dossier."""
    case_id: str
    alert_entity_id: str
    investigation_status: str
    forensic_evidence: ForensicEvidence
    drafted_sar: Dict[str, Any]
    audit_verdict: AuditVerdict
    creation_time: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "alert_entity_id": self.alert_entity_id,
            "investigation_status": self.investigation_status,
            "forensic_evidence": self.forensic_evidence.to_dict(),
            "drafted_sar": self.drafted_sar,
            "audit_verdict": {
                "sar_id": self.audit_verdict.sar_id,
                "verdict": self.audit_verdict.verdict,
                "confidence_level": self.audit_verdict.confidence_level,
                "regulatory_citations": self.audit_verdict.regulatory_citations,
                "compliance_score": self.audit_verdict.compliance_score,
                "auditor_comments": self.audit_verdict.auditor_comments,
                "audit_timestamp": self.audit_verdict.audit_timestamp
            },
            "creation_time": self.creation_time
        }

    def to_markdown(self) -> str:
        """Renders the entire case dossier as a clean, publication-grade Markdown report."""
        sar = self.drafted_sar
        verdict = self.audit_verdict
        ev = self.forensic_evidence

        md = []
        md.append(f"# 🛡️ Autonomous AML Regulatory Dossier: `{self.case_id}`")
        md.append(f"**Target Entity:** `{self.alert_entity_id}` | **Filing Status:** `{verdict.verdict}`")
        md.append(f"**Compliance Score:** `{verdict.compliance_score:.1f}/100` | **Confidence:** `{verdict.confidence_level*100:.1f}%`\n")
        
        md.append("## 1. Executive Summary")
        md.append(sar.get("executive_summary", "N/A") + "\n")

        md.append("## 2. Forensic Graph Evidence")
        md.append(f"- **ML Risk Probability:** `{ev.risk_score:.4f}` ({ev.risk_score*100:.1f}%)")
        md.append(f"- **Conformal Risk Tier:** `{ev.conformal_tier}`")
        md.append(f"- **Kirchhoff Peeling Ratio:** `{ev.kirchhoff_peeling_ratio:.4f}`")
        md.append(f"- **Smurfing Burst Intensity:** `{ev.smurfing_burst_score:.2f} tx/hr`")
        md.append(f"- **Circular Cycle Detected:** `{'YES' if ev.cycle_detected else 'NO'}`")
        md.append(f"- **Long-Dwell Dormancy:** `{ev.dormant_delay_days:.1f} Days`")
        md.append(f"- **Total Flow Volume:** `${ev.total_inbound_volume + ev.total_outbound_volume:,.2f} USD`")
        md.append(f"- **Counterparty Entities ({len(ev.suspect_counterparties)}):** `{', '.join(ev.suspect_counterparties[:8])}`\n")

        md.append("## 3. Statutory Regulatory Audit & Legal Citations")
        for cite in verdict.regulatory_citations:
            md.append(f"- 📜 **{cite}**")
        md.append(f"\n**Auditor Findings:** {verdict.auditor_comments}\n")

        md.append("## 4. Part III — FinCEN / FATF Forensic Narrative")
        md.append("```text")
        md.append(sar.get("part_iii_forensic_narrative", ""))
        md.append("```\n")

        md.append("## 5. Recommended Action Plan")
        md.append(f"> **{sar.get('part_v_recommendation', '')}**\n")

        return "\n".join(md)


class AMLSwarmOrchestrator:
    """
    Master Orchestration Engine for the Autonomous Multi-Agent Compliance Swarm.
    Dispatches alerts through Investigator, Drafter, and Auditor agents in sub-second time.
    """
    def __init__(self, filing_institution: str = "Intelligent-AML Tier-1 Financial Unit"):
        self.investigator = ForensicInvestigatorAgent()
        self.sar_drafter = SARDrafterAgent(filing_institution=filing_institution)
        self.auditor = ComplianceAuditorAgent()

    def process_alert(self, alert_entity_id: str,
                      risk_score: float,
                      conformal_tier: str,
                      in_edges: List[Dict[str, Any]],
                      out_edges: List[Dict[str, Any]],
                      extended_hops: Optional[List[Dict[str, Any]]] = None) -> InvestigationDossier:
        """
        Processes a single transaction / account alert through the multi-agent swarm.
        """
        # Step 1: Investigator Agent analyzes the localized graph topology
        evidence = self.investigator.investigate_subgraph(
            alert_entity_id=alert_entity_id,
            risk_score=risk_score,
            conformal_tier=conformal_tier,
            in_edges=in_edges,
            out_edges=out_edges,
            extended_hops=extended_hops
        )

        # Step 2: SAR Drafter Agent converts forensic evidence into formal regulatory report
        drafted_sar = self.sar_drafter.draft_sar(evidence=evidence)

        # Step 3: Compliance Auditor Agent validates statutory alignment and issues verdict
        audit_verdict = self.auditor.audit_sar(sar_document=drafted_sar)

        # Step 4: Assemble complete Dossier
        case_id = f"CASE-{alert_entity_id[:8].upper()}-{int(time.time())}"
        
        return InvestigationDossier(
            case_id=case_id,
            alert_entity_id=alert_entity_id,
            investigation_status=audit_verdict.verdict,
            forensic_evidence=evidence,
            drafted_sar=drafted_sar,
            audit_verdict=audit_verdict
        )

    def batch_process_alerts(self, alerts: List[Dict[str, Any]]) -> List[InvestigationDossier]:
        """
        Processes a batch of surveillance alerts in sequence.
        """
        dossiers = []
        for alert in alerts:
            d = self.process_alert(
                alert_entity_id=alert["alert_entity_id"],
                risk_score=alert["risk_score"],
                conformal_tier=alert.get("conformal_tier", "Tier 2: Manual Review"),
                in_edges=alert.get("in_edges", []),
                out_edges=alert.get("out_edges", []),
                extended_hops=alert.get("extended_hops", None)
            )
            dossiers.append(d)
        return dossiers


# Alias for backward compatibility
SwarmOrchestrator = AMLSwarmOrchestrator
