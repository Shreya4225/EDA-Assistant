# src/ui/layout.py

import streamlit as st
from src.tools.utils import load_dataset
from src.pipeline.profiler import profile_dataset
from src.agents.nlp_intent_parser import parse_chart_request
from src.tools.chart_generator import generate_chart


def render_main_layout():
    """
    Renders the main tabbed layout for the EDA Assistant.
    Currently each tab only shows placeholder content.
    Logic will be added step by step.
    """
    st.title("🧠 EDA Assistant")

    tabs = st.tabs([
        "1. Upload & Profiling",
        "2. Cleaning & Fixes",
        "3. Chat with EDA Agent",
        "4. Export Report"
    ])

    # Tab 1: Upload & Profiling (placeholder for now)
    

# inside render_main_layout(), Tab 1 content

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

                st.success("File uploaded and loaded successfully!")

                st.write("### 🔍 Data Preview")
                st.dataframe(df.head())
                st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

                # ➤ Run Profiling
                profile_result = profile_dataset(df)
                st.session_state["profile_result"] = profile_result

                st.write("## 📌 Basic Profiling Results")

                st.write("### 🧩 Column Types")
                st.dataframe(profile_result["column_types"])

                st.write("### ⚠️ Missing Values")
                st.dataframe(profile_result["missing_values"])

                st.write("### 📊 Statistics (for numeric columns)")
                if not profile_result["stats"].empty:
                    st.dataframe(profile_result["stats"])
                else:
                    st.info("No numeric columns found.")

            except Exception as e:
                st.error(f"Error loading file: {e}")

        else:
            st.info("Please upload a file to proceed.")



    # Tab 2: Cleaning & Fixes (placeholder)
    # Tab 2: Data Cleaning & Fixes

    with tabs[1]:
        st.subheader("Step 2: Review suggested fixes & clean data")

        if "raw_dataset" not in st.session_state:
            st.warning("⚠️ No dataset found. Please upload data in Tab 1.")
            st.stop()

        df = st.session_state["raw_dataset"]
        profile = st.session_state.get("profile_result")

        missing_df = profile["missing_values"]
        missing_cols = missing_df[missing_df["Missing Count"] > 0].index.tolist()

        if not missing_cols:
            st.success("🎉 No missing data detected. You can move to the next step!")
            st.stop()

        st.write("### ⚠️ Missing Value Columns")
        st.dataframe(missing_df.loc[missing_cols])

        # Suggested strategies
        from src.pipeline.cleaner import suggest_imputation, apply_imputation

        suggestions = suggest_imputation(df)

        st.write("### 🧠 Suggested Imputation Methods")

        user_strategies = {}

        for col, default_method in suggestions.items():
            user_strategies[col] = st.selectbox(
                f"Column: {col}",
                ["Median", "Mean", "Most Frequent", "Drop"],
                index=["Median", "Mean", "Most Frequent", "Drop"].index(default_method)
            )

        if st.button("Apply Fixes"):
            cleaned_df = apply_imputation(df, user_strategies)
            st.session_state["cleaned_dataset"] = cleaned_df
            st.success("Data cleaned successfully! Proceed to Step 3.")
            st.write("### Cleaned Data Preview")
            st.dataframe(cleaned_df.head())

            # Convert cleaned dataframe to CSV for download
            csv_data = cleaned_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="⬇️ Download Cleaned Dataset",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )
        # After cleaned data preview

        


    # Tab 3: Chat with EDA Agent (placeholder)
        # Tab 3: Chat with EDA Agent

    from src.agents.llm_client import get_llm

    with tabs[2]:
        st.subheader("Step 3: Chat with the EDA Agent")

        if "cleaned_dataset" not in st.session_state:
            st.warning("⚠️ No cleaned dataset found. Please complete Step 2.")
            st.stop()

        df = st.session_state["cleaned_dataset"]

        from src.agents.nlp_intent_parser import detect_intent, parse_chart_request
        from src.tools.chart_generator import generate_chart

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []  # Initialize history

        # Clear chat input function (callback)
        def reset_input():
            st.session_state["chat_input"] = ""

        # Display chat history (text + images)
        for chat in st.session_state["chat_history"]:
            if chat["role"] == "user":
                st.markdown(f"**You:** {chat['message']}")
            elif chat["role"] == "assistant":
                st.markdown(f"**Assistant:** {chat['message']}")
            elif chat["role"] == "chart":
                st.image(chat["message"])

        # User input box with callback
        # Input box uses a temporary key
        user_msg = st.text_input("Ask something about your dataset:")

        if st.button("Send") and user_msg.strip():
            st.session_state["chat_history"].append({"role": "user", "message": user_msg})

            intent = detect_intent(user_msg)

            if intent == "describe":
                response = f"This dataset has **{df.shape[0]} rows** and **{df.shape[1]} columns**."

            elif intent == "columns":
                response = "Here are the columns:\n\n" + "\n".join([f"- {col}" for col in df.columns])

            elif intent == "missing":
                response = "Missing values:\n\n" + df.isnull().sum().to_string()

            elif intent == "stats":
                response = "Basic statistics:\n\n" + df.describe().transpose().to_string()

            elif intent == "chart":
                detected_cols, chart_type = parse_chart_request(user_msg, list(df.columns))

                if len(detected_cols) == 0:
                    response = "Please mention a valid column name for visualization."

                elif len(detected_cols) == 1:
                    img_path = generate_chart(df, detected_cols[0], chart_type=chart_type)
                    st.session_state["chat_history"].append({"role": "assistant", "message": f"📊 {chart_type.title()} Chart: **{detected_cols[0]}**"})
                    st.session_state["chat_history"].append({"role": "chart", "message": img_path})
                    st.rerun()

                else:
                    img_path = generate_chart(df, detected_cols[0], detected_cols[1], chart_type="scatter")
                    st.session_state["chat_history"].append({"role": "assistant", "message": f"📊 Scatter Plot: **{detected_cols[0]} vs {detected_cols[1]}**"})
                    st.session_state["chat_history"].append({"role": "chart", "message": img_path})
                    st.rerun()

            else:
                llm = get_llm()

                system_prompt = (
                    "You are an intelligent EDA assistant. Only respond based on the dataset context. "
                    "Be brief and helpful. No code."
                )

                dataset_info = (
                    f"Columns: {list(df.columns)}\n"
                    f"Rows: {df.shape[0]}\n"
                )

                conversation = ""
                for chat in st.session_state["chat_history"][-4:]:
                    conversation += f"{chat['role']}: {chat['message']}\n"

                prompt = (
                    f"{system_prompt}\n"
                    f"Dataset Info:\n{dataset_info}\n"
                    f"Recent Chat:\n{conversation}\n"
                    f"User Query: {user_msg}"
                )

                response = llm.invoke(prompt).content

            st.session_state["chat_history"].append({"role": "assistant", "message": response})
            st.rerun()




    # from src.agents.llm_client import get_llm

    # with tabs[2]:
    #     st.subheader("Step 3: Chat with the EDA Agent")

    #     if "cleaned_dataset" not in st.session_state:
    #         st.warning("⚠️ No cleaned dataset found. Please complete Step 2.")
    #         st.stop()

    #     df = st.session_state["cleaned_dataset"]

    #     from src.agents.nlp_intent_parser import detect_intent, parse_chart_request
    #     from src.tools.chart_generator import generate_chart

    #     if "chat_history" not in st.session_state:
    #         st.session_state["chat_history"] = []  # Initialize history

    #     # Display chat history (text + images)
    #     for chat in st.session_state["chat_history"]:
    #         if chat["role"] == "user":
    #             st.markdown(f"**You:** {chat['message']}")
    #         elif chat["role"] == "assistant":
    #             st.markdown(f"**Assistant:** {chat['message']}")
    #         elif chat["role"] == "chart":
    #             st.image(chat["message"])

    #     # User input box
    #     # user_input = st.text_input("Ask something about your dataset:")
    #     user_input = st.text_input(
    #         "Ask something about your dataset:",
    #         key="chat_input"
    #     )


    #     if st.button("Send") and user_input.strip():
    #         st.session_state["chat_history"].append({"role": "user", "message": user_input})

    #         intent = detect_intent(user_input)

    #         # ---- Intent handling ----
    #         if intent == "describe":
    #             response = f"This dataset has **{df.shape[0]} rows** and **{df.shape[1]} columns**."

    #         elif intent == "columns":
    #             response = "Here are the columns:\n\n" + "\n".join([f"- {col}" for col in df.columns])

    #         elif intent == "missing":
    #             response = "Missing values:\n\n" + df.isnull().sum().to_string()

    #         elif intent == "stats":
    #             response = "Basic statistics:\n\n" + df.describe().transpose().to_string()

    #         elif intent == "chart":
    #             detected_cols, chart_type = parse_chart_request(user_input, list(df.columns))

    #             if len(detected_cols) == 0:
    #                 response = "Please mention a valid column name for visualization."

    #             elif len(detected_cols) == 1:
    #                 img_path = generate_chart(df, detected_cols[0], chart_type=chart_type)
    #                 st.session_state["chat_history"].append(
    #                     {"role": "assistant", "message": f"📊 {chart_type.title()} Chart for **{detected_cols[0]}**"}
    #                 )
    #                 st.session_state["chat_history"].append(
    #                     {"role": "chart", "message": img_path}
    #                 )
    #                 response = None

    #             else:  # 2+ columns → scatter
    #                 img_path = generate_chart(df, detected_cols[0], detected_cols[1], chart_type="scatter")
    #                 st.session_state["chat_history"].append(
    #                     {"role": "assistant", "message": f"📊 Scatter Plot: **{detected_cols[0]} vs {detected_cols[1]}**"}
    #                 )
    #                 st.session_state["chat_history"].append(
    #                     {"role": "chart", "message": img_path}
    #                 )
    #                 response = None

    #         else:
    #             # LLM fallback - intelligent dataset-aware insights
    #             llm = get_llm()

    #             system_prompt = (
    #                 "You are an intelligent EDA assistant. "
    #                 "You help users analyze their dataset through natural conversation. "
    #                 "Keep responses short and focused on the provided dataset."
    #             )

    #             dataset_info = (
    #                 f"Dataset Columns: {list(df.columns)}\n"
    #                 f"Number of rows: {df.shape[0]}\n"
    #             )

    #             chat_context = ""
    #             for chat in st.session_state["chat_history"][-4:]:  # recent context only
    #                 chat_context += f"{chat['role']}: {chat['message']}\n"

    #             final_prompt = (
    #                 f"{system_prompt}\n"
    #                 f"Dataset Info:\n{dataset_info}\n"
    #                 f"Conversation so far:\n{chat_context}\n"
    #                 f"User Query:\n{user_input}"
    #             )

    #             llm_response = llm.invoke(final_prompt)
    #             response = llm_response.content


    #         # Only add text response if present
    #         if response:
    #             st.session_state["chat_history"].append({"role": "assistant", "message": response})

    #         #st.stop()
    #         st.session_state["chat_input"] = ""  # Clear text box
    #         st.experimental_rerun()  # Or st.rerun()






    # Tab 4: Export Report (placeholder)
    # with tabs[3]:
    #     st.subheader("Step 4: Export cleaned data & PDF report")
    #     st.info("Export options will be implemented here soon.")
    #     from src.pipeline.report_builder import generate_report_charts

    #     if "cleaned_dataset" in st.session_state:
    #         if st.button("Generate Test Charts"):
    #             paths, captions = generate_report_charts(st.session_state["cleaned_dataset"])
    #             st.write("Generated charts:")
    #             st.write(paths)
    #             st.write(captions)
    #     else:
    #         st.info("Upload & clean dataset first.")

    with tabs[3]:
        # Tab 4: Export Report
        st.subheader("Step 4: Export cleaned data & PDF report")

        if "cleaned_dataset" not in st.session_state:
            st.warning("⚠️ No cleaned dataset found. Complete Step 2 first.")
            st.stop()

        df = st.session_state["cleaned_dataset"]

        from src.agents.llm_client import get_llm
        from src.pipeline.pdf_report import generate_pdf_report

        st.write("Click the button to generate your EDA report PDF:")

        if st.button("Generate & Download Report"):
    
            llm = get_llm()

            # Prepare dataset context for AI
            dataset_details = f"""
            Columns: {list(df.columns)}
            Rows: {df.shape[0]}
            Describe Stats:
            {df.describe().to_string()}
            Missing Values:
            {df.isnull().sum().to_string()}
            """

            ai_insight_prompt = f"""
            You are an EDA expert. Create 4-6 short bullet-point insights 
            based ONLY on the dataset below:

            {dataset_details}

            Be concise, analytical, and insightful.
            Do not mention that the dataset was given or describe the process.
            No introductions or disclaimers.
            """

            ai_response = llm.invoke(ai_insight_prompt).content

            # Generate PDF using AI insights
            pdf_path = generate_pdf_report(df, ai_response)

            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=file,
                    file_name="EDA_Report.pdf",
                    mime="application/pdf"
                )

            st.success("Report successfully generated! Download above.")


        # if st.button("Generate & Download Report"):
        #     llm = get_llm()
        #     ai_insight_prompt = (
        #         "Provide 4-6 short bullet point insights about this dataset "
        #         "based only on the features and summary statistics."
        #     )
        #     ai_response = llm.invoke(ai_insight_prompt).content

        #     pdf_path = generate_pdf_report(df, ai_response)

        #     with open(pdf_path, "rb") as file:
        #         st.download_button(
        #             label="📥 Download PDF Report",
        #             data=file,
        #             file_name="EDA_Report.pdf",
        #             mime="application/pdf"
        #         )

        #     st.success("Report successfully generated! Download above.")



