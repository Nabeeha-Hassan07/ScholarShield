
import os
import re
import uuid
from pathlib import Path


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

# Resolve storage relative to the project root, not the terminal's
# current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORAGE_DIRECTORY = PROJECT_ROOT / "storage" / "documents"


def validate_file(uploaded_file):
    """
    Validate an uploaded document's presence, size, and extension.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file selected."

    filename = getattr(uploaded_file, "name", None)

    if not isinstance(filename, str) or not filename.strip():
        return False, "Invalid filename."

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Unsupported file type."

    try:
        file_size = getattr(uploaded_file, "size", None)

        if file_size is None:
            if hasattr(uploaded_file, "getbuffer"):
                file_size = len(uploaded_file.getbuffer())
            else:
                return False, "Unable to determine file size."

        if file_size <= 0:
            return False, "The uploaded file is empty."

        if file_size > MAX_FILE_SIZE:
            return False, "File size exceeds the 10 MB limit."

    except (OSError, ValueError, TypeError):
        return False, "Unable to validate the uploaded file."

    return True, ""


def count_sentences(text):
    """
    Estimate sentence count using sentence-ending punctuation.

    This lightweight heuristic is suitable for document metadata,
    but it is not a full linguistic sentence-boundary detector.
    """
    if not isinstance(text, str) or not text.strip():
        return 0

    # Count punctuation runs followed by whitespace or end of text.
    # Avoids counting decimal points such as the one in 3.14.
    sentence_endings = re.findall(r"[.!?]+(?=\s|$)", text.strip())

    return len(sentence_endings)


def save_uploaded_file(uploaded_file):
    """
    Save an uploaded document using a unique, sanitized filename.

    Returns:
        str: Absolute path to the saved file.
    """
    if uploaded_file is None:
        raise ValueError("No file selected.")

    original_name = getattr(uploaded_file, "name", None)

    if not isinstance(original_name, str) or not original_name.strip():
        raise ValueError("Invalid filename.")

    # Keep only the filename, never any supplied directory components.
    safe_name = Path(original_name.replace("\\", "/")).name

    # Replace unsafe characters while preserving ordinary filenames.
    safe_name = re.sub(r"[^\w.-]", "_", safe_name, flags=re.UNICODE)
    safe_name = safe_name.strip(".")

    if not safe_name or safe_name in {".", ".."}:
        raise ValueError("Invalid filename.")

    if not hasattr(uploaded_file, "getbuffer"):
        raise ValueError("Unsupported uploaded-file object.")

    file_data = uploaded_file.getbuffer()

    if len(file_data) == 0:
        raise ValueError("The uploaded file is empty.")

    STORAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = STORAGE_DIRECTORY / unique_filename

    with open(file_path, "wb") as file:
        file.write(file_data)

    return str(file_path)