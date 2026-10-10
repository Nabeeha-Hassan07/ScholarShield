from collections import Counter
from difflib import SequenceMatcher

import nltk
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.metrics.pairwise import cosine_similarity

from nlp.preprocessing import preprocess_text
from nlp.lexical_similarity import calculate_lexical_similarity
from nlp.semantic_similarity import analyze_semantic_similarity
from nlp.syntactic_similarity import calculate_syntactic_similarity
from nlp.similar_passages import detect_similar_passages
from nlp.similarity_explanation import generate_similarity_explanation
from nlp.multi_level_score import generate_multi_level_result
from nlp.word_sense import disambiguate_word
from nlp.meaning_representation import meaning_representation
from nlp.model_loader import get_sentence_transformer


# ============================================================
# CONTEXT / WORD-SENSE HELPERS
# ============================================================

def _sentence_containing_word(text, word):
    """
    Return the first sentence containing the given word.
    """
    if not text or not word:
        return None

    try:
        sentences = nltk.sent_tokenize(text)
    except Exception:
        sentences = [text]

    word_lower = word.lower()

    for sentence in sentences:
        try:
            tokens = nltk.word_tokenize(sentence)
        except Exception:
            tokens = sentence.split()

        if any(token.lower() == word_lower for token in tokens):
            return sentence

    return None


def _content_words(tokens):
    """
    Select words that are useful for contextual comparison.

    Function words and very short tokens are excluded so that
    contextual similarity is not dominated by common academic
    stop-words.
    """
    if not tokens:
        return []

    try:
        tagged = pos_tag(tokens)
    except Exception:
        tagged = [(token, "") for token in tokens]

    allowed_prefixes = ("N", "V", "J", "R")

    words = []

    for word, tag in tagged:

        word = word.lower().strip()

        if len(word) < 3:
            continue

        if tag and not tag.startswith(allowed_prefixes):
            continue

        words.append(word)

    return words


def calculate_contextual_similarity(
    target_text,
    reference_text,
    target_preprocessed,
    reference_preprocessed
):
    """
    Calculate contextual / word-sense similarity.

    A word contributes strongly only when ScholarShield selects
    the SAME WordNet sense in both documents.

    Different senses are treated as contextual mismatches rather
    than being rewarded by WordNet semantic relatedness.
    """

    target_tokens = _content_words(
        target_preprocessed.get("normalized_tokens", [])
    )

    reference_tokens = _content_words(
        reference_preprocessed.get("normalized_tokens", [])
    )

    target_counts = Counter(target_tokens)
    reference_counts = Counter(reference_tokens)

    shared_words = sorted(
        set(target_counts) & set(reference_counts),
        key=lambda word: (
            -(target_counts[word] + reference_counts[word]),
            word
        )
    )

    if not shared_words:
        return {
            "contextual_score": 0.0,
            "shared_context_words": [],
            "analyzed_words": [],
            "matched_senses": 0,
            "sense_matches": 0
        }

    candidate_words = []

    for word in shared_words:
        try:
            sense_count = len(wordnet.synsets(word))
        except Exception:
            sense_count = 0

        if sense_count >= 2:
            candidate_words.append(word)

    candidate_words = candidate_words[:30]

    if not candidate_words:
        return {
            "contextual_score": 0.0,
            "shared_context_words": shared_words,
            "analyzed_words": [],
            "matched_senses": 0,
            "sense_matches": 0
        }

    analyzed_words = []
    sense_scores = []

    for word in candidate_words:

        target_sentence = _sentence_containing_word(
            target_text,
            word
        )

        reference_sentence = _sentence_containing_word(
            reference_text,
            word
        )

        if not target_sentence or not reference_sentence:
            continue

        try:
            target_sense = disambiguate_word(
                word,
                target_sentence
            )

            reference_sense = disambiguate_word(
                word,
                reference_sentence
            )
        except Exception:
            continue

        target_synset_name = target_sense.get("sense")
        reference_synset_name = reference_sense.get("sense")

        if not target_synset_name or not reference_synset_name:
            continue

        target_confidence = float(
            target_sense.get("confidence", 0.0)
        )

        reference_confidence = float(
            reference_sense.get("confidence", 0.0)
        )

        if (
            target_confidence < 0.50
            or reference_confidence < 0.50
        ):
            continue

        same_sense = (
            target_synset_name == reference_synset_name
        )

        if same_sense:
            score = min(
                target_confidence,
                reference_confidence
            )
        else:
            score = 0.0

        sense_scores.append(score * 100.0)

        analyzed_words.append({
            "word": word,
            "target_sense": target_synset_name,
            "reference_sense": reference_synset_name,
            "target_context_confidence": round(
                target_confidence * 100,
                2
            ),
            "reference_context_confidence": round(
                reference_confidence * 100,
                2
            ),
            "same_sense": same_sense,
            "similarity": round(
                score * 100.0,
                2
            )
        })

    if not sense_scores:
        contextual_score = 0.0
    else:
        contextual_score = (
            sum(sense_scores)
            /
            len(sense_scores)
        )

    matched_senses = sum(
        1
        for item in analyzed_words
        if item.get("same_sense")
    )

    return {
        "contextual_score": round(
            max(
                0.0,
                min(100.0, contextual_score)
            ),
            2
        ),
        "shared_context_words": shared_words,
        "analyzed_words": analyzed_words,
        "matched_senses": matched_senses,
        "sense_matches": len(analyzed_words)
    }


