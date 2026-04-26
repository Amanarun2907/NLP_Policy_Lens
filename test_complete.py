"""
test_complete.py - Comprehensive end-to-end test for all PolicyLens modules.
Run from the policylens directory: python test_complete.py
"""

import sys
import os
import traceback

# Ensure policylens root is on path
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

PASS = 0
FAIL = 0
ERRORS = []

def ok(name):
    global PASS
    PASS += 1
    print(f"  [PASS] {name}")

def fail(name, err):
    global FAIL
    FAIL += 1
    msg = f"  [FAIL] {name}: {err}"
    ERRORS.append(msg)
    print(msg)

# ─────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────

BUDGET_SENTENCES = [
    "The government has allocated Rs. 1,50,000 crore for agriculture and allied sectors in the Union Budget 2024-25.",
    "I propose to allocate Rs. 2,50,000 crore for infrastructure development including roads and highways.",
    "The fiscal deficit is targeted at 5.1 percent of GDP for the current financial year.",
    "Income tax exemption limit has been raised to Rs. 7 lakh under the new tax regime.",
    "A new scheme for skill development will be launched with an outlay of Rs. 10,000 crore.",
    "GST revenue has shown a growth of 12 percent year-on-year reaching Rs. 1.68 lakh crore.",
    "Capital expenditure has been increased by 33 percent to Rs. 10 lakh crore.",
    "The government proposes to set up 100 new medical colleges across the country.",
    "Defence allocation has been increased to Rs. 6,21,541 crore for the year 2024-25.",
    "Digital India initiative will receive Rs. 14,903 crore for broadband and internet connectivity.",
    "Revenue expenditure is estimated at Rs. 35 lakh crore for the fiscal year.",
    "Pradhan Mantri Awas Yojana will benefit 2 crore families with affordable housing.",
    "The government will establish a new fund for green energy transition worth Rs. 20,000 crore.",
    "Customs duty on solar panels has been reduced to promote renewable energy adoption.",
    "The GDP growth rate is projected at 7.3 percent for the current financial year.",
]

ECONOMIC_SURVEY_SENTENCES = [
    "India's GDP growth rate is estimated at 7.3 percent for the financial year 2023-24.",
    "Consumer price inflation (CPI) moderated to 5.4 percent in the current year.",
    "The fiscal deficit stood at 5.9 percent of GDP in 2022-23.",
    "Agricultural sector grew at 4.0 percent driven by good monsoon and higher MSP.",
    "Industrial production (IIP) growth averaged 5.8 percent during April-November 2023.",
    "Services sector continues to be the dominant contributor to GDP at 55 percent.",
    "Foreign exchange reserves stood at $620 billion as of December 2023.",
    "The government recommends strengthening the digital payment infrastructure.",
    "Policy reforms should focus on improving ease of doing business for MSMEs.",
    "Export growth needs to be accelerated through trade facilitation measures.",
    "Unemployment rate declined to 7.8 percent according to PLFS data.",
    "Credit growth in the banking sector was robust at 15.4 percent year-on-year.",
    "The current account deficit narrowed to 1.8 percent of GDP in Q2 FY24.",
    "India's nominal GDP is projected to reach Rs. 300 lakh crore by 2024-25.",
    "Gross fixed capital formation as a percentage of GDP improved to 29.8 percent.",
]

