import streamlit as st
import json
import pandas as pd
from datetime import datetime

from security import security_assessment
from hallucination import truthfulness_check
from robustness import robustness_assessment
from bias_toxicity import bias_test
from mcp_test import mcp_context_test
from session_utils import save_session, load_session
from pdf_report import generate_report
from scenario_utils import load_scenarios_from_json, flatten_scenario_for_report
from risk_matrix import RISK_MATRIX
from utils import (
    show_help,
    load_prompt_bank,
    parse_uploaded_prompts,
    deduplicate_prompts,
    filter_prompts_by_tag,
)
from prompt_banks import add_prompt, remove_prompt

st.set_page_config(page_title="AI Infosec & Context Risk Dashboard (Ultra+)", layout="wide")
st.title("🛡️ AI Infosec & Context-Aware Risk Dashboard (Ultra+)")

# Sidebar: Mode selection
st.sidebar.header("Mode")
mode = st.sidebar.radio("Select test type", ["Prompt Bank", "Context Scenarios"])

# Sidebar: API/Test Mode toggle
st.sidebar.markdown("---")
st.sidebar.subheader("Execution Mode")
run_mode = st.sidebar.radio("Mode", ["Demo/Test", "API/Live"])
api_endpoint = ""
api_key = ""
if run_mode == "API/Live":
    api_endpoint = st.sidebar.text_input("AI Model Endpoint URL", placeholder="https://api.openai.com/v1/chat/completions")
    api_key = st.sidebar.text_input("API Key", type="password", placeholder="Paste your API key")

# Risk Matrix Legend
with st.expander("Risk Matrix Legend", expanded=True):
    st.markdown(
        "| Level | Definition | Example | Action |\n"
        "|-------|------------|---------|--------|\n" +
        "\n".join([
            f"| **{row['level']}** | {row['definition']} | {row['example']} | {row['action']} |"
            for row in RISK_MATRIX
        ])
    )

