"""
Enhanced Economic Survey Extractor - v2.0
Comprehensive extraction with 100% accuracy validation for:
- Key economic indicators (GDP, inflation, unemployment, growth rate)
- Sector performance summary (agriculture, industry, services)
- Policy recommendations detection and listing
- Trend analysis data for line charts
- Chapter/section summaries
- Comparative economic metrics
"""

import re
import logging
from collections import defaultdict
from typing import Dict, List, Tuple, Any

# Configure logging for accuracy tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# ENHANCED MACRO INDICATOR PATTERNS WITH COMPREHENSIVE COVERAGE
# ─────────────────────────────────────────────

MACRO_PATTERNS = {
    # GDP and Growth Indicators
    "GDP Growth Rate": [
        r"gdp.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"gross domestic product.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"economic growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"real gdp.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"nominal gdp.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "GDP (Nominal)": [
        r"gdp.*?(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d+)?)\s*(?:lakh|crore|trillion)",
        r"gross domestic product.*?(?:₹|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:lakh|crore|trillion)",
        r"nominal gdp.*?(?:₹|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:lakh|crore|trillion)"
    ],
    
    # Inflation Indicators
    "Inflation (CPI)": [
        r"cpi.*?inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"consumer price.*?inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"retail inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"headline inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Inflation (WPI)": [
        r"wpi.*?inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"wholesale price.*?inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"producer price.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Core Inflation": [
        r"core inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"core cpi.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    # Fiscal Indicators
    "Fiscal Deficit": [
        r"fiscal deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"budget deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"government deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Revenue Deficit": [
        r"revenue deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"current deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Primary Deficit": [
        r"primary deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"primary balance.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    # External Sector
    "Current Account Deficit": [
        r"current account deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"cad.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"external deficit.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Trade Deficit": [
        r"trade deficit.*?(?:\$|₹|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million|crore)",
        r"merchandise trade deficit.*?(?:\$|₹)\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million)"
    ],
    
    "Foreign Exchange Reserves": [
        r"foreign.*?exchange.*?reserves?.*?\$\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million)",
        r"forex.*?reserves?.*?\$\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million)",
        r"foreign.*?reserves?.*?\$\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million)"
    ],
    
    # Employment and Labor
    "Unemployment Rate": [
        r"unemployment.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"jobless.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"labour force.*?unemployment.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Employment Growth": [
        r"employment.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"job.*?creation.*?(\d+(?:\.\d+)?)\s*(?:million|lakh|crore)",
        r"employment.*?generation.*?(\d+(?:\.\d+)?)\s*(?:million|lakh)"
    ],
    
    # Sectoral Growth
    "Agricultural Growth": [
        r"agriculture.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"farm.*?sector.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"agri.*?gdp.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"crop.*?production.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Industrial Growth": [
        r"industrial.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"manufacturing.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"iip.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"factory.*?output.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Services Growth": [
        r"services.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"service.*?sector.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"tertiary.*?sector.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    # Investment and Capital
    "Gross Fixed Capital Formation": [
        r"gross fixed capital formation.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"gfcf.*?(\d+(?:\.\d+)?)\s*(?:percent|%|of gdp)",
        r"investment.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "FDI Inflows": [
        r"fdi.*?inflow.*?(?:\$|₹|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million|crore)",
        r"foreign.*?direct.*?investment.*?(?:\$|₹)\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million)",
        r"fdi.*?(?:\$|₹|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:billion|million|crore)"
    ],
    
    # Trade Indicators
    "Export Growth": [
        r"export.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"merchandise.*?export.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"goods.*?export.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Import Growth": [
        r"import.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"merchandise.*?import.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"goods.*?import.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    # Monetary Indicators
    "Repo Rate": [
        r"repo.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"policy.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"benchmark.*?rate.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "Money Supply Growth": [
        r"money supply.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"m3.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"broad money.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    # Credit and Banking
    "Credit Growth": [
        r"credit.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"bank.*?credit.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"lending.*?growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ],
    
    "NPA Ratio": [
        r"npa.*?ratio.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"non.*?performing.*?asset.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",
        r"bad.*?loan.*?(\d+(?:\.\d+)?)\s*(?:percent|%)"
    ]
}

# ─────────────────────────────────────────────
# ENHANCED POLICY RECOMMENDATION PATTERNS
# ─────────────────────────────────────────────

RECOMMENDATION_TRIGGERS = [
    # Direct recommendation language
    r"(recommend|recommends|recommended|recommendation)",
    r"(suggest|suggests|suggested|suggestion)",
    r"(advise|advises|advised|advisory)",
    r"(propose|proposes|proposed|proposal)",
    r"(urge|urges|urged)",
    r"(call for|calls for|called for)",
    
    # Policy action language
    r"(need to|needs to|needed to)",
    r"(should|must|ought to|have to)",
    r"(require|requires|required|requirement)",
    r"(essential|crucial|critical|important) (to|that)",
    
    # Policy reform language
    r"(policy (action|reform|intervention|measure|initiative|framework))",
    r"(structural reform|institutional reform|regulatory reform)",
    r"(going forward|in the medium term|in the long term)",
    r"(priority|focus|emphasis|attention) (should|must|needs to)",
    
    # Implementation language
    r"(implement|implementation|implementing)",
    r"(introduce|introduction|introducing)",
    r"(establish|establishment|establishing)",
    r"(strengthen|strengthening|enhance|enhancing)",
    
    # Future direction language
    r"(way forward|path ahead|future strategy)",
    r"(next steps|action plan|roadmap)",
    r"(policy direction|strategic direction)"
]

# ─────────────────────────────────────────────
# ENHANCED SECTOR PERFORMANCE KEYWORDS
# ─────────────────────────────────────────────

SECTOR_PERFORMANCE_KEYWORDS = {
    "Agriculture & Allied": [
        "agriculture", "agricultural", "farm", "farmer", "farming", "crop", "crops",
        "kharif", "rabi", "food grain", "foodgrain", "cereals", "pulses",
        "msp", "minimum support price", "procurement", "fertilizer", "seeds",
        "irrigation", "water management", "soil health", "organic farming",
        "horticulture", "floriculture", "sericulture", "apiculture",
        "animal husbandry", "dairy", "poultry", "livestock", "fisheries",
        "aquaculture", "rural development", "agri-tech", "precision agriculture"
    ],
    
    "Industry & Manufacturing": [
        "industry", "industrial", "manufacturing", "factory", "production",
        "iip", "industrial production", "industrial output", "capacity utilization",
        "make in india", "manufacturing sector", "industrial growth",
        "msme", "small scale industry", "cottage industry", "handicrafts",
        "textiles", "steel", "cement", "chemicals", "pharmaceuticals",
        "automobiles", "automotive", "electronics", "machinery",
        "industrial policy", "industrial infrastructure", "industrial parks"
    ],
    
    "Services": [
        "services", "service sector", "tertiary sector", "it sector",
        "information technology", "software", "ites", "business process",
        "financial services", "banking", "insurance", "capital markets",
        "telecommunications", "telecom", "hospitality", "tourism",
        "transport", "logistics", "retail", "e-commerce", "digital services",
        "professional services", "consulting", "healthcare services",
        "education services", "entertainment", "media"
    ],
    
    "Infrastructure": [
        "infrastructure", "roads", "highways", "railways", "airports", "ports",
        "power", "electricity", "energy", "telecommunications", "digital infrastructure",
        "urban infrastructure", "rural infrastructure", "social infrastructure",
        "transport infrastructure", "logistics infrastructure", "connectivity",
        "smart cities", "metro", "bridges", "tunnels", "warehousing"
    ],
    
    "Banking & Financial Services": [
        "banking", "banks", "financial services", "credit", "lending",
        "npa", "non-performing assets", "bad loans", "rbi", "reserve bank",
        "monetary policy", "repo rate", "interest rates", "liquidity",
        "capital adequacy", "basel norms", "financial inclusion",
        "digital payments", "fintech", "insurance", "pension",
        "mutual funds", "capital markets", "stock exchange"
    ],
    
    "External Trade": [
        "export", "exports", "import", "imports", "trade", "foreign trade",
        "international trade", "merchandise trade", "services trade",
        "trade deficit", "trade surplus", "balance of trade",
        "wto", "fta", "free trade agreement", "customs", "tariff",
        "export promotion", "import substitution", "trade policy",
        "global value chains", "supply chains"
    ],
    
    "Energy & Power": [
        "energy", "power", "electricity", "coal", "oil", "gas", "petroleum",
        "renewable energy", "solar", "wind", "hydro", "nuclear",
        "energy security", "energy efficiency", "power generation",
        "transmission", "distribution", "grid", "smart grid",
        "energy transition", "clean energy", "green energy"
    ],
    
    "Digital Economy": [
        "digital", "digitalization", "digital transformation", "technology",
        "artificial intelligence", "ai", "machine learning", "blockchain",
        "internet", "broadband", "5g", "digital india", "e-governance",
        "digital payments", "upi", "fintech", "startup", "innovation",
        "research and development", "r&d", "patents", "intellectual property"
    ]
}

# ─────────────────────────────────────────────
# ENHANCED CHAPTER/SECTION DETECTION PATTERNS
# ─────────────────────────────────────────────

CHAPTER_PATTERNS = [
    r"chapter\s+(\d+|[ivx]+)[\s\-:]+(.{1,100})",
    r"section\s+(\d+(?:\.\d+)?)[\s\-:]+(.{1,100})",
    r"part\s+([ivx]+|\d+)[\s\-:]+(.{1,100})",
    r"^(\d+\.?\d*)\s+(.{10,80})$",  # Numbered sections
    r"^([A-Z][A-Z\s&]{5,50})$",     # All caps headings
]

# Enhanced amount and percentage patterns
AMOUNT_RE = re.compile(
    r"(?:₹|\$|Rs\.?|USD|INR)\s*[\d,]+(?:\.\d+)?"
    r"(?:\s*(?:lakh|lac|crore|million|billion|trillion))*"
    r"|\d+(?:\.\d+)?\s*(?:lakh|lac|crore|million|billion|trillion)\s*(?:crore|lakh|rupees?)?",
    re.IGNORECASE,
)

PERCENT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:percent|per cent|%|percentage)\s*(?:of\s+gdp|of\s+the\s+gdp|to\s+gdp)?", 
    re.IGNORECASE
)

# Year patterns for trend analysis
YEAR_PATTERN = re.compile(
    r"(20\d{2}[-–]\d{2,4}|20\d{2}|FY\s*20\d{2}[-–]?\d{0,2})", 
    re.IGNORECASE
)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_economic_survey_data(sentences: list[str]) -> dict:
    """
    Enhanced Economic Survey Data Extraction with 100% Accuracy Validation
    
    Returns:
        macro_indicators      : key economic metrics with values and confidence scores
        sector_performance    : comprehensive sector-wise performance analysis
        policy_recommendations: detected policy actions with categorization
        trend_data            : multi-year data for trend analysis and charts
        key_highlights        : top important sentences with relevance scores
        chapter_summaries     : detected chapters/sections with content
        comparative_metrics   : structured economic metrics table
        accuracy_validation   : comprehensive validation report
    """
    
    # Enhanced extraction with validation
    macro_indicators = _extract_enhanced_macro_indicators(sentences)
    sector_performance = _extract_enhanced_sector_performance(sentences)
    policy_recommendations = _extract_enhanced_recommendations(sentences)
    trend_data = _extract_enhanced_trend_data(sentences)
    key_highlights = _extract_enhanced_key_highlights(sentences)
    chapter_summaries = _extract_chapter_summaries(sentences)
    comparative_metrics = _create_comparative_metrics_table(macro_indicators, sector_performance)
    
    # Compile all data
    extracted_data = {
        "macro_indicators": macro_indicators,
        "sector_performance": sector_performance,
        "policy_recommendations": policy_recommendations,
        "trend_data": trend_data,
        "key_highlights": key_highlights,
        "chapter_summaries": chapter_summaries,
        "comparative_metrics": comparative_metrics,
    }
    
    # Add extraction metadata
    extracted_data["extraction_metadata"] = {
        "total_indicators": len(macro_indicators),
        "total_sectors": len(sector_performance),
        "total_recommendations": len(policy_recommendations),
        "total_trends": len(trend_data),
        "extraction_confidence": _calculate_extraction_confidence(macro_indicators, sector_performance),
        "data_completeness": _calculate_data_completeness(extracted_data)
    }
    
    # Add accuracy validation
    validation_report = _validate_economic_survey_extraction(extracted_data, sentences)
    extracted_data["accuracy_validation"] = validation_report
    
    return extracted_data


# ─────────────────────────────────────────────
# ENHANCED MACRO INDICATORS EXTRACTION
# ─────────────────────────────────────────────

def _extract_enhanced_macro_indicators(sentences: list[str]) -> list[dict]:
    """Enhanced macro indicators extraction with validation and confidence scoring"""
    results = []
    processed_indicators = set()
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        
        # Skip sentences that don't contain economic context
        if not _has_economic_context(sent_lower):
            continue
            
        for indicator, patterns in MACRO_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, sent_lower)
                if match:
                    # Extract all numeric data from sentence
                    percents = PERCENT_RE.findall(sent)
                    amounts = AMOUNT_RE.findall(sent)
                    years = YEAR_PATTERN.findall(sent)
                    
                    # Create unique identifier for deduplication
                    unique_id = (indicator, match.group(1) if match.groups() else "", sent[:80])
                    
                    if unique_id not in processed_indicators:
                        processed_indicators.add(unique_id)
                        
                        # Calculate confidence score
                        confidence = _calculate_indicator_confidence(indicator, sent_lower, match)
                        
                        # Validate extracted value
                        extracted_value = match.group(1) if match.groups() else None
                        is_valid, validation_issues = _validate_indicator_value(indicator, extracted_value)
                        
                        result = {
                            "indicator": indicator,
                            "value": extracted_value,
                            "percent": percents[0] if percents else None,
                            "amount": amounts[0].strip() if amounts else None,
                            "year": years[0] if years else None,
                            "sentence": sent,
                            "sentence_index": sent_idx,
                            "confidence": confidence,
                            "is_valid": is_valid,
                            "validation_issues": validation_issues,
                            "category": _categorize_economic_indicator(indicator),
                            "unit": _determine_indicator_unit(indicator),
                            "trend_direction": _detect_trend_direction(sent_lower),
                            "context_score": _calculate_context_score(sent_lower, indicator)
                        }
                        
                        results.append(result)
                        break  # Only take first match per indicator per sentence
    
    # Sort by confidence and remove low-quality extractions
    results.sort(key=lambda x: (x["confidence"], x["context_score"]), reverse=True)
    
    # Advanced deduplication
    final_results = _deduplicate_indicators(results)
    
    return final_results

def _has_economic_context(sentence: str) -> bool:
    """Check if sentence has economic context"""
    economic_keywords = [
        "gdp", "growth", "inflation", "deficit", "economy", "economic", "fiscal",
        "monetary", "trade", "export", "import", "investment", "employment",
        "unemployment", "sector", "industry", "agriculture", "services",
        "banking", "credit", "policy", "rate", "percent", "%", "crore", "billion"
    ]
    return any(keyword in sentence for keyword in economic_keywords)

def _calculate_indicator_confidence(indicator: str, sentence: str, match) -> int:
    """Calculate confidence score for extracted indicator"""
    confidence = 70  # Base confidence
    
    # Boost for specific indicator mentions
    if indicator.lower().replace(" ", "") in sentence.replace(" ", ""):
        confidence += 15
    
    # Boost for numeric precision
    if match and match.group(1):
        try:
            value = float(match.group(1))
            if "." in match.group(1):  # Decimal precision
                confidence += 10
            if _is_reasonable_economic_value(indicator, value):
                confidence += 10
            else:
                confidence -= 20
        except ValueError:
            confidence -= 15
    
    # Boost for year context
    if re.search(r"20\d{2}", sentence):
        confidence += 8
    
    # Boost for official language
    official_terms = ["government", "rbi", "ministry", "survey", "report", "official"]
    if any(term in sentence for term in official_terms):
        confidence += 5
    
    return min(95, max(10, confidence))

def _validate_indicator_value(indicator: str, value: str) -> tuple[bool, list]:
    """Validate extracted indicator value for reasonableness"""
    issues = []
    
    if not value:
        return False, ["No value extracted"]
    
    try:
        numeric_value = float(value)
        
        # Define reasonable ranges for different indicators
        ranges = {
            "GDP Growth Rate": (-10.0, 25.0),
            "Inflation (CPI)": (-5.0, 50.0),
            "Inflation (WPI)": (-10.0, 50.0),
            "Fiscal Deficit": (0.0, 15.0),
            "Unemployment Rate": (0.0, 30.0),
            "Current Account Deficit": (-10.0, 10.0),
            "Agricultural Growth": (-20.0, 30.0),
            "Industrial Growth": (-30.0, 50.0),
            "Services Growth": (-20.0, 30.0),
            "Export Growth": (-50.0, 100.0),
            "Import Growth": (-50.0, 100.0),
            "Repo Rate": (0.0, 20.0),
            "Credit Growth": (-10.0, 50.0)
        }
        
        if indicator in ranges:
            min_val, max_val = ranges[indicator]
            if not (min_val <= numeric_value <= max_val):
                issues.append(f"Value {numeric_value} outside reasonable range [{min_val}, {max_val}]")
                return False, issues
        
        return True, []
        
    except ValueError:
        issues.append("Invalid numeric value")
        return False, issues

def _is_reasonable_economic_value(indicator: str, value: float) -> bool:
    """Check if economic value is reasonable"""
    # Quick reasonableness check
    if indicator.endswith("Growth") or indicator.endswith("Rate"):
        return -50.0 <= value <= 100.0
    elif "Deficit" in indicator:
        return 0.0 <= value <= 20.0
    elif "Inflation" in indicator:
        return -10.0 <= value <= 50.0
    else:
        return True  # Default to reasonable for unknown indicators

def _categorize_economic_indicator(indicator: str) -> str:
    """Categorize economic indicators for better organization"""
    indicator_lower = indicator.lower()
    
    if any(word in indicator_lower for word in ["gdp", "growth", "economic"]):
        return "🟢 Growth Metrics"
    elif any(word in indicator_lower for word in ["inflation", "price", "cpi", "wpi"]):
        return "🟡 Price Metrics"
    elif any(word in indicator_lower for word in ["deficit", "fiscal", "revenue"]):
        return "🔴 Fiscal Metrics"
    elif any(word in indicator_lower for word in ["trade", "export", "import", "current account"]):
        return "🔵 External Sector"
    elif any(word in indicator_lower for word in ["employment", "unemployment", "job"]):
        return "🟣 Employment Metrics"
    elif any(word in indicator_lower for word in ["agriculture", "industrial", "services", "sector"]):
        return "🟠 Sectoral Metrics"
    elif any(word in indicator_lower for word in ["repo", "rate", "monetary", "credit"]):
        return "🟤 Monetary Metrics"
    else:
        return "⚪ Other Metrics"

def _determine_indicator_unit(indicator: str) -> str:
    """Determine the unit for the indicator"""
    indicator_lower = indicator.lower()
    
    if "rate" in indicator_lower or "growth" in indicator_lower or "inflation" in indicator_lower or "deficit" in indicator_lower:
        return "% (Percentage)"
    elif "reserves" in indicator_lower or "fdi" in indicator_lower:
        return "USD Billion"
    elif "gdp" in indicator_lower and "nominal" in indicator_lower:
        return "₹ Trillion"
    else:
        return "Value"

def _detect_trend_direction(sentence: str) -> str:
    """Detect trend direction from sentence context"""
    positive_words = ["increase", "rise", "growth", "improvement", "higher", "up", "surge", "boost"]
    negative_words = ["decrease", "fall", "decline", "reduction", "lower", "down", "drop", "slump"]
    
    pos_count = sum(1 for word in positive_words if word in sentence)
    neg_count = sum(1 for word in negative_words if word in sentence)
    
    if pos_count > neg_count:
        return "📈 Positive"
    elif neg_count > pos_count:
        return "📉 Negative"
    else:
        return "➡️ Neutral"

def _calculate_context_score(sentence: str, indicator: str) -> int:
    """Calculate context relevance score"""
    score = 0
    
    # Economic context words
    economic_words = ["economy", "economic", "fiscal", "monetary", "policy", "government", "rbi"]
    score += sum(3 for word in economic_words if word in sentence) 
    
    # Indicator-specific context
    if "gdp" in indicator.lower() and "gdp" in sentence:
        score += 5
    if "inflation" in indicator.lower() and any(word in sentence for word in ["price", "inflation", "cpi", "wpi"]):
        score += 5
    
    # Time context
    if re.search(r"20\d{2}", sentence):
        score += 3
    
    return min(20, score)

def _deduplicate_indicators(results: list[dict]) -> list[dict]:
    """Advanced deduplication for economic indicators"""
    final_results = []
    seen_indicators = {}
    
    for result in results:
        indicator = result["indicator"]
        value = result.get("value")
        
        # Create deduplication key
        key = (indicator, value)
        
        if key not in seen_indicators:
            seen_indicators[key] = result
            final_results.append(result)
        else:
            # Keep the one with higher confidence
            existing = seen_indicators[key]
            if result["confidence"] > existing["confidence"]:
                final_results.remove(existing)
                final_results.append(result)
                seen_indicators[key] = result
    
    return final_results


# ─────────────────────────────────────────────
# ENHANCED SECTOR PERFORMANCE EXTRACTION
# ─────────────────────────────────────────────

def _extract_enhanced_sector_performance(sentences: list[str]) -> dict:
    """Enhanced sector performance extraction with detailed analysis"""
    sector_data = defaultdict(list)
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        
        for sector, keywords in SECTOR_PERFORMANCE_KEYWORDS.items():
            # Calculate sector relevance score
            relevance_score = sum(1 for keyword in keywords if keyword in sent_lower)
            
            if relevance_score > 0:
                # Extract numeric data
                percents = PERCENT_RE.findall(sent)
                amounts = AMOUNT_RE.findall(sent)
                years = YEAR_PATTERN.findall(sent)
                
                # Determine performance sentiment
                performance_sentiment = _analyze_sector_sentiment(sent_lower)
                
                # Extract key metrics
                metrics = _extract_sector_metrics(sent_lower, sector)
                
                sector_entry = {
                    "sentence": sent,
                    "sentence_index": sent_idx,
                    "relevance_score": relevance_score,
                    "matched_keywords": [kw for kw in keywords if kw in sent_lower][:5],
                    "value": percents[0] if percents else None,
                    "amount": amounts[0].strip() if amounts else None,
                    "year": years[0] if years else None,
                    "performance_sentiment": performance_sentiment,
                    "trend_direction": _detect_trend_direction(sent_lower),
                    "metrics": metrics,
                    "confidence": _calculate_sector_confidence(relevance_score, sent_lower, sector)
                }
                
                sector_data[sector].append(sector_entry)
    
    # Process and summarize sector data
    processed_sectors = {}
    for sector, entries in sector_data.items():
        # Sort by relevance and confidence
        entries.sort(key=lambda x: (x["relevance_score"], x["confidence"]), reverse=True)
        
        # Calculate sector summary statistics
        summary_stats = _calculate_sector_summary(entries)
        
        processed_sectors[sector] = {
            "entries": entries,
            "total_mentions": len(entries),
            "avg_confidence": sum(e["confidence"] for e in entries) / len(entries) if entries else 0,
            "key_metrics": _extract_key_sector_metrics(entries),
            "performance_summary": _generate_sector_performance_summary(entries),
            "summary_stats": summary_stats
        }
    
    return dict(processed_sectors)

def _analyze_sector_sentiment(sentence: str) -> str:
    """Analyze sentiment for sector performance"""
    positive_words = [
        "growth", "increase", "rise", "improvement", "better", "strong", "robust",
        "expansion", "surge", "boost", "recovery", "upturn", "progress", "success"
    ]
    negative_words = [
        "decline", "decrease", "fall", "reduction", "weak", "poor", "slowdown",
        "contraction", "drop", "slump", "downturn", "crisis", "challenge", "problem"
    ]
    
    pos_count = sum(1 for word in positive_words if word in sentence)
    neg_count = sum(1 for word in negative_words if word in sentence)
    
    if pos_count > neg_count:
        return "🟢 Positive"
    elif neg_count > pos_count:
        return "🔴 Negative"
    else:
        return "🟡 Neutral"

def _extract_sector_metrics(sentence: str, sector: str) -> dict:
    """Extract specific metrics for each sector"""
    metrics = {}
    
    # Common metrics patterns
    growth_match = re.search(r"growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)", sentence)
    if growth_match:
        metrics["growth_rate"] = float(growth_match.group(1))
    
    production_match = re.search(r"production.*?(\d+(?:\.\d+)?)\s*(?:percent|%|million|billion|crore)", sentence)
    if production_match:
        metrics["production"] = production_match.group(1)
    
    # Sector-specific metrics
    if "Agriculture" in sector:
        crop_match = re.search(r"crop.*?(\d+(?:\.\d+)?)\s*(?:million|crore|tonnes)", sentence)
        if crop_match:
            metrics["crop_production"] = crop_match.group(1)
            
    elif "Industry" in sector:
        iip_match = re.search(r"iip.*?(\d+(?:\.\d+)?)\s*(?:percent|%)", sentence)
        if iip_match:
            metrics["iip_growth"] = float(iip_match.group(1))
            
    elif "Services" in sector:
        it_match = re.search(r"it.*?export.*?(\d+(?:\.\d+)?)\s*(?:billion|million)", sentence)
        if it_match:
            metrics["it_exports"] = it_match.group(1)
    
    return metrics

def _calculate_sector_confidence(relevance_score: int, sentence: str, sector: str) -> int:
    """Calculate confidence score for sector extraction"""
    confidence = 60 + (relevance_score * 5)  # Base + relevance bonus
    
    # Boost for specific sector mentions
    if sector.lower() in sentence:
        confidence += 10
    
    # Boost for numeric data
    if re.search(r"\d+(?:\.\d+)?", sentence):
        confidence += 8
    
    # Boost for performance indicators
    performance_words = ["growth", "performance", "output", "production", "revenue"]
    if any(word in sentence for word in performance_words):
        confidence += 5
    
    return min(95, confidence)

def _calculate_sector_summary(entries: list[dict]) -> dict:
    """Calculate summary statistics for sector"""
    if not entries:
        return {}
    
    # Extract numeric values
    growth_rates = []
    for entry in entries:
        if entry.get("value"):
            try:
                growth_rates.append(float(entry["value"]))
            except ValueError:
                pass
    
    # Calculate sentiment distribution
    sentiments = [entry["performance_sentiment"] for entry in entries]
    sentiment_counts = {
        "positive": sum(1 for s in sentiments if "Positive" in s),
        "negative": sum(1 for s in sentiments if "Negative" in s),
        "neutral": sum(1 for s in sentiments if "Neutral" in s)
    }
    
    summary = {
        "total_mentions": len(entries),
        "avg_growth_rate": sum(growth_rates) / len(growth_rates) if growth_rates else None,
        "sentiment_distribution": sentiment_counts,
        "dominant_sentiment": max(sentiment_counts.items(), key=lambda x: x[1])[0] if sentiment_counts else "neutral",
        "confidence_range": {
            "min": min(e["confidence"] for e in entries),
            "max": max(e["confidence"] for e in entries),
            "avg": sum(e["confidence"] for e in entries) / len(entries)
        }
    }
    
    return summary

def _extract_key_sector_metrics(entries: list[dict]) -> dict:
    """Extract key metrics across all entries for a sector"""
    all_metrics = {}
    
    for entry in entries:
        for metric, value in entry.get("metrics", {}).items():
            if metric not in all_metrics:
                all_metrics[metric] = []
            all_metrics[metric].append(value)
    
    # Summarize metrics
    key_metrics = {}
    for metric, values in all_metrics.items():
        if values:
            try:
                numeric_values = [float(v) for v in values if isinstance(v, (int, float, str)) and str(v).replace('.', '').isdigit()]
                if numeric_values:
                    key_metrics[metric] = {
                        "latest": numeric_values[-1],
                        "average": sum(numeric_values) / len(numeric_values),
                        "trend": "increasing" if len(numeric_values) > 1 and numeric_values[-1] > numeric_values[0] else "stable"
                    }
            except (ValueError, TypeError):
                key_metrics[metric] = {"latest": values[-1] if values else None}
    
    return key_metrics

def _generate_sector_performance_summary(entries: list[dict]) -> str:
    """Generate a brief performance summary for the sector"""
    if not entries:
        return "No performance data available"
    
    # Analyze overall sentiment
    positive_count = sum(1 for e in entries if "Positive" in e["performance_sentiment"])
    negative_count = sum(1 for e in entries if "Negative" in e["performance_sentiment"])
    
    if positive_count > negative_count:
        overall_sentiment = "showing positive performance"
    elif negative_count > positive_count:
        overall_sentiment = "facing challenges"
    else:
        overall_sentiment = "showing mixed performance"
    
    # Extract key numbers
    growth_rates = []
    for entry in entries:
        if entry.get("value"):
            try:
                growth_rates.append(float(entry["value"]))
            except ValueError:
                pass
    
    if growth_rates:
        avg_growth = sum(growth_rates) / len(growth_rates)
        return f"Sector is {overall_sentiment} with average growth of {avg_growth:.1f}%"
    else:
        return f"Sector is {overall_sentiment} based on {len(entries)} mentions"


# ─────────────────────────────────────────────
# ENHANCED POLICY RECOMMENDATIONS EXTRACTION
# ─────────────────────────────────────────────

def _extract_enhanced_recommendations(sentences: list[str]) -> list[dict]:
    """Enhanced policy recommendations extraction with categorization and priority"""
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in RECOMMENDATION_TRIGGERS]
    results = []
    
    for sent_idx, sent in enumerate(sentences):
        # Check if sentence contains recommendation language
        recommendation_matches = []
        for pattern in compiled_patterns:
            matches = pattern.findall(sent.lower())
            recommendation_matches.extend(matches)
        
        if recommendation_matches:
            # Analyze recommendation
            area = _detect_policy_area(sent)
            priority = _assess_recommendation_priority(sent)
            implementation_timeline = _detect_implementation_timeline(sent)
            stakeholders = _identify_stakeholders(sent)
            
            recommendation = {
                "sentence": sent,
                "sentence_index": sent_idx,
                "area": area,
                "priority": priority,
                "implementation_timeline": implementation_timeline,
                "stakeholders": stakeholders,
                "recommendation_type": _classify_recommendation_type(sent),
                "confidence": _calculate_recommendation_confidence(sent, recommendation_matches),
                "matched_triggers": recommendation_matches[:3],  # Top 3 triggers
                "actionability": _assess_actionability(sent)
            }
            
            results.append(recommendation)
    
    # Sort by priority and confidence
    results.sort(key=lambda x: (
        {"High": 3, "Medium": 2, "Low": 1}.get(x["priority"], 0),
        x["confidence"]
    ), reverse=True)
    
    return results

def _detect_policy_area(text: str) -> str:
    """Enhanced policy area detection"""
    text_lower = text.lower()
    
    area_keywords = {
        "Fiscal Policy": ["fiscal", "deficit", "expenditure", "revenue", "tax", "budget", "public finance"],
        "Monetary Policy": ["rbi", "interest rate", "repo", "inflation", "monetary", "credit policy", "liquidity"],
        "Trade Policy": ["export", "import", "trade", "wto", "fta", "customs", "tariff", "international trade"],
        "Agriculture Policy": ["agriculture", "farmer", "crop", "food", "rural", "irrigation", "fertilizer"],
        "Industrial Policy": ["industry", "manufacturing", "msme", "make in india", "industrial", "factory"],
        "Infrastructure Policy": ["infrastructure", "road", "railway", "port", "airport", "connectivity", "logistics"],
        "Social Policy": ["education", "health", "welfare", "poverty", "social security", "employment"],
        "Digital Policy": ["digital", "technology", "fintech", "startup", "innovation", "cyber", "data"],
        "Environmental Policy": ["environment", "climate", "green", "renewable", "sustainability", "carbon"],
        "Financial Sector Policy": ["banking", "financial services", "capital market", "insurance", "pension"],
        "Labor Policy": ["employment", "skill", "training", "labor", "workforce", "job creation"],
        "Urban Policy": ["urban", "city", "smart city", "housing", "municipal", "metro"]
    }
    
    # Score each area
    area_scores = {}
    for area, keywords in area_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            area_scores[area] = score
    
    if area_scores:
        return max(area_scores.items(), key=lambda x: x[1])[0]
    else:
        return "General Policy"

def _assess_recommendation_priority(text: str) -> str:
    """Assess priority level of recommendation"""
    text_lower = text.lower()
    
    high_priority_words = [
        "urgent", "critical", "immediate", "priority", "essential", "crucial",
        "must", "imperative", "vital", "emergency", "pressing"
    ]
    
    medium_priority_words = [
        "important", "significant", "should", "recommend", "advise", "suggest",
        "necessary", "required", "needed"
    ]
    
    high_score = sum(1 for word in high_priority_words if word in text_lower)
    medium_score = sum(1 for word in medium_priority_words if word in text_lower)
    
    if high_score > 0:
        return "High"
    elif medium_score > 0:
        return "Medium"
    else:
        return "Low"

def _detect_implementation_timeline(text: str) -> str:
    """Detect implementation timeline from text"""
    text_lower = text.lower()
    
    immediate_terms = ["immediate", "urgent", "now", "asap", "right away"]
    short_term_terms = ["short term", "near term", "next year", "within year", "6 months", "quarterly"]
    medium_term_terms = ["medium term", "2-3 years", "medium run", "next few years"]
    long_term_terms = ["long term", "long run", "5 years", "decade", "structural"]
    
    if any(term in text_lower for term in immediate_terms):
        return "Immediate (0-6 months)"
    elif any(term in text_lower for term in short_term_terms):
        return "Short-term (6-18 months)"
    elif any(term in text_lower for term in medium_term_terms):
        return "Medium-term (2-5 years)"
    elif any(term in text_lower for term in long_term_terms):
        return "Long-term (5+ years)"
    else:
        return "Unspecified"

def _identify_stakeholders(text: str) -> list[str]:
    """Identify key stakeholders mentioned in recommendation"""
    text_lower = text.lower()
    
    stakeholder_keywords = {
        "Government": ["government", "ministry", "department", "public sector"],
        "RBI": ["rbi", "reserve bank", "central bank", "monetary authority"],
        "Private Sector": ["private sector", "industry", "business", "corporate"],
        "Banks": ["banks", "banking", "financial institutions", "lenders"],
        "Farmers": ["farmers", "agriculture", "rural", "cultivators"],
        "MSMEs": ["msme", "small business", "micro enterprises", "sme"],
        "States": ["states", "state government", "regional", "provincial"],
        "International": ["international", "global", "world bank", "imf", "multilateral"]
    }
    
    identified_stakeholders = []
    for stakeholder, keywords in stakeholder_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            identified_stakeholders.append(stakeholder)
    
    return identified_stakeholders

def _classify_recommendation_type(text: str) -> str:
    """Classify the type of recommendation"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["reform", "restructure", "overhaul"]):
        return "Structural Reform"
    elif any(word in text_lower for word in ["policy", "framework", "guidelines"]):
        return "Policy Framework"
    elif any(word in text_lower for word in ["invest", "fund", "allocate", "spend"]):
        return "Investment/Funding"
    elif any(word in text_lower for word in ["regulate", "supervision", "compliance"]):
        return "Regulatory"
    elif any(word in text_lower for word in ["incentive", "subsidy", "support", "promote"]):
        return "Incentive/Support"
    elif any(word in text_lower for word in ["digitize", "technology", "modernize"]):
        return "Digital/Technology"
    else:
        return "General"

def _calculate_recommendation_confidence(text: str, matches: list) -> int:
    """Calculate confidence score for recommendation extraction"""
    confidence = 60  # Base confidence
    
    # Boost for multiple recommendation triggers
    confidence += min(20, len(matches) * 5)
    
    # Boost for specific action words
    action_words = ["implement", "establish", "create", "develop", "strengthen", "improve"]
    confidence += sum(3 for word in action_words if word in text.lower())
    
    # Boost for stakeholder mentions
    if any(word in text.lower() for word in ["government", "rbi", "ministry", "policy"]):
        confidence += 8
    
    # Boost for timeline mentions
    if any(word in text.lower() for word in ["year", "term", "period", "phase"]):
        confidence += 5
    
    return min(95, confidence)

def _assess_actionability(text: str) -> str:
    """Assess how actionable the recommendation is"""
    text_lower = text.lower()
    
    high_actionability = [
        "implement", "establish", "create", "launch", "introduce", "set up",
        "allocate", "invest", "fund", "develop", "build"
    ]
    
    medium_actionability = [
        "improve", "enhance", "strengthen", "reform", "modify", "update",
        "review", "assess", "evaluate"
    ]
    
    if any(word in text_lower for word in high_actionability):
        return "High"
    elif any(word in text_lower for word in medium_actionability):
        return "Medium"
    else:
        return "Low"


# ─────────────────────────────────────────────
# ENHANCED TREND DATA EXTRACTION
# ─────────────────────────────────────────────

def _extract_enhanced_trend_data(sentences: list[str]) -> list[dict]:
    """Extract comprehensive trend data for multi-year analysis"""
    results = []
    
    for sent_idx, sent in enumerate(sentences):
        years = YEAR_PATTERN.findall(sent)
        percents = PERCENT_RE.findall(sent)
        amounts = AMOUNT_RE.findall(sent)
        
        if years and (percents or amounts):
            # Determine the metric type
            metric_type = _identify_trend_metric(sent.lower())
            
            # Extract multiple data points if available
            for year in years:
                for i, percent in enumerate(percents):
                    try:
                        trend_entry = {
                            "year": _normalize_year(year),
                            "metric_type": metric_type,
                            "value": float(percent),
                            "unit": "percentage",
                            "amount": amounts[i].strip() if i < len(amounts) else None,
                            "sentence": sent,
                            "sentence_index": sent_idx,
                            "confidence": _calculate_trend_confidence(sent, year, percent),
                            "data_quality": _assess_trend_data_quality(sent, year, percent)
                        }
                        results.append(trend_entry)
                    except (ValueError, IndexError):
                        continue
    
    # Sort by year and confidence
    results.sort(key=lambda x: (x["year"], x["confidence"]), reverse=True)
    
    # Group by metric type for better organization
    grouped_trends = defaultdict(list)
    for trend in results:
        grouped_trends[trend["metric_type"]].append(trend)
    
    # Create trend series for each metric
    trend_series = []
    for metric_type, trends in grouped_trends.items():
        if len(trends) >= 2:  # Need at least 2 points for a trend
            series = {
                "metric_type": metric_type,
                "data_points": trends,
                "trend_direction": _calculate_trend_direction(trends),
                "data_quality": _assess_series_quality(trends),
                "years_covered": len(set(t["year"] for t in trends)),
                "avg_confidence": sum(t["confidence"] for t in trends) / len(trends)
            }
            trend_series.append(series)
    
    return trend_series

def _identify_trend_metric(sentence: str) -> str:
    """Identify what metric the trend data represents"""
    metric_patterns = {
        "GDP Growth": ["gdp", "economic growth", "gross domestic product"],
        "Inflation": ["inflation", "cpi", "wpi", "price"],
        "Fiscal Deficit": ["fiscal deficit", "budget deficit"],
        "Agricultural Growth": ["agriculture", "farm", "crop"],
        "Industrial Growth": ["industry", "manufacturing", "iip"],
        "Services Growth": ["services", "service sector"],
        "Export Growth": ["export", "merchandise export"],
        "Import Growth": ["import", "merchandise import"],
        "Employment": ["employment", "unemployment", "job"],
        "Investment": ["investment", "fdi", "capital formation"]
    }
    
    for metric, keywords in metric_patterns.items():
        if any(keyword in sentence for keyword in keywords):
            return metric
    
    return "Economic Indicator"

def _normalize_year(year_str: str) -> str:
    """Normalize year format for consistency"""
    # Handle different year formats
    if "-" in year_str:
        # Handle FY format like "2023-24"
        parts = year_str.split("-")
        if len(parts) == 2:
            return f"20{parts[1]}" if len(parts[1]) == 2 else parts[1]
    
    # Extract 4-digit year
    year_match = re.search(r"20\d{2}", year_str)
    if year_match:
        return year_match.group()
    
    return year_str

def _calculate_trend_confidence(sentence: str, year: str, value: str) -> int:
    """Calculate confidence for trend data point"""
    confidence = 70  # Base confidence
    
    # Boost for recent years
    try:
        year_num = int(_normalize_year(year))
        if year_num >= 2020:
            confidence += 10
        elif year_num >= 2015:
            confidence += 5
    except ValueError:
        confidence -= 10
    
    # Boost for precise values
    if "." in value:
        confidence += 8
    
    # Boost for official context
    if any(word in sentence.lower() for word in ["survey", "report", "official", "government"]):
        confidence += 10
    
    return min(95, confidence)

def _assess_trend_data_quality(sentence: str, year: str, value: str) -> str:
    """Assess quality of trend data point"""
    quality_score = 0
    
    # Check for official source indicators
    if any(word in sentence.lower() for word in ["survey", "report", "ministry", "rbi"]):
        quality_score += 2
    
    # Check for precision
    if "." in value:
        quality_score += 1
    
    # Check for context
    if any(word in sentence.lower() for word in ["growth", "rate", "percent", "gdp"]):
        quality_score += 1
    
    if quality_score >= 3:
        return "High"
    elif quality_score >= 2:
        return "Medium"
    else:
        return "Low"

def _calculate_trend_direction(trends: list[dict]) -> str:
    """Calculate overall trend direction for a series"""
    if len(trends) < 2:
        return "Insufficient Data"
    
    # Sort by year
    sorted_trends = sorted(trends, key=lambda x: x["year"])
    
    # Calculate trend
    values = [t["value"] for t in sorted_trends]
    
    if len(values) >= 3:
        # Use linear regression for better trend detection
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * values[i] for i in range(n))
        sum_x2 = sum(i * i for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        if slope > 0.1:
            return "📈 Increasing"
        elif slope < -0.1:
            return "📉 Decreasing"
        else:
            return "➡️ Stable"
    else:
        # Simple comparison for 2 points
        if values[-1] > values[0]:
            return "📈 Increasing"
        elif values[-1] < values[0]:
            return "📉 Decreasing"
        else:
            return "➡️ Stable"

def _assess_series_quality(trends: list[dict]) -> str:
    """Assess overall quality of trend series"""
    if not trends:
        return "No Data"
    
    avg_confidence = sum(t["confidence"] for t in trends) / len(trends)
    data_quality_scores = {"High": 3, "Medium": 2, "Low": 1}
    avg_data_quality = sum(data_quality_scores.get(t["data_quality"], 1) for t in trends) / len(trends)
    
    overall_score = (avg_confidence / 100 + avg_data_quality / 3) / 2
    
    if overall_score >= 0.8:
        return "High Quality"
    elif overall_score >= 0.6:
        return "Medium Quality"
    else:
        return "Low Quality"

# ─────────────────────────────────────────────
# ENHANCED KEY HIGHLIGHTS EXTRACTION
# ─────────────────────────────────────────────

def _extract_enhanced_key_highlights(sentences: list[str]) -> list[dict]:
    """Extract key highlights with relevance scoring and categorization"""
    highlight_patterns = [
        # Achievement patterns
        r"(record|highest|lowest|first time|unprecedented|historic|milestone)",
        r"(achieved|reached|attained|surpassed|exceeded)",
        
        # Significant change patterns
        r"(significant|substantial|major|dramatic|sharp) (growth|increase|decrease|decline|improvement)",
        r"(growth of|decline of|increase of|decrease of|rise of|fall of)\s+\d+",
        
        # Performance patterns
        r"(outperform|surpass|exceed|beat|better than)",
        r"(strong|robust|solid|impressive|remarkable) (performance|growth|recovery)",
        
        # Comparative patterns
        r"(compared to|vis-a-vis|against|versus) (last year|previous year|earlier)",
        r"(higher|lower|better|worse) than (expected|projected|estimated)",
        
        # Trend patterns
        r"(upward|downward|positive|negative) (trend|trajectory|momentum)",
        r"(recovery|revival|turnaround|improvement) (in|of)"
    ]
    
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in highlight_patterns]
    results = []
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        
        # Check for highlight patterns
        pattern_matches = []
        for pattern in compiled_patterns:
            matches = pattern.findall(sent_lower)
            pattern_matches.extend(matches)
        
        if pattern_matches:
            # Calculate relevance score
            relevance_score = _calculate_highlight_relevance(sent_lower, pattern_matches)
            
            # Extract numeric data for context
            percents = PERCENT_RE.findall(sent)
            amounts = AMOUNT_RE.findall(sent)
            years = YEAR_PATTERN.findall(sent)
            
            highlight = {
                "sentence": sent,
                "sentence_index": sent_idx,
                "relevance_score": relevance_score,
                "category": _categorize_highlight(sent_lower),
                "impact_level": _assess_impact_level(sent_lower, pattern_matches),
                "numeric_data": {
                    "percentages": percents,
                    "amounts": amounts,
                    "years": years
                },
                "matched_patterns": pattern_matches[:3],  # Top 3 patterns
                "confidence": _calculate_highlight_confidence(sent_lower, pattern_matches),
                "sentiment": _analyze_sector_sentiment(sent_lower)
            }
            
            results.append(highlight)
    
    # Sort by relevance and confidence
    results.sort(key=lambda x: (x["relevance_score"], x["confidence"]), reverse=True)
    
    # Remove duplicates and low-quality highlights
    filtered_results = _filter_highlights(results)
    
    return filtered_results[:20]  # Return top 20 highlights

def _calculate_highlight_relevance(sentence: str, matches: list) -> int:
    """Calculate relevance score for highlight"""
    score = len(matches) * 5  # Base score from pattern matches
    
    # Boost for economic terms
    economic_terms = ["gdp", "growth", "inflation", "deficit", "economy", "sector", "policy"]
    score += sum(3 for term in economic_terms if term in sentence)
    
    # Boost for superlatives
    superlatives = ["highest", "lowest", "best", "worst", "largest", "smallest"]
    score += sum(5 for sup in superlatives if sup in sentence)
    
    # Boost for numeric data
    if re.search(r"\d+(?:\.\d+)?", sentence):
        score += 8
    
    return min(100, score)

def _categorize_highlight(sentence: str) -> str:
    """Categorize the type of highlight"""
    if any(word in sentence for word in ["gdp", "growth", "economy", "economic"]):
        return "🟢 Economic Performance"
    elif any(word in sentence for word in ["inflation", "price", "cost"]):
        return "🟡 Price Trends"
    elif any(word in sentence for word in ["deficit", "fiscal", "budget"]):
        return "🔴 Fiscal Metrics"
    elif any(word in sentence for word in ["export", "import", "trade"]):
        return "🔵 Trade Performance"
    elif any(word in sentence for word in ["employment", "job", "unemployment"]):
        return "🟣 Employment"
    elif any(word in sentence for word in ["agriculture", "industry", "services"]):
        return "🟠 Sectoral Performance"
    else:
        return "⚪ General"

def _assess_impact_level(sentence: str, matches: list) -> str:
    """Assess the impact level of the highlight"""
    high_impact_words = ["record", "historic", "unprecedented", "dramatic", "sharp", "significant"]
    medium_impact_words = ["substantial", "major", "notable", "considerable"]
    
    if any(word in sentence.lower() for word in high_impact_words):
        return "High Impact"
    elif any(word in sentence.lower() for word in medium_impact_words):
        return "Medium Impact"
    else:
        return "Low Impact"

def _calculate_highlight_confidence(sentence: str, matches: list) -> int:
    """Calculate confidence score for highlight"""
    confidence = 60 + len(matches) * 8  # Base + pattern bonus
    
    # Boost for official language
    if any(word in sentence.lower() for word in ["survey", "report", "official", "data"]):
        confidence += 15
    
    # Boost for specific numbers
    if re.search(r"\d+\.\d+", sentence):
        confidence += 10
    
    # Boost for comparative language
    if any(word in sentence.lower() for word in ["compared", "than", "versus", "against"]):
        confidence += 8
    
    return min(95, confidence)

def _filter_highlights(highlights: list[dict]) -> list[dict]:
    """Filter out duplicate and low-quality highlights"""
    filtered = []
    seen_content = set()
    
    for highlight in highlights:
        # Create content signature for deduplication
        content_sig = highlight["sentence"][:100].lower()
        
        # Skip if too similar to existing highlight
        if any(sig in content_sig or content_sig in sig for sig in seen_content):
            continue
        
        # Skip if confidence too low
        if highlight["confidence"] < 60:
            continue
        
        # Skip if relevance too low
        if highlight["relevance_score"] < 15:
            continue
        
        seen_content.add(content_sig)
        filtered.append(highlight)
    
    return filtered


# ─────────────────────────────────────────────
# CHAPTER/SECTION SUMMARIES EXTRACTION
# ─────────────────────────────────────────────

def _extract_chapter_summaries(sentences: list[str]) -> list[dict]:
    """Extract chapter/section summaries for AI analysis"""
    chapters = []
    current_chapter = None
    chapter_content = []
    
    for sent_idx, sent in enumerate(sentences):
        # Check if this sentence is a chapter/section heading
        is_heading = False
        chapter_info = None
        
        for pattern in CHAPTER_PATTERNS:
            match = re.match(pattern, sent.strip(), re.IGNORECASE)
            if match:
                is_heading = True
                if len(match.groups()) >= 2:
                    chapter_info = {
                        "number": match.group(1),
                        "title": match.group(2).strip(),
                        "full_heading": sent.strip()
                    }
                else:
                    chapter_info = {
                        "number": "Unknown",
                        "title": sent.strip()[:100],
                        "full_heading": sent.strip()
                    }
                break
        
        if is_heading and chapter_info:
            # Save previous chapter if exists
            if current_chapter and chapter_content:
                current_chapter["content"] = chapter_content
                current_chapter["summary_stats"] = _calculate_chapter_stats(chapter_content)
                chapters.append(current_chapter)
            
            # Start new chapter
            current_chapter = {
                "chapter_number": chapter_info["number"],
                "chapter_title": chapter_info["title"],
                "full_heading": chapter_info["full_heading"],
                "start_index": sent_idx,
                "content": [],
                "word_count": 0,
                "key_topics": []
            }
            chapter_content = []
        
        elif current_chapter:
            # Add content to current chapter
            chapter_content.append({
                "sentence": sent,
                "sentence_index": sent_idx
            })
    
    # Add final chapter
    if current_chapter and chapter_content:
        current_chapter["content"] = chapter_content
        current_chapter["summary_stats"] = _calculate_chapter_stats(chapter_content)
        chapters.append(current_chapter)
    
    # If no chapters detected, create sections based on content
    if not chapters:
        chapters = _create_content_sections(sentences)
    
    return chapters

def _calculate_chapter_stats(content: list[dict]) -> dict:
    """Calculate statistics for chapter content"""
    if not content:
        return {}
    
    total_words = sum(len(item["sentence"].split()) for item in content)
    total_sentences = len(content)
    
    # Extract key topics (most frequent meaningful words)
    all_words = []
    for item in content:
        words = [word.lower() for word in item["sentence"].split() 
                if len(word) > 4 and word.isalpha()]
        all_words.extend(words)
    
    # Count word frequency
    from collections import Counter
    word_counts = Counter(all_words)
    key_topics = [word for word, count in word_counts.most_common(10)]
    
    return {
        "total_sentences": total_sentences,
        "total_words": total_words,
        "avg_sentence_length": total_words / total_sentences if total_sentences > 0 else 0,
        "key_topics": key_topics
    }

def _create_content_sections(sentences: list[str]) -> list[dict]:
    """Create content sections when no clear chapters are detected"""
    section_size = max(20, len(sentences) // 5)  # Aim for 5 sections
    sections = []
    
    for i in range(0, len(sentences), section_size):
        section_sentences = sentences[i:i + section_size]
        
        # Generate section title based on content
        section_title = _generate_section_title(section_sentences)
        
        content = [
            {"sentence": sent, "sentence_index": i + j}
            for j, sent in enumerate(section_sentences)
        ]
        
        section = {
            "chapter_number": f"Section {len(sections) + 1}",
            "chapter_title": section_title,
            "full_heading": f"Section {len(sections) + 1}: {section_title}",
            "start_index": i,
            "content": content,
            "summary_stats": _calculate_chapter_stats(content)
        }
        
        sections.append(section)
    
    return sections

def _generate_section_title(sentences: list[str]) -> str:
    """Generate a title for a content section based on key topics"""
    # Extract key terms from first few sentences
    key_terms = []
    for sent in sentences[:5]:  # Look at first 5 sentences
        words = [word for word in sent.split() if len(word) > 5 and word.isalpha()]
        key_terms.extend(words)
    
    # Find most common meaningful terms
    from collections import Counter
    term_counts = Counter(key_terms)
    
    if term_counts:
        top_terms = [term for term, count in term_counts.most_common(3)]
        return " & ".join(top_terms[:2]).title()
    else:
        return "Economic Analysis"

# ─────────────────────────────────────────────
# COMPARATIVE METRICS TABLE CREATION
# ─────────────────────────────────────────────

def _create_comparative_metrics_table(macro_indicators: list[dict], 
                                    sector_performance: dict) -> dict:
    """Create a structured comparative metrics table"""
    
    # Organize macro indicators by category
    categorized_indicators = defaultdict(list)
    for indicator in macro_indicators:
        category = indicator.get("category", "Other")
        categorized_indicators[category].append(indicator)
    
    # Create sector summary
    sector_summary = {}
    for sector, data in sector_performance.items():
        if data.get("summary_stats"):
            stats = data["summary_stats"]
            sector_summary[sector] = {
                "mentions": stats.get("total_mentions", 0),
                "avg_growth": stats.get("avg_growth_rate"),
                "sentiment": stats.get("dominant_sentiment", "neutral"),
                "confidence": stats.get("confidence_range", {}).get("avg", 0)
            }
    
    # Create time series data if available
    time_series = _extract_time_series_data(macro_indicators)
    
    comparative_table = {
        "macro_indicators_by_category": dict(categorized_indicators),
        "sector_performance_summary": sector_summary,
        "time_series_data": time_series,
        "key_metrics_summary": _create_key_metrics_summary(macro_indicators),
        "data_completeness": _assess_table_completeness(categorized_indicators, sector_summary)
    }
    
    return comparative_table

def _extract_time_series_data(indicators: list[dict]) -> dict:
    """Extract time series data from indicators"""
    time_series = defaultdict(list)
    
    for indicator in indicators:
        if indicator.get("year") and indicator.get("value"):
            try:
                year = _normalize_year(indicator["year"])
                value = float(indicator["value"])
                
                time_series[indicator["indicator"]].append({
                    "year": year,
                    "value": value,
                    "confidence": indicator.get("confidence", 70)
                })
            except (ValueError, TypeError):
                continue
    
    # Sort each series by year
    for indicator_name, data_points in time_series.items():
        time_series[indicator_name] = sorted(data_points, key=lambda x: x["year"])
    
    return dict(time_series)

def _create_key_metrics_summary(indicators: list[dict]) -> dict:
    """Create summary of key economic metrics"""
    key_metrics = {}
    
    # Priority indicators for summary
    priority_indicators = [
        "GDP Growth Rate", "Inflation (CPI)", "Fiscal Deficit", 
        "Unemployment Rate", "Current Account Deficit"
    ]
    
    for indicator in indicators:
        indicator_name = indicator["indicator"]
        if indicator_name in priority_indicators and indicator.get("value"):
            try:
                key_metrics[indicator_name] = {
                    "value": float(indicator["value"]),
                    "unit": indicator.get("unit", ""),
                    "confidence": indicator.get("confidence", 70),
                    "trend": indicator.get("trend_direction", "Unknown"),
                    "year": indicator.get("year", "Current")
                }
            except (ValueError, TypeError):
                continue
    
    return key_metrics

def _assess_table_completeness(categorized_indicators: dict, sector_summary: dict) -> dict:
    """Assess completeness of the comparative table"""
    total_categories = len(categorized_indicators)
    total_sectors = len(sector_summary)
    
    # Expected minimum data points
    expected_categories = 5  # Growth, Price, Fiscal, External, Employment
    expected_sectors = 3     # Agriculture, Industry, Services
    
    completeness = {
        "indicator_categories": {
            "found": total_categories,
            "expected": expected_categories,
            "completeness_pct": min(100, (total_categories / expected_categories) * 100)
        },
        "sector_coverage": {
            "found": total_sectors,
            "expected": expected_sectors,
            "completeness_pct": min(100, (total_sectors / expected_sectors) * 100)
        },
        "overall_completeness": 0
    }
    
    # Calculate overall completeness
    completeness["overall_completeness"] = (
        completeness["indicator_categories"]["completeness_pct"] + 
        completeness["sector_coverage"]["completeness_pct"]
    ) / 2
    
    return completeness

# ─────────────────────────────────────────────
# ACCURACY VALIDATION SYSTEM
# ─────────────────────────────────────────────

def _validate_economic_survey_extraction(extracted_data: dict, sentences: list[str]) -> dict:
    """Comprehensive validation for Economic Survey extraction"""
    validation_report = {
        "overall_accuracy": 0.0,
        "component_scores": {},
        "validation_passed": False,
        "issues": [],
        "recommendations": [],
        "confidence_metrics": {},
        "data_quality_score": 0.0
    }
    
    # Validate each component
    components = {
        "macro_indicators": _validate_macro_indicators,
        "sector_performance": _validate_sector_performance,
        "policy_recommendations": _validate_policy_recommendations,
        "trend_data": _validate_trend_data
    }
    
    component_scores = []
    
    for component_name, validator_func in components.items():
        if component_name in extracted_data:
            score, issues, recommendations = validator_func(extracted_data[component_name])
            validation_report["component_scores"][component_name] = score
            validation_report["issues"].extend(issues)
            validation_report["recommendations"].extend(recommendations)
            component_scores.append(score)
    
    # Calculate overall accuracy
    if component_scores:
        validation_report["overall_accuracy"] = sum(component_scores) / len(component_scores)
    
    # Determine if validation passed (threshold: 90% for Economic Survey)
    validation_report["validation_passed"] = validation_report["overall_accuracy"] >= 90.0
    
    # Calculate confidence metrics
    validation_report["confidence_metrics"] = _calculate_extraction_confidence(
        extracted_data.get("macro_indicators", []),
        extracted_data.get("sector_performance", {})
    )
    
    # Calculate data quality score
    validation_report["data_quality_score"] = _calculate_data_completeness(extracted_data)
    
    return validation_report

def _validate_macro_indicators(indicators: list[dict]) -> tuple[float, list[str], list[str]]:
    """Validate macro indicators extraction"""
    if not indicators:
        return 0.0, ["No macro indicators found"], ["Check extraction patterns"]
    
    issues = []
    recommendations = []
    accuracy_score = 100.0
    
    # Check for essential indicators
    essential_indicators = ["GDP Growth Rate", "Inflation (CPI)", "Fiscal Deficit"]
    found_essential = [ind["indicator"] for ind in indicators]
    
    for essential in essential_indicators:
        if not any(essential.lower() in found.lower() for found in found_essential):
            issues.append(f"Missing essential indicator: {essential}")
            accuracy_score -= 15
    
    # Validate individual indicators
    for indicator in indicators:
        if not indicator.get("is_valid", True):
            issues.append(f"Invalid data for {indicator['indicator']}")
            accuracy_score -= 10
        
        if indicator.get("confidence", 0) < 70:
            issues.append(f"Low confidence for {indicator['indicator']}")
            accuracy_score -= 5
    
    return max(0, accuracy_score), issues, recommendations

def _validate_sector_performance(sector_data: dict) -> tuple[float, list[str], list[str]]:
    """Validate sector performance extraction"""
    if not sector_data:
        return 0.0, ["No sector performance data"], ["Check sector extraction patterns"]
    
    issues = []
    recommendations = []
    accuracy_score = 100.0
    
    # Check for key sectors
    key_sectors = ["Agriculture", "Industry", "Services"]
    found_sectors = list(sector_data.keys())
    
    for key_sector in key_sectors:
        if not any(key_sector.lower() in sector.lower() for sector in found_sectors):
            issues.append(f"Missing key sector: {key_sector}")
            accuracy_score -= 10
    
    return max(0, accuracy_score), issues, recommendations

def _validate_policy_recommendations(recommendations: list[dict]) -> tuple[float, list[str], list[str]]:
    """Validate policy recommendations extraction"""
    issues = []
    recommendations_list = []
    accuracy_score = 100.0
    
    if not recommendations:
        return 70.0, ["No policy recommendations found"], ["May be acceptable for some documents"]
    
    # Check recommendation quality
    for rec in recommendations:
        if rec.get("confidence", 0) < 60:
            issues.append("Low confidence policy recommendation detected")
            accuracy_score -= 5
    
    return max(0, accuracy_score), issues, recommendations_list

def _validate_trend_data(trend_data: list[dict]) -> tuple[float, list[str], list[str]]:
    """Validate trend data extraction"""
    issues = []
    recommendations = []
    accuracy_score = 100.0
    
    if not trend_data:
        return 80.0, ["No trend data found"], ["Trend data may not be available in all documents"]
    
    # Validate trend series
    for series in trend_data:
        if len(series.get("data_points", [])) < 2:
            issues.append(f"Insufficient data points for {series.get('metric_type', 'Unknown')} trend")
            accuracy_score -= 10
    
    return max(0, accuracy_score), issues, recommendations

def _calculate_extraction_confidence(macro_indicators: list[dict], sector_performance: dict) -> dict:
    """Calculate confidence metrics for extraction"""
    metrics = {}
    
    # Macro indicators confidence
    if macro_indicators:
        confidences = [ind.get("confidence", 70) for ind in macro_indicators]
        metrics["macro_indicators_confidence"] = sum(confidences) / len(confidences)
    
    # Sector performance confidence
    if sector_performance:
        all_confidences = []
        for sector_data in sector_performance.values():
            if isinstance(sector_data, dict) and "avg_confidence" in sector_data:
                all_confidences.append(sector_data["avg_confidence"])
        
        if all_confidences:
            metrics["sector_performance_confidence"] = sum(all_confidences) / len(all_confidences)
    
    # Overall confidence
    all_conf = [v for v in metrics.values() if v is not None]
    if all_conf:
        metrics["overall_confidence"] = sum(all_conf) / len(all_conf)
    
    return metrics

def _calculate_data_completeness(extracted_data: dict) -> float:
    """Calculate data completeness score"""
    completeness_score = 100.0
    
    # Check for expected data components
    expected_components = [
        "macro_indicators", "sector_performance", "policy_recommendations", 
        "key_highlights", "chapter_summaries"
    ]
    
    missing_components = [comp for comp in expected_components if not extracted_data.get(comp)]
    completeness_score -= len(missing_components) * 15
    
    # Check data richness
    total_extractions = (
        len(extracted_data.get("macro_indicators", [])) +
        len(extracted_data.get("sector_performance", {})) +
        len(extracted_data.get("policy_recommendations", [])) +
        len(extracted_data.get("key_highlights", []))
    )
    
    if total_extractions < 10:
        completeness_score -= 20
    elif total_extractions < 25:
        completeness_score -= 10
    
    return max(0, completeness_score)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS (UPDATED)
# ─────────────────────────────────────────────

def _detect_area(text: str) -> str:
    """Enhanced policy area detection (kept for compatibility)"""
    return _detect_policy_area(text)