FINANCIAL_DOC_SENTENCES = [
    "The company reported total revenue of Rs. 45,000 crore for FY 2023-24.",
    "Net profit after tax stood at Rs. 5,200 crore, a growth of 18 percent year-on-year.",
    "EBITDA margin improved to 22.5 percent from 19.8 percent in the previous year.",
    "Total assets of the company stood at Rs. 1,20,000 crore as on March 31, 2024.",
    "Earnings per share (EPS) increased to Rs. 45.6 from Rs. 38.2 in FY23.",
    "The company faces significant risk from rising raw material costs and supply chain disruptions.",
    "Management expects revenue growth of 15-18 percent in the next financial year.",
    "Shareholders equity stood at Rs. 35,000 crore as on the balance sheet date.",
    "The company has significant exposure to foreign currency risk due to import dependence.",
    "Operating profit for the quarter was Rs. 2,800 crore, up 22 percent quarter-on-quarter.",
    "Total liabilities including long-term debt stood at Rs. 85,000 crore.",
    "The board has recommended a dividend of Rs. 12 per share for FY 2023-24.",
    "Gross profit margin stood at 38.5 percent for the financial year under review.",
    "The company is exposed to regulatory risk in its pharmaceutical segment.",
    "Capital expenditure for the year was Rs. 8,500 crore towards capacity expansion.",
]

NEWSPAPER_SENTENCES = [
    "The Prime Minister announced a new scheme for farmers providing direct income support.",
    "Parliament passed the Finance Bill with several amendments to income tax provisions.",
    "The Reserve Bank of India kept the repo rate unchanged at 6.5 percent.",
    "India's stock market Sensex crossed 75,000 points for the first time in history.",
    "The government signed a bilateral trade agreement with the European Union.",
    "A major earthquake measuring 6.2 on the Richter scale struck the Himalayan region.",
    "The Indian cricket team won the Test series against Australia by 3-1.",
    "New electric vehicle policy announced with subsidies for domestic manufacturers.",
    "The Supreme Court delivered a landmark judgment on electoral bonds scheme.",
    "India's exports grew by 8.5 percent in March 2024 reaching $41.7 billion.",
    "The Health Ministry launched a new vaccination drive targeting 10 crore children.",
    "Technology giant announced investment of $3 billion in India's AI infrastructure.",
    "Opposition parties staged a walkout in Lok Sabha over the budget proposals.",
    "India successfully launched the PSLV-C58 mission carrying earth observation satellites.",
    "The government approved merger of two public sector banks to create a stronger entity.",
]

# ─────────────────────────────────────────────
# 1. MODULE IMPORTS
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("1. MODULE IMPORTS")
print("="*60)

# Modules
try:
    from modules.financial_extractor import extract_financial_data
    ok("modules.financial_extractor")
except Exception as e:
    fail("modules.financial_extractor", traceback.format_exc())

try:
    from modules.economic_survey_extractor import extract_economic_survey_data
    ok("modules.economic_survey_extractor")
except Exception as e:
    fail("modules.economic_survey_extractor", traceback.format_exc())

try:
    from modules.financial_doc_extractor import extract_financial_doc_data
    ok("modules.financial_doc_extractor")
except Exception as e:
    fail("modules.financial_doc_extractor", traceback.format_exc())

try:
    from modules.newspaper_extractor import extract_newspaper_data
    ok("modules.newspaper_extractor")
except Exception as e:
    fail("modules.newspaper_extractor", traceback.format_exc())

try:
    from modules.policy_extractor import extract_policy_data
    ok("modules.policy_extractor")
except Exception as e:
    fail("modules.policy_extractor", traceback.format_exc())

try:
    from modules.tax_extractor import extract_tax_data
    ok("modules.tax_extractor")
except Exception as e:
    fail("modules.tax_extractor", traceback.format_exc())

try:
    from modules.groq_analyzer import generate_executive_summary
    ok("modules.groq_analyzer")
except Exception as e:
    fail("modules.groq_analyzer", traceback.format_exc())

try:
    from modules.comparison_engine import compare_documents
    ok("modules.comparison_engine")
except Exception as e:
    fail("modules.comparison_engine", traceback.format_exc())

# Utils
try:
    from utils.accuracy_validator import validate_extraction_accuracy, get_accuracy_summary
    ok("utils.accuracy_validator")
except Exception as e:
    fail("utils.accuracy_validator", traceback.format_exc())

try:
    from utils.comparison_viz import (
        sector_comparison_chart, sector_change_waterfall,
        fiscal_comparison_chart, sentiment_comparison_chart
    )
    ok("utils.comparison_viz")
