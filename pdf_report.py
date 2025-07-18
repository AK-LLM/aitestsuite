# pdf_report.py

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
import matplotlib.pyplot as plt
from collections import Counter

# Map for attack categories to frameworks
CATEGORY_MAP = {
    "Prompt Injection": {"vector": "Prompt Injection", "frameworks": "OWASP LLM #1, MITRE ATLAS ATC-PRM"},
    "Roleplay & Jailbreak": {"vector": "Jailbreak/Role Abuse", "frameworks": "OWASP LLM #2, MITRE ATLAS ATC-ROL"},
    "Context Carryover": {"vector": "Context Leakage", "frameworks": "OWASP LLM #4, MITRE ATLAS ATC-CTX"},
    "PII & Privacy": {"vector": "PII Exposure", "frameworks": "NIST 800-53 PL-4, GDPR"},
    "Bias & Toxicity": {"vector": "Bias/Toxicity", "frameworks": "OWASP LLM #5"},
    "Long Context & Overflow": {"vector": "Memory/Overflow", "frameworks": "OWASP LLM #4"},
    "MCP/Context Manipulation": {"vector": "Context Manipulation", "frameworks": "MITRE ATLAS ATC-CTX"},
    "Fact/Fiction Shift": {"vector": "Fact Consistency", "frameworks": "NIST 800-53 SI-4"},
    "Edge Cases": {"vector": "Adversarial Input", "frameworks": "MITRE ATLAS ATC-ADV"},
    "Complex Dialogues": {"vector": "Social Engineering", "frameworks": "MITRE ATLAS ATC-ENG"},
    "Fine-grained Hallucination": {"vector": "Hallucination", "frameworks": "OWASP LLM #6"},
    "Regulatory": {"vector": "Compliance", "frameworks": "GDPR, HIPAA"},
    "Ethics": {"vector": "Value Alignment", "frameworks": "OECD, UNESCO"},
    "Stress": {"vector": "Robustness/Scalability", "frameworks": "OWASP LLM #10"},
}

def _map_category(cat):
    return CATEGORY_MAP.get(cat, {"vector": cat, "frameworks": "-"})

def safe_val(val, default):
    if val is None:
        return default
    if isinstance(val, str) and val.strip() == "":
        return default
    return val

