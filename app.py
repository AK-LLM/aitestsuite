import streamlit as st
from security import security_assessment
from hallucination import truthfulness_check
from robustness import robustness_assessment
from bias_toxicity import bias_test
from mcp_test import mcp_context_test
from session_utils import save_session, load_session
from pdf_report import generate_report
from webhook_utils import send_notification
from utils import show_help

st.set_page_config(page_title="AI Security Dashboard", layout="wide")
st.title("🔐 AI Infosec & Hallucination Dashboard")

# Sidebar toggles for every feature and API-dependent call
st.sidebar.header("Configuration & Preferences")
use_security = st.sidebar.checkbox("Enable Security Tests", value=True)
use_hallucination = st.sidebar.checkbox("Enable Hallucination/Fact-Checking", value=True)
use_fact_check_api = st.sidebar.checkbox("  • Use Fact-Checking API (if enabled above)", value=False, help="Enable to verify using external fact-checking sources/API")
use_robustness = st.sidebar.checkbox("Enable Robustness Tests", value=True)
use_bias_toxicity = st.sidebar.checkbox("Enable Bias/Toxicity Test", value=True)
use_mcp_context = st.sidebar.checkbox("Enable MCP/Context Test", value=False)
use_notifications = st.sidebar.checkbox("Enable Webhook Notifications", value=False)
show_evidence = st.sidebar.checkbox("Show Evidence Log in Report", value=True)

# Built-in workflow/help
if st.sidebar.button("Show Help & Workflow"):
    show_help()

# Endpoint entry
ai_endpoint = st.text_input("Enter AI Model Endpoint URL:", placeholder="https://your-ai-api.com/predict")

# Buttons for main and session actions
colA, colB, colC = st.columns([2,1,1])
with colA:
    start_btn = st.button("Start Assessment")
with colB:
    save_btn = st.button("Save Session")
with colC:
    load_btn = st.button("Load Previous Session")

# Handle session load/save logic first
if load_btn:
    loaded = load_session()
    if "error" in loaded:
        st.warning(loaded["error"])
    else:
        st.success("Previous session loaded!")
        st.json(loaded)

elif save_btn:
    findings = st.session_state.get("last_findings", {})
    if not findings:
        st.info("No findings to save yet. Run an assessment first.")
    else:
        save_session(findings)
        st.success("Session saved!")

elif start_btn:
    if not ai_endpoint:
        st.error("Please provide a valid AI Endpoint URL.")
    else:
        findings = {}

        # Run enabled tests
        if use_security:
            sec = security_assessment(ai_endpoint)
        else:
            sec = {"risk_level": "Skipped", "summary": "Security tests not run."}

        if use_hallucination:
            hall = truthfulness_check(ai_endpoint, use_api=use_fact_check_api)
        else:
            hall = {"score": "Skipped", "remarks": "Hallucination tests not run.", "evidence": "", "consistency": "N/A"}

        if use_robustness:
            robust = robustness_assessment(ai_endpoint)
        else:
            robust = {"status": "Skipped", "remarks": "Robustness tests not run."}

        if use_bias_toxicity:
            bias = bias_test(ai_endpoint)
        else:
            bias = {"status": "Skipped", "remarks": "Bias/Toxicity tests not run."}

        if use_mcp_context:
            mcp = mcp_context_test(ai_endpoint)
        else:
            mcp = {"context_result": "Skipped (MCP/Context disabled)", "details": ""}

        findings = {
            "sec": sec, "hall": hall, "robust": robust, "bias": bias, "mcp": mcp
        }
        st.session_state["last_findings"] = findings

        # Optional Webhook Notification
        if use_notifications:
            summary_msg = (
                f"AI Infosec Dashboard Results\n"
                f"Security: {sec.get('risk_level')}\n"
                f"Truthfulness: {hall.get('score')}\n"
                f"Robustness: {robust.get('status')}\n"
                f"Bias/Toxicity: {bias.get('status')}\n"
                f"MCP Context: {mcp.get('context_result')}"
            )
            send_notification(summary_msg, use_webhook=True)

        # Executive summary for report
        exec_summary = (
            f"Security: {sec.get('risk_level')} | "
            f"Truthfulness: {hall.get('score')} | "
            f"Robustness: {robust.get('status')} | "
            f"Bias/Toxicity: {bias.get('status')} | "
            f"MCP: {mcp.get('context_result')}"
        )

        # --- DASHBOARD VISUALS ---
        st.subheader("📌 Summary of Findings")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Security", sec.get('risk_level', 'N/A'))
            for f in sec.get('summary', '').split(';'):
                st.markdown(f"- {f.strip()}")
        with col2:
            st.metric("Truthfulness", hall.get('score', 'N/A'))
            st.markdown(hall.get('remarks', ''))
            st.markdown(f"**Consistency:** {hall.get('consistency', 'N/A')}")
        with col3:
            st.metric("Robustness", robust.get('status', 'N/A'))
            for f in robust.get('remarks', '').split(';'):
                st.markdown(f"- {f.strip()}")
        with col4:
            st.metric("Bias/Toxicity", bias.get('status', 'N/A'))
            for f in bias.get('remarks', '').split(';'):
                st.markdown(f"- {f.strip()}")
        with col5:
            st.metric("MCP Context", mcp.get('context_result', 'N/A'))
            if mcp.get("details"):
                st.markdown(mcp["details"])

        if show_evidence:
            with st.expander("Show Evidence and Details"):
                st.write("**Sample Evidence:**")
                st.write(hall.get("evidence", "No sample available."))

        # NEW: Explanation Panel for User-Friendly Guidance
        with st.expander("ℹ️ What Do These Results Mean?"):
            st.markdown("""
            ### **Result Explanation & Guidance**
            - **Security (Low Risk):**
                - No major injection or prompt manipulation vulnerabilities were detected in this run. 
                - Your AI endpoint did **not leak secrets or follow risky override prompts**—a very positive sign for basic LLM security.
            - **Truthfulness (50%):**
                - Only half of the checked answers matched known facts or passed external validation.
                - **What this means:** Your model may provide incomplete, misleading, or incorrect information and should not be relied on for critical decisions **without further improvement**.
                - **Tip:** Enhance with fact-check APIs or retrain with higher-quality data.
            - **Robustness (Partial/Failed):**
                - The endpoint struggled or errored on empty, long, or junk inputs. 
                - **What this means:** It may be vulnerable to denial-of-service, or return confusing/unhelpful errors to users.
                - **Tip:** Add input validation and user-friendly error handling.
            - **Bias/Toxicity (Flagged):**
                - At least one output suggested a **gender bias** (“CEO” described as male).
                - **What this means:** The AI may inadvertently reinforce stereotypes or fail ethical/compliance audits.
                - **Tip:** Use larger, more diverse training data and consider post-processing to flag and fix bias.
            - **MCP Context:**
                - The model’s responses were validated using MCP Context API.
                - **What this means:** The AI is aware of and can leverage external tools or up-to-date context—helpful for “plugin” or retrieval-augmented scenarios.
            ---
            **How to Use This Dashboard:**
            - “Low Risk” or “Passed” means the check is green, but always monitor new releases/versions.
            - Anything “Flagged,” “Partial/Failed,” or below 80% is an action item for your team.
            - Use this report to prioritize fixes and track improvement over time.
            """)

        # PDF
        pdf_bytes = generate_report(
            sec, hall, robust, bias, exec_summary,
            hall.get("evidence", "Evidence not available."), mcp
        )
        st.download_button("Download Comprehensive Report (PDF)", data=pdf_bytes,
                           file_name="AI_Infosec_Report.pdf", mime="application/pdf")
