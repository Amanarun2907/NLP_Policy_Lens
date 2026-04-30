"""Quick test for Phase 2 modules — no PDF needed."""
from utils.text_cleaner import clean_text
from utils.normalizer   import normalize_text, parse_amount

# ── Test 1: Text Cleaner
raw = """
UNION BUDGET 2024-25
1
Page 2
- - - - -
The Government has proposed an allocation of Rs. 1,50,000 crore for infrastructure.
The Government has proposed an allocation of Rs. 1,50,000 crore for infrastructure.
This is a duplicate line that should be removed.
This is a duplicate line that should be removed.
A new scheme will be launched for farmers
across the country to improve agricultural productivity.
"""

cleaned = clean_text(raw, language="English")
print("=" * 60)
print("CLEANED TEXT:")
print(cleaned)

# ── Test 2: Normalizer
samples = [
    "An allocation of ₹2 lakh crore has been proposed.",
    "Rs. 50,000 crore for defence sector.",
    "two lakh crore rupees for infrastructure.",
    "fifty thousand crore for education.",
    "$5 billion in foreign investment.",
    "The fiscal deficit is 5.1% of GDP.",
]

print("\n" + "=" * 60)
print("NORMALIZED TEXT:")
for s in samples:
    print(f"  IN : {s}")
    print(f"  OUT: {normalize_text(s)}")
    print()

# ── Test 3: parse_amount
amounts = [
    "2 lakh crore",
    "50,000 crore",
    "1.5 lakh crore",
    "five hundred crore",
]
print("=" * 60)
print("PARSED AMOUNTS:")
for a in amounts:
    print(f"  '{a}'  →  {parse_amount(a):,.0f}")
