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
    # Remove non-printable characters
    t = t.replace("\r", "")
    t = t.replace("\n\n", "\n")
    t = t.strip()
    return t if t else "-"

class PromptReportPDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=True, align='C')
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'C')

    def result_block(self, data, idx):
        def safe_line(label, val):
            v = clean(val)
            return f"{label}: {v if v and v != '-' else '-'}"
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=True)
        self.set_font("DejaVu", "", 11)
        self.multi_cell(0, 7, clean(data.get("prompt", "-")))
        self.ln(1)
        self.set_font("DejaVu", "I", 10)
        self.multi_cell(0, 6, "AI Response: " + clean(data.get("result", "-")))
        self.ln(1)
        self.set_font("DejaVu", "B", 10)
        badge = clean(data.get("risk_badge", "-"))
        score = clean(data.get("risk_score", "-"))
        self.cell(0, 7, f"Risk: {badge if badge else '-'} - {score if score else '-'}", ln=True)
        self.set_font("DejaVu", "", 10)
        self.multi_cell(0, 6, safe_line("Evidence", data.get("evidence", "-")))
        self.multi_cell(0, 6, safe_line("Recommendations", data.get("recommendations", "-")))
        self.ln(2)

def ensure_font():
    """Ensure DejaVuSans.ttf exists, raise error if not."""
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"Missing font file: {FONT_PATH}. Place DejaVuSans.ttf in the project folder.")
    return FONT_PATH

def generate_report(results):
    ensure_font()
    pdf = PromptReportPDF()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "I", FONT_PATH, uni=True)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Summary of Results", ln=True)
    pdf.ln(2)
    for idx, res in enumerate(results):
        pdf.result_block(res, idx)
    return pdf.output(dest="S").encode("latin-1")
