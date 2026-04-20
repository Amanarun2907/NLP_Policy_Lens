"""
Phase 6 – Newspaper Analysis Extractor
Handles: PDF newspapers, news articles, press releases
Extracts: Named entities, topics, sentiment per article,
          events, dates, category tagging, bias detection,
          keyword frequency, daily summary
"""

import re
from collections import defaultdict, Counter

# ─────────────────────────────────────────────
# CATEGORY KEYWORDS
# ─────────────────────────────────────────────

NEWS_CATEGORIES = {
    "Politics":       ["parliament", "minister", "government", "election", "party", "vote",
                       "pm", "president", "cabinet", "policy", "bill", "lok sabha", "rajya sabha"],
    "Economy":        ["economy", "gdp", "inflation", "market", "stock", "sensex", "nifty",
                       "rbi", "budget", "fiscal", "trade", "export", "import", "rupee"],
    "Business":       ["company", "corporate", "merger", "acquisition", "ipo", "profit",
                       "revenue", "quarterly", "earnings", "ceo", "startup", "investment"],
    "Technology":     ["technology", "tech", "ai", "artificial intelligence", "software",
                       "digital", "cyber", "internet", "app", "data", "cloud", "5g"],
    "Health":         ["health", "hospital", "disease", "vaccine", "medicine", "doctor",
                       "patient", "pandemic", "virus", "who", "treatment", "drug"],
    "Sports":         ["cricket", "football", "tennis", "olympic", "match", "tournament",
                       "player", "team", "score", "championship", "ipl", "fifa"],
    "International":  ["international", "global", "world", "foreign", "bilateral", "summit",
                       "un", "nato", "war", "conflict", "treaty", "sanctions"],
    "Environment":    ["climate", "environment", "pollution", "carbon", "emission",
                       "renewable", "forest", "biodiversity", "green", "sustainability"],
    "Crime & Law":    ["crime", "arrest", "police", "court", "judge", "verdict", "accused",
                       "investigation", "fir", "bail", "sentence", "law"],
    "Education":      ["education", "school", "university", "exam", "student", "teacher",
                       "curriculum", "neet", "jee", "board exam", "scholarship"],
    "Science":        ["science", "research", "discovery", "space", "isro", "nasa",
                       "experiment", "study", "scientist", "innovation", "breakthrough"],
    "Social":         ["social", "community", "welfare", "poverty", "inequality",
                       "women", "child", "tribal", "minority", "protest", "movement"],
}

# ─────────────────────────────────────────────
# BIAS INDICATORS
# ─────────────────────────────────────────────

POSITIVE_BIAS = [
    "praised", "lauded", "commended", "welcomed", "hailed", "celebrated",
    "successful", "achievement", "milestone", "historic", "landmark",
    "excellent", "outstanding", "remarkable", "impressive",
]
NEGATIVE_BIAS = [
    "criticized", "condemned", "slammed", "attacked", "accused", "blamed",
    "failed", "failure", "disaster", "crisis", "controversy", "scandal",
    "alleged", "reportedly", "claimed", "questioned", "doubted",
]
NEUTRAL_INDICATORS = [
    "said", "stated", "announced", "reported", "according to",
    "confirmed", "informed", "noted", "added", "mentioned",
]

# ─────────────────────────────────────────────
# EVENT TRIGGERS
# ─────────────────────────────────────────────

EVENT_TRIGGERS = [
    r"(launched|inaugurated|opened|unveiled|announced|signed|passed|approved)",
    r"(arrested|detained|convicted|acquitted|sentenced)",
    r"(died|passed away|killed|injured|survived)",
    r"(won|lost|defeated|elected|appointed|resigned|fired|quit)",
    r"(earthquake|flood|cyclone|disaster|accident|explosion|fire)",
    r"(summit|conference|meeting|talks|negotiation|agreement|deal)",
    r"(protest|rally|strike|demonstration|march)",
]

