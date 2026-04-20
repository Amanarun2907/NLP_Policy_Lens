"""
PDF Extraction Module
Handles: pdfplumber (primary), PyPDF2 (fallback), pytesseract (scanned PDFs)
Supports: English and Hindi documents
"""

import pdfplumber
import PyPDF2
import pytesseract
from PIL import Image
from langdetect import detect
import io
import re
import os


# ─────────────────────────────────────────────
# MAIN EXTRACTOR
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str, language: str = "English") -> dict:
    """
    Extract full text from a PDF file.
    Returns a dict with:
        - full_text     : complete raw text
        - pages         : list of per-page text
        - page_count    : total pages
        - detected_lang : auto-detected language
        - method        : extraction method used
    """
    result = {
        "full_text": "",
        "pages": [],
        "page_count": 0,
        "detected_lang": language,
        "method": "pdfplumber",
    }

    # Try pdfplumber first (best for structured PDFs)
    try:
        pages, full_text = _extract_pdfplumber(pdf_path)
        if full_text.strip():
            result["pages"]      = pages
            result["full_text"]  = full_text
            result["page_count"] = len(pages)
            result["method"]     = "pdfplumber"
            result["detected_lang"] = _detect_language(full_text, language)
            return result
    except Exception:
        pass

    # Fallback: PyPDF2
    try:
        pages, full_text = _extract_pypdf2(pdf_path)
        if full_text.strip():
            result["pages"]      = pages
            result["full_text"]  = full_text
            result["page_count"] = len(pages)
            result["method"]     = "PyPDF2"
            result["detected_lang"] = _detect_language(full_text, language)
            return result
    except Exception:
        pass

    # Last resort: OCR via pytesseract (scanned PDFs)
    try:
        pages, full_text = _extract_ocr(pdf_path, language)
        result["pages"]      = pages
        result["full_text"]  = full_text
        result["page_count"] = len(pages)
        result["method"]     = "OCR (pytesseract)"
        result["detected_lang"] = _detect_language(full_text, language)
    except Exception as e:
        result["full_text"] = ""
        result["method"]    = f"Failed: {str(e)}"

    return result


# ─────────────────────────────────────────────
# EXTRACTION METHODS
# ─────────────────────────────────────────────

def _extract_pdfplumber(pdf_path: str):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    full_text = "\n".join(pages)
    return pages, full_text


def _extract_pypdf2(pdf_path: str):
    pages = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
    full_text = "\n".join(pages)
    return pages, full_text


def _extract_ocr(pdf_path: str, language: str = "English"):
    """Convert PDF pages to images and run OCR."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError("PyMuPDF (fitz) required for OCR. Run: pip install pymupdf")

    lang_code = "hin+eng" if language == "Hindi" else "eng"
    pages = []

    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix  = page.get_pixmap(dpi=200)
        img  = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang=lang_code)
        pages.append(text)

    full_text = "\n".join(pages)
    return pages, full_text


# ─────────────────────────────────────────────
# LANGUAGE DETECTION
# ─────────────────────────────────────────────

def _detect_language(text: str, user_selected: str) -> str:
    """Auto-detect language; fall back to user selection."""
    try:
        sample = text[:2000]
        code   = detect(sample)
        if code == "hi":
            return "Hindi"
        return "English"
    except Exception:
        return user_selected
