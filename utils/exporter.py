"""
Exporter Module - Phase 10
Handles: CSV, JSON, and PDF report generation
"""

import os
import json
import io
from datetime import datetime
import pandas as pd
from fpdf import FPDF


# ─────────────────────────────────────────────
# CSV EXPORTS
# ─────────────────────────────────────────────

def export_sentences_csv(sentences: list[str]) -> bytes:
    df = pd.DataFrame({"sentence": sentences})
    return df.to_csv(index=False).encode("utf-8")


def export_keywords_csv(keywords: list[dict]) -> bytes:
    df = pd.DataFrame(keywords)
    return df.to_csv(index=False).encode("utf-8")


def export_ranked_csv(ranked: list[dict]) -> bytes:
    df = pd.DataFrame(ranked)[["rank", "score", "sentence"]]
    return df.to_csv(index=False).encode("utf-8")


def export_sectors_csv(sector_allocations: list[dict]) -> bytes:
    rows = [{
        "Sector":          s["sector"],
        "Amount Text":     s["amount_text"],
        "Amount (Crore)":  s["amount_crore"],
        "Sentence":        s["sentence"],
    } for s in sector_allocations]
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_fiscal_csv(fiscal_indicators: list[dict]) -> bytes:
    rows = [{
        "Indicator":      f["indicator"],
        "Amount":         f.get("amount_text") or "",
        "Percent":        f.get("percent") or "",
        "Sentence":       f["sentence"],
    } for f in fiscal_indicators]
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_tax_csv(tax_changes: list[dict]) -> bytes:
    rows = [{
        "Category":    t["category"],
        "Change Type": t.get("change_type",""),
        "Amount":      t.get("amount") or "",
        "Percent":     t.get("percent") or "",
        "Sentence":    t["sentence"],
    } for t in tax_changes]
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_policy_csv(schemes: list[dict]) -> bytes:
    rows = [{
        "Category": s["category"],
        "Priority": s["priority"],
        "Sentence": s["sentence"],
    } for s in schemes]
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_metrics_csv(metrics: list) -> bytes:
    """Export metrics/indicators to CSV — handles both Financial Doc and Economic Survey formats."""
    rows = []
    for m in metrics:
        if not isinstance(m, dict):
            continue
        # Economic Survey uses "indicator", Financial Doc uses "metric"
        name = m.get("indicator") or m.get("metric") or m.get("name") or "Unknown"
        rows.append({
            "Indicator / Metric": name,
            "Value":    m.get("value") or m.get("amount") or "",
            "Percent":  m.get("percent") or "",
            "Year":     m.get("year") or "",
            "Category": m.get("category") or "",
            "Confidence": m.get("confidence") or "",
            "Sentence": m.get("sentence") or "",
        })
    if not rows:
        return b"No data available"
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_news_csv(category_tags: dict, events: list[dict]) -> bytes:
    rows = []
    for cat, sents in category_tags.items():
        for s in sents:
            rows.append({"Category": cat, "Sentence": s})
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def export_comparison_csv(comparison_data: dict, year1: str, year2: str) -> bytes:
    sec = comparison_data.get("sector_comparison", [])
    if not sec:
        return b"No comparison data"
    return pd.DataFrame(sec).to_csv(index=False).encode("utf-8")


# ─────────────────────────────────────────────
# JSON EXPORT
# ─────────────────────────────────────────────

def export_full_json(data: dict, doc_type: str) -> bytes:
    """Export all extracted data as structured JSON."""
    safe = {}
    skip_keys = {"sentences", "ranked", "raw"}

    for key, val in data.items():
        if key in skip_keys:
            continue
        if isinstance(val, (dict, list, str, int, float, bool, type(None))):
            safe[key] = val

    output = {
        "meta": {
            "doc_type":   doc_type,
            "exported_at": datetime.now().isoformat(),
            "page_count": data.get("raw", {}).get("page_count", 0),
            "language":   data.get("raw", {}).get("detected_lang", ""),
        },
        "data": safe,
    }
    return json.dumps(output, indent=2, default=str).encode("utf-8")


# ─────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────

