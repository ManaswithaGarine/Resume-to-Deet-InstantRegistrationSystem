"""Clean and normalise raw extracted text."""
import re

def clean_text(text: str) -> str:
    """
    - Remove excessive whitespace and special characters.
    - Normalise unicode.
    - Collapse blank lines.
    """
    if not text:
        return ""
    # Normalise unicode
    text = text.encode("ascii", "ignore").decode("ascii")
    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # Collapse 3+ blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
