import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


# ---------------------------------------------------------
# NLTK RESOURCE SETUP
# ---------------------------------------------------------

def download_morphology_resources():
    resources = [
        ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
        ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4")
    ]

    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


download_morphology_resources()


# ---------------------------------------------------------
# INITIALIZE COMPONENTS
# ---------------------------------------------------------

LEMMATIZER = WordNetLemmatizer()


# ---------------------------------------------------------
# POS → WORDNET POS
# ---------------------------------------------------------

def get_wordnet_pos(tag):
    """
    Convert NLTK POS tags into WordNet-compatible tags.
    """

    if tag.startswith("J"):
        return wordnet.ADJ

    if tag.startswith("V"):
        return wordnet.VERB

    if tag.startswith("N"):
        return wordnet.NOUN

    if tag.startswith("R"):
        return wordnet.ADV

    return wordnet.NOUN


# ---------------------------------------------------------
# MORPHOLOGICAL ANALYSIS
# ---------------------------------------------------------

def analyze_morphology(tokens):
    """
    Perform morphological analysis on a list of tokens.

    Returns:
    - token
    - POS tag
    - WordNet POS
    - lemma
    """

    if not tokens:
        return []

    # Assign grammatical categories
    tagged_tokens = pos_tag(tokens)

    results = []

    for token, pos_tag_value in tagged_tokens:

        wordnet_pos = get_wordnet_pos(pos_tag_value)

        lemma = LEMMATIZER.lemmatize(
            token,
            pos=wordnet_pos
        )

        results.append({
            "token": token,
            "pos": pos_tag_value,
            "wordnet_pos": wordnet_pos,
            "lemma": lemma
        })

    return results


# ---------------------------------------------------------
# MORPHOLOGICAL SUMMARY
# ---------------------------------------------------------

def morphology_summary(morphology_results):
    """
    Generate basic morphological statistics.
    """

    if not morphology_results:
        return {
            "token_count": 0,
            "unique_lemmas": 0,
            "pos_distribution": {}
        }

    lemmas = set()
    pos_distribution = {}

    for item in morphology_results:

        lemmas.add(item["lemma"])

        pos = item["pos"]

        pos_distribution[pos] = (
            pos_distribution.get(pos, 0) + 1
        )

    return {
        "token_count": len(morphology_results),
        "unique_lemmas": len(lemmas),
        "pos_distribution": pos_distribution
    }