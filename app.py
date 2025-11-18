# app.py

import streamlit as st
from src.ui.layout import render_main_layout

def main():
    # Basic page config
    st.set_page_config(
        page_title="EDA Assistant",
        page_icon="📊",
        layout="wide"
    )

    # Render main UI
    render_main_layout()

if __name__ == "__main__":
    main()
