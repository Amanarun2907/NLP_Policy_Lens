"""
Branch A – Financial Information Extractor
Extracts: sector allocations, fiscal indicators, capital expenditure,
          budget estimates, economic indicators
"""

import re
from collections import defaultdict
from utils.normalizer import parse_amount

# ─────────────────────────────────────────────
# ENHANCED SECTOR KEYWORD MAP WITH COMPREHENSIVE COVERAGE
# ─────────────────────────────────────────────

SECTOR_KEYWORDS = {
    "Agriculture & Allied":    [
        "agriculture", "farmer", "farming", "crop", "kisan", "agri", "horticulture", 
        "fisheries", "animal husbandry", "dairy", "poultry", "livestock", "irrigation",
        "fertilizer", "seed", "pesticide", "organic farming", "food processing",
        "agricultural credit", "crop insurance", "msp", "minimum support price",
        "pradhan mantri kisan", "pm kisan", "kisan credit card", "agricultural marketing"
    ],
    "Education & Skill Development": [
        "education", "school", "college", "university", "student", "learning", "skill",
        "eklavya", "navodaya", "kendriya vidyalaya", "higher education", "technical education",
        "vocational training", "skill development", "digital literacy", "teacher training",
        "scholarship", "mid day meal", "sarva shiksha abhiyan", "rashtriya madhyamik",
        "iit", "iim", "nit", "research", "innovation", "startup india"
    ],
    "Health & Medical":        [
        "health", "hospital", "medical", "healthcare", "ayushman", "pmjay", "medicine",
        "doctor", "nutrition", "vaccine", "immunization", "maternal health", "child health",
        "mental health", "telemedicine", "medical college", "aiims", "national health mission",
        "health insurance", "medical equipment", "pharmaceutical", "drug", "wellness"
    ],
    "Defence & Security":      [
        "defence", "defense", "military", "army", "navy", "air force", "security", "border",
        "paramilitary", "coast guard", "bsf", "crpf", "cisf", "itbp", "ssb", "nsg",
        "defence procurement", "modernization", "indigenous defence", "make in india defence",
        "border infrastructure", "strategic", "national security", "cyber security"
    ],
    "Infrastructure & Construction": [
        "infrastructure", "road", "highway", "bridge", "construction", "building", "corridor",
        "expressway", "flyover", "metro", "airport", "port", "connectivity", "transport",
        "logistics", "warehousing", "cold storage", "bharatmala", "sagarmala", "dedicated freight corridor",
        "industrial corridor", "smart cities", "urban infrastructure", "rural connectivity"
    ],
    "Railways & Transportation": [
        "railway", "rail", "train", "metro", "station", "track", "vande bharat", "locomotive",
        "coach", "wagon", "signaling", "electrification", "high speed rail", "bullet train",
        "railway safety", "railway modernization", "dedicated freight corridor", "metro rail",
        "monorail", "light rail", "public transport", "mass rapid transit"
    ],
    "Energy & Power":          [
        "energy", "power", "electricity", "solar", "renewable", "wind", "nuclear", "coal",
        "petroleum", "gas", "hydroelectric", "thermal", "grid", "transmission", "distribution",
        "energy efficiency", "clean energy", "green energy", "battery", "electric vehicle",
        "fuel", "lng", "cng", "lpg", "oil", "refinery", "pipeline", "power plant"
    ],
    "Housing & Urban Development": [
        "housing", "house", "home", "shelter", "pmay", "pradhan mantri awas", "affordable housing",
        "slum rehabilitation", "urban development", "city", "smart city", "municipality",
        "amrut", "swachh bharat", "solid waste management", "sewerage", "water supply",
        "urban planning", "real estate", "construction", "building materials"
    ],
    "Rural Development":       [
        "rural", "village", "panchayat", "gram", "mgnrega", "mnrega", "rural employment",
        "rural infrastructure", "rural roads", "pradhan mantri gram sadak yojana", "pmgsy",
        "rural electrification", "rural water supply", "rural sanitation", "rural housing",
        "self help group", "shg", "microfinance", "rural livelihood", "deen dayal"
    ],
    "Digital India & Technology": [
        "digital", "technology", "tech", "internet", "broadband", "startup", "innovation",
        "ai", "artificial intelligence", "machine learning", "blockchain", "iot", "5g",
        "digital india", "e-governance", "digital payment", "fintech", "cybersecurity",
        "data center", "semiconductor", "electronics", "software", "it", "ites", "digitization"
    ],
    "Water Resources & Management": [
        "water", "jal", "irrigation", "dam", "river", "flood", "jal jeevan mission",
        "water supply", "drinking water", "groundwater", "watershed", "river linking",
        "water conservation", "rainwater harvesting", "desalination", "water treatment",
        "sewage treatment", "river cleaning", "namami gange", "cauvery", "narmada"
    ],
    "Finance & Banking":       [
        "bank", "banking", "finance", "credit", "loan", "nbfc", "insurance", "mudra",
        "financial inclusion", "jan dhan", "digital payment", "upi", "fintech", "capital market",
        "stock exchange", "sebi", "rbi", "monetary policy", "fiscal policy", "public sector bank",
        "cooperative bank", "microfinance", "payment bank", "small finance bank"
    ],
    "MSME & Industry":         [
        "msme", "small business", "micro", "medium enterprise", "cottage industry", "handicraft",
        "handloom", "khadi", "manufacturing", "industrial", "factory", "production",
        "make in india", "atmanirbhar", "self reliant", "industrial promotion", "cluster development",
        "technology upgradation", "quality certification", "export promotion"
    ],
    "Social Welfare & Inclusion": [
        "welfare", "women", "child", "elderly", "disabled", "sc", "st", "obc", "tribal",
        "minority", "social justice", "empowerment", "gender", "pension", "scholarship",
        "reservation", "affirmative action", "inclusive development", "social security",
        "anganwadi", "integrated child development", "beti bachao beti padhao"
    ],
    "Environment & Climate":   [
        "environment", "climate", "green", "forest", "pollution", "carbon", "emission",
        "biodiversity", "wildlife", "national park", "afforestation", "reforestation",
        "clean air", "clean water", "waste management", "recycling", "sustainable development",
        "climate change", "global warming", "renewable energy", "electric vehicle", "cng"
    ],
    "Space & Science":         [
        "space", "isro", "science", "research", "innovation", "r&d", "satellite", "mission",
        "chandrayaan", "mangalyaan", "gaganyaan", "pslv", "gslv", "scientific research",
        "technology development", "laboratory", "csir", "drdo", "atomic energy", "nuclear research"
    ],
    "Tourism & Culture":       [
        "tourism", "tourist", "heritage", "culture", "pilgrimage", "archaeological",
        "monument", "museum", "art", "craft", "cultural heritage", "incredible india",
        "spiritual tourism", "eco tourism", "adventure tourism", "medical tourism",
        "film", "entertainment", "media", "broadcasting", "doordarshan"
    ],
    "Trade & Commerce":        [
        "export", "import", "trade", "commerce", "wto", "fta", "foreign trade", "international trade",
        "export promotion", "import substitution", "trade facilitation", "customs", "port",
        "logistics", "warehousing", "e-commerce", "digital commerce", "retail", "wholesale"
    ],
    "Textiles & Apparel":      [
        "textile", "garment", "fabric", "cotton", "handloom", "khadi", "silk", "jute",
        "wool", "synthetic fiber", "apparel", "fashion", "clothing", "yarn", "weaving",
        "spinning", "dyeing", "printing", "textile machinery", "technical textile"
    ],
    "Food & Public Distribution": [
        "food", "pds", "public distribution", "ration", "food security", "food subsidy",
        "buffer stock", "fci", "food corporation", "grain", "wheat", "rice", "sugar",
        "cooking gas", "lpg subsidy", "kerosene", "food processing", "cold chain",
        "storage", "warehousing", "food safety", "nutrition"
    ],
    "Petroleum & Natural Gas": [
        "petroleum", "oil", "gas", "lng", "lpg", "cng", "refinery", "exploration",
        "drilling", "pipeline", "fuel", "petrol", "diesel", "kerosene", "crude oil",
        "natural gas", "shale gas", "biofuel", "ethanol", "biodiesel", "energy security"
    ],
    "Steel & Mining":          [
        "steel", "iron", "mining", "coal", "mineral", "ore", "metal", "aluminum",
        "copper", "zinc", "lead", "gold", "diamond", "limestone", "bauxite",
        "iron ore", "coal mining", "mineral exploration", "geological survey",
        "mining safety", "sustainable mining", "beneficiation"
    ],
    "Chemicals & Fertilizers": [
        "chemical", "fertilizer", "pesticide", "pharmaceutical", "drug", "medicine",
        "petrochemical", "plastic", "polymer", "dye", "paint", "cosmetic",
        "agrochemical", "specialty chemical", "bulk chemical", "fine chemical",
        "chemical safety", "chemical industry", "pharma industry"
    ],
    "Telecommunications":      [
        "telecom", "telecommunication", "mobile", "phone", "internet", "broadband",
        "fiber optic", "tower", "spectrum", "5g", "4g", "satellite communication",
        "digital communication", "bsnl", "mtnl", "trai", "dot", "universal service obligation"
    ]
}

