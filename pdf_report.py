# pdf_report.py (Unicode/emoji safe, fpdf2 + DejaVuSans.ttf)
from fpdf import FPDF
from io import BytesIO
import os

def generate_report(results):
    pdf = FPDF()
    pdf.add_page()
    # Use a Unicode font (ensure DejaVuSans.ttf is in your project directory)
    font_path = "DejaVuSans.ttf"
    if not os.path.isfile(font_path):
        raise FileNotFoundError(
            f"Font file '{font_path}' not found. Please download DejaVuSans.ttf and place it in your project folder.\n"
            "Download: https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans.ttf?raw=true"
        )
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(200, 10, "AI Prompt Assessment Report", ln=True, align="C")
    pdf.ln(10)
    for i, r in enumerate(results, 1):
        pdf.multi_cell(0, 10, f"{i}. Prompt: {r['prompt']}")
        pdf.multi_cell(0, 8, f"Risk: {r.get('risk_badge','N/A')} - {r.get('risk_score','N/A')}")
        for k in ["security", "hallucination", "robustness", "bias", "mcp"]:
            if k in r and isinstance(r[k], dict):
                pdf.multi_cell(0, 8, f"{k.capitalize()}: {r[k]}")
        if r.get("evidence"):
            pdf.multi_cell(0, 8, "Evidence: " + "; ".join([str(e) for e in r["evidence"]]))
        if r.get("recommendations"):
            pdf.multi_cell(0, 8, "Recommendations: " + "; ".join([str(e) for e in r["recommendations"]]))
        pdf.ln(4)

    buffer = BytesIO()
    pdf.output(buffer)
    pdf_bytes = buffer.getvalue()
    return pdf_bytes
