"""
tests/test_screening_engine.py — Unit & Integration Tests for Screening Fidelity
Tests:
1. Normalization: diacritics, case-folding, legal suffixes, Bangla-to-Latin transliterations.
2. Algorithms: Jaro-Winkler, Token-Set ratio, Soundex phonetic.
3. Attribute corroboration: DOB, country, national ID / passport.
4. Official Watchlist Registry metadata and entity search.
"""

import pytest
from src.screening.normalizer import (
    strip_diacritics,
    strip_legal_suffixes,
    standardize_bangla_transliteration,
    normalize_entity_name,
    get_name_order_permutations,
)
from src.screening.matcher import (
    jaro_similarity,
    jaro_winkler_similarity,
    token_set_similarity,
    soundex,
    phonetic_similarity,
    compute_screening_score,
    ScreeningThresholdConfig,
)
from src.screening.watchlist_registry import watchlist_registry


def test_strip_diacritics():
    """Diacritics and non-spacing marks must be normalized to ASCII equivalents."""
    assert strip_diacritics("Müller") == "Muller"
    assert strip_diacritics("François") == "Francois"
    assert strip_diacritics("Łódź") == "Lodz"
    assert strip_diacritics("São Paulo") == "Sao Paulo"
    assert strip_diacritics("Željko") == "Zeljko"


def test_strip_legal_suffixes():
    """Corporate entity suffixes across international & offshore jurisdictions must be removed."""
    tokens1 = ["gulf", "star", "commodities", "fze"]
    assert strip_legal_suffixes(tokens1) == ["gulf", "star", "commodities"]

    tokens2 = ["helvetia", "metallurgical", "trading", "ag"]
    assert strip_legal_suffixes(tokens2) == ["helvetia", "metallurgical"]

    tokens3 = ["caspian", "petroleum", "freight", "services", "ltd"]
    assert strip_legal_suffixes(tokens3) == ["caspian", "petroleum", "freight"]

    tokens4 = ["singapore", "industrial", "pte", "ltd"]
    assert strip_legal_suffixes(tokens4) == ["singapore", "industrial"]


def test_standardize_bangla_transliteration():
    """Common Bangla-to-Latin phonetic transliteration variants must standardize to canonical forms."""
    assert standardize_bangla_transliteration("md. farhan ahmed") == "mohammed farhan ahmed"
    assert standardize_bangla_transliteration("seikh rohman") == "sheikh rahman"
    assert standardize_bangla_transliteration("choudhury kahn") == "chowdhury khan"
    assert standardize_bangla_transliteration("hussain haque") == "hossain haq"


def test_name_order_permutations():
    """Last, First vs First Last permutations must generate canonical representations."""
    perms = get_name_order_permutations("Hasan, Nazmul")
    assert "nazmul hassan" in perms or "hassan nazmul" in perms or "hasan nazmul" in perms


def test_jaro_winkler_similarity():
    """Jaro-Winkler must score identical strings 1.0 and similar strings proportionally."""
    assert jaro_winkler_similarity("GULF STAR", "GULF STAR") == 1.0
    assert jaro_winkler_similarity("", "SOMETHING") == 0.0

    sim = jaro_winkler_similarity("GULF STAR COMMODITIES", "GULF STAR TRADING")
    assert 0.70 < sim < 0.95


def test_token_set_similarity_permutation_invariance():
    """Token-set ratio must be invariant to word order permutations and extraneous tokens."""
    s1 = "Farhan Ahmed Kazi"
    s2 = "Kazi Farhan Ahmed"
    score = token_set_similarity(s1, s2)
    assert score >= 0.95


def test_soundex_phonetic_matching():
    """Soundex must map phonetically equivalent names to the same code."""
    # Sheikh vs Seikh
    assert soundex("Sheikh") == soundex("Seikh")
    # Khan vs Kahn
    assert soundex("Khan") == soundex("Kahn")
    # Smith vs Smyth
    assert soundex("Smith") == soundex("Smyth")


def test_screening_score_with_dob_and_country_corroboration():
    """Corroborating DOB and Country must appropriately adjust match scores."""
    # Base match without corroboration
    res_base = compute_screening_score(
        query_name="Mohammed Farooq Sheikh",
        target_name="Sheikh Mohammed Faruk"
    )
    assert res_base.match_score >= 80.0

    # Match with matching DOB and Country -> score boost
    res_boosted = compute_screening_score(
        query_name="Mohammed Farooq Sheikh",
        target_name="Sheikh Mohammed Faruk",
        query_dob="1974-06-15",
        target_dob="1974-06-15",
        query_country="Pakistan",
        target_country="Pakistan"
    )
    assert res_boosted.match_score > res_base.match_score
    assert res_boosted.corroboration_score > 0
    assert res_boosted.corroboration_details["dob_status"] == "EXACT_MATCH"
    assert res_boosted.corroboration_details["country_status"] == "MATCH"

    # Match with mismatched DOB -> score penalty
    res_penalized = compute_screening_score(
        query_name="Mohammed Farooq Sheikh",
        target_name="Sheikh Mohammed Faruk",
        query_dob="1995-12-01",
        target_dob="1974-06-15"
    )
    assert res_penalized.match_score < res_base.match_score
    assert res_penalized.corroboration_details["dob_status"] == "MISMATCH_PENALTY"


def test_official_watchlist_registry_metadata():
    """Watchlist Registry must contain all 5 required official lists with valid hashes and versions."""
    feeds = watchlist_registry.get_feeds()
    feed_ids = {f["list_id"] for f in feeds}
    expected = {"OFAC_SDN", "UN_CONSOLIDATED", "EU_CONSOLIDATED", "UK_HMT", "BFIU_DOMESTIC"}
    assert expected.issubset(feed_ids)

    for f in feeds:
        assert f["version"] != ""
        assert len(f["sha256_hash"]) == 64
        assert f["fetch_timestamp"].endswith("Z")
        assert f["total_records"] > 0
        assert f["status"] == "SYNCED_VERIFIED"


def test_watchlist_registry_candidate_screening():
    """Screening an ad-hoc entity against the registry must yield high-confidence true hit."""
    hits = watchlist_registry.screen_candidate("Gulf Star Commodities FZE")
    assert len(hits) > 0
    top_hit = hits[0]
    assert top_hit["entity_id"] == "OFAC-SDN-19482"
    assert top_hit["match_score"] >= 85.0
    assert top_hit["disposition"] == "CONFIRMED_TRUE_HIT"
    assert "algorithm_breakdown" in top_hit
    assert "token_diffs" in top_hit
