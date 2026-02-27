"""OCR fallback for scanned or image-based PDFs."""
import io
import pytesseract
from PIL import Image
import pdfplumber

def extract_text_with_ocr(file) -> str:
    """
    Convert each PDF page to an image and run Tesseract OCR.
    Args:
        file: FileStorage or file-like object.
    Returns:
        Extracted text string.
    """
    try:
        data = file.read() if hasattr(file, "read") else open(file, "rb").read()
        text_parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                img = page.to_image(resolution=200).original
                text = pytesseract.image_to_string(img)
                text_parts.append(text)
        return "\n".join(text_parts)
    except Exception as e:
        print(f"[ocr_handler] Error: {e}")
        return ""
