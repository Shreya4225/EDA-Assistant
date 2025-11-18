# src/tools/chart_generator.py

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

TEMP_DIR = "src/data/temp"

os.makedirs(TEMP_DIR, exist_ok=True)

def generate_chart(df: pd.DataFrame, col1: str, col2: str = None, chart_type: str = "line"):
    """
    Generates chart and saves into temp folder.
    Returns the image file path.
    """

    plt.figure(figsize=(8, 4))

    if chart_type == "line":
        df[col1].plot(kind="line")
        plt.title(f"Line Plot of {col1}")

    elif chart_type == "bar":
        df[col1].value_counts().plot(kind="bar")
        plt.title(f"Bar Chart of {col1}")

    elif chart_type == "hist":
        df[col1].plot(kind="hist", bins=30)
        plt.title(f"Histogram of {col1}")

    elif chart_type == "scatter" and col2:
        plt.scatter(df[col1], df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title(f"Scatter Plot: {col1} vs {col2}")

    elif chart_type == "heatmap":
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")

    else:
        return None

    filename = f"chart_{chart_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(TEMP_DIR, filename)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

    return file_path
