# pdf_report.py

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# Cross-mapping for frameworks (extend as needed)
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

def generate_report(results):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(letter), leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18)
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleB = styles["Heading2"]
    styleSmall = ParagraphStyle(name='Small', fontSize=8, leading=10)

    elements = []
    elements.append(Paragraph("<b>AI Context Security Assessment Report</b>", styles["Title"]))
    elements.append(Spacer(1, 18))

    # ==== SUMMARY COVERAGE ====
    metric_set = set()
    category_hits = {}
    for r in results:
        cat = r.get("category", "Unknown")
        metric = _map_category(cat)["vector"]
        metric_set.add(metric)
        category_hits[metric] = category_hits.get(metric, 0) + 1

    elements.append(Paragraph("<b>Summary Coverage Matrix</b>", styleB))
    coverage_data = [["Security Metric / Attack Vector", "Cases Detected"]]
    for metric in sorted(metric_set):
        coverage_data.append([metric, str(category_hits.get(metric, 0))])
    coverage_tbl = Table(coverage_data, hAlign="LEFT", colWidths=[240, 100])
    coverage_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#223344")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 11),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
    ]))
    elements.append(coverage_tbl)
    elements.append(Spacer(1, 14))

    # ==== DETAILED FINDINGS ====
    elements.append(Paragraph("<b>Detailed Scenario Findings</b>", styleB))

    findings_data = [[
        "Scenario ID", "Category", "Attack Vector", "Severity", "Risk Description", "Evidence", "Recommendation", "Framework Mapping"
    ]]
    for r in results:
        cat = r.get("category", "Unknown")
        m = _map_category(cat)
        findings_data.append([
            r.get("scenario_id", "-"),
            cat,
            m["vector"],
            r.get("risk_level", "-"),
            r.get("risk_description", "-"),
            r.get("evidence", "-"),
            r.get("recommendations", "-"),
            m["frameworks"],
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
    elements.append(findings_tbl)

    # ==== LEGEND ====
    elements.append(PageBreak())
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

