from fpdf import FPDF
import os

FONT_PATH = "DejaVuSans.ttf"

def clean(text):
    """Clean and normalize text for PDF."""
    if not text:
        return "-"
    try:
        t = str(text)
    except Exception:
        return "-"
    t = t.replace("\r", "")
    t = t.replace("\n\n", "\n")
    t = t.strip()
    return t if t else "-"

class PromptReportPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", 0, 1, "C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_prompt_result(self, idx, prompt, result):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=1)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 7, clean(prompt))
        self.ln(1)
        # Risk Level
        risk = result.get("risk", "-")
        if isinstance(risk, (list, tuple)):
            risk = ", ".join([clean(r) for r in risk])
        self.set_font("Arial", "B", 11)
        self.cell(0, 7, f"Risk: {clean(risk)}", ln=1)
        # Evidence
        evidence = result.get("evidence", "-")
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, f"Evidence: {clean(evidence)}")
        # Recommendations
        recommendations = result.get("recommendations", "-")
        self.set_font("Arial", "I", 11)
        self.multi_cell(0, 6, f"Recommendations: {clean(recommendations)}")
        self.ln(2)

def generate_report(results):
    pdf = PromptReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    # Use DejaVu font if available
    if os.path.exists(FONT_PATH):
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
        pdf.add_font("DejaVu", "I", FONT_PATH, uni=True)
        pdf.set_font("DejaVu", "", 11)
    else:
        pdf.set_font("Arial", "", 11)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Summary of Results", ln=1)
    pdf.ln(2)
    for idx, item in enumerate(results):
        prompt = item.get("prompt", "-")
        result = item.get("result", {}) if isinstance(item.get("result", {}), dict) else {}
        pdf.add_prompt_result(idx, prompt, result)
    # Output the PDF as bytes for Streamlit
    pdf_bytes = pdf.output(dest="S")
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin-1")
    return pdf_bytes
