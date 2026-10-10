def _format_percentage(score):
    return f"{score:.2f}%"


def _get_level(score):
    if score >= 70:
        return "high"
    elif score >= 40:
        return "moderate"
    else:
        return "low"


def explain_lexical_similarity(lexical_result):
    if not lexical_result:
        return {
            "level": "unavailable",
            "score": 0.0,
            "summary": "No lexical similarity information is available.",
            "details": []
        }

    score = lexical_result.get("lexical_score", 0.0)
    common_terms = lexical_result.get("common_terms", [])

    level = _get_level(score)
    details = []

    if level == "high":
        details.append(
            "The documents share a substantial amount of vocabulary "
            "or closely related terms."
        )
    elif level == "moderate":
        details.append(
            "The documents share a moderate amount of vocabulary "
            "or closely related terms."
        )
    else:
        details.append(
            "The documents use relatively different vocabulary."
        )

    if common_terms:
        displayed_terms = common_terms[:10]
        details.append(
            "Examples of shared terms include: "
            + ", ".join(displayed_terms)
            + "."
        )

    return {
        "level": level,
        "score": score,
        "summary": (
            f"Lexical similarity is {_format_percentage(score)}, "
            f"indicating {level} vocabulary overlap."
        ),
        "details": details
    }


def explain_semantic_similarity(semantic_result):
    if not semantic_result:
        return {
            "level": "unavailable",
            "score": 0.0,
            "summary": "No semantic similarity information is available.",
            "details": []
        }

    score = semantic_result.get("semantic_similarity_score", 0.0)
    level = _get_level(score)

    if level == "high":
        interpretation = (
            "The documents express strongly related meanings or ideas, "
            "even when some wording may differ."
        )
    elif level == "moderate":
        interpretation = (
            "The documents share some meaningful conceptual similarity."
        )
    else:
        interpretation = (
            "The documents have relatively limited semantic similarity."
        )

    return {
        "level": level,
        "score": score,
        "summary": (
            f"Semantic similarity is {_format_percentage(score)}, "
            f"indicating {level} similarity in meaning."
        ),
        "details": [interpretation]
    }


def explain_syntactic_similarity(syntactic_result):
    if not syntactic_result:
        return {
            "level": "unavailable",
            "score": 0.0,
            "summary": "No syntactic similarity information is available.",
            "details": []
        }

    score = syntactic_result.get("syntactic_score", 0.0)
    level = _get_level(score)

    if level == "high":
        interpretation = (
            "The documents use similar grammatical and dependency structures."
        )
    elif level == "moderate":
        interpretation = (
            "The documents have some similarities in grammatical "
            "and dependency structure."
        )
    else:
        interpretation = (
            "The documents use substantially different grammatical "
            "or dependency structures."
        )

    return {
        "level": level,
        "score": score,
        "summary": (
            f"Syntactic similarity is {_format_percentage(score)}, "
            f"indicating {level} structural similarity."
        ),
        "details": [interpretation]
    }


def explain_contextual_similarity(contextual_result):
    if not contextual_result:
        return {
            "level": "unavailable",
            "score": 0.0,
            "summary": "No contextual similarity information is available.",
            "details": []
        }

    score = contextual_result.get("contextual_score", 0.0)
    level = _get_level(score)

    if level == "high":
        interpretation = (
            "Shared content words tend to have related meanings when "
            "interpreted within their surrounding sentence context."
        )
    elif level == "moderate":
        interpretation = (
            "Several shared words have related meanings in their "
            "surrounding contexts, although the correspondence is not uniform."
        )
    else:
        interpretation = (
            "The shared vocabulary shows relatively limited correspondence "
            "when interpreted in context."
        )

    return {
        "level": level,
        "score": score,
        "summary": (
            f"Contextual similarity is {_format_percentage(score)}, "
            f"indicating {level} contextual and word-sense correspondence."
        ),
        "details": [interpretation]
    }


def explain_meaning_similarity(meaning_result):
    if not meaning_result:
        return {
            "level": "unavailable",
            "score": 0.0,
            "summary": "No meaning representation information is available.",
            "details": []
        }

    score = meaning_result.get("meaning_score", 0.0)
    level = _get_level(score)

    if level == "high":
        interpretation = (
            "The documents show strong correspondence in semantic frames, "
            "predicates, and semantic roles such as actions, entities, "
            "and their relationships."
        )
    elif level == "moderate":
        interpretation = (
            "The documents show some correspondence in predicates, "
            "semantic roles, and meaning relationships."
        )
    else:
        interpretation = (
            "The documents show relatively limited correspondence "
            "in their underlying semantic roles and meaning structures."
        )

    return {
        "level": level,
        "score": score,
        "summary": (
            f"Meaning similarity is {_format_percentage(score)}, "
            f"indicating {level} correspondence in semantic structure."
        ),
        "details": [interpretation]
    }