class PolicyLensPDF(FPDF):
    def __init__(self, doc_type: str, year: str = ""):
        super().__init__()
        self.doc_type = doc_type
        self.year     = year
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_fill_color(36, 113, 163)
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 4)
        title = f"PolicyLens Report  |  {self.doc_type}"
        if self.year:
            title += f"  |  {self.year}"
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10,
                  f"Generated by PolicyLens  |  {datetime.now().strftime('%d %b %Y %H:%M')}  |  Page {self.page_no()}",
                  align="C")

    def section_title(self, title: str):
        self.ln(4)
        self.set_fill_color(214, 234, 248)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(27, 38, 49)
        self.cell(0, 9, f"  {title}", ln=True, fill=True)
        self.ln(2)

    def body_text(self, text: str, size: int = 10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(30, 30, 30)
        safe = text.encode("latin-1", errors="replace").decode("latin-1")
        if self.get_x() > self.w - self.r_margin - 10:
            self.ln(4)
        self.multi_cell(0, 6, safe, max_line_height=self.font_size)
        self.ln(1)

    def kv_row(self, key: str, value: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(36, 113, 163)
        self.cell(60, 7, key + ":", ln=False)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        safe_val = str(value).encode("latin-1", errors="replace").decode("latin-1")
        self.cell(0, 7, safe_val, ln=True)

    def bullet(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        safe = ("  * " + text).encode("latin-1", errors="replace").decode("latin-1")
        # Ensure we have enough width before writing
        if self.get_x() > self.w - self.r_margin - 10:
            self.ln(4)
        self.multi_cell(0, 6, safe, max_line_height=self.font_size)


def generate_pdf_report(data: dict, doc_type: str,
                        ai_summary: str = "", year: str = "") -> bytes:
    """
    Generate a full PDF report from extracted data.
    Returns PDF as bytes.
    """
    pdf = PolicyLensPDF(doc_type, year)
    pdf.add_page()

    # ── META
    pdf.section_title("Document Information")
    raw = data.get("raw", {})
    pdf.kv_row("Document Type",  doc_type)
    pdf.kv_row("Pages",          str(raw.get("page_count", "N/A")))
    pdf.kv_row("Language",       raw.get("detected_lang", "N/A"))
    pdf.kv_row("Extraction",     raw.get("method", "N/A"))
    pdf.kv_row("Sentences",      str(len(data.get("sentences", []))))
    pdf.kv_row("Generated At",   datetime.now().strftime("%d %b %Y %H:%M"))

    # ── SENTIMENT
    senti = data.get("sentiment", {})
    pdf.section_title("Sentiment Analysis")
    pdf.kv_row("Overall Sentiment", senti.get("label", "N/A"))
    pdf.kv_row("Score",             str(senti.get("score", 0)))
    pdf.kv_row("Positive Sentences",str(senti.get("positive", 0)))
    pdf.kv_row("Negative Sentences",str(senti.get("negative", 0)))

    # ── TOP KEYWORDS
    kws = data.get("keywords", [])
    if kws:
        pdf.section_title("Top Keywords")
        kw_line = "  |  ".join(f"{k['keyword']} ({k['frequency']})" for k in kws[:15])
        pdf.body_text(kw_line)

    # ── DOC-TYPE SPECIFIC SECTIONS
    if doc_type == "Financial Budget":
        _pdf_budget_sections(pdf, data)
    elif doc_type == "Economic Survey":
        _pdf_economic_sections(pdf, data)
    elif doc_type == "Financial Document":
        _pdf_findoc_sections(pdf, data)
    elif doc_type == "Newspaper Analysis":
        _pdf_newspaper_sections(pdf, data)

    # ── AI SUMMARY
    if ai_summary:
        pdf.add_page()
        pdf.section_title("AI-Generated Executive Summary")
        pdf.body_text(ai_summary)

    # ── TOP RANKED SENTENCES
    ranked = data.get("ranked", [])
    if ranked:
        pdf.add_page()
        pdf.section_title("Top Ranked Sentences")
        for r in ranked[:10]:
            pdf.bullet(f"[#{r['rank']} score={r['score']}] {r['sentence'][:200]}")

    return bytes(pdf.output())


# ─────────────────────────────────────────────
# PDF SECTION HELPERS
# ─────────────────────────────────────────────

def _pdf_budget_sections(pdf: PolicyLensPDF, data: dict):
    fin = data.get("financial", {})
    pol = data.get("policy", {})
    tax = data.get("tax", {})

    # Sector allocations
    top = fin.get("top_sectors", [])
    if top:
        pdf.section_title("Sector-wise Allocations (Top 10)")
        for s in top[:10]:
            pdf.kv_row(s["sector"], f"Rs. {s['total_crore']:,.0f} Crore")

    # Fiscal indicators
    fi = fin.get("fiscal_indicators", [])
    if fi:
        pdf.section_title("Fiscal Indicators")
        for f in fi[:8]:
            val = f.get("percent") or f.get("amount_text") or "N/A"
            pdf.kv_row(f["indicator"], str(val))

    # Policy schemes
    schemes = pol.get("schemes", [])
    if schemes:
        pdf.section_title(f"Policy Schemes & Initiatives ({len(schemes)} detected)")
        for s in schemes[:10]:
            pdf.bullet(f"[{s['category']}] {s['sentence'][:180]}")

    # Named schemes
    named = pol.get("named_schemes", [])
    if named:
        pdf.section_title("Named Schemes")
        for n in named[:10]:
            pdf.bullet(f"{n['name']}  [{n['category']}]")

    # Tax changes
    tax_ch = tax.get("tax_changes", [])
    if tax_ch:
        pdf.section_title(f"Tax Changes ({len(tax_ch)} detected)")
        for t in tax_ch[:10]:
            val = t.get("amount") or (str(t.get("percent","")) + "%") or "N/A"
            pdf.kv_row(f"{t['category']} ({t.get('change_type','')})", val)


def _pdf_economic_sections(pdf: PolicyLensPDF, data: dict):
    eco = data.get("economic", {})

    macro = eco.get("macro_indicators", [])
    if macro:
        pdf.section_title("Macro Economic Indicators")
        for m in macro[:10]:
            val = m.get("percent") or m.get("value") or "N/A"
            pdf.kv_row(m["indicator"], str(val))

    recs = eco.get("policy_recommendations", [])
    if recs:
        pdf.section_title(f"Policy Recommendations ({len(recs)})")
        for r in recs[:8]:
            pdf.bullet(f"[{r['area']}] {r['sentence'][:180]}")

    highlights = eco.get("key_highlights", [])
    if highlights:
        pdf.section_title("Key Highlights")
        for h in highlights[:8]:
            pdf.bullet(h[:200])


def _pdf_findoc_sections(pdf: PolicyLensPDF, data: dict):
    fd = data.get("fin_doc", {})

    metrics = fd.get("financial_metrics", [])
    if metrics:
        pdf.section_title("Financial Metrics")
        for m in metrics[:12]:
            val = m.get("amount") or (str(m.get("percent","")) + "%") or "N/A"
            pdf.kv_row(m["metric"], str(val))

    risks = fd.get("risk_factors", [])
    if risks:
        pdf.section_title(f"Risk Factors ({len(risks)} detected)")
        for r in risks[:8]:
            pdf.bullet(f"[{r['risk_type']} - {r['severity']}] {r['sentence'][:160]}")

    flags = fd.get("red_flags", [])
    if flags:
        pdf.section_title(f"Red Flags ({len(flags)} detected)")
        for f in flags[:6]:
            pdf.bullet(f"{f['flag']}: {f['sentence'][:160]}")

    mgmt = fd.get("mgmt_highlights", [])
    if mgmt:
        pdf.section_title("Management Highlights")
        for m in mgmt[:6]:
            pdf.bullet(f"[{m['theme']}] {m['sentence'][:180]}")


def _pdf_newspaper_sections(pdf: PolicyLensPDF, data: dict):
    news = data.get("newspaper", {})

    summary = news.get("daily_summary", [])
    if summary:
        pdf.section_title("Daily News Summary")
        for i, s in enumerate(summary, 1):
            pdf.bullet(f"{i}. {s[:200]}")

    events = news.get("events", [])
    if events:
        pdf.section_title(f"Key Events ({len(events)} detected)")
        for e in events[:8]:
            date_str = f" [{e['date']}]" if e.get("date") else ""
            pdf.bullet(f"[{e['event_type']}]{date_str} {e['sentence'][:160]}")

    bias = news.get("bias_analysis", {})
    if bias:
        pdf.section_title("Bias & Tone Analysis")
        pdf.kv_row("Overall Tone",      bias.get("overall_tone", "N/A"))
        pdf.kv_row("Positive Signals",  str(bias.get("positive_signals", 0)))
        pdf.kv_row("Negative Signals",  str(bias.get("negative_signals", 0)))
        pdf.kv_row("Bias Percentage",   f"{bias.get('bias_percent', 0)}%")

    ents = news.get("named_entities", {})
    if ents:
        pdf.section_title("Named Entities")
        pdf.kv_row("People",    ", ".join(ents.get("people", [])[:8]))
        pdf.kv_row("Orgs",      ", ".join(ents.get("orgs", [])[:8]))
        pdf.kv_row("Locations", ", ".join(ents.get("locations", [])[:8]))
