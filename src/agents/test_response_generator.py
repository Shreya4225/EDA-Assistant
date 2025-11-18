import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pandas as pd
from src.agents.response_generator import handle_user_query

df = pd.DataFrame({
    "Sales": [100, 200, 150, 180],
    "Region": ["West", "East", "East", "West"]
})

queries = [
    "show sales distribution",
    "plot relationship between sales and sales",
    "what are the columns?",
    "show bar chart"
]

for q in queries:
    print("\nQuery:", q)
    resp, img = handle_user_query(df, q)
    print("Response:", resp)
    print("Chart Path:", img)
