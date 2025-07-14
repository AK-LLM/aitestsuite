import streamlit as st
from security import security_assessment
from hallucination import truthfulness_check
from robustness import robustness_assessment
from bias_toxicity import bias_test
from session_utils import save_session, load_session
from pdf_report import generate_report
from utils import show_help

st.set_page_config(page_title="AI Security Dashboard", layout="wide")
st.title("🔐 AI Infosec & Hallucination Dashboard")

if st.sidebar.button("Show Help & Workflow"):
    show_help()

ai_endpoint = st.text_input("Enter AI Model Endpoint URL:", placeholder="https://your-ai-api.com/predict")

use_fact_check_api = st.sidebar.checkbox("Enable Fact-Checking API", value=False)
use_bias_toxicity = st.sidebar.checkbox("Enable Bias/Toxicity Test", value=True)

if st.button("Start Assessment"):
    findings = {}
    if ai_endpoint:
        sec = security_assessment(ai_endpoint)
        hall = truthfulness_check(ai_endpoint, use_api=use_fact_check_api)
        robust = robustness_assessment(ai_endpoint)
        bias = bias_test(ai_endpoint) if use_bias_toxicity else {"status": "Skipped", "remarks": ""}
        findings.update({"sec": sec, "hall": hall, "robust": robust, "bias": bias})
        exec_summary = f"Security: {sec['risk_level']}; Truthfulness: {hall['score']}; Robustness: {robust['status']}; Bias: {bias['status']}"
        evidence = hall.get("evidence", "")
        st.subheader("📌 Summary of Findings")
        st.write(f"**Security:** {sec['summary']}")
        st.write(f"**Truthfulness:** {hall['remarks']}")
        st.write(f"**Robustness:** {robust['remarks']}")
        st.write(f"**Bias/Toxicity:** {bias['remarks']}")
        # Save/load session
        if st.button("Save Session"):
            save_session(findings)
            st.success("Session saved!")
        if st.button("Load Previous Session"):
            loaded = load_session()
            st.write("Loaded Findings:", loaded)
        # PDF
        pdf_bytes = generate_report(sec, hall, robust, bias, exec_summary, evidence)
        st.download_button("Download Comprehensive Report (PDF)", data=pdf_bytes,
                           file_name="AI_Infosec_Report.pdf", mime="application/pdf")
    else:
        st.error("Please provide a valid AI Endpoint URL.")
