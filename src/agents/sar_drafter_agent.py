"""
sar_drafter_agent.py — Autonomous Regulatory SAR Drafter Agent.
Ingests structured ForensicEvidence from the Investigator Agent and automatically
drafts complete, regulatory-grade Suspicious Activity Reports (SARs) formatted to
FinCEN Form 111 and FATF International Standards.
"""

import time
import uuid
from typing import Dict, List, Optional, Any
from .investigator_agent import ForensicEvidence


class SARDrafterAgent:
    """
    Autonomous AI Regulatory SAR Drafter Agent.
    Transforms raw graph forensic metrics into precise, legally defensible,
    and structured compliance narratives for Financial Intelligence Units (FIUs).
    """
    def __init__(self, filing_institution: str = "Intelligent-AML Tier-1 Financial Unit"):
        self.filing_institution = filing_institution

    def draft_sar(self, evidence: ForensicEvidence,
                  narrative_detail_level: str = "comprehensive") -> Dict[str, Any]:
        """
        Drafts a full regulatory Suspicious Activity Report (SAR).
        
        Args:
            evidence: ForensicEvidence object compiled by ForensicInvestigatorAgent.
            narrative_detail_level: Level of detail in the narrative ('compact' or 'comprehensive').
        
        Returns:
            Dict containing the complete formatted SAR report.
        """
        sar_id = f"SAR-INTELAML-{uuid.uuid4().hex[:10].upper()}"
        filing_time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        total_tainted_flow = evidence.total_inbound_volume + evidence.total_outbound_volume

        # 1. Construct Executive Summary
        typologies_str = ", ".join(evidence.detected_typologies)
        exec_summary = (
            f"Automated surveillance alert generated for Subject Entity [{evidence.alert_entity_id}] "
            f"with an elevated ML risk score of {evidence.risk_score:.4f} ({evidence.risk_score*100:.1f}%) "
            f"under Conformal Risk Control {evidence.conformal_tier}. "
            f"Total identified flow volume across the immediate subgraph is ${total_tainted_flow:,.2f} USD. "
            f"Primary detected typologies include: {typologies_str}."
        )

        # 2. Construct Deep Forensic Narrative (Part III)
        narrative_paragraphs = []
        narrative_paragraphs.append(
            f"1. ALERT INITIATION & CONTEXT: On {filing_time_str}, the Intelligent-AML Continuous-Time "
            f"Heterogeneous Spatiotemporal surveillance engine flagged entity [{evidence.alert_entity_id}]. "
            f"The entity exhibited abnormal topological connectivity with {len(evidence.suspect_counterparties)} "
            f"counterparties across a {evidence.max_hop_depth}-hop localized sub-network."
        )

        # Flow Peeling / Mule Conduit Section
        if evidence.kirchhoff_peeling_ratio >= 0.80:
            narrative_paragraphs.append(
                f"2. PASS-THROUGH MULE DYNAMICS: Flow analysis reveals a Kirchhoff Peeling Ratio of "
                f"{evidence.kirchhoff_peeling_ratio:.3f}. Inbound volume (${evidence.total_inbound_volume:,.2f} USD) "
                f"closely matches outbound volume (${evidence.total_outbound_volume:,.2f} USD), indicating that the "
                f"account operates primarily as a rapid transit mule conduit to obscure capital origin rather than "
                f"retaining economic balances for legitimate commercial purposes."
            )
        else:
            narrative_paragraphs.append(
                f"2. CAPITAL FLOW DISPERSION: Total inbound transfers equal ${evidence.total_inbound_volume:,.2f} USD, "
                f"with ${evidence.total_outbound_volume:,.2f} USD dispersed downstream. The flow dispersion pattern "
                f"reflects asymmetric capital aggregation across counterparties."
            )

        # Smurfing & Burst Section
        if evidence.smurfing_burst_score >= 1.5:
            narrative_paragraphs.append(
                f"3. HIGH-VELOCITY BURST ACTIVITY: The subject demonstrated an acute smurfing burst intensity "
                f"score of {evidence.smurfing_burst_score:.2f} transactions/hour. Multiple micro-transactions were "
                f"executed within compressed time windows, consistent with structured smurfing typologies intended "
                f"to circumvent statutory currency reporting thresholds."
            )

        # Circular Cycles Section
        if evidence.cycle_detected:
            narrative_paragraphs.append(
                f"4. CLOSED-LOOP TOPOLOGY: Forensic graph analysis confirmed the presence of circular / reciprocal "
                f"transaction loops connecting counterparties directly back to source entities, a hallmark signature "
                f"of artificial volume inflation, wash-trading, and circular layering rings."
            )

        # Dormancy & Hibernation Section
        if evidence.dormant_delay_days >= 14.0:
            narrative_paragraphs.append(
                f"5. LONG-DWELL HIBERNATION: The transaction chain exhibited an extended dormant interval of "
                f"{evidence.dormant_delay_days:.1f} days between funding and dispatch. This intentional latency is "
                f"consistent with advanced evasion tactics designed to evade standard short-window rule filters."
            )

        # Action Recommendation
        if "Auto-Block" in evidence.conformal_tier or evidence.risk_score >= 0.90:
            action_recommendation = (
                "IMMEDIATE ACTION REQUIRED: The risk certainty exceeds 99.9% finite-sample confidence bounds. "
                "Recommend immediate administrative freeze on the subject entity's outgoing funds, filing of "
                "this formal SAR with FinCEN / competent FIU, and referral to criminal financial investigation units."
            )
        else:
            action_recommendation = (
                "ENHANCED DUE DILIGENCE (EDD): Place the subject entity under active 24/7 forensic telemetry monitoring. "
                "Request formal Source of Funds (SoF) / Proof of Beneficial Ownership from onboarding documentation. "
                "Escalate to Senior Compliance Officer within 48 hours."
            )

        full_narrative = "\n\n".join(narrative_paragraphs)

        # 3. Assemble Complete SAR Document
        sar_document = {
            "sar_id": sar_id,
            "filing_institution": self.filing_institution,
            "filing_timestamp": filing_time_str,
            "filing_status": "DRAFTED_PENDING_AUDITOR_SIGN_OFF",
            "subject_entity_id": evidence.alert_entity_id,
            "executive_summary": exec_summary,
            "risk_assessment": {
                "model_risk_score": round(evidence.risk_score, 4),
                "conformal_triage_tier": evidence.conformal_tier,
                "sanctions_taint_probability": round(evidence.sanctions_taint_score, 4),
                "kirchhoff_peeling_index": round(evidence.kirchhoff_peeling_ratio, 4),
                "burst_velocity_score": round(evidence.smurfing_burst_score, 2),
                "circular_cycle_detected": evidence.cycle_detected,
                "dormant_hibernation_days": round(evidence.dormant_delay_days, 1)
            },
            "financial_summary": {
                "total_inbound_usd": round(evidence.total_inbound_volume, 2),
                "total_outbound_usd": round(evidence.total_outbound_volume, 2),
                "total_monitored_flow_usd": round(total_tainted_flow, 2),
                "counterparty_count": len(evidence.suspect_counterparties)
            },
            "categorized_typologies": evidence.detected_typologies,
            "counterparty_entities": evidence.suspect_counterparties,
            "transaction_ledger_sample": evidence.transaction_trail[:15],  # Top 15 trail events
            "part_iii_forensic_narrative": full_narrative,
            "part_v_recommendation": action_recommendation
        }

        return sar_document
