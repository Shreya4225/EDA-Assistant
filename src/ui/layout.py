import streamlit as st
import re
from src.tools.utils import load_dataset
from src.pipeline.profiler import profile_dataset
from src.agents.response_generator import handle_user_query


def markdown_to_html(text):
    """Convert basic Markdown formatting to HTML"""
    # Bold: **text** or __text__ -> <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    
    # Italic: *text* or _text_ -> <em>text</em>
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Code: `text` -> <code>text</code>
    text = re.sub(r'`(.*?)`', r'<code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace;">\1</code>', text)
    
    # Line breaks
    text = text.replace('\n', '<br>')
    
    return text


def inject_custom_css():
    """Inject custom CSS for stunning UI"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Content Background */
    .block-container {
        background: white;
        border-radius: 20px;
        padding: 2rem 3rem;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Custom Title */
    .custom-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .custom-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 8px;
        border-radius: 12px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        font-size: 0.95rem;
        border: none;
        padding: 0 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Card Styling */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
        display: inline-block;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File Uploader */
    .uploadedFile {
        border-radius: 12px;
        border: 2px dashed #667eea;
        background: #f8fafc;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: #764ba2;
        background: #f1f5f9;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    
    /* Chat Message Styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 12px 0;
        margin-left: 20%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease;
    }
    
    .assistant-message {
        background: #f8fafc;
        color: #1e293b;
        padding: 16px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 12px 0;
        margin-right: 20%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 12px;
        padding: 16px;
        font-weight: 500;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.6);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)


def render_main_layout():
    """
    Main UI layout with stunning design and 4 tabs:
    1️⃣ Upload file + profiling
    2️⃣ Cleaning and fixes
    3️⃣ Chat with EDA agent
    4️⃣ Export report
    """
    
    # Inject custom CSS
    inject_custom_css()
    
    # Custom Title
    st.markdown('<h1 class="custom-title">🧠 EDA Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="custom-subtitle">Your AI-Powered Data Analysis Companion</p>', unsafe_allow_html=True)

    tabs = st.tabs([
        "📁 Upload & Profiling",
        "🧹 Cleaning & Fixes",
        "💬 Chat with AI",
        "📄 Export Report"
    ])

    # ==================== TAB 1: Upload & Profiling ====================
    with tabs[0]:
        st.markdown('<div class="section-header">📁 Step 1: Upload & Profile Your Dataset</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            uploaded_file = st.file_uploader(
                "Drop your CSV or Excel file here",
                type=["csv", "xlsx", "xls"],
                help="Upload your dataset to begin analysis"
            )

        if uploaded_file is not None:
            try:
                with st.spinner("🔄 Loading your dataset..."):
                    df = load_dataset(uploaded_file)
                    st.session_state["raw_dataset"] = df

                st.success("✨ File Uploaded Successfully!")
                
                # Metrics Row
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📊 Total Rows</div>
                        <div class="metric-value">{df.shape[0]:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📋 Columns</div>
                        <div class="metric-value">{df.shape[1]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">⚠️ Missing %</div>
                        <div class="metric-value">{missing_pct:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">💾 Memory</div>
                        <div class="metric-value">{memory_mb:.1f}MB</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br><br>", unsafe_allow_html=True)

                # Data Preview with custom styling
                st.markdown('<div class="section-header">🔍 Data Preview</div>', unsafe_allow_html=True)
                st.dataframe(df.head(10), use_container_width=True, height=400)

                # Run profiling
                with st.spinner("🔬 Analyzing your data..."):
                    profile = profile_dataset(df)
                    st.session_state["profile_result"] = profile

                st.markdown("<br>", unsafe_allow_html=True)

                # Profiling Results in Expandable Sections
                with st.expander("📊 Column Types Analysis", expanded=True):
                    st.dataframe(profile["column_types"], use_container_width=True)

                with st.expander("⚠️ Missing Values Report", expanded=True):
                    missing_df = profile["missing_values"]
                    if missing_df["Missing Count"].sum() > 0:
                        st.warning(f"Found {missing_df['Missing Count'].sum():,} missing values across {(missing_df['Missing Count'] > 0).sum()} columns")
                        st.dataframe(missing_df, use_container_width=True)
                    else:
                        st.success("🎉 No missing values detected!")

                with st.expander("📈 Statistical Summary", expanded=True):
                    if not profile["stats"].empty:
                        st.dataframe(profile["stats"], use_container_width=True)
                    else:
                        st.info("ℹ️ No numeric columns found for statistical analysis.")

            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        else:
            # Empty State
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 16px; margin-top: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">📂</div>
                <h3 style="color: #64748b; font-weight: 600;">No File Uploaded Yet</h3>
                <p style="color: #94a3b8; font-size: 1.1rem;">Upload a CSV or Excel file to start your analysis journey</p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== TAB 2: Cleaning & Fixes ====================
    with tabs[1]:
        st.markdown('<div class="section-header">🧹 Step 2: Clean & Fix Your Data</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if "raw_dataset" not in st.session_state:
            st.warning("⚠️ Please upload a dataset first (Tab 1)")
            st.stop()

        df = st.session_state["raw_dataset"]
        profile = st.session_state.get("profile_result")

        if profile is None:
            st.error("Profile data not found. Please reload the dataset in Tab 1.")
            st.stop()

        missing_df = profile["missing_values"]
        missing_cols = missing_df[missing_df["Missing Count"] > 0].index.tolist()

        if not missing_cols:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                 border-radius: 16px; color: white; margin-top: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">✅</div>
                <h2 style="font-weight: 700;">Perfect! No Missing Data Found</h2>
                <p style="font-size: 1.1rem; opacity: 0.9;">Your dataset is clean and ready for analysis</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Store as cleaned even if no cleaning needed
            if "cleaned_dataset" not in st.session_state:
                st.session_state["cleaned_dataset"] = df
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("💡 Move to the next tab to chat with the AI agent!")
            st.stop()

        # Missing Data Visualization
        st.markdown('<div class="section-header">⚠️ Missing Data Overview</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(missing_df.loc[missing_cols], use_container_width=True)
        
        with col2:
            total_missing = missing_df.loc[missing_cols, "Missing Count"].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🔍 Total Missing</div>
                <div class="metric-value">{total_missing:,}</div>
                <div style="margin-top: 8px; font-size: 0.85rem;">Across {len(missing_cols)} columns</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Imputation Strategy Selection
        from src.pipeline.cleaner import suggest_imputation, apply_imputation
        suggestions = suggest_imputation(df)

        st.markdown('<div class="section-header">🧠 AI-Suggested Fixes</div>', unsafe_allow_html=True)
        st.info("💡 Our AI recommends the best imputation method for each column. You can customize below.")
        
        st.markdown("<br>", unsafe_allow_html=True)

        user_strategies = {}
        
        # Create a nice grid for strategy selection
        cols_per_row = 2
        for i in range(0, len(missing_cols), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(missing_cols):
                    col_name = missing_cols[i + j]
                    default = suggestions[col_name]
                    
                    with col:
                        with st.container():
                            st.markdown(f"**🔹 {col_name}**")
                            user_strategies[col_name] = st.selectbox(
                                f"Strategy for {col_name}",
                                ["Median", "Mean", "Most Frequent", "Drop"],
                                index=["Median", "Mean", "Most Frequent", "Drop"].index(default),
                                key=f"strategy_{col_name}",
                                label_visibility="collapsed"
                            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Apply Fixes Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Apply Cleaning Strategy", use_container_width=True):
                with st.spinner("🔄 Cleaning your data..."):
                    cleaned_df = apply_imputation(df, user_strategies)
                    st.session_state["cleaned_dataset"] = cleaned_df

                st.success("✨ Data cleaned successfully!")
                # st.balloons()

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">✅ Cleaned Data Preview</div>', unsafe_allow_html=True)
                st.dataframe(cleaned_df.head(10), use_container_width=True, height=400)

                # Download cleaned data
                st.markdown("<br>", unsafe_allow_html=True)
                csv_data = cleaned_df.to_csv(index=False).encode("utf-8")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="⬇️ Download Cleaned Dataset",
                        data=csv_data,
                        file_name="cleaned_dataset.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

    # ==================== TAB 3: Chat with EDA Agent ====================
    with tabs[2]:
        st.markdown('<div class="section-header">💬 Step 3: Chat with AI Agent</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        df = st.session_state.get("cleaned_dataset")
        if df is None:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: #fff3cd; border-radius: 16px; 
                 border: 2px solid #ffc107; margin-top: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">⚠️</div>
                <h3 style="color: #856404;">Complete Previous Steps First</h3>
                <p style="color: #856404; font-size: 1.1rem;">Please upload and clean your dataset before chatting with the AI</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Chat Interface
        st.markdown("""
        <div style="background: #f8fafc; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h4 style="margin: 0; color: #1e293b;">🤖 AI Data Assistant</h4>
            <p style="margin: 8px 0 0 0; color: #64748b;">Ask anything about your dataset - trends, correlations, visualizations, or insights!</p>
        </div>
        """, unsafe_allow_html=True)

        # Chat Input
        col1, col2 = st.columns([6, 1])
        with col1:
            user_msg = st.text_input(
                "Type your question here...",
                key="chat_input",
                placeholder="e.g., Show me the correlation between columns...",
                label_visibility="collapsed"
            )
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)

        if send_button and user_msg.strip():
            # Add user message
            st.session_state["chat_history"].append(
                {"role": "user", "message": user_msg}
            )

            # Get AI response
            with st.spinner("🤔 AI is thinking..."):
                response_text, chart_path = handle_user_query(user_msg)

            # Add assistant response
            st.session_state["chat_history"].append(
                {"role": "assistant", "message": response_text}
            )

            # Add chart if available
            if chart_path:
                st.session_state["chat_history"].append(
                    {"role": "chart", "message": chart_path}
                )

            st.rerun()

        # Display Chat History
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state["chat_history"]:
            chat_container = st.container()
            with chat_container:
                for chat in st.session_state["chat_history"]:
                    if chat["role"] == "user":
                        # Escape HTML in user messages for security
                        user_text = chat['message'].replace('<', '&lt;').replace('>', '&gt;')
                        st.markdown(f"""
                        <div class="user-message">
                            <strong>🧑‍💻 You:</strong><br>
                            {user_text}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif chat["role"] == "assistant":
                        # Convert Markdown to HTML for assistant messages
                        assistant_text = markdown_to_html(chat['message'])
                        st.markdown(f"""
                        <div class="assistant-message">
                            <strong>🤖 AI Assistant:</strong><br>
                            {assistant_text}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elif chat["role"] == "chart":
                        col1, col2, col3 = st.columns([1, 3, 1])
                        with col2:
                            st.image(chat["message"], use_container_width=True)

            # Clear Chat Button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🧹 Clear Chat History", use_container_width=True):
                    st.session_state["chat_history"] = []
                    st.rerun()
        else:
            # Empty state for chat
            st.markdown("""
            <div style="text-align: center; padding: 80px 20px; background: #f8fafc; border-radius: 16px; margin-top: 20px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">💭</div>
                <h3 style="color: #64748b;">Start a Conversation</h3>
                <p style="color: #94a3b8; font-size: 1.1rem;">Ask questions about your data and get instant insights</p>
                <div style="margin-top: 30px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">
                    <p style="color: #64748b;"><strong>💡 Try asking:</strong></p>
                    <ul style="color: #94a3b8; line-height: 2;">
                        <li>"Show me a correlation heatmap"</li>
                        <li>"What are the top 5 insights from this data?"</li>
                        <li>"Plot the distribution of [column name]"</li>
                        <li>"Find outliers in the dataset"</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ==================== TAB 4: Export Report ====================
    with tabs[3]:
        st.markdown('<div class="section-header">📄 Step 4: Export Professional Report</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if "cleaned_dataset" not in st.session_state:
            st.warning("⚠️ Please complete previous steps first!")
            st.stop()

        from src.agents.llm_client import get_llm
        from src.pipeline.pdf_report import generate_pdf_report

        df = st.session_state["cleaned_dataset"]
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; 
             border-radius: 16px; color: white; text-align: center; margin-bottom: 30px;">
            <h2 style="margin: 0 0 16px 0;">📊 Generate EDA Report</h2>
            <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                Get a comprehensive PDF report with AI-generated insights and statistics
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Report Preview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Report Will Include:")
            st.markdown("""
            - ✅ Dataset Overview & Statistics
            - ✅ Column Type Analysis
            - ✅ Missing Value Report
            - ✅ AI-Generated Insights
            - ✅ Data Quality Assessment
            """)
        
        with col2:
            st.markdown("### 📈 Quick Stats:")
            st.metric("Total Records", f"{df.shape[0]:,}")
            st.metric("Total Features", f"{df.shape[1]}")
            st.metric("Data Quality", f"{((1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100):.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # Generate Report Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎨 Generate PDF Report", use_container_width=True):
                with st.spinner("🔄 Creating your professional report..."):
                    llm = get_llm()

                    prompt = (
                        "Provide 4-6 key insights about this dataset:\n"
                        f"Columns: {list(df.columns)}\n"
                        f"Missing Values: {df.isnull().sum().to_dict()}\n"
                        f"Statistics: {df.describe().to_string()}"
                    )
                    
                    insights = llm.invoke(prompt).content
                    pdf_path = generate_pdf_report(df, insights)

                st.success("✨ Report generated successfully!")
                # st.balloons()

                st.markdown("<br>", unsafe_allow_html=True)

                with open(pdf_path, "rb") as f:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=f,
                            file_name="EDA_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

