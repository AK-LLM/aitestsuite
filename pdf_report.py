from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from risk_matrix import RISK_MATRIX

def safe(val):
    if val is None:
        return "-"
    if isinstance(val, list):
        return "; ".join(str(x) for x in val if x)
    return str(val)

def draw_risk_matrix(c, y, width):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Risk Matrix Legend")
    y -= 16
    c.setFont("Helvetica", 10)
    for row in RISK_MATRIX:
        c.drawString(60, y, f"{row['level']} - {row['definition']}")
        y -= 13
        c.drawString(80, y, f"Example: {row['example']}")
        y -= 13
        c.drawString(80, y, f"Action: {row['action']}")
        y -= 15
    y -= 10
    return y

def generate_report(scenario_results):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 35

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Context-Aware Risk Assessment Report")
    y -= 28

    # Risk Matrix Legend
    y = draw_risk_matrix(c, y, width)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Scenario Findings")
    y -= 18

    c.setFont("Helvetica", 10)
    for idx, item in enumerate(scenario_results):
        if y < 130:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Scenario Findings (cont’d)")
            y -= 18
            c.setFont("Helvetica", 10)

        c.setFont("Helvetica-Bold", 11)
        c.drawString(55, y, f"Scenario {idx+1}: {safe(item.get('scenario_id'))}")
        y -= 14
        c.setFont("Helvetica", 10)

        # Context trace
        c.drawString(60, y, f"Context Trace: {safe(item.get('context_trace'))[:120]}")
        y -= 12
        # Show descriptive finding (risk/why/evidence/rec)
        c.drawString(60, y, f"Risk Level: {item.get('risk_level')} | {item.get('risk_description')}")
        y -= 12
        c.drawString(60, y, f"Evidence: {safe(item.get('evidence'))}")
        y -= 12
        c.drawString(60, y, f"Recommendation: {safe(item.get('recommendations'))}")
        y -= 12
        c.drawString(60, y, f"Root Cause: {safe(item.get('root_cause'))}")
        y -= 10
        c.drawString(60, y, f"Expected: {safe(item.get('expected_behavior'))}")
        y -= 12
        c.drawString(60, y, f"Tags: {safe(item.get('tags'))}")
        y -= 12
        c.drawString(60, y, f"Description: {safe(item.get('description'))}")
        y -= 14

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