except Exception as e:
    fail("utils.comparison_viz", traceback.format_exc())

try:
    from utils.exporter import (
        export_metrics_csv, export_news_csv, export_sectors_csv,
        export_fiscal_csv, export_tax_csv, export_policy_csv, export_full_json
    )
    ok("utils.exporter")
except Exception as e:
    fail("utils.exporter", traceback.format_exc())

try:
    from utils.groq_client import chat
    ok("utils.groq_client")
except Exception as e:
    fail("utils.groq_client", traceback.format_exc())

try:
    from utils.keyword_scorer import rank_sentences, get_top_keywords
    ok("utils.keyword_scorer")
except Exception as e:
    fail("utils.keyword_scorer", traceback.format_exc())

try:
    from utils.ner_extractor import extract_entities, tag_sentence
    ok("utils.ner_extractor")
except Exception as e:
    fail("utils.ner_extractor", traceback.format_exc())

try:
    from utils.normalizer import normalize_text, parse_amount
    ok("utils.normalizer")
except Exception as e:
    fail("utils.normalizer", traceback.format_exc())

try:
    from utils.pdf_extractor import extract_text_from_pdf
    ok("utils.pdf_extractor")
except Exception as e:
    fail("utils.pdf_extractor", traceback.format_exc())

try:
    from utils.sentence_segmenter import segment_sentences
    ok("utils.sentence_segmenter")
except Exception as e:
    fail("utils.sentence_segmenter", traceback.format_exc())

try:
    from utils.sentiment_analyzer import analyze_sentiment
    ok("utils.sentiment_analyzer")
except Exception as e:
    fail("utils.sentiment_analyzer", traceback.format_exc())

try:
    from utils.text_cleaner import clean_text
    ok("utils.text_cleaner")
except Exception as e:
    fail("utils.text_cleaner", traceback.format_exc())

try:
    from utils.visualizer import (
        sector_bar_chart, sentiment_donut, keyword_freq_bar, word_cloud_chart
    )
    ok("utils.visualizer")
except Exception as e:
    fail("utils.visualizer", traceback.format_exc())

# ─────────────────────────────────────────────
# 2. FINANCIAL BUDGET EXTRACTION
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("2. FINANCIAL BUDGET EXTRACTION")
print("="*60)

try:
    from modules.financial_extractor import extract_financial_data
    result = extract_financial_data(BUDGET_SENTENCES)
    assert isinstance(result, dict), "Result must be a dict"
    assert "sector_allocations" in result, "Missing sector_allocations"
    assert "fiscal_indicators" in result, "Missing fiscal_indicators"
    assert "top_sectors" in result, "Missing top_sectors"
    ok("extract_financial_data returns correct keys")
except Exception as e:
    fail("extract_financial_data", traceback.format_exc())

try:
    from modules.policy_extractor import extract_policy_data
    pol = extract_policy_data(BUDGET_SENTENCES)
    assert isinstance(pol, dict), "Policy result must be a dict"
    assert "schemes" in pol, "Missing schemes"
    assert "total_count" in pol, "Missing total_count"
    ok("extract_policy_data returns correct keys")
except Exception as e:
    fail("extract_policy_data", traceback.format_exc())

try:
    from modules.tax_extractor import extract_tax_data
    tax = extract_tax_data(BUDGET_SENTENCES)
    assert isinstance(tax, dict), "Tax result must be a dict"
    assert "tax_changes" in tax, "Missing tax_changes"
    assert "total_count" in tax, "Missing total_count"
    ok("extract_tax_data returns correct keys")
except Exception as e:
    fail("extract_tax_data", traceback.format_exc())

# ─────────────────────────────────────────────
# 3. ECONOMIC SURVEY EXTRACTION
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("3. ECONOMIC SURVEY EXTRACTION")
print("="*60)

