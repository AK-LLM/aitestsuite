# pdf_report.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_report(results):
    if results is None:
        results = []

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Prompt Security & Hallucination Assessment")
    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Summary of Results")
    y -= 25

    c.setFont("Helvetica", 10)

    if not results:
        c.drawString(60, y, "No results found.")
        y -= 15
    else:
        for idx, res in enumerate(results):
            if y < 100:
                c.showPage()
                y = height - 50
            c.setFont("Helvetica-Bold", 11)
            c.drawString(55, y, f"Prompt {idx+1}:")
            y -= 15

            c.setFont("Helvetica", 10)
            c.drawString(70, y, f"Prompt: {str(res.get('prompt', '-') or '-')[:100]}")
            y -= 13
            c.drawString(70, y, f"AI Response: {str(res.get('answer', '-') or '-')[:100]}")
            y -= 13
            c.drawString(70, y, f"Risk: {str(res.get('risk_level', '-') or '-')}")
            y -= 13
            c.drawString(70, y, f"Evidence: {str(res.get('evidence', '-') or '-')[:100]}")
            y -= 13
            c.drawString(70, y, f"Recommendations: {str(res.get('recommendations', '-') or '-')[:100]}")
            y -= 20

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
