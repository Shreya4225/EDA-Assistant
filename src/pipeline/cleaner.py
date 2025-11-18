# src/pipeline/cleaner.py

import pandas as pd

def suggest_imputation(df: pd.DataFrame) -> dict:
    """
    Suggests a default imputation strategy per column with missing values:
    - Numerical: median
    - Categorical: most frequent
    """
    suggestions = {}
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                suggestions[col] = "Median"
            else:
                suggestions[col] = "Most Frequent"
    return suggestions


def apply_imputation(df: pd.DataFrame, strategies: dict) -> pd.DataFrame:
    """
    Applies selected imputation strategies per column.
    """
    df_clean = df.copy()

    for col, method in strategies.items():
        if method == "Median":
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
        elif method == "Mean":
            df_clean[col].fillna(df_clean[col].mean(), inplace=True)
        elif method == "Most Frequent":
            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        elif method == "Drop":
            df_clean.dropna(subset=[col], inplace=True)

    return df_clean
