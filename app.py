import streamlit as st
from security import security_assessment
from hallucination import truthfulness_check
from robustness import robustness_assessment
from mcp_test import mcp_context_test
from webhook_utils import send_notification
from pdf_report import generate_report
from utils import show_help

st.set_page_config(page_title="AI Security Dashboard", layout="wide")
st.title("🔐 AI Infosec & Hallucination Dashboard")

# Sidebar Configuration
st.sidebar.header("Configuration & Preferences")
use_fact_check_api = st.sidebar.checkbox("Enable External Fact-Checking API", value=False)
use_webhooks = st.sidebar.checkbox("Enable Slack/Jira Notifications", value=False)
use_mcp_context = st.sidebar.checkbox("Enable Knowledge Base Grounding (MCP)", value=False)

# Built-in Help
if st.sidebar.button("Show Help & Workflow"):
    show_help()

ai_endpoint = st.text_input("Enter AI Model Endpoint URL:", placeholder="https://your-ai-api.com/predict")

if st.button("Start Assessment"):
    if ai_endpoint:
        with st.spinner("Running Security Assessment..."):
            sec_results = security_assessment(ai_endpoint)
        st.success("✅ Security tests complete.")

        with st.spinner("Checking Truthfulness & Hallucinations..."):
            hall_results = truthfulness_check(ai_endpoint, use_api=use_fact_check_api)
        st.success("✅ Hallucination tests complete.")

        with st.spinner("Running Robustness Tests..."):
            robust_results = robustness_assessment(ai_endpoint)
        st.success("✅ Robustness tests complete.")

        if use_mcp_context:
            with st.spinner("Running MCP Contextual Test..."):
                mcp_results = mcp_context_test(ai_endpoint)
            st.success("✅ MCP Context Test complete.")
        else:
            mcp_results = {"context_result": "Skipped (MCP disabled)."}

        # Optional Webhook Notification
        summary_msg = (
            f"AI Infosec Dashboard Results\n"
            f"Security: {sec_results['risk_level']}\n"
            f"Truthfulness: {hall_results['score']}\n"
            f"Robustness: {robust_results['status']}\n"
            f"MCP Context: {mcp_results['context_result']}"
        )
        send_notification(summary_msg, use_webhook=use_webhooks)

        st.subheader("📌 Summary of Findings")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Security Risk", sec_results["risk_level"])
            st.write(sec_results["summary"])
        with col2:
            st.metric("Truthfulness", hall_results["score"])
            st.write(hall_results["remarks"])
        with col3:
            st.metric("Robustness", robust_results["status"])
            st.write(robust_results["remarks"])
        with col4:
            st.metric("MCP Context", mcp_results["context_result"])
            st.write(mcp_results.get("details", ""))

        pdf_bytes = generate_report(sec_results, hall_results, robust_results, mcp_results)
        st.download_button("Download Comprehensive Report (PDF)", data=pdf_bytes,
                           file_name="AI_Infosec_Report.pdf", mime="application/pdf")
    else:
        st.error("Please provide a valid AI Endpoint URL.")
