"""
Test Accuracy Validation System
Comprehensive testing for PolicyLens accuracy validation features
"""

import json
import sys
import os
from typing import Dict, Any

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.accuracy_validator import AccuracyValidator, validate_extraction_accuracy, get_accuracy_summary

def create_test_data() -> Dict[str, Any]:
    """Create comprehensive test data for validation testing"""
    return {
        "sector_allocations": [
            {
                "sector": "Agriculture & Allied",
                "amount_crore": 125000.0,
                "amount_text": "₹1,25,000 crore",
                "sentence": "The government has allocated ₹1,25,000 crore for agriculture and allied sectors in this budget.",
                "confidence": 95
            },
            {
                "sector": "Education & Skill Development", 
                "amount_crore": 85000.0,
                "amount_text": "₹85,000 crore",
                "sentence": "Education sector receives a substantial allocation of ₹85,000 crore for infrastructure development.",
                "confidence": 92
            },
            {
                "sector": "Health & Medical",
                "amount_crore": 75000.0,
                "amount_text": "₹75,000 crore",
                "sentence": "Healthcare budget provision stands at ₹75,000 crore including medical infrastructure.",
                "confidence": 90
            }
        ],
        "fiscal_indicators": [
            {
                "indicator": "Fiscal Deficit",
                "percent": 3.4,
                "amount_text": "₹18,35,000 crore",
                "amount_crore": 1835000.0,
                "sentence": "The fiscal deficit is estimated at 3.4% of GDP, amounting to ₹18,35,000 crore.",
                "confidence": 98
            },
            {
                "indicator": "Revenue Deficit", 
                "percent": 2.1,
                "sentence": "Revenue deficit is projected at 2.1% of GDP for the current fiscal year.",
                "confidence": 95
            },
            {
                "indicator": "GDP Growth",
                "percent": 6.8,
                "sentence": "The economy is expected to grow at 6.8% in the current financial year.",
                "confidence": 93
            }
        ],
        "policy_schemes": [
            {
                "sentence": "The government announces the new Digital India Mission 2.0 scheme for rural connectivity.",
                "category": "Digital Infrastructure"
            },
            {
                "sentence": "Pradhan Mantri Kisan Samman Nidhi scheme will be expanded to cover more farmers.",
                "category": "Agriculture"
            },
            {
                "sentence": "A new skill development initiative will be launched for youth employment.",
                "category": "Employment"
            }
        ],
        "tax_changes": [
            {
                "sentence": "Income tax rates for the middle class have been reduced by 2%.",
                "category": "Income Tax",
                "percent": 2.0,
                "change_type": "Reduced"
            },
            {
                "sentence": "GST on essential medicines is exempted from taxation.",
                "category": "GST",
                "change_type": "Exempted"
            }
        ]
    }

def create_problematic_test_data() -> Dict[str, Any]:
    """Create test data with known issues for validation testing"""
    return {
        "sector_allocations": [
            {
                "sector": "Unknown Sector",
                "amount_crore": -5000.0,  # Negative amount - should fail
                "amount_text": "₹-5,000 crore",
                "sentence": "This sentence doesn't mention the sector name at all.",
                "confidence": 45
            },
            {
                "sector": "Agriculture",
                "amount_crore": 50000000.0,  # Unrealistically large - should flag
                "amount_text": "₹50,00,000 crore", 
                "sentence": "Agriculture gets ₹50,00,000 crore allocation.",
                "confidence": 60
            }
        ],
        "fiscal_indicators": [
            {
                "indicator": "Fiscal Deficit",
                "percent": 25.0,  # Unrealistic percentage - should fail
                "sentence": "Fiscal deficit is 25% of GDP.",
                "confidence": 70
            },
            {
                "indicator": "GDP Growth",
                "percent": -15.0,  # Unrealistic negative growth - should flag
                "sentence": "GDP growth is -15%.",
                "confidence": 65
            }
        ],
        "policy_schemes": [
            {
                "sentence": "This is not a policy sentence at all.",  # No policy keywords
                "category": "Other"
            }
        ],
        "tax_changes": [
            {
                "sentence": "Tax rate is now 150%.",  # Unrealistic tax rate
                "percent": 150.0,
                "confidence": 50
            }
        ]
    }