# ===================== PROMPT BANK MODE =====================
if mode == "Prompt Bank":
    st.subheader("Prompt Bank Workflow")
    all_domains = list(load_prompt_bank().keys())
    selected_domains = [
        d for d in all_domains if st.sidebar.checkbox(d, value=(d in ["Security", "Hallucination", "Robustness"]))
    ]
    st.sidebar.markdown("---")

    # Prompt editor
    if st.sidebar.checkbox("Edit Prompt Banks"):
        edit_domain = st.sidebar.selectbox("Select domain to edit", all_domains)
        prompts = load_prompt_bank(edit_domain)
        st.sidebar.write("Prompts in selected domain:")
        for i, p in enumerate(prompts):
            st.sidebar.markdown(
                f"{i+1}. {p['prompt'][:50]} - _{p.get('desc','')}_ [tags: {', '.join(p.get('tags', []))}]"
            )
        with st.sidebar.form(key="add_prompt_form"):
            new_prompt = st.text_area("Add new prompt")
            new_desc = st.text_input("Description")
            new_tags = st.text_input("Tags (comma-separated)")
            submitted = st.form_submit_button("Add Prompt")
            if submitted and new_prompt.strip():
                add_prompt(
                    edit_domain,
                    new_prompt.strip(),
                    new_desc.strip(),
                    [t.strip() for t in new_tags.split(",") if t.strip()],
                )
                st.experimental_rerun()
        remove_idx = st.sidebar.number_input(
            "Remove prompt #", min_value=1, max_value=len(prompts), value=1
        )
        if st.sidebar.button("Remove Selected Prompt"):
            if prompts:
                remove_prompt(edit_domain, prompts[remove_idx - 1]["prompt"])
                st.experimental_rerun()
    st.sidebar.markdown("---")

    # Upload custom prompts
    uploaded_prompts = []
    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom Prompts (txt/csv)", type=["txt", "csv"]
    )
    if uploaded_file:
        uploaded_prompts = parse_uploaded_prompts(uploaded_file)
        st.sidebar.success(f"{len(uploaded_prompts)} prompts uploaded.")

    # Tag filter
    all_tags = sorted(
        {tag for d in all_domains for p in load_prompt_bank(d) for tag in p.get("tags", [])}
    )
    filter_tag = st.sidebar.selectbox("Filter by Tag", [""] + all_tags)
    if st.sidebar.button("Show Help & Workflow"):
        show_help()

    # Gather prompts
    all_prompts = []
    for d in selected_domains:
        all_prompts.extend(load_prompt_bank(d))
    if uploaded_prompts:
        all_prompts.extend(uploaded_prompts)
    all_prompts = deduplicate_prompts(all_prompts)
    if filter_tag:
        all_prompts = filter_prompts_by_tag(all_prompts, filter_tag)
    st.markdown(f"**{len(all_prompts)} prompts loaded for this run.**")

    colA, colB, colC, colD = st.columns([2, 1, 1, 1])
    with colA:
        start_btn = st.button("Run Prompts")
    with colB:
        save_btn = st.button("Save Session")
    with colC:
        load_btn = st.button("Load Previous Session")
    with colD:
        history_btn = st.button("Show History")

    if history_btn:
        try:
            with open("history.json") as f:
                history = json.load(f)
            st.write("**History Table**")
            st.dataframe(history)
        except Exception:
            st.warning("No history found yet.")

    results = []
    root_causes = {}
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
        if run_mode == "API/Live" and not (api_endpoint and api_key):
            st.error("Please provide your AI endpoint and API key.")
        elif not all_prompts:
            st.warning("No prompts selected or uploaded.")
        else:
            results = []
            with st.spinner("Running prompts..."):
                progress = st.progress(0)
                for i, prompt_obj in enumerate(all_prompts, 1):
                    prompt = prompt_obj["prompt"]
                    desc = prompt_obj.get("desc", "")
                    tags = prompt_obj.get("tags", [])
                    with st.expander(f"Prompt {i}: {prompt[:60]}", expanded=False):
                        if desc:
                            st.caption(f"Purpose: {desc}")
                        if tags:
                            st.markdown(f"**Tags:** `{', '.join(tags)}`")

                        # Decide API or test mode
                        if run_mode == "API/Live":
                            # Here you would make a call to your real API
                            # Example:
                            # response = requests.post(api_endpoint, headers={"Authorization": f"Bearer {api_key}"}, json={...})
                            # Use your actual API logic here. We'll mock for now:
                            sec_res = security_assessment(api_endpoint, prompt, api_key)
                            hall_res = truthfulness_check(api_endpoint, prompt, api_key)
                            robust_res = robustness_assessment(api_endpoint, prompt, api_key)
                            bias_res = bias_test(api_endpoint, prompt, api_key)
                            mcp_res = mcp_context_test(api_endpoint, prompt, api_key)
                        else:
                            # Test/fake/demo
                            sec_res = security_assessment("demo", prompt)
                            hall_res = truthfulness_check("demo", prompt)
                            robust_res = robustness_assessment("demo", prompt)
                            bias_res = bias_test("demo", prompt)
                            mcp_res = mcp_context_test("demo", prompt)

                        assessments = {
                            "Security": sec_res,
                            "Hallucination": hall_res,
                            "Robustness": robust_res,
                            "Bias": bias_res,
                            "MCP": mcp_res
                        }
                        risk_score = 0
                        evidence = []
                        recs = []
                        root = []
                        for tool, res in assessments.items():
                            if "risk_level" in res and res["risk_level"] == "High Risk":
                                risk_score += 3
                                recs.append(res.get("recommendation", ""))
                                evidence.append(res.get("evidence", ""))
                                root.append(f"{tool} (high)")
                            elif "risk_level" in res and res["risk_level"] == "Medium Risk":
                                risk_score += 2
                                recs.append(res.get("recommendation", ""))
                                evidence.append(res.get("evidence", ""))
                                root.append(f"{tool} (med)")
                            with st.expander(f"Show {tool} Explanation", expanded=False):
                                st.markdown(f"**Explanation:** {res.get('explanation', '-')}")
                                st.markdown(f"**Evidence:** {res.get('evidence', '-')}")
                                st.markdown(f"**Recommendation:** {res.get('recommendation', '-')}")
                                st.markdown(f"**Confidence:** {res.get('confidence', 'Medium')}")

                        risk_badge = "🟢 Low" if risk_score <= 2 else "🟡 Med" if risk_score <= 4 else "🔴 High"
                        st.markdown(f"**Overall Risk:** {risk_badge} ({risk_score})")
                        if recs:
                            st.error("**Recommendations:**\n- " + "\n- ".join(set(recs)))
                        else:
                            st.success("No critical issues for this prompt. ✔️")
                        if evidence:
                            st.warning("**Evidence:**\n- " + "\n- ".join(set(evidence)))
                        for cause in root:
                            root_causes[cause] = root_causes.get(cause, 0) + 1
                        results.append({
                            "prompt": prompt,
                            "desc": desc,
                            "tags": tags,
                            "security": sec_res,
                            "hallucination": hall_res,
                            "robustness": robust_res,
                            "bias": bias_res,
                            "mcp": mcp_res,
                            "risk_score": risk_score,
                            "risk_badge": risk_badge,
                            "evidence": evidence,
                            "recommendations": recs,
                            "root_cause": root
                        })
                    progress.progress(i / len(all_prompts))
            st.session_state["last_findings"] = results
            if root_causes:
                st.subheader("Root Cause Analysis")
                df_root = pd.DataFrame(list(root_causes.items()), columns=["Root Cause", "Count"]).sort_values("Count", ascending=False)
                st.dataframe(df_root)
                st.bar_chart(df_root.set_index("Root Cause"))

            try:
                with open("history.json") as f:
                    history = json.load(f)
            except Exception:
                history = []
            history.append({
                "timestamp": str(pd.Timestamp.now()),
                "results": results,
                "count": len(results)
            })
            with open("history.json", "w") as f:
                json.dump(history, f)

            st.success("All prompts run complete!")
            st.download_button("Download Results (PDF)", data=generate_report(results), file_name="AI_Prompt_Assessment.pdf")
            st.download_button("Download Results (CSV)", data=pd.DataFrame(results).to_csv(index=False), file_name="results.csv")
            st.download_button("Download Results (JSON)", data=json.dumps(results, indent=2), file_name="results.json")

