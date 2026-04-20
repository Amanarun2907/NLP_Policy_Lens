"""
PolicyLens - Main Streamlit Application
Dark formal theme - Complete Financial Budget Analysis
Run: streamlit run app.py
"""
import os, tempfile, json
import streamlit as st
import pandas as pd

from config import APP_TITLE, APP_ICON, APP_TAGLINE, DOC_TYPES, LANGUAGES

st.set_page_config(
    page_title="PolicyLens | Budget Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DARK FORMAL THEME CSS — COMPLETE TEXT VISIBILITY FIX
st.markdown("""
<style>
/* ══════════════════════════════════════════
   GLOBAL — force all text visible on dark bg
   ══════════════════════════════════════════ */
.stApp { background-color: #0D1117; color: #E6EDF3; }
.stApp * { color: #E6EDF3; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── All native Streamlit text elements */
p, span, div, label, li, td, th, h1, h2, h3, h4, h5, h6 { color: #E6EDF3 !important; }
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #E6EDF3 !important; }
.stText, .stCaption { color: #8B949E !important; }

/* ── Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
    border-right: 1px solid #30363D;
}
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
[data-testid="stSidebar"] label { color: #8B949E !important; font-size:13px !important; }

/* ── Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161B22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #30363D;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8B949E !important;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: #1F6FEB !important;
    color: #FFFFFF !important;
}
.stTabs [data-baseweb="tab"] p { color: #8B949E !important; }
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }

/* ── KPI / Metric cards */
.kpi-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border-top: 3px solid;
    position: relative;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-label { font-size: 12px; color: #8B949E !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.kpi-value { font-size: 26px; font-weight: 700; color: #E6EDF3 !important; line-height: 1.2; }
.kpi-sub   { font-size: 12px; color: #8B949E !important; margin-top: 4px; }

/* ── Streamlit native metric widget */
[data-testid="stMetric"] { background: #161B22; border-radius: 10px; padding: 12px; border: 1px solid #30363D; }
[data-testid="stMetricLabel"] { color: #8B949E !important; font-size: 13px !important; }
[data-testid="stMetricValue"] { color: #E6EDF3 !important; font-size: 24px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { color: #3FB950 !important; }

/* ── Section headers */
.sec-header {
    font-size: 18px; font-weight: 700; color: #E6EDF3 !important;
    border-left: 4px solid #1F6FEB;
    padding: 8px 0 8px 14px;
    margin: 24px 0 16px 0;
    background: linear-gradient(90deg, rgba(31,111,235,0.08) 0%, transparent 100%);
    border-radius: 0 8px 8px 0;
}

/* ── AI response box */
.ai-response {
    background: #161B22;
    border: 1px solid #1F6FEB;
    border-radius: 12px;
    padding: 22px 24px;
    margin-top: 14px;
    color: #E6EDF3 !important;
    font-size: 14px;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ── Sentence / info cards */
.sentence-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #C9D1D9 !important;
    line-height: 1.6;
}
.sentence-card * { color: #C9D1D9 !important; }

/* ── Tag pills */
.tag { display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; margin:2px; }
.tag-green  { background:#0D4429; color:#3FB950 !important; border:1px solid #238636; }
.tag-blue   { background:#0C2D6B; color:#58A6FF !important; border:1px solid #1F6FEB; }
.tag-red    { background:#4D1A1A; color:#F85149 !important; border:1px solid #DA3633; }
.tag-orange { background:#4D2A00; color:#F0883E !important; border:1px solid #9E6A03; }
.tag-purple { background:#2D1B69; color:#BC8CFF !important; border:1px solid #6E40C9; }

/* ── Dataframe / table — full dark theme */
.stDataFrame { border-radius: 10px; overflow: hidden; }
[data-testid="stDataFrame"] { background: #161B22 !important; }
.stDataFrame thead tr th {
    background: #1F6FEB !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 12px !important;
}
.stDataFrame tbody tr td {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    font-size: 13px !important;
    border-color: #30363D !important;
}
.stDataFrame tbody tr:nth-child(even) td { background: #0D1117 !important; }
.stDataFrame tbody tr:hover td { background: #21262D !important; }

/* ── Selectbox / dropdown */
[data-testid="stSelectbox"] label { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] { background: #161B22 !important; border-color: #30363D !important; border-radius: 8px !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #E6EDF3 !important; background: #161B22 !important; }
[data-baseweb="popover"] { background: #161B22 !important; border: 1px solid #30363D !important; }
[data-baseweb="popover"] li { color: #E6EDF3 !important; background: #161B22 !important; }
[data-baseweb="popover"] li:hover { background: #21262D !important; }

/* ── Text input / textarea */
.stTextInput label { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }
.stTextInput input {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    border-color: #30363D !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}
.stTextInput input:focus { border-color: #1F6FEB !important; box-shadow: 0 0 0 2px rgba(31,111,235,0.2) !important; }
.stTextArea label { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }
.stTextArea textarea {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    border-color: #30363D !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}

/* ── Number input */
.stNumberInput label { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }
.stNumberInput input { background: #161B22 !important; color: #E6EDF3 !important; border-color: #30363D !important; border-radius: 8px !important; }

/* ── Slider */
.stSlider label { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] { color: #8B949E !important; }
.stSlider [data-baseweb="slider"] div { background: #30363D !important; }

/* ── Checkbox / Radio */
.stCheckbox label, .stRadio label { color: #E6EDF3 !important; font-size: 14px !important; }
.stRadio [data-testid="stWidgetLabel"] { color: #8B949E !important; font-size: 13px !important; font-weight: 600 !important; }

/* ── Expander */
.streamlit-expanderHeader {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    border-radius: 8px !important;
    border: 1px solid #30363D !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
.streamlit-expanderHeader:hover { background: #21262D !important; }
.streamlit-expanderContent {
    background: #0D1117 !important;
    border: 1px solid #30363D !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 12px 16px !important;
}
.streamlit-expanderContent * { color: #E6EDF3 !important; }

/* ── Alert boxes */
[data-testid="stAlert"] { border-radius: 8px !important; font-size: 14px !important; }
.stSuccess, [data-testid="stAlert"][kind="success"] {
    background: #0D4429 !important; color: #3FB950 !important;
    border: 1px solid #238636 !important;
}
.stInfo, [data-testid="stAlert"][kind="info"] {
    background: #0C2D6B !important; color: #58A6FF !important;
    border: 1px solid #1F6FEB !important;
}
.stWarning, [data-testid="stAlert"][kind="warning"] {
    background: #4D2A00 !important; color: #F0883E !important;
    border: 1px solid #9E6A03 !important;
}
.stError, [data-testid="stAlert"][kind="error"] {
    background: #4D1A1A !important; color: #F85149 !important;
    border: 1px solid #DA3633 !important;
}
.stSuccess *, .stInfo *, .stWarning *, .stError * { color: inherit !important; }

/* ── Chat messages */
[data-testid="stChatMessage"] {
    background: #161B22 !important;
    border-radius: 10px !important;
    border: 1px solid #30363D !important;
    padding: 12px 16px !important;
}
[data-testid="stChatMessage"] * { color: #E6EDF3 !important; }
[data-testid="stChatInput"] textarea {
    background: #161B22 !important;
    color: #E6EDF3 !important;
    border-color: #30363D !important;
}

/* ── Spinner */
.stSpinner > div { border-top-color: #1F6FEB !important; }

/* ── Progress bar */
.stProgress > div > div { background: #1F6FEB !important; }

/* ── Buttons */
.stButton > button {
    background: #1F6FEB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
}
.stButton > button:hover { background: #388BFD !important; }
.stButton > button p { color: #FFFFFF !important; }

/* ── Download buttons */
.stDownloadButton > button {
    background: #161B22 !important;
    color: #58A6FF !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover { border-color: #58A6FF !important; }
.stDownloadButton > button p { color: #58A6FF !important; }

/* ── Divider */
hr { border-color: #30363D !important; }

/* ── Caption text */
.stCaption, [data-testid="stCaptionContainer"] { color: #8B949E !important; font-size: 12px !important; }

/* ── File uploader */
[data-testid="stFileUploader"] label { color: #8B949E !important; font-size: 13px !important; }
[data-testid="stFileUploadDropzone"] {
    background: #161B22 !important;
    border: 2px dashed #30363D !important;
    border-radius: 8px !important;
    color: #8B949E !important;
}
[data-testid="stFileUploadDropzone"] * { color: #8B949E !important; }

/* ── Plotly chart containers */
.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* ── Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #58A6FF; }

/* ── Column containers */
[data-testid="column"] { padding: 0 6px !important; }

/* ── Markdown headers */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #E6EDF3 !important;
    font-weight: 700 !important;
}
.stMarkdown strong, .stMarkdown b { color: #E6EDF3 !important; font-weight: 700 !important; }
.stMarkdown em, .stMarkdown i { color: #C9D1D9 !important; }
.stMarkdown code {
    background: #21262D !important;
    color: #F0883E !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 13px !important;
}
.stMarkdown a { color: #58A6FF !important; }
.stMarkdown a:hover { color: #79C0FF !important; }
.stMarkdown ul li, .stMarkdown ol li { color: #C9D1D9 !important; margin-bottom: 4px !important; }
.stMarkdown blockquote { border-left: 3px solid #1F6FEB !important; padding-left: 12px !important; color: #8B949E !important; }

/* ── Table (markdown tables) */
.stMarkdown table { border-collapse: collapse !important; width: 100% !important; }
.stMarkdown table th {
    background: #1F6FEB !important; color: #FFFFFF !important;
    padding: 10px 14px !important; font-weight: 700 !important;
    border: 1px solid #30363D !important;
}
.stMarkdown table td {
    background: #161B22 !important; color: #E6EDF3 !important;
    padding: 8px 14px !important; border: 1px solid #30363D !important;
}
.stMarkdown table tr:nth-child(even) td { background: #0D1117 !important; }
.stMarkdown table tr:hover td { background: #21262D !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px 0">
        <div style="font-size:32px">🔍</div>
        <div style="font-size:20px;font-weight:700;color:#E6EDF3">PolicyLens</div>
        <div style="font-size:12px;color:#8B949E;margin-top:4px">Budget Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    doc_type = st.selectbox("📄 Document Type", DOC_TYPES)
    language = st.selectbox("🌐 Language", LANGUAGES)
    st.divider()

    uploaded = st.file_uploader(
        "📂 Upload PDF Document", type=["pdf"],
        help="Upload budget speech, economic survey, annual report, or newspaper PDF",
    )

    if doc_type == "Financial Budget":
        st.divider()
        st.markdown('<div style="font-size:13px;font-weight:600;color:#8B949E;margin-bottom:8px">📅 YEAR-ON-YEAR COMPARISON</div>', unsafe_allow_html=True)
        uploaded2 = st.file_uploader("Upload 2nd Budget PDF", type=["pdf"], key="pdf2",
                                     help="Upload a second budget for side-by-side comparison")
        c1, c2 = st.columns(2)
        year1 = c1.text_input("Year 1", "2023-24")
        year2 = c2.text_input("Year 2", "2024-25")
    else:
        uploaded2 = None
        year1, year2 = "", ""

    st.divider()
    st.markdown('<div style="font-size:11px;color:#8B949E;text-align:center">💡 Try with Union Budget 2016-17 PDF</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════
if not uploaded:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px 0">
        <div style="font-size:48px">🔍</div>
        <div style="font-size:36px;font-weight:700;color:#E6EDF3;margin:12px 0 8px 0">PolicyLens</div>
        <div style="font-size:16px;color:#8B949E">Transform complex policy documents into structured insights</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    cards = [
        ("📄", "Financial Budget", "#1F6FEB",
         "Sector allocations • Fiscal indicators • Tax changes • Policy schemes • AI insights"),
        ("📈", "Economic Survey", "#238636",
         "Macro indicators • Sector performance • Policy recommendations • Trend analysis"),
        ("🏢", "Financial Document", "#9E6A03",
         "Revenue & profit • Risk factors • Red flags • Management highlights"),
        ("📰", "Newspaper Analysis", "#8957E5",
         "Named entities • Category tagging • Events • Bias detection • Daily summary"),
    ]
    for col, (icon, title, color, desc) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="background:#161B22;border:1px solid #30363D;border-top:3px solid {color};
            border-radius:12px;padding:20px;height:160px">
                <div style="font-size:24px">{icon}</div>
                <div style="font-size:15px;font-weight:700;color:#E6EDF3;margin:8px 0 6px 0">{title}</div>
                <div style="font-size:12px;color:#8B949E;line-height:1.6">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#161B22;border:1px solid #1F6FEB;border-radius:12px;padding:20px;text-align:center">
        <span style="color:#58A6FF;font-size:15px">👈 Select document type and upload a PDF from the sidebar to begin analysis</span>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════
# PROCESS PDF
# ══════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def process_pdf(file_bytes: bytes, doc_type: str, language: str) -> dict:
    from utils.pdf_extractor      import extract_text_from_pdf
    from utils.text_cleaner       import clean_text
    from utils.normalizer         import normalize_text
    from utils.sentence_segmenter import segment_sentences
    from utils.ner_extractor      import extract_entities, extract_monetary_values
    from utils.keyword_scorer     import rank_sentences, get_top_keywords
    from utils.sentiment_analyzer import analyze_sentiment
    from utils.accuracy_validator import validate_extraction_accuracy, get_accuracy_summary

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(file_bytes)
        tmp_path = f.name

    raw    = extract_text_from_pdf(tmp_path, language)
    clean  = clean_text(raw["full_text"], language)
    norm   = normalize_text(clean)
    sents  = segment_sentences(norm, language)
    ents   = extract_entities(sents)
    money  = extract_monetary_values(sents)
    ranked = rank_sentences(sents, top_n=50)
    kws    = get_top_keywords(sents, top_n=40)
    senti  = analyze_sentiment(norm)
    os.unlink(tmp_path)

    result = {
        "raw": raw, "clean_text": clean, "norm_text": norm,
        "sentences": sents, "entities": ents, "money": money,
        "ranked": ranked, "keywords": kws, "sentiment": senti,
    }

    if doc_type == "Financial Budget":
        from modules.financial_extractor import extract_financial_data
        from modules.policy_extractor    import extract_policy_data
        from modules.tax_extractor       import extract_tax_data
        result["financial"] = extract_financial_data(sents)
        result["policy"]    = extract_policy_data(sents)
        result["tax"]       = extract_tax_data(sents)
        
        # Validate extraction accuracy for financial budget
        validation_report = validate_extraction_accuracy({
            "sector_allocations": result["financial"].get("sector_allocations", []),
            "fiscal_indicators": result["financial"].get("fiscal_indicators", []),
            "policy_schemes": result["policy"].get("schemes", []),
            "tax_changes": result["tax"].get("tax_changes", [])
        }, norm)
        
        result["accuracy_validation"] = validation_report
        result["accuracy_summary"] = get_accuracy_summary(validation_report)

    elif doc_type == "Economic Survey":
        from modules.economic_survey_extractor import extract_economic_survey_data
        from modules.financial_extractor       import extract_financial_data
        result["economic"]  = extract_economic_survey_data(sents)
        result["financial"] = extract_financial_data(sents)

    elif doc_type == "Financial Document":
        from modules.financial_doc_extractor import extract_financial_doc_data
        result["fin_doc"] = extract_financial_doc_data(sents)

    elif doc_type == "Newspaper Analysis":
        from modules.newspaper_extractor import extract_newspaper_data
        result["newspaper"] = extract_newspaper_data(sents)

    return result


with st.spinner("🔍 Analysing document — extracting insights..."):
    data = process_pdf(uploaded.read(), doc_type, language)

# Enhanced status bar with accuracy information
pg = data['raw']['page_count']
sn = len(data['sentences'])
mt = data['raw']['method']
lg = data['raw']['detected_lang']

# Get accuracy information if available
accuracy_info = ""
if doc_type == "Financial Budget" and "accuracy_validation" in data:
    validation = data["accuracy_validation"]
    overall_accuracy = validation.get("overall_accuracy", 0)
    validation_passed = validation.get("validation_passed", False)
    
    accuracy_color = "#3FB950" if validation_passed else "#F85149"
    accuracy_icon = "✅" if validation_passed else "⚠️"
    accuracy_info = f'<span style="color:{accuracy_color}">{accuracy_icon} {overall_accuracy:.1f}% accuracy</span>'

st.markdown(f"""
<div style="background:#161B22;border:1px solid #238636;border-radius:8px;
padding:10px 18px;margin-bottom:16px;display:flex;gap:24px;flex-wrap:wrap;align-items:center">
<span style="color:#3FB950;font-weight:600">✅ Document Ready</span>
<span style="color:#8B949E">📄 {pg} pages</span>
<span style="color:#8B949E">📝 {sn} sentences</span>
<span style="color:#8B949E">⚙️ {mt}</span>
<span style="color:#8B949E">🌐 {lg}</span>
{accuracy_info}
</div>""", unsafe_allow_html=True)

# Show accuracy summary for financial budgets
if doc_type == "Financial Budget" and "accuracy_summary" in data:
    with st.expander("📊 Extraction Accuracy Report", expanded=False):
        st.markdown(data["accuracy_summary"])


# ══════════════════════════════════════════════
# ROUTE TO RENDER FUNCTIONS
# ══════════════════════════════════════════════
from budget_dashboard import render_budget_dashboard
from renders import _render_economic, _render_fin_doc, _render_newspaper

if doc_type == "Financial Budget":
    render_budget_dashboard(data, year1, year2, uploaded2, language)

elif doc_type == "Economic Survey":
    tabs = st.tabs(["📊 Overview","📈 Macro","🏭 Sectors","💡 Recommendations",
                    "😊 Sentiment","🔤 Keywords","🤖 AI Analysis","💬 Chatbot","📥 Export"])
    _render_economic(tabs, data, language)
    
    # Show accuracy summary for Economic Survey
    if "accuracy_validation" in data.get("economic", {}):
        with st.expander("📊 Economic Survey Accuracy Report", expanded=False):
            validation = data["economic"]["accuracy_validation"]
            overall_accuracy = validation.get("overall_accuracy", 0)
            validation_passed = validation.get("validation_passed", False)
            
            accuracy_color = "#3FB950" if validation_passed else "#F85149"
            accuracy_icon = "✅" if validation_passed else "⚠️"
            
            st.markdown(f"""
            <div style="background:#161B22;border:1px solid {accuracy_color};border-radius:8px;
            padding:12px 18px;margin-bottom:16px">
                <div style="color:{accuracy_color};font-weight:600;font-size:16px">
                    {accuracy_icon} Economic Survey Analysis Report
                </div>
                <div style="color:#E6EDF3;margin-top:8px">
                    <strong>Overall Accuracy:</strong> {overall_accuracy:.1f}%<br>
                    <strong>Validation Status:</strong> {'PASSED' if validation_passed else 'NEEDS REVIEW'}<br>
                    <strong>Data Quality:</strong> {validation.get('data_quality_score', 0):.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show component scores
            component_scores = validation.get("component_scores", {})
            if component_scores:
                st.markdown("#### Component Analysis Scores")
                cols = st.columns(len(component_scores))
                for i, (component, score) in enumerate(component_scores.items()):
                    with cols[i]:
                        st.metric(component.replace("_", " ").title(), f"{score:.1f}%")
            
            # Show issues if any
            issues = validation.get("issues", [])
            if issues:
                st.markdown("#### ⚠️ Issues Detected")
                for issue in issues[:5]:
                    st.warning(f"• {issue}")
            
            # Show recommendations
            recommendations = validation.get("recommendations", [])
            if recommendations:
                st.markdown("#### 💡 Recommendations")
                for rec in recommendations[:3]:
                    st.info(f"• {rec}")

elif doc_type == "Financial Document":
    tabs = st.tabs(["📊 Overview","💹 Metrics","⚠️ Risks","🚩 Red Flags",
                    "📋 Management","😊 Sentiment","🔤 Keywords",
                    "🤖 AI Analysis","💬 Chatbot","📥 Export"])
    _render_fin_doc(tabs, data, language)

elif doc_type == "Newspaper Analysis":
    tabs = st.tabs(["📊 Overview","📰 Categories","🎭 Events","👥 Entities",
                    "😊 Sentiment","⚖️ Bias","🔤 Keywords",
                    "🤖 AI Analysis","💬 Chatbot","📥 Export"])
    _render_newspaper(tabs, data, language)
