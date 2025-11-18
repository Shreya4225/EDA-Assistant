# src/ui/layout.py

import streamlit as st
from src.tools.utils import load_dataset
from src.pipeline.profiler import profile_dataset
from src.agents.response_generator import handle_user_query


def render_main_layout():
    """
    Main UI layout with 4 tabs:
    1️⃣ Upload file + profiling
    2️⃣ Cleaning and fixes
    3️⃣ Chat with EDA agent
    4️⃣ Export report
    """
    st.title("🧠 EDA Assistant")

    tabs = st.tabs([
        "1. Upload & Profiling",
        "2. Cleaning & Fixes",
        "3. Chat with EDA Agent",
        "4. Export Report"
    ])

    # TAB 1 — Upload & Profiling
    with tabs[0]:
        st.subheader("Step 1: Upload your dataset & run profiling")

        uploaded_file = st.file_uploader(
            "Upload a CSV or Excel file",
            type=["csv", "xlsx", "xls"]
        )

        if uploaded_file is not None:
            try:
                df = load_dataset(uploaded_file)
                st.session_state["raw_dataset"] = df

                st.success("File Uploaded Successfully! 🎉")

                st.write("### 🔍 Data Preview")
                st.dataframe(df.head())
                st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

                # Run profiling
                profile = profile_dataset(df)
                st.session_state["profile_result"] = profile

                st.write("## 📌 Basic Profiling")
                st.write("### 🧩 Column Types")
                st.dataframe(profile["column_types"])

                st.write("### ⚠️ Missing Values")
                st.dataframe(profile["missing_values"])

                st.write("### 📊 Stats for Numeric Columns")
                if not profile["stats"].empty:
                    st.dataframe(profile["stats"])
                else:
                    st.info("No numeric columns found.")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("Upload a file to continue!")

    # TAB 2 — Fix Missing Values
    with tabs[1]:
        st.subheader("Step 2: Fix Missing Values")

        if "raw_dataset" not in st.session_state:
            st.warning("Upload dataset first (Tab 1)")
            st.stop()

        df = st.session_state["raw_dataset"]
        profile = st.session_state.get("profile_result")

        missing_df = profile["missing_values"]
        missing_cols = missing_df[missing_df["Missing Count"] > 0].index.tolist()

        if not missing_cols:
            st.success("🎯 No missing data found! Move to next step.")
            st.stop()

        st.write("### Missing Columns")
        st.dataframe(missing_df.loc[missing_cols])

        from src.pipeline.cleaner import suggest_imputation, apply_imputation
        suggestions = suggest_imputation(df)

        st.write("### 🧠 Suggested Fixes")

        # Local dict to collect strategies for this run
        user_strategies = {}
        for col, default in suggestions.items():
            user_strategies[col] = st.selectbox(
                f"Column: {col}",
                ["Median", "Mean", "Most Frequent", "Drop"],
                index=["Median", "Mean", "Most Frequent", "Drop"].index(default)
            )

        if st.button("Apply Fixes"):
            # Apply imputation using chosen strategies
            cleaned_df = apply_imputation(df, user_strategies)
            st.session_state["cleaned_dataset"] = cleaned_df

            st.success("Data cleaned! Now go to Step 3")

            st.write("### Cleaned Data")
            st.dataframe(cleaned_df.head())

            # 🔽 Download cleaned dataset
            csv_data = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Cleaned Dataset",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    # TAB 3 — Chat with EDA Agent
    with tabs[2]:
        st.subheader("Step 3: Chat with EDA Agent 🤖")

        df = st.session_state.get("cleaned_dataset")
        if df is None:
            st.warning("⚠️ Complete Step 2 first!")
            st.stop()

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        user_msg = st.text_input("Ask about your dataset:", key="chat_input")

        if st.button("Send") and user_msg.strip():
            # User message
            st.session_state["chat_history"].append(
                {"role": "user", "message": user_msg}
            )

            # EDA brain
            response_text, chart_path = handle_user_query(user_msg)

            # Assistant text response
            st.session_state["chat_history"].append(
                {"role": "assistant", "message": response_text}
            )

            # Optional chart
            if chart_path:
                st.session_state["chat_history"].append(
                    {"role": "chart", "message": chart_path}
                )

            st.rerun()

        # Chat history display
        for chat in st.session_state["chat_history"]:
            if chat["role"] == "user":
                st.markdown(f"🧑‍💻 **You:** {chat['message']}")
            elif chat["role"] == "assistant":
                st.markdown(f"🤖 **EDA Agent:** {chat['message']}")
            elif chat["role"] == "chart":
                st.image(chat["message"], caption="📈 Chart")

        if st.button("Clear Chat 🧹"):
            st.session_state["chat_history"] = []
            st.rerun()

    # TAB 4 — Export Report
    with tabs[3]:
        st.subheader("Step 4: Export Report")

        if "cleaned_dataset" not in st.session_state:
            st.warning("Upload & clean dataset first!")
            st.stop()

        from src.agents.llm_client import get_llm
        from src.pipeline.pdf_report import generate_pdf_report

        df = st.session_state["cleaned_dataset"]
        st.write("Generate EDA Summary PDF")

        if st.button("Generate PDF Report"):
            llm = get_llm()

            prompt = (
                "Give 4–6 quick insights about the dataset:\n"
                f"Columns: {list(df.columns)}\n"
                f"Missing: {df.isnull().sum().to_dict()}\n"
                f"Stats: {df.describe().to_string()}"
            )
            insights = llm.invoke(prompt).content

            pdf_path = generate_pdf_report(df, insights)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name="EDA_Report.pdf",
                    mime="application/pdf"
                )

            st.success("Report ready!")