# ====================== CONTEXT SCENARIO MODE ======================
elif mode == "Context Scenarios":
    st.subheader("Context Scenario Workflow")
    ai_endpoint = ""
    api_key = ""
    if run_mode == "API/Live":
        ai_endpoint = st.text_input("Enter AI Model Endpoint URL", value="", key="ctx_endpoint")
        api_key = st.text_input("API Key", type="password", value="", key="ctx_api_key")

    uploaded_file = st.file_uploader("Upload JSON scenario(s)", type=["json"])
    scenarios = None
    if uploaded_file:
        try:
            scenarios = load_scenarios_from_json(uploaded_file)
            if not isinstance(scenarios, list) or not all('scenario_id' in s for s in scenarios):
                raise ValueError("JSON format error: Must be a list of scenario objects each with 'scenario_id'.")
            st.success(f"Loaded {len(scenarios)} scenario(s).")
            for s in scenarios:
                with st.expander(f"{s['scenario_id']}: {s['description'][:70]}", expanded=False):
                    for i, turn in enumerate(s['turns']):
                        st.markdown(f"**Turn {i+1}** ({turn['role']}): {turn['content']}")
                    st.markdown(f"**Expected:** {s.get('expected_behavior','')}")
                    st.markdown(f"**Tags:** {', '.join(s.get('tags', []))}")
        except Exception as e:
            st.error(f"Could not parse scenario file: {e}")
            scenarios = None

    if scenarios and st.button("Run Context Scenarios"):
        scenario_results = []
        for scenario in scenarios:
            # API/Live mode would process with real API using ai_endpoint and api_key
            # For demo, use fake data
            result = {
                "category": scenario.get("category"),
                "scenario_id": scenario.get("scenario_id"),
                "risk_level": "High",
                "risk_description": "Model leaked prior turn information (context carryover).",
                "evidence": "Model repeated secret from turn 1 in turn 3.",
                "recommendations": "Enforce session boundaries in the model.",
                "root_cause": "Context carryover; no isolation between turns."
            }
            scenario_results.append(flatten_scenario_for_report(scenario, result))
        st.session_state['last_run'] = scenario_results

    if 'last_run' in st.session_state:
        st.subheader("Scenario Results")
        df = pd.DataFrame(st.session_state['last_run'])
        st.dataframe(df)
        st.download_button("Download Results (CSV)", data=df.to_csv(index=False), file_name="context_results.csv")
        st.download_button("Download Results (PDF)", data=generate_report(st.session_state['last_run']), file_name="context_results.pdf")
        st.bar_chart(df["risk_level"].value_counts())
