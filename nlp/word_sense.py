import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from sklearn.metrics.pairwise import cosine_similarity

from nlp.model_loader import get_sentence_transformer


def download_word_sense_resources():
    """Download resources required for Word Sense Analysis."""
    resources = [
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
        ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng")
    ]

    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


download_word_sense_resources()


def get_wordnet_pos(tag):
    """Convert an NLTK POS tag to a WordNet POS category."""
    if tag.startswith("J"):
        return wordnet.ADJ

    if tag.startswith("V"):
        return wordnet.VERB

    if tag.startswith("N"):
        return wordnet.NOUN

    if tag.startswith("R"):
        return wordnet.ADV

    return None


def get_target_word_pos(word, sentence):
    """Determine the grammatical POS of the target word."""
    if not word or not sentence:
        return None, None

    try:
        tokens = nltk.word_tokenize(sentence)
        tagged_tokens = pos_tag(tokens)
    except Exception:
        return None, None

    for token, tag in tagged_tokens:
        if token.lower() == word.lower():
            return get_wordnet_pos(tag), tag

    return None, None


def get_word_senses(word, pos=None):
    """Return possible WordNet senses for a word."""
    if not word:
        return []

    try:
        if pos:
            synsets = wordnet.synsets(
                word.lower(),
                pos=pos
            )
        else:
            synsets = wordnet.synsets(
                word.lower()
            )
    except Exception:
        return []

    senses = []

    for synset in synsets:
        senses.append({
            "synset": synset.name(),
            "definition": synset.definition(),
            "examples": synset.examples(),
            "pos": synset.pos()
        })

    return senses


def create_context(text, word):
    """Remove the target word so surrounding context drives WSD."""
    if not text:
        return ""

    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        tokens = text.split()

    context_tokens = [
        token
        for token in tokens
        if token.lower() != word.lower()
    ]

    return " ".join(context_tokens)


def calculate_sense_similarity(context, sense_definition):
    """
    Compare context with a WordNet sense definition.

    Returns the raw cosine similarity in the range [-1, 1].
    The raw value is intentionally preserved here; a cosine value
    of 0 must NOT become an artificial 50% confidence.
    """
    if not context or not sense_definition:
        return 0.0

    try:
        model = get_sentence_transformer()

        context_embedding = model.encode(context)
        sense_embedding = model.encode(sense_definition)

        similarity = cosine_similarity(
            [context_embedding],
            [sense_embedding]
        )[0][0]

        return float(similarity)

    except Exception:
        return 0.0


def _confidence_from_scores(best_score, second_score=None):
    """
    Convert WSD evidence into a confidence value in [0, 1].

    The best score measures absolute contextual compatibility.
    The margin between the best and second-best sense measures how
    decisively that sense wins. Both are required for high confidence.
    """
    # Convert cosine [-1, 1] to a bounded evidence score [0, 1].
    evidence = (float(best_score) + 1.0) / 2.0
    evidence = max(0.0, min(1.0, evidence))

    if second_score is None:
        margin = 1.0
    else:
        margin = float(best_score) - float(second_score)
        # A 0.20 cosine gap is treated as a strong decision.
        margin = max(0.0, min(1.0, margin / 0.20))

    # Absolute contextual evidence is more important than the margin,
    # but both are required to claim a reliable sense assignment.
    confidence = (
        (evidence * 0.70)
        +
        (margin * 0.30)
    )

    return max(0.0, min(1.0, confidence))


def rank_senses(word, sentence, top_n=3):
    """
    Rank WordNet senses according to contextual compatibility.

    The returned ``similarity`` field remains a percentage for
    compatibility with the existing UI. A new ``confidence`` field
    provides the normalized WSD confidence used by the contextual
    similarity engine.
    """
    if not word or not sentence:
        return []

    wordnet_pos, nltk_pos = get_target_word_pos(
        word,
        sentence
    )

    senses = get_word_senses(
        word,
        pos=wordnet_pos
    )

    if not senses:
        return []

    context = create_context(
        sentence,
        word
    )

    ranked_senses = []

    for sense in senses:
        raw_similarity = calculate_sense_similarity(
            context,
            sense["definition"]
        )

        ranked_senses.append({
            "synset": sense["synset"],
            "definition": sense["definition"],
            "examples": sense["examples"],
            "pos": sense["pos"],
            "similarity": round(
                raw_similarity * 100.0,
                2
            ),
            "raw_similarity": raw_similarity
        })

    ranked_senses.sort(
        key=lambda item: item["raw_similarity"],
        reverse=True
    )

    for index, item in enumerate(ranked_senses):
        second_score = None

        if index == 0 and len(ranked_senses) > 1:
            second_score = ranked_senses[1]["raw_similarity"]

        if index == 0:
            item["confidence"] = round(
                _confidence_from_scores(
                    item["raw_similarity"],
                    second_score
                ),
                4
            )
        else:
            item["confidence"] = 0.0

    return ranked_senses[:top_n]


def disambiguate_word(word, sentence):
    """Select the best contextual sense and expose its confidence."""
    if not word or not sentence:
        return None

    wordnet_pos, nltk_pos = get_target_word_pos(
        word,
        sentence
    )

    ranked_senses = rank_senses(
        word,
        sentence,
        top_n=3
    )

    if not ranked_senses:
        return {
            "word": word,
            "pos": nltk_pos,
            "sense": None,
            "definition": None,
            "similarity": 0.0,
            "confidence": 0.0
        }

    best_sense = ranked_senses[0]

    return {
        "word": word,
        "pos": nltk_pos,
        "sense": best_sense["synset"],
        "definition": best_sense["definition"],
        "similarity": best_sense["similarity"],
        "confidence": best_sense.get(
            "confidence",
            0.0
        )
    }


def analyze_word_context(word, sentence):
    """Perform complete Word Sense & Context Analysis."""
    wordnet_pos, nltk_pos = get_target_word_pos(
        word,
        sentence
    )

    context = create_context(
        sentence,
        word
    )

    all_senses = get_word_senses(
        word,
        pos=wordnet_pos
    )

    ranked_senses = rank_senses(
        word,
        sentence,
        top_n=3
    )

    selected_sense = None

    if ranked_senses:
        selected_sense = ranked_senses[0]

    return {
        "word": word,
        "pos": nltk_pos,
        "context": context,
        "sense_count": len(all_senses),
        "top_senses": ranked_senses,
        "selected_sense": selected_sense
    }