# ─────────────────────────────────────────────
# ENHANCED FISCAL INDICATOR PATTERNS WITH COMPREHENSIVE COVERAGE
# ─────────────────────────────────────────────

FISCAL_PATTERNS = {
    "Fiscal Deficit":      [
        r"fiscal deficit", r"fiscal gap", r"budget deficit", r"government deficit",
        r"deficit.*gdp", r"deficit.*percent", r"deficit.*%"
    ],
    "Revenue Deficit":     [
        r"revenue deficit", r"revenue gap", r"current account deficit"
    ],
    "Primary Deficit":     [
        r"primary deficit", r"primary balance", r"primary surplus"
    ],
    "Capital Expenditure": [
        r"capital expenditure", r"capex", r"capital outlay", r"capital spending",
        r"infrastructure spending", r"investment expenditure", r"development expenditure"
    ],
    "Revenue Expenditure": [
        r"revenue expenditure", r"current expenditure", r"non-plan expenditure",
        r"establishment expenditure", r"administrative expenditure"
    ],
    "Total Expenditure":   [
        r"total expenditure", r"aggregate expenditure", r"government expenditure",
        r"public expenditure", r"budget expenditure", r"total spending"
    ],
    "Tax Revenue":         [
        r"tax revenue", r"gross tax", r"net tax", r"direct tax", r"indirect tax",
        r"income tax", r"corporate tax", r"gst", r"customs duty", r"excise duty"
    ],
    "Non-Tax Revenue":     [
        r"non.tax revenue", r"non tax revenue", r"other receipts", r"miscellaneous receipts",
        r"dividend", r"interest receipts", r"fees", r"penalties"
    ],
    "GDP Growth":          [
        r"gdp growth", r"economic growth", r"growth rate", r"real gdp",
        r"nominal gdp", r"gdp.*percent", r"gdp.*%"
    ],
    "GDP":                 [
        r"\bgdp\b", r"gross domestic product", r"national income", r"economic output"
    ],
    "Inflation":           [
        r"inflation", r"cpi", r"wpi", r"price rise", r"consumer price index",
        r"wholesale price index", r"retail inflation", r"core inflation"
    ],
    "Borrowing":           [
        r"borrowing", r"market borrowing", r"net borrowing", r"government borrowing",
        r"public debt", r"fiscal borrowing", r"debt.*gdp"
    ],
    "Disinvestment":       [
        r"disinvestment", r"privatisation", r"privatization", r"strategic sale",
        r"stake sale", r"equity sale", r"psu disinvestment"
    ],
    "Budget Estimate":     [
        r"budget estimate", r"\bbe\b", r"budgeted", r"estimated expenditure",
        r"budget provision", r"budget allocation"
    ],
    "Revised Estimate":    [
        r"revised estimate", r"\bre\b", r"revised expenditure", r"revised allocation"
    ],
    "Foreign Exchange":    [
        r"foreign exchange", r"forex", r"foreign reserve", r"external reserves",
        r"foreign currency", r"dollar reserves", r"forex reserves"
    ],
    "Current Account":     [
        r"current account deficit", r"current account surplus", r"trade deficit",
        r"trade surplus", r"balance of payments", r"external sector"
    ],
    "Debt to GDP":         [
        r"debt.*gdp", r"debt gdp ratio", r"public debt.*gdp", r"government debt.*gdp"
    ],
    "Interest Payments":   [
        r"interest payment", r"debt service", r"interest burden", r"interest expenditure"
    ],
    "Subsidy":            [
        r"subsidy", r"subsidies", r"food subsidy", r"fertilizer subsidy",
        r"fuel subsidy", r"petroleum subsidy", r"lpg subsidy"
    ],
    "Pension":            [
        r"pension", r"pension expenditure", r"pension liability", r"retirement benefits"
    ]
}

