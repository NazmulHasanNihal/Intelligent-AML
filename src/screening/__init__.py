"""
src/screening/ — Screening Fidelity & Entity Resolution Package
Exposes normalizer, multi-algorithm matcher, and official watchlist registry.
"""

from src.screening.normalizer import (
    normalize_entity_name,
    strip_diacritics,
    strip_legal_suffixes,
    standardize_bangla_transliteration,
    get_token_bag,
    get_name_order_permutations,
)
from src.screening.matcher import (
    compute_screening_score,
    jaro_winkler_similarity,
    token_set_similarity,
    phonetic_similarity,
    soundex,
    MatchResult,
    ScreeningThresholdConfig,
    DEFAULT_THRESHOLDS,
)
from src.screening.watchlist_registry import (
    WatchlistRegistry,
    WatchlistFeedMetadata,
    WatchlistEntity,
    watchlist_registry,
)

__all__ = [
    "normalize_entity_name",
    "strip_diacritics",
    "strip_legal_suffixes",
    "standardize_bangla_transliteration",
    "get_token_bag",
    "get_name_order_permutations",
    "compute_screening_score",
    "jaro_winkler_similarity",
    "token_set_similarity",
    "phonetic_similarity",
    "soundex",
    "MatchResult",
    "ScreeningThresholdConfig",
    "DEFAULT_THRESHOLDS",
    "WatchlistRegistry",
    "WatchlistFeedMetadata",
    "WatchlistEntity",
    "watchlist_registry",
]
