# src/tools/utils.py

import pandas as pd

def load_dataset(uploaded_file):
    """
    Loads CSV or Excel into a Pandas DataFrame.
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
            return pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise e
