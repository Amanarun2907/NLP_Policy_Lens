"""
Groq AI Analyzer
Provides all AI-powered analysis features:
  1.  Executive Summary
  2.  Plain-English Explanation
  3.  Impact Analysis (who benefits / who is affected)
  4.  Policy Critique & Recommendations
  5.  Financial Health Summary  (for financial docs)
  6.  Red Flag Narrative        (for financial docs)
  7.  News Brief                (for newspapers)
  8.  Bias Report               (for newspapers)
  9.  Hindi Summary             (for Hindi docs)
  10. Q&A Chatbot               (any document)
  11. Year-on-Year Comparison   (two budgets)
  12. Sector Deep-Dive          (specific sector)
"""

import os, sys

# Ensure the policylens root is always on the path so utils can be found
# regardless of how Streamlit imports this module
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../policylens/modules
_ROOT = os.path.dirname(_HERE)                               # .../policylens
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils.groq_client import chat, chat_with_history

# ─────────────────────────────────────────────
# SYSTEM PROMPTS
# ─────────────────────────────────────────────

_BASE = (
    "You are PolicyLens AI, an expert analyst specialising in "
    "Indian government policy documents, financial documents, and news analysis. "
    "Be precise, factual, and use simple language. "
    "Always structure your response clearly with headings or bullet points."
)

_BUDGET_SYSTEM = _BASE + (
    " You are analysing an Indian Union Budget or Economic Survey document. "
    "Focus on fiscal policy, sector allocations, tax changes, and economic impact."
)

_FINANCE_SYSTEM = _BASE + (
    " You are analysing a corporate financial document such as an annual report "
    "or balance sheet. Focus on financial health, risks, and performance."
)

_NEWS_SYSTEM = _BASE + (
    " You are analysing a newspaper or news article. "
    "Focus on key events, entities, sentiment, and factual accuracy."
)

_HINDI_SYSTEM = (
    "आप PolicyLens AI हैं, जो भारतीय नीति दस्तावेज़ों के विशेषज्ञ विश्लेषक हैं। "
    "सरल हिंदी में उत्तर दें। मुख्य बिंदुओं को बुलेट पॉइंट में लिखें।"
)


# ─────────────────────────────────────────────
# 1. EXECUTIVE SUMMARY
# ─────────────────────────────────────────────

def generate_executive_summary(text: str, doc_type: str = "Financial Budget") -> str:
    """
    Generate a 3-paragraph executive summary of the document.
    """
    system = _get_system(doc_type)
    prompt = f"""
Analyse the following {doc_type} document text and write a concise executive summary.

Structure your response as:
**Overview** (1 paragraph – what this document is about)
**Key Highlights** (5-7 bullet points – most important findings)
**Conclusion** (1 paragraph – overall assessment)

Document Text:
{text[:6000]}
"""
    return chat(system, prompt, temperature=0.3, max_tokens=1024)


# ─────────────────────────────────────────────
# 2. PLAIN-ENGLISH EXPLANATION
# ─────────────────────────────────────────────

def explain_in_plain_english(text: str, doc_type: str = "Financial Budget") -> str:
    """
    Explain the document in simple language for a common person.
    """
    system = _get_system(doc_type)
    prompt = f"""
Explain the following {doc_type} document in very simple language that a common person 
with no financial background can understand.

Use:
- Simple words, no jargon
- Short sentences
- Relatable examples where possible
- Bullet points for key takeaways

Answer the question: "What does this mean for me as a common citizen?"

Document Text:
{text[:5000]}
"""
    return chat(system, prompt, temperature=0.4, max_tokens=1024)


# ─────────────────────────────────────────────
# 3. IMPACT ANALYSIS
# ─────────────────────────────────────────────

def analyze_impact(text: str, doc_type: str = "Financial Budget") -> str:
    """
    Who benefits and who is affected by this document.
    """
    system = _get_system(doc_type)
    prompt = f"""
Analyse the following {doc_type} document and provide a detailed impact analysis.

Structure your response as:

**Who Benefits:**
- List groups/sectors that gain from this document (with reasons)

**Who is Adversely Affected:**
- List groups/sectors that may be negatively impacted (with reasons)

**Neutral / Mixed Impact:**
- Groups with mixed or unclear impact

**Overall Assessment:**
- One paragraph summary of the net impact

Document Text:
{text[:5000]}
"""
    return chat(system, prompt, temperature=0.3, max_tokens=1200)


