"""
Keyword Scoring & Sentence Ranking Module
Uses TF-IDF + domain keyword boosting to rank sentences by importance.
"""

import re
import math
from collections import Counter

import nltk
from nltk.corpus import stopwords

try:
    _STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    _STOPWORDS = set(stopwords.words("english"))

# Add domain-specific stop words
_STOPWORDS.update([
    "government", "india", "country", "year", "also", "would",
    "shall", "may", "said", "one", "two", "three", "per",
])

# ─────────────────────────────────────────────
# DOMAIN BOOST KEYWORDS  (higher = more important)
# ─────────────────────────────────────────────

DOMAIN_BOOST = {
    # Financial
    "crore": 3.0, "lakh": 2.5, "allocation": 3.0, "budget": 2.0,
    "expenditure": 2.5, "revenue": 2.5, "deficit": 3.0, "gdp": 3.0,
    "fiscal": 2.5, "capital": 2.0, "borrowing": 2.5, "disinvestment": 2.5,
    # Policy
    "scheme": 3.0, "initiative": 2.5, "launch": 2.0, "propose": 2.5,
    "announce": 2.5, "establish": 2.0, "mission": 2.0, "programme": 2.0,
    "yojana": 3.0, "abhiyan": 2.5,
    # Tax
    "tax": 2.5, "gst": 3.0, "exemption": 2.5, "rebate": 2.5,
    "surcharge": 2.5, "deduction": 2.0, "slab": 2.5, "duty": 2.0,
    # Sectors
    "agriculture": 2.0, "education": 2.0, "health": 2.0, "defence": 2.0,
    "infrastructure": 2.0, "railways": 2.0, "energy": 2.0, "digital": 2.0,
}


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def rank_sentences(sentences: list[str], top_n: int = 50) -> list[dict]:
    """
    Score and rank sentences by importance.
    Returns list of {sentence, score, rank} sorted by score desc.
    """
    if not sentences:
        return []

    tfidf_scores = _compute_tfidf(sentences)
    scored = []

    for i, sent in enumerate(sentences):
        tfidf  = tfidf_scores.get(i, 0.0)
        boost  = _domain_boost_score(sent)
        length = _length_score(sent)
        final  = tfidf * 0.5 + boost * 0.35 + length * 0.15

        scored.append({
            "sentence": sent,
            "score":    round(final, 4),
            "tfidf":    round(tfidf, 4),
            "boost":    round(boost, 4),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    for rank, item in enumerate(scored, 1):
        item["rank"] = rank

    return scored[:top_n]


def get_top_keywords(sentences: list[str], top_n: int = 30) -> list[dict]:
    """
    Return top N keywords with their frequency and boost score.
    """
    all_tokens = []
    for sent in sentences:
        tokens = _tokenize(sent)
        all_tokens.extend(tokens)

    freq = Counter(all_tokens)
    results = []
    for word, count in freq.most_common(top_n * 2):
        boost = DOMAIN_BOOST.get(word.lower(), 1.0)
        results.append({
            "keyword":   word,
            "frequency": count,
            "boost":     boost,
            "score":     round(count * boost, 2),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def compute_sentence_similarity(s1: str, s2: str) -> float:
    """Cosine similarity between two sentences (bag-of-words)."""
    t1 = Counter(_tokenize(s1))
    t2 = Counter(_tokenize(s2))
    common = set(t1) & set(t2)
    if not common:
        return 0.0
    dot    = sum(t1[w] * t2[w] for w in common)
    norm1  = math.sqrt(sum(v**2 for v in t1.values()))
    norm2  = math.sqrt(sum(v**2 for v in t2.values()))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return [t for t in tokens if t not in _STOPWORDS]


def _compute_tfidf(sentences: list[str]) -> dict:
    """Compute TF-IDF scores per sentence, return {sent_idx: score}."""
    N = len(sentences)
    tokenized = [_tokenize(s) for s in sentences]

    # Document frequency
    df = Counter()
    for tokens in tokenized:
        df.update(set(tokens))

    scores = {}
    for i, tokens in enumerate(tokenized):
        if not tokens:
            scores[i] = 0.0
            continue
        tf = Counter(tokens)
        score = 0.0
        for word, count in tf.items():
            tf_val  = count / len(tokens)
            idf_val = math.log((N + 1) / (df[word] + 1)) + 1
            score  += tf_val * idf_val
        scores[i] = score / len(tf)
    return scores


def _domain_boost_score(sentence: str) -> float:
    tokens = _tokenize(sentence)
    if not tokens:
        return 0.0
    total = sum(DOMAIN_BOOST.get(t, 0.0) for t in tokens)
    return min(total / len(tokens), 5.0)   # cap at 5


def _length_score(sentence: str) -> float:
    """Prefer sentences of 15-40 words."""
    words = sentence.split()
    n = len(words)
    if 15 <= n <= 40:
        return 1.0
    elif n < 15:
        return n / 15
    else:
        return max(0.3, 1 - (n - 40) / 100)
