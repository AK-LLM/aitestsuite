import streamlit as st

def show_help():
    st.sidebar.title("🛠️ Workflow Guide & Help")
    st.sidebar.markdown("""
    **Step-by-step Workflow:**
    1. Enter your AI model's API endpoint URL.
    2. Configure feature toggles in the sidebar:
        - **Fact-Checking API**: Validate truthfulness with external sources (or run local-only check).
        - **Notifications**: Send results to Slack/Jira, or bypass for privacy.
        - **MCP Context**: Check with external context (or local bypass).
    3. Click **Start Assessment**.
    4. Review summary metrics.
    5. Download the PDF report.

    **Tool Descriptions:**
    - **Security Test**: Checks prompt injection.
    - **Truthfulness Test**: Evaluates factual accuracy.
    - **Robustness Test**: Tests model stability.
    - **MCP Context Test**: Evaluates external knowledge/context use.

    **Support:**  
    Contact your AI Infosec team for more help or enhancements.
    """)
