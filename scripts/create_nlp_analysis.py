"""
NLP Analysis Notebook Generator for PolicyLens Project
Generates comprehensive NLP analytics with visualizations and statistics
"""

import json

# Create Jupyter notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

# Cell 1: Title and Introduction
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🔍 PolicyLens - Comprehensive NLP Analysis Report\n",
        "\n",
        "## Natural Language Processing Project - Complete Analytics\n",
        "\n",
        "**Project**: PolicyLens - Policy Document Intelligence Platform  \n",
        "**Domains**: Budget Analysis, Economic Survey, Financial Documents, Newspaper Analysis, Budget Comparison  \n",
        "**NLP Techniques**: Named Entity Recognition (NER), Sentiment Analysis, Keyword Extraction, TF-IDF, Information Extraction\n",
        "\n",
        "---\n",
        "\n",
        "### 📋 Table of Contents\n",
        "1. **Setup & Data Loading**\n",
        "2. **Text Preprocessing Analytics**\n",
        "3. **Named Entity Recognition (NER) Analysis**\n",
        "4. **Sentiment Analysis with Visualizations**\n",
        "5. **Keyword Extraction & TF-IDF Analysis**\n",
        "6. **Domain 1: Financial Budget Analysis**\n",
        "7. **Domain 2: Economic Survey Analysis**\n",
        "8. **Domain 3: Financial Document Analysis**\n",
        "9. **Domain 4: Newspaper Analysis**\n",
        "10. **Domain 5: Budget Comparison Analysis**\n",
        "11. **Accuracy Validation & Quality Metrics**\n",
        "12. **Statistical Summary & Insights**\n",
        "\n",
        "---"
    ]
})

# Cell 2: Imports and Setup
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Import required libraries\n",
        "import os\n",
        "import sys\n",
        "import warnings\n",
        "warnings.filterwarnings('ignore')\n",
        "\n",
        "# Data manipulation\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "from collections import Counter, defaultdict\n",
        "import json\n",
        "\n",
        "# Visualization\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import plotly.express as px\n",
        "import plotly.graph_objects as go\n",
        "from plotly.subplots import make_subplots\n",
        "\n",
        "# NLP Libraries\n",
        "import re\n",
        "import nltk\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.tokenize import word_tokenize, sent_tokenize\n",
        "from wordcloud import WordCloud\n",
        "\n",
        "# Download NLTK data\n",
        "try:\n",
        "    nltk.data.find('tokenizers/punkt')\n",
        "except LookupError:\n",
        "    nltk.download('punkt', quiet=True)\n",
        "    nltk.download('stopwords', quiet=True)\n",
        "    nltk.download('averaged_perceptron_tagger', quiet=True)\n",
        "\n",
        "# Set plotting style\n",
        "plt.style.use('seaborn-v0_8-darkgrid')\n",
        "sns.set_palette(\"husl\")\n",
        "\n",
        "# Configure display\n",
        "pd.set_option('display.max_columns', None)\n",
        "pd.set_option('display.max_rows', 100)\n",
        "pd.set_option('display.width', 1000)\n",
        "\n",
        "print(\"✅ All libraries imported successfully!\")\n",
        "print(f\"📊 Pandas version: {pd.__version__}\")\n",
        "print(f\"📈 Matplotlib version: {plt.matplotlib.__version__}\")\n",
        "print(f\"🔤 NLTK version: {nltk.__version__}\")"
    ]
})

