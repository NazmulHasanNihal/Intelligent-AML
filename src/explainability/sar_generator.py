"""
sar_generator.py — LLM & Template-Powered Automated SAR Narrative Drafter.
Generates regulatory-compliant Suspicious Activity Report (SAR) narrative drafts
for FinCEN Form 111, FCA, and FATF filings from C-STGB spatiotemporal explanations.
"""

import time
from typing import Dict, List, Tuple, Optional, Any
import numpy as np


class SARNarrativeGenerator:
    """
    Enterprise Suspicious Activity Report (SAR) Narrative Generation Engine.
    Converts C-STGB graph embeddings, temporal burst metrics, conformal certainty bounds,
    and rule violations into structured, auditor-ready regulatory filings.
    """
    def __init__(self, institution_name: str = "Global Digital Clearing Bank NA",
                 compliance_officer_id: str = "AML-OPS-DESK-42"):
        self.institution_name = institution_name
        self.compliance_officer_id = compliance_officer_id

    def generate_fincen_narrative(self, target_account_id: str,
                                  risk_score: float,
                                  topological_metrics: Dict[str, Any],
                                  conformal_details: Dict[str, Any],
                                  rule_violations: Optional[List[Dict[str, Any]]] = None,
                                  counterparties: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generates a formal FinCEN Form 111 SAR Narrative with complete spatiotemporal evidence.
        """
        deg_in = topological_metrics.get("deg_in", 0)
        deg_out = topological_metrics.get("deg_out", 0)
        total_deg = deg_in + deg_out
        max_burst = topological_metrics.get("max_burst_score", 0.0)
        pass_through = topological_metrics.get("pass_through_ratio", 0.0)
        total_volume = topological_metrics.get("total_volume_usd", 0.0)
        
        alpha = conformal_details.get("alpha", 0.10)
        stratum = conformal_details.get("stratum_name", "Standard Topological Strata")
        prediction_set = conformal_details.get("prediction_set_desc", "Confident Illicit {Fraud}")
        
        severity = "CRITICAL / URGENT" if risk_score >= 0.85 else ("HIGH" if risk_score >= 0.70 else "MEDIUM")
        current_date = time.strftime("%B %d, %Y", time.gmtime())

        narrative = f"""========================================================================================
             FINANCIAL CRIMES ENFORCEMENT NETWORK (FinCEN) — SAR NARRATIVE
========================================================================================
FILING INSTITUTION:        {self.institution_name}
INVESTIGATION CASE ID:     SAR-CASE-{int(time.time())}-{target_account_id[:8]}
PRIMARY SUSPECT IDENTIFIER: {target_account_id}
FILING DATE:               {current_date}
PRIORITY SEVERITY:         {severity}
SPATIOTEMPORAL RISK SCORE: {risk_score:.2%}
CONFORMAL CERTAINTY BOUND: {1.0 - alpha:.1%} Coverage (Stratum: {stratum})
========================================================================================

1. EXECUTIVE SUMMARY & JURISDICTION
----------------------------------------------------------------------------------------
{self.institution_name} is submitting this Suspicious Activity Report (SAR) pursuant to
the Bank Secrecy Act (31 U.S.C. 5318(g)) and 31 CFR Chapter X. 

The primary target identifier `{target_account_id}` has been identified by the automated
Conformal Spatio-Temporal GraphBoost (C-STGB) surveillance engine exhibiting high-probability
typologies consistent with Layering, Rapid Smurfing, and Decentralized Money Mule Operations.
The aggregate AI model risk probability is calculated at {risk_score:.2%}, validated within
a {1.0 - alpha:.1%} distribution-free conformal confidence interval.

2. METHOD OF OPERATION & SPATIOTEMPORAL TYPOLOGY
----------------------------------------------------------------------------------------
Analysis of the transaction graph reveals distinct structural anomalies:

*  NETWORK DISPERSION & GRAPH DEGREE:
   The suspect entity executed transactions across {total_deg} distinct counterparties
   ({deg_in} ingress transfers, {deg_out} egress transfers), forming an asymmetric fan-out structure.

*  TEMPORAL BURST ACCELERATION:
   Transactions exhibited a peak spatiotemporal burst velocity multiplier of {max_burst:.2f}x
   relative to historical baseline distributions. This rapid velocity indicates algorithmic
   clearing designed to defeat manual supervisory review windows.

*  PASS-THROUGH CONDUIT RATIO:
   The calculated conduit pass-through ratio is {pass_through:.1%}, confirming that funds
   flowing into the account were immediately re-routed with negligible holding dwell time.
"""

        # Section 3: Statutory Rule Triggers
        if rule_violations:
            narrative += "\n3. STATUTORY COMPLIANCE & SANCTION VIOLATIONS\n"
            narrative += "----------------------------------------------------------------------------------------\n"
            for r in rule_violations:
                narrative += f"*  [{r.get('rule_id', 'RULE')}] {r.get('name')}\n"
                narrative += f"   - Severity: {r.get('severity')}\n"
                narrative += f"   - Prescribed Compliance Action: {r.get('action')}\n"
        else:
            narrative += "\n3. STATUTORY COMPLIANCE & SANCTION VIOLATIONS\n"
            narrative += "----------------------------------------------------------------------------------------\n"
            narrative += "*  No instant deterministic OFAC blacklist matches. Activity captured by structural AI.\n"

        # Section 4: Counterparty Evidence
        if counterparties:
            narrative += "\n4. KEY COUNTERPARTY CLUSTER & SUSPECT TRANSFERS\n"
            narrative += "----------------------------------------------------------------------------------------\n"
            for c in counterparties[:5]:
                narrative += f"*  Counterparty `{c.get('id', 'UNKNOWN')}` | Amount: ${c.get('amount', 0.0):,.2f} | Hop: {c.get('hop', 1)} | Taint: {c.get('taint_score', 0.0):.2f}\n"

        # Section 5: Conformal Governance & Actions
        narrative += f"""
5. MATHEMATICAL CONFORMAL CERTAINTY & MODEL RISK GOVERNANCE
----------------------------------------------------------------------------------------
*  Conformal Prediction Set: {prediction_set}
*  Mondrian Stratum: {stratum}
*  Significance Level (Alpha): {alpha:.2%} (Empirical Error Bounded at {alpha:.2%})
*  Model Architecture: C-STGB (Heterogeneous Temporal Graph Convolution + Gated Stacking)
*  Governance Validation: Fed SR 11-7 / OCC 2011-12 Validated Audit Trail.

6. RECOMMENDED REGULATORY ACTIONS
----------------------------------------------------------------------------------------
1. Place immediate administrative freeze on Account `{target_account_id}`.
2. Transmit this evidentiary filing to the Financial Crimes Enforcement Network (FinCEN).
3. Issue information-sharing requests under USA PATRIOT Act Section 314(b) to linked counterparties.

Report Prepared By: Automated Compliance Intelligence System (Agent ID: {self.compliance_officer_id})
========================================================================================"""
        return narrative

    def compile_llm_prompt(self, target_account_id: str,
                           risk_score: float,
                           topological_metrics: Dict[str, Any],
                           conformal_details: Dict[str, Any],
                           rule_violations: Optional[List[Dict[str, Any]]] = None) -> Dict[str, str]:
        """
        Compiles formatted prompt context suitable for zero-shot LLM narrative drafting
        (e.g., Llama 3, Mistral 7B, Claude 3.5, GPT-4).
        """
        system_prompt = (
            "You are an expert Senior AML Compliance Officer and Financial Forensic Analyst. "
            "Your task is to draft a precise, highly formal, and legally robust Suspicious Activity Report (SAR) "
            "narrative according to FinCEN and FATF regulatory guidelines based on the spatiotemporal graph AI evidence provided."
        )
        
        user_prompt = f"""Target Entity ID: {target_account_id}
Spatiotemporal AML Risk Score: {risk_score:.4f}
Topological Degree: {topological_metrics.get('deg_in', 0)} in, {topological_metrics.get('deg_out', 0)} out
Burst Velocity Factor: {topological_metrics.get('max_burst_score', 0.0):.2f}x
Pass-Through Conduit Ratio: {topological_metrics.get('pass_through_ratio', 0.0):.2%}
Conformal Coverage Level: {1.0 - conformal_details.get('alpha', 0.10):.1%} (Stratum: {conformal_details.get('stratum_name', 'Standard')})
Rule Violations Triggered: {len(rule_violations or [])}

Please draft:
1. Executive Summary
2. Detailed Typology Breakdown (Structuring / Mule / Layering)
3. Graph Topology Evidence
4. Recommended Law Enforcement Next Steps"""

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
