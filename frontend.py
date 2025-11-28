# frontend.py
import streamlit as st
import requests
import pandas as pd
import base64
from io import BytesIO
from PIL import Image

API_BASE_URL = "http://backend:8000"  

st.set_page_config(
    page_title="Autonomous Data Analyst",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# SESSION STATE INITIALIZATION
# ===========================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None


# ===========================
# DARK MODE CSS
# ===========================
st.markdown("""
<style>
:root {
    --bg: #0e1117;
    --card: #161a23;
    --text: #e4e6eb;
    --accent: #6366f1; 
}

body, .stApp {
    background-color: var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background-color: var(--card);
    border-right: 1px solid #262b39;
}

h1, h2, h3, h4 {
    color: var(--text);
}

.stButton>button {
    background-color: var(--accent);
    color: white;
    border-radius: 6px;
    border: none;
    padding: 0.6rem 1.2rem;
    transition: 0.2s;
    font-weight: 500;
}
.stButton>button:hover {
    background-color: #4f52d2;
}

[data-testid="stFileUploader"] {
    background-color: var(--card);
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #262b39;
}

textarea, input, select {
    background-color: #1e2230 !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

[data-testid="stDataFrame"] {
    background-color: var(--card);
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================
st.sidebar.title("📊 Data Analyst Dashboard")

mode = st.sidebar.radio(
    "Navigation",
    ["Upload CSV & Analyze", "Ask a Question"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("💡 *Powered by Autonomous Agents & LLMs*")


# ==========================================================
# MODE 1 — UPLOAD CSV & ANALYZE
# ==========================================================
if mode == "Upload CSV & Analyze":

    st.title("📁 Upload CSV for Automated Analysis")

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_df = df

        st.write("### Preview of your data:")
        st.dataframe(df.head())

        if st.button("🚀 Run Analysis"):
            with st.spinner("Analyzing dataset using agents..."):

                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/analyze-csv",
                        files=files,
                        timeout=180
                    )
                    response.raise_for_status()

                    # Save the result permanently
                    st.session_state.analysis_result = response.json()

                    st.success("Analysis Complete ✓")

                except Exception as e:
                    st.error(f"Error: {e}")

    # ==========================================================
    # SHOW PREVIOUS ANALYSIS IF EXISTS
    # ==========================================================
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.subheader("📌 Summary Report")
        st.write(result.get("summary_report", "No summary available"))

        st.subheader("📊 EDA / Analysis Report")
        st.write(result.get("analysis_report", "No analysis available"))

        st.subheader("🧹 Data Quality Report")
        st.write(result.get("data_quality_report", "No quality report available"))

        st.subheader("🚨 Anomaly Report")
        st.write(result.get("anomaly_report", "No anomalies reported"))

        # ============================
        # Visualizations
        # ============================
        if "generated_visualizations" in result:
            visualizations = result["generated_visualizations"]
            if visualizations:
                st.subheader("📊 Visualizations")

                for viz_b64 in visualizations:
                    try:
                        img_bytes = base64.b64decode(viz_b64)
                        img = Image.open(BytesIO(img_bytes))
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Failed to load image: {e}")

        if result.get("dashboard_url"):
            st.subheader("📈 Dashboard")
            st.markdown(f"[Open Dashboard]({result['dashboard_url']})")


# ==========================================================
# MODE 2 — ASK A QUESTION
# ==========================================================

if mode == "Ask a Question":

    st.title("❓ Ask a Question About Your Dataset")

    # -------------------------------
    # Ask-AI Session State (LOCAL)
    # -------------------------------
    if "ask_answer" not in st.session_state:
        st.session_state.ask_answer = None

    dataset_name = st.text_input("Dataset Name (same filename used during upload)")
    question = st.text_area("Your Question")

    if st.button("💬 Get Answer"):
        if not dataset_name or not question:
            st.warning("Please enter both dataset name and question.")
        else:
            with st.spinner("Retrieving answer..."):
                try:
                    params = {"dataset": dataset_name, "query": question}
                    response = requests.get(f"{API_BASE_URL}/ask", params=params)
                    response.raise_for_status()

                    # Save answer permanently
                    st.session_state.ask_answer = response.json().get("answer", "No answer available")

                except Exception as e:
                    st.error(f"Error: {e}")

    # -------------------------------------
    # Show saved answer (PERSIST across tabs)
    # -------------------------------------
    if st.session_state.ask_answer:
        st.subheader("🔍 Answer")
        st.write(st.session_state.ask_answer)