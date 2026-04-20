"""
Phase 5 – Financial Document Extractor
Handles: Annual Reports, Balance Sheets, Company Filings, Prospectus
Extracts: Revenue, Profit/Loss, EBITDA, Ratios, Risk Factors,
          Management Discussion, Key Dates, Named Entities
"""

import re
from collections import defaultdict

# ─────────────────────────────────────────────
# PATTERNS
# ─────────────────────────────────────────────

AMOUNT_RE = re.compile(
    r"(?:₹|\$|Rs\.?|USD|INR)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|million|billion|thousand|cr|mn|bn))*"
    r"|\d+(?:\.\d+)?\s*(?:lakh|crore|million|billion|thousand|cr|mn|bn)",
    re.IGNORECASE,
)
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:percent|per cent|%)", re.IGNORECASE)
DATE_RE    = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}"
    r"|FY\s*\d{2,4}[-–]\d{2,4}"
    r"|Q[1-4]\s*FY\s*\d{2,4})\b",
    re.IGNORECASE,
)

# ── Financial Metric Keywords
METRIC_PATTERNS = {
    "Revenue":              [r"revenue", r"total income", r"net sales", r"turnover"],
    "Net Profit":           [r"net profit", r"profit after tax", r"\bpat\b", r"net income"],
    "Gross Profit":         [r"gross profit", r"gross margin"],
    "EBITDA":               [r"\bebitda\b", r"earnings before interest"],
    "Operating Profit":     [r"operating profit", r"operating income", r"\bebit\b"],
    "Total Assets":         [r"total assets", r"asset base"],
    "Total Liabilities":    [r"total liabilities", r"total debt"],
    "Equity":               [r"shareholders.? equity", r"net worth", r"book value"],
    "EPS":                  [r"\beps\b", r"earnings per share"],
    "Debt":                 [r"\bdebt\b", r"long.term debt", r"short.term debt", r"borrowings"],
    "Cash Flow":            [r"cash flow", r"operating cash", r"free cash flow"],
    "Dividend":             [r"dividend", r"dividend per share", r"\bdps\b"],
    "Market Cap":           [r"market cap", r"market capitalisation", r"market capitalization"],
    "Return on Equity":     [r"\broe\b", r"return on equity"],
    "Return on Assets":     [r"\broa\b", r"return on assets"],
    "Debt-to-Equity":       [r"debt.to.equity", r"\bd/e\b", r"leverage ratio"],
    "Current Ratio":        [r"current ratio", r"liquidity ratio"],
    "Interest Coverage":    [r"interest coverage", r"interest service"],
}

RISK_TRIGGERS = [
    r"risk factor", r"material risk", r"key risk",
    r"(may|might|could) (adversely|negatively) (affect|impact)",
    r"(uncertainty|uncertainties)", r"(litigation|legal proceedings)",
    r"(regulatory|compliance) risk", r"(competition|competitive) risk",
    r"(cyber|data) (risk|breach|security)", r"(foreign exchange|currency) risk",
    r"(credit|default) risk", r"(liquidity|funding) risk",
    r"(operational|execution) risk",
]

MGMT_TRIGGERS = [
    r"(management|board) (discussion|commentary|outlook|review)",
    r"(going forward|outlook|guidance|forecast)",
    r"(strategy|strategic|initiative|priority)",
    r"(growth (driver|opportunity|plan))",
    r"(key (highlight|achievement|milestone|development))",
    r"(chairman|ceo|md|managing director).{0,30}(message|letter|statement)",
]

