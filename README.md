# PolicyLens - NLP-Driven Policy Document Analysis

An NLP-driven system that reads policy documents and converts them into structured visual insights.

## 📁 Project Structure

```
NLPTK/
│
├── docs/                           # Documentation and visual assets
│   ├── flowcharts/                 # Project flowcharts and diagrams
│   │   ├── FINAL_FLOWCHART_CLEAN.png
│   │   ├── FINAL_POLICYLENS_FLOWCHART.png
│   │   ├── flowchart1_project_description.png
│   │   └── flowchart2_nlp_pipeline.png
│   └── project_docs/               # Project documentation
│       ├── NLP_README.md
│       ├── NLP_SUBMISSION_GUIDE.md
│       └── description.txt
│
├── scripts/                        # Utility scripts
│   ├── flowcharts.py              # Flowchart generation script
│   ├── pipeline.py                # Pipeline visualization script
│   └── punya.py                   # Test script
│
├── policylens/                     # Main application directory
│   ├── modules/                   # Core NLP modules
│   │   ├── __init__.py
│   │   ├── comparison_engine.py
│   │   ├── economic_survey_extractor.py
│   │   ├── financial_doc_extractor.py
│   │   ├── financial_extractor.py
│   │   ├── groq_analyzer.py
│   │   ├── newspaper_extractor.py
│   │   ├── policy_extractor.py
│   │   └── tax_extractor.py
│   │
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   ├── accuracy_validator.py
│   │   ├── comparison_viz.py
│   │   ├── exporter.py
│   │   ├── groq_client.py
│   │   ├── keyword_scorer.py
│   │   ├── ner_extractor.py
│   │   ├── normalizer.py
│   │   ├── pdf_extractor.py
│   │   ├── sentence_segmenter.py
│   │   ├── sentiment_analyzer.py
│   │   ├── text_cleaner.py
│   │   └── visualizer.py
│   │
│   ├── scripts/                   # Execution and utility scripts
│   │   ├── add_domain_analysis.py
│   │   ├── add_final_analysis.py
│   │   ├── add_remaining_domains.py
│   │   ├── build_and_execute_notebook.py
│   │   ├── build_nb.py
│   │   ├── complete_nlp_notebook.py
│   │   ├── create_nlp_analysis.py
│   │   ├── execute_notebook.py
│   │   ├── generate_all_graphs_as_images.py
│   │   ├── generate_all_nlp_graphs.py
│   │   ├── run_all_cells.py
│   │   ├── run_and_save_notebook.py
│   │   └── run_nlp_analysis.py
│   │
│   ├── tests/                     # Test files
│   │   ├── test_accuracy_validation.py
│   │   ├── test_complete.py
│   │   ├── test_phase2.py
│   │   ├── test_phase3.py
│   │   ├── test_phase4.py
│   │   ├── test_phase5_6.py
│   │   └── test_phase7.py
│   │
│   ├── notebooks/                 # Jupyter notebooks
│   │   ├── NLP.ipynb
│   │   └── NLP_COMPLETE.ipynb
│   │
│   ├── nlp_graphs/               # Generated NLP analysis graphs (PNG)
│   ├── generated_graphs/         # Generated HTML graphs and visualizations
│   ├── outputs/                  # Output files (reports, exports)
│   │
│   ├── app.py                    # Main Streamlit application
│   ├── budget_dashboard.py       # Budget dashboard module
│   ├── config.py                 # Configuration settings
│   ├── renders.py                # Rendering utilities
│   ├── setup.py                  # Setup script
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # Project README
│   ├── NLP_README.md            # NLP-specific documentation
│   ├── NLP_SUBMISSION_GUIDE.md  # Submission guide
│   ├── description.txt          # Project description
│   ├── .env                     # Environment variables
│   ├── .gitignore               # Git ignore rules
│   ├── start.bat                # Windows start script
│   └── OPEN_NOTEBOOK.bat        # Notebook launcher script
│
├── .zencoder/                    # Zencoder workflows
└── .zenflow/                     # Zenflow workflows
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Navigate to the policylens directory:
```bash
cd policylens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (if available)
   - Configure your API keys and settings

### Running the Application

**Option 1: Using the start script (Windows)**
```bash
start.bat
```

**Option 2: Using Python directly**
```bash
streamlit run app.py
```

**Option 3: Open Jupyter Notebook**
```bash
OPEN_NOTEBOOK.bat
```
or
```bash
jupyter notebook notebooks/NLP_COMPLETE.ipynb
```

## 📊 Features

- **PDF Text Extraction**: Extract text from policy documents using pdfplumber and PyPDF2
- **NLP Processing**: Advanced text analysis using spaCy and NLTK
- **Financial Extraction**: Identify sector allocations, fiscal indicators, and budget data
- **Policy Detection**: Detect new schemes and government initiatives
- **Tax Analysis**: Extract tax changes and exemptions
- **Interactive Dashboard**: Visualize insights using Streamlit and Plotly
- **Year-on-Year Comparison**: Compare budget data across years

## 🛠️ Technology Stack

- **PDF Extraction**: pdfplumber, PyPDF2, pytesseract
- **NLP Processing**: spaCy, NLTK, Regex
- **Data Handling**: Pandas, NumPy
- **Visualization**: Streamlit, Plotly, Matplotlib
- **Machine Learning**: scikit-learn (TF-IDF)

## 📖 Documentation

For detailed documentation, see:
- [NLP README](docs/project_docs/NLP_README.md)
- [Submission Guide](docs/project_docs/NLP_SUBMISSION_GUIDE.md)
- [Project Description](docs/project_docs/description.txt)

## 🧪 Testing

Run tests from the policylens directory:
```bash
cd policylens
python -m pytest tests/
```

Or run individual test files:
```bash
python tests/test_complete.py
```

## 📈 Generating Flowcharts

To regenerate project flowcharts:
```bash
python scripts/flowcharts.py
python scripts/pipeline.py
```

## 📝 License

[Add your license information here]

## 👥 Contributors

[Add contributor information here]

## 🤝 Contributing

[Add contribution guidelines here]