# Cell 3: Load Project Modules
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Add project modules to path\n",
        "sys.path.insert(0, os.path.abspath('.'))\n",
        "\n",
        "# Import PolicyLens modules\n",
        "from utils.pdf_extractor import extract_text_from_pdf\n",
        "from utils.text_cleaner import clean_text\n",
        "from utils.normalizer import normalize_text\n",
        "from utils.sentence_segmenter import segment_sentences\n",
        "from utils.ner_extractor import extract_entities, extract_entities_spacy, extract_monetary_values\n",
        "from utils.keyword_scorer import rank_sentences, get_top_keywords\n",
        "from utils.sentiment_analyzer import analyze_sentiment\n",
        "from utils.accuracy_validator import validate_extraction_accuracy, get_accuracy_summary\n",
        "\n",
        "from modules.financial_extractor import extract_financial_data\n",
        "from modules.policy_extractor import extract_policy_data\n",
        "from modules.tax_extractor import extract_tax_data\n",
        "from modules.economic_survey_extractor import extract_economic_survey_data\n",
        "from modules.financial_doc_extractor import extract_financial_doc_data\n",
        "from modules.newspaper_extractor import extract_newspaper_data\n",
        "from modules.comparison_engine import compare_budgets\n",
        "\n",
        "print(\"✅ PolicyLens modules loaded successfully!\")\n",
        "print(\"📦 Available NLP pipelines:\")\n",
        "print(\"   - Text Preprocessing (Cleaning, Normalization, Segmentation)\")\n",
        "print(\"   - Named Entity Recognition (NER)\")\n",
        "print(\"   - Sentiment Analysis\")\n",
        "print(\"   - Keyword Extraction & TF-IDF\")\n",
        "print(\"   - Domain-Specific Information Extraction\")\n",
        "print(\"   - Accuracy Validation\")"
    ]
})

# Cell 4: Sample Data Preparation
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 📂 1. Data Loading & Preparation\n",
        "\n",
        "For this analysis, we'll use sample budget text to demonstrate all NLP techniques.  \n",
        "In production, this would load actual PDF documents."
    ]
})

notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Sample Budget Speech Text (Representative of Indian Union Budget)\n",
        "sample_budget_text = \"\"\"\n",
        "Madam Speaker, I present the Union Budget for the financial year 2024-25.\n",
        "\n",
        "The total budget outlay is Rs. 47.66 lakh crore, representing a growth of 6.1 percent over the previous year.\n",
        "The fiscal deficit is estimated at 5.1 percent of GDP, down from 5.8 percent last year.\n",
        "Capital expenditure has been increased to Rs. 11.11 lakh crore, a significant boost to infrastructure development.\n",
        "\n",
        "For agriculture and allied sectors, I propose an allocation of Rs. 1.52 lakh crore.\n",
        "This includes Rs. 87,000 crore for the Pradhan Mantri Kisan Samman Nidhi scheme.\n",
        "We will establish 100 new Krishi Vigyan Kendras to promote modern farming techniques.\n",
        "\n",
        "For education and skill development, the allocation is Rs. 1.25 lakh crore.\n",
        "We will set up 50 new Eklavya Model Residential Schools in tribal areas.\n",
        "Digital literacy programs will be expanded to cover 5 crore citizens.\n",
        "\n",
        "Healthcare receives a major boost with an allocation of Rs. 89,155 crore.\n",
        "The Ayushman Bharat scheme will be expanded to cover 2 crore additional families.\n",
        "We will establish 157 new medical colleges across the country.\n",
        "\n",
        "Defence allocation stands at Rs. 6.21 lakh crore, ensuring our armed forces remain modernized.\n",
        "This includes Rs. 1.72 lakh crore for capital procurement of new equipment.\n",
        "\n",
        "Infrastructure development gets Rs. 2.75 lakh crore allocation.\n",
        "The Bharatmala project will construct 25,000 km of new highways.\n",
        "Metro rail projects in 15 cities will receive Rs. 45,000 crore.\n",
        "\n",
        "For railways, I propose Rs. 2.55 lakh crore, the highest ever allocation.\n",
        "We will introduce 50 new Vande Bharat trains connecting major cities.\n",
        "Railway electrification will be completed on 5,000 km of track.\n",
        "\n",
        "Renewable energy sector receives Rs. 35,000 crore to achieve our climate goals.\n",
        "Solar power capacity will be increased by 50 GW through rooftop installations.\n",
        "Electric vehicle adoption will be promoted with subsidies worth Rs. 10,000 crore.\n",
        "\n",
        "Housing and urban development gets Rs. 79,000 crore allocation.\n",
        "Under Pradhan Mantri Awas Yojana, we will construct 80 lakh affordable homes.\n",
        "Smart Cities Mission will be extended to 25 additional cities.\n",
        "\n",
        "Rural development receives Rs. 1.60 lakh crore for comprehensive growth.\n",
        "MGNREGA allocation is Rs. 86,000 crore to provide employment guarantee.\n",
        "Pradhan Mantri Gram Sadak Yojana will connect 25,000 villages with all-weather roads.\n",
        "\n",
        "Digital India initiatives get Rs. 18,000 crore to accelerate technology adoption.\n",
        "BharatNet will provide broadband connectivity to 2.5 lakh gram panchayats.\n",
        "Startup India program will support 10,000 new startups with funding and mentorship.\n",
        "\n",
        "Water resources management receives Rs. 70,000 crore allocation.\n",
        "Jal Jeevan Mission will provide tap water connections to 5 crore rural households.\n",
        "River cleaning projects will be initiated for 15 major rivers.\n",
        "\n",
        "MSME sector gets special attention with Rs. 22,000 crore allocation.\n",
        "MUDRA loans will be extended to 3 crore small businesses.\n",
        "Technology upgradation schemes will benefit 50,000 MSMEs.\n",
        "\n",
        "On taxation, I propose the following changes:\n",
        "Income tax exemption limit is raised to Rs. 3 lakh for individuals.\n",
        "New tax regime offers rates of 5% up to Rs. 7 lakh, 10% up to Rs. 10 lakh, and 15% up to Rs. 15 lakh.\n",
        "Corporate tax for new manufacturing companies reduced to 15 percent.\n",
        "GST compliance has been simplified with quarterly returns for small businesses.\n",
        "Customs duty on electric vehicles reduced from 100% to 70%.\n",
        "\n",
        "Social welfare programs receive Rs. 3.25 lakh crore allocation.\n",
        "Pension schemes will cover 5 crore additional senior citizens.\n",
        "Scholarship programs will benefit 2 crore students from economically weaker sections.\n",
        "\n",
        "The government remains committed to fiscal consolidation and sustainable growth.\n",
        "Revenue receipts are estimated at Rs. 30.80 lakh crore, growing at 11.5 percent.\n",
        "Tax revenue is projected at Rs. 26.02 lakh crore with improved compliance.\n",
        "Non-tax revenue stands at Rs. 4.78 lakh crore from dividends and spectrum auctions.\n",
        "\n",
        "Disinvestment target is set at Rs. 61,000 crore for the current year.\n",
        "Market borrowing will be Rs. 15.43 lakh crore to fund the fiscal deficit.\n",
        "\n",
        "This budget aims to make India a developed nation by 2047, focusing on inclusive growth,\n",
        "sustainable development, and technological advancement. We are building an Atmanirbhar Bharat\n",
        "that is self-reliant, innovative, and globally competitive.\n",
        "\n",
        "Thank you.\n",
        "\"\"\"\n",
        "\n",
        "print(\"✅ Sample budget text loaded\")\n",
        "print(f\"📄 Text length: {len(sample_budget_text)} characters\")\n",
        "print(f\"📝 Approximate words: {len(sample_budget_text.split())} words\")"
    ]
})

# Cell 5: Text Preprocessing Analytics
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 🧹 2. Text Preprocessing Analytics\n",
        "\n",
        "### NLP Pipeline Stage 1: Text Cleaning & Normalization\n",
        "\n",
        "This section demonstrates the text preprocessing pipeline with before/after statistics."
    ]
})

notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Step 1: Text Cleaning\n",
        "cleaned_text = clean_text(sample_budget_text, language=\"English\")\n",
        "\n",
        "# Step 2: Text Normalization\n",
        "normalized_text = normalize_text(cleaned_text)\n",
        "\n",
        "# Step 3: Sentence Segmentation\n",
        "sentences = segment_sentences(normalized_text, language=\"English\")\n",
        "\n",
        "# Preprocessing Statistics\n",
        "preprocessing_stats = {\n",
        "    \"Original Text Length\": len(sample_budget_text),\n",
        "    \"Cleaned Text Length\": len(cleaned_text),\n",
        "    \"Normalized Text Length\": len(normalized_text),\n",
        "    \"Total Sentences\": len(sentences),\n",
        "    \"Average Sentence Length\": np.mean([len(s.split()) for s in sentences]),\n",
        "    \"Median Sentence Length\": np.median([len(s.split()) for s in sentences]),\n",
        "    \"Longest Sentence\": max([len(s.split()) for s in sentences]),\n",
        "    \"Shortest Sentence\": min([len(s.split()) for s in sentences]),\n",
        "    \"Total Words\": len(normalized_text.split()),\n",
        "    \"Unique Words\": len(set(normalized_text.lower().split())),\n",
        "    \"Vocabulary Richness\": len(set(normalized_text.lower().split())) / len(normalized_text.split())\n",
        "}\n",
        "\n",
        "# Display statistics\n",
        "preprocessing_df = pd.DataFrame(list(preprocessing_stats.items()), \n",
        "                                columns=['Metric', 'Value'])\n",
        "print(\"\\n📊 TEXT PREPROCESSING STATISTICS\")\n",
        "print(\"=\" * 60)\n",
        "print(preprocessing_df.to_string(index=False))\n",
        "\n",
        "# Visualize preprocessing impact\n",
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
        "\n",
        "# Chart 1: Text length comparison\n",
        "lengths = [preprocessing_stats[\"Original Text Length\"], \n",
        "           preprocessing_stats[\"Cleaned Text Length\"],\n",
        "           preprocessing_stats[\"Normalized Text Length\"]]\n",
        "stages = ['Original', 'Cleaned', 'Normalized']\n",
        "colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']\n",
        "axes[0].bar(stages, lengths, color=colors, alpha=0.7, edgecolor='black')\n",
        "axes[0].set_title('Text Length Across Preprocessing Stages', fontsize=12, fontweight='bold')\n",
        "axes[0].set_ylabel('Character Count')\n",
        "axes[0].grid(axis='y', alpha=0.3)\n",
        "\n",
        "# Chart 2: Sentence length distribution\n",
        "sentence_lengths = [len(s.split()) for s in sentences]\n",
        "axes[1].hist(sentence_lengths, bins=20, color='#95E1D3', alpha=0.7, edgecolor='black')\n",
        "axes[1].axvline(preprocessing_stats[\"Average Sentence Length\"], \n",
        "                color='red', linestyle='--', linewidth=2, label=f'Mean: {preprocessing_stats[\"Average Sentence Length\"]:.1f}')\n",
        "axes[1].axvline(preprocessing_stats[\"Median Sentence Length\"], \n",
        "                color='blue', linestyle='--', linewidth=2, label=f'Median: {preprocessing_stats[\"Median Sentence Length\"]:.1f}')\n",
        "axes[1].set_title('Sentence Length Distribution', fontsize=12, fontweight='bold')\n",
        "axes[1].set_xlabel('Words per Sentence')\n",
        "axes[1].set_ylabel('Frequency')\n",
        "axes[1].legend()\n",
        "axes[1].grid(axis='y', alpha=0.3)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print(f\"\\n✅ Preprocessing complete: {len(sentences)} sentences extracted\")"
    ]
})

# Save the notebook
with open('NLP.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ NLP.ipynb notebook created successfully!")
print("📍 Location: policylens/NLP.ipynb")
print("🚀 Open it with Jupyter Notebook or JupyterLab to run the analysis")
