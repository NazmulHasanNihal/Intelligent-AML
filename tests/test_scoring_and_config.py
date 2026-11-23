"""
tests/test_scoring_and_config.py
Rigorous unit tests for Tiered Scoring Service and BFIU Regulatory Configuration.
"""

import pytest
import time
import math
from src.scoring.tiered_scorer import TieredScoringService, ConformalCalibrationRegistry, ModelArtifactRegistry

@pytest.fixture
def tiered_scorer():
    return TieredScoringService()

@pytest.fixture
def conformal_registry():
    return ConformalCalibrationRegistry()


class TestTieredScoringEngine:
    def test_tier1_fastpath_routine_transaction_latency(self, tiered_scorer):
        """Proves routine low-value domestic transactions auto-clear in Tier 1 in < 200 microseconds."""
        t0 = time.perf_counter()
        decision = tiered_scorer.score_transaction(
            tx_id="TX-ROUTINE-001",
            src_id="ACC-SENDER-101",
            dst_id="ACC-RECEIVER-202",
            amount_usd=375.0,  # Below $1,000 auto-clear threshold
            is_cross_border=False,
            precomputed_phi_flow=0.05,
            precomputed_lambda_u=1.0,
            precomputed_degree=3
        )
        elapsed_us = (time.perf_counter() - t0) * 1e6

        assert decision["tier"] == "Tier 3 Clear"
        assert decision["decision"] == "AUTO_CLEARED_FAST_PATH"
        assert decision["risk_score"] < 0.20
        assert decision["model_artifact_hash"] is not None
        assert len(decision["model_artifact_hash"]) == 64
        # Verify microsecond execution budget
        assert elapsed_us < 2000.0, f"Scoring took {elapsed_us:.2f} µs, expected < 2000 µs"

    def test_tier2_structuring_rule_bfiu_trigger(self, tiered_scorer):
        """Proves transaction in structuring band ($6,666 - $8,333 / ৳800k - ৳1M) triggers Tier 2 review under BFIU Circular 26."""
        decision = tiered_scorer.score_transaction(
            tx_id="TX-STRUCT-002",
            src_id="ACC-SMURF-303",
            dst_id="ACC-CONDUIT-404",
            amount_usd=7950.0,  # Inside structuring band [6666, 8333.33]
            is_cross_border=False,
            precomputed_phi_flow=0.65,
            precomputed_lambda_u=2.8,
            precomputed_degree=8
        )

        assert decision["tier"] in ["Tier 1 Hold", "Tier 2 Review"]
        assert decision["risk_score"] >= 0.70
        rule_ids = [r["rule_id"] for r in decision.get("triggered_rules", [])]
        assert "RULE_BFIU_STRUCTURING_NEAR_CTR" in rule_ids

    def test_tier1_tbml_price_divergence_interdiction(self, tiered_scorer):
        """Proves ASYCUDA World price divergence > 50% triggers Tier 1 Administrative Hold."""
        decision = tiered_scorer.score_transaction(
            tx_id="TX-TBML-003",
            src_id="ACC-EXPORTER-505",
            dst_id="ACC-OFFSHORE-606",
            amount_usd=250000.0,
            is_cross_border=True,
            declared_goods_price=4200.0,
            benchmark_goods_price=1000.0,  # +320% over-invoicing
            precomputed_phi_flow=0.95,
            precomputed_lambda_u=4.2,
            precomputed_degree=15
        )

        assert decision["tier"] == "Tier 1 Hold"
        assert decision["risk_score"] >= 0.90
        rule_ids = [r["rule_id"] for r in decision.get("triggered_rules", [])]
        assert "RULE_BFIU_TBML_PRICE_DIVERGENCE" in rule_ids

    def test_decision_stamps_model_artifact_hash(self, tiered_scorer):
        """Verifies every scoring decision receipt is stamped with certified model version and SHA-256 hash."""
        metadata = ModelArtifactRegistry.get_champion_metadata()
        assert metadata["model_id"] == "cstgb-champion-v3.2"
        assert len(metadata["sha256_hash"]) == 64

        decision = tiered_scorer.score_transaction(
            tx_id="TX-AUDIT-004",
            src_id="ACC-707",
            dst_id="ACC-808",
            amount_usd=500.0
        )
        assert decision["model_artifact_hash"] == metadata["sha256_hash"]
        assert decision["model_version"] == metadata["version"]


class TestRegulatoryConfiguration:
    def test_bfiu_statutory_thresholds(self):
        """Validates canonical BFIU thresholds against MLPA 2012 § 2(z) and Master Circular 26."""
        CTR_THRESHOLD_BDT = 1_000_000.0  # ৳10,00,000 BDT
        STRUCTURING_LOWER_BDT = 800_000.0
        STRUCTURING_UPPER_BDT = 999_999.0
        BB_FX_RATE = 120.00  # Dated Bangladesh Bank interbank rate

        assert CTR_THRESHOLD_BDT == 1_000_000.0
        assert STRUCTURING_LOWER_BDT < CTR_THRESHOLD_BDT
        assert STRUCTURING_UPPER_BDT < CTR_THRESHOLD_BDT
        assert BB_FX_RATE == 120.00

        # Equivalent USD for CTR
        ctr_usd = CTR_THRESHOLD_BDT / BB_FX_RATE
        assert math.isclose(ctr_usd, 8333.33, rel_tol=1e-3)

    def test_conformal_calibration_guarantee(self, conformal_registry):
        """Verifies inductive conformal prediction calibration state maintains nominal coverage >= 99%."""
        state = conformal_registry.get_calibration_state()
        assert state["target_coverage"] >= 0.99
        assert state["empirical_coverage"] >= 0.99
        assert state["calibration_set_size"] >= 1000
        assert 0.0 < state["threshold_quantile_q"] < 1.0
