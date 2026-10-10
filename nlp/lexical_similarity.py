import math
from collections import Counter


# ---------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------

def _safe_tokens(tokens):
    """
    Remove empty values and normalize tokens to lowercase.
    """

    if not tokens:
        return []

    return [
        str(token).lower()
        for token in tokens
        if str(token).strip()
    ]


# ---------------------------------------------------------
# EXACT WORD OVERLAP
# ---------------------------------------------------------

def exact_word_overlap(tokens_a, tokens_b):
    """
    Calculate overlap using the exact words appearing
    in both texts.

    Returns a percentage from 0 to 100.
    """

    tokens_a = _safe_tokens(tokens_a)
    tokens_b = _safe_tokens(tokens_b)

    set_a = set(tokens_a)
    set_b = set(tokens_b)

    if not set_a or not set_b:
        return 0.0

    common_words = set_a.intersection(set_b)

    smaller_set_size = min(len(set_a), len(set_b))

    return (len(common_words) / smaller_set_size) * 100


# ---------------------------------------------------------
# LEMMA OVERLAP
# ---------------------------------------------------------

def lemma_overlap(lemmas_a, lemmas_b):
    """
    Calculate overlap using lemmatized words.

    This allows related word forms such as:

        models → model
        predicting → predict

    to be treated as the same lexical item.
    """

    lemmas_a = _safe_tokens(lemmas_a)
    lemmas_b = _safe_tokens(lemmas_b)

    set_a = set(lemmas_a)
    set_b = set(lemmas_b)

    if not set_a or not set_b:
        return 0.0

    common_lemmas = set_a.intersection(set_b)

    smaller_set_size = min(len(set_a), len(set_b))

    return (len(common_lemmas) / smaller_set_size) * 100


# ---------------------------------------------------------
# JACCARD SIMILARITY
# ---------------------------------------------------------

def jaccard_similarity(tokens_a, tokens_b):
    """
    Calculate Jaccard similarity between two token sets.

    Jaccard = intersection / union

    Returns a percentage from 0 to 100.
    """

    tokens_a = set(_safe_tokens(tokens_a))
    tokens_b = set(_safe_tokens(tokens_b))

    union = tokens_a.union(tokens_b)

    if not union:
        return 0.0

    intersection = tokens_a.intersection(tokens_b)

    return (len(intersection) / len(union)) * 100


# ---------------------------------------------------------
# TF-IDF COSINE SIMILARITY
# ---------------------------------------------------------

def cosine_similarity(tokens_a, tokens_b):
    """
    Calculate cosine similarity between two token
    frequency vectors.

    This is a lightweight TF-based lexical comparison.
    """

    tokens_a = _safe_tokens(tokens_a)
    tokens_b = _safe_tokens(tokens_b)

    if not tokens_a or not tokens_b:
        return 0.0

    counter_a = Counter(tokens_a)
    counter_b = Counter(tokens_b)

    vocabulary = set(counter_a).union(counter_b)

    dot_product = 0.0
    magnitude_a = 0.0
    magnitude_b = 0.0

    for word in vocabulary:

        value_a = counter_a.get(word, 0)
        value_b = counter_b.get(word, 0)

        dot_product += value_a * value_b
        magnitude_a += value_a ** 2
        magnitude_b += value_b ** 2

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    similarity = dot_product / (
        math.sqrt(magnitude_a) *
        math.sqrt(magnitude_b)
    )

    return similarity * 100


# ---------------------------------------------------------
# COMMON TERMS
# ---------------------------------------------------------

def get_common_terms(tokens_a, tokens_b):
    """
    Return the unique terms appearing in both texts.
    """

    set_a = set(_safe_tokens(tokens_a))
    set_b = set(_safe_tokens(tokens_b))

    return sorted(set_a.intersection(set_b))


# ---------------------------------------------------------
# UNIQUE TERMS
# ---------------------------------------------------------

def get_unique_terms(tokens_a, tokens_b):
    """
    Return terms that occur only in either document.
    """

    set_a = set(_safe_tokens(tokens_a))
    set_b = set(_safe_tokens(tokens_b))

    return {
        "document_a_only": sorted(set_a - set_b),
        "document_b_only": sorted(set_b - set_a)
    }


# ---------------------------------------------------------
# COMPLETE LEXICAL ANALYSIS
# ---------------------------------------------------------

def calculate_lexical_similarity(
    tokens_a,
    tokens_b,
    lemmas_a=None,
    lemmas_b=None
):
    """
    Perform the complete lexical comparison.

    Returns all lexical measurements in one structured result.
    """

    if lemmas_a is None:
        lemmas_a = tokens_a

    if lemmas_b is None:
        lemmas_b = tokens_b

    exact_score = exact_word_overlap(
        tokens_a,
        tokens_b
    )

    lemma_score = lemma_overlap(
        lemmas_a,
        lemmas_b
    )

    jaccard_score = jaccard_similarity(
        tokens_a,
        tokens_b
    )

    cosine_score = cosine_similarity(
        tokens_a,
        tokens_b
    )

    common_terms = get_common_terms(
        lemmas_a,
        lemmas_b
    )

    unique_terms = get_unique_terms(
        lemmas_a,
        lemmas_b
    )

    # Weighted lexical score
    lexical_score = (
        (lemma_score * 0.30) +
        (jaccard_score * 0.20) +
        (cosine_score * 0.50)
    )

    return {
        "exact_word_overlap": round(exact_score, 2),
        "lemma_overlap": round(lemma_score, 2),
        "jaccard_similarity": round(jaccard_score, 2),
        "cosine_similarity": round(cosine_score, 2),
        "lexical_score": round(lexical_score, 2),
        "common_terms": common_terms,
        "unique_terms": unique_terms
    }