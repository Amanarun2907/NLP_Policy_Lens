"""
Sentence Segmentation Module — Fast
Uses regex-based splitting for speed. NLTK only as fallback.
"""

import re

# Pre-compiled patterns
_ABBREV_RE   = re.compile(r"\b(Rs|Dr|Mr|Mrs|Prof|Govt|Dept|No|Fig|approx|est|i\.e|e\.g|viz|etc)\.", re.IGNORECASE)
_SPLIT_RE    = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
_LETTER_RE   = re.compile(r"[a-zA-Z\u0900-\u097F]")
_NUMONLY_RE  = re.compile(r"^[\d\s.,;:\-()%₹]+$")
_HINDI_RE    = re.compile(r"[।.]\s+|\n")


def segment_sentences(text: str, language: str = "English") -> list:
    """
    Fast sentence segmentation. Capped at 800 sentences.
    """
    if not text or not text.strip():
        return []

    if language == "Hindi":
        sentences = _hindi(text)
    else:
        sentences = _english(text)

    result = [s.strip() for s in sentences if _is_valid(s)]
    return result[:800]


def segment_paragraphs(text: str) -> list:
    paras = re.split(r"\n{2,}", text)
    return [p.strip() for p in paras if p.strip()]


def _english(text: str) -> list:
    # Protect abbreviations
    protected = _ABBREV_RE.sub(lambda m: m.group(0).replace(".", "__DOT__"), text)

    # Try NLTK first (accurate), fall back to regex (fast)
    try:
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(protected, language="english")
    except Exception:
        sentences = _SPLIT_RE.split(protected)

    return [s.replace("__DOT__", ".") for s in sentences]


def _hindi(text: str) -> list:
    return _HINDI_RE.split(text)


def _is_valid(s: str) -> bool:
    s = s.strip()
    if len(s) < 15:
        return False
    if not _LETTER_RE.search(s):
        return False
    if _NUMONLY_RE.fullmatch(s):
        return False
    return True
