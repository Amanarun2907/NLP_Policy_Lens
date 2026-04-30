"""Test Phase 5 & 6 – Financial Document + Newspaper Analysis."""
from utils.sentence_segmenter         import segment_sentences
from modules.financial_doc_extractor  import extract_financial_doc_data
from modules.newspaper_extractor      import extract_newspaper_data

# ══════════════════════════════════════════════
# PHASE 5 – FINANCIAL DOCUMENT
# ══════════════════════════════════════════════
FIN_DOC = """
The company reported total revenue of Rs. 45,000 crore for FY2024, a growth of 18 percent year-on-year.
Net profit after tax stood at Rs. 6,200 crore, compared to Rs. 4,800 crore in the previous year.
EBITDA margin improved to 22 percent from 19 percent in FY2023.
The board of directors has recommended a dividend of Rs. 15 per share for FY2024.
Earnings per share increased to Rs. 42.5 from Rs. 33.2 in the prior year.
Total debt stood at Rs. 12,000 crore with a debt-to-equity ratio of 0.8.
The company faces significant regulatory risk due to pending litigation in multiple jurisdictions.
There is uncertainty about the outcome of the ongoing tax dispute with the Income Tax Department.
Revenue declined by 5 percent in Q3 FY2024 due to weak demand in the export markets.
The management remains focused on expanding into new geographies and digital channels going forward.
Return on equity improved to 18.5 percent in FY2024 from 14.2 percent in FY2023.
The company signed a strategic agreement with Infosys for digital transformation on 15 March 2024.
Key risks include cyber security threats, foreign exchange volatility, and competitive pressure.
The audit committee noted a material weakness in internal controls related to inventory management.
Cash flow from operations was Rs. 8,500 crore, up 25 percent compared to the previous year.
"""

print("=" * 65)
print("PHASE 5 – FINANCIAL DOCUMENT ANALYSIS")
sentences_fin = segment_sentences(FIN_DOC)
fin = extract_financial_doc_data(sentences_fin)

print(f"\n  Financial Metrics ({len(fin['financial_metrics'])}):")
for m in fin["financial_metrics"][:6]:
    print(f"    [{m['metric']:22s}]  {str(m['amount']):25s}  {m['year'] or ''}")

print(f"\n  Risk Factors ({len(fin['risk_factors'])}):")
for r in fin["risk_factors"][:4]:
    print(f"    [{r['risk_type']:22s}]  Severity={r['severity']}  | {r['sentence'][:70]}")

print(f"\n  Red Flags ({len(fin['red_flags'])}):")
for f in fin["red_flags"][:4]:
    print(f"    {f['flag']:35s}  | {f['sentence'][:60]}")

print(f"\n  Management Highlights ({len(fin['mgmt_highlights'])}):")
for h in fin["mgmt_highlights"][:3]:
    print(f"    [{h['theme']:22s}]  {h['sentence'][:70]}")

print(f"\n  Key Dates ({len(fin['key_dates'])}):")
for d in fin["key_dates"][:4]:
    print(f"    {d['date']:20s}  | {d['sentence'][:60]}")

print(f"\n  Named Entities:")
print(f"    Companies : {fin['named_entities'].get('companies', [])[:5]}")
print(f"    People    : {fin['named_entities'].get('people', [])[:5]}")

print(f"\n  Performance Summary ({len(fin['performance_summary'])}):")
for p in fin["performance_summary"][:3]:
    print(f"    [{p['direction']:8s}]  {p['change']}%  | {p['sentence'][:70]}")


# ══════════════════════════════════════════════
# PHASE 6 – NEWSPAPER ANALYSIS
# ══════════════════════════════════════════════
NEWSPAPER = """
Prime Minister Narendra Modi inaugurated the new AIIMS hospital in Rajkot on Monday.
The Supreme Court of India delivered a landmark verdict on electoral bonds, calling them unconstitutional.
India's GDP growth rate is estimated at 7.6 percent for the fiscal year 2023-24, the highest among G20 nations.
The Indian cricket team won the T20 World Cup defeating South Africa in the final by 7 runs.
Sensex surged 800 points after the RBI kept interest rates unchanged at 6.5 percent.
Tata Motors announced the acquisition of a UK-based EV startup for $500 million.
A massive earthquake of magnitude 6.8 struck the Himalayan region causing widespread damage.
The government launched a new scheme to provide free education to 10 lakh tribal students.
Scientists at ISRO successfully tested the new Gaganyaan crew module in Sriharikota.
Opposition parties criticized the government's handling of the unemployment crisis.
The United Nations climate summit in Dubai concluded with a historic agreement on fossil fuels.
Infosys reported quarterly revenue of Rs. 38,000 crore, a growth of 12 percent year-on-year.
Police arrested three suspects in connection with the Rs. 500 crore bank fraud case in Mumbai.
India signed a free trade agreement with the UAE boosting bilateral trade to $100 billion.
"""

print("\n" + "=" * 65)
print("PHASE 6 – NEWSPAPER ANALYSIS")
sentences_news = segment_sentences(NEWSPAPER)
news = extract_newspaper_data(sentences_news)

print(f"\n  Category Distribution:")
for cat, sents in sorted(news["category_tags"].items(), key=lambda x: -len(x[1])):
    print(f"    {cat:20s}  {len(sents)} sentence(s)")

print(f"\n  Events Detected ({len(news['events'])}):")
for e in news["events"][:5]:
    print(f"    [{e['event_type']:25s}]  {e['sentence'][:70]}")

print(f"\n  Top Keywords:")
for k in news["keyword_freq"][:10]:
    print(f"    {k['keyword']:20s}  freq={k['frequency']}")

print(f"\n  Bias Analysis:")
b = news["bias_analysis"]
print(f"    Overall Tone     : {b['overall_tone']}")
print(f"    Positive Signals : {b['positive_signals']}")
print(f"    Negative Signals : {b['negative_signals']}")
print(f"    Bias %           : {b['bias_percent']}%")

print(f"\n  Top Topics:")
for t in news["topics"][:5]:
    print(f"    Rank {t['rank']}  {t['topic']:20s}  score={t['score']}")

print(f"\n  Daily Summary (5 bullets):")
for i, bullet in enumerate(news["daily_summary"], 1):
    print(f"    {i}. {bullet[:100]}")

print(f"\n  Named Entities:")
print(f"    People    : {news['named_entities'].get('people', [])[:5]}")
print(f"    Orgs      : {news['named_entities'].get('orgs', [])[:5]}")
print(f"    Locations : {news['named_entities'].get('locations', [])[:5]}")
