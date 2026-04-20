"""
Branch B – Policy & Scheme Detector
Extracts: new schemes, government initiatives, missions, programmes,
          portals, policy announcements, beneficiary info
"""

import re
from collections import defaultdict

# ─────────────────────────────────────────────
# TRIGGER PHRASES
# ─────────────────────────────────────────────

LAUNCH_TRIGGERS = [
    r"i propose to (launch|introduce|set up|establish|create|announce|start)",
    r"i am pleased to (announce|inform|introduce|launch)",
    r"(a new|new) (scheme|initiative|mission|programme|program|portal|platform|fund|policy|framework|yojana|abhiyan|project)",
    r"will be (launched|established|set up|created|introduced|announced|operationalised)",
    r"has been (launched|established|set up|created|introduced|announced)",
    r"(government|govt|we) (will|shall|propose to|intend to) (launch|introduce|set up|establish|create)",
    r"(scheme|mission|programme|yojana|abhiyan) (for|to|will)",
    r"(launch|introduce|roll out|roll-out) (a|the|new)",
]

SCHEME_NAME_PATTERNS = [
    r"(?:PM|Pradhan Mantri|National|Rashtriya|Atal|Swachh|Digital|Jal|Ayushman|Ujjwala|Mudra|PMAY|PMGSY)\s+[A-Z][a-zA-Z\s]+(?:Yojana|Mission|Scheme|Programme|Abhiyan|Portal|Fund|Initiative)?",
    r"[A-Z][a-zA-Z]+\s+(?:Yojana|Mission|Scheme|Programme|Abhiyan|Portal|Fund|Initiative)",
]

CATEGORY_KEYWORDS = {
    "Agriculture":      ["farmer", "agriculture", "kisan", "crop", "irrigation", "fisheries"],
    "Education":        ["school", "education", "student", "learning", "skill", "training"],
    "Health":           ["health", "hospital", "medical", "nutrition", "ayushman", "medicine"],
    "Digital":          ["digital", "technology", "internet", "broadband", "startup", "fintech"],
    "Infrastructure":   ["road", "highway", "railway", "infrastructure", "construction"],
    "Social Welfare":   ["women", "child", "elderly", "tribal", "sc", "st", "obc", "welfare"],
    "Energy":           ["solar", "energy", "power", "renewable", "electricity"],
    "Housing":          ["housing", "house", "shelter", "home"],
    "Employment":       ["employment", "job", "livelihood", "skill", "apprentice"],
    "Environment":      ["environment", "climate", "green", "forest", "carbon"],
    "Finance":          ["credit", "loan", "bank", "insurance", "mudra", "finance"],
    "Trade":            ["export", "import", "trade", "commerce"],
}


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_policy_data(sentences: list[str]) -> dict:
    """
    Returns:
        schemes          : list of detected scheme/initiative sentences
        named_schemes    : list of specifically named schemes found
        by_category      : schemes grouped by category
        announcements    : general policy announcements
        beneficiaries    : sentences mentioning beneficiary counts
    """
    schemes       = _extract_schemes(sentences)
    named_schemes = _extract_named_schemes(sentences)
    announcements = _extract_announcements(sentences)
    beneficiaries = _extract_beneficiaries(sentences)
    by_category   = _group_by_category(schemes)

    return {
        "schemes":       schemes,
        "named_schemes": named_schemes,
        "by_category":   by_category,
        "announcements": announcements,
        "beneficiaries": beneficiaries,
        "total_count":   len(schemes),
    }


# ─────────────────────────────────────────────
# BRANCH B1 – SCHEME DETECTION
# ─────────────────────────────────────────────

def _extract_schemes(sentences: list[str]) -> list[dict]:
    results = []
    compiled = [re.compile(p, re.IGNORECASE) for p in LAUNCH_TRIGGERS]

    for sent in sentences:
        matched_triggers = [p.pattern for p in compiled if p.search(sent)]
        if matched_triggers:
            category = _detect_category(sent)
            results.append({
                "sentence":  sent,
                "category":  category,
                "triggers":  matched_triggers[:2],
                "priority":  _score_priority(sent),
            })

    # Sort by priority
    results.sort(key=lambda x: x["priority"], reverse=True)
    return results


# ─────────────────────────────────────────────
# BRANCH B2 – NAMED SCHEME EXTRACTION
# ─────────────────────────────────────────────

def _extract_named_schemes(sentences: list[str]) -> list[dict]:
    results = []
    full_text = " ".join(sentences)

    for pattern in SCHEME_NAME_PATTERNS:
        matches = re.findall(pattern, full_text)
        for match in matches:
            name = match.strip()
            if len(name) > 5:
                results.append({
                    "name":     name,
                    "category": _detect_category(name),
                })

    # Deduplicate
    seen = set()
    deduped = []
    for r in results:
        if r["name"] not in seen:
            seen.add(r["name"])
            deduped.append(r)
    return deduped


# ─────────────────────────────────────────────
# BRANCH B3 – GENERAL ANNOUNCEMENTS
# ─────────────────────────────────────────────

def _extract_announcements(sentences: list[str]) -> list[dict]:
    announcement_triggers = [
        r"(propose|announce|introduce|present|table)",
        r"(target|aim|objective|goal)\s+(is|of|to)",
        r"(increase|raise|enhance|strengthen|improve)\s+(?:the\s+)?(?:allocation|funding|support|capacity)",
        r"(reduce|cut|lower|decrease)\s+(?:the\s+)?(?:tax|duty|rate|burden)",
    ]
    compiled = [re.compile(p, re.IGNORECASE) for p in announcement_triggers]
    results  = []

    for sent in sentences:
        if any(p.search(sent) for p in compiled):
            results.append({
                "sentence": sent,
                "category": _detect_category(sent),
            })
    return results


# ─────────────────────────────────────────────
# BRANCH B4 – BENEFICIARY EXTRACTION
# ─────────────────────────────────────────────

def _extract_beneficiaries(sentences: list[str]) -> list[dict]:
    patterns = [
        r"(\d+(?:\.\d+)?\s*(?:lakh|crore|million|thousand|hundred)?\s*(?:families|households|farmers|students|women|persons|people|beneficiaries|workers|youth|children))",
        r"(benefit(?:ing|ted|s)?\s+(?:over\s+)?[\d,]+(?:\.\d+)?\s*(?:lakh|crore|million)?)",
    ]
    results = []
    for sent in sentences:
        for pat in patterns:
            matches = re.findall(pat, sent, re.IGNORECASE)
            for m in matches:
                results.append({
                    "beneficiary_text": m.strip(),
                    "sentence":         sent,
                })
    return results


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "General"


def _group_by_category(schemes: list[dict]) -> dict:
    grouped = defaultdict(list)
    for s in schemes:
        grouped[s["category"]].append(s["sentence"])
    return dict(grouped)


def _score_priority(sentence: str) -> int:
    score = 0
    high_priority = ["crore", "lakh", "scheme", "mission", "yojana", "launch", "new", "propose"]
    for word in high_priority:
        if word in sentence.lower():
            score += 1
    return score