def test_accuracy_validator():
    """Test the AccuracyValidator class"""
    print("🧪 Testing AccuracyValidator Class...")
    
    validator = AccuracyValidator()
    
    # Test with good data
    print("\n📊 Testing with high-quality data...")
    good_data = create_test_data()
    original_text = """
    The Union Budget 2024-25 presents a comprehensive financial plan for India's development.
    The government has allocated ₹1,25,000 crore for agriculture and allied sectors in this budget.
    Education sector receives a substantial allocation of ₹85,000 crore for infrastructure development.
    Healthcare budget provision stands at ₹75,000 crore including medical infrastructure.
    The fiscal deficit is estimated at 3.4% of GDP, amounting to ₹18,35,000 crore.
    Revenue deficit is projected at 2.1% of GDP for the current fiscal year.
    The economy is expected to grow at 6.8% in the current financial year.
    """
    
    validation_report = validator.validate_complete_extraction(good_data, original_text)
    
    print(f"✅ Overall Accuracy: {validation_report['overall_accuracy']:.1f}%")
    print(f"✅ Validation Passed: {validation_report['validation_passed']}")
    print(f"✅ Issues Found: {len(validation_report['issues'])}")
    
    # Test with problematic data
    print("\n⚠️ Testing with problematic data...")
    bad_data = create_problematic_test_data()
    
    validation_report_bad = validator.validate_complete_extraction(bad_data, original_text)
    
    print(f"❌ Overall Accuracy: {validation_report_bad['overall_accuracy']:.1f}%")
    print(f"❌ Validation Passed: {validation_report_bad['validation_passed']}")
    print(f"❌ Issues Found: {len(validation_report_bad['issues'])}")
    
    if validation_report_bad['issues']:
        print("\n🔍 Issues Detected:")
        for i, issue in enumerate(validation_report_bad['issues'][:5], 1):
            print(f"   {i}. {issue}")
    
    return validation_report, validation_report_bad

def test_sector_allocation_validation():
    """Test sector allocation validation specifically"""
    print("\n🏗️ Testing Sector Allocation Validation...")
    
    validator = AccuracyValidator()
    
    # Test valid allocations
    valid_allocations = [
        {
            "sector": "Agriculture & Allied",
            "amount_crore": 125000.0,
            "amount_text": "₹1,25,000 crore",
            "sentence": "The government has allocated ₹1,25,000 crore for agriculture and allied sectors.",
            "confidence": 95
        }
    ]
    
    score, issues, recommendations = validator._validate_sector_allocations(
        valid_allocations, 
        "The government has allocated ₹1,25,000 crore for agriculture and allied sectors."
    )
    
    print(f"✅ Valid Allocation Score: {score:.1f}%")
    print(f"✅ Issues: {len(issues)}")
    
    # Test invalid allocations
    invalid_allocations = [
        {
            "sector": "Unknown Sector",
            "amount_crore": -1000.0,  # Negative amount
            "amount_text": "₹-1,000 crore",
            "sentence": "This sentence has no sector mention.",
            "confidence": 30
        }
    ]
    
    score_bad, issues_bad, recommendations_bad = validator._validate_sector_allocations(
        invalid_allocations,
        "This sentence has no sector mention."
    )
    
    print(f"❌ Invalid Allocation Score: {score_bad:.1f}%")
    print(f"❌ Issues: {len(issues_bad)}")
    
    if issues_bad:
        print("🔍 Issues Found:")
        for issue in issues_bad:
            print(f"   - {issue}")

