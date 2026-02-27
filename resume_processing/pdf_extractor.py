"""Extract raw text from a PDF file using pdfplumber."""
import pdfplumber
import io

def extract_text_from_pdf(file) -> str:
    """
    Args:
        file: FileStorage object or file-like object.
    Returns:
        Concatenated text from all pages, or empty string on failure.
    """
    try:
        if hasattr(file, "read"):
            data = file.read()
            file.seek(0)
        else:
            with open(file, "rb") as f:
                data = f.read()

        text_parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        print(f"[pdf_extractor] Error: {e}")
        return ""
