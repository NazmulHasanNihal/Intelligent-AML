"""
src/screening/normalizer.py — Comprehensive Entity Normalization Engine
Implements:
1. Unicode NFKD decomposition and diacritic mark stripping (e.g., Müller -> Muller).
2. Case folding and punctuation harmonization.
3. Legal entity corporate suffix stripping (LLC, FZE, Ltd, AG, GmbH, Corp, etc.).
4. Name-order permutations (Last, First <-> First Last).
5. Bangla-to-Latin transliteration variant standardization.
"""

import re
import unicodedata
from typing import List, Set, Tuple


# Corporate legal suffix dictionary across international and offshore jurisdictions
CORPORATE_LEGAL_SUFFIXES: Set[str] = {
    # English / Global
    "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corp.", "corporation",
    "inc", "inc.", "incorporated", "co", "co.", "company", "plc", "p.l.c.",
    "holdings", "holding", "group", "enterprises", "enterprise", "industries",
    "industry", "syndicate", "international", "intl", "global", "trading",
    "logistics", "shipping", "services", "management", "investments",
    # UAE / Gulf Offshore
    "fze", "fzc", "fzco", "dmcc", "llc - so", "pjsc", "prjs",
    # German / Swiss / European
    "ag", "a.g.", "gmbh", "g.m.b.h.", "sa", "s.a.", "sarl", "bv", "b.v.", "nv", "n.v.",
    # Asian / Regional
    "pte", "pte.", "pte ltd", "sdn bhd", "bhd", "pvt", "pvt.", "private limited"
}

# Bangla-to-Latin phonetic transliteration harmonization map
BANGLA_TRANSLITERATION_MAP = [
    # Common Honorifics / Titles
    (r"\bmd\.(?=\s|$)", "mohammed"),
    (r"\bmd\b", "mohammed"),
    (r"\bmohammad\b", "mohammed"),
    (r"\bmuhammad\b", "mohammed"),
    (r"\bmohammod\b", "mohammed"),
    (r"\bseikh\b", "sheikh"),
    (r"\bshaikh\b", "sheikh"),
    (r"\bshaykh\b", "sheikh"),
    (r"\bsheykh\b", "sheikh"),
    # Common Bangla Patronymics and Surnames
    (r"\brohman\b", "rahman"),
    (r"\brokhman\b", "rahman"),
    (r"\brehman\b", "rahman"),
    (r"\bchoudhury\b", "chowdhury"),
    (r"\bchowdury\b", "chowdhury"),
    (r"\bchaudhury\b", "chowdhury"),
    (r"\bchaudhri\b", "chowdhury"),
    (r"\bchoudhry\b", "chowdhury"),
    (r"\bkahn\b", "khan"),
    (r"\bahmad\b", "ahmed"),
    (r"\behmed\b", "ahmed"),
    (r"\bhussain\b", "hossain"),
    (r"\bhussein\b", "hossain"),
    (r"\bhossein\b", "hossain"),
    (r"\bhasan\b", "hassan"),
    (r"\bhaque\b", "haq"),
    (r"\bhuq\b", "haq"),
    (r"\bislam\b", "islam"),
    (r"\bislem\b", "islam"),
    (r"\bali\b", "ali"),
    (r"\bul\b", "ul"),
    (r"\bal-", "al "),
    (r"\bel-", "al "),
]


def strip_diacritics(text: str) -> str:
    """
    Decomposes Unicode characters into NFKD canonical form and strips
    all non-spacing combining diacritical marks.
    E.g., "Müller" -> "Muller", "François" -> "Francois", "Łódź" -> "Lodz".
    """
    if not text:
        return ""
    # Normalize NFKD (Compatibility Decomposition)
    nfkd_form = unicodedata.normalize("NFKD", text)
    # Filter out combining diacritical marks (Mn category)
    without_diacritics = "".join(c for c in nfkd_form if unicodedata.category(c) != "Mn")
    # Replace non-standard letters
    char_replacements = {
        "ł": "l", "Ł": "L", "ø": "o", "Ø": "O", "æ": "ae", "Æ": "AE",
        "œ": "oe", "Œ": "OE", "ß": "ss", "đ": "d", "Đ": "D"
    }
    for orig, rep in char_replacements.items():
        without_diacritics = without_diacritics.replace(orig, rep)
    return without_diacritics


def strip_legal_suffixes(tokens: List[str]) -> List[str]:
    """
    Removes corporate legal entity designations from the end of a token list.
    E.g., ['gulf', 'star', 'commodities', 'fze'] -> ['gulf', 'star', 'commodities']
    """
    cleaned = list(tokens)
    while cleaned:
        tail = cleaned[-1]
        # Check single token
        if tail in CORPORATE_LEGAL_SUFFIXES:
            cleaned.pop()
            continue
        # Check two-token suffix (e.g., 'pte', 'ltd')
        if len(cleaned) >= 2:
            two_word = f"{cleaned[-2]} {cleaned[-1]}"
            if two_word in CORPORATE_LEGAL_SUFFIXES:
                cleaned.pop()
                cleaned.pop()
                continue
        break
    return cleaned


def standardize_bangla_transliteration(text: str) -> str:
    """
    Applies phonetic standardization rules for Bengali/Bangla names transliterated into Latin characters.
    """
    normalized = text
    for pattern, replacement in BANGLA_TRANSLITERATION_MAP:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized


def normalize_entity_name(
    raw_name: str,
    strip_legal: bool = True,
    apply_bangla_rules: bool = True
) -> str:
    """
    Full enterprise normalization pipeline:
    1. Unicode decomposition & diacritics removal.
    2. Lowercase folding.
    3. Punctuation removal (retaining alphanumeric and spaces).
    4. Optional Bangla-to-Latin transliteration mapping.
    5. Tokenization and optional legal suffix stripping.
    6. Reassembly into canonical spaced string.
    """
    if not raw_name:
        return ""

    # Step 1: Strip diacritics
    cleaned = strip_diacritics(raw_name)

    # Step 2: Lowercase
    cleaned = cleaned.lower()

    # Step 3: Standardize Bangla transliterations if applicable
    if apply_bangla_rules:
        cleaned = standardize_bangla_transliteration(cleaned)

    # Step 4: Replace punctuation with spaces
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)

    # Step 5: Collapse multiple spaces
    tokens = cleaned.split()

    # Step 6: Strip legal suffixes
    if strip_legal:
        tokens = strip_legal_suffixes(tokens)

    return " ".join(tokens)


def get_token_bag(name: str) -> List[str]:
    """Returns normalized tokens as a clean list."""
    return normalize_entity_name(name, strip_legal=True).split()


def get_name_order_permutations(name: str) -> List[str]:
    """
    Generates standard name-order permutations:
    - Original normalized
    - Alphabetically sorted tokens (order-invariant)
    - Reversed order (e.g. 'Hasan, Nazmul' -> 'Nazmul Hasan')
    """
    tokens = get_token_bag(name)
    if not tokens:
        return []

    original = " ".join(tokens)
    permutations = [original]

    if len(tokens) > 1:
        # Sorted tokens (canonical invariant)
        sorted_order = " ".join(sorted(tokens))
        if sorted_order not in permutations:
            permutations.append(sorted_order)

        # Reversed order
        reversed_order = " ".join(reversed(tokens))
        if reversed_order not in permutations:
            permutations.append(reversed_order)

    return permutations