try:
    from modules.economic_survey_extractor import extract_economic_survey_data
    eco = extract_economic_survey_data(ECONOMIC_SURVEY_SENTENCES)
    assert isinstance(eco, dict), "Economic survey result must be a dict"
    assert "macro_indicators" in eco, "Missing macro_indicators"
    assert "sector_performance" in eco, "Missing sector_performance"
    assert "policy_recommendations" in eco, "Missing policy_recommendations"
    ok("extract_economic_survey_data returns correct keys")
except Exception as e:
    fail("extract_economic_survey_data", traceback.format_exc())

try:
    eco = extract_economic_survey_data(ECONOMIC_SURVEY_SENTENCES)
    macro = eco.get("macro_indicators", [])
    assert isinstance(macro, list), "macro_indicators must be a list"
    ok("macro_indicators is a list")
except Exception as e:
    fail("macro_indicators type check", traceback.format_exc())

# ─────────────────────────────────────────────
# 4. FINANCIAL DOCUMENT EXTRACTION
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("4. FINANCIAL DOCUMENT EXTRACTION")
print("="*60)

try:
    from modules.financial_doc_extractor import extract_financial_doc_data
    fd = extract_financial_doc_data(FINANCIAL_DOC_SENTENCES)
    assert isinstance(fd, dict), "Financial doc result must be a dict"
    assert "financial_metrics" in fd, "Missing financial_metrics"
    assert "risk_factors" in fd, "Missing risk_factors"
    ok("extract_financial_doc_data returns correct keys")
except Exception as e:
    fail("extract_financial_doc_data", traceback.format_exc())

try:
    fd = extract_financial_doc_data(FINANCIAL_DOC_SENTENCES)
    metrics = fd.get("financial_metrics", [])
    assert isinstance(metrics, list), "financial_metrics must be a list"
    ok("financial_metrics is a list")
except Exception as e:
    fail("financial_metrics type check", traceback.format_exc())

# ─────────────────────────────────────────────
# 5. NEWSPAPER EXTRACTION
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("5. NEWSPAPER EXTRACTION")
print("="*60)

try:
    from modules.newspaper_extractor import extract_newspaper_data
    news = extract_newspaper_data(NEWSPAPER_SENTENCES)
    assert isinstance(news, dict), "Newspaper result must be a dict"
    assert "category_tags" in news, "Missing category_tags"
    assert "events" in news, "Missing events"
    ok("extract_newspaper_data returns correct keys")
except Exception as e:
    fail("extract_newspaper_data", traceback.format_exc())

try:
    news = extract_newspaper_data(NEWSPAPER_SENTENCES)
    cats = news.get("category_tags", {})
    assert isinstance(cats, dict), "category_tags must be a dict"
    ok("category_tags is a dict")
except Exception as e:
    fail("category_tags type check", traceback.format_exc())

# ─────────────────────────────────────────────
# 6. ACCURACY VALIDATOR
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("6. ACCURACY VALIDATOR")
print("="*60)

try:
    from utils.accuracy_validator import validate_extraction_accuracy, get_accuracy_summary
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    pol_result = extract_policy_data(BUDGET_SENTENCES)
    tax_result = extract_tax_data(BUDGET_SENTENCES)
    validation_data = {
        "sector_allocations": fin_result.get("sector_allocations", []),
        "fiscal_indicators": fin_result.get("fiscal_indicators", []),
        "policy_schemes": pol_result.get("schemes", []),
        "tax_changes": tax_result.get("tax_changes", []),
    }
    report = validate_extraction_accuracy(validation_data, " ".join(BUDGET_SENTENCES))
    assert isinstance(report, dict), "Validation report must be a dict"
    assert "overall_accuracy" in report, "Missing overall_accuracy"
    assert "validation_passed" in report, "Missing validation_passed"
    ok("validate_extraction_accuracy returns correct keys")
except Exception as e:
    fail("validate_extraction_accuracy", traceback.format_exc())