# ─────────────────────────────────────────────
# ENHANCED AMOUNT AND PERCENTAGE PATTERNS
# ─────────────────────────────────────────────

AMOUNT_RE = re.compile(
    r"(?:₹|Rs\.?|INR|USD|\$)\s*[\d,]+(?:\.\d+)?"
    r"(?:\s*(?:lakh|lac|crore|million|billion|thousand|hundred|trillion))*"
    r"|\d+(?:\.\d+)?\s*(?:lakh|lac|crore|million|billion|thousand|trillion)\s*(?:crore|lakh|rupees?)?",
    re.IGNORECASE,
)

PERCENT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:percent|per cent|%|percentage)\s*(?:of\s+gdp|of\s+the\s+gdp|to\s+gdp)?", 
    re.IGNORECASE
)

# Enhanced patterns for better number extraction
CURRENCY_SYMBOLS = [r"₹", r"Rs\.?", r"INR", r"USD", r"\$"]
MULTIPLIERS = {
    "hundred": 0.000001,    # in crore
    "thousand": 0.0001,     # in crore  
    "lakh": 0.01,          # 1 lakh = 0.01 crore
    "lac": 0.01,           # alternate spelling
    "crore": 1.0,          # base unit
    "million": 0.1,        # 1 million ≈ 0.1 crore
    "billion": 100.0,      # 1 billion = 100 crore
    "trillion": 100000.0,  # 1 trillion = 1 lakh crore
}


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def extract_financial_data(sentences: list[str]) -> dict:
    """
    Main extraction function.
    Returns:
        sector_allocations : list of {sector, amount_text, amount_value, sentence}
        fiscal_indicators  : list of {indicator, amount_text, percent, sentence}
        economic_indicators: list of {indicator, value, unit, sentence}
        top_sectors        : sorted sector allocation summary
    """
    sector_allocations  = _extract_sector_allocations(sentences)
    fiscal_indicators   = _extract_fiscal_indicators(sentences)
    economic_indicators = _extract_economic_indicators(sentences)

    # Build top sectors summary
    sector_summary = defaultdict(float)
    for item in sector_allocations:
        if item["amount_crore"] > 0:
            sector_summary[item["sector"]] += item["amount_crore"]

    top_sectors = sorted(
        [{"sector": k, "total_crore": round(v, 2)} for k, v in sector_summary.items()],
        key=lambda x: x["total_crore"], reverse=True
    )

    return {
        "sector_allocations":  sector_allocations,
        "fiscal_indicators":   fiscal_indicators,
        "economic_indicators": economic_indicators,
        "top_sectors":         top_sectors,
    }