RED_FLAG_TRIGGERS = [
    r"(decline|decrease|fall|drop|loss|negative)\s+(?:in\s+)?(?:revenue|profit|margin|growth)",
    r"(impairment|write.?off|write.?down)",
    r"(going concern|doubt|uncertainty) about",
    r"(qualified|adverse|disclaimer) opinion",
    r"(fraud|misappropriation|embezzlement)",
    r"(regulatory (action|penalty|fine|notice))",
    r"(default|non.payment|overdue)",
    r"(significant (loss|decline|deterioration))",
    r"(material weakness|internal control)",
]


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_financial_doc_data(sentences: list[str]) -> dict:
    """
    Returns:
        financial_metrics  : revenue, profit, EBITDA, ratios etc.
        risk_factors       : identified risk sentences
        red_flags          : warning signals
        mgmt_highlights    : management discussion highlights
        key_dates          : important dates mentioned
        named_entities     : companies, people, locations
        ratio_summary      : key ratios table
        performance_summary: YoY comparison if available
    """
    financial_metrics   = _extract_metrics(sentences)
    risk_factors        = _extract_risks(sentences)
    red_flags           = _extract_red_flags(sentences)
    mgmt_highlights     = _extract_mgmt_highlights(sentences)
    key_dates           = _extract_dates(sentences)
    named_entities      = _extract_named_entities(sentences)
    ratio_summary       = _build_ratio_summary(financial_metrics)
    performance_summary = _extract_performance_summary(sentences)

    return {
        "financial_metrics":   financial_metrics,
        "risk_factors":        risk_factors,
        "red_flags":           red_flags,
        "mgmt_highlights":     mgmt_highlights,
        "key_dates":           key_dates,
        "named_entities":      named_entities,
        "ratio_summary":       ratio_summary,
        "performance_summary": performance_summary,
    }


# ─────────────────────────────────────────────
# METRIC EXTRACTION
# ─────────────────────────────────────────────

def _extract_metrics(sentences: list[str]) -> list[dict]:
    results = []
    for sent in sentences:
        sent_lower = sent.lower()
        for metric, patterns in METRIC_PATTERNS.items():
            if any(re.search(p, sent_lower) for p in patterns):
                amounts  = AMOUNT_RE.findall(sent)
                percents = PERCENT_RE.findall(sent)
                years    = re.findall(r"FY\s*\d{2,4}[-–]?\d{0,4}|20\d{2}", sent)
                results.append({
                    "metric":   metric,
                    "amount":   amounts[0].strip() if amounts else None,
                    "percent":  percents[0] if percents else None,
                    "year":     years[0] if years else None,
                    "sentence": sent,
                })
    # Deduplicate
    seen, deduped = set(), []
    for r in results:
        key = (r["metric"], r["sentence"][:50])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped


# ─────────────────────────────────────────────
# RISK FACTORS
# ─────────────────────────────────────────────

def _extract_risks(sentences: list[str]) -> list[dict]:
    compiled = [re.compile(p, re.IGNORECASE) for p in RISK_TRIGGERS]
    results  = []
    for sent in sentences:
        matched = [p.pattern for p in compiled if p.search(sent)]
        if matched:
            results.append({
                "sentence":   sent,
                "risk_type":  _classify_risk(sent),
                "severity":   _risk_severity(sent),
            })
    return results


def _classify_risk(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["cyber", "data", "security"]):       return "Cyber / Data Risk"
    if any(w in t for w in ["regulatory", "compliance"]):        return "Regulatory Risk"
    if any(w in t for w in ["credit", "default"]):               return "Credit Risk"
    if any(w in t for w in ["liquidity", "funding"]):            return "Liquidity Risk"
    if any(w in t for w in ["currency", "foreign exchange"]):    return "FX Risk"
    if any(w in t for w in ["competition", "competitive"]):      return "Competition Risk"
    if any(w in t for w in ["litigation", "legal"]):             return "Legal Risk"
    if any(w in t for w in ["operational", "execution"]):        return "Operational Risk"
    return "General Risk"


def _risk_severity(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["material", "significant", "major", "critical", "severe"]):
        return "High"
    if any(w in t for w in ["moderate", "potential", "possible"]):
        return "Medium"
    return "Low"


# ─────────────────────────────────────────────
# RED FLAGS
# ─────────────────────────────────────────────

def _extract_red_flags(sentences: list[str]) -> list[dict]:
    compiled = [re.compile(p, re.IGNORECASE) for p in RED_FLAG_TRIGGERS]
    results  = []
    for sent in sentences:
        matched = [p.pattern for p in compiled if p.search(sent)]
        if matched:
            results.append({
                "sentence": sent,
                "flag":     _classify_red_flag(sent),
            })
    return results