try:
    summary = get_accuracy_summary(report)
    assert isinstance(summary, str), "Accuracy summary must be a string"
    ok("get_accuracy_summary returns string")
except Exception as e:
    fail("get_accuracy_summary", traceback.format_exc())

# ─────────────────────────────────────────────
# 7. EXPORTER FUNCTIONS
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("7. EXPORTER FUNCTIONS")
print("="*60)

try:
    from utils.exporter import export_metrics_csv
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    eco_result = extract_economic_survey_data(ECONOMIC_SURVEY_SENTENCES)
    # Test with fiscal indicators (financial budget format)
    csv_bytes = export_metrics_csv(fin_result.get("fiscal_indicators", []))
    assert isinstance(csv_bytes, bytes), "export_metrics_csv must return bytes"
    ok("export_metrics_csv (fiscal indicators)")
except Exception as e:
    fail("export_metrics_csv (fiscal indicators)", traceback.format_exc())

try:
    # Test with macro indicators (economic survey format)
    eco_result = extract_economic_survey_data(ECONOMIC_SURVEY_SENTENCES)
    csv_bytes = export_metrics_csv(eco_result.get("macro_indicators", []))
    assert isinstance(csv_bytes, bytes), "export_metrics_csv must return bytes"
    ok("export_metrics_csv (macro indicators)")
except Exception as e:
    fail("export_metrics_csv (macro indicators)", traceback.format_exc())

try:
    from utils.exporter import export_news_csv
    news_result = extract_newspaper_data(NEWSPAPER_SENTENCES)
    csv_bytes = export_news_csv(
        news_result.get("category_tags", {}),
        news_result.get("events", [])
    )
    assert isinstance(csv_bytes, bytes), "export_news_csv must return bytes"
    ok("export_news_csv")
except Exception as e:
    fail("export_news_csv", traceback.format_exc())

try:
    from utils.exporter import export_sectors_csv
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    csv_bytes = export_sectors_csv(fin_result.get("sector_allocations", []))
    assert isinstance(csv_bytes, bytes), "export_sectors_csv must return bytes"
    ok("export_sectors_csv")
except Exception as e:
    fail("export_sectors_csv", traceback.format_exc())

try:
    from utils.exporter import export_fiscal_csv
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    csv_bytes = export_fiscal_csv(fin_result.get("fiscal_indicators", []))
    assert isinstance(csv_bytes, bytes), "export_fiscal_csv must return bytes"
    ok("export_fiscal_csv")
except Exception as e:
    fail("export_fiscal_csv", traceback.format_exc())

try:
    from utils.exporter import export_tax_csv
    tax_result = extract_tax_data(BUDGET_SENTENCES)
    csv_bytes = export_tax_csv(tax_result.get("tax_changes", []))
    assert isinstance(csv_bytes, bytes), "export_tax_csv must return bytes"
    ok("export_tax_csv")
except Exception as e:
    fail("export_tax_csv", traceback.format_exc())

try:
    from utils.exporter import export_policy_csv
    pol_result = extract_policy_data(BUDGET_SENTENCES)
    csv_bytes = export_policy_csv(pol_result.get("schemes", []))
    assert isinstance(csv_bytes, bytes), "export_policy_csv must return bytes"
    ok("export_policy_csv")
except Exception as e:
    fail("export_policy_csv", traceback.format_exc())

try:
    from utils.exporter import export_full_json
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    data_dict = {
        "financial": fin_result,
        "sentences": BUDGET_SENTENCES,
        "raw": {"page_count": 1, "detected_lang": "English", "method": "test"},
    }
    json_bytes = export_full_json(data_dict, "Financial Budget")
    assert isinstance(json_bytes, bytes), "export_full_json must return bytes"
    import json
    parsed = json.loads(json_bytes)
    assert "meta" in parsed, "JSON must have meta key"
    assert "data" in parsed, "JSON must have data key"
    ok("export_full_json")
except Exception as e:
    fail("export_full_json", traceback.format_exc())

