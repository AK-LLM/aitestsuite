from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def safe(val):
    """Ensure all fields are printable and no None/nulls."""
    if val is None:
        return "-"
    if isinstance(val, list):
        return "; ".join(str(x) for x in val if x)
    return str(val)

def generate_report(results):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 17)
    c.drawString(50, y, "AI Prompt Security & Hallucination Assessment")
    y -= 35

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Summary of Results")
    y -= 22

    c.setFont("Helvetica", 10)

    if not results:
        c.drawString(60, y, "No results found.")
        y -= 15
    else:
        for idx, res in enumerate(results):
            if y < 120:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica-Bold", 17)
                c.drawString(50, y, "AI Prompt Security & Hallucination Assessment (cont’d)")
                y -= 35
                c.setFont("Helvetica-Bold", 13)
                c.drawString(50, y, "Summary of Results (cont’d)")
                y -= 22
                c.setFont("Helvetica", 10)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(55, y, f"Prompt {idx+1}:")
            y -= 15
            c.setFont("Helvetica", 10)

            # Print main fields
            fields = [
                ("Prompt", res.get("prompt", "-")),
                ("Description", res.get("desc", "-")),
                ("Tags", ", ".join(res.get("tags", []))),
                ("Risk Score", res.get("risk_score", "-")),
                ("Risk Badge", res.get("risk_badge", "-")),
                ("Evidence", "; ".join(res.get("evidence", []))),
                ("Recommendations", "; ".join(res.get("recommendations", []))),
            ]
            for label, field in fields:
                # Wrap long lines
                lines = []
                t = safe(field)
                while len(t) > 105:
                    idx_ = t[:105].rfind(" ")
                    if idx_ == -1: idx_ = 105
                    lines.append(t[:idx_])
                    t = t[idx_:].lstrip()
                lines.append(t)
                for line in lines:
                    c.drawString(70, y, f"{label}: {line}")
                    y -= 12

            # Nested results
            for k in ("security", "hallucination", "robustness", "bias", "mcp"):
                v = res.get(k)
                if isinstance(v, dict):
                    c.drawString(70, y, f"{k.capitalize()} Results:")
                    y -= 12
                    for subk, subv in v.items():
                        line = f"    {subk}: {safe(subv)}"
                        c.drawString(80, y, line)
                        y -= 12

            y -= 8
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
