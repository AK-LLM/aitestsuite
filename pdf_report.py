from fpdf import FPDF
import os

# Helper to load Unicode-safe font
def ensure_font(pdf):
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf font not found. Please add it to your app directory.")
    if "DejaVu" not in pdf.fonts:
        pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=10)

def safe_text(text, limit=150):
    """Truncate and clean text for PDF cell."""
    s = str(text).replace('\n', ' ').replace('\r', ' ')
    return s[:limit] + ('...' if len(s) > limit else '')

def generate_report(results):
    pdf = FPDF()
    pdf.add_page()
    ensure_font(pdf)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("DejaVu", size=16)
    pdf.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align='C')
    pdf.ln(5)

    pdf.set_font("DejaVu", size=11)
    pdf.cell(0, 10, "Summary of Results", ln=1)

    for idx, r in enumerate(results, 1):
        pdf.set_font("DejaVu", size=10)
        pdf.cell(0, 8, f"Prompt {idx}:", ln=1)
        pdf.set_font("DejaVu", size=9)
        pdf.multi_cell(0, 7, safe_text(r.get("prompt", "N/A"), 300))
        
        pdf.set_font("DejaVu", size=9)
        risk_badge = safe_text(r.get("risk_badge", "N/A"))
        risk_score = safe_text(r.get("risk_score", "N/A"))
        pdf.multi_cell(0, 7, f"Risk: {risk_badge} – {risk_score}")
        
        result = safe_text(r.get("result", "N/A"), 600)
        pdf.multi_cell(0, 7, f"Result: {result}")
        
        if "explanation" in r:
            pdf.multi_cell(0, 7, "Explanation: " + safe_text(r["explanation"], 600))
        
        pdf.ln(2)
        pdf.set_draw_color(150, 150, 150)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    # Export PDF to bytes for Streamlit
    return pdf.output(dest='S').encode('latin-1')

