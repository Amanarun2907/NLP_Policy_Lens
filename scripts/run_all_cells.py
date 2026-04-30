#!/usr/bin/env python
"""Run all NLP notebook cells and display outputs"""

import sys
sys.path.insert(0, '.')

print("="*70)
print("🚀 RUNNING ALL NLP ANALYSIS CELLS")
print("="*70)
print()

# CELL 1: Import Libraries
print("📦 CELL 1: Importing Libraries...")
print("-"*70)
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

from utils.text_cleaner import clean_text
from utils.normalizer import normalize_text
from utils.sentence_segmenter import segment_sentences
from utils.ner_extractor import extract_entities, extract_monetary_values
from utils.keyword_scorer import rank_sentences, get_top_keywords
from utils.sentiment_analyzer import analyze_sentiment
from modules.financial_extractor import extract_financial_data
from modules.policy_extractor import extract_policy_data
from modules.tax_extractor import extract_tax_data

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
print("✅ All libraries loaded successfully!")
print()

# CELL 2: Load Sample Data
print("📄 CELL 2: Loading Sample Budget Text...")
print("-"*70)
sample_budget_text = """
Madam Speaker, I present the Union Budget for the financial year 2024-25.

The total budget outlay is Rs. 47.66 lakh crore, representing a growth of 6.1 percent over the previous year.
The fiscal deficit is estimated at 5.1 percent of GDP, down from 5.8 percent last year.
Capital expenditure has been increased to Rs. 11.11 lakh crore, a significant boost to infrastructure development.

For agriculture and allied sectors, I propose an allocation of Rs. 1.52 lakh crore.
This includes Rs. 87,000 crore for the Pradhan Mantri Kisan Samman Nidhi scheme.

For education and skill development, the allocation is Rs. 1.25 lakh crore.
Healthcare receives a major boost with an allocation of Rs. 89,155 crore.
Defence allocation stands at Rs. 6.21 lakh crore.
Infrastructure development gets Rs. 2.75 lakh crore allocation.
For railways, I propose Rs. 2.55 lakh crore.
Renewable energy sector receives Rs. 35,000 crore.
Housing and urban development gets Rs. 79,000 crore allocation.
Rural development receives Rs. 1.60 lakh crore.
Digital India initiatives get Rs. 18,000 crore.
Water resources management receives Rs. 70,000 crore allocation.
MSME sector gets Rs. 22,000 crore allocation.
Social welfare programs receive Rs. 3.25 lakh crore allocation.

On taxation, I propose the following changes:
Income tax exemption limit is raised to Rs. 3 lakh for individuals.
Corporate tax for new manufacturing companies reduced to 15 percent.
GST compliance has been simplified with quarterly returns for small businesses.

Thank you.
"""
print(f"✅ Budget text loaded: {len(sample_budget_text)} characters")
print()

# CELL 3: Text Preprocessing
print("🧹 CELL 3: Text Preprocessing...")
print("-"*70)
cleaned_text = clean_text(sample_budget_text, 'English')
normalized_text = normalize_text(cleaned_text)
sentences = segment_sentences(normalized_text, 'English')

print(f"✅ Preprocessing Complete:")
print(f"   • Total Sentences: {len(sentences)}")
print(f"   • Total Words: {len(normalized_text.split())}")
print(f"   • Unique Words: {len(set(normalized_text.lower().split()))}")
print(f"   • Avg Sentence Length: {len(normalized_text.split())/len(sentences):.1f} words")
print()

# CELL 4: Named Entity Recognition
print("🏷️  CELL 4: Named Entity Recognition...")
print("-"*70)
entities = extract_entities(sentences)
monetary_values = extract_monetary_values(sentences)

print(f"✅ NER Results:")
print(f"   • Monetary Values: {len(monetary_values)}")
print(f"   • Sectors: {len(entities.get('sectors', []))}")
print(f"   • Dates: {len(entities.get('dates', []))}")
print(f"   • Organizations: {len(entities.get('organizations', []))}")
print(f"\n   Sample Monetary Values:")
for i, mv in enumerate(monetary_values[:5], 1):
    print(f"   {i}. {mv.get('value_text', 'N/A')}")
print()

# CELL 5: Sentiment Analysis
print("😊 CELL 5: Sentiment Analysis...")
print("-"*70)
sentiment_result = analyze_sentiment(normalized_text)

print(f"✅ Sentiment Analysis Results:")
print(f"   • Overall Sentiment: {sentiment_result['label']}")
print(f"   • Sentiment Score: {sentiment_result['score']:.3f} (Range: -1 to +1)")
print(f"   • Positive Sentences: {sentiment_result['positive']} ({sentiment_result['positive']/sentiment_result['total']*100:.1f}%)")
print(f"   • Negative Sentences: {sentiment_result['negative']} ({sentiment_result['negative']/sentiment_result['total']*100:.1f}%)")
print(f"   • Neutral Sentences: {sentiment_result['neutral']} ({sentiment_result['neutral']/sentiment_result['total']*100:.1f}%)")
print()

