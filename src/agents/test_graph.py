import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import pandas as pd
from src.agents.langgraph_workflow import chatbot

df = pd.DataFrame({
    "Sales": [100, 200, 150, 180],
    "Region": ["West", "East", "East", "West"]
})

result = chatbot.invoke({"user_input": "show sales distribution", "df": df})
print(result)
