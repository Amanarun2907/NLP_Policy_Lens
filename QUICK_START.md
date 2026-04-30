# 🚀 Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional)

---

## ⚡ Installation (5 minutes)

### Step 1: Navigate to the project
```bash
cd policylens
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure environment (optional)
```bash
# Copy and edit .env file if needed
cp .env.example .env
# Edit .env with your API keys
```

---

## 🎯 Running the Application

### Option 1: Windows Quick Start
```bash
# Double-click or run:
start.bat
```

### Option 2: Command Line
```bash
streamlit run app.py
```

### Option 3: Jupyter Notebook
```bash
# Double-click or run:
OPEN_NOTEBOOK.bat

# Or manually:
jupyter notebook notebooks/NLP_COMPLETE.ipynb
```

---

## 📊 Using PolicyLens

### 1. Upload a Document
- Open the Streamlit app (usually at `http://localhost:8501`)
- Click "Upload PDF" button
- Select a policy document (Budget Speech, Economic Survey, etc.)

### 2. View Analysis
The dashboard will automatically display:
- 📈 Sector allocations (bar charts)
- 💰 Fiscal indicators (KPIs)
- 📋 New schemes and initiatives
- 💵 Tax changes summary
- 📊 Year-on-year comparisons

### 3. Export Results
- Download visualizations as images
- Export data as CSV/JSON
- Generate PDF reports

---

## 🧪 Testing

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test
```bash
python tests/test_complete.py
```

### Run with verbose output
```bash
python -m pytest tests/ -v
```

---

## 📈 Generating Visualizations

### Generate flowcharts
```bash
cd ..
python scripts/flowcharts.py
```
Output: `docs/flowcharts/flowchart1_project_description.png` and `flowchart2_nlp_pipeline.png`

### Generate pipeline diagram
```bash
python scripts/pipeline.py
```
Output: `docs/flowcharts/FINAL_FLOWCHART_CLEAN.png`

### Generate NLP graphs
```bash
cd policylens
python scripts/generate_all_nlp_graphs.py
```
Output: `nlp_graphs/*.png`

---

## 🔧 Common Tasks

### Update dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear generated files
```bash
# Windows
del /q generated_graphs\*
del /q nlp_graphs\*

# Linux/Mac
rm -rf generated_graphs/*
rm -rf nlp_graphs/*
```

### Run NLP analysis
```bash
python scripts/run_nlp_analysis.py
```

### Build and execute notebook
```bash
python scripts/build_and_execute_notebook.py
```

---

## 🐛 Troubleshooting

### Issue: Module not found
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Issue: PDF extraction fails
**Solution:**
- Ensure the PDF is not password-protected
- Try OCR for scanned PDFs (pytesseract must be installed)
- Check if the PDF is corrupted

### Issue: Streamlit won't start
**Solution:**
```bash
# Check if streamlit is installed
pip show streamlit

# Reinstall if needed
pip install streamlit --upgrade
```

---

## 📚 Documentation

- **Main README**: `README.md`
- **Structure Guide**: `STRUCTURE.md`
- **NLP Documentation**: `docs/project_docs/NLP_README.md`
- **Submission Guide**: `docs/project_docs/NLP_SUBMISSION_GUIDE.md`

---

## 💡 Tips

1. **First time users**: Start with the Jupyter notebook to understand the workflow
2. **Developers**: Check `STRUCTURE.md` for detailed project organization
3. **Testing**: Always run tests after making changes
4. **Performance**: Use smaller PDFs for testing (< 50 pages)
5. **Visualization**: Generated graphs are saved automatically in `generated_graphs/`

---

## 🆘 Getting Help

1. Check the documentation in `docs/project_docs/`
2. Review the flowcharts in `docs/flowcharts/`
3. Look at example notebooks in `notebooks/`
4. Check test files in `tests/` for usage examples

---

## ⚙️ Configuration

### Environment Variables (`.env`)
```env
# API Keys (if using Groq or other services)
GROQ_API_KEY=your_api_key_here

# Application Settings
DEBUG=False
MAX_FILE_SIZE=100MB
```

### Config File (`config.py`)
Edit `config.py` to customize:
- PDF extraction settings
- NLP model parameters
- Visualization preferences
- Output formats

---

## 🎓 Learning Path

1. **Beginner**: 
   - Run `start.bat`
   - Upload a sample PDF
   - Explore the dashboard

2. **Intermediate**:
   - Open `notebooks/NLP_COMPLETE.ipynb`
   - Run cells step-by-step
   - Understand the NLP pipeline

3. **Advanced**:
   - Modify modules in `modules/`
   - Add custom extractors
   - Extend visualization options
   - Write new tests

---

## 📞 Support

For issues or questions:
1. Check existing documentation
2. Review test files for examples
3. Examine the flowcharts for workflow understanding

---

**Happy Analyzing! 🎉**
