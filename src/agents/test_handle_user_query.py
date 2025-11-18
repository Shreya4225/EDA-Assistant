import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
from src.agents.response_generator import handle_user_query

# Load any small CSV you have; or use your raw_dataset sample
df = pd.read_csv("src/data/sample_dataset.csv")  # adjust path if needed

queries = [
    "describe the dataset",
    "columns",
    "missing values",
    "stats",
    "show distribution of age",
    "hello"
]

for q in queries:
    print("\n=== QUERY:", q, "===")
    text, chart = handle_user_query(df, q)
    print("TEXT RESPONSE:\n", text)
    print("CHART PATH:", chart)
