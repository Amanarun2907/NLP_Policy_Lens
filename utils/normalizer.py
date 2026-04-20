"""
Text Normalization Module
Converts all currency / number formats into a unified numeric value.

Handles:
  ₹2 lakh crore        → 200000000000  (2e11)
  Rs. 2,00,000 crore   → 2000000000000
  two lakh crore       → 200000000000
  50,000 crore         → 500000000000
  $5 billion           → 5000000000
  15%                  → 15.0  (percent)
"""

import re


# ─────────────────────────────────────────────
# WORD → NUMBER MAP  (English + Hindi transliteration)
# ─────────────────────────────────────────────

WORD_NUM = {
    # English
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
    # Hindi transliteration
    "ek": 1, "do": 2, "teen": 3, "char": 4, "paanch": 5,
    "chhe": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
}

MULTIPLIER = {
    "hundred":      100,
    "thousand":     1_000,
    "lakh":         100_000,
    "lac":          100_000,
    "million":      1_000_000,
    "crore":        10_000_000,
    "billion":      1_000_000_000,
    "trillion":     1_000_000_000_000,
    # Hindi
    "hajar":        1_000,
    "hazaar":       1_000,
}


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def normalize_text(text: str) -> str:
    """
    Replace all currency / number expressions in text
    with a canonical  ₹<value>  or  <value>  token.
    """
    text = _normalize_written_numbers(text)
    text = _normalize_numeric_currency(text)
    text = _normalize_plain_numbers(text)
    return text


def parse_amount(expr: str) -> float:
    """
    Parse a single amount expression and return float value.
    e.g.  "2 lakh crore"  →  2e11
    """
    expr = expr.lower().strip()
    expr = re.sub(r"[₹$rs.,]", "", expr)
    expr = expr.strip()

    # Try direct float first
    try:
        return float(expr.replace(",", ""))
    except ValueError:
        pass

    return _parse_word_number(expr)


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

def _normalize_numeric_currency(text: str) -> str:
    """
    Patterns like:  ₹1.5 lakh crore  /  Rs 50,000 crore  /  $5 billion
    → ₹<normalized_number>
    """
    pattern = re.compile(
        r"(?:₹|Rs\.?|INR|USD|\$)\s*"
        r"([\d,]+(?:\.\d+)?)"
        r"(?:\s*(lakh|lac|crore|million|billion|trillion|thousand|hundred))?"
        r"(?:\s*(lakh|lac|crore|million|billion|trillion|thousand))?",
        re.IGNORECASE,
    )

    def replacer(m):
        num_str  = m.group(1).replace(",", "")
        unit1    = (m.group(2) or "").lower()
        unit2    = (m.group(3) or "").lower()
        try:
            value = float(num_str)
        except ValueError:
            return m.group(0)
        if unit1 in MULTIPLIER:
            value *= MULTIPLIER[unit1]
        if unit2 in MULTIPLIER:
            value *= MULTIPLIER[unit2]
        return f"₹{value:,.0f}"

    return pattern.sub(replacer, text)


def _normalize_written_numbers(text: str) -> str:
    """
    Patterns like:  two lakh crore  /  fifty thousand crore
    → ₹<value>
    """
    word_pat = "|".join(WORD_NUM.keys())
    mult_pat = "|".join(MULTIPLIER.keys())

    pattern = re.compile(
        rf"(?:(?:{word_pat})\s+)+(?:{mult_pat})(?:\s+(?:{mult_pat}))?",
        re.IGNORECASE,
    )

    def replacer(m):
        val = _parse_word_number(m.group(0))
        if val > 0:
            return f"₹{val:,.0f}"
        return m.group(0)

    return pattern.sub(replacer, text)


def _normalize_plain_numbers(text: str) -> str:
    """
    Normalize comma-separated numbers like 1,00,000 → 100000
    """
    pattern = re.compile(r"\b(\d{1,3}(?:,\d{2,3})+)\b")

    def replacer(m):
        return m.group(1).replace(",", "")

    return pattern.sub(replacer, text)


def _parse_word_number(expr: str) -> float:
    """
    Parse expressions like:
      'two lakh crore'      → 2 * 1e5 * 1e7 = 2e12
      'fifty thousand crore'→ 50 * 1e3 * 1e7 = 5e11
      'five hundred crore'  → 500 * 1e7 = 5e9
      '1.5 lakh crore'      → 1.5 * 1e5 * 1e7 = 1.5e12
    """
    tokens  = expr.lower().split()
    # collect numeric base then apply multipliers left-to-right
    segments = []   # list of floats after each multiplier
    current  = 0.0

    for token in tokens:
        clean = re.sub(r"[^a-z0-9.]", "", token)
        if not clean:
            continue
        # numeric literal
        try:
            current += float(clean)
            continue
        except ValueError:
            pass
        # word number
        if clean in WORD_NUM:
            current += WORD_NUM[clean]
            continue
        # multiplier
        if clean in MULTIPLIER:
            mult = MULTIPLIER[clean]
            if current == 0:
                current = 1.0
            current *= mult
            # if next multiplier is larger (e.g. lakh crore), keep accumulating
            # push to segments only when we hit a "terminal" large multiplier
            if mult >= 10_000_000:   # crore or above → push
                segments.append(current)
                current = 0.0
            # else keep current for chaining (e.g. fifty thousand → 50000)

    if current:
        segments.append(current)

    return sum(segments) if segments else 0.0
