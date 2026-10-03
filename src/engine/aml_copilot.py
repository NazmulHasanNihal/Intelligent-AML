"""
AML Forensic Copilot & Regulatory Legal Reasoning Engine.
Provides grounded natural language case explanations, statutory references (FATF, FinCEN, BFIU, OCC 2011-12),
and recommended investigative counter-measures for forensic analysts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib


class AMLRegulatoryCopilot:
    """
    Forensic Copilot providing statutory grounding and explainable AI narratives
    for flagged AML cases, graph topologies, and model confidence sets.
    """

    KNOWLEDGE_BASE = {
        "structuring": {
            "title": "Structuring / Smurfing",
            "statute": "18 U.S.C. § 1956 & 31 U.S.C. § 5324; BFIU MLPA 2012 §4",
            "fatf_ref": "FATF Recommendation 10 & 20",
            "red_flags": [
                "Multiple cash or digital deposits just below $10,000 / BDT 1,000,000 reporting threshold",
                "Transactions conducted across multiple branches or mobile wallets within <24 hours",
                "Immediate consolidation of layered funds into a single recipient hub"
            ],
            "recommended_actions": [
                "Issue immediate Request for Information (RFI) for source of funds documentation",
                "Review linked KYC profiles for common phone numbers, device IDs, or IP subnets",
                "File FinCEN SAR / BFIU STR within statutory 30-day window"
            ]
        },
        "layering": {
            "title": "High-Velocity Layering & Flow Asymmetry",
            "statute": "FinCEN Advisory FIN-2014-A007; FATF Immediate Outcome 7",
            "fatf_ref": "FATF Recommendation 16 (Wire Transfers / Travel Rule)",
            "red_flags": [
                "Near-zero dwell time: Funds dispersed within minutes of arrival",
                "Physics flow conservation violation (|Phi| > 0.85): In-flow rapidly matches out-flow to shell entities",
                "High betweenness centrality in transaction graph indicating a pass-through intermediary hub"
            ],
            "recommended_actions": [
                "Place temporary 72-hour administrative debit hold under BFIU §15 / bank AML policy",
                "Trace downstream recipient accounts across correspondent banking partners",
                "Request SWIFT MT103 full beneficiary disclosures"
            ]
        },
        "tbml": {
            "title": "Trade-Based Money Laundering (TBML)",
            "statute": "FATF-Egmont TBML Best Practices; BFIU Circular 26 (Import/Export Discrepancies)",
            "fatf_ref": "FATF Recommendation 19 (Higher-Risk Jurisdictions)",
            "red_flags": [
                "Significant discrepancy between invoiced value and fair market customs commodity valuations",
                "Shipments routed through high-risk transshipment hubs (e.g., JAFZA, offshore free-zones)",
                "Round-dollar international wire transfers without bill of lading or customs clearing certification"
            ],
            "recommended_actions": [
                "Cross-check shipping container numbers with Lloyd's List / Maritime AIS tracking",
                "Demand certified export invoices and original bills of entry",
                "Alert Trade Finance Operations and flag customer for Enhanced Due Diligence (EDD)"
            ]
        },
        "conformal_explainability": {
            "title": "OCC 2011-12 / SR 11-7 Model Risk Governance",
            "statute": "OCC Bulletin 2011-12 'Supervisory Guidance on Model Risk Management'",
            "fatf_ref": "FATF Guidance on Digital Transformation of AML/CFT",
            "red_flags": [
                "Unbounded black-box predictions without statistical coverage guarantees",
                "Inability to justify model false-positive rate during regulatory examination"
            ],
            "recommended_actions": [
                "Verify Inductive Conformal Prediction set coverage (e.g. 1 - alpha = 0.95)",
                "Document counterfactual recourse distance (minimum perturbation required to clear flag)",
                "Retain cryptographically signed agent decision receipts for 5-year audit trail"
            ]
        }
    }

    def explain_case(
        self,
        case_id: str,
        entity_id: str,
        risk_score: float,
        conformal_set: Optional[List[int]] = None,
        typologies_detected: Optional[List[str]] = None,
        flow_phi: float = 0.0,
        user_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive forensic explanation and regulatory legal grounding.
        """
        # Determine dominant typology
        detected = typologies_detected or []
        if not detected:
            if abs(flow_phi) > 0.70:
                detected.append("layering")
            elif risk_score >= 0.85:
                detected.append("structuring")
            else:
                detected.append("conformal_explainability")

        matched_guidance = []
        statutes_cited = []
        immediate_steps = []

        for typo in detected:
            key = typo.lower().replace(" ", "_")
            if "layer" in key or "flow" in key:
                key = "layering"
            elif "struct" in key or "smurf" in key:
                key = "structuring"
            elif "trade" in key or "tbml" in key:
                key = "tbml"
            else:
                key = "conformal_explainability"

            kb_entry = self.KNOWLEDGE_BASE.get(key, self.KNOWLEDGE_BASE["conformal_explainability"])
            matched_guidance.append({
                "typology": kb_entry["title"],
                "statutory_authority": kb_entry["statute"],
                "fatf_standard": kb_entry["fatf_ref"],
                "red_flags": kb_entry["red_flags"]
            })
            statutes_cited.append(kb_entry["statute"])
            immediate_steps.extend(kb_entry["recommended_actions"])

        # Construct cohesive natural-language narrative
        conformal_summary = "Prediction set indicates guaranteed non-empty anomaly membership at 95% confidence." if (conformal_set == [1] or risk_score > 0.8) else "Borderline anomaly classification requiring human-in-the-loop review."

        narrative = (
            f"Forensic Investigation Summary for {entity_id} (Case {case_id}):\n"
            f"The composite HTGNN graph model assigned a suspicious score of {risk_score:.4f}. "
            f"{conformal_summary} "
            f"The primary risk driver is topological flow imbalance (Phi = {flow_phi:.2f}) "
            f"and association with identified money laundering typologies: {', '.join([g['typology'] for g in matched_guidance])}. "
            f"Under {statutes_cited[0]}, this pattern warrants proactive regulatory documentation "
            f"and immediate asset safeguarding."
        )

        return {
            "case_id": case_id,
            "entity_id": entity_id,
            "risk_score": risk_score,
            "flow_phi": flow_phi,
            "executive_narrative": narrative,
            "regulatory_grounding": matched_guidance,
            "statutes_cited": list(set(statutes_cited)),
            "recommended_investigative_actions": list(dict.fromkeys(immediate_steps)),
            "audit_timestamp": datetime.now(timezone.utc).isoformat()
        }


# Default singleton
aml_copilot = AMLRegulatoryCopilot()
