import streamlit as st
from src.ui.layout import render_main_layout


def main():
    """
    Main application entry point with enhanced configuration
    """
    
    # Enhanced Page Configuration
    st.set_page_config(
        page_title="EDA Assistant - AI Powered Data Analysis",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://github.com/yourusername/eda-assistant',
            'Report a bug': 'https://github.com/yourusername/eda-assistant/issues',
            'About': '''
            # EDA Assistant 🧠
            
            **Version:** 2.0.0
            
            An AI-powered Exploratory Data Analysis tool that helps you:
            - 📊 Profile your datasets instantly
            - 🧹 Clean and fix data issues
            - 💬 Chat with AI for insights
            - 📄 Generate professional reports
            
            Built with ❤️ using Streamlit and LangChain
            '''
        }
    )
    
    # Initialize session state variables
    initialize_session_state()
    
    # Render the main layout
    render_main_layout()


def initialize_session_state():
    """
    Initialize all required session state variables
    """
    
    # Dataset storage
    if "raw_dataset" not in st.session_state:
        st.session_state["raw_dataset"] = None
    
    if "cleaned_dataset" not in st.session_state:
        st.session_state["cleaned_dataset"] = None
    
    # Profiling results
    if "profile_result" not in st.session_state:
        st.session_state["profile_result"] = None
    
    # Chat history for AI agent
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # User preferences
    if "theme" not in st.session_state:
        st.session_state["theme"] = "gradient"
    
    # Analytics tracking
    if "page_views" not in st.session_state:
        st.session_state["page_views"] = 0
    
    st.session_state["page_views"] += 1


if __name__ == "__main__":
    main()


# import streamlit as st
# from src.ui.layout import render_main_layout


# def main():
#     """
#     Main application entry point with enhanced configuration
#     """
    
#     # Enhanced Page Configuration
#     st.set_page_config(
#         page_title="EDA Assistant - AI Powered Data Analysis",
#         page_icon="🧠",
#         layout="wide",
#         initial_sidebar_state="collapsed",
#         menu_items={
#             'Get Help': 'https://github.com/yourusername/eda-assistant',
#             'Report a bug': 'https://github.com/yourusername/eda-assistant/issues',
#             'About': '''
#             # EDA Assistant 🧠
            
#             **Version:** 2.0.0
            
#             An AI-powered Exploratory Data Analysis tool that helps you:
#             - 📊 Profile your datasets instantly
#             - 🧹 Clean and fix data issues
#             - 💬 Chat with AI for insights
#             - 📄 Generate professional reports
            
#             Built with ❤️ using Streamlit and LangChain
#             '''
#         }
#     )
    
#     # Initialize session state variables
#     initialize_session_state()
    
#     # Render the main layout
#     render_main_layout()


# def initialize_session_state():
#     """
#     Initialize all required session state variables
#     """
    
#     # Dataset storage
#     if "raw_dataset" not in st.session_state:
#         st.session_state["raw_dataset"] = None
    
#     if "cleaned_dataset" not in st.session_state:
#         st.session_state["cleaned_dataset"] = None
    
#     # Profiling results
#     if "profile_result" not in st.session_state:
#         st.session_state["profile_result"] = None
    
#     # Chat history for AI agent
#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []
    
#     # User preferences
#     if "theme" not in st.session_state:
#         st.session_state["theme"] = "gradient"
    
#     # Analytics tracking
#     if "page_views" not in st.session_state:
#         st.session_state["page_views"] = 0
    
#     st.session_state["page_views"] += 1


# if __name__ == "__main__":
#     main()