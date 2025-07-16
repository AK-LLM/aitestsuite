from fpdf import FPDF
import os

FONT_PATH = "DejaVuSans.ttf"

def clean(text):
    """Clean and normalize text for PDF."""
    if text is None:
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
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def result_block(self, data, idx):
        # Each prompt/result block
        self.set_font("DejaVu", "B", 13)
        self.cell(0, 10, f"Prompt {idx + 1}:", ln=1)
        self.set_font("DejaVu", "", 11)
        self.multi_cell(0, 8, clean(data.get("prompt")))
        self.ln(1)

        self.set_font("DejaVu", "I", 11)
        self.cell(0, 7, "Purpose: " + clean(data.get("purpose")), ln=1)
        self.set_font("DejaVu", "", 11)

        # RISK
        self.set_font("DejaVu", "B", 11)
        self.cell(0, 7, "Risk:", ln=1)
        self.set_font("DejaVu", "", 11)
        risk = str(data.get("risk", "-"))
        self.multi_cell(0, 7, risk)
        self.ln(1)

        # Evidence
        self.set_font("DejaVu", "B", 11)
        self.cell(0, 7, "Evidence:", ln=1)
        self.set_font("DejaVu", "", 11)
        evidence = clean(data.get("evidence"))
        if not evidence:
            evidence = "-"
        self.multi_cell(0, 7, evidence)
        self.ln(1)

        # Recommendations
        self.set_font("DejaVu", "B", 11)
        self.cell(0, 7, "Recommendations:", ln=1)
        self.set_font("DejaVu", "", 11)
        rec = clean(data.get("recommendations"))
        if not rec:
            rec = "-"
        self.multi_cell(0, 7, rec)
        self.ln(5)

def generate_report(results):
    pdf = PromptReportPDF()
    pdf.add_page()

    # Register the font (DejaVu)
    if os.path.exists(FONT_PATH):
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
        pdf.add_font("DejaVu", "I", FONT_PATH, uni=True)
    else:
        # Use built-in font as fallback
        pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 12, "Summary of Results", ln=1)
    pdf.ln(5)

    for idx, res in enumerate(results):
        pdf.result_block(res, idx)

    return pdf.output(dest='S').encode('latin-1')

