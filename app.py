import streamlit as st
from security import security_assessment
from hallucination import truthfulness_check
from robustness import robustness_assessment
from pdf_report import generate_report
from utils import show_help

st.set_page_config(page_title="AI Security Dashboard", layout="wide")
st.title("🔐 AI Infosec & Hallucination Dashboard")

# Sidebar Help Section
if st.sidebar.button("Show Help & Workflow"):
    show_help()

ai_endpoint = st.text_input("Enter AI Model Endpoint URL:", placeholder="https://your-ai-api.com/predict")

if st.button("Start Assessment"):
    if ai_endpoint:
        with st.spinner("Running Security Assessment..."):
            sec_results = security_assessment(ai_endpoint)
        st.success("✅ Security tests complete.")

        with st.spinner("Checking Truthfulness & Hallucinations..."):
            hall_results = truthfulness_check(ai_endpoint)
        st.success("✅ Hallucination tests complete.")

        with st.spinner("Running Robustness Tests..."):
            robust_results = robustness_assessment(ai_endpoint)
        st.success("✅ Robustness tests complete.")

        st.subheader("📌 Summary of Findings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Security Risk", sec_results["risk_level"])
            st.write(sec_results["summary"])

        with col2:
            st.metric("Truthfulness", hall_results["score"])
            st.write(hall_results["remarks"])

        with col3:
            st.metric("Robustness", robust_results["status"])
            st.write(robust_results["remarks"])

        pdf_bytes = generate_report(sec_results, hall_results, robust_results)
        st.download_button("Download Comprehensive Report (PDF)", data=pdf_bytes,
                           file_name="AI_Infosec_Report.pdf", mime="application/pdf")
    else:
        st.error("Please provide a valid AI Endpoint URL.")
