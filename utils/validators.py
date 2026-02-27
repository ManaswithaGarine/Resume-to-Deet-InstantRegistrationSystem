"""Input validation helpers."""

MAX_SIZE_MB = 10

def validate_pdf(file) -> tuple[bool, str]:
    """
    Validates that the uploaded file is a PDF and within size limits.
    Returns (True, "") on success or (False, error_message) on failure.
    """
    filename = getattr(file, "filename", "") or ""
    if not filename.lower().endswith(".pdf"):
        return False, "Only PDF files are supported."

    file.seek(0, 2)          # seek to end
    size = file.tell()
    file.seek(0)             # reset

    if size > MAX_SIZE_MB * 1024 * 1024:
        return False, f"File exceeds {MAX_SIZE_MB} MB limit."

    if size == 0:
        return False, "Uploaded file is empty."

    return True, ""