def _classify_red_flag(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["fraud", "misappropriation"]):       return "🚨 Fraud / Misappropriation"
    if any(w in t for w in ["going concern", "doubt"]):          return "⚠️ Going Concern"
    if any(w in t for w in ["qualified", "adverse", "disclaimer"]): return "⚠️ Audit Qualification"
    if any(w in t for w in ["impairment", "write-off"]):         return "📉 Impairment / Write-off"
    if any(w in t for w in ["default", "non-payment"]):          return "🔴 Default Risk"
    if any(w in t for w in ["regulatory", "penalty", "fine"]):   return "⚖️ Regulatory Action"
    if any(w in t for w in ["decline", "loss", "drop"]):         return "📉 Performance Decline"
    return "⚠️ General Warning"


# ─────────────────────────────────────────────
# MANAGEMENT HIGHLIGHTS
# ─────────────────────────────────────────────

def _extract_mgmt_highlights(sentences: list[str]) -> list[dict]:
    compiled = [re.compile(p, re.IGNORECASE) for p in MGMT_TRIGGERS]
    results  = []
    for sent in sentences:
        if any(p.search(sent) for p in compiled):
            results.append({
                "sentence": sent,
                "theme":    _mgmt_theme(sent),
            })
    return results


def _mgmt_theme(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["growth", "expand", "scale"]):       return "Growth Strategy"
    if any(w in t for w in ["outlook", "guidance", "forecast"]): return "Outlook / Guidance"
    if any(w in t for w in ["achievement", "milestone"]):        return "Achievement"
    if any(w in t for w in ["strategy", "priority", "focus"]):   return "Strategic Priority"
    return "General Commentary"


# ─────────────────────────────────────────────
# KEY DATES
# ─────────────────────────────────────────────

def _extract_dates(sentences: list[str]) -> list[dict]:
    results = []
    for sent in sentences:
        dates = DATE_RE.findall(sent)
        for d in dates:
            results.append({"date": d, "sentence": sent})
    return results


# ─────────────────────────────────────────────
# NAMED ENTITIES
# ─────────────────────────────────────────────

def _extract_named_entities(sentences: list[str]) -> dict:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return {"companies": [], "people": [], "locations": []}

    companies, people, locations = set(), set(), set()
    for sent in sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                companies.add(ent.text.strip())
            elif ent.label_ == "PERSON":
                people.add(ent.text.strip())
            elif ent.label_ in ("GPE", "LOC"):
                locations.add(ent.text.strip())

    return {
        "companies": sorted(companies),
        "people":    sorted(people),
        "locations": sorted(locations),
    }


# ─────────────────────────────────────────────
# RATIO SUMMARY
# ─────────────────────────────────────────────

def _build_ratio_summary(metrics: list[dict]) -> list[dict]:
    ratio_metrics = ["Return on Equity", "Return on Assets", "Debt-to-Equity",
                     "Current Ratio", "Interest Coverage", "EPS"]
    summary = []
    for m in metrics:
        if m["metric"] in ratio_metrics:
            summary.append({
                "ratio":  m["metric"],
                "value":  m["amount"] or m["percent"],
                "year":   m["year"],
            })
    return summary


# ─────────────────────────────────────────────
# PERFORMANCE SUMMARY
# ─────────────────────────────────────────────

def _extract_performance_summary(sentences: list[str]) -> list[dict]:
    yoy_patterns = [
        r"(grew|increased|rose|jumped|surged)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"(declined|decreased|fell|dropped)\s+(?:by\s+)?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"(compared to|versus|vs\.?)\s+(?:previous|last|prior)\s+(?:year|quarter|period)",
        r"(year.on.year|yoy|quarter.on.quarter|qoq)\s+(?:growth|decline|change)",
    ]
    compiled = [re.compile(p, re.IGNORECASE) for p in yoy_patterns]
    results  = []
    for sent in sentences:
        matched = [p.pattern for p in compiled if p.search(sent)]
        if matched:
            percents = PERCENT_RE.findall(sent)
            results.append({
                "sentence": sent,
                "change":   percents[0] if percents else None,
                "direction": "Positive" if re.search(r"grew|increased|rose|jumped|surged", sent, re.I) else "Negative",
            })
    return results
