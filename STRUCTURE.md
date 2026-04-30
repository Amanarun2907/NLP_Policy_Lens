# Project Structure Overview

## 📋 Organization Summary

This document provides a detailed overview of the reorganized project structure.

---

## 🗂️ Root Level Structure

```
NLPTK/
├── 📁 docs/                    # All documentation and visual assets
├── 📁 scripts/                 # Utility and generation scripts
├── 📁 policylens/              # Main application (core project)
├── 📁 .zencoder/               # Zencoder configuration
├── 📁 .zenflow/                # Zenflow configuration
├── 📄 README.md                # Main project README
└── 📄 STRUCTURE.md             # This file
```

---

## 📚 Documentation (`docs/`)

### `docs/flowcharts/`
Contains all project flowcharts and visual diagrams:
- `FINAL_FLOWCHART_CLEAN.png` - Clean version of the NLP pipeline
- `FINAL_POLICYLENS_FLOWCHART.png` - Complete PolicyLens flowchart
- `flowchart1_project_description.png` - Project description flowchart
- `flowchart2_nlp_pipeline.png` - Detailed NLP pipeline flowchart

### `docs/project_docs/`
Contains project documentation:
- `NLP_README.md` - NLP-specific documentation
- `NLP_SUBMISSION_GUIDE.md` - Submission guidelines
- `description.txt` - Project description

---

## 🔧 Scripts (`scripts/`)

Utility scripts for project maintenance:
- `flowcharts.py` - Generates project flowcharts (2 detailed flowcharts)
- `pipeline.py` - Generates pipeline visualization
- `punya.py` - Test/utility script

**Usage:**
```bash
python scripts/flowcharts.py    # Generate flowcharts
python scripts/pipeline.py      # Generate pipeline diagram
```

---

## 🎯 Main Application (`policylens/`)

### Core Application Files
- `app.py` - Main Streamlit application entry point
- `budget_dashboard.py` - Budget dashboard module
- `config.py` - Configuration settings
- `renders.py` - Rendering utilities
- `setup.py` - Package setup script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked in git)
- `.gitignore` - Git ignore rules

### Launch Scripts
- `start.bat` - Windows launcher for the application
- `OPEN_NOTEBOOK.bat` - Opens Jupyter notebooks

---

## 📦 Modules (`policylens/modules/`)

Core NLP processing modules:

| Module | Purpose |
|--------|---------|
| `comparison_engine.py` | Compare budget data across years |
| `economic_survey_extractor.py` | Extract data from economic surveys |
| `financial_doc_extractor.py` | Extract financial document data |
| `financial_extractor.py` | Extract financial information |
| `groq_analyzer.py` | Groq API integration for analysis |
| `newspaper_extractor.py` | Extract data from news articles |
| `policy_extractor.py` | Extract policy information |
| `tax_extractor.py` | Extract tax-related information |

---

## 🛠️ Utilities (`policylens/utils/`)

Helper functions and utilities:

| Utility | Purpose |
|---------|---------|
| `accuracy_validator.py` | Validate extraction accuracy |
| `comparison_viz.py` | Comparison visualizations |
| `exporter.py` | Export data to various formats |
| `groq_client.py` | Groq API client |
| `keyword_scorer.py` | TF-IDF keyword scoring |
| `ner_extractor.py` | Named Entity Recognition |
| `normalizer.py` | Text normalization |
| `pdf_extractor.py` | PDF text extraction |
| `sentence_segmenter.py` | Sentence segmentation |
| `sentiment_analyzer.py` | Sentiment analysis |
| `text_cleaner.py` | Text cleaning and preprocessing |
| `visualizer.py` | Data visualization utilities |

---

## 📜 Scripts (`policylens/scripts/`)

Execution and utility scripts:

### Domain Analysis
- `add_domain_analysis.py` - Add domain-specific analysis
- `add_final_analysis.py` - Add final analysis layer
- `add_remaining_domains.py` - Complete domain coverage

