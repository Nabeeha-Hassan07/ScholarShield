import re
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ---------------------------------------------------------
# NLTK RESOURCE SETUP
# ---------------------------------------------------------

def download_nltk_resources():
    """
    Download the NLTK resources required by ScholarShield.
    """

    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4")
    ]

    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


download_nltk_resources()


# ---------------------------------------------------------
# INITIALIZE NLP COMPONENTS
# ---------------------------------------------------------

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------

def clean_text(text):
    """
    Clean extracted document text.

    Operations:
    - Convert input to string
    - Normalize line breaks
    - Remove excessive whitespace
    - Preserve meaningful punctuation
    """

    if not text:
        return ""

    text = str(text)

    # Normalize different types of line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Replace multiple newlines with a single space
    text = re.sub(r"\n+", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------
# SENTENCE SEGMENTATION
# ---------------------------------------------------------

def split_sentences(text):
    """
    Divide document text into individual sentences.
    """

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    return sent_tokenize(cleaned_text)


# ---------------------------------------------------------
# TOKENIZATION
# ---------------------------------------------------------

def tokenize_text(text):
    """
    Tokenize text into individual word/punctuation tokens.
    """

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    return word_tokenize(cleaned_text)


# ---------------------------------------------------------
# NORMALIZED TOKENS
# ---------------------------------------------------------

def normalize_tokens(tokens):
    """
    Normalize tokens by:
    - converting to lowercase
    - retaining alphabetic words
    - removing stopwords
    """

    normalized = []

    for token in tokens:

        token = token.lower()

        # Keep alphabetic words only
        if not token.isalpha():
            continue

        # Remove common stopwords
        if token in STOP_WORDS:
            continue

        normalized.append(token)

    return normalized


# ---------------------------------------------------------
# LEMMATIZATION
# ---------------------------------------------------------

def lemmatize_tokens(tokens):
    """
    Convert normalized tokens to their base dictionary forms.
    """

    return [
        LEMMATIZER.lemmatize(token)
        for token in tokens
    ]


# ---------------------------------------------------------
# COMPLETE PREPROCESSING PIPELINE
# ---------------------------------------------------------

def preprocess_text(text):
    """
    Run the complete ScholarShield preprocessing pipeline.

    Returns a structured dictionary containing:
    - cleaned text
    - sentences
    - original tokens
    - normalized tokens
    - lemmatized tokens
    """

    cleaned_text = clean_text(text)

    sentences = split_sentences(cleaned_text)

    tokens = tokenize_text(cleaned_text)

    normalized_tokens = normalize_tokens(tokens)

    lemmatized_tokens = lemmatize_tokens(normalized_tokens)

    return {
        "original_text": text,
        "cleaned_text": cleaned_text,
        "sentences": sentences,
        "tokens": tokens,
        "normalized_tokens": normalized_tokens,
        "lemmatized_tokens": lemmatized_tokens,
        "sentence_count": len(sentences),
        "token_count": len(tokens),
        "normalized_token_count": len(normalized_tokens)
    }