# ─────────────────────────────────────────────
# 8. VISUALIZER FUNCTIONS
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("8. VISUALIZER FUNCTIONS")
print("="*60)

try:
    from utils.visualizer import sector_bar_chart
    import plotly.graph_objects as go
    fin_result = extract_financial_data(BUDGET_SENTENCES)
    top_sectors = fin_result.get("top_sectors", [])
    # Use dummy data if extraction returned nothing
    if not top_sectors:
        top_sectors = [{"sector": "Agriculture", "total_crore": 150000},
                       {"sector": "Defence", "total_crore": 621541}]
    fig = sector_bar_chart(top_sectors)
    assert isinstance(fig, go.Figure), "sector_bar_chart must return go.Figure"
    ok("sector_bar_chart")
except Exception as e:
    fail("sector_bar_chart", traceback.format_exc())

try:
    from utils.visualizer import sentiment_donut
    senti = analyze_sentiment(" ".join(BUDGET_SENTENCES))
    fig = sentiment_donut(senti, "Test Sentiment")
    assert isinstance(fig, go.Figure), "sentiment_donut must return go.Figure"
    ok("sentiment_donut")
except Exception as e:
    fail("sentiment_donut", traceback.format_exc())

try:
    from utils.visualizer import keyword_freq_bar
    from utils.keyword_scorer import get_top_keywords
    kws = get_top_keywords(BUDGET_SENTENCES, top_n=20)
    fig = keyword_freq_bar(kws, 20, "Test Keywords")
    assert isinstance(fig, go.Figure), "keyword_freq_bar must return go.Figure"
    ok("keyword_freq_bar")
except Exception as e:
    fail("keyword_freq_bar", traceback.format_exc())

try:
    from utils.visualizer import word_cloud_chart
    from utils.keyword_scorer import get_top_keywords
    kws = get_top_keywords(BUDGET_SENTENCES, top_n=20)
    fig = word_cloud_chart(kws, "Test Word Cloud")
    assert isinstance(fig, go.Figure), "word_cloud_chart must return go.Figure"
    ok("word_cloud_chart")
except Exception as e:
    fail("word_cloud_chart", traceback.format_exc())

# ─────────────────────────────────────────────
# 9. COMPARISON ENGINE
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("9. COMPARISON ENGINE")
print("="*60)

try:
    from modules.comparison_engine import compare_documents
    from utils.keyword_scorer import get_top_keywords, rank_sentences
    from utils.sentiment_analyzer import analyze_sentiment

    fin1 = extract_financial_data(BUDGET_SENTENCES)
    pol1 = extract_policy_data(BUDGET_SENTENCES)
    tax1 = extract_tax_data(BUDGET_SENTENCES)

    # Use economic survey sentences as "second budget" for comparison
    fin2 = extract_financial_data(ECONOMIC_SURVEY_SENTENCES)
    pol2 = extract_policy_data(ECONOMIC_SURVEY_SENTENCES)
    tax2 = extract_tax_data(ECONOMIC_SURVEY_SENTENCES)

    data1 = {
        "financial": fin1, "policy": pol1, "tax": tax1,
        "sentences": BUDGET_SENTENCES,
        "keywords": get_top_keywords(BUDGET_SENTENCES, 20),
        "sentiment": analyze_sentiment(" ".join(BUDGET_SENTENCES)),
        "ranked": rank_sentences(BUDGET_SENTENCES, 10),
    }
    data2 = {
        "financial": fin2, "policy": pol2, "tax": tax2,
        "sentences": ECONOMIC_SURVEY_SENTENCES,
        "keywords": get_top_keywords(ECONOMIC_SURVEY_SENTENCES, 20),
        "sentiment": analyze_sentiment(" ".join(ECONOMIC_SURVEY_SENTENCES)),
        "ranked": rank_sentences(ECONOMIC_SURVEY_SENTENCES, 10),
    }

    comp = compare_documents(data1, data2, "2023-24", "2024-25")
    assert isinstance(comp, dict), "compare_documents must return a dict"
    assert "sector_comparison" in comp, "Missing sector_comparison"
    assert "sentiment_comparison" in comp, "Missing sentiment_comparison"
    ok("compare_documents returns correct keys")
