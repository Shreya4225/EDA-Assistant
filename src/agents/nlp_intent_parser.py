# src/agents/nlp_intent_parser.py

# src/agents/nlp_intent_parser.py

import re
from typing import List, Tuple
import pandas as pd

# --- Detect Intent ---
def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(x in text for x in ["describe", "summary", "overview"]):
        return "describe"
    if "column" in text or "columns" in text:
        return "columns"
    if "missing" in text or "null" in text:
        return "missing"
    if any(x in text for x in ["mean", "median", "std", "statistics", "stat"]):
        return "stats"
    if any(x in text for x in ["plot", "chart", "visual", "show", "graph", "trend",
                               "distribution", "compare", "relationship", "heatmap"]):
        return "chart"

    return "unknown"


# --- Smart chart type inference ---
def infer_best_chart(df, user_text: str) -> Tuple[List[str], str]:
    numeric_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime", "datetime64[ns]"]).columns.tolist()

    # Trend intent
    if "trend" in user_text or "time" in user_text:
        if date_cols and numeric_cols:
            return [date_cols[0], numeric_cols[0]], "line"

    # Histogram
    if "distribution" in user_text or "hist" in user_text:
        if numeric_cols:
            return [numeric_cols[0]], "hist"

    # Scatter
    if "compare" in user_text or "relationship" in user_text:
        if len(numeric_cols) >= 2:
            return numeric_cols[:2], "scatter"

    # Bar chart for categorical
    if "bar" in user_text or "category" in user_text:
        if cat_cols:
            return [cat_cols[0]], "bar"

    # Heatmap
    if "heatmap" in user_text:
        if len(numeric_cols) >= 2:
            return numeric_cols, "heatmap"

    # Default fallback
    if numeric_cols:
        return [numeric_cols[0]], "hist"

    return [], "unknown"


# --- Parse chart request (uses inference if needed) ---
def parse_chart_request(user_input: str, df_columns: List[str], df: pd.DataFrame = None) -> Tuple[List[str], str]:
    user_lower = user_input.lower()
    detected_cols = []

    # Detect explicit column mentions
    for col in df_columns:
        if col.lower() in user_lower:
            detected_cols.append(col)

    # Detect explicit chart type
    if "line" in user_lower or "trend" in user_lower:
        chart_type = "line"
    elif "scatter" in user_lower or "relationship" in user_lower:
        chart_type = "scatter"
    elif "bar" in user_lower or "category" in user_lower or "count" in user_lower:
        chart_type = "bar"
    elif "distribution" in user_lower or "hist" in user_lower:
        chart_type = "hist"
    elif "heatmap" in user_lower:
        chart_type = "heatmap"
    else:
        chart_type = "auto"

    # If user did not specify column → infer from dataset
    if len(detected_cols) == 0 and df is not None:
        detected_cols, chart_type = infer_best_chart(df, user_lower)

    return detected_cols, chart_type




# # src/agents/nlp_intent_parser.py

# def detect_intent(user_input: str) -> str:
#     """
#     Simple rule-based intent detector.
#     Returns one of the following:
#     - "describe"
#     - "columns"
#     - "missing"
#     - "stats"
#     - "chart"
#     - "unknown"
#     """
#     text = user_input.lower()

#     if any(word in text for word in ["describe", "summary", "overview"]):
#         return "describe"
#     if "column" in text or "columns" in text:
#         return "columns"
#     if "missing" in text or "null" in text:
#         return "missing"
#     if any(word in text for word in ["mean", "median", "std", "statistics", "stat"]):
#         return "stats"
#     if any(word in text for word in ["plot", "chart", "visual", "graph", "trend", "distribution", "relation"]):
#         return "chart"

#     return "unknown"



# def extract_columns(user_input: str, df_columns: list) -> list:
#     """
#     Extract column names mentioned in the user's text.
#     """
#     text = user_input.lower()
#     detected = [col for col in df_columns if col.lower() in text]
#     return detected



# def detect_chart_type(user_input: str) -> str:
#     """
#     Determine the chart type from user input.
#     Returns: bar, scatter, hist, heatmap, line (default)
#     """
#     text = user_input.lower()

#     if "bar" in text:
#         return "bar"
#     if "scatter" in text:
#         return "scatter"
#     if any(word in text for word in ["hist", "distribution", "dist"]):
#         return "hist"
#     if "heatmap" in text:
#         return "heatmap"
    
#     return "line"  # Default fallback



# def parse_chart_request(user_input: str, df_columns: list):
#     """
#     Extract both chart type and the relevant columns.
#     Returns:
#         detected_columns (list)
#         chart_type (str)
#     """
#     detected_cols = extract_columns(user_input, df_columns)
#     chart_type = detect_chart_type(user_input)

#     return detected_cols, chart_type