AMOUNT_RE  = re.compile(
    r"(?:₹|\$|Rs\.?|USD|EUR|GBP)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|million|billion|thousand))*",
    re.IGNORECASE,
)
DATE_RE = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}"
    r"|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday))\b",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_newspaper_data(sentences: list[str]) -> dict:
    """
    Returns:
        named_entities    : people, orgs, locations
        topics            : top themes / topics
        category_tags     : sentences grouped by news category
        sentiment         : overall + per-category sentiment
        events            : key events detected
        key_dates         : dates mentioned
        keyword_freq      : top keywords with frequency
        bias_analysis     : tone / bias detection
        daily_summary     : 5-bullet auto summary
        most_mentioned    : top entities ranked
    """
    named_entities  = _extract_entities(sentences)
    category_tags   = _categorize_sentences(sentences)
    events          = _extract_events(sentences)
    key_dates       = _extract_dates(sentences)
    keyword_freq    = _keyword_frequency(sentences)
    bias_analysis   = _detect_bias(sentences)
    sentiment       = _sentiment_by_category(category_tags)
    topics          = _extract_topics(sentences)
    daily_summary   = _generate_summary_bullets(sentences, category_tags)
    most_mentioned  = _most_mentioned_entities(named_entities)

    return {
        "named_entities":  named_entities,
        "category_tags":   category_tags,
        "events":          events,
        "key_dates":       key_dates,
        "keyword_freq":    keyword_freq,
        "bias_analysis":   bias_analysis,
        "sentiment":       sentiment,
        "topics":          topics,
        "daily_summary":   daily_summary,
        "most_mentioned":  most_mentioned,
    }


# ─────────────────────────────────────────────
# NAMED ENTITY EXTRACTION
# ─────────────────────────────────────────────

def _extract_entities(sentences: list[str]) -> dict:
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        people, orgs, locations = set(), set(), set()
        for sent in sentences:
            doc = nlp(sent)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    people.add(ent.text.strip())
                elif ent.label_ == "ORG":
                    orgs.add(ent.text.strip())
                elif ent.label_ in ("GPE", "LOC"):
                    locations.add(ent.text.strip())
        return {
            "people":    sorted(people),
            "orgs":      sorted(orgs),
            "locations": sorted(locations),
        }
    except Exception:
        return {"people": [], "orgs": [], "locations": []}


# ─────────────────────────────────────────────
# CATEGORY TAGGING
# ─────────────────────────────────────────────

def _categorize_sentences(sentences: list[str]) -> dict:
    grouped = defaultdict(list)
    for sent in sentences:
        sent_lower = sent.lower()
        assigned   = False
        for category, keywords in NEWS_CATEGORIES.items():
            if any(kw in sent_lower for kw in keywords):
                grouped[category].append(sent)
                assigned = True
        if not assigned:
            grouped["General"].append(sent)
    return dict(grouped)


# ─────────────────────────────────────────────
# EVENT EXTRACTION
# ─────────────────────────────────────────────

def _extract_events(sentences: list[str]) -> list[dict]:
    compiled = [re.compile(p, re.IGNORECASE) for p in EVENT_TRIGGERS]
    results  = []
    for sent in sentences:
        matched = [p.pattern for p in compiled if p.search(sent)]
        if matched:
            dates   = DATE_RE.findall(sent)
            amounts = AMOUNT_RE.findall(sent)
            results.append({
                "sentence":   sent,
                "event_type": _classify_event(sent),
                "date":       dates[0] if dates else None,
                "amount":     amounts[0].strip() if amounts else None,
            })
    return results


def _classify_event(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["launched", "inaugurated", "unveiled", "opened"]):
        return "Launch / Inauguration"
    if any(w in t for w in ["arrested", "convicted", "sentenced", "acquitted"]):
        return "Legal / Crime"
    if any(w in t for w in ["died", "killed", "injured"]):
        return "Casualty / Incident"
    if any(w in t for w in ["won", "elected", "appointed"]):
        return "Political / Electoral"
    if any(w in t for w in ["earthquake", "flood", "cyclone", "disaster"]):
        return "Natural Disaster"
    if any(w in t for w in ["summit", "conference", "agreement", "deal"]):
        return "Diplomatic / Agreement"
    if any(w in t for w in ["protest", "strike", "rally"]):
        return "Protest / Movement"
    return "General Event"


# ─────────────────────────────────────────────
# KEY DATES
# ─────────────────────────────────────────────

def _extract_dates(sentences: list[str]) -> list[dict]:
    results = []
    for sent in sentences:
        dates = DATE_RE.findall(sent)
        for d in dates:
            results.append({"date": d, "sentence": sent[:100]})
    return results


# ─────────────────────────────────────────────
# KEYWORD FREQUENCY
# ─────────────────────────────────────────────

