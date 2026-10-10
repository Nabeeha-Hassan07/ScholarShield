from sklearn.metrics.pairwise import cosine_similarity

from nlp.model_loader import (
    MODEL_NAME,
    get_sentence_transformer
)


def generate_embedding(text):
    if not text or not str(text).strip():
        return None

    model = get_sentence_transformer()

    embedding = model.encode(text)

    return embedding


def calculate_semantic_similarity(text_a, text_b):
    """
    Calculate semantic similarity between two pieces of text.
    Returns a percentage from 0 to 100.
    """
    if not text_a or not text_b:
        return 0.0

    embedding_a = generate_embedding(text_a)
    embedding_b = generate_embedding(text_b)

    similarity = cosine_similarity(
        [embedding_a],
        [embedding_b]
    )[0][0]

    # Convert cosine similarity to percentage
    score = similarity * 100

    # Keep score within 0-100
    score = max(0.0, min(100.0, score))

    return round(score, 2)


def analyze_semantic_similarity(text_a, text_b):
    """
    Perform semantic similarity analysis and return
    structured results.
    """
    score = calculate_semantic_similarity(text_a, text_b)

    return {
        "model": MODEL_NAME,
        "semantic_similarity_score": score
    }