
def extract_txt_text(uploaded_file):

    file_bytes = uploaded_file.read()

    if not file_bytes:
        raise ValueError("The uploaded text file is empty.")

    try:
        return file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Unable to read this text file as UTF-8. "
            "Please upload a UTF-8 encoded .txt file."
        ) from exc