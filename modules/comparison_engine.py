"""
Enhanced Comparison Engine for Year-on-Year Budget Analysis
Provides comprehensive comparison capabilities with detailed insights
"""

import pandas as pd
from collections import defaultdict
from typing import Dict, List, Any
import re

def compare_documents(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """
    Comprehensive comparison of two budget documents with enhanced analytics.
    
    Returns detailed comparison across all dimensions:
    - Sector allocations with change analysis
    - Fiscal indicators comparison
    - Policy schemes comparison
    - Tax changes comparison
    - Keyword shift analysis
    - Sentiment comparison
    - Summary statistics
    """
    
    comparison_result = {
        "summary_stats": _compare_summary_stats(data1, data2, year1, year2),
        "sector_comparison": _compare_sectors(data1, data2, year1, year2),
        "fiscal_comparison": _compare_fiscal_indicators(data1, data2, year1, year2),
        "policy_comparison": _compare_policies(data1, data2, year1, year2),
        "tax_comparison": _compare_tax_changes(data1, data2, year1, year2),
        "keyword_comparison": _compare_keywords(data1, data2, year1, year2),
        "sentiment_comparison": _compare_sentiment(data1, data2, year1, year2),
        "innovation_comparison": _compare_innovation_metrics(data1, data2, year1, year2),
        "metadata": {
            "year1": year1,
            "year2": year2,
            "comparison_timestamp": pd.Timestamp.now().isoformat(),
            "analysis_version": "2.0"
        }
    }
    
    return comparison_result

def _compare_summary_stats(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Generate high-level summary statistics comparison."""
    
    # Extract key metrics
    fin1 = data1.get("financial", {})
    fin2 = data2.get("financial", {})
    pol1 = data1.get("policy", {})
    pol2 = data2.get("policy", {})
    
    # Calculate total allocations
    total1 = sum(s["total_crore"] for s in fin1.get("top_sectors", []))
    total2 = sum(s["total_crore"] for s in fin2.get("top_sectors", []))
    
    # Calculate changes
    allocation_change = total2 - total1
    allocation_change_pct = (allocation_change / total1 * 100) if total1 > 0 else 0
    
    # Scheme counts
    scheme_count1 = pol1.get("total_count", 0)
    scheme_count2 = pol2.get("total_count", 0)
    scheme_change = scheme_count2 - scheme_count1
    
    # Sector counts
    sector_count1 = len(fin1.get("top_sectors", []))
    sector_count2 = len(fin2.get("top_sectors", []))
    
    return {
        "total_allocation": {
            year1: round(total1, 2),
            year2: round(total2, 2),
            "change_crore": round(allocation_change, 2),
            "change_pct": round(allocation_change_pct, 2),
            "direction": "increase" if allocation_change > 0 else "decrease" if allocation_change < 0 else "stable"
        },
        "scheme_count": {
            year1: scheme_count1,
            year2: scheme_count2,
            "change": scheme_change,
            "change_pct": round((scheme_change / scheme_count1 * 100) if scheme_count1 > 0 else 0, 1)
        },
        "sector_count": {
            year1: sector_count1,
            year2: sector_count2,
            "change": sector_count2 - sector_count1
        },
        "document_size": {
            year1: len(data1.get("sentences", [])),
            year2: len(data2.get("sentences", [])),
            "change": len(data2.get("sentences", [])) - len(data1.get("sentences", []))
        }
    }

def _compare_sectors(data1: dict, data2: dict, year1: str, year2: str) -> List[dict]:
    """Compare sector allocations with detailed change analysis."""
    
    fin1 = data1.get("financial", {})
    fin2 = data2.get("financial", {})
    
    sectors1 = {s["sector"]: s["total_crore"] for s in fin1.get("top_sectors", [])}
    sectors2 = {s["sector"]: s["total_crore"] for s in fin2.get("top_sectors", [])}
    
    # Get all unique sectors
    all_sectors = set(sectors1.keys()) | set(sectors2.keys())
    
    comparison = []
    for sector in all_sectors:
        val1 = sectors1.get(sector, 0)
        val2 = sectors2.get(sector, 0)
        
        change_crore = val2 - val1
        change_pct = (change_crore / val1 * 100) if val1 > 0 else (100 if val2 > 0 else 0)
        
        # Determine direction and significance
        if abs(change_pct) < 5:
            direction = "stable"
            significance = "minor"
        elif change_pct > 0:
            direction = "increase"
            significance = "major" if change_pct > 25 else "moderate"
        else:
            direction = "decrease"
            significance = "major" if change_pct < -25 else "moderate"
        
        comparison.append({
            "sector": sector,
            f"{year1}_crore": round(val1, 2),
            f"{year2}_crore": round(val2, 2),
            "change_crore": round(change_crore, 2),
            "change_pct": round(change_pct, 2),
            "direction": direction,
            "significance": significance,
            "status": _determine_sector_status(val1, val2),
            "priority_shift": _calculate_priority_shift(sector, sectors1, sectors2)
        })
    
    # Sort by absolute change amount
    comparison.sort(key=lambda x: abs(x["change_crore"]), reverse=True)
    
    return comparison

def _compare_fiscal_indicators(data1: dict, data2: dict, year1: str, year2: str) -> List[dict]:
    """Compare fiscal indicators with trend analysis."""
    
    fin1 = data1.get("financial", {})
    fin2 = data2.get("financial", {})
    
    fiscal1 = {f["indicator"]: f.get("percent") for f in fin1.get("fiscal_indicators", []) if f.get("percent")}
    fiscal2 = {f["indicator"]: f.get("percent") for f in fin2.get("fiscal_indicators", []) if f.get("percent")}
    
    # Convert string percentages to float
    for indicator in fiscal1:
        try:
            fiscal1[indicator] = float(str(fiscal1[indicator]).replace("%", ""))
        except (ValueError, TypeError):
            fiscal1[indicator] = None
    
    for indicator in fiscal2:
        try:
            fiscal2[indicator] = float(str(fiscal2[indicator]).replace("%", ""))
        except (ValueError, TypeError):
            fiscal2[indicator] = None
    
    all_indicators = set(fiscal1.keys()) | set(fiscal2.keys())
    
    comparison = []
    for indicator in all_indicators:
        val1 = fiscal1.get(indicator)
        val2 = fiscal2.get(indicator)
        
        if val1 is not None and val2 is not None:
            change = val2 - val1
            direction = "improved" if _is_improvement(indicator, change) else "worsened" if change != 0 else "stable"
            
            comparison.append({
                "indicator": indicator,
                f"{year1}_%": val1,
                f"{year2}_%": val2,
                "change": round(change, 2),
                "direction": direction,
                "fiscal_health_impact": _assess_fiscal_health_impact(indicator, change)
            })
    
    return comparison

def _compare_policies(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Compare policy schemes and initiatives."""
    
    pol1 = data1.get("policy", {})
    pol2 = data2.get("policy", {})
    
    schemes1 = set(s.get("name", s.get("sentence", ""))[:50] for s in pol1.get("named_schemes", []))
    schemes2 = set(s.get("name", s.get("sentence", ""))[:50] for s in pol2.get("named_schemes", []))
    
    # Analyze scheme changes
    new_schemes = schemes2 - schemes1
    dropped_schemes = schemes1 - schemes2
    continued_schemes = schemes1 & schemes2
    
    # Category comparison
    cat1 = pol1.get("by_category", {})
    cat2 = pol2.get("by_category", {})
    
    category_changes = {}
    all_categories = set(cat1.keys()) | set(cat2.keys())
    
    for category in all_categories:
        count1 = len(cat1.get(category, []))
        count2 = len(cat2.get(category, []))
        category_changes[category] = {
            year1: count1,
            year2: count2,
            "change": count2 - count1
        }
    
    return {
        "total_year1": pol1.get("total_count", 0),
        "total_year2": pol2.get("total_count", 0),
        "new_schemes": list(new_schemes),
        "dropped_schemes": list(dropped_schemes),
        "continued_schemes": list(continued_schemes),
        "category_changes": category_changes,
        "innovation_score": _calculate_policy_innovation_score(pol2, pol1)
    }

def _compare_tax_changes(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Compare tax policy changes."""
    
    tax1 = data1.get("tax", {})
    tax2 = data2.get("tax", {})
    
    # Compare tax change counts by category
    changes1 = tax1.get("tax_changes", [])
    changes2 = tax2.get("tax_changes", [])
    
    cat_count1 = defaultdict(int)
    cat_count2 = defaultdict(int)
    
    for change in changes1:
        cat_count1[change.get("category", "Other")] += 1
    
    for change in changes2:
        cat_count2[change.get("category", "Other")] += 1
    
    all_categories = set(cat_count1.keys()) | set(cat_count2.keys())
    
    category_comparison = {}
    for category in all_categories:
        category_comparison[category] = {
            year1: cat_count1[category],
            year2: cat_count2[category],
            "change": cat_count2[category] - cat_count1[category]
        }
    
    return {
        "total_changes": {
            year1: len(changes1),
            year2: len(changes2),
            "change": len(changes2) - len(changes1)
        },
        "category_comparison": category_comparison,
        "tax_burden_trend": _analyze_tax_burden_trend(changes1, changes2)
    }

def _compare_keywords(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Compare keyword frequency and identify shifts in focus."""
    
    kw1 = {kw["keyword"]: kw["frequency"] for kw in data1.get("keywords", [])}
    kw2 = {kw["keyword"]: kw["frequency"] for kw in data2.get("keywords", [])}
    
    # Find emerging and declining keywords
    all_keywords = set(kw1.keys()) | set(kw2.keys())
    
    emerging_keywords = []
    declining_keywords = []
    stable_keywords = []
    
    for keyword in all_keywords:
        freq1 = kw1.get(keyword, 0)
        freq2 = kw2.get(keyword, 0)
        
        if freq1 == 0 and freq2 > 0:
            emerging_keywords.append({"keyword": keyword, "frequency": freq2})
        elif freq1 > 0 and freq2 == 0:
            declining_keywords.append({"keyword": keyword, "frequency": freq1})
        elif freq1 > 0 and freq2 > 0:
            change_pct = (freq2 - freq1) / freq1 * 100
            if abs(change_pct) > 20:  # Significant change threshold
                if change_pct > 0:
                    emerging_keywords.append({
                        "keyword": keyword, 
                        "frequency": freq2, 
                        "change_pct": round(change_pct, 1)
                    })
                else:
                    declining_keywords.append({
                        "keyword": keyword, 
                        "frequency": freq1, 
                        "change_pct": round(change_pct, 1)
                    })
            else:
                stable_keywords.append({"keyword": keyword, "frequency": freq2})
    
    # Sort by frequency/change
    emerging_keywords.sort(key=lambda x: x["frequency"], reverse=True)
    declining_keywords.sort(key=lambda x: x["frequency"], reverse=True)
    
    return {
        "emerging_keywords": emerging_keywords[:10],
        "declining_keywords": declining_keywords[:10],
        "stable_keywords": stable_keywords[:10],
        "focus_shift_analysis": _analyze_focus_shift(emerging_keywords, declining_keywords)
    }

def _compare_sentiment(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Compare document sentiment and tone."""
    
    sent1 = data1.get("sentiment", {})
    sent2 = data2.get("sentiment", {})
    
    score1 = sent1.get("score", 0)
    score2 = sent2.get("score", 0)
    
    sentiment_change = score2 - score1
    
    return {
        year1: {
            "label": sent1.get("label", "Neutral"),
            "score": score1,
            "positive": sent1.get("positive", 0),
            "negative": sent1.get("negative", 0),
            "neutral": sent1.get("neutral", 0)
        },
        year2: {
            "label": sent2.get("label", "Neutral"),
            "score": score2,
            "positive": sent2.get("positive", 0),
            "negative": sent2.get("negative", 0),
            "neutral": sent2.get("neutral", 0)
        },
        "sentiment_change": round(sentiment_change, 3),
        "tone_shift": _determine_tone_shift(score1, score2),
        "optimism_index": _calculate_optimism_index(sent1, sent2)
    }

def _compare_innovation_metrics(data1: dict, data2: dict, year1: str, year2: str) -> dict:
    """Compare innovation and modernization focus."""
    
    # Innovation keywords to track
    innovation_keywords = [
        "digital", "technology", "ai", "artificial intelligence", "startup", 
        "innovation", "research", "development", "modernization", "automation",
        "blockchain", "iot", "5g", "cyber", "fintech", "biotech"
    ]
    
    kw1 = {kw["keyword"]: kw["frequency"] for kw in data1.get("keywords", [])}
    kw2 = {kw["keyword"]: kw["frequency"] for kw in data2.get("keywords", [])}
    
    innovation_score1 = sum(kw1.get(kw, 0) for kw in innovation_keywords)
    innovation_score2 = sum(kw2.get(kw, 0) for kw in innovation_keywords)
    
    return {
        "innovation_score": {
            year1: innovation_score1,
            year2: innovation_score2,
            "change": innovation_score2 - innovation_score1,
            "change_pct": round((innovation_score2 - innovation_score1) / max(innovation_score1, 1) * 100, 1)
        },
        "digital_focus_shift": innovation_score2 > innovation_score1,
        "modernization_trend": _assess_modernization_trend(kw1, kw2)
    }

# Helper functions

def _determine_sector_status(val1: float, val2: float) -> str:
    """Determine if sector is new, dropped, or continuing."""
    if val1 == 0 and val2 > 0:
        return "new"
    elif val1 > 0 and val2 == 0:
        return "dropped"
    else:
        return "continuing"

def _calculate_priority_shift(sector: str, sectors1: dict, sectors2: dict) -> dict:
    """Calculate how sector priority has shifted."""
    # Sort sectors by allocation to get rankings
    sorted1 = sorted(sectors1.items(), key=lambda x: x[1], reverse=True)
    sorted2 = sorted(sectors2.items(), key=lambda x: x[1], reverse=True)
    
    rank1 = next((i+1 for i, (s, _) in enumerate(sorted1) if s == sector), None)
    rank2 = next((i+1 for i, (s, _) in enumerate(sorted2) if s == sector), None)
    
    if rank1 and rank2:
        rank_change = rank1 - rank2  # Positive means moved up in priority
        return {
            "previous_rank": rank1,
            "current_rank": rank2,
            "rank_change": rank_change,
            "priority_direction": "increased" if rank_change > 0 else "decreased" if rank_change < 0 else "stable"
        }
    else:
        return {"status": "new" if rank2 else "dropped"}

def _is_improvement(indicator: str, change: float) -> bool:
    """Determine if a change in fiscal indicator is an improvement."""
    # For deficit indicators, decrease is improvement
    if "deficit" in indicator.lower():
        return change < 0
    # For growth indicators, increase is improvement
    elif "growth" in indicator.lower():
        return change > 0
    # For revenue indicators, increase is improvement
    elif "revenue" in indicator.lower():
        return change > 0
    else:
        return False  # Neutral for unknown indicators

def _assess_fiscal_health_impact(indicator: str, change: float) -> str:
    """Assess the impact of fiscal indicator change on overall fiscal health."""
    if abs(change) < 0.1:
        return "minimal"
    elif _is_improvement(indicator, change):
        return "positive" if abs(change) > 0.5 else "slightly_positive"
    else:
        return "negative" if abs(change) > 0.5 else "slightly_negative"

def _calculate_policy_innovation_score(pol2: dict, pol1: dict) -> float:
    """Calculate policy innovation score based on new initiatives."""
    new_schemes = len(pol2.get("named_schemes", [])) - len(pol1.get("named_schemes", []))
    new_categories = len(pol2.get("by_category", {})) - len(pol1.get("by_category", {}))
    
    # Simple scoring: new schemes + new categories, normalized
    base_score = max(new_schemes * 2 + new_categories * 5, 0)
    return min(base_score / 10, 10)  # Scale to 0-10

def _analyze_tax_burden_trend(changes1: list, changes2: list) -> str:
    """Analyze overall tax burden trend."""
    # Count increases vs decreases
    increases1 = sum(1 for c in changes1 if "increase" in c.get("change_type", "").lower())
    decreases1 = sum(1 for c in changes1 if "decrease" in c.get("change_type", "").lower())
    
    increases2 = sum(1 for c in changes2 if "increase" in c.get("change_type", "").lower())
    decreases2 = sum(1 for c in changes2 if "decrease" in c.get("change_type", "").lower())
    
    net1 = increases1 - decreases1
    net2 = increases2 - decreases2
    
    if net2 > net1:
        return "increasing_burden"
    elif net2 < net1:
        return "decreasing_burden"
    else:
        return "stable_burden"

def _analyze_focus_shift(emerging: list, declining: list) -> str:
    """Analyze the shift in policy focus based on keyword changes."""
    if not emerging and not declining:
        return "stable_focus"
    
    # Categorize keywords
    tech_keywords = ["digital", "technology", "ai", "innovation", "startup"]
    social_keywords = ["welfare", "health", "education", "employment"]
    infra_keywords = ["infrastructure", "road", "transport", "connectivity"]
    
    emerging_tech = sum(1 for kw in emerging if any(tech in kw["keyword"].lower() for tech in tech_keywords))
    emerging_social = sum(1 for kw in emerging if any(social in kw["keyword"].lower() for social in social_keywords))
    emerging_infra = sum(1 for kw in emerging if any(infra in kw["keyword"].lower() for infra in infra_keywords))
    
    if emerging_tech > emerging_social and emerging_tech > emerging_infra:
        return "shift_to_technology"
    elif emerging_social > emerging_tech and emerging_social > emerging_infra:
        return "shift_to_social"
    elif emerging_infra > emerging_tech and emerging_infra > emerging_social:
        return "shift_to_infrastructure"
    else:
        return "balanced_focus"

def _determine_tone_shift(score1: float, score2: float) -> str:
    """Determine the shift in document tone."""
    diff = score2 - score1
    if abs(diff) < 0.1:
        return "stable"
    elif diff > 0.2:
        return "more_positive"
    elif diff > 0:
        return "slightly_positive"
    elif diff < -0.2:
        return "more_negative"
    else:
        return "slightly_negative"

def _calculate_optimism_index(sent1: dict, sent2: dict) -> float:
    """Calculate an optimism index based on sentiment changes."""
    # Simple formula: (positive_ratio_2 - positive_ratio_1) * 100
    total1 = sent1.get("positive", 0) + sent1.get("negative", 0) + sent1.get("neutral", 0)
    total2 = sent2.get("positive", 0) + sent2.get("negative", 0) + sent2.get("neutral", 0)
    
    if total1 == 0 or total2 == 0:
        return 0
    
    ratio1 = sent1.get("positive", 0) / total1
    ratio2 = sent2.get("positive", 0) / total2
    
    return round((ratio2 - ratio1) * 100, 2)

def _assess_modernization_trend(kw1: dict, kw2: dict) -> str:
    """Assess the modernization trend based on keyword changes."""
    modern_keywords = ["digital", "online", "electronic", "automated", "smart", "tech"]
    traditional_keywords = ["manual", "paper", "offline", "traditional", "conventional"]
    
    modern_score1 = sum(kw1.get(kw, 0) for kw in modern_keywords)
    modern_score2 = sum(kw2.get(kw, 0) for kw in modern_keywords)
    
    traditional_score1 = sum(kw1.get(kw, 0) for kw in traditional_keywords)
    traditional_score2 = sum(kw2.get(kw, 0) for kw in traditional_keywords)
    
    modern_change = modern_score2 - modern_score1
    traditional_change = traditional_score2 - traditional_score1
    
    if modern_change > traditional_change:
        return "accelerating_modernization"
    elif modern_change < traditional_change:
        return "slowing_modernization"
    else:
        return "steady_modernization"