# ─────────────────────────────────────────────
# BRANCH A1 – SECTOR ALLOCATIONS
# ─────────────────────────────────────────────

def _extract_sector_allocations(sentences: list[str]) -> list[dict]:
    """
    Enhanced sector allocation extraction with improved accuracy and deduplication.
    """
    results = []
    processed_combinations = set()  # To avoid duplicates
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        amounts = AMOUNT_RE.findall(sent)
        
        if not amounts:
            continue
            
        # Score sentence relevance for budget allocation context
        allocation_score = 0
        allocation_keywords = [
            "allocation", "budget", "provision", "outlay", "expenditure", 
            "spending", "fund", "crore", "lakh", "billion", "allocated",
            "earmarked", "set aside", "provided", "sanctioned"
        ]
        
        for keyword in allocation_keywords:
            if keyword in sent_lower:
                allocation_score += 1
        
        # Skip sentences that don't seem to be about budget allocations
        if allocation_score == 0 and not any(word in sent_lower for word in ["crore", "lakh", "billion", "₹", "rs"]):
            continue
            
        for sector, keywords in SECTOR_KEYWORDS.items():
            # Calculate sector relevance score
            sector_score = 0
            matched_keywords = []
            
            for kw in keywords:
                if kw in sent_lower:
                    sector_score += 1
                    matched_keywords.append(kw)
            
            # Require minimum relevance for sector matching
            if sector_score == 0:
                continue
                
            # Boost score for exact sector name matches
            if sector.lower().replace(" & ", " ").replace(" and ", " ") in sent_lower:
                sector_score += 3
                
            for amt_text in amounts:
                amt_val = _parse_to_raw(amt_text)
                
                # Filter out unreasonably small or large amounts
                if amt_val < 0.01 or amt_val > 5000000:  # Less than 1 lakh or more than 50 lakh crore
                    continue
                
                # Create unique key for deduplication
                unique_key = (sector, round(amt_val, 2), sent[:100])
                
                if unique_key not in processed_combinations:
                    processed_combinations.add(unique_key)
                    
                    results.append({
                        "sector": sector,
                        "amount_text": amt_text.strip(),
                        "amount_value": amt_val,
                        "amount_crore": round(amt_val, 2),
                        "sentence": sent,
                        "sentence_index": sent_idx,
                        "sector_score": sector_score,
                        "allocation_score": allocation_score,
                        "matched_keywords": matched_keywords[:3],  # Top 3 matched keywords
                        "confidence": min(95, 70 + sector_score * 5 + allocation_score * 3)
                    })
    
    # Sort by confidence and amount for better quality results
    results.sort(key=lambda x: (x["confidence"], x["amount_crore"]), reverse=True)
    
    # Advanced deduplication: merge similar entries for same sector
    final_results = []
    sector_totals = {}
    
    for result in results:
        sector = result["sector"]
        amount = result["amount_crore"]
        
        # Check if this is likely a duplicate or sub-component
        is_duplicate = False
        for existing in final_results:
            if (existing["sector"] == sector and 
                abs(existing["amount_crore"] - amount) / max(existing["amount_crore"], amount) < 0.1):
                # Very similar amounts for same sector - likely duplicate
                is_duplicate = True
                # Keep the one with higher confidence
                if result["confidence"] > existing["confidence"]:
                    final_results.remove(existing)
                    final_results.append(result)
                break
        
        if not is_duplicate:
            final_results.append(result)
            
    return final_results


# ─────────────────────────────────────────────
# BRANCH A2 – FISCAL INDICATORS
# ─────────────────────────────────────────────

