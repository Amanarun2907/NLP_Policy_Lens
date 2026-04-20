"""
Branch C – Tax Change Extractor
Extracts: income tax slabs, GST changes, customs duty, exemptions,
          rebates, surcharges, TDS/TCS, capital gains
"""

import re

# ─────────────────────────────────────────────
# TAX CATEGORY PATTERNS
# ─────────────────────────────────────────────

TAX_CATEGORIES = {
    "Income Tax": [
        r"income tax", r"personal income", r"individual tax",
        r"tax slab", r"tax rate", r"section 87a", r"rebate",
        r"basic exemption", r"standard deduction",
    ],
    "Corporate Tax": [
        r"corporate tax", r"company tax", r"domestic company",
        r"manufacturing company", r"base erosion",
    ],
    "GST": [
        r"\bgst\b", r"goods and services tax", r"igst", r"cgst", r"sgst",
        r"input tax credit", r"itc", r"gst rate", r"gst exemption",
    ],
    "Customs Duty": [
        r"customs duty", r"basic customs", r"import duty",
        r"countervailing duty", r"anti.dumping",
    ],
    "Excise Duty": [
        r"excise duty", r"central excise", r"cess",
    ],
    "Capital Gains": [
        r"capital gain", r"long.term capital", r"short.term capital",
        r"ltcg", r"stcg", r"securities transaction",
    ],
    "TDS / TCS": [
        r"\btds\b", r"\btcs\b", r"tax deducted at source",
        r"tax collected at source", r"withholding tax",
    ],
    "Surcharge & Cess": [
        r"surcharge", r"health.*cess", r"education.*cess",
        r"swachh bharat cess",
    ],
    "Exemption & Deduction": [
        r"exemption", r"deduction", r"section 80", r"section 10",
        r"tax.free", r"tax exempt", r"tax benefit", r"tax relief",
    ],
    "New Tax Regime": [
        r"new tax regime", r"old tax regime", r"optional regime",
        r"default regime",
    ],
}

CHANGE_INDICATORS = [
    r"(increased|raised|hiked|enhanced|revised upward)",
    r"(decreased|reduced|lowered|cut|revised downward)",
    r"(introduced|proposed|announced|notified|applicable)",
    r"(exempted|waived|abolished|removed|withdrawn)",
    r"(extended|continued|retained|maintained)",
    r"(new|revised|updated|modified|amended)",
]

AMOUNT_RE  = re.compile(
    r"(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|million|thousand))*"
    r"|\d+(?:\.\d+)?\s*(?:lakh|crore|million|thousand)",
    re.IGNORECASE,
)
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:percent|per cent|%)", re.IGNORECASE)
SLAB_RE    = re.compile(
    r"(?:income|salary|earning)s?\s+(?:up to|upto|between|above|exceeding)\s+"
    r"(?:₹|Rs\.?)?\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore)?",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_tax_data(sentences: list[str]) -> dict:
    """
    Returns:
        tax_changes    : all tax-related sentences with category + change type
        income_tax     : income tax specific changes
        gst_changes    : GST specific changes
        customs_changes: customs duty changes
        tax_slabs      : detected tax slab sentences
        exemptions     : exemption / deduction sentences
        summary_table  : compact summary per category
    """
    tax_changes     = _extract_all_tax_changes(sentences)
    income_tax      = [t for t in tax_changes if t["category"] == "Income Tax"]
    gst_changes     = [t for t in tax_changes if t["category"] == "GST"]
    customs_changes = [t for t in tax_changes if t["category"] == "Customs Duty"]
    exemptions      = [t for t in tax_changes if t["category"] == "Exemption & Deduction"]
    tax_slabs       = _extract_tax_slabs(sentences)
    summary_table   = _build_summary_table(tax_changes)

    return {
        "tax_changes":     tax_changes,
        "income_tax":      income_tax,
        "gst_changes":     gst_changes,
        "customs_changes": customs_changes,
        "exemptions":      exemptions,
        "tax_slabs":       tax_slabs,
        "summary_table":   summary_table,
        "total_count":     len(tax_changes),
    }


# ─────────────────────────────────────────────
# BRANCH C1 – ALL TAX CHANGES
# ─────────────────────────────────────────────

def _extract_all_tax_changes(sentences: list[str]) -> list[dict]:
    results  = []
    compiled_changes = [re.compile(p, re.IGNORECASE) for p in CHANGE_INDICATORS]

    for sent in sentences:
        sent_lower = sent.lower()
        for category, patterns in TAX_CATEGORIES.items():
            if any(re.search(p, sent_lower) for p in patterns):
                change_type = _detect_change_type(sent, compiled_changes)
                amounts     = AMOUNT_RE.findall(sent)
                percents    = PERCENT_RE.findall(sent)

                results.append({
                    "category":    category,
                    "change_type": change_type,
                    "amount":      amounts[0].strip() if amounts else None,
                    "percent":     percents[0] if percents else None,
                    "sentence":    sent,
                    "priority":    _tax_priority(sent),
                })

    # Deduplicate
    seen = set()
    deduped = []
    for r in results:
        key = (r["category"], r["sentence"][:60])
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    deduped.sort(key=lambda x: x["priority"], reverse=True)
    return deduped


# ─────────────────────────────────────────────
# BRANCH C2 – TAX SLABS
# ─────────────────────────────────────────────

def _extract_tax_slabs(sentences: list[str]) -> list[dict]:
    results = []
    for sent in sentences:
        slab_matches = SLAB_RE.findall(sent)
        percents     = PERCENT_RE.findall(sent)
        if slab_matches or ("nil" in sent.lower() and "income" in sent.lower()):
            results.append({
                "slab_text": slab_matches[0] if slab_matches else sent[:80],
                "rate":      percents[0] if percents else "Nil",
                "sentence":  sent,
            })
    return results


# ─────────────────────────────────────────────
# BRANCH C3 – SUMMARY TABLE
# ─────────────────────────────────────────────

def _build_summary_table(tax_changes: list[dict]) -> list[dict]:
    from collections import Counter
    cat_counts = Counter(t["category"] for t in tax_changes)
    table = []
    for cat, count in cat_counts.most_common():
        items = [t for t in tax_changes if t["category"] == cat]
        change_types = [t["change_type"] for t in items if t["change_type"] != "Mentioned"]
        table.append({
            "category":    cat,
            "count":       count,
            "change_types": list(set(change_types)),
        })
    return table


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _detect_change_type(sentence: str, compiled: list) -> str:
    sent_lower = sentence.lower()
    if re.search(r"increase|raise|hike|enhance|higher|more", sent_lower):
        return "Increased"
    if re.search(r"decrease|reduce|lower|cut|less|abolish|remove|waive", sent_lower):
        return "Reduced / Removed"
    if re.search(r"introduce|propose|new|launch|announce", sent_lower):
        return "Newly Introduced"
    if re.search(r"exempt|waive|nil|zero", sent_lower):
        return "Exempted"
    if re.search(r"extend|continue|retain|maintain", sent_lower):
        return "Continued"
    return "Mentioned"


def _tax_priority(sentence: str) -> int:
    score = 0
    high = ["crore", "lakh", "percent", "%", "slab", "exemption",
            "rebate", "surcharge", "gst", "income tax", "customs"]
    for word in high:
        if word in sentence.lower():
            score += 1
    return score
