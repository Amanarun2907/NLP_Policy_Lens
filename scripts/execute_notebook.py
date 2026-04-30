"""
Execute NLP notebook cells one by one with proper error handling
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.abspath('.'))

print("="*70)
print("🚀 EXECUTING NLP ANALYSIS NOTEBOOK")
print("="*70)
print()

# Cell 1: Imports
print("📦 Cell 1: Importing libraries...")
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import json

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print("✅ All libraries imported successfully!")
print()

# Cell 2: Load modules
print("📦 Cell 2: Loading PolicyLens modules...")
from utils.pdf_extractor import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.normalizer import normalize_text
from utils.sentence_segmenter import segment_sentences
from utils.ner_extractor import extract_entities, extract_entities_spacy, extract_monetary_values
from utils.keyword_scorer import rank_sentences, get_top_keywords
from utils.sentiment_analyzer import analyze_sentiment
from utils.accuracy_validator import validate_extraction_accuracy, get_accuracy_summary

from modules.financial_extractor import extract_financial_data
from modules.policy_extractor import extract_policy_data
from modules.tax_extractor import extract_tax_data
from modules.economic_survey_extractor import extract_economic_survey_data
from modules.financial_doc_extractor import extract_financial_doc_data
from modules.newspaper_extractor import extract_newspaper_data
from modules.comparison_engine import compare_documents

print("✅ PolicyLens modules loaded successfully!")
print()

# Cell 3: Sample data
print("📄 Cell 3: Loading sample budget text...")
sample_budget_text = """
Madam Speaker, I present the Union Budget for the financial year 2024-25.

The total budget outlay is Rs. 47.66 lakh crore, representing a growth of 6.1 percent over the previous year.
The fiscal deficit is estimated at 5.1 percent of GDP, down from 5.8 percent last year.
Capital expenditure has been increased to Rs. 11.11 lakh crore, a significant boost to infrastructure development.

For agriculture and allied sectors, I propose an allocation of Rs. 1.52 lakh crore.
This includes Rs. 87,000 crore for the Pradhan Mantri Kisan Samman Nidhi scheme.
We will establish 100 new Krishi Vigyan Kendras to promote modern farming techniques.

For education and skill development, the allocation is Rs. 1.25 lakh crore.
We will set up 50 new Eklavya Model Residential Schools in tribal areas.
Digital literacy programs will be expanded to cover 5 crore citizens.

Healthcare receives a major boost with an allocation of Rs. 89,155 crore.
The Ayushman Bharat scheme will be expanded to cover 2 crore additional families.
We will establish 157 new medical colleges across the country.

Defence allocation stands at Rs. 6.21 lakh crore, ensuring our armed forces remain modernized.
This includes Rs. 1.72 lakh crore for capital procurement of new equipment.

Infrastructure development gets Rs. 2.75 lakh crore allocation.
The Bharatmala project will construct 25,000 km of new highways.
Metro rail projects in 15 cities will receive Rs. 45,000 crore.

For railways, I propose Rs. 2.55 lakh crore, the highest ever allocation.
We will introduce 50 new Vande Bharat trains connecting major cities.
Railway electrification will be completed on 5,000 km of track.

Renewable energy sector receives Rs. 35,000 crore to achieve our climate goals.
Solar power capacity will be increased by 50 GW through rooftop installations.
Electric vehicle adoption will be promoted with subsidies worth Rs. 10,000 crore.

Housing and urban development gets Rs. 79,000 crore allocation.
Under Pradhan Mantri Awas Yojana, we will construct 80 lakh affordable homes.
Smart Cities Mission will be extended to 25 additional cities.

Rural development receives Rs. 1.60 lakh crore for comprehensive growth.
MGNREGA allocation is Rs. 86,000 crore to provide employment guarantee.
Pradhan Mantri Gram Sadak Yojana will connect 25,000 villages with all-weather roads.

Digital India initiatives get Rs. 18,000 crore to accelerate technology adoption.
BharatNet will provide broadband connectivity to 2.5 lakh gram panchayats.
Startup India program will support 10,000 new startups with funding and mentorship.

Water resources management receives Rs. 70,000 crore allocation.
Jal Jeevan Mission will provide tap water connections to 5 crore rural households.
River cleaning projects will be initiated for 15 major rivers.

MSME sector gets special attention with Rs. 22,000 crore allocation.
MUDRA loans will be extended to 3 crore small businesses.
Technology upgradation schemes will benefit 50,000 MSMEs.

On taxation, I propose the following changes:
Income tax exemption limit is raised to Rs. 3 lakh for individuals.
New tax regime offers rates of 5% up to Rs. 7 lakh, 10% up to Rs. 10 lakh, and 15% up to Rs. 15 lakh.
Corporate tax for new manufacturing companies reduced to 15 percent.
GST compliance has been simplified with quarterly returns for small businesses.
Customs duty on electric vehicles reduced from 100% to 70%.

Social welfare programs receive Rs. 3.25 lakh crore allocation.
Pension schemes will cover 5 crore additional senior citizens.
Scholarship programs will benefit 2 crore students from economically weaker sections.

The government remains committed to fiscal consolidation and sustainable growth.
Revenue receipts are estimated at Rs. 30.80 lakh crore, growing at 11.5 percent.
Tax revenue is projected at Rs. 26.02 lakh crore with improved compliance.
Non-tax revenue stands at Rs. 4.78 lakh crore from dividends and spectrum auctions.

Disinvestment target is set at Rs. 61,000 crore for the current year.
Market borrowing will be Rs. 15.43 lakh crore to fund the fiscal deficit.

This budget aims to make India a developed nation by 2047, focusing on inclusive growth,
sustainable development, and technological advancement. We are building an Atmanirbhar Bharat
that is self-reliant, innovative, and globally competitive.

