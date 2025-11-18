# src/pipeline/report_builder.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

REPORT_CHART_DIR = "src/data/report_charts"

# Ensure chart directory exists
os.makedirs(REPORT_CHART_DIR, exist_ok=True)


def _save_chart(fig, filename: str) -> str:
    """Save chart to disk and return its filepath."""
    path = os.path.join(REPORT_CHART_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def _get_numeric_cols(df):
    return df.select_dtypes(include=["int64", "float64"]).columns.tolist()


def _get_cat_cols(df):
    return df.select_dtypes(include=["object"]).columns.tolist()


def _get_date_cols(df):
    return df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()


def generate_report_charts(df):
    """Automatically selects and generates up to 6 charts."""

    numeric_cols = _get_numeric_cols(df)
    cat_cols = _get_cat_cols(df)
    date_cols = _get_date_cols(df)

    chart_paths = []
    captions = []

    # 1️⃣ Histogram
    if numeric_cols:
        col = numeric_cols[0]
        fig = plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        chart_paths.append(_save_chart(fig, "histogram.png"))
        captions.append(f"Histogram of {col} — distribution of values.")

    # 2️⃣ Boxplot
    if numeric_cols:
        col = numeric_cols[0]
        fig = plt.figure()
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot of {col}")
        chart_paths.append(_save_chart(fig, "boxplot.png"))
        captions.append(f"Boxplot of {col} — outlier detection.")

    # 3️⃣ Bar chart for categorical
    if cat_cols:
        col = cat_cols[0]
        fig = plt.figure()
        df[col].value_counts().plot(kind="bar")
        plt.title(f"Distribution of {col}")
        chart_paths.append(_save_chart(fig, "bar_chart.png"))
        captions.append(f"Distribution of {col} — frequency counts.")

    # 4️⃣ Scatter plot
    if len(numeric_cols) >= 2:
        fig = plt.figure()
        sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]])
        plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
        chart_paths.append(_save_chart(fig, "scatter.png"))
        captions.append("Scatter plot — correlation between numeric values.")

    # 5️⃣ Line chart (trend)
    if date_cols and numeric_cols:
        fig = plt.figure()
        sns.lineplot(x=df[date_cols[0]], y=df[numeric_cols[0]])
        plt.title(f"Trend of {numeric_cols[0]} over time")
        chart_paths.append(_save_chart(fig, "line.png"))
        captions.append("Line chart — numeric trend over dates.")

    # 6️⃣ Correlation Heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = plt.figure(figsize=(6, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        chart_paths.append(_save_chart(fig, "heatmap.png"))
        captions.append("Heatmap — strength of numeric relationships.")

    return chart_paths, captions
