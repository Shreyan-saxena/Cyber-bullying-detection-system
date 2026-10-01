# test.py — run this to test sentiment analysis
from classifier import FastClassifier
from detector import GroqDetector

clf = FastClassifier()
det = GroqDetector()

tests = [
    "I absolutely love the new update, it's amazing!",
    "This is the worst experience I've ever had.",
    "The weather is quite normal today, nothing special.",
    "I'm not sure if I like it or hate it, it's okay I guess.",
    "This is so cool! I'm really happy with the results."
]

for text in tests:
    print(f"\nText: {text}")
    
    # Stage 1: Classifier
    clf_result = clf.score(text)
    print(f"Fast Classifier: {clf_result['label']} (conf: {clf_result['score']:.2f})")
    
    # Stage 2: Groq LLM
    llm_result = det.analyze(text)
    print(f"Groq LLM: {llm_result.get('verdict')} ({llm_result.get('confidence', 0)})")
    print(f"Reasoning: {llm_result.get('reasoning')}")
