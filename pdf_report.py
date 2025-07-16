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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_dejavu = False
        if os.path.exists(FONT_PATH):
            try:
                self.add_font("DejaVu", "", FONT_PATH, uni=True)
                self.add_font("DejaVu", "B", FONT_PATH, uni=True)
                self.has_dejavu = True
            except Exception as e:
                print("Warning: Could not load DejaVuSans.ttf, using default font. Error:", e)
        else:
            print("Warning: DejaVuSans.ttf not found, using default font.")

    def header(self):
        if self.has_dejavu:
            self.set_font("DejaVu", "B", 16)
        else:
            self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AI Prompt Security & Hallucination Assessment", ln=True, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        if self.has_dejavu:
            self.set_font("DejaVu", "", 9)
        else:
            self.set_font("Arial", "", 9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def result_block(self, data, idx):
        fontname = "DejaVu" if self.has_dejavu else "Arial"
        # Section header
        self.set_font(fontname, "B", 12)
        self.cell(0, 8, f"Prompt {idx + 1}:", ln=True)
        # Prompt
        self.set_font(fontname, "", 11)
        self.multi_cell(0, 7, clean(data.get("prompt")))
        self.ln(1)
        # Output test result
        self.set_font(fontname, "B", 10)
        self.multi_cell(0, 6, "Test Result: " + clean(data.get("result")))
        # Output risk, evidence, recommendations if present
        for key in ["risk", "evidence", "recommendations"]:
            val = data.get(key)
            if val:
                self.set_font(fontname, "B", 10)
                self.cell(0, 6, f"{key.capitalize()}:", ln=True)
                self.set_font(fontname, "", 10)
                self.multi_cell(0, 6, clean(val))
        self.ln(2)

def generate_report(results):
    pdf = PromptReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    fontname = "DejaVu" if pdf.has_dejavu else "Arial"
    pdf.set_font(fontname, "", 12)
    pdf.cell(0, 10, "Summary of Results", ln=True)
    pdf.ln(2)
    for idx, res in enumerate(results):
        pdf.result_block(res, idx)
        pdf.ln(2)
    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin-1")