def _extract_fiscal_indicators(sentences: list[str]) -> list[dict]:
    """
    Enhanced fiscal indicators extraction with better accuracy and context awareness.
    Uses the new enhanced extraction method for improved results.
    """
    # Use the enhanced extraction method
    enhanced_results = _enhance_fiscal_indicator_extraction(sentences)
    
    # If enhanced method returns good results, use them
    if enhanced_results and len(enhanced_results) >= 3:
        return enhanced_results
    
    # Otherwise, fall back to original method with enhancements
    results = []
    processed_indicators = set()
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        
        for indicator, patterns in FISCAL_PATTERNS.items():
            # Check if any pattern matches
            pattern_matches = []
            for pattern in patterns:
                matches = list(re.finditer(pattern, sent_lower))
                pattern_matches.extend(matches)
            
            if not pattern_matches:
                continue
                
            # Extract amounts and percentages from the sentence
            amounts = AMOUNT_RE.findall(sent)
            percents = PERCENT_RE.findall(sent)
            
            # Calculate context relevance score
            context_score = _calculate_fiscal_context_score(sent_lower, indicator)
            
            # Process amounts
            processed_amounts = []
            for amt_text in amounts:
                amt_val = _parse_to_raw(amt_text)
                if amt_val > 0 and _is_reasonable_fiscal_amount(amt_val, indicator):
                    processed_amounts.append({
                        "text": amt_text.strip(),
                        "value_crore": round(amt_val, 2)
                    })
            
            # Process percentages
            processed_percents = []
            for pct in percents:
                try:
                    pct_val = float(pct)
                    if _is_reasonable_fiscal_percentage(pct_val, indicator):
                        processed_percents.append(pct_val)
                except ValueError:
                    continue
            
            # Create result entry
            amount_info = processed_amounts[0] if processed_amounts else None
            percent_info = processed_percents[0] if processed_percents else None
            
            # Create unique identifier for deduplication
            unique_id = (indicator, 
                        amount_info["text"] if amount_info else "", 
                        percent_info if percent_info else "",
                        sent[:80])
            
            if unique_id not in processed_indicators:
                processed_indicators.add(unique_id)
                
                # Calculate confidence score
                confidence = _calculate_fiscal_confidence(
                    context_score, amount_info, percent_info, indicator, sent_lower
                )
                
                result = {
                    "indicator": indicator,
                    "sentence": sent,
                    "sentence_index": sent_idx,
                    "context_score": context_score,
                    "confidence": min(confidence, 95)
                }
                
                # Add amount information
                if amount_info:
                    result["amount_text"] = amount_info["text"]
                    result["amount_crore"] = amount_info["value_crore"]
                else:
                    result["amount_text"] = None
                    result["amount_crore"] = None
                
                # Add percentage information
                if percent_info:
                    result["percent"] = percent_info
                else:
                    result["percent"] = None
                
                # Add category for better organization
                result["category"] = _categorize_fiscal_indicator(indicator)
                
                results.append(result)
    
    # Sort by confidence and relevance
    results.sort(key=lambda x: (x["confidence"], x["context_score"]), reverse=True)
    
    # Advanced deduplication
    final_results = _deduplicate_fiscal_indicators(results)
    
    return final_results


# ─────────────────────────────────────────────
# BRANCH A3 – ECONOMIC INDICATORS
# ─────────────────────────────────────────────

def _extract_economic_indicators(sentences: list[str]) -> list[dict]:
    results = []
    econ_patterns = [
        (r"gdp.*?(\d+(?:\.\d+)?)\s*(?:percent|%|lakh crore|crore)", "GDP"),
        (r"inflation.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",            "Inflation"),
        (r"growth.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",               "Growth Rate"),
        (r"unemployment.*?(\d+(?:\.\d+)?)\s*(?:percent|%)",         "Unemployment"),
        (r"export.*?(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)",              "Exports"),
        (r"import.*?(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)",              "Imports"),
        (r"foreign.*?reserve.*?(?:\$|USD)\s*([\d,]+(?:\.\d+)?)",    "Forex Reserves"),
    ]
    for sent in sentences:
        sent_lower = sent.lower()
        for pattern, indicator in econ_patterns:
            match = re.search(pattern, sent_lower)
            if match:
                results.append({
                    "indicator": indicator,
                    "value":     match.group(1),
                    "sentence":  sent,
                })
    return results


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _parse_to_raw(amount_text: str) -> float:
    """
    Enhanced amount parser with better accuracy and error handling.
    Convert amount text to value in crore with improved precision.
    
    Examples:
        'Rs. 1,50,000 crore' → 150000.0 crore
        'Rs. 10 lakh crore'  → 1000000.0 crore (10 lakh crore)
        '₹5.5 trillion'      → 550000.0 crore
        '$100 billion'       → 8500.0 crore (approx, assuming 1 USD = 85 INR)
    """
    try:
        text = amount_text.lower().strip()
        original_text = text
        
        # Handle currency conversion (basic USD to INR)
        usd_to_inr_rate = 83.0  # Approximate rate
        is_usd = bool(re.search(r'usd|\$', text))
        
        # Remove currency symbols
        text = re.sub(r"[₹$]|rs\.?|inr|usd", "", text).strip()
        
        # Remove commas and extra spaces
        text = re.sub(r"[,\s]+", " ", text).strip()

        # Enhanced pattern matching for number + unit combinations
        # Pattern: number + optional unit1 + optional unit2
        pattern = r"([\d.]+)(?:\s+(hundred|thousand|lakh|lac|crore|million|billion|trillion))?(?:\s+(hundred|thousand|lakh|lac|crore|million|billion|trillion|rupees?))?.*"
        match = re.match(pattern, text, re.IGNORECASE)
        
        if not match:
            # Fallback: try to extract just the number
            numbers = re.findall(r'[\d.]+', text)
            if numbers:
                return float(numbers[0]) * (1/usd_to_inr_rate if is_usd else 1)
            return 0.0

        value = float(match.group(1))
        unit1 = (match.group(2) or "").lower()
        unit2 = (match.group(3) or "").lower()

        # Apply multipliers
        if unit1 in MULTIPLIERS:
            value *= MULTIPLIERS[unit1]
        if unit2 in MULTIPLIERS and unit2 != "rupees":
            value *= MULTIPLIERS[unit2]
        
        # Handle special cases like "lakh crore"
        if unit1 == "lakh" and unit2 == "crore":
            value = float(match.group(1)) * 100000  # 1 lakh crore = 100000 crore
        elif unit1 == "thousand" and unit2 == "crore":
            value = float(match.group(1)) * 1000    # 1 thousand crore = 1000 crore

        # Convert USD to INR if needed
        if is_usd:
            value = value / usd_to_inr_rate

        # Ensure reasonable bounds (budget figures shouldn't be negative or extremely large)
        if value < 0:
            value = 0
        elif value > 10000000:  # 1 crore crore seems unreasonable
            # Might be a parsing error, try simpler approach
            numbers = re.findall(r'[\d.]+', original_text)
            if numbers:
                value = float(numbers[0])
                if "lakh" in original_text:
                    value *= 0.01
                elif "thousand" in original_text:
                    value *= 0.0001

        return round(value, 2)
        
    except Exception as e:
        # Enhanced error logging for debugging
        import logging
        logging.warning(f"Amount parsing failed for '{amount_text}': {str(e)}")
        return 0.0


