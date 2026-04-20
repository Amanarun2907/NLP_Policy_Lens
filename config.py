import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = "llama-3.3-70b-versatile"

# ── Document types
DOC_TYPES = [
    "Financial Budget",
    "Economic Survey",
    "Financial Document",
    "Newspaper Analysis",
]

# ── Supported languages
LANGUAGES = ["English", "Hindi"]

# ── spaCy model
SPACY_MODEL_EN = "en_core_web_sm"

# ── Output directories
OUTPUT_DIR  = "outputs"
CHARTS_DIR  = "outputs/charts"
EXPORTS_DIR = "outputs/exports"

# ── App meta
APP_TITLE   = "PolicyLens"
APP_ICON    = "🔍"
APP_TAGLINE = "Transform complex policy documents into structured insights"