# ============================================================
# MEANING REPRESENTATION HELPERS
# ============================================================

def _string_similarity(first, second):
    """
    Basic normalized string similarity used as a fallback for
    short predicate/argument values.
    """
    if not first or not second:
        return 0.0

    return SequenceMatcher(
        None,
        str(first).lower().strip(),
        str(second).lower().strip()
    ).ratio()


def _predicate_similarity(first, second):
    """
    Compare two predicates using:
        1. Exact lemma agreement
        2. WordNet semantic relatedness
        3. Lexical fallback
    """
    if not first or not second:
        return 0.0

    first = str(first).lower().strip()
    second = str(second).lower().strip()

    if first == second:
        return 1.0

    try:

        first_synsets = wordnet.synsets(
            first,
            pos=wordnet.VERB
        )

        second_synsets = wordnet.synsets(
            second,
            pos=wordnet.VERB
        )

        relations = []

        for first_synset in first_synsets[:5]:

            for second_synset in second_synsets[:5]:

                relation = first_synset.wup_similarity(
                    second_synset
                )

                if relation is None:

                    relation = first_synset.path_similarity(
                        second_synset
                    )

                if relation is not None:
                    relations.append(
                        float(relation)
                    )

        if relations:
            return max(relations)

    except Exception:
        pass

    return _string_similarity(
        first,
        second
    )


def _role_text(arguments, role):
    """
    Convert a meaning-representation role into one text string.
    """
    values = arguments.get(
        role,
        []
    )

    if not values:
        return ""

    if isinstance(values, str):
        return values.strip()

    return " ".join(
        str(value)
        for value in values
    ).strip()


# ------------------------------------------------------------
# EMBEDDING CACHE
# ------------------------------------------------------------

def _collect_frame_texts(frames):
    """
    Collect every unique semantic-role phrase that may need
    sentence-transformer encoding.
    """

    texts = set()

    roles = [
        "subject",
        "object",
        "indirect_object",
        "modifiers"
    ]

    for frame in frames:

        arguments = frame.get(
            "arguments",
            {}
        )

        for role in roles:

            text = _role_text(
                arguments,
                role
            )

            if text:
                texts.add(text)

    return texts


