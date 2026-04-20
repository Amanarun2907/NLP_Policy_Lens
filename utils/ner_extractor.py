"""
Named Entity Recognition (NER) Module — Fast Rule-Based
Uses lightweight regex + keyword matching for speed.
spaCy is only used when explicitly needed (named entity tab).
"""

import re
from collections import defaultdict

# ── Pre-compiled patterns ───────────────────────────────────────────────────
SECTORS = [
    "agriculture", "education", "health", "defence", "infrastructure",
    "railways", "roads", "highways", "energy", "power", "water",
    "housing", "urban development", "rural development", "finance",
    "banking", "insurance", "technology", "digital", "space", "science",
    "research", "environment", "climate", "social welfare", "women",
    "child", "msme", "startup", "export", "import", "trade",
    "petroleum", "gas", "mining", "steel", "textiles", "pharma",
    "tourism", "sports", "culture", "skill development", "employment",
]

FISCAL_KEYWORDS = [
    "fiscal deficit", "revenue deficit", "primary deficit",
    "capital expenditure", "revenue expenditure", "gdp",
    "gross domestic product", "inflation", "cpi", "wpi",
    "borrowing", "disinvestment", "tax revenue", "non-tax revenue",
    "budget estimate", "revised estimate",
]

POLICY_TRIGGERS = [
    "i propose", "i am pleased", "government will", "government proposes",
    "we will launch", "we will establish", "new scheme", "new initiative",
    "a new", "will be set up", "will be established", "will be launched",
    "has been announced", "is being launched", "scheme for", "mission for",
    "programme for", "yojana", "abhiyan", "mission", "portal",
]

TAX_TRIGGERS = [
    "income tax", "corporate tax", "gst", "customs duty", "excise duty",
    "surcharge", "cess", "rebate", "exemption", "deduction",
    "tax slab", "tax rate", "tax relief", "tax benefit",
    "section 80", "section 87", "tds", "tcs", "capital gains",
    "long term", "short term", "tax free", "tax exempt",
]

# Pre-compiled sets for O(1) lookup
_SECTOR_SET = set(SECTORS)
_FISCAL_SET = set(FISCAL_KEYWORDS)
_POLICY_SET = set(POLICY_TRIGGERS)
_TAX_SET    = set(TAX_TRIGGERS)

# Regex patterns
_MONEY_RE     = re.compile(
    r"(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|lac|crore|million|billion|thousand))*",
    re.IGNORECASE,
)
_PERCENT_RE   = re.compile(r"(\d+(?:\.\d+)?)\s*(?:percent|per cent|%)", re.IGNORECASE)
_FINANCIAL_RE = re.compile(r"[₹$]|crore|lakh|billion|million|rs\.", re.IGNORECASE)

# Regex for rule-based entity extraction (fast, no spaCy)
_ORG_RE  = re.compile(
    r"\b(Ministry of \w+|Department of \w+|Reserve Bank|RBI|SEBI|NITI Aayog"
    r"|Government of India|Supreme Court|High Court|Parliament|Lok Sabha|Rajya Sabha"
    r"|World Bank|IMF|WTO|ISRO|DRDO|NASSCOM|CII|FICCI|ASSOCHAM)\b",
    re.IGNORECASE,
)
_LOC_RE  = re.compile(
    r"\b(India|Delhi|Mumbai|Kolkata|Chennai|Bangalore|Hyderabad|Pune|Ahmedabad"
    r"|Rajasthan|Maharashtra|Gujarat|Karnataka|Tamil Nadu|Uttar Pradesh|Bihar"
    r"|West Bengal|Madhya Pradesh|Andhra Pradesh|Telangana|Kerala|Odisha"
    r"|Asia|Europe|USA|China|Pakistan|Bangladesh|Sri Lanka|Nepal)\b",
)
_DATE_RE = re.compile(
    r"\b(?:FY\s*\d{2,4}[-–]?\d{0,4}|20\d{2}[-–]\d{2,4}|20\d{2}"
    r"|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_entities(sentences: list) -> dict:
    """
    Fast rule-based entity extraction — no spaCy overhead.
    Processes all sentences in a single pass.
    """
    result = defaultdict(list)
    orgs_seen  = set()
    locs_seen  = set()
    dates_seen = set()

    for sent in sentences:
        sent_lower = sent.lower()

        # Money
        for m in _MONEY_RE.findall(sent):
            result["money"].append({"text": m.strip(), "sentence": sent})

        # Percentages
        for p in _PERCENT_RE.findall(sent):
            result["percentages"].append({"text": p + "%", "sentence": sent})

        # Organizations (rule-based)
        for m in _ORG_RE.findall(sent):
            if m not in orgs_seen:
                orgs_seen.add(m)
                result["organizations"].append(m)

        # Locations (rule-based)
        for m in _LOC_RE.findall(sent):
            if m not in locs_seen:
                locs_seen.add(m)
                result["locations"].append(m)

        # Dates
        for d in _DATE_RE.findall(sent):
            if d not in dates_seen:
                dates_seen.add(d)
                result["dates"].append(d)

        # Sectors
        for sector in _SECTOR_SET:
            if sector in sent_lower:
                result["sectors"].append({"sector": sector.title(), "sentence": sent})
                break

        # Fiscal terms
        for term in _FISCAL_SET:
            if term in sent_lower:
                result["fiscal_terms"].append({"term": term.title(), "sentence": sent})
                break

    return dict(result)


def extract_entities_spacy(sentences: list) -> dict:
    """
    Full spaCy NER — only called when user views the Entities tab.
    Lazy-loads spaCy to avoid startup cost.
    """
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm", disable=["lemmatizer"])
        except OSError:
            import subprocess, sys
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=False)
            nlp = spacy.load("en_core_web_sm", disable=["lemmatizer"])

        result = defaultdict(list)
        # Only process first 200 sentences for speed
        for sent, doc in zip(sentences[:200], nlp.pipe(sentences[:200], batch_size=64)):
            for ent in doc.ents:
                label = ent.label_
                text  = ent.text.strip()
                if label == "MONEY":
                    result["money"].append({"text": text, "sentence": sent})
                elif label == "ORG":
                    result["organizations"].append(text)
                elif label in ("GPE", "LOC"):
                    result["locations"].append(text)
                elif label == "DATE":
                    result["dates"].append(text)
                elif label == "PERCENT":
                    result["percentages"].append({"text": text, "sentence": sent})

        result["organizations"] = list(set(result["organizations"]))
        result["locations"]     = list(set(result["locations"]))
        result["dates"]         = list(set(result["dates"]))
        return dict(result)

    except Exception:
        # Fallback to fast rule-based
        return extract_entities(sentences)


def tag_sentence(sentence: str) -> list:
    """Return tags for a single sentence using pre-compiled sets."""
    tags       = []
    sent_lower = sentence.lower()

    if any(t in sent_lower for t in _POLICY_SET):
        tags.append("POLICY")
    if any(t in sent_lower for t in _TAX_SET):
        tags.append("TAX")
    if any(t in sent_lower for t in _FISCAL_SET):
        tags.append("FISCAL")
    if any(s in sent_lower for s in _SECTOR_SET):
        tags.append("SECTOR")
    if _FINANCIAL_RE.search(sent_lower):
        tags.append("FINANCIAL")

    return tags if tags else ["OTHER"]


def extract_monetary_values(sentences: list) -> list:
    """Extract all monetary mentions with context."""
    results = []
    for sent in sentences:
        for m in _MONEY_RE.findall(sent):
            results.append({
                "value_text": m.strip(),
                "sentence":   sent,
                "tags":       tag_sentence(sent),
            })
    return results
