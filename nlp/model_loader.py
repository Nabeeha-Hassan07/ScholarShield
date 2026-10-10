from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_MODEL = None


def get_sentence_transformer():
    """
    Load the Sentence Transformer model only once.

    The model is loaded from the local cache when available.
    If it is not cached (for example, on a fresh deployment),
    SentenceTransformer can download it normally.

    Subsequent calls reuse the already-loaded model.
    """

    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer(
            MODEL_NAME,
            local_files_only=False
        )

    return _MODEL