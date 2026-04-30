"""Test Phase 7 – Groq AI Integration."""
from modules.groq_analyzer import (
    generate_executive_summary,
    explain_in_plain_english,
    analyze_impact,
    critique_and_recommend,
    financial_health_summary,
    red_flag_narrative,
    generate_news_brief,
    generate_bias_report,
    generate_hindi_summary,
    answer_question,
    compare_two_budgets,
    sector_deep_dive,
)

BUDGET_TEXT = """
The Government has proposed an allocation of Rs. 1,50,000 crore for infrastructure development.
I propose to launch a new scheme for farmers to improve agricultural productivity.
The fiscal deficit is targeted at 5.1 percent of GDP for the year 2024-25.
Income tax exemption limit has been increased to Rs. 12 lakh for individual taxpayers.
A new Digital India Mission will be established with an outlay of Rs. 10,000 crore.
The capital expenditure has been increased by 33 percent to Rs. 10 lakh crore.
GST collections have shown robust growth reaching a record high of Rs. 1.87 lakh crore.
An amount of Rs. 60,000 crore has been allocated for the health sector.
Corporate tax rate has been reduced to 22 percent for domestic companies.
The Pradhan Mantri Awas Yojana will be extended to cover 2 crore more families.
Long term capital gains tax has been revised to 12.5 percent.
"""

FIN_DOC_TEXT = """
The company reported total revenue of Rs. 45,000 crore for FY2024, a growth of 18 percent.
Net profit after tax stood at Rs. 6,200 crore compared to Rs. 4,800 crore last year.
The company faces significant regulatory risk due to pending litigation.
Revenue declined by 5 percent in Q3 FY2024 due to weak demand.
The audit committee noted a material weakness in internal controls.
Return on equity improved to 18.5 percent in FY2024.
"""

NEWS_TEXT = """
Prime Minister Narendra Modi inaugurated the new AIIMS hospital in Rajkot.
India's GDP growth rate is estimated at 7.6 percent for fiscal year 2023-24.
The Indian cricket team won the T20 World Cup defeating South Africa by 7 runs.
Sensex surged 800 points after the RBI kept interest rates unchanged.
Opposition parties criticized the government's handling of the unemployment crisis.
"""

BUDGET_2023 = "Fiscal deficit target was 5.9 percent of GDP. Capital expenditure was Rs. 7.5 lakh crore. Income tax exemption was Rs. 5 lakh."
BUDGET_2024 = "Fiscal deficit target is 5.1 percent of GDP. Capital expenditure is Rs. 10 lakh crore. Income tax exemption raised to Rs. 12 lakh."

METRICS = {
    "financial_metrics": [
        {"metric": "Revenue",    "amount": "Rs. 45,000 crore", "percent": None},
        {"metric": "Net Profit", "amount": "Rs. 6,200 crore",  "percent": None},
        {"metric": "ROE",        "amount": None,               "percent": "18.5"},
    ]
}

RED_FLAGS = [
    {"flag": "⚠️ Audit Qualification", "sentence": "The audit committee noted a material weakness in internal controls."},
    {"flag": "📉 Performance Decline",  "sentence": "Revenue declined by 5 percent in Q3 FY2024."},
]

CATEGORY_TAGS = {
    "Politics": ["PM Modi inaugurated AIIMS hospital."],
    "Economy":  ["GDP growth at 7.6 percent."],
    "Sports":   ["India won T20 World Cup."],
}

BIAS_DATA = {"overall_tone": "Positive", "positive_signals": 3, "negative_signals": 2, "bias_percent": 71.4}

CHAT_HISTORY = []

tests = [
    ("1. Executive Summary",        lambda: generate_executive_summary(BUDGET_TEXT)),
    ("2. Plain English",            lambda: explain_in_plain_english(BUDGET_TEXT)),
    ("3. Impact Analysis",          lambda: analyze_impact(BUDGET_TEXT)),
    ("4. Critique & Recommend",     lambda: critique_and_recommend(BUDGET_TEXT)),
    ("5. Financial Health",         lambda: financial_health_summary(FIN_DOC_TEXT, METRICS)),
    ("6. Red Flag Narrative",       lambda: red_flag_narrative(RED_FLAGS, FIN_DOC_TEXT)),
    ("7. News Brief",               lambda: generate_news_brief(NEWS_TEXT, CATEGORY_TAGS)),
    ("8. Bias Report",              lambda: generate_bias_report(NEWS_TEXT, BIAS_DATA)),
    ("9. Hindi Summary",            lambda: generate_hindi_summary(BUDGET_TEXT)),
    ("10. Q&A Chatbot",             lambda: answer_question("What is the income tax exemption limit?", BUDGET_TEXT, CHAT_HISTORY)),
    ("11. Year-on-Year Comparison", lambda: compare_two_budgets(BUDGET_2023, BUDGET_2024, "2023-24", "2024-25")),
    ("12. Sector Deep-Dive",        lambda: sector_deep_dive("Agriculture", BUDGET_TEXT)),
]

for name, fn in tests:
    print("\n" + "=" * 65)
    print(f"TEST {name}")
    print("=" * 65)
    result = fn()
    # Print first 400 chars to keep output manageable
    print(result[:400])
    print("..." if len(result) > 400 else "")
    print(f"[Response length: {len(result)} chars]")
