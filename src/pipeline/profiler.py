# src/pipeline/profiler.py

import pandas as pd

def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Performs lightweight EDA profiling.
    Returns:
        A dictionary containing:
        - missing_values: missing count & percentage
        - column_types: dtype classification
        - stats: basic statistics for numeric columns
    """
    # Missing values info
    missing_values = (
        df.isnull().sum()
        .to_frame("Missing Count")
        .assign(Percentage=lambda x: (x["Missing Count"] / len(df)) * 100)
    )

    # Column type info
    column_types = df.dtypes.to_frame("Type")

    # Basic numeric stats
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().T if not numeric_df.empty else pd.DataFrame()

    # Build profile dictionary
    profile = {
        "missing_values": missing_values,
        "column_types": column_types,
        "stats": stats
    }

    return profile
