from typing import Optional


DEFAULT_WEIGHTS = {
    "lexical": 0.20,
    "syntactic": 0.20,
    "semantic": 0.30,
    "contextual": 0.15,
    "meaning": 0.15
}


def _safe_score(score):
    """
    Convert a score into a valid 0-100 range.
    """
    if score is None:
        return 0.0

    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0.0

    return max(0.0, min(100.0, score))


def calculate_multi_level_score(
    lexical_score: Optional[float] = None,
    syntactic_score: Optional[float] = None,
    semantic_score: Optional[float] = None,
    contextual_score: Optional[float] = None,
    meaning_score: Optional[float] = None,
    weights=None
):
    """
    Calculate similarity across multiple linguistic levels.
    """

    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    scores = {
        "lexical": _safe_score(lexical_score),
        "syntactic": _safe_score(syntactic_score),
        "semantic": _safe_score(semantic_score),
        "contextual": _safe_score(contextual_score),
        "meaning": _safe_score(meaning_score)
    }

    weighted_score = (
        scores["lexical"] * weights["lexical"] +
        scores["syntactic"] * weights["syntactic"] +
        scores["semantic"] * weights["semantic"] +
        scores["contextual"] * weights["contextual"] +
        scores["meaning"] * weights["meaning"]
    )

    return {
        "lexical_score": round(scores["lexical"], 2),
        "syntactic_score": round(scores["syntactic"], 2),
        "semantic_score": round(scores["semantic"], 2),
        "contextual_score": round(scores["contextual"], 2),
        "meaning_score": round(scores["meaning"], 2),
        "overall_score": round(weighted_score, 2),
        "weights": weights
    }


def get_similarity_level(score):
    """
    Convert the overall similarity score into an
    interpretable similarity level.
    """

    score = _safe_score(score)

    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Moderate"
    elif score >= 20:
        return "Low"
    else:
        return "Very Low"


def generate_multi_level_result(
    lexical_score=None,
    syntactic_score=None,
    semantic_score=None,
    contextual_score=None,
    meaning_score=None,
    weights=None
):
    """
    Generate the complete multi-level similarity result.
    """

    result = calculate_multi_level_score(
        lexical_score=lexical_score,
        syntactic_score=syntactic_score,
        semantic_score=semantic_score,
        contextual_score=contextual_score,
        meaning_score=meaning_score,
        weights=weights
    )

    result["similarity_level"] = get_similarity_level(
        result["overall_score"]
    )

    return result