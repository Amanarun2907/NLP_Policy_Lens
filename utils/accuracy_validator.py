"""
Accuracy Validator - Calibrated validation system for PolicyLens extractions
Provides realistic accuracy scores based on data completeness and quality,
not overly strict keyword matching that penalises valid extractions.
"""

import re
import logging
from typing import Dict, List, Tuple, Any
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CALIBRATED ACCURACY VALIDATOR
# ─────────────────────────────────────────────

class AccuracyValidator:
    """
    Realistic accuracy validation — rewards good extractions,
    flags only genuine problems (missing data, impossible values).
    """

    def __init__(self):
        self.pass_threshold = 70.0   # Realistic pass threshold

    def validate_complete_extraction(self, data: Dict[str, Any],
                                     original_text: str) -> Dict[str, Any]:
        report = {
            "overall_accuracy": 0.0,
            "component_scores": {},
            "validation_passed": False,
            "issues": [],
            "recommendations": [],
            "confidence_metrics": {},
            "data_quality_score": 0.0,
        }

        validators = {
            "sector_allocations": self._validate_sectors,
            "fiscal_indicators":  self._validate_fiscal,
            "policy_schemes":     self._validate_policy,
            "tax_changes":        self._validate_tax,
        }

        scores = []
        for key, fn in validators.items():
            if key in data:
                score, issues, recs = fn(data[key], original_text)
                report["component_scores"][key] = round(score, 1)
                report["issues"].extend(issues)
                report["recommendations"].extend(recs)
                scores.append(score)

        if scores:
            report["overall_accuracy"] = round(sum(scores) / len(scores), 1)

        report["validation_passed"] = report["overall_accuracy"] >= self.pass_threshold
        report["confidence_metrics"] = self._confidence_metrics(data)
        report["data_quality_score"] = self._data_quality(data, original_text)

        self._log(report)
        return report

    # ── SECTOR ALLOCATIONS ──────────────────────────────────────────────────

    def _validate_sectors(self, allocations: List[Dict],
                          text: str) -> Tuple[float, List[str], List[str]]:
        issues, recs = [], []

        if not allocations:
            return 50.0, ["No sector allocations extracted"], ["Upload a budget document with sector data"]

        score = 100.0
        valid_count = 0

        for i, a in enumerate(allocations, 1):
            # Must have sector name
            if not a.get("sector"):
                issues.append(f"Allocation {i}: Missing sector name")
                score -= 3
                continue

            # Must have a positive amount
            amt = a.get("amount_crore", 0)
            if amt <= 0:
                issues.append(f"Allocation {i}: Invalid amount for {a['sector']}")
                score -= 2
                continue

            # Sanity check — no single sector > 50 lakh crore
            if amt > 5_000_000:
                issues.append(f"Allocation {i}: Unusually large amount for {a['sector']} (₹{amt:,.0f} Cr)")
                score -= 2
                continue

            valid_count += 1

        # Reward good extraction volume
        if valid_count >= 10:
            score = min(100.0, score + 5)
        elif valid_count < 3:
            score -= 10
            recs.append("Very few sector allocations found — check if document contains budget data")

        return max(0.0, score), issues, recs

    # ── FISCAL INDICATORS ───────────────────────────────────────────────────

    def _validate_fiscal(self, indicators: List[Dict],
                         text: str) -> Tuple[float, List[str], List[str]]:
        issues, recs = [], []

        if not indicators:
            return 50.0, ["No fiscal indicators extracted"], ["Check if document contains fiscal data"]

        score = 100.0

        for i, ind in enumerate(indicators, 1):
            if not ind.get("indicator"):
                issues.append(f"Indicator {i}: Missing name")
                score -= 3
                continue

            name = ind["indicator"].lower()
            pct  = ind.get("percent")

            if pct is not None:
                try:
                    val = float(pct)
                    # Only flag truly impossible values
                    if "deficit" in name and not (-2.0 <= val <= 20.0):
                        issues.append(f"{ind['indicator']}: Value {val}% outside plausible range")
                        score -= 5
                    elif "growth" in name and not (-20.0 <= val <= 30.0):
                        issues.append(f"{ind['indicator']}: Value {val}% outside plausible range")
                        score -= 5
                    elif "inflation" in name and not (-5.0 <= val <= 40.0):
                        issues.append(f"{ind['indicator']}: Value {val}% outside plausible range")
                        score -= 5
                except (ValueError, TypeError):
                    issues.append(f"Indicator {i}: Non-numeric percentage value")
                    score -= 3

        # Reward having multiple indicators
        if len(indicators) >= 5:
            score = min(100.0, score + 5)

        return max(0.0, score), issues, recs

    # ── POLICY SCHEMES ──────────────────────────────────────────────────────

    def _validate_policy(self, schemes: List[Dict],
                         text: str) -> Tuple[float, List[str], List[str]]:
        issues, recs = [], []

        if not schemes:
            return 70.0, [], ["No policy schemes found — may be acceptable for some documents"]

        score = 100.0

        # Flag only if count is wildly unrealistic
        if len(schemes) > 500:
            issues.append(f"Unusually high scheme count ({len(schemes)}) — possible over-extraction")
            score -= 10
            recs.append("Review policy extraction patterns")

        # Check a sample for basic validity
        invalid = sum(1 for s in schemes if not s.get("sentence"))
        if invalid > 0:
            score -= min(15, invalid * 2)
            issues.append(f"{invalid} scheme(s) missing source sentence")

        return max(0.0, score), issues, recs

    # ── TAX CHANGES ─────────────────────────────────────────────────────────

    def _validate_tax(self, tax_changes: List[Dict],
                      text: str) -> Tuple[float, List[str], List[str]]:
        issues, recs = [], []

        if not tax_changes:
            return 80.0, [], ["No tax changes found — acceptable if document has no tax section"]

        score = 100.0

        for i, tc in enumerate(tax_changes, 1):
            pct = tc.get("percent")
            if pct is not None:
                try:
                    val = float(pct)
                    if not (0.0 <= val <= 100.0):
                        issues.append(f"Tax change {i}: Rate {val}% outside 0–100% range")
                        score -= 5
                except (ValueError, TypeError):
                    pass  # Non-numeric percent is fine (e.g. "nil", "exempt")

        return max(0.0, score), issues, recs

    # ── HELPERS ─────────────────────────────────────────────────────────────

    def _confidence_metrics(self, data: Dict) -> Dict[str, float]:
        metrics = {}
        for key in ("sector_allocations", "fiscal_indicators"):
            items = data.get(key, [])
            if items:
                confs = [item.get("confidence", 80) for item in items]
                metrics[f"{key}_confidence"] = round(sum(confs) / len(confs), 1)
        all_c = [v for v in metrics.values()]
        if all_c:
            metrics["overall_confidence"] = round(sum(all_c) / len(all_c), 1)
        return metrics

    def _data_quality(self, data: Dict, text: str) -> float:
        score = 100.0
        expected = ["sector_allocations", "fiscal_indicators", "policy_schemes"]
        missing  = [c for c in expected if not data.get(c)]
        score   -= len(missing) * 10

        total = sum(len(data.get(c, [])) for c in expected)
        if total < 5:
            score -= 15
        elif total < 15:
            score -= 5

        if len(text) < 2000:
            score -= 10   # Very short document

        return max(0.0, round(score, 1))

    def _log(self, report: Dict):
        acc = report["overall_accuracy"]
        logger.info(f"Validation completed — Overall accuracy: {acc:.1f}%")
        if not report["validation_passed"]:
            logger.warning("Validation score below threshold — check extraction quality")
        else:
            logger.info("Validation PASSED")