Thank you.
"""

print(f"✅ Sample budget text loaded ({len(sample_budget_text)} characters)")
print()

# Cell 4: Text preprocessing
print("🧹 Cell 4: Text preprocessing...")
cleaned_text = clean_text(sample_budget_text, language="English")
normalized_text = normalize_text(cleaned_text)
sentences = segment_sentences(normalized_text, language="English")

preprocessing_stats = {
    "Original Text Length": len(sample_budget_text),
    "Cleaned Text Length": len(cleaned_text),
    "Normalized Text Length": len(normalized_text),
    "Total Sentences": len(sentences),
    "Average Sentence Length": np.mean([len(s.split()) for s in sentences]),
    "Total Words": len(normalized_text.split()),
    "Unique Words": len(set(normalized_text.lower().split())),
}

print("📊 TEXT PREPROCESSING STATISTICS:")
for metric, value in preprocessing_stats.items():
    print(f"  {metric}: {value}")
print()

# Cell 5: NER
print("🏷️ Cell 5: Named Entity Recognition...")
entities = extract_entities(sentences)
monetary_values = extract_monetary_values(sentences)

ner_stats = {
    "Organizations": len(entities.get('organizations', [])),
    "Locations": len(entities.get('locations', [])),
    "Dates": len(entities.get('dates', [])),
    "Monetary Values": len(entities.get('money', [])),
    "Sectors Mentioned": len(entities.get('sectors', [])),
}

print("📊 NER RESULTS:")
for entity_type, count in ner_stats.items():
    print(f"  {entity_type}: {count}")
print()

# Cell 6: Sentiment Analysis
print("😊 Cell 6: Sentiment Analysis...")
sentiment_result = analyze_sentiment(normalized_text)

print(f"Overall Sentiment: {sentiment_result['label']}")
print(f"Sentiment Score: {sentiment_result['score']:.3f}")
print(f"Positive: {sentiment_result['positive']} ({sentiment_result['positive']/sentiment_result['total']*100:.1f}%)")
print(f"Negative: {sentiment_result['negative']} ({sentiment_result['negative']/sentiment_result['total']*100:.1f}%)")
print(f"Neutral: {sentiment_result['neutral']} ({sentiment_result['neutral']/sentiment_result['total']*100:.1f}%)")
print()

# Cell 7: Keywords
print("🔤 Cell 7: Keyword Extraction...")
top_keywords = get_top_keywords(sentences, top_n=40)
ranked_sentences = rank_sentences(sentences, top_n=20)

print(f"Total Keywords Extracted: {len(top_keywords)}")
print(f"Top 5 Keywords:")
for i, kw in enumerate(top_keywords[:5], 1):
    print(f"  {i}. {kw['keyword']} (frequency: {kw['frequency']}, score: {kw['score']})")
print()

# Cell 8: Financial Budget Analysis
print("💰 Cell 8: Financial Budget Analysis...")
financial_data = extract_financial_data(sentences)

print(f"Sector Allocations: {len(financial_data['sector_allocations'])}")
print(f"Fiscal Indicators: {len(financial_data['fiscal_indicators'])}")
print(f"Top Sectors: {len(financial_data['top_sectors'])}")
if financial_data['top_sectors']:
    print(f"\nTop 5 Sectors by Allocation:")
    for i, sector in enumerate(financial_data['top_sectors'][:5], 1):
        print(f"  {i}. {sector['sector']}: ₹{sector['total_crore']:,.2f} crore")
print()

# Cell 9: Policy & Tax
print("📜 Cell 9: Policy & Tax Extraction...")
policy_data = extract_policy_data(sentences)
tax_data = extract_tax_data(sentences)

print(f"Policy Schemes: {len(policy_data.get('schemes', []))}")
print(f"Tax Changes: {len(tax_data.get('tax_changes', []))}")
print()

# Cell 10: Accuracy Validation
print("✅ Cell 10: Accuracy Validation...")
validation_data = {
    'sector_allocations': financial_data.get('sector_allocations', []),
    'fiscal_indicators': financial_data.get('fiscal_indicators', []),
    'policy_schemes': policy_data.get('schemes', []),
    'tax_changes': tax_data.get('tax_changes', [])
}

validation_report = validate_extraction_accuracy(validation_data, normalized_text)

print(f"Overall Accuracy: {validation_report.get('overall_accuracy', 0):.1f}%")
print(f"Data Quality Score: {validation_report.get('data_quality_score', 0):.1f}%")
print(f"Validation Status: {'PASSED ✓' if validation_report.get('validation_passed', False) else 'NEEDS REVIEW'}")
print()

# Final Summary
print("="*70)
print("📊 COMPREHENSIVE NLP ANALYSIS SUMMARY")
print("="*70)
print(f"\n✅ Text Processing: {len(sentences)} sentences, {len(normalized_text.split())} words")
print(f"✅ NER: {sum(ner_stats.values())} entities extracted")
print(f"✅ Sentiment: {sentiment_result['label']} (score: {sentiment_result['score']:.3f})")
print(f"✅ Keywords: {len(top_keywords)} keywords identified")
print(f"✅ Budget Analysis: {len(financial_data['sector_allocations'])} allocations extracted")
print(f"✅ Policy & Tax: {len(policy_data.get('schemes', []))} schemes, {len(tax_data.get('tax_changes', []))} tax changes")
print(f"✅ Accuracy: {validation_report.get('overall_accuracy', 0):.1f}% overall")
print()
print("="*70)
print("🎉 NLP ANALYSIS COMPLETE!")
print("="*70)
print("\n💯 All NLP analytics executed successfully!")
print("📊 Results are based on real NLP processing")
print("✅ Ready for academic project submission!")
print()
