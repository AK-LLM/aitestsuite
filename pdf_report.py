from fpdf import FPDF
import os

def ensure_font(pdf):
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf font not found. Please add it to your app directory.")
    if "DejaVu" not in pdf.fonts:
        pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=10)

def safe_text(text, limit=120, fallback="N/A"):
    """Prepare text for safe PDF rendering."""
    if text is None:
        return fallback
    try:
        s = str(text)
        # Remove excessive whitespace and newlines
        s = s.replace('\n', ' ').replace('\r', ' ')
        # Remove any control characters FPDF can't handle
        s = ''.join(ch if 32 <= ord(ch) <= 126 or ch in "–—’‘”“…" else '?' for ch in s)
        if len(s) > limit:
            s = s[:limit] + "..."
        return s
    except Exception:
        return fallback

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
        try:
            pdf.set_font("DejaVu", size=10)
            pdf.cell(0, 8, f"Prompt {idx}:", ln=1)
            pdf.set_font("DejaVu", size=9)
            prompt = safe_text(r.get("prompt", ""), 250)
            pdf.multi_cell(0, 7, prompt)
            
            risk_badge = safe_text(r.get("risk_badge", ""))
            ris
