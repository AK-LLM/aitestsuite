from prompt_banks import get_prompt_bank, add_prompt, remove_prompt
import streamlit as st
import pandas as pd

def show_help():
    st.info("""
    **Help & Workflow**
    - Use the sidebar to select or edit prompt banks, upload prompts, and tag prompts by risk or type.
    - Run all or selected prompts for risk assessment.
    - Results show per-prompt evidence, risk, and a custom recommendation.
    - Download results as PDF, CSV, or JSON. Re-run or replay past sessions for regression analysis.
    """)

def load_prompt_bank(domain=None):
    return get_prompt_bank(domain)

def parse_uploaded_prompts(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        prompts = []
        for _, row in df.iterrows():
            prompts.append({
                "prompt": row['prompt'],
                "desc": row.get('desc', ""),
                "tags": row.get('tags', "").split(",") if 'tags' in row and isinstance(row['tags'], str) else []
            })
        return prompts
    except Exception:
        uploaded_file.seek(0)
        return [{"prompt": line.strip(), "desc": "", "tags": []} for line in uploaded_file if line.strip()]

def deduplicate_prompts(prompts):
    seen = set()
    unique = []
    for p in prompts:
        key = (p['prompt'], p.get('desc', ''))
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

def filter_prompts_by_tag(prompts, tag):
    return [p for p in prompts if tag in p.get('tags', [])]