def test_fiscal_indicator_validation():
    """Test fiscal indicator validation specifically"""
    print("\n📊 Testing Fiscal Indicator Validation...")
    
    validator = AccuracyValidator()
    
    # Test valid indicators
    valid_indicators = [
        {
            "indicator": "Fiscal Deficit",
            "percent": 3.4,
            "sentence": "The fiscal deficit is estimated at 3.4% of GDP.",
            "confidence": 98
        }
    ]
    
    score, issues, recommendations = validator._validate_fiscal_indicators(
        valid_indicators,
        "The fiscal deficit is estimated at 3.4% of GDP."
    )
    
    print(f"✅ Valid Indicator Score: {score:.1f}%")
    print(f"✅ Issues: {len(issues)}")
    
    # Test invalid indicators
    invalid_indicators = [
        {
            "indicator": "Fiscal Deficit", 
            "percent": 25.0,  # Unrealistic
            "sentence": "Fiscal deficit is 25%.",
            "confidence": 60
        }
    ]
    
    score_bad, issues_bad, recommendations_bad = validator._validate_fiscal_indicators(
        invalid_indicators,
        "Fiscal deficit is 25%."
    )
    
    print(f"❌ Invalid Indicator Score: {score_bad:.1f}%")
    print(f"❌ Issues: {len(issues_bad)}")

def test_confidence_metrics():
    """Test confidence metrics calculation"""
    print("\n🎯 Testing Confidence Metrics...")
    
    validator = AccuracyValidator()
    test_data = create_test_data()
    
    metrics = validator._calculate_confidence_metrics(test_data)
    
    print("📊 Confidence Metrics:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.1f}%")

def test_data_quality_score():
    """Test data quality score calculation"""
    print("\n🏆 Testing Data Quality Score...")
    
    validator = AccuracyValidator()
    test_data = create_test_data()
    original_text = "Sample budget document with comprehensive financial data and policy information."
    
    quality_score = validator._calculate_data_quality_score(test_data, original_text)
    
    print(f"📊 Data Quality Score: {quality_score:.1f}%")

def test_accuracy_summary():
    """Test accuracy summary generation"""
    print("\n📋 Testing Accuracy Summary Generation...")
    
    test_data = create_test_data()
    original_text = "Sample budget document text for testing."
    
    validation_report = validate_extraction_accuracy(test_data, original_text)
    summary = get_accuracy_summary(validation_report)
    
    print("📊 Generated Summary:")
    print(summary)

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🔬 Testing Edge Cases...")
    
    validator = AccuracyValidator()
    
    # Test empty data
    empty_data = {
        "sector_allocations": [],
        "fiscal_indicators": [],
        "policy_schemes": [],
        "tax_changes": []
    }
    
    validation_report = validator.validate_complete_extraction(empty_data, "Empty document")
    print(f"📊 Empty Data Accuracy: {validation_report['overall_accuracy']:.1f}%")
    
    # Test minimal data
    minimal_data = {
        "sector_allocations": [
            {
                "sector": "Test",
                "amount_crore": 1000.0,
                "sentence": "Test allocation of ₹1,000 crore for test sector.",
                "confidence": 80
            }
        ]
    }
    
    validation_report = validator.validate_complete_extraction(minimal_data, "Minimal document")
    print(f"📊 Minimal Data Accuracy: {validation_report['overall_accuracy']:.1f}%")

def run_comprehensive_tests():
    """Run all accuracy validation tests"""
    print("🚀 Starting Comprehensive Accuracy Validation Tests")
    print("=" * 60)
    
    try:
        # Test main validator
        good_report, bad_report = test_accuracy_validator()
        
        # Test specific components
        test_sector_allocation_validation()
        test_fiscal_indicator_validation()
        test_confidence_metrics()
        test_data_quality_score()
        test_accuracy_summary()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ All Accuracy Validation Tests Completed Successfully!")
        
        # Summary
        print(f"\n📊 Test Summary:")
        print(f"   Good Data Accuracy: {good_report['overall_accuracy']:.1f}%")
        print(f"   Bad Data Accuracy: {bad_report['overall_accuracy']:.1f}%")
        print(f"   Validation System: {'✅ Working' if good_report['validation_passed'] and not bad_report['validation_passed'] else '❌ Issues'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)