except Exception as e:
    fail("compare_documents", traceback.format_exc())

# ─────────────────────────────────────────────
# 10. SYNTAX CHECK OF KEY FILES
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("10. SYNTAX CHECK OF renders.py, budget_dashboard.py, app.py")
print("="*60)

import ast

for fname in ["renders.py", "budget_dashboard.py", "app.py"]:
    fpath = os.path.join(_HERE, fname)
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        ok(f"{fname} syntax OK")
    except SyntaxError as e:
        fail(f"{fname} syntax", f"SyntaxError at line {e.lineno}: {e.msg} — {e.text!r}")
    except FileNotFoundError:
        fail(f"{fname} syntax", "File not found")
    except Exception as e:
        fail(f"{fname} syntax", traceback.format_exc())

# ─────────────────────────────────────────────
# ADDITIONAL UTILITY TESTS
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("11. UTILITY MODULE TESTS")
print("="*60)

try:
    from utils.text_cleaner import clean_text
    cleaned = clean_text("Hello   World.\n\nTest sentence.", "English")
    assert isinstance(cleaned, str), "clean_text must return str"
    ok("clean_text")
except Exception as e:
    fail("clean_text", traceback.format_exc())

try:
    from utils.normalizer import normalize_text, parse_amount
    norm = normalize_text("Rs. 1,50,000 crore allocated for agriculture.")
    assert isinstance(norm, str), "normalize_text must return str"
    val = parse_amount("2 lakh crore")
    assert isinstance(val, float), "parse_amount must return float"
    ok("normalize_text and parse_amount")
except Exception as e:
    fail("normalize_text / parse_amount", traceback.format_exc())

try:
    from utils.sentence_segmenter import segment_sentences
    sents = segment_sentences("India's GDP grew by 7 percent. Inflation was 5 percent.", "English")
    assert isinstance(sents, list), "segment_sentences must return list"
    ok("segment_sentences")
except Exception as e:
    fail("segment_sentences", traceback.format_exc())

try:
    from utils.sentiment_analyzer import analyze_sentiment
    result = analyze_sentiment("The economy showed strong growth and improvement.")
    assert isinstance(result, dict), "analyze_sentiment must return dict"
    assert "label" in result, "Missing label"
    assert "score" in result, "Missing score"
    ok("analyze_sentiment")
except Exception as e:
    fail("analyze_sentiment", traceback.format_exc())

try:
    from utils.keyword_scorer import rank_sentences, get_top_keywords
    ranked = rank_sentences(BUDGET_SENTENCES, top_n=5)
    assert isinstance(ranked, list), "rank_sentences must return list"
    kws = get_top_keywords(BUDGET_SENTENCES, top_n=10)
    assert isinstance(kws, list), "get_top_keywords must return list"
    ok("rank_sentences and get_top_keywords")
except Exception as e:
    fail("rank_sentences / get_top_keywords", traceback.format_exc())

try:
    from utils.ner_extractor import extract_entities, tag_sentence
    ents = extract_entities(BUDGET_SENTENCES)
    assert isinstance(ents, dict), "extract_entities must return dict"
    tags = tag_sentence(BUDGET_SENTENCES[0])
    assert isinstance(tags, list), "tag_sentence must return list"
    ok("extract_entities and tag_sentence")
except Exception as e:
    fail("extract_entities / tag_sentence", traceback.format_exc())

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"  PASSED : {PASS}")
print(f"  FAILED : {FAIL}")
print(f"  TOTAL  : {PASS + FAIL}")

if ERRORS:
    print("\nALL ERRORS:")
    for e in ERRORS:
        print(e)
else:
    print("\nAll tests passed!")
