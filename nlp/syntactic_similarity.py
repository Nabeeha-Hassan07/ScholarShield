from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

from nlp.syntax import analyze_syntax


def extract_dependency_patterns(text):
    """
    Extract POS + dependency patterns from a document.
    """
    if not text:
        return []

    syntax_result = analyze_syntax(text)
    patterns = []

    for sentence in syntax_result["sentences"]:
        for token in sentence["tokens"]:
            if token["is_punctuation"]:
                continue

            pattern = f"{token['pos']}:{token['dependency']}"
            patterns.append(pattern)

    return patterns


def dependency_pattern_similarity(text_a, text_b):
    """
    Compare POS/dependency pattern distributions.
    """
    patterns_a = extract_dependency_patterns(text_a)
    patterns_b = extract_dependency_patterns(text_b)

    if not patterns_a or not patterns_b:
        return 0.0

    counter_a = Counter(patterns_a)
    counter_b = Counter(patterns_b)

    vocabulary = sorted(
        set(counter_a).union(counter_b)
    )

    vector_a = [
        counter_a.get(pattern, 0)
        for pattern in vocabulary
    ]

    vector_b = [
        counter_b.get(pattern, 0)
        for pattern in vocabulary
    ]

    similarity = cosine_similarity(
        [vector_a],
        [vector_b]
    )[0][0]

    return round(similarity * 100, 2)


def extract_sentence_structure(text):
    """
    Extract the ordered dependency structure of each sentence.

    Example:
    nsubj -> ROOT -> dobj
    """
    if not text:
        return []

    syntax_result = analyze_syntax(text)
    structures = []

    for sentence in syntax_result["sentences"]:
        dependencies = []

        for token in sentence["tokens"]:
            if token["is_punctuation"]:
                continue

            dependencies.append(token["dependency"])

        if dependencies:
            structures.append(tuple(dependencies))

    return structures


def sentence_structure_similarity(text_a, text_b):
    """
    Compare sentence-level dependency structures.

    A sentence receives a structural match when its
    dependency sequence is identical to a sentence
    in the other document.
    """
    structures_a = extract_sentence_structure(text_a)
    structures_b = extract_sentence_structure(text_b)

    if not structures_a or not structures_b:
        return 0.0

    matches = 0

    for structure_a in structures_a:
        if structure_a in structures_b:
            matches += 1

    total_sentences = max(
        len(structures_a),
        len(structures_b)
    )

    return round((matches / total_sentences) * 100, 2)


def extract_pos_sequence(text):
    """
    Extract POS tag sequence from a document.
    """
    if not text:
        return []

    syntax_result = analyze_syntax(text)
    pos_sequence = []

    for sentence in syntax_result["sentences"]:
        for token in sentence["tokens"]:
            if token["is_punctuation"]:
                continue

            pos_sequence.append(token["pos"])

    return pos_sequence


def pos_pattern_similarity(text_a, text_b):
    """
    Compare POS-tag distributions between two documents.
    """
    pos_a = extract_pos_sequence(text_a)
    pos_b = extract_pos_sequence(text_b)

    if not pos_a or not pos_b:
        return 0.0

    counter_a = Counter(pos_a)
    counter_b = Counter(pos_b)

    vocabulary = sorted(
        set(counter_a).union(counter_b)
    )

    vector_a = [
        counter_a.get(pos, 0)
        for pos in vocabulary
    ]

    vector_b = [
        counter_b.get(pos, 0)
        for pos in vocabulary
    ]

    similarity = cosine_similarity(
        [vector_a],
        [vector_b]
    )[0][0]

    return round(similarity * 100, 2)


def calculate_syntactic_similarity(text_a, text_b):
    """
    Calculate the overall syntactic similarity.
    """

    dependency_score = dependency_pattern_similarity(
        text_a,
        text_b
    )

    sentence_structure_score = sentence_structure_similarity(
        text_a,
        text_b
    )

    pos_score = pos_pattern_similarity(
        text_a,
        text_b
    )

    syntactic_score = (
        (dependency_score * 0.30) +
        (sentence_structure_score * 0.50) +
        (pos_score * 0.20)
    )

    return {
        "dependency_similarity": dependency_score,
        "sentence_structure_similarity": sentence_structure_score,
        "pos_similarity": pos_score,
        "syntactic_score": round(syntactic_score, 2)
    }