
import re

import pymupdf


# Known ScholarShield test-document headers and footers.
TEST_PAGE_PATTERNS = [
    re.compile(
        r"^\**ScholarShield Targeted NLP Test\**\s*"
        r"(?:\|\s*)?Page\s+\d+\**$",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"^\**ScholarShield NLP Test Document\**\s*"
        r"(?:\|\s*)?Page\s+\d+\**$",
        flags=re.IGNORECASE,
    ),
]

# Metadata used only by the synthetic NLP test documents.
TEST_METADATA_PATTERNS = [
    re.compile(r"^Test\s+focus\s*:", flags=re.IGNORECASE),
    re.compile(r"^Test\s+keywords\s*:", flags=re.IGNORECASE),
]


def clean_pdf_text(text):
    """
    Remove known ScholarShield synthetic-test headers,
    footers, and metadata before NLP processing.

    Preserve all other non-empty lines.
    """
    if not text:
        return ""

    cleaned_lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove only recognized test-document page headers/footers.
        if any(pattern.fullmatch(line) for pattern in TEST_PAGE_PATTERNS):
            continue

        # Remove known synthetic-test metadata.
        if any(pattern.match(line) for pattern in TEST_METADATA_PATTERNS):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def extract_pdf_text(uploaded_file):
    """
    Extract text from an uploaded PDF and clean known test metadata.

    Args:
        uploaded_file: A Streamlit UploadedFile or compatible
                       binary file-like object.

    Returns:
        str: Extracted and cleaned PDF text.

    Raises:
        ValueError: If the PDF is empty or invalid.
    """
    if hasattr(uploaded_file, "getvalue"):
        pdf_bytes = uploaded_file.getvalue()
    else:
        pdf_bytes = uploaded_file.read()

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf_document:
            extracted_pages = []

            for page in pdf_document:
                page_text = page.get_text()

                if page_text and page_text.strip():
                    extracted_pages.append(page_text)

    except Exception as exc:
        raise ValueError(
            "Unable to read this PDF. Please upload a valid PDF file."
        ) from exc

    extracted_text = "\n".join(extracted_pages)

    return clean_pdf_text(extracted_text)