def _build_embedding_cache(model, frames):
    """
    Build a reusable embedding cache for all semantic-role
    phrases in the supplied frames.
    """

    texts = _collect_frame_texts(
        frames
    )

    if not texts:
        return {}

    texts = list(texts)

    try:

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return {
            text: embeddings[index]
            for index, text in enumerate(texts)
        }

    except Exception:

        return {}


def _embedding_similarity_from_cache(
    embedding_cache,
    first,
    second
):
    """
    Calculate cosine similarity using cached embeddings.

    IMPORTANT:
    Do not remap [-1, 1] to [0, 1].

    That old mapping made a neutral cosine of 0.0 appear as
    50% similarity, which artificially inflated meaning scores.

    Here:
        cosine <= 0       -> 0 similarity
        cosine > 0        -> direct positive similarity
    """

    if not first or not second:
        return 0.0

    first = str(first).strip()
    second = str(second).strip()

    first_embedding = embedding_cache.get(
        first
    )

    second_embedding = embedding_cache.get(
        second
    )

    if first_embedding is None or second_embedding is None:

        return _string_similarity(
            first,
            second
        )

    try:

        score = cosine_similarity(
            [first_embedding],
            [second_embedding]
        )[0][0]

        # Positive cosine similarity is evidence of relatedness.
        # Zero/negative cosine similarity is treated as no
        # meaningful role similarity.
        return max(
            0.0,
            min(
                1.0,
                float(score)
            )
        )

    except Exception:

        return _string_similarity(
            first,
            second
        )


def _role_similarity(
    embedding_cache,
    target_arguments,
    reference_arguments
):
    """
    Compare semantic roles using cached embeddings.

    Only roles containing actual information are considered.

    If a role exists in one frame but not the other, that is a
    mismatch. If a role is absent from both frames, it provides
    no evidence and is ignored.

    Negation is only rewarded when BOTH frames explicitly contain
    the same negation state. Two non-negated sentences do not get
    an artificial similarity bonus.
    """

    roles = [
        "subject",
        "object",
        "indirect_object",
        "modifiers"
    ]

    role_scores = []

    for role in roles:

        target_text = _role_text(
            target_arguments,
            role
        )

        reference_text = _role_text(
            reference_arguments,
            role
        )

        if not target_text and not reference_text:
            continue

        if not target_text or not reference_text:

            # One frame explicitly contains this role while the
            # other does not. Treat it as a mismatch.
            role_scores.append(0.0)
            continue

        role_scores.append(
            _embedding_similarity_from_cache(
                embedding_cache,
                target_text,
                reference_text
            )
        )

    if not role_scores:
        role_score = 0.0
    else:
        role_score = (
            sum(role_scores)
            /
            len(role_scores)
        )

    target_negation = bool(
        target_arguments.get(
            "negation"
        )
    )

    reference_negation = bool(
        reference_arguments.get(
            "negation"
        )
    )

    # Negation only affects the score when at least one frame
    # explicitly contains negation.
    if target_negation or reference_negation:
        negation_score = (
            1.0
            if target_negation == reference_negation
            else 0.0
        )

        return (
            (role_score * 0.85)
            +
            (negation_score * 0.15)
        )

    return role_score


def _frame_similarity(
    embedding_cache,
    target_frame,
    reference_frame
):
    """
    Compare two predicate-argument meaning frames.

    Predicate similarity contributes 45%.
    Semantic-role similarity contributes 55%.

    A frame with neither meaningful predicate similarity nor
    meaningful role similarity is not considered a strong
    semantic-frame match.
    """

    predicate_score = _predicate_similarity(
        target_frame.get(
            "predicate"
        ),
        reference_frame.get(
            "predicate"
        )
    )

    role_score = _role_similarity(
        embedding_cache,
        target_frame.get(
            "arguments",
            {}
        ),
        reference_frame.get(
            "arguments",
            {}
        )
    )

    # Prevent weak generic predicates/roles from producing a
    # substantial frame score merely because every frame must
    # find a "best" candidate.
    if (
        predicate_score < 0.25
        and
        role_score < 0.30
    ):
        return 0.0

    score = (
        (predicate_score * 0.45)
        +
        (role_score * 0.55)
    )

    return max(
        0.0,
        min(
            1.0,
            score
        )
    )


