"""
rule_engine.py — Deterministic Hard-Rule Guardrails & Hybrid Decision Gate.
Combines statutory banking compliance rules (OFAC/PEP, CTR Structuring, Rapid Velocity)
with soft C-STGB machine learning probabilities for zero-tolerance AML governance.
"""

import time
from typing import Dict, List, Tuple, Optional, Any, Set
import numpy as np


class HardRuleEngine:
    """
    Deterministic Compliance Rule Engine implementing FATF, FinCEN, and BSA statutory rules.
    Provides fast, pre-inference filtering and hybrid decision gating.
    """
    def __init__(self, structuring_threshold: float = 10_000.0,
                 structuring_window_hours: float = 24.0,
                 velocity_drain_seconds: float = 300.0):
        self.structuring_threshold = structuring_threshold
        self.structuring_window_seconds = structuring_window_hours * 3600.0
        self.velocity_drain_seconds = velocity_drain_seconds

        # In-memory sanction / watchlist database (OFAC SDN, PEP, Blacklisted Crypto Wallets)
        self.sanctioned_entities: Set[str] = {
            "OFAC_SDN_001", "OFAC_SDN_992", "TORNADO_CASH_ROUTER", "LAZARUS_GROUP_HOT",
            "DARKNET_HYDRA_GATEWAY", "BLOCKED_SANCTION_RUS_04", "PEP_HIGH_RISK_88"
        }
        self.high_risk_jurisdictions: Set[str] = {
            "PRK", "IRN", "MMR", "SYR", "CUB", "RUS_SANCTIONED_ZONE"
        }

    def add_sanctioned_entity(self, entity_id: str) -> None:
        """Dynamically registers a sanctioned identifier / wallet address."""
        self.sanctioned_entities.add(str(entity_id))

    def evaluate_rules(self, transaction: Dict[str, Any], 
                       recent_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Evaluates deterministic statutory rules on a transaction payload.
        Returns:
            triggered_rules: List of triggered rule descriptions.
            rule_risk_score: Deterministic risk score [0.0 to 1.0].
            is_blocked: Boolean indicating instant statutory block.
        """
        src_id = str(transaction.get("src_id", ""))
        dst_id = str(transaction.get("dst_id", ""))
        amount = float(transaction.get("amount", 0.0))
        jurisdiction = str(transaction.get("jurisdiction", "USA")).upper()
        timestamp = float(transaction.get("timestamp", time.time()))

        triggered = []
        rule_risk = 0.0
        is_blocked = False

        # RULE 1: OFAC / Sanctioned Entity Screening (Statutory Block)
        if src_id in self.sanctioned_entities or dst_id in self.sanctioned_entities:
            triggered.append({
                "rule_id": "RULE_OFAC_001",
                "name": "OFAC Sanctions List Direct Match",
                "severity": "CRITICAL",
                "action": "INSTANT_BLOCK_AND_SEIZE",
                "risk_contribution": 1.0
            })
            rule_risk = 1.0
            is_blocked = True

        # RULE 2: High-Risk Sanctioned Jurisdiction Route
        if jurisdiction in self.high_risk_jurisdictions:
            triggered.append({
                "rule_id": "RULE_FATF_JURISDICTION",
                "name": "FATF Blacklisted Jurisdiction Transfer",
                "severity": "HIGH",
                "action": "MANDATORY_SAR_FILING",
                "risk_contribution": 0.95
            })
            rule_risk = max(rule_risk, 0.95)

        # RULE 3: Currency Transaction Report (CTR) Structuring / Smurfing Detection
        # Detecting transactions just below the $10,000 threshold ($8,500 - $9,999)
        if 8_500.0 <= amount < self.structuring_threshold:
            triggered.append({
                "rule_id": "RULE_BSA_STRUCTURING_SINGLE",
                "name": "Sub-Threshold Structuring Flag (Single $8.5k-$10k Transfer)",
                "severity": "MEDIUM",
                "action": "ENHANCED_SURVEILLANCE",
                "risk_contribution": 0.65
            })
            rule_risk = max(rule_risk, 0.65)

        # RULE 4: Multi-Transaction Structuring Aggregate Rule
        if recent_history:
            recent_sub_threshold = [
                tx for tx in recent_history 
                if (timestamp - float(tx.get("timestamp", timestamp))) <= self.structuring_window_seconds
                and 5_000.0 <= float(tx.get("amount", 0.0)) < self.structuring_threshold
            ]
            if len(recent_sub_threshold) >= 2:
                total_structured_vol = sum(float(tx.get("amount", 0.0)) for tx in recent_sub_threshold) + amount
                triggered.append({
                    "rule_id": "RULE_BSA_SMURFING_BURST",
                    "name": f"Repeated Smurfing Aggregation ({len(recent_sub_threshold)+1} txs totaling ${total_structured_vol:,.2f})",
                    "severity": "HIGH",
                    "action": "TRIGGER_FORM_111_SAR",
                    "risk_contribution": 0.90
                })
                rule_risk = max(rule_risk, 0.90)

            # RULE 5: Rapid Inflow-Outflow Velocity Drain (Money Mule Pass-Through)
            inflows = [
                tx for tx in recent_history 
                if str(tx.get("dst_id")) == src_id and (timestamp - float(tx.get("timestamp", timestamp))) <= self.velocity_drain_seconds
            ]
            if inflows:
                inflow_val = sum(float(tx.get("amount", 0.0)) for tx in inflows)
                if inflow_val > 0 and (amount / inflow_val) >= 0.85:
                    triggered.append({
                        "rule_id": "RULE_RAPID_DRAIN_VELOCITY",
                        "name": f"Rapid Mule Liquidation ({amount/inflow_val:.1%} drained within {self.velocity_drain_seconds}s)",
                        "severity": "HIGH",
                        "action": "ADMINISTRATIVE_HOLD",
                        "risk_contribution": 0.85
                    })
                    rule_risk = max(rule_risk, 0.85)

        return {
            "triggered_rules": triggered,
            "rule_risk_score": rule_risk,
            "is_blocked": is_blocked,
            "rule_count": len(triggered)
        }


class HybridDecisionGate:
    """
    Hybrid Decision Gate fusing Deterministic Rules with C-STGB Spatiotemporal AI.
    Guarantees that statutory redlines are never bypassed by AI probabilities.
    """
    def __init__(self, rule_engine: Optional[HardRuleEngine] = None, 
                 alert_threshold: float = 0.50):
        self.rule_engine = rule_engine or HardRuleEngine()
        self.alert_threshold = float(alert_threshold)

    def evaluate_hybrid(self, transaction: Dict[str, Any], ai_risk_score: float,
                        conformal_prediction_set: Optional[int] = None,
                        recent_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Executes hybrid arbitration between deterministic rules and C-STGB.
        Returns unified triage package with regulatory compliance audit tags.
        """
        rule_eval = self.rule_engine.evaluate_rules(transaction, recent_history)
        rule_risk = rule_eval["rule_risk_score"]
        is_blocked = rule_eval["is_blocked"]

        # Unified Arbitration: Statutory overrides take precedence; otherwise maximum risk bound
        if is_blocked:
            final_risk = 1.0
            triage_action = "CRITICAL_STATUTORY_BLOCK"
        elif rule_risk > 0.80:
            final_risk = max(rule_risk, float(ai_risk_score))
            triage_action = "MANDATORY_REGULATORY_SAR"
        elif float(ai_risk_score) >= self.alert_threshold:
            final_risk = float(ai_risk_score)
            triage_action = "ESCALATE_TO_COMPLIANCE_INVESTIGATION"
        elif conformal_prediction_set == 2:  # Conformal uncertain set {0, 1}
            final_risk = max(rule_risk, float(ai_risk_score))
            triage_action = "SECONDARY_HUMAN_REVIEW_QUEUE"
        else:
            final_risk = max(rule_risk, float(ai_risk_score))
            triage_action = "AUTO_CLEARED_PASS"

        return {
            "final_risk_score": round(final_risk, 4),
            "ai_risk_score": round(float(ai_risk_score), 4),
            "rule_risk_score": round(rule_risk, 4),
            "triage_action": triage_action,
            "is_blocked": is_blocked,
            "conformal_status": "CONFIDENT_FRAUD" if conformal_prediction_set == 1 else (
                "CONFIDENT_LICIT" if conformal_prediction_set == 0 else "UNCERTAIN_REVIEW"
            ),
            "triggered_rules": rule_eval["triggered_rules"]
        }
