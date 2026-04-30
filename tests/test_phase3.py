"""Quick test for Phase 3 NLP Core modules."""
from utils.sentence_segmenter import segment_sentences
from utils.ner_extractor       import extract_entities, tag_sentence, extract_monetary_values
from utils.keyword_scorer      import rank_sentences, get_top_keywords
from utils.sentiment_analyzer  import analyze_sentiment

SAMPLE = """
The Government has proposed an allocation of Rs. 1,50,000 crore for infrastructure development.
I propose to launch a new scheme for farmers to improve agricultural productivity across the country.
The fiscal deficit is targeted at 5.1 percent of GDP for the year 2024-25.
Income tax exemption limit has been increased to Rs. 12 lakh for individual taxpayers.
A new Digital India Mission will be established with an outlay of Rs. 10,000 crore.
The capital expenditure has been increased by 33 percent to Rs. 10 lakh crore.
GST collections have shown robust growth reaching a record high of Rs. 1.87 lakh crore in April.
We will set up 100 new Eklavya Model Residential Schools in tribal areas.
The revenue deficit is estimated at 2.9 percent of GDP.
Customs duty on mobile phones has been reduced to promote domestic manufacturing.
"""

print("=" * 65)
print("1. SENTENCE SEGMENTATION")
sentences = segment_sentences(SAMPLE, language="English")
for i, s in enumerate(sentences, 1):
    print(f"  [{i}] {s[:90]}")

print("\n" + "=" * 65)
print("2. SENTENCE TAGGING")
for s in sentences[:5]:
    tags = tag_sentence(s)
    print(f"  TAGS {tags}")
    print(f"  SENT {s[:80]}\n")

print("=" * 65)
print("3. NER EXTRACTION")
ents = extract_entities(sentences)
print(f"  Money mentions  : {len(ents.get('money', []))}")
print(f"  Sectors found   : {list(set(e['sector'] for e in ents.get('sectors', [])))}")
print(f"  Fiscal terms    : {list(set(e['term'] for e in ents.get('fiscal_terms', [])))}")
print(f"  Organizations   : {ents.get('organizations', [])}")

print("\n" + "=" * 65)
print("4. MONETARY VALUES")
moneys = extract_monetary_values(sentences)
for m in moneys:
    print(f"  {m['value_text']:30s}  tags={m['tags']}")

print("\n" + "=" * 65)
print("5. TOP KEYWORDS")
kws = get_top_keywords(sentences, top_n=10)
for k in kws:
    print(f"  {k['keyword']:20s}  freq={k['frequency']}  score={k['score']}")

print("\n" + "=" * 65)
print("6. SENTENCE RANKING (top 5)")
ranked = rank_sentences(sentences, top_n=5)
for r in ranked:
    print(f"  Rank {r['rank']}  score={r['score']}  | {r['sentence'][:80]}")

print("\n" + "=" * 65)
print("7. SENTIMENT ANALYSIS")
result = analyze_sentiment(SAMPLE)
print(f"  Overall label : {result['label']}")
print(f"  Score         : {result['score']}")
print(f"  Positive sents: {result['positive']}")
print(f"  Negative sents: {result['negative']}")
print(f"  Neutral sents : {result['neutral']}")
