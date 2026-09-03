"""
src.agents — Autonomous Multi-Agent Forensic Investigation & Compliance Swarm.
"""

from .investigator_agent import ForensicInvestigatorAgent, ForensicEvidence, TransactionEdge
from .sar_drafter_agent import SARDrafterAgent
from .compliance_auditor_agent import ComplianceAuditorAgent, AuditVerdict
from .swarm_orchestrator import AMLSwarmOrchestrator, InvestigationDossier

__all__ = [
    "ForensicInvestigatorAgent",
    "ForensicEvidence",
    "TransactionEdge",
    "SARDrafterAgent",
    "ComplianceAuditorAgent",
    "AuditVerdict",
    "AMLSwarmOrchestrator",
    "InvestigationDossier"
]