# ─────────────────────────────────────────────
# ENHANCED ACCURACY FUNCTIONS
# ─────────────────────────────────────────────

def _validate_sector_allocation(sector: str, amount: float, sentence: str) -> dict:
    """
    Validate and score sector allocation extraction for accuracy.
    Returns validation metrics and confidence score.
    """
    validation = {
        "is_valid": True,
        "confidence": 70,  # Base confidence
        "issues": [],
        "enhancements": []
    }
    
    # Check amount reasonableness
    if amount <= 0:
        validation["is_valid"] = False
        validation["issues"].append("Invalid amount (zero or negative)")
        return validation
    
    if amount < 0.01:  # Less than 1 lakh
        validation["confidence"] -= 20
        validation["issues"].append("Very small amount (< 1 lakh)")
    elif amount > 1000000:  # More than 10 lakh crore
        validation["confidence"] -= 30
        validation["issues"].append("Extremely large amount (> 10 lakh crore)")
    
    # Check sentence context
    sentence_lower = sentence.lower()
    
    # Positive indicators
    budget_keywords = ["allocation", "budget", "provision", "outlay", "expenditure", "allocated", "earmarked"]
    for keyword in budget_keywords:
        if keyword in sentence_lower:
            validation["confidence"] += 5
            validation["enhancements"].append(f"Contains budget keyword: {keyword}")
    
    # Negative indicators
    negative_keywords = ["previous", "last year", "compared to", "reduction", "cut"]
    for keyword in negative_keywords:
        if keyword in sentence_lower:
            validation["confidence"] -= 10
            validation["issues"].append(f"Contains potentially confusing keyword: {keyword}")
    
    # Check for fiscal year mentions
    if re.search(r'\d{4}-\d{2,4}', sentence):
        validation["confidence"] += 10
        validation["enhancements"].append("Contains fiscal year reference")
    
    # Check for percentage mentions (might be growth, not allocation)
    if "%" in sentence and "growth" in sentence_lower:
        validation["confidence"] -= 15
        validation["issues"].append("Might be growth percentage, not allocation")
    
    # Sector name validation
    sector_words = sector.lower().split()
    sector_mentions = sum(1 for word in sector_words if word in sentence_lower)
    if sector_mentions == 0:
        validation["confidence"] -= 25
        validation["issues"].append("Sector name not clearly mentioned in sentence")
    elif sector_mentions >= len(sector_words) * 0.7:
        validation["confidence"] += 15
        validation["enhancements"].append("Strong sector name match")
    
    # Final confidence bounds
    validation["confidence"] = max(10, min(95, validation["confidence"]))
    
    return validation