def plot_bar(data_dict, title, ylabel):
    """Return a ReportLab Image of a matplotlib bar chart."""
    fig, ax = plt.subplots(figsize=(6, 2.7), dpi=110)
    items = list(data_dict.items())
    keys = [str(k) for k, v in items]
    vals = [v for k, v in items]
    bars = ax.bar(keys, vals, color="#556b8a")
    ax.set_title(title, fontsize=12)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    for bar in bars:
        ax.annotate(str(bar.get_height()), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image(buf, width=320, height=145)

def split_results_by_type(results):
    # If your results have a "mode" or "source" key, split accordingly
    # Otherwise, guess by keys present (e.g., context scenarios usually have "scenario_id")
    prompt_attacks = []
    context_attacks = []
    for r in results:
        if r.get("mode") == "Context Scenario" or r.get("source") == "Context Scenario" or "context" in r.get("category","").lower():
            context_attacks.append(r)
        else:
            prompt_attacks.append(r)
    return prompt_attacks, context_attacks

def get_risk_status(risk):
    if risk is None or risk == "":
        return "Pass"
    if isinstance(risk, str):
        if "fail" in risk.lower():
            return "Fail"
        if "not applicable" in risk.lower() or "n/a" in risk.lower():
            return "Not Applicable"
        if "mitigated" in risk.lower():
            return "Mitigated"
        if "compliant" in risk.lower():
            return "Compliant"
        if "high" in risk.lower():
            return "High"
        if "medium" in risk.lower():
            return "Medium"
        if "low" in risk.lower():
            return "Low"
    return risk

def findings_table_block(results, table_title="Findings Table"):
    findings_data = [[
        "Scenario ID", "Category", "Attack Vector", "Severity", "Risk Description", "Evidence", "Recommendation", "Framework Mapping"
    ]]
    for r in results:
        cat = r.get("category", "Unknown")
        m = _map_category(cat)
        findings_data.append([
            safe_val(r.get("scenario_id", "-"), "-"),
            safe_val(cat, "Not Applicable"),
            safe_val(m["vector"], "Not Applicable"),
            get_risk_status(r.get("risk_level", None)),
            safe_val(r.get("risk_description", None), "No issue detected"),
            safe_val(r.get("evidence", None), "N/A"),
            safe_val(r.get("recommendations", None), "N/A"),
            safe_val(m["frameworks"], "Not Applicable"),
        ])
    findings_tbl = Table(findings_data, repeatRows=1, hAlign="LEFT", colWidths=[70, 80, 100, 60, 170, 120, 120, 120])
    findings_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#223344")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.18, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 8),
        ("ALIGN", (3,1), (3,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return findings_tbl

def generate_report(results):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(letter), leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18)
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleB = styles["Heading2"]
    styleSmall = ParagraphStyle(name='Small', fontSize=8, leading=10)

    elements = []
    elements.append(Paragraph("<b>AI Security Assessment Report</b>", styles["Title"]))
    elements.append(Spacer(1, 18))

    prompt_attacks, context_attacks = split_results_by_type(results)

    # ===== PROMPT ATTACKS SECTION =====
    if prompt_attacks:
        # --- Risk Graphs for Prompt Attacks
        risk_levels = Counter([get_risk_status(r.get("risk_level", None)) for r in prompt_attacks])
        category_hits = Counter([_map_category(r.get("category", "Unknown"))["vector"] for r in prompt_attacks])

        elements.append(Paragraph("<b>Prompt Attack Risk Levels</b>", styleB))
        elements.append(plot_bar(risk_levels, "Prompt Attack: Risk Levels", "Count"))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>Prompt Attack Vectors Detected</b>", styleB))
        elements.append(plot_bar(category_hits, "Prompt Attack Vectors", "Cases"))
        elements.append(Spacer(1, 14))

        elements.append(Paragraph("<b>Prompt Attack Findings</b>", styleB))
        elements.append(findings_table_block(prompt_attacks, "Prompt Attack Findings"))
        elements.append(PageBreak())

    # ===== CONTEXT SCENARIOS SECTION =====
    if context_attacks:
        risk_levels = Counter([get_risk_status(r.get("risk_level", None)) for r in context_attacks])
        category_hits = Counter([_map_category(r.get("category", "Unknown"))["vector"] for r in context_attacks])

        elements.append(Paragraph("<b>Context Scenario Risk Levels</b>", styleB))
        elements.append(plot_bar(risk_levels, "Context Scenarios: Risk Levels", "Count"))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>Context Scenario Vectors Detected</b>", styleB))
        elements.append(plot_bar(category_hits, "Context Scenario Vectors", "Cases"))
        elements.append(Spacer(1, 14))

        elements.append(Paragraph("<b>Context Scenario Findings</b>", styleB))
        elements.append(findings_table_block(context_attacks, "Context Scenario Findings"))
        elements.append(PageBreak())

    # ==== LEGEND ====
    elements.append(Paragraph("<b>Legend & Framework References</b>", styles["Heading3"]))
    elements.append(Spacer(1, 8))
    legend = [
        ["Attack Vector", "Description"],
        ["Prompt Injection", "Tricking model to ignore prior instructions or security boundaries"],
        ["Jailbreak/Role Abuse", "Getting the AI to break its rules via roleplay or prompt chaining"],
        ["Context Leakage", "Leaking information from previous turns or sessions"],
        ["PII Exposure", "Revealing personal or confidential data"],
        ["Bias/Toxicity", "Producing biased, unfair, or toxic output"],
        ["Memory/Overflow", "Losing context, hallucinating or mixing facts in long chains"],
        ["Compliance", "Failure to meet GDPR, HIPAA, or similar standards"],
        ["Robustness/Scalability", "Model crashes, instability under stress/flood"],
        ["Value Alignment", "Responding to manipulation or ethical traps"],
    ]
    legend_tbl = Table(legend, hAlign="LEFT", colWidths=[120, 340])
    legend_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#3b4252")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.13, colors.grey),
    ]))
    elements.append(legend_tbl)
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Framework references: OWASP Top 10 for LLMs, MITRE ATLAS, NIST 800-53, GDPR, HIPAA, etc.",
        styleSmall
    ))

    doc.build(elements)
    pdf = buf.getvalue()
    buf.close()
    return pdf
