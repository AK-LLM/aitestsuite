from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_report(results):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, y, "AI Prompt Security & Hallucination Assessment")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(60, y, "Summary of Results")
    y -= 24

    if not results:
        c.drawString(60, y, "No results found.")
    else:
        for idx, res in enumerate(results):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(60, y, f"Prompt {idx+1}:")
            y -= 16

            c.setFont("Helvetica", 11)
            prompt = res.get("prompt", "-")
            c.drawString(70, y, f"Prompt: {prompt}")
            y -= 16

            answer = res.get("answer", "-")
            c.drawString(70, y, f"AI Response: {answer}")
            y -= 14

            risk = res.get("risk_level", "-")
            c.drawString(70, y, f"Risk: {risk}")
            y -= 14

            evidence = res.get("evidence", "-")
            c.drawString(70, y, f"Evidence: {evidence}")
            y -= 14

            recommendations = res.get("recommendations", "-")
            c.drawString(70, y, f"Recommendations: {recommendations}")
            y -= 24

            # Start a new page if too low
            if y < 80:
                c.showPage()
                y = height - 40

    c.save()
    buffer.seek(0)
    return buffer.read()