def _enhance_fiscal_indicator_extraction(sentences: list[str]) -> list[dict]:
    """
    Enhanced fiscal indicator extraction with cross-validation and accuracy improvements.
    """
    results = []
    processed_indicators = set()
    
    # Enhanced patterns with context awareness
    enhanced_patterns = {
        **FISCAL_PATTERNS,
        "Budget Size": [
            r"budget.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)",
            r"total.*?budget.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)",
            r"expenditure.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)"
        ],
        "Tax Collection": [
            r"tax.*?collection.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)",
            r"revenue.*?collection.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)"
        ],
        "Subsidy Expenditure": [
            r"subsidy.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)",
            r"subsidies.*?(?:₹|rs\.?)\s*[\d,]+(?:\.\d+)?\s*(?:lakh|crore|billion|trillion)"
        ]
    }
    
    for sent_idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        
        # Skip sentences that are clearly not about fiscal indicators
        if not any(word in sent_lower for word in ["fiscal", "budget", "deficit", "gdp", "revenue", "expenditure", "growth", "inflation"]):
            continue
        
        for indicator, patterns in enhanced_patterns.items():
            # Check if any pattern matches
            pattern_matches = []
            for pattern in patterns:
                matches = list(re.finditer(pattern, sent_lower))
                pattern_matches.extend(matches)
            
            if not pattern_matches:
                continue
            
            # Extract amounts and percentages with enhanced validation
            amounts = AMOUNT_RE.findall(sent)
            percents = PERCENT_RE.findall(sent)
            
            # Enhanced context scoring
            context_score = _calculate_fiscal_context_score(sent_lower, indicator)
            
            # Process amounts with validation
            processed_amounts = []
            for amt_text in amounts:
                amt_val = _parse_to_raw(amt_text)
                if amt_val > 0:
                    # Validate amount reasonableness for fiscal indicators
                    if _is_reasonable_fiscal_amount(amt_val, indicator):
                        processed_amounts.append({
                            "text": amt_text.strip(),
                            "value_crore": round(amt_val, 2)
                        })
            
            # Process percentages with validation
            processed_percents = []
            for pct in percents:
                try:
                    pct_val = float(pct)
                    if _is_reasonable_fiscal_percentage(pct_val, indicator):
                        processed_percents.append(pct_val)
                except ValueError:
                    continue
            
            # Create result entry with enhanced validation
            amount_info = processed_amounts[0] if processed_amounts else None
            percent_info = processed_percents[0] if processed_percents else None
            
            # Skip if no valid data found
            if not amount_info and not percent_info:
                continue
            
            # Create unique identifier for deduplication
            unique_id = (indicator, 
                        amount_info["text"] if amount_info else "", 
                        percent_info if percent_info else "",
                        sent[:80])
            
            if unique_id not in processed_indicators:
                processed_indicators.add(unique_id)
                
                # Calculate enhanced confidence score
                confidence = _calculate_fiscal_confidence(
                    context_score, amount_info, percent_info, indicator, sent_lower
                )
                
                result = {
                    "indicator": indicator,
                    "sentence": sent,
                    "sentence_index": sent_idx,
                    "context_score": context_score,
                    "confidence": confidence,
                    "extraction_method": "enhanced_nlp"
                }
                
                # Add amount information
                if amount_info:
                    result["amount_text"] = amount_info["text"]
                    result["amount_crore"] = amount_info["value_crore"]
                else:
                    result["amount_text"] = None
                    result["amount_crore"] = None
                
                # Add percentage information
                if percent_info:
                    result["percent"] = percent_info
                else:
                    result["percent"] = None
                
                # Add category for better organization
                result["category"] = _categorize_fiscal_indicator(indicator)
                
                # Add validation metadata
                result["validation"] = _validate_fiscal_extraction(result)
                
                results.append(result)
    
    # Sort by confidence and relevance
    results.sort(key=lambda x: (x["confidence"], x["context_score"]), reverse=True)
    
    # Advanced deduplication with cross-validation
    final_results = _deduplicate_fiscal_indicators(results)
    
    return final_results

def _calculate_fiscal_context_score(sentence: str, indicator: str) -> int:
    """Calculate context relevance score for fiscal indicators"""
    score = 0
    
    # Base fiscal context words
    fiscal_context_words = {
        "budget": 3, "fiscal": 3, "government": 2, "expenditure": 3, 
        "revenue": 3, "deficit": 4, "surplus": 3, "gdp": 4, 
        "economic": 2, "financial": 2, "policy": 2, "allocation": 3,
        "spending": 3, "investment": 2, "borrowing": 3, "debt": 3
    }
    
    for word, weight in fiscal_context_words.items():
        if word in sentence:
            score += weight
    
    # Indicator-specific bonuses
    indicator_lower = indicator.lower()
    if "deficit" in indicator_lower and "deficit" in sentence:
        score += 5
    if "growth" in indicator_lower and ("growth" in sentence or "gdp" in sentence):
        score += 5
    if "revenue" in indicator_lower and "revenue" in sentence:
        score += 5
    
    return score