# CELL 6: Keyword Extraction
print("🔤 CELL 6: Keyword Extraction & TF-IDF...")
print("-"*70)
top_keywords = get_top_keywords(sentences, top_n=20)
ranked_sentences = rank_sentences(sentences, top_n=10)

print(f"✅ Keyword Extraction Results:")
print(f"   • Total Keywords: {len(top_keywords)}")
print(f"\n   Top 10 Keywords:")
for i, kw in enumerate(top_keywords[:10], 1):
    print(f"   {i}. {kw['keyword']:.<20} Frequency: {kw['frequency']:>3}  Score: {kw['score']:>6.1f}")
print()

# CELL 7: Word Cloud Generation
print("☁️  CELL 7: Generating Word Cloud...")
print("-"*70)
wordcloud_text = ' '.join([kw['keyword'] for kw in top_keywords for _ in range(kw['frequency'])])
wordcloud = WordCloud(width=1200, height=600, background_color='white',
                      colormap='viridis', max_words=50).generate(wordcloud_text)

plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Budget Speech Word Cloud', fontsize=20, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('wordcloud.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Word cloud saved as 'wordcloud.png'")
print()

# CELL 8: Financial Budget Analysis
print("💰 CELL 8: Financial Budget Analysis...")
print("-"*70)
financial_data = extract_financial_data(sentences)

print(f"✅ Financial Analysis Results:")
print(f"   • Sector Allocations: {len(financial_data['sector_allocations'])}")
print(f"   • Fiscal Indicators: {len(financial_data['fiscal_indicators'])}")
print(f"   • Top Sectors: {len(financial_data['top_sectors'])}")

if financial_data['top_sectors']:
    print(f"\n   Top 10 Sectors by Allocation:")
    for i, sector in enumerate(financial_data['top_sectors'][:10], 1):
        print(f"   {i}. {sector['sector']:.<40} ₹{sector['total_crore']:>10,.2f} crore")
print()

# CELL 9: Policy & Tax Analysis
print("📜 CELL 9: Policy & Tax Extraction...")
print("-"*70)
policy_data = extract_policy_data(sentences)
tax_data = extract_tax_data(sentences)

print(f"✅ Policy & Tax Results:")
print(f"   • Policy Schemes: {len(policy_data.get('schemes', []))}")
print(f"   • Tax Changes: {len(tax_data.get('tax_changes', []))}")

if policy_data.get('schemes'):
    print(f"\n   Sample Policy Schemes:")
    for i, scheme in enumerate(policy_data['schemes'][:5], 1):
        scheme_name = scheme.get('name', scheme.get('sentence', 'Unknown'))[:60]
        print(f"   {i}. {scheme_name}")
print()

# CELL 10: Comprehensive Summary
print("📊 CELL 10: Comprehensive NLP Analysis Summary")
print("-"*70)
print(f"\n✅ TEXT PROCESSING:")
print(f"   • Sentences Analyzed: {len(sentences)}")
print(f"   • Words Processed: {len(normalized_text.split())}")
print(f"   • Vocabulary Size: {len(set(normalized_text.lower().split()))}")

print(f"\n✅ NAMED ENTITY RECOGNITION:")
print(f"   • Monetary Values: {len(monetary_values)}")
print(f"   • Sectors: {len(entities.get('sectors', []))}")
print(f"   • Total Entities: {sum([len(entities.get(k, [])) for k in entities.keys()])}")

print(f"\n✅ SENTIMENT ANALYSIS:")
print(f"   • Overall: {sentiment_result['label']}")
print(f"   • Score: {sentiment_result['score']:.3f}")
print(f"   • Positivity Rate: {sentiment_result['positive']/sentiment_result['total']*100:.1f}%")

print(f"\n✅ KEYWORD EXTRACTION:")
print(f"   • Keywords Identified: {len(top_keywords)}")
print(f"   • Top Keyword: {top_keywords[0]['keyword']} ({top_keywords[0]['frequency']} times)")

print(f"\n✅ FINANCIAL BUDGET ANALYSIS:")
print(f"   • Sector Allocations: {len(financial_data['sector_allocations'])}")
print(f"   • Fiscal Indicators: {len(financial_data['fiscal_indicators'])}")
print(f"   • Total Sectors: {len(financial_data['top_sectors'])}")

print(f"\n✅ POLICY & TAX:")
print(f"   • Policy Schemes: {len(policy_data.get('schemes', []))}")
print(f"   • Tax Changes: {len(tax_data.get('tax_changes', []))}")

print()
print("="*70)
print("🎉 ALL CELLS EXECUTED SUCCESSFULLY!")
print("="*70)
print(f"\n💯 NLP Analysis Complete:")
print(f"   ✅ 10 cells executed")
print(f"   ✅ {len(monetary_values)} extractions")
print(f"   ✅ {len(top_keywords)} keywords")
print(f"   ✅ {len(financial_data['sector_allocations'])} allocations")
print(f"   ✅ 1 word cloud generated")
print(f"\n📊 Ready for academic report submission!")
print("="*70)