def _best_frame_match(
    embedding_cache,
    frame,
    candidate_frames
):
    """
    Find the strongest meaning-frame match.

    Candidate comparisons reuse cached embeddings.
    """

    if not candidate_frames:
        return 0.0, None

    best_score = 0.0
    best_frame = None

    for candidate in candidate_frames:

        score = _frame_similarity(
            embedding_cache,
            frame,
            candidate
        )

        if score > best_score:

            best_score = score
            best_frame = candidate

    return (
        best_score,
        best_frame
    )


def calculate_meaning_similarity(
    target_text,
    reference_text
):
    """
    Calculate meaning-representation similarity.

    Semantic frames are generated once and role embeddings are
    cached once for efficient comparison.

    The final score remains bidirectional:

        target -> reference
        reference -> target
    """

    # --------------------------------------------------------
    # 1. BUILD MEANING REPRESENTATIONS
    # --------------------------------------------------------

    target_meaning = meaning_representation(
        target_text
    )

    reference_meaning = meaning_representation(
        reference_text
    )

    target_frames = target_meaning.get(
        "semantic_frames",
        []
    )

    reference_frames = reference_meaning.get(
        "semantic_frames",
        []
    )

    if not target_frames or not reference_frames:

        return {
            "meaning_score": 0.0,
            "target_frame_count": len(
                target_frames
            ),
            "reference_frame_count": len(
                reference_frames
            ),
            "matched_frames": 0,
            "frame_matches": []
        }

    # --------------------------------------------------------
    # 2. LOAD SENTENCE TRANSFORMER ONCE
    # --------------------------------------------------------

    model = get_sentence_transformer()

    # --------------------------------------------------------
    # 3. BUILD ONE GLOBAL EMBEDDING CACHE
    # --------------------------------------------------------

    all_frames = (
        target_frames
        +
        reference_frames
    )

    embedding_cache = _build_embedding_cache(
        model,
        all_frames
    )

    # --------------------------------------------------------
    # 4. TARGET -> REFERENCE
    # --------------------------------------------------------

    target_to_reference = []
    target_matches = []

    for target_frame in target_frames:

        score, matched_frame = _best_frame_match(
            embedding_cache,
            target_frame,
            reference_frames
        )

        target_to_reference.append(
            score
        )

        if matched_frame is not None:

            target_matches.append(
                {
                    "target_predicate":
                        target_frame.get(
                            "predicate"
                        ),

                    "reference_predicate":
                        matched_frame.get(
                            "predicate"
                        ),

                    "similarity":
                        round(
                            score * 100,
                            2
                        )
                }
            )

    # --------------------------------------------------------
    # 5. REFERENCE -> TARGET
    # --------------------------------------------------------

    reference_to_target = []

    for reference_frame in reference_frames:

        score, _ = _best_frame_match(
            embedding_cache,
            reference_frame,
            target_frames
        )

        reference_to_target.append(
            score
        )

    # --------------------------------------------------------
    # 6. BIDIRECTIONAL SCORE
    # --------------------------------------------------------

    if target_to_reference:

        forward_score = (
            sum(target_to_reference)
            /
            len(target_to_reference)
        )

    else:

        forward_score = 0.0

    if reference_to_target:

        backward_score = (
            sum(reference_to_target)
            /
            len(reference_to_target)
        )

    else:

        backward_score = 0.0

    meaning_score = (
        (forward_score + backward_score)
        /
        2.0
    ) * 100.0

    # --------------------------------------------------------
    # 7. RETURN RESULT
    # --------------------------------------------------------

    return {
        "meaning_score": round(
            max(
                0.0,
                min(
                    100.0,
                    meaning_score
                )
            ),
            2
        ),

        "target_frame_count": len(
            target_frames
        ),

        "reference_frame_count": len(
            reference_frames
        ),

        "matched_frames": len(
            target_matches
        ),

        "frame_matches": target_matches,

        "target_frames": target_frames,

        "reference_frames": reference_frames
    }


