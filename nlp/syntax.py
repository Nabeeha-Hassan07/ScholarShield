import spacy


# ---------------------------------------------------------
# LOAD SPACY MODEL
# ---------------------------------------------------------

nlp = spacy.load("en_core_web_sm")


# ---------------------------------------------------------
# SYNTAX ANALYSIS
# ---------------------------------------------------------

def analyze_syntax(text):
    """
    Perform syntactic and dependency analysis on text.

    Returns sentence-level syntactic information including:
    - tokens
    - POS tags
    - dependency relations
    - syntactic heads
    - named entities
    """

    if not text:
        return {
            "sentences": [],
            "entities": []
        }

    doc = nlp(text)

    sentences = []

    for sentence in doc.sents:

        sentence_tokens = []

        for token in sentence:

            if token.is_space:
                continue

            sentence_tokens.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dependency": token.dep_,
                "head": token.head.text,
                "is_stop": token.is_stop,
                "is_punctuation": token.is_punct
            })

        sentences.append({
            "text": sentence.text,
            "tokens": sentence_tokens
        })

    entities = []

    for entity in doc.ents:

        entities.append({
            "text": entity.text,
            "label": entity.label_,
            "description": spacy.explain(entity.label_)
        })

    return {
        "sentences": sentences,
        "entities": entities
    }


# ---------------------------------------------------------
# DEPENDENCY RELATION EXTRACTION
# ---------------------------------------------------------

def extract_dependencies(text):
    """
    Extract dependency relationships from the document.
    """

    if not text:
        return []

    doc = nlp(text)

    dependencies = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        dependencies.append({
            "word": token.text,
            "head": token.head.text,
            "dependency": token.dep_,
            "pos": token.pos_
        })

    return dependencies


# ---------------------------------------------------------
# SYNTAX SUMMARY
# ---------------------------------------------------------

def syntax_summary(syntax_result):
    """
    Generate basic syntactic statistics.
    """

    sentences = syntax_result.get("sentences", [])
    entities = syntax_result.get("entities", [])

    token_count = 0
    dependency_distribution = {}
    pos_distribution = {}

    for sentence in sentences:

        for token in sentence["tokens"]:

            if token["is_punctuation"]:
                continue

            token_count += 1

            dependency = token["dependency"]
            dependency_distribution[dependency] = (
                dependency_distribution.get(dependency, 0) + 1
            )

            pos = token["pos"]
            pos_distribution[pos] = (
                pos_distribution.get(pos, 0) + 1
            )

    return {
        "sentence_count": len(sentences),
        "token_count": token_count,
        "entity_count": len(entities),
        "dependency_distribution": dependency_distribution,
        "pos_distribution": pos_distribution
    }