def generate_simple_explanation(
    lexical_explanation,
    semantic_explanation,
    syntactic_explanation,
    contextual_explanation,
    meaning_explanation,
    multi_level_result
):
    overall_score = multi_level_result.get("overall_score", 0.0)
    similarity_level = multi_level_result.get(
        "similarity_level",
        "Unknown"
    )

    strong_dimensions = []

    explanations = [
        lexical_explanation,
        semantic_explanation,
        syntactic_explanation,
        contextual_explanation,
        meaning_explanation
    ]

    dimension_names = [
        "vocabulary",
        "meaning",
        "sentence structure",
        "word context",
        "underlying meaning structure"
    ]

    for explanation, name in zip(explanations, dimension_names):
        if explanation["level"] == "high":
            strong_dimensions.append(name)

    if strong_dimensions:
        if len(strong_dimensions) == 1:
            strength_text = strong_dimensions[0]
        elif len(strong_dimensions) == 2:
            strength_text = (
                f"{strong_dimensions[0]} and {strong_dimensions[1]}"
            )
        else:
            strength_text = (
                ", ".join(strong_dimensions[:-1])
                + ", and "
                + strong_dimensions[-1]
            )

        return (
            f"The two documents show {similarity_level.lower()} overall "
            f"similarity ({_format_percentage(overall_score)}). "
            f"They have particularly strong correspondence in "
            f"{strength_text}. "
            f"Some similarities may come from shared wording, while others "
            f"come from similar ideas, context, sentence structure, or "
            f"underlying semantic relationships."
        )

    return (
        f"The two documents show {similarity_level.lower()} overall "
        f"similarity ({_format_percentage(overall_score)}). "
        f"The result combines similarities in vocabulary, sentence "
        f"structure, meaning, context, and semantic relationships."
    )


def generate_overall_interpretation(
    lexical_explanation,
    semantic_explanation,
    syntactic_explanation,
    contextual_explanation,
    meaning_explanation,
    multi_level_result
):
    overall_score = multi_level_result.get("overall_score", 0.0)
    similarity_level = multi_level_result.get(
        "similarity_level",
        "Unknown"
    )

    weights = multi_level_result.get("weights", {})

    highest_dimension = None
    highest_score = -1

    dimensions = {
        "lexical": lexical_explanation,
        "syntactic": syntactic_explanation,
        "semantic": semantic_explanation,
        "contextual": contextual_explanation,
        "meaning": meaning_explanation
    }

    for name, explanation in dimensions.items():
        score = explanation.get("score", 0.0)

        if score > highest_score:
            highest_score = score
            highest_dimension = name

    dimension_labels = {
        "lexical": "lexical similarity",
        "syntactic": "syntactic similarity",
        "semantic": "semantic similarity",
        "contextual": "contextual similarity",
        "meaning": "meaning similarity"
    }

    strongest_text = ""

    if highest_dimension:
        strongest_text = (
            f"The strongest individual dimension is "
            f"{dimension_labels[highest_dimension]} at "
            f"{_format_percentage(highest_score)}."
        )

    weight_text = ""

    if weights:
        weight_text = (
            " The final score is produced by combining the five NLP "
            "dimensions using their configured weights rather than simply "
            "averaging the component scores."
        )

    return (
        f"The overall similarity score is {_format_percentage(overall_score)}, "
        f"classified as {similarity_level}. "
        f"{strongest_text}"
        f"{weight_text} "
        f"This means the result reflects multiple forms of similarity, "
        f"including shared vocabulary, grammatical structure, semantic "
        f"meaning, contextual word relationships, and deeper meaning "
        f"representation."
    )


def generate_similarity_explanation(
    lexical_result=None,
    semantic_result=None,
    syntactic_result=None,
    contextual_result=None,
    meaning_result=None,
    multi_level_result=None
):
    lexical_explanation = explain_lexical_similarity(
        lexical_result
    )

    semantic_explanation = explain_semantic_similarity(
        semantic_result
    )

    syntactic_explanation = explain_syntactic_similarity(
        syntactic_result
    )

    contextual_explanation = explain_contextual_similarity(
        contextual_result
    )

    meaning_explanation = explain_meaning_similarity(
        meaning_result
    )

    if not multi_level_result:
        multi_level_result = {
            "overall_score": 0.0,
            "similarity_level": "Unknown",
            "weights": {}
        }

    simple_explanation = generate_simple_explanation(
        lexical_explanation,
        semantic_explanation,
        syntactic_explanation,
        contextual_explanation,
        meaning_explanation,
        multi_level_result
    )

    overall_interpretation = generate_overall_interpretation(
        lexical_explanation,
        semantic_explanation,
        syntactic_explanation,
        contextual_explanation,
        meaning_explanation,
        multi_level_result
    )

    technical_explanation = (
        "ScholarShield evaluates document similarity across five "
        "complementary NLP dimensions. Lexical analysis examines shared "
        "vocabulary; syntactic analysis compares grammatical and dependency "
        "structure; semantic analysis compares sentence-level meaning; "
        "contextual analysis considers word meaning within surrounding "
        "context; and meaning representation compares deeper semantic "
        "relationships such as predicates and semantic roles."
    )

    return {
        "overall_score": round(
            multi_level_result.get("overall_score", 0.0),
            2
        ),

        "similarity_level": multi_level_result.get(
            "similarity_level",
            "Unknown"
        ),

        "simple_explanation": simple_explanation,

        "technical_explanation": technical_explanation,

        "component_explanations": {
            "lexical": lexical_explanation,
            "semantic": semantic_explanation,
            "syntactic": syntactic_explanation,
            "contextual": contextual_explanation,
            "meaning": meaning_explanation
        },

        "overall_interpretation": overall_interpretation,

        # Keep these keys for compatibility with existing UI/code.
        "lexical": lexical_explanation,
        "semantic": semantic_explanation,
        "syntactic": syntactic_explanation,
        "contextual": contextual_explanation,
        "meaning": meaning_explanation,

        "explanation": simple_explanation
    }