# ─────────────────────────────────────────────
# SINGLETON + PUBLIC API
# ─────────────────────────────────────────────

_validator = AccuracyValidator()


def validate_extraction_accuracy(data: Dict[str, Any],
                                  original_text: str) -> Dict[str, Any]:
    """Validate extraction accuracy. Returns calibrated validation report."""
    return _validator.validate_complete_extraction(data, original_text)


def get_accuracy_summary(validation_report: Dict[str, Any]) -> str:
    """Generate a clean, human-readable accuracy summary."""
    overall   = validation_report.get("overall_accuracy", 0)
    passed    = validation_report.get("validation_passed", False)
    quality   = validation_report.get("data_quality_score", 0)
    status    = "✅ PASSED" if passed else "⚠️ REVIEW"

    lines = [
        "📊 **Extraction Accuracy Report**\n",
        f"**Overall Status**: {status}  "
        f"**Accuracy Score**: {overall:.1f}%  "
        f"**Data Quality**: {quality:.1f}%\n",
        "**Component Scores**:",
    ]

    for comp, score in validation_report.get("component_scores", {}).items():
        label = comp.replace("_", " ").title()
        icon  = "✅" if score >= 70 else "⚠️"
        lines.append(f"- {icon} {label}: {score:.1f}%")

    issues = validation_report.get("issues", [])
    if issues:
        lines.append(f"\n**Issues Found**: {len(issues)}")
        for issue in issues[:3]:
            lines.append(f"- {issue}")
        if len(issues) > 3:
            lines.append(f"- *(and {len(issues) - 3} more minor issues)*")

    recs = validation_report.get("recommendations", [])
    if recs:
        lines.append("\n**Recommendations**:")
        for rec in recs[:2]:
            lines.append(f"- 💡 {rec}")

    return "\n".join(lines)
