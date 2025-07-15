import os

# ---- Font auto-downloader (only runs once) ----
def ensure_font():
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        import requests
        url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf"
        r = requests.get(url)
        if r.status_code == 200:
            with open(font_path, "wb") as f:
                f.write(r.content)
        else:
            raise FileNotFoundError("Could not download DejaVuSans.ttf font. Please check your internet connection.")
    return font_path

# ---- Use this in your PDF function ----
from fpdf import FPDF
from io import BytesIO

def generate_report(results):
    font_path = ensure_font()
    pdf = FPDF()
    pdf.add_page()
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
