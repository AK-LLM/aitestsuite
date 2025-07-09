import streamlit as st

def show_help():
    st.sidebar.title("🛠️ Workflow Guide")
    st.sidebar.markdown("""
    **Step-by-step Workflow:**
    1. Enter your AI model's API endpoint URL.
    2. Click **"Start Assessment"** to initiate automated tests.
    3. Review preliminary findings for each assessment.
    4. Download detailed PDF report for further analysis.

    **Tool Descriptions:**
    - **Security Test:** Checks for prompt injection.
    - **Truthfulness Test:** Verifies factual accuracy (hallucination detection).
    - **Robustness Test:** Evaluates AI stability with edge-case inputs.

    **Support:**  
    Contact the AI Infosec team for technical assistance or feedback.
    """)
