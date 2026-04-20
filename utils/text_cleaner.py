"""
Text Cleaning & Preprocessing Module
Handles: noise removal, line merging, deduplication
Supports: English and Hindi
"""

import re
import unicodedata


# ─────────────────────────────────────────────
# MASTER CLEANER
# ─────────────────────────────────────────────

def clean_text(raw_text: str, language: str = "English") -> str:
    """
    Full cleaning pipeline:
    1. Unicode normalization
    2. Remove headers / footers / page numbers
    3. Fix broken lines
    4. Remove special noise characters
    5. Collapse extra whitespace
    6. Remove duplicate lines
    """
    text = _normalize_unicode(raw_text)
    text = _remove_page_artifacts(text)
    text = _fix_broken_lines(text)
    text = _remove_noise(text, language)
    text = _collapse_whitespace(text)
    text = _remove_duplicate_lines(text)
    return text.strip()


# ─────────────────────────────────────────────
# STEP 1 – Unicode Normalization
# ─────────────────────────────────────────────

def _normalize_unicode(text: str) -> str:
    # Normalize to NFC (important for Hindi Devanagari)
    text = unicodedata.normalize("NFC", text)
    # Replace common ligature / encoding artifacts
    replacements = {
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u00a0": " ", "\u200b": "",
        "\ufeff": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


# ─────────────────────────────────────────────
# STEP 2 – Remove Page Artifacts
# ─────────────────────────────────────────────

def _remove_page_artifacts(text: str) -> str:
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()

        # Skip pure page numbers  e.g.  "1", "- 2 -", "Page 3"
        if re.fullmatch(r"[-\s]*\d{1,4}[-\s]*", stripped):
            continue
        if re.match(r"(?i)^page\s+\d+", stripped):
            continue

        # Skip very short repeated header/footer lines (≤ 6 words, all caps)
        words = stripped.split()
        if len(words) <= 6 and stripped.isupper() and len(stripped) < 60:
            continue

        # Skip lines that are only dashes / underscores / dots
        if re.fullmatch(r"[-_=.•*~\s]+", stripped):
            continue

        cleaned.append(line)
    return "\n".join(cleaned)


# ─────────────────────────────────────────────
# STEP 3 – Fix Broken Lines
# ─────────────────────────────────────────────

def _fix_broken_lines(text: str) -> str:
    """
    Merge lines that were broken mid-sentence.
    A line is considered broken if it does NOT end with
    sentence-ending punctuation.
    """
    lines  = text.split("\n")
    merged = []
    buffer = ""

    sentence_end = re.compile(r"[.!?।]\s*$")   # । is Hindi full stop

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append("")
            continue

        if buffer:
            buffer += " " + stripped
        else:
            buffer = stripped

        if sentence_end.search(stripped):
            merged.append(buffer.strip())
            buffer = ""

    if buffer:
        merged.append(buffer.strip())

    return "\n".join(merged)


# ─────────────────────────────────────────────
# STEP 4 – Remove Noise Characters
# ─────────────────────────────────────────────

def _remove_noise(text: str, language: str = "English") -> str:
    # Remove non-printable control characters (keep newlines)
    text = re.sub(r"[^\S\n]+", " ", text)          # multiple spaces → single
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", text)  # control chars

    if language == "English":
        # Keep: letters, digits, common punctuation, currency symbols
        text = re.sub(r"[^\w\s.,;:!?()\-\'\"/₹%@#&+]", " ", text)
    else:
        # Hindi: keep Devanagari range + English + punctuation + ₹
        text = re.sub(
            r"[^\u0900-\u097F\w\s.,;:!?()\-\'\"/₹%@#&+।]", " ", text
        )

    return text


# ─────────────────────────────────────────────
# STEP 5 – Collapse Whitespace
# ─────────────────────────────────────────────

def _collapse_whitespace(text: str) -> str:
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


# ─────────────────────────────────────────────
# STEP 6 – Remove Duplicate Lines
# ─────────────────────────────────────────────

def _remove_duplicate_lines(text: str) -> str:
    lines = text.split("\n")
    seen  = set()
    out   = []
    for line in lines:
        key = line.strip().lower()
        if key in seen and len(key) > 20:
            continue
        seen.add(key)
        out.append(line)
    return "\n".join(out)
