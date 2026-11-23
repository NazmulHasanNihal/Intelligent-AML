"""
src/screening/matcher.py — Multi-Algorithm Screening & Entity Resolution Engine
Implements:
1. Jaro-Winkler string similarity with prefix weighting.
2. Token-Set Ratio (set intersection/union with permutation tolerance).
3. Soundex phonetic encoding and similarity.
4. Attribute corroboration (DOB, Country, National ID/TIN).
5. Configurable thresholds and detailed per-algorithm score breakdown.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from src.screening.normalizer import normalize_entity_name, get_token_bag, get_name_order_permutations


@dataclass
class ScreeningThresholdConfig:
    auto_freeze_threshold: float = 85.0     # >= 85% -> CONFIRMED_TRUE_HIT
    quarantine_threshold: float = 65.0      # >= 65% and < 85% -> PENDING_REVIEW
    weight_jaro_winkler: float = 0.40       # 40% weight
    weight_token_set: float = 0.40          # 40% weight
    weight_phonetic: float = 0.20           # 20% weight
    dob_match_bonus: float = 10.0           # +10% if DOB matches exactly
    dob_mismatch_penalty: float = 15.0      # -15% if DOBs are known and differ
    country_match_bonus: float = 5.0        # +5% if country/domicile matches
    identifier_match_bonus: float = 25.0    # +25% if passport/national ID matches exactly


DEFAULT_THRESHOLDS = ScreeningThresholdConfig()


def jaro_similarity(s1: str, s2: str) -> float:
    """Computes standard Jaro distance between two strings."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    transpositions //= 2
    return (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0


def jaro_winkler_similarity(s1: str, s2: str, prefix_weight: float = 0.1, max_prefix: int = 4) -> float:
    """
    Computes Jaro-Winkler similarity, boosting the score for strings
    that share a common prefix of up to max_prefix characters.
    Returns float in range [0.0, 1.0].
    """
    j_sim = jaro_similarity(s1, s2)
    if j_sim < 0.7:
        return j_sim

    prefix_len = 0
    for c1, c2 in zip(s1[:max_prefix], s2[:max_prefix]):
        if c1 == c2:
            prefix_len += 1
        else:
            break

    return j_sim + prefix_len * prefix_weight * (1.0 - j_sim)


def token_set_similarity(s1: str, s2: str) -> float:
    """
    Computes Token-Set similarity ratio.
    Finds common tokens and remainder tokens in both strings,
    measuring Jaro-Winkler across sorted combinations.
    Handles word order permutations and extraneous words (e.g., 'Al-Mansoor Trading' vs 'Trading Al-Mansoor LLC').
    """
    tokens1 = set(get_token_bag(s1))
    tokens2 = set(get_token_bag(s2))

    if not tokens1 or not tokens2:
        return 0.0
    if tokens1 == tokens2:
        return 1.0

    intersection = tokens1.intersection(tokens2)
    diff1 = tokens1 - intersection
    diff2 = tokens2 - intersection

    sorted_intersect = " ".join(sorted(intersection))
    sorted_diff1 = " ".join(sorted(diff1))
    sorted_diff2 = " ".join(sorted(diff2))

    comb1 = (sorted_intersect + " " + sorted_diff1).strip()
    comb2 = (sorted_intersect + " " + sorted_diff2).strip()

    scores = [
        jaro_winkler_similarity(sorted_intersect, comb1) if sorted_intersect else 0.0,
        jaro_winkler_similarity(sorted_intersect, comb2) if sorted_intersect else 0.0,
        jaro_winkler_similarity(comb1, comb2)
    ]
    return max(scores)


def soundex(text: str) -> str:
    """
    Computes classic American Soundex code for phonetic matching.
    Output: Letter + 3 digits (e.g. 'R550').
    """
    if not text:
        return "Z000"

    cleaned = "".join(c.upper() for c in text if c.isalpha())
    if not cleaned:
        return "Z000"

    mapping = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6"
    }

    first_char = cleaned[0]
    encoded = [first_char]

    prev_code = mapping.get(first_char, "")
    for char in cleaned[1:]:
        code = mapping.get(char, "")
        if code:
            if code != prev_code:
                encoded.append(code)
            prev_code = code
        else:
            prev_code = ""

    soundex_code = "".join(encoded)[:4]
    return soundex_code.ljust(4, "0")


def phonetic_similarity(s1: str, s2: str) -> float:
    """
    Computes phonetic similarity between two strings by comparing
    Soundex codes across their constituent tokens.
    """
    t1 = get_token_bag(s1)
    t2 = get_token_bag(s2)

    if not t1 or not t2:
        return 0.0

    soundex1 = [soundex(t) for t in t1]
    soundex2 = [soundex(t) for t in t2]

    # Exact phonetic matches
    matched = sum(1 for sx in soundex1 if sx in soundex2)
    max_tokens = max(len(soundex1), len(soundex2))

    return matched / max_tokens if max_tokens > 0 else 0.0


@dataclass
class MatchResult:
    match_score: float
    jaro_winkler_score: float
    token_set_score: float
    phonetic_score: float
    corroboration_score: float
    corroboration_details: Dict[str, Any]
    match_type: str
    disposition: str
    token_diffs: Dict[str, List[str]]
    screened_name: str
    matched_entity: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_score": round(self.match_score, 1),
            "algorithm_breakdown": {
                "jaro_winkler_score": round(self.jaro_winkler_score, 1),
                "token_set_score": round(self.token_set_score, 1),
                "phonetic_score": round(self.phonetic_score, 1),
                "corroboration_adjustment": round(self.corroboration_score, 1)
            },
            "corroboration_details": self.corroboration_details,
            "match_type": self.match_type,
            "disposition": self.disposition,
            "token_diffs": self.token_diffs,
            "screened_name": self.screened_name,
            "matched_entity": self.matched_entity
        }


