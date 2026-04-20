"""
Sentiment Analysis Module
Analyzes tone of sentences/paragraphs.
Uses rule-based lexicon (no external model needed, fast).
"""

import re
from collections import Counter

# ─────────────────────────────────────────────
# LEXICONS
# ─────────────────────────────────────────────

POSITIVE_WORDS = {
    "growth", "increase", "improve", "boost", "strengthen", "develop",
    "progress", "benefit", "success", "achieve", "enhance", "promote",
    "support", "invest", "expand", "rise", "gain", "opportunity",
    "innovation", "reform", "empower", "uplift", "welfare", "prosper",
    "efficient", "effective", "robust", "resilient", "sustainable",
    "inclusive", "transparent", "digital", "modern", "advanced",
    "record", "highest", "best", "excellent", "significant", "major",
    "landmark", "historic", "transformative", "revolutionary",
}

NEGATIVE_WORDS = {
    "deficit", "debt", "decline", "decrease", "fall", "reduce",
    "challenge", "problem", "issue", "concern", "risk", "threat",
    "burden", "loss", "failure", "weak", "slow", "low", "poor",
    "inflation", "unemployment", "poverty", "inequality", "crisis",
    "shortage", "gap", "lag", "delay", "obstacle", "difficulty",
}

NEUTRAL_WORDS = {
    "propose", "announce", "allocate", "estimate", "target",
    "plan", "review", "assess", "monitor", "implement",
}


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a text block.
    Returns:
        label    : Positive / Negative / Neutral
        score    : float -1.0 to +1.0
        positive : count of positive signals
        negative : count of negative signals
        breakdown: per-sentence sentiment list
    """
    sentences  = _split_sentences(text)
    breakdown  = [_score_sentence(s) for s in sentences if s.strip()]

    if not breakdown:
        return _empty_result()

    avg_score = sum(b["score"] for b in breakdown) / len(breakdown)
    pos_count = sum(1 for b in breakdown if b["label"] == "Positive")
    neg_count = sum(1 for b in breakdown if b["label"] == "Negative")
    neu_count = sum(1 for b in breakdown if b["label"] == "Neutral")

    if avg_score > 0.05:
        label = "Positive"
    elif avg_score < -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label":     label,
        "score":     round(avg_score, 3),
        "positive":  pos_count,
        "negative":  neg_count,
        "neutral":   neu_count,
        "total":     len(breakdown),
        "breakdown": breakdown,
    }


def analyze_section_sentiments(sections: dict) -> dict:
    """
    Analyze sentiment for multiple named sections.
    sections = {"Section Name": "text..."}
    Returns {section_name: sentiment_result}
    """
    return {name: analyze_sentiment(text) for name, text in sections.items()}


# ─────────────────────────────────────────────
# INTERNAL
# ─────────────────────────────────────────────

def _score_sentence(sentence: str) -> dict:
    tokens = re.findall(r"\b[a-z]{3,}\b", sentence.lower())
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    total = pos + neg

    if total == 0:
        score = 0.0
        label = "Neutral"
    else:
        score = (pos - neg) / total
        if score > 0.1:
            label = "Positive"
        elif score < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

    return {
        "sentence": sentence[:120] + "..." if len(sentence) > 120 else sentence,
        "score":    round(score, 3),
        "label":    label,
        "pos_hits": pos,
        "neg_hits": neg,
    }


def _split_sentences(text: str) -> list[str]:
    return re.split(r"[.!?।]\s+", text)


def _empty_result() -> dict:
    return {
        "label": "Neutral", "score": 0.0,
        "positive": 0, "negative": 0, "neutral": 0,
        "total": 0, "breakdown": [],
    }
