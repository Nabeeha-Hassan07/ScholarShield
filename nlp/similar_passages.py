import re

from sklearn.metrics.pairwise import cosine_similarity

from nlp.preprocessing import split_sentences
from nlp.model_loader import get_sentence_transformer


DEFAULT_THRESHOLD = 60.0

# Very common words that do not provide strong evidence
# that two passages are actually similar in content.
GENERIC_WORDS = {
    "document",
    "documents",
    "text",
    "texts",
    "page",
    "pages",
    "section",
    "sections",
    "paragraph",
    "paragraphs",
    "sentence",
    "sentences",
    "meaning",
    "meanings",
    "context",
    "contexts",
    "focus",
    "focused",
    "analysis",
    "analyses",
    "analyze",
    "analyzed",
    "result",
    "results",
    "information",
    "content",
    "example",
    "examples",
    "study",
    "studies",
    "system",
    "systems",
    "using",
    "used",
    "use",
    "shows",
    "show",
    "refers",
    "referring",
    "describes",
    "described",
}


def _content_words(sentence):
    """
    Extract meaningful words from a sentence.

    Very common academic/documentation words are ignored because
    they are weak evidence of actual passage similarity.
    """

    if not sentence:
        return set()

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z'-]+\b",
        sentence.lower()
    )

    meaningful_words = set()

    for word in words:

        word = word.strip("-'")

        if len(word) < 3:
            continue

        if word in GENERIC_WORDS:
            continue

        meaningful_words.add(word)

    return meaningful_words


def _has_lexical_support(target_sentence, reference_sentence):
    """
    Check whether a medium-strength semantic match is supported
    by at least two meaningful shared words.

    This prevents generic semantic similarity from producing
    false passage matches when only one ambiguous/common term
    is shared.
    """

    target_words = _content_words(target_sentence)
    reference_words = _content_words(reference_sentence)

    shared_words = target_words.intersection(reference_words)

    return len(shared_words) >= 2


def _is_valid_passage_match(
    target_sentence,
    reference_sentence,
    similarity_score
):
    """
    Decide whether a sentence pair should be reported as
    a meaningful similar passage.

    Very high semantic similarity is strong evidence by itself.

    Medium semantic similarity must also have lexical support.
    """

    if similarity_score >= 80.0:
        return True

    if similarity_score >= DEFAULT_THRESHOLD:
        return _has_lexical_support(
            target_sentence,
            reference_sentence
        )

    return False


def generate_sentence_embeddings(sentences):
    """
    Generate embeddings for a list of sentences.
    """

    if not sentences:
        return []

    model = get_sentence_transformer()

    embeddings = model.encode(
        sentences,
        convert_to_numpy=True
    )

    return embeddings


def calculate_sentence_similarities(
    target_sentences,
    reference_sentences
):
    """
    Compare every target sentence with every reference sentence.
    """

    if not target_sentences or not reference_sentences:
        return []

    target_embeddings = generate_sentence_embeddings(
        target_sentences
    )

    reference_embeddings = generate_sentence_embeddings(
        reference_sentences
    )

    similarity_matrix = cosine_similarity(
        target_embeddings,
        reference_embeddings
    )

    return similarity_matrix


def detect_similar_passages(
    target_text,
    reference_text,
    threshold=DEFAULT_THRESHOLD
):
    """
    Detect meaningful similar sentence pairs between two documents.

    A sentence pair is reported when:

    1. Semantic similarity reaches the configured threshold.
    2. Very high semantic similarity (80%+) is accepted directly.
    3. Medium similarity (60% to 79.99%) must also have
       meaningful lexical support.
    4. A reference sentence is not reused for multiple
       target sentences.
    """

    target_sentences = split_sentences(target_text)
    reference_sentences = split_sentences(reference_text)

    if not target_sentences or not reference_sentences:
        return []

    similarity_matrix = calculate_sentence_similarities(
        target_sentences,
        reference_sentences
    )

    matches = []

    # Keep track of reference sentences that have already
    # been assigned to a stronger target passage.
    used_reference_indices = set()

    # Process strongest candidate pairs first so that the
    # best-supported matches get priority.
    candidate_pairs = []

    for target_index, target_sentence in enumerate(
        target_sentences
    ):

        for reference_index, reference_sentence in enumerate(
            reference_sentences
        ):

            similarity_score = (
                similarity_matrix[
                    target_index,
                    reference_index
                ] * 100
            )

            similarity_score = max(
                0.0,
                min(100.0, similarity_score)
            )

            if similarity_score >= threshold:

                candidate_pairs.append({
                    "target_index": target_index,
                    "reference_index": reference_index,
                    "target_sentence": target_sentence,
                    "reference_sentence": reference_sentence,
                    "similarity_score": float(
                        similarity_score
                    )
                })

    candidate_pairs.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    used_target_indices = set()

    for candidate in candidate_pairs:

        target_index = candidate["target_index"]
        reference_index = candidate["reference_index"]

        target_sentence = candidate["target_sentence"]
        reference_sentence = candidate["reference_sentence"]

        similarity_score = candidate["similarity_score"]

        # Do not allow the same sentence to be repeatedly
        # reported against several passages.
        if target_index in used_target_indices:
            continue

        if reference_index in used_reference_indices:
            continue

        if not _is_valid_passage_match(
            target_sentence,
            reference_sentence,
            similarity_score
        ):
            continue

        matches.append({
            "target_sentence": target_sentence,
            "reference_sentence": reference_sentence,
            "target_index": target_index,
            "reference_index": reference_index,
            "similarity_score": round(
                float(similarity_score),
                2
            ),
            "similarity_type": "Semantic"
        })

        used_target_indices.add(target_index)
        used_reference_indices.add(reference_index)

    matches.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return matches


def detect_similar_passages_multiple(
    target_text,
    reference_documents,
    threshold=DEFAULT_THRESHOLD
):
    """
    Compare one target document against multiple
    reference documents.
    """

    if not target_text or not reference_documents:
        return []

    all_matches = []

    for reference_document in reference_documents:

        reference_id = reference_document.get(
            "document_id"
        )

        reference_name = reference_document.get(
            "filename"
        )

        reference_text = reference_document.get(
            "text",
            ""
        )

        matches = detect_similar_passages(
            target_text,
            reference_text,
            threshold
        )

        for match in matches:

            match["reference_document_id"] = reference_id
            match["reference_filename"] = reference_name

            all_matches.append(match)

    all_matches.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return all_matches