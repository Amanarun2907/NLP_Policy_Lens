"""Test Phase 4 – all extraction branches."""
from utils.sentence_segmenter       import segment_sentences
from modules.financial_extractor    import extract_financial_data
from modules.policy_extractor       import extract_policy_data
from modules.tax_extractor          import extract_tax_data
from modules.economic_survey_extractor import extract_economic_survey_data

SAMPLE = """
The Government has proposed an allocation of Rs. 1,50,000 crore for infrastructure development.
I propose to launch a new scheme for farmers to improve agricultural productivity across the country.
The fiscal deficit is targeted at 5.1 percent of GDP for the year 2024-25.
Income tax exemption limit has been increased to Rs. 12 lakh for individual taxpayers.
A new Digital India Mission will be established with an outlay of Rs. 10,000 crore.
The capital expenditure has been increased by 33 percent to Rs. 10 lakh crore.
GST collections have shown robust growth reaching a record high of Rs. 1.87 lakh crore in April.
We will set up 100 new Eklavya Model Residential Schools in tribal areas.
The revenue deficit is estimated at 2.9 percent of GDP.
Customs duty on mobile phones has been reduced to promote domestic manufacturing.
An amount of Rs. 60,000 crore has been allocated for the health sector.
The Pradhan Mantri Awas Yojana will be extended to cover 2 crore more families.
Corporate tax rate has been reduced to 22 percent for domestic companies.
The GDP growth rate is estimated at 7.2 percent for the current fiscal year.
Agriculture sector grew at 3.5 percent during the year.
We recommend structural reforms in the banking sector to reduce NPAs.
Exports reached a record high of 450 billion dollars during 2023-24.
A new Startup India Fund of Rs. 1,000 crore will be created to support innovation.
Long term capital gains tax has been revised to 12.5 percent.
The government will establish 50 new tourist circuits under the Swadesh Darshan scheme.
"""

sentences = segment_sentences(SAMPLE)
print(f"Total sentences: {len(sentences)}\n")

# ── BRANCH A
print("=" * 65)
print("BRANCH A – FINANCIAL EXTRACTION")
fin = extract_financial_data(sentences)
print(f"\n  Sector Allocations ({len(fin['sector_allocations'])}):")
for s in fin["sector_allocations"][:5]:
    print(f"    [{s['sector']:20s}]  {s['amount_text']:25s}  ({s['amount_crore']} Cr)")
print(f"\n  Fiscal Indicators ({len(fin['fiscal_indicators'])}):")
for f in fin["fiscal_indicators"][:5]:
    print(f"    [{f['indicator']:22s}]  amt={f['amount_text']}  pct={f['percent']}")
print(f"\n  Top Sectors by Allocation:")
for t in fin["top_sectors"][:5]:
    print(f"    {t['sector']:25s}  {t['total_crore']:>12.2f} Cr")

# ── BRANCH B
print("\n" + "=" * 65)
print("BRANCH B – POLICY & SCHEME EXTRACTION")
pol = extract_policy_data(sentences)
print(f"\n  Schemes detected     : {pol['total_count']}")
print(f"  Named schemes        : {len(pol['named_schemes'])}")
print(f"  Beneficiary mentions : {len(pol['beneficiaries'])}")
print(f"\n  By Category:")
for cat, items in pol["by_category"].items():
    print(f"    {cat:20s}  {len(items)} scheme(s)")
print(f"\n  Named Schemes Found:")
for ns in pol["named_schemes"][:5]:
    print(f"    {ns['name']}  [{ns['category']}]")

# ── BRANCH C
print("\n" + "=" * 65)
print("BRANCH C – TAX EXTRACTION")
tax = extract_tax_data(sentences)
print(f"\n  Total tax changes : {tax['total_count']}")
print(f"  Income tax items  : {len(tax['income_tax'])}")
print(f"  GST items         : {len(tax['gst_changes'])}")
print(f"  Customs items     : {len(tax['customs_changes'])}")
print(f"  Exemptions        : {len(tax['exemptions'])}")
print(f"\n  Summary Table:")
for row in tax["summary_table"]:
    print(f"    {row['category']:25s}  count={row['count']}  changes={row['change_types']}")

# ── ECONOMIC SURVEY
print("\n" + "=" * 65)
print("ECONOMIC SURVEY EXTRACTION")
eco = extract_economic_survey_data(sentences)
print(f"\n  Macro Indicators ({len(eco['macro_indicators'])}):")
for m in eco["macro_indicators"][:6]:
    print(f"    [{m['indicator']:22s}]  val={m['value']}  pct={m['percent']}")
print(f"\n  Sector Performance:")
for sec, items in eco["sector_performance"].items():
    print(f"    {sec:20s}  {len(items)} mention(s)")
print(f"\n  Policy Recommendations : {len(eco['policy_recommendations'])}")
print(f"  Trend Data Points      : {len(eco['trend_data'])}")
print(f"  Key Highlights         : {len(eco['key_highlights'])}")
