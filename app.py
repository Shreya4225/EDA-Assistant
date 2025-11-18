# # app.py

# import streamlit as st
# from src.ui.layout import render_main_layout

# def main():
#     # Basic page config
#     st.set_page_config(
#         page_title="EDA Assistant",
#         page_icon="📊",
#         layout="wide"
#     )

#     # Render main UI
#     render_main_layout()

# if __name__ == "__main__":
#     main()


import streamlit as st
from src.ui.layout import render_main_layout

def main():
    st.set_page_config(
        page_title="EDA Assistant",
        page_icon="📊",
        layout="wide"
    )

    # 🔹 Ensure cleaned dataset key always exists in session state
    if "cleaned_dataset" not in st.session_state:
        st.session_state["cleaned_dataset"] = None

    render_main_layout()

if __name__ == "__main__":
    main()
