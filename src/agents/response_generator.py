# src/agents/response_generator.py

import streamlit as st
from src.agents.llm_client import get_llm
from src.agents.nlp_intent_parser import detect_intent, parse_chart_request
from src.tools.chart_generator import generate_chart
import pandas as pd


def handle_user_query(user_input: str):
    df = st.session_state.get("cleaned_dataset")

    if df is None:
        return ("⚠️ No dataset found. Please upload and clean data first.", None)

    intent = detect_intent(user_input)
    df_columns = df.columns.tolist()

    # --- Intent: Describe Dataset ---
    if intent == "describe":
        return (
            f"The dataset has **{df.shape[0]} rows** and **{df.shape[1]} columns**.\n\n"
            "Column names:\n- " + "\n- ".join(df_columns),
            None
        )

    # --- Intent: Show Columns ---
    if intent == "columns":
        return (
            "Here are the columns:\n- " + "\n- ".join(df_columns),
            None
        )

    # --- Intent: Missing Values ---
    if intent == "missing":
        missing = df.isnull().sum()
        msg = "Missing values per column:\n" + missing.to_string()
        return (msg, None)

    # --- Intent: Stats ---
    if intent == "stats":
        stats = df.describe().transpose()
        msg = "📊 Basic Statistics:\n\n" + stats.to_string()
        return (msg, None)

    # --- Intent: Chart ---
    if intent == "chart":
        detected_cols, chart_type = parse_chart_request(user_input, df_columns, df)

        if len(detected_cols) == 0:
            return ("Please mention a valid column name to visualize.", None)

        if len(detected_cols) == 1:
            img = generate_chart(df, detected_cols[0], chart_type=chart_type)
            return (f"📈 Showing {chart_type} chart for **{detected_cols[0]}**", img)

        if len(detected_cols) >= 2:
            img = generate_chart(df, detected_cols[0], detected_cols[1], chart_type="scatter")
            return (f"📈 Scatter plot: **{detected_cols[0]} vs {detected_cols[1]}**", img)

    # --- Fallback: LLM handles unknown ---
    llm = get_llm()
    try:
        ai_msg = llm.invoke(
            f"You are an EDA assistant. Respond briefly.\nUser: {user_input}"
        )
        response = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)
    except:
        response = "I couldn't understand that — try asking about statistics or charts."

    return (response, None)
