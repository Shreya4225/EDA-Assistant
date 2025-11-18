import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.agents.nlp_intent_parser import detect_intent

queries = [
    "describe the dataset",
    "Describe",
    "give me an overview",
    "show distribution of age"
]

for q in queries:
    print(q, "->", detect_intent(q))