### Notebook Management
- `build_and_execute_notebook.py` - Build and run notebooks
- `build_nb.py` - Build notebook structure
- `complete_nlp_notebook.py` - Complete NLP notebook generation
- `execute_notebook.py` - Execute Jupyter notebooks
- `run_all_cells.py` - Run all notebook cells
- `run_and_save_notebook.py` - Run and save notebooks

### Analysis & Visualization
- `create_nlp_analysis.py` - Create NLP analysis
- `run_nlp_analysis.py` - Run NLP analysis pipeline
- `generate_all_graphs_as_images.py` - Generate graph images
- `generate_all_nlp_graphs.py` - Generate all NLP graphs

---

## 🧪 Tests (`policylens/tests/`)

Test suite for validation:

| Test File | Coverage |
|-----------|----------|
| `test_accuracy_validation.py` | Accuracy validation tests |
| `test_complete.py` | Complete integration tests |
| `test_phase2.py` | Phase 2 functionality |
| `test_phase3.py` | Phase 3 functionality |
| `test_phase4.py` | Phase 4 functionality |
| `test_phase5_6.py` | Phase 5 & 6 functionality |
| `test_phase7.py` | Phase 7 functionality |

**Run tests:**
```bash
cd policylens
python -m pytest tests/
```

---

## 📓 Notebooks (`policylens/notebooks/`)

Jupyter notebooks for analysis:
- `NLP.ipynb` - Main NLP analysis notebook
- `NLP_COMPLETE.ipynb` - Complete NLP workflow notebook

**Open notebooks:**
```bash
cd policylens
jupyter notebook notebooks/
```

---

## 📊 Generated Content

### `policylens/nlp_graphs/`
PNG images of NLP analysis graphs (15 graphs):
- Sentence length histograms
- Word length distributions
- Sentiment analysis charts
- Keyword trends
- Entity type distributions
- Performance metrics
- Budget allocations
- Word clouds

### `policylens/generated_graphs/`
HTML interactive graphs and visualizations:
- Interactive Plotly charts
- HTML graph files (graph1-15)
- Word cloud images

### `policylens/outputs/`
Generated reports and exports:
- PDF reports
- CSV exports
- JSON data files

---

## 🔄 Workflow Directories

### `.zencoder/workflows/`
Zencoder workflow configurations

### `.zenflow/workflows/`
Zenflow workflow configurations

---

## 📝 Key Changes Made

### ✅ Improvements
1. **Separated concerns**: Scripts, docs, and main app are now clearly separated
2. **Better organization**: Test files in `tests/`, notebooks in `notebooks/`
3. **Cleaner root**: Only essential files at root level
4. **Documentation centralized**: All docs in `docs/` folder
5. **Generated content organized**: Graphs and outputs in dedicated folders

### 📂 File Movements
- ✓ Flowchart images → `docs/flowcharts/`
- ✓ Documentation → `docs/project_docs/`
- ✓ Generation scripts → `scripts/`
- ✓ Test files → `policylens/tests/`
- ✓ Utility scripts → `policylens/scripts/`
- ✓ Notebooks → `policylens/notebooks/`
- ✓ Generated graphs → `policylens/generated_graphs/`

---

## 🚀 Quick Navigation

| Task | Command |
|------|---------|
| Start application | `cd policylens && streamlit run app.py` |
| Run tests | `cd policylens && python -m pytest tests/` |
| Open notebook | `cd policylens && jupyter notebook notebooks/` |
| Generate flowcharts | `python scripts/flowcharts.py` |
| Install dependencies | `cd policylens && pip install -r requirements.txt` |

---

## 📌 Notes

- All Python scripts should be run from their respective directories
- Environment variables are stored in `policylens/.env`
- Generated content is gitignored (check `.gitignore`)
- Documentation is duplicated in both `docs/` and `policylens/` for convenience

---

**Last Updated:** April 30, 2026