def compute_screening_score(
    query_name: str,
    target_name: str,
    query_dob: Optional[str] = None,
    target_dob: Optional[str] = None,
    query_country: Optional[str] = None,
    target_country: Optional[str] = None,
    query_id: Optional[str] = None,
    target_id: Optional[str] = None,
    config: Optional[ScreeningThresholdConfig] = None
) -> MatchResult:
    """
    Computes comprehensive multi-algorithm match score with attribute corroboration:
    1. Normalizes both names (stripping legal suffixes, diacritics, and transliteration noise).
    2. Runs Jaro-Winkler, Token-Set, and Phonetic Soundex algorithms.
    3. Evaluates corroborating metadata (DOB, Country/Domicile, National ID / Tax ID).
    4. Calculates final composite score bounded [0.0, 100.0].
    5. Determines operational disposition (CONFIRMED_TRUE_HIT, PENDING_REVIEW, DISMISSED_FALSE_POSITIVE).
    """
    cfg = config or DEFAULT_THRESHOLDS

    norm_query = normalize_entity_name(query_name)
    norm_target = normalize_entity_name(target_name)

    # 1. Exact match check
    if norm_query == norm_target and norm_query != "":
        jw_score = 100.0
        token_score = 100.0
        phonetic_score = 100.0
        match_type = "EXACT_NAME_MATCH"
    else:
        # Check permutations (e.g. Last First vs First Last)
        query_perms = get_name_order_permutations(query_name)
        target_perms = get_name_order_permutations(target_name)

        is_word_reversal = False
        for qp in query_perms:
            if qp in target_perms and qp != "":
                is_word_reversal = True
                break

        # Compute Jaro-Winkler
        jw_raw = jaro_winkler_similarity(norm_query, norm_target)
        jw_score = jw_raw * 100.0

        # Compute Token-Set
        token_raw = token_set_similarity(query_name, target_name)
        token_score = token_raw * 100.0

        # Compute Phonetic
        phonetic_raw = phonetic_similarity(query_name, target_name)
        phonetic_score = phonetic_raw * 100.0

        if is_word_reversal:
            match_type = "WORD_REVERSAL_PERMUTATION"
        elif jw_score >= 88.0 and token_score >= 88.0:
            match_type = "FUZZY_JARO_WINKLER"
        elif phonetic_score >= 75.0 and jw_score >= 70.0:
            match_type = "PHONETIC_SOUNDEX"
        elif token_score >= 70.0:
            match_type = "TOKEN_SET_PARTIAL"
        else:
            match_type = "LOW_SIMILARITY"

    # Base linguistic score
    base_score = (
        cfg.weight_jaro_winkler * jw_score +
        cfg.weight_token_set * token_score +
        cfg.weight_phonetic * phonetic_score
    )

    # 2. Corroborating Attribute Adjustments
    corroboration_adj = 0.0
    corroboration_details: Dict[str, Any] = {
        "dob_status": "NOT_PROVIDED",
        "country_status": "NOT_PROVIDED",
        "id_status": "NOT_PROVIDED"
    }

    # Identifier check
    if query_id and target_id:
        clean_qid = query_id.replace("-", "").replace(" ", "").upper()
        clean_tid = target_id.replace("-", "").replace(" ", "").upper()
        if clean_qid == clean_tid and clean_qid != "":
            corroboration_adj += cfg.identifier_match_bonus
            corroboration_details["id_status"] = "EXACT_MATCH"
        else:
            corroboration_details["id_status"] = "MISMATCH"

    # DOB check
    if query_dob and target_dob:
        if query_dob == target_dob:
            corroboration_adj += cfg.dob_match_bonus
            corroboration_details["dob_status"] = "EXACT_MATCH"
        else:
            corroboration_adj -= cfg.dob_mismatch_penalty
            corroboration_details["dob_status"] = "MISMATCH_PENALTY"

    # Country check
    if query_country and target_country:
        if query_country.strip().lower() == target_country.strip().lower():
            corroboration_adj += cfg.country_match_bonus
            corroboration_details["country_status"] = "MATCH"
        else:
            corroboration_details["country_status"] = "DIFFERENT_JURISDICTION"

    # Final composite score bounded [0.0, 100.0]
    final_score = max(0.0, min(100.0, base_score + corroboration_adj))

    # Token differences
    q_tokens = get_token_bag(query_name)
    t_tokens = get_token_bag(target_name)
    common_tokens = sorted(list(set(q_tokens).intersection(set(t_tokens))))

    token_diffs = {
        "screenedTokens": q_tokens,
        "matchedTokens": t_tokens,
        "commonTokens": common_tokens
    }

    # Operational Disposition
    if final_score >= cfg.auto_freeze_threshold:
        disposition = "CONFIRMED_TRUE_HIT"
    elif final_score >= cfg.quarantine_threshold:
        disposition = "PENDING_REVIEW"
    else:
        disposition = "DISMISSED_FALSE_POSITIVE"

    return MatchResult(
        match_score=final_score,
        jaro_winkler_score=jw_score,
        token_set_score=token_score,
        phonetic_score=phonetic_score,
        corroboration_score=corroboration_adj,
        corroboration_details=corroboration_details,
        match_type=match_type,
        disposition=disposition,
        token_diffs=token_diffs,
        screened_name=query_name,
        matched_entity=target_name
    )