def _keyword_frequency(sentences: list[str], top_n: int = 30) -> list[dict]:
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "by", "from", "is", "are", "was", "were",
        "has", "have", "had", "be", "been", "being", "that", "this",
        "it", "its", "as", "not", "also", "said", "will", "would",
        "could", "should", "may", "might", "can", "do", "did", "does",
    }
    all_words = []
    for sent in sentences:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", sent.lower())
        all_words.extend([w for w in words if w not in stop_words])

    freq = Counter(all_words)
    return [{"keyword": w, "frequency": c} for w, c in freq.most_common(top_n)]


# ─────────────────────────────────────────────
# BIAS DETECTION
# ─────────────────────────────────────────────

def _detect_bias(sentences: list[str]) -> dict:
    pos_count = neg_count = neu_count = 0
    biased_sentences = []

    for sent in sentences:
        sent_lower = sent.lower()
        pos = sum(1 for w in POSITIVE_BIAS if w in sent_lower)
        neg = sum(1 for w in NEGATIVE_BIAS if w in sent_lower)
        neu = sum(1 for w in NEUTRAL_INDICATORS if w in sent_lower)

        pos_count += pos
        neg_count += neg
        neu_count += neu

        if pos > 0 or neg > 0:
            bias = "Pro" if pos > neg else "Against" if neg > pos else "Neutral"
            biased_sentences.append({
                "sentence":   sent[:120],
                "bias":       bias,
                "pos_signals": pos,
                "neg_signals": neg,
            })

    total = pos_count + neg_count + neu_count or 1
    return {
        "overall_tone":       "Positive" if pos_count > neg_count else "Negative" if neg_count > pos_count else "Neutral",
        "positive_signals":   pos_count,
        "negative_signals":   neg_count,
        "neutral_signals":    neu_count,
        "bias_percent":       round((pos_count + neg_count) / total * 100, 1),
        "biased_sentences":   biased_sentences[:10],
    }


# ─────────────────────────────────────────────
# SENTIMENT BY CATEGORY
# ─────────────────────────────────────────────

def _sentiment_by_category(category_tags: dict) -> dict:
    from utils.sentiment_analyzer import analyze_sentiment
    result = {}
    for category, sents in category_tags.items():
        if sents:
            text = " ".join(sents)
            result[category] = analyze_sentiment(text)
    return result


# ─────────────────────────────────────────────
# TOPIC EXTRACTION
# ─────────────────────────────────────────────

def _extract_topics(sentences: list[str]) -> list[dict]:
    """Simple topic extraction using category keyword density."""
    topic_scores = Counter()
    for sent in sentences:
        sent_lower = sent.lower()
        for category, keywords in NEWS_CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in sent_lower)
            if score > 0:
                topic_scores[category] += score

    return [
        {"topic": cat, "score": score, "rank": i + 1}
        for i, (cat, score) in enumerate(topic_scores.most_common(10))
    ]


# ─────────────────────────────────────────────
# DAILY SUMMARY BULLETS
# ─────────────────────────────────────────────

def _generate_summary_bullets(sentences: list[str], category_tags: dict) -> list[str]:
    """
    Pick the top sentence from each major category as a summary bullet.
    """
    priority_cats = ["Politics", "Economy", "Business", "International", "Technology",
                     "Health", "Sports", "Crime & Law", "Environment", "Social"]
    bullets = []
    for cat in priority_cats:
        sents = category_tags.get(cat, [])
        if sents:
            # Pick the longest sentence as most informative
            best = max(sents, key=lambda s: len(s))
            bullets.append(f"[{cat}] {best[:150]}")
        if len(bullets) >= 5:
            break

    # Fill remaining from general if needed
    if len(bullets) < 5:
        general = category_tags.get("General", [])
        for s in general[:5 - len(bullets)]:
            bullets.append(f"[General] {s[:150]}")

    return bullets[:5]


# ─────────────────────────────────────────────
# MOST MENTIONED ENTITIES
# ─────────────────────────────────────────────

def _most_mentioned_entities(named_entities: dict) -> list[dict]:
    full_text_tokens = (
        named_entities.get("people", []) +
        named_entities.get("orgs", []) +
        named_entities.get("locations", [])
    )
    freq = Counter(full_text_tokens)
    return [
        {"entity": e, "count": c, "type": _entity_type(e, named_entities)}
        for e, c in freq.most_common(15)
    ]


def _entity_type(entity: str, named_entities: dict) -> str:
    if entity in named_entities.get("people", []):    return "Person"
    if entity in named_entities.get("orgs", []):      return "Organization"
    if entity in named_entities.get("locations", []): return "Location"
    return "Unknown"