# ─────────────────────────────────────────────
# 4. POLICY CRITIQUE & RECOMMENDATIONS
# ─────────────────────────────────────────────

def critique_and_recommend(text: str, doc_type: str = "Financial Budget") -> str:
    """
    Critical analysis and policy recommendations.
    """
    system = _get_system(doc_type)
    prompt = f"""
Provide a balanced critical analysis of the following {doc_type} document.

Structure your response as:

**Strengths:**
- What has been done well

**Weaknesses / Gaps:**
- What is missing or could be improved

**Recommendations:**
- Specific actionable suggestions for improvement

**Overall Rating:** (out of 10 with justification)

Document Text:
{text[:5000]}
"""
    return chat(system, prompt, temperature=0.4, max_tokens=1200)


# ─────────────────────────────────────────────
# 5. FINANCIAL HEALTH SUMMARY
# ─────────────────────────────────────────────

def financial_health_summary(text: str, metrics: dict) -> str:
    """
    AI-powered financial health assessment for corporate documents.
    """
    metrics_str = "\n".join(
        f"- {m['metric']}: {m.get('amount') or m.get('percent', 'N/A')}"
        for m in metrics.get("financial_metrics", [])[:15]
    )
    prompt = f"""
Analyse the financial health of this company based on the document and extracted metrics.

Extracted Metrics:
{metrics_str}

Document Text:
{text[:4000]}

Provide:
**Financial Health Score:** (1-10 with justification)
**Strengths:** (3-5 bullet points)
**Concerns:** (3-5 bullet points)
**Outlook:** (short-term and long-term)
**Investor Recommendation:** (Buy / Hold / Avoid with reasoning)
"""
    return chat(_FINANCE_SYSTEM, prompt, temperature=0.3, max_tokens=1200)


# ─────────────────────────────────────────────
# 6. RED FLAG NARRATIVE
# ─────────────────────────────────────────────

def red_flag_narrative(red_flags: list[dict], text: str) -> str:
    """
    Detailed narrative about detected red flags.
    """
    flags_str = "\n".join(
        f"- {f['flag']}: {f['sentence'][:120]}"
        for f in red_flags[:10]
    )
    prompt = f"""
The following red flags were detected in a financial document:

{flags_str}

Based on these red flags and the document context below, provide:
**Risk Assessment:** (overall risk level: Low / Medium / High / Critical)
**Explanation of Each Red Flag:** (what it means in simple terms)
**Potential Consequences:** (what could happen if these risks materialise)
**Suggested Actions:** (what an investor or stakeholder should do)

Document Context:
{text[:3000]}
"""
    return chat(_FINANCE_SYSTEM, prompt, temperature=0.3, max_tokens=1200)


# ─────────────────────────────────────────────
# 7. NEWS BRIEF
# ─────────────────────────────────────────────

def generate_news_brief(text: str, category_tags: dict) -> str:
    """
    Generate a structured news brief from newspaper content.
    """
    cat_summary = "\n".join(
        f"- {cat}: {len(sents)} articles"
        for cat, sents in category_tags.items()
    )
    prompt = f"""
You are a news editor. Based on the following newspaper content, write a structured daily news brief.

Category Distribution:
{cat_summary}

Newspaper Content:
{text[:5000]}

Write:
**Top Story:** (most important news item)
**Politics & Government:** (2-3 key points)
**Economy & Business:** (2-3 key points)
**International:** (2-3 key points)
**Other Notable News:** (2-3 bullet points)
**Editor's Note:** (1 sentence overall assessment of today's news)
"""
    return chat(_NEWS_SYSTEM, prompt, temperature=0.4, max_tokens=1200)


# ─────────────────────────────────────────────
# 8. BIAS REPORT
# ─────────────────────────────────────────────

def generate_bias_report(text: str, bias_data: dict) -> str:
    """
    Detailed bias and tone analysis of newspaper content.
    """
    prompt = f"""
Analyse the tone and potential bias in the following newspaper content.

Pre-detected signals:
- Overall Tone: {bias_data.get('overall_tone')}
- Positive Signals: {bias_data.get('positive_signals')}
- Negative Signals: {bias_data.get('negative_signals')}
- Bias Percentage: {bias_data.get('bias_percent')}%

Newspaper Content:
{text[:4000]}

Provide:
**Tone Analysis:** (objective assessment of the overall tone)
**Potential Bias Detected:** (political, economic, social bias if any)
**Loaded Language Examples:** (specific words/phrases that indicate bias)
**Balanced Perspective:** (what the other side of the story might be)
**Credibility Assessment:** (how reliable does this reporting appear)
"""
    return chat(_NEWS_SYSTEM, prompt, temperature=0.3, max_tokens=1200)


