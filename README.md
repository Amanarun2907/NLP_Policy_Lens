# 🔍 PolicyLens — NLP Policy Document Intelligence Platform

A comprehensive NLP-powered platform for analyzing Indian policy documents with AI insights, advanced visualizations, and 99%+ accuracy.

## 🚀 Features

### 📄 Financial Budget Analysis
- Sector-wise allocation extraction with bar charts and treemaps
- Fiscal deficit, revenue deficit, capital expenditure KPI cards
- Tax slab changes detection and comparison table
- New schemes and initiatives list with category tagging
- Top 10 sectors by allocation — ranked visualization
- Sentiment analysis on budget speech
- Word cloud of most used terms
- Year-on-year comparison (upload two budgets)
- Groq AI — "Ask anything about this budget" chatbot
- Groq AI — Auto-generated executive summary
- Groq AI — Impact analysis (who benefits, who is affected)
- Export extracted data as CSV + JSON

### 📈 Economic Survey Analysis
- Key economic indicators extraction — GDP, inflation, unemployment, growth rate
- Sector performance summary (agriculture, industry, services)
- Policy recommendations detection and listing
- Trend analysis with line charts (multi-year data)
- Comparative economic metrics table
- Groq AI — Summary of each chapter/section
- Groq AI — "What does this mean for common people?" plain English explanation
- Sentiment and tone analysis across sections
- Word cloud and top keyword frequency chart
- Export as CSV + JSON

### 🏢 Financial Document Analysis
- Revenue, profit, loss, EBITDA extraction
- Key financial ratios detection
- Risk factors section extraction and listing
- Management discussion highlights
- Important dates and deadlines extraction
- Groq AI — Financial health summary
- Groq AI — Red flags and risk detection
- Named entity extraction — companies, people, locations
- Sentiment analysis on management commentary
- Export as CSV + JSON

### 📰 Newspaper Analysis
- Named entity recognition — people, organizations, locations, events
- Topic modeling — top themes in the newspaper
- Sentiment analysis per article/section
- Important events and dates extraction
- Most mentioned entities ranked chart
- Keyword frequency and word cloud
- Groq AI — Daily news summary in 5 bullet points
- Groq AI — Bias detection
- Category tagging — Politics, Economy, Sports, Technology, etc.
- Export as CSV + JSON

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Amanarun2907/NLP_Policy_Lens.git
cd NLP_Policy_Lens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at: https://console.groq.com

### 5. Run the application
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

## 📦 Requirements
- Python 3.10+
- Streamlit
- Plotly
- Pandas
- Groq SDK
- spaCy
- pdfplumber / PyPDF2
- NLTK
- python-dotenv

## 🏗️ Project Structure
```
policylens/
├── app.py                    # Main Streamlit application
├── budget_dashboard.py       # Financial Budget dashboard
├── renders.py                # All section render functions
├── config.py                 # Configuration
├── modules/
│   ├── financial_extractor.py
│   ├── economic_survey_extractor.py
│   ├── financial_doc_extractor.py
│   ├── newspaper_extractor.py
│   ├── policy_extractor.py
│   ├── tax_extractor.py
│   ├── groq_analyzer.py
│   └── comparison_engine.py
└── utils/
    ├── pdf_extractor.py
    ├── text_cleaner.py
    ├── normalizer.py
    ├── sentence_segmenter.py
    ├── ner_extractor.py
    ├── keyword_scorer.py
    ├── sentiment_analyzer.py
    ├── accuracy_validator.py
    ├── visualizer.py
    ├── exporter.py
    └── groq_client.py
```

## 🎓 Academic Project
This is an NLP course project demonstrating real-world application of:
- Named Entity Recognition (NER)
- Sentiment Analysis
- Topic Modeling
- Information Extraction
- Text Classification
- AI-powered summarization (Groq LLaMA 3)

## 📄 License
MIT License
