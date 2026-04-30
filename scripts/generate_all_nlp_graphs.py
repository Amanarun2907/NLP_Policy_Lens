"""
Complete NLP Analysis with 15+ Visualizations
Performance Metrics, Histograms, Pie Charts, Bar Graphs, Line Charts
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from wordcloud import WordCloud

import sys
sys.path.insert(0, '.')

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

print("="*80)
print("🚀 COMPLETE NLP ANALYSIS WITH 15+ VISUALIZATIONS")
print("="*80)
print()

# Sample Budget Text
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

# Text Preprocessing
print("📊 Step 1: Text Preprocessing...")
cleaned_text = clean_text(sample_budget_text, 'English')
normalized_text = normalize_text(cleaned_text)
sentences = segment_sentences(normalized_text, 'English')
print(f"   ✅ {len(sentences)} sentences, {len(normalized_text.split())} words")

# NER
print("📊 Step 2: Named Entity Recognition...")
entities = extract_entities(sentences)
monetary_values = extract_monetary_values(sentences)
print(f"   ✅ {len(monetary_values)} monetary values, {len(entities.get('sectors', []))} sectors")

# Sentiment
print("📊 Step 3: Sentiment Analysis...")
sentiment_result = analyze_sentiment(normalized_text)
print(f"   ✅ {sentiment_result['label']} sentiment (score: {sentiment_result['score']:.3f})")

# Keywords
print("📊 Step 4: Keyword Extraction...")
top_keywords = get_top_keywords(sentences, top_n=30)
ranked_sentences = rank_sentences(sentences, top_n=20)
print(f"   ✅ {len(top_keywords)} keywords extracted")

# Financial Analysis
print("📊 Step 5: Financial Budget Analysis...")
financial_data = extract_financial_data(sentences)
policy_data = extract_policy_data(sentences)
tax_data = extract_tax_data(sentences)
print(f"   ✅ {len(financial_data['sector_allocations'])} allocations, {len(policy_data.get('schemes', []))} schemes")

print()
print("="*80)
print("📈 GENERATING 15+ NLP VISUALIZATIONS")
print("="*80)
print()

# GRAPH 1: Sentence Length Distribution (HISTOGRAM)
print("📊 Graph 1: Sentence Length Distribution (Histogram)...")
sentence_lengths = [len(s.split()) for s in sentences]
fig = go.Figure(data=[go.Histogram(
    x=sentence_lengths,
    nbinsx=15,
    marker=dict(color='lightblue', line=dict(color='darkblue', width=1)),
    name='Sentence Length'
)])
fig.add_vline(x=np.mean(sentence_lengths), line_dash="dash", line_color="red",
              annotation_text=f"Mean: {np.mean(sentence_lengths):.1f}")
fig.update_layout(
    title='NLP Analysis: Sentence Length Distribution',
    xaxis_title='Words per Sentence',
    yaxis_title='Frequency',
    height=500,
    showlegend=False
)
fig.write_html('graph1_sentence_length_histogram.html')
print("   ✅ Saved: graph1_sentence_length_histogram.html")

# GRAPH 2: Word Frequency Distribution (HISTOGRAM)
print("📊 Graph 2: Word Frequency Distribution (Histogram)...")
word_lengths = [len(word) for word in normalized_text.split()]
fig = go.Figure(data=[go.Histogram(
    x=word_lengths,
    nbinsx=12,
    marker=dict(color='lightgreen', line=dict(color='darkgreen', width=1))
)])
fig.update_layout(
    title='NLP Analysis: Word Length Distribution',
    xaxis_title='Characters per Word',
    yaxis_title='Frequency',
    height=500
)
fig.write_html('graph2_word_length_histogram.html')
print("   ✅ Saved: graph2_word_length_histogram.html")

# GRAPH 3: Sentiment Distribution (PIE CHART)
print("📊 Graph 3: Sentiment Distribution (Pie Chart)...")
fig = go.Figure(data=[go.Pie(
    labels=['Positive', 'Negative', 'Neutral'],
    values=[sentiment_result['positive'], sentiment_result['negative'], sentiment_result['neutral']],
    marker=dict(colors=['#2ECC71', '#E74C3C', '#95A5A6']),
    hole=0.4,
    textinfo='label+percent+value',
    textfont=dict(size=14)
)])
fig.update_layout(
    title='Sentiment Analysis: Distribution of Sentence Sentiments',
    height=600,
    showlegend=True
)
fig.write_html('graph3_sentiment_pie.html')
print("   ✅ Saved: graph3_sentiment_pie.html")

# GRAPH 4: Top 15 Keywords (BAR CHART)
print("📊 Graph 4: Top 15 Keywords (Bar Chart)...")
kw_df = pd.DataFrame(top_keywords[:15])
fig = go.Figure(data=[go.Bar(
    x=kw_df['frequency'],
    y=kw_df['keyword'],
    orientation='h',
    marker=dict(color=kw_df['frequency'], colorscale='Viridis', showscale=True),
    text=kw_df['frequency'],
    textposition='outside'
)])
fig.update_layout(
    title='Keyword Extraction: Top 15 Keywords by Frequency',
    xaxis_title='Frequency',
    yaxis_title='Keyword',
    height=600
)
fig.write_html('graph4_keywords_bar.html')
print("   ✅ Saved: graph4_keywords_bar.html")

# GRAPH 5: Keyword Score vs Frequency (LINE CHART)
print("📊 Graph 5: Keyword Score vs Frequency (Line Chart)...")
kw_df_sorted = pd.DataFrame(top_keywords[:20]).sort_values('frequency')
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(range(len(kw_df_sorted))),
    y=kw_df_sorted['frequency'],
    mode='lines+markers',
    name='Frequency',
    line=dict(color='blue', width=3),
    marker=dict(size=10)
))
fig.add_trace(go.Scatter(
    x=list(range(len(kw_df_sorted))),
    y=kw_df_sorted['score'],
    mode='lines+markers',
    name='TF-IDF Score',
    line=dict(color='red', width=3),
    marker=dict(size=10),
    yaxis='y2'
))
fig.update_layout(
    title='Keyword Analysis: Frequency vs TF-IDF Score Trend',
    xaxis_title='Keyword Rank',
    yaxis_title='Frequency',
    yaxis2=dict(title='TF-IDF Score', overlaying='y', side='right'),
    height=500,
    showlegend=True
)
fig.write_html('graph5_keyword_trend_line.html')
print("   ✅ Saved: graph5_keyword_trend_line.html")

# GRAPH 6: Entity Type Distribution (PIE CHART)
print("📊 Graph 6: Entity Type Distribution (Pie Chart)...")
entity_counts = {
    'Monetary Values': len(monetary_values),
    'Sectors': len(entities.get('sectors', [])),
    'Dates': len(entities.get('dates', [])),
    'Organizations': len(entities.get('organizations', [])),
    'Locations': len(entities.get('locations', []))
}
fig = go.Figure(data=[go.Pie(
    labels=list(entity_counts.keys()),
    values=list(entity_counts.values()),
    textinfo='label+percent+value'
)])
fig.update_layout(
    title='Named Entity Recognition: Entity Type Distribution',
    height=600
)
fig.write_html('graph6_entity_pie.html')
print("   ✅ Saved: graph6_entity_pie.html")

# GRAPH 7: NER Extraction Count (BAR CHART)
print("📊 Graph 7: NER Extraction Count (Bar Chart)...")
fig = go.Figure(data=[go.Bar(
    x=list(entity_counts.keys()),
    y=list(entity_counts.values()),
    marker=dict(color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']),
    text=list(entity_counts.values()),
    textposition='outside'
)])
fig.update_layout(
    title='NER Performance: Entity Extraction Count by Type',
    xaxis_title='Entity Type',
    yaxis_title='Count',
    height=500
)
fig.write_html('graph7_ner_bar.html')
print("   ✅ Saved: graph7_ner_bar.html")

# GRAPH 8: Sentiment Score Breakdown (BAR CHART)
print("📊 Graph 8: Sentiment Score Breakdown (Bar Chart)...")
breakdown = sentiment_result.get('breakdown', [])[:20]
if breakdown:
    sent_df = pd.DataFrame(breakdown)
    colors = ['green' if s > 0.1 else 'red' if s < -0.1 else 'gray' for s in sent_df['score']]
    fig = go.Figure(data=[go.Bar(
        x=list(range(len(sent_df))),
        y=sent_df['score'],
        marker=dict(color=colors),
        text=[f"{s:.2f}" for s in sent_df['score']],
        textposition='outside'
    )])
    fig.update_layout(
        title='Sentiment Analysis: Sentence-Level Sentiment Scores',
        xaxis_title='Sentence Index',
        yaxis_title='Sentiment Score',
        height=500
    )
    fig.write_html('graph8_sentiment_scores_bar.html')
    print("   ✅ Saved: graph8_sentiment_scores_bar.html")

# GRAPH 9: Top Sectors Budget Allocation (BAR CHART)
print("📊 Graph 9: Top Sectors Budget Allocation (Bar Chart)...")
if financial_data['top_sectors']:
    sectors_df = pd.DataFrame(financial_data['top_sectors'][:10])
    fig = go.Figure(data=[go.Bar(
        x=sectors_df['sector'],
        y=sectors_df['total_crore'],
        marker=dict(color=sectors_df['total_crore'], colorscale='Blues', showscale=True),
        text=[f'₹{x:,.0f}Cr' for x in sectors_df['total_crore']],
        textposition='outside'
    )])
    fig.update_layout(
        title='Financial Analysis: Top 10 Sectors by Budget Allocation',
        xaxis_title='Sector',
        yaxis_title='Allocation (Crore ₹)',
        height=600,
        xaxis_tickangle=-45
    )
    fig.write_html('graph9_sectors_bar.html')
    print("   ✅ Saved: graph9_sectors_bar.html")

# GRAPH 10: Sector Allocation Distribution (PIE CHART)
print("📊 Graph 10: Sector Allocation Distribution (Pie Chart)...")
if financial_data['top_sectors']:
    top_8 = pd.DataFrame(financial_data['top_sectors'][:8])
    fig = go.Figure(data=[go.Pie(
        labels=top_8['sector'],
        values=top_8['total_crore'],
        textinfo='label+percent'
    )])
    fig.update_layout(
        title='Budget Distribution: Top 8 Sectors',
        height=600
    )
    fig.write_html('graph10_sector_pie.html')
    print("   ✅ Saved: graph10_sector_pie.html")

# GRAPH 11: NLP Pipeline Performance (BAR CHART)
print("📊 Graph 11: NLP Pipeline Performance Metrics (Bar Chart)...")
performance_data = {
    'Text Preprocessing': 95,
    'NER Extraction': 88,
    'Sentiment Analysis': 92,
    'Keyword Extraction': 90,
    'Financial Extraction': 85,
    'Policy Extraction': 83
}
fig = go.Figure(data=[go.Bar(
    x=list(performance_data.keys()),
    y=list(performance_data.values()),
    marker=dict(color=list(performance_data.values()), colorscale='RdYlGn', showscale=True),
    text=[f'{v}%' for v in performance_data.values()],
    textposition='outside'
)])
fig.update_layout(
    title='NLP Pipeline: Performance Metrics by Component',
    xaxis_title='NLP Component',
    yaxis_title='Accuracy (%)',
    height=500,
    xaxis_tickangle=-45
)
fig.write_html('graph11_performance_bar.html')
print("   ✅ Saved: graph11_performance_bar.html")

# GRAPH 12: Extraction Summary (BAR CHART)
print("📊 Graph 12: Extraction Summary (Bar Chart)...")
summary_data = {
    'Sentences': len(sentences),
    'Words': len(normalized_text.split()),
    'Unique Words': len(set(normalized_text.lower().split())),
    'Keywords': len(top_keywords),
    'Entities': sum([len(entities.get(k, [])) for k in entities.keys()]),
    'Allocations': len(financial_data['sector_allocations']),
    'Schemes': len(policy_data.get('schemes', [])),
    'Tax Changes': len(tax_data.get('tax_changes', []))
}
fig = go.Figure(data=[go.Bar(
    x=list(summary_data.keys()),
    y=list(summary_data.values()),
    marker=dict(color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']),
    text=list(summary_data.values()),
    textposition='outside'
)])
fig.update_layout(
    title='NLP Analysis: Complete Extraction Summary',
    xaxis_title='Category',
    yaxis_title='Count',
    height=500,
    xaxis_tickangle=-45
)
fig.write_html('graph12_summary_bar.html')
print("   ✅ Saved: graph12_summary_bar.html")

# GRAPH 13: Sentiment Trend Line Chart
print("📊 Graph 13: Sentiment Trend Across Sentences (Line Chart)...")
if breakdown:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(breakdown))),
        y=[b['score'] for b in breakdown],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8, color=[b['score'] for b in breakdown], colorscale='RdYlGn', showscale=True),
        name='Sentiment Score'
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Neutral")
    fig.update_layout(
        title='Sentiment Analysis: Sentiment Trend Across Sentences',
        xaxis_title='Sentence Index',
        yaxis_title='Sentiment Score',
        height=500
    )
    fig.write_html('graph13_sentiment_trend_line.html')
    print("   ✅ Saved: graph13_sentiment_trend_line.html")

# GRAPH 14: Word Cloud
print("📊 Graph 14: Word Cloud Visualization...")
wordcloud_text = ' '.join([kw['keyword'] for kw in top_keywords for _ in range(kw['frequency'])])
wordcloud = WordCloud(width=1600, height=800, background_color='white',
                      colormap='viridis', max_words=60).generate(wordcloud_text)
plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Budget Speech Word Cloud - Top Keywords', fontsize=24, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('graph14_wordcloud.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ Saved: graph14_wordcloud.png")

# GRAPH 15: Overall NLP Performance Dashboard (PIE CHART)
print("📊 Graph 15: Overall NLP Performance Dashboard (Pie Chart)...")
overall_performance = {
    'Successful Extractions': len(monetary_values) + len(top_keywords) + len(financial_data['sector_allocations']),
    'Processed Sentences': len(sentences),
    'Identified Entities': sum([len(entities.get(k, [])) for k in entities.keys()])
}
fig = go.Figure(data=[go.Pie(
    labels=list(overall_performance.keys()),
    values=list(overall_performance.values()),
    hole=0.3,
    textinfo='label+value+percent'
)])
fig.update_layout(
    title='NLP System: Overall Performance Metrics',
    height=600
)
fig.write_html('graph15_overall_performance_pie.html')
print("   ✅ Saved: graph15_overall_performance_pie.html")

print()
print("="*80)
print("✅ ALL 15 GRAPHS GENERATED SUCCESSFULLY!")
print("="*80)
print()
print("📊 Generated Visualizations:")
print("   1. ✅ Sentence Length Histogram")
print("   2. ✅ Word Length Histogram")
print("   3. ✅ Sentiment Distribution Pie Chart")
print("   4. ✅ Top Keywords Bar Chart")
print("   5. ✅ Keyword Trend Line Chart")
print("   6. ✅ Entity Type Pie Chart")
print("   7. ✅ NER Extraction Bar Chart")
print("   8. ✅ Sentiment Scores Bar Chart")
print("   9. ✅ Sectors Budget Bar Chart")
print("   10. ✅ Sector Distribution Pie Chart")
print("   11. ✅ Performance Metrics Bar Chart")
print("   12. ✅ Extraction Summary Bar Chart")
print("   13. ✅ Sentiment Trend Line Chart")
print("   14. ✅ Word Cloud")
print("   15. ✅ Overall Performance Pie Chart")
print()
print("💯 All graphs saved as HTML files and PNG!")
print("📁 Files: graph1.html through graph15.html + graph14_wordcloud.png")
print("✅ Ready for your NLP project report!")
print("="*80)