# ─────────────────────────────────────────────
# 9. HINDI SUMMARY
# ─────────────────────────────────────────────

def generate_hindi_summary(text: str, doc_type: str = "Financial Budget") -> str:
    """
    Generate summary in Hindi for Hindi documents or Hindi-speaking users.
    """
    prompt = f"""
निम्नलिखित {doc_type} दस्तावेज़ का सारांश सरल हिंदी में लिखें।

संरचना:
**मुख्य बिंदु:** (5-7 बुलेट पॉइंट)
**महत्वपूर्ण आंकड़े:** (प्रमुख संख्याएं और आवंटन)
**आम नागरिक पर प्रभाव:** (सरल भाषा में)
**निष्कर्ष:** (एक पैराग्राफ)

दस्तावेज़:
{text[:5000]}
"""
    return chat(_HINDI_SYSTEM, prompt, temperature=0.3, max_tokens=1024)


# ─────────────────────────────────────────────
# 10. Q&A CHATBOT
# ─────────────────────────────────────────────

def answer_question(
    question:     str,
    document_text: str,
    history:      list[dict],
    doc_type:     str = "Financial Budget",
) -> str:
    """
    Answer a user question about the uploaded document.
    Maintains conversation history for follow-up questions.
    """
    system = _get_system(doc_type) + f"""

You have access to the following document. Answer questions based ONLY on this document.
If the answer is not in the document, say "This information is not available in the document."
Always cite the relevant part of the document in your answer.

Document:
{document_text[:6000]}
"""
    history_with_question = history + [{"role": "user", "content": question}]
    return chat_with_history(system, history_with_question, temperature=0.2, max_tokens=800)


# ─────────────────────────────────────────────
# 11. YEAR-ON-YEAR COMPARISON
# ─────────────────────────────────────────────

def compare_two_budgets(
    text_year1: str,
    text_year2: str,
    year1:      str = "Year 1",
    year2:      str = "Year 2",
) -> str:
    """
    AI-powered comparison of two budget documents.
    """
    prompt = f"""
Compare the following two Union Budget documents and provide a detailed year-on-year analysis.

{year1} Budget (excerpt):
{text_year1[:3000]}

{year2} Budget (excerpt):
{text_year2[:3000]}

Provide:
**Key Differences:** (major changes between the two budgets)
**Sector-wise Changes:** (which sectors got more/less allocation)
**Tax Policy Changes:** (what changed in taxation)
**Fiscal Position:** (how the fiscal deficit/expenditure changed)
**New Initiatives in {year2}:** (schemes/policies introduced in the newer budget)
**Discontinued/Modified in {year2}:** (what was removed or changed)
**Overall Assessment:** (which budget is more progressive and why)
"""
    return chat(_BUDGET_SYSTEM, prompt, temperature=0.3, max_tokens=1500)


# ─────────────────────────────────────────────
# 12. SECTOR DEEP-DIVE
# ─────────────────────────────────────────────

def sector_deep_dive(sector: str, text: str, doc_type: str = "Financial Budget") -> str:
    """
    Deep analysis of a specific sector from the document.
    """
    system = _get_system(doc_type)
    prompt = f"""
Provide a comprehensive deep-dive analysis of the "{sector}" sector based on the following document.

Structure:
**Allocation & Funding:** (how much money, compared to previous if mentioned)
**Key Schemes & Initiatives:** (specific programmes for this sector)
**Policy Changes:** (regulatory or policy shifts affecting this sector)
**Challenges Mentioned:** (problems acknowledged in the document)
**Growth Outlook:** (expected impact and growth trajectory)
**Beneficiaries:** (who in this sector benefits most)
**Critical Assessment:** (is the allocation adequate? what is missing?)

Document:
{text[:5000]}
"""
    return chat(system, prompt, temperature=0.3, max_tokens=1200)


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _get_system(doc_type: str) -> str:
    if doc_type in ("Financial Budget", "Economic Survey"):
        return _BUDGET_SYSTEM
    elif doc_type == "Financial Document":
        return _FINANCE_SYSTEM
    elif doc_type == "Newspaper Analysis":
        return _NEWS_SYSTEM
    return _BASE
