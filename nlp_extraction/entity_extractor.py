"""
Extract personal entities (name, email, phone) from resume text.
Uses regex for reliable extraction without requiring a trained NER model.
"""
import re

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE_RE = re.compile(r"(?:\+?\d[\s.-]?){7,14}\d")

def extract_entities(text: str) -> dict:
    """
    Returns:
        {
          "name":  str or "",
          "email": str or "",
          "phone": str or "",
        }
    """
    email = ""
    match = EMAIL_RE.search(text)
    if match:
        email = match.group()

    phone = ""
    match = PHONE_RE.search(text)
    if match:
        phone = match.group().strip()

    name = _extract_name(text)

    return {"name": name, "email": email, "phone": phone}


def _extract_name(text: str) -> str:
    """
    Heuristic: the first non-empty line that is title-cased and
    does not look like a section header is likely the candidate name.
    """
    skip_words = {"resume", "curriculum", "vitae", "cv", "profile", "summary"}
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) > 60 or len(line) < 3:
            continue
        if line.lower() in skip_words:
            continue
        words = line.split()
        if all(w[0].isupper() for w in words if w.isalpha()):
            return line
    return ""