def _is_reasonable_fiscal_amount(amount: float, indicator: str) -> bool:
    """Check if fiscal amount is reasonable for the indicator type"""
    indicator_lower = indicator.lower()
    
    # Different indicators have different reasonable ranges
    if "deficit" in indicator_lower:
        return 1000 <= amount <= 2000000  # 1000 crore to 20 lakh crore
    elif "gdp" in indicator_lower:
        return 10000 <= amount <= 50000000  # 1 lakh crore to 50 crore crore
    elif "expenditure" in indicator_lower:
        return 1000 <= amount <= 10000000  # 1000 crore to 1 crore crore
    elif "revenue" in indicator_lower:
        return 1000 <= amount <= 5000000   # 1000 crore to 50 lakh crore
    else:
        return 100 <= amount <= 10000000   # General range
    
def _is_reasonable_fiscal_percentage(percentage: float, indicator: str) -> bool:
    """Check if fiscal percentage is reasonable for the indicator type"""
    indicator_lower = indicator.lower()
    
    if "deficit" in indicator_lower:
        return 0.1 <= percentage <= 15.0  # Deficit as % of GDP
    elif "growth" in indicator_lower:
        return -5.0 <= percentage <= 20.0  # Growth rates
    elif "inflation" in indicator_lower:
        return -2.0 <= percentage <= 25.0  # Inflation rates
    else:
        return 0.0 <= percentage <= 100.0  # General percentage range

def _calculate_fiscal_confidence(context_score: int, amount_info: dict, 
                               percent_info: float, indicator: str, sentence: str) -> int:
    """Calculate comprehensive confidence score for fiscal indicators"""
    confidence = 60  # Base confidence
    
    # Context bonus
    confidence += min(25, context_score * 2)
    
    # Data availability bonus
    if amount_info:
        confidence += 10
    if percent_info:
        confidence += 10
    
    # Indicator-specific adjustments
    indicator_lower = indicator.lower()
    if indicator_lower in ["fiscal deficit", "revenue deficit", "gdp growth"]:
        confidence += 5  # High-priority indicators
    
    # Sentence quality checks
    if len(sentence.split()) >= 10:  # Substantial sentence
        confidence += 5
    if any(year in sentence for year in ["2023", "2024", "2025"]):  # Recent year
        confidence += 5
    
    # Penalty for ambiguous sentences
    if "estimate" in sentence or "projected" in sentence:
        confidence -= 5
    if "previous" in sentence or "last year" in sentence:
        confidence -= 10
    
    return max(10, min(95, confidence))

def _validate_fiscal_extraction(result: dict) -> dict:
    """Validate fiscal indicator extraction"""
    validation = {
        "is_valid": True,
        "quality_score": result["confidence"],
        "issues": [],
        "recommendations": []
    }
    
    # Check for data consistency
    if result.get("amount_crore") and result.get("percent"):
        # Both amount and percentage present - check for consistency if possible
        validation["recommendations"].append("Cross-validate amount and percentage")
    
    # Check sentence quality
    sentence = result["sentence"]
    if len(sentence.split()) < 8:
        validation["issues"].append("Short sentence - may lack context")
        validation["quality_score"] -= 10
    
    # Check for fiscal year context
    if not re.search(r'\d{4}', sentence):
        validation["issues"].append("No year mentioned - temporal context unclear")
        validation["quality_score"] -= 5
    
    return validation

def _deduplicate_fiscal_indicators(results: list[dict]) -> list[dict]:
    """Advanced deduplication for fiscal indicators"""
    final_results = []
    seen_combinations = {}
    
    for result in results:
        indicator = result["indicator"]
        amount = result.get("amount_crore")
        percent = result.get("percent")
        
        # Create deduplication key
        key = (indicator, 
               round(amount, -2) if amount else None,  # Round to nearest 100 crore
               round(percent, 1) if percent else None)  # Round to 1 decimal
        
        if key not in seen_combinations:
            seen_combinations[key] = result
            final_results.append(result)
        else:
            # Keep the one with higher confidence
            existing = seen_combinations[key]
            if result["confidence"] > existing["confidence"]:
                final_results.remove(existing)
                final_results.append(result)
                seen_combinations[key] = result
    
    return final_results


# ─────────────────────────────────────────────
# HELPER: CATEGORIZE FISCAL INDICATOR
# ─────────────────────────────────────────────

def _categorize_fiscal_indicator(indicator: str) -> str:
    """Categorize fiscal indicators for better organization and display"""
    indicator_lower = indicator.lower()

    if any(word in indicator_lower for word in ["deficit", "gap", "shortfall"]):
        return "🔴 Deficit Metrics"
    elif any(word in indicator_lower for word in ["growth", "gdp", "expansion"]):
        return "🟢 Growth Metrics"
    elif any(word in indicator_lower for word in ["revenue", "tax", "income"]):
        return "🟡 Revenue Metrics"
    elif any(word in indicator_lower for word in ["expenditure", "spending", "outlay", "capex", "capital"]):
        return "🟠 Expenditure Metrics"
    elif any(word in indicator_lower for word in ["borrowing", "debt", "loan", "liability"]):
        return "🟣 Debt Metrics"
    elif any(word in indicator_lower for word in ["subsidy", "transfer", "grant"]):
        return "🔵 Transfer Metrics"
    else:
        return "⚪ Other Metrics"