# ============================================================
# COMPLETE DOCUMENT ANALYSIS
# ============================================================

def analyze_document_pair(target_text, reference_text):
    """
    Run the complete ScholarShield NLP analysis
    for one target document and one reference document.
    """

    if not target_text or not reference_text:
        return {
            "success": False,
            "error": "Both target and reference documents are required."
        }

    try:

        # --------------------------------------------------
        # 1. PREPROCESSING
        # --------------------------------------------------

        target_preprocessed = preprocess_text(
            target_text
        )

        reference_preprocessed = preprocess_text(
            reference_text
        )

        # --------------------------------------------------
        # 2. LEXICAL SIMILARITY
        # --------------------------------------------------

        lexical_result = calculate_lexical_similarity(
            target_preprocessed["normalized_tokens"],
            reference_preprocessed["normalized_tokens"],
            target_preprocessed["lemmatized_tokens"],
            reference_preprocessed["lemmatized_tokens"]
        )

        # --------------------------------------------------
        # 3. SEMANTIC SIMILARITY
        # --------------------------------------------------

        semantic_result = analyze_semantic_similarity(
            target_text,
            reference_text
        )

        # --------------------------------------------------
        # 4. SYNTACTIC SIMILARITY
        # --------------------------------------------------

        syntactic_result = calculate_syntactic_similarity(
            target_text,
            reference_text
        )

        # --------------------------------------------------
        # 5. CONTEXT / WORD-SENSE SIMILARITY
        # --------------------------------------------------

        contextual_result = calculate_contextual_similarity(
            target_text,
            reference_text,
            target_preprocessed,
            reference_preprocessed
        )

        # --------------------------------------------------
        # 6. MEANING REPRESENTATION SIMILARITY
        # --------------------------------------------------

        meaning_result = calculate_meaning_similarity(
            target_text,
            reference_text
        )

        # --------------------------------------------------
        # 7. SIMILAR PASSAGES
        # --------------------------------------------------

        similar_passages = detect_similar_passages(
            target_text,
            reference_text
        )

        # --------------------------------------------------
        # 8. MULTI-LEVEL SCORE
        # --------------------------------------------------

        multi_level_result = generate_multi_level_result(
            lexical_score=lexical_result["lexical_score"],
            syntactic_score=syntactic_result["syntactic_score"],
            semantic_score=semantic_result[
                "semantic_similarity_score"
            ],
            contextual_score=contextual_result[
                "contextual_score"
            ],
            meaning_score=meaning_result[
                "meaning_score"
            ]
        )

        # --------------------------------------------------
        # 9. SIMILARITY EXPLANATION
        # --------------------------------------------------

        explanation = generate_similarity_explanation(
            lexical_result=lexical_result,
            semantic_result=semantic_result,
            syntactic_result=syntactic_result,
            contextual_result=contextual_result,
            meaning_result=meaning_result,
            multi_level_result=multi_level_result
        )

        # --------------------------------------------------
        # 10. FINAL RESULT
        # --------------------------------------------------

        return {
            "success": True,

            "preprocessing": {
                "target": target_preprocessed,
                "reference": reference_preprocessed
            },

            "lexical": lexical_result,

            "semantic": semantic_result,

            "syntactic": syntactic_result,

            "contextual": contextual_result,

            "meaning": meaning_result,

            "similar_passages": similar_passages,

            "multi_level": multi_level_result,

            "explanation": explanation
        }

    except Exception as error:

        import traceback

        print("\n" + "=" * 70)
        print("SCHOLARSHIELD NLP ENGINE ERROR")
        print("=" * 70)

        traceback.print_exc()

        print("=" * 70)

        return {
            "success": False,
            "error": str(error)
        }
