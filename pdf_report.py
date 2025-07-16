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
                self.add_font("DejaVu", "I", FONT_PATH, uni=True)
                self.add_font("DejaVu", "BI", FONT_PATH, uni=True)
                self.has_dejavu = True
            except Exception:
                self.has_dejavu = False

    def safe_font(self, style="", size=11):
        """Switch to DejaVu if available, else Arial."""
        if self.has_dejavu:
            self.set_font("DejaVu", style, size)
        else:
            base = "Arial"
            self.set_font(base, style, size)

    def header(self):
        self.safe_font("B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.safe_font("", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def result_block(self, data, idx):
        self.safe_font("B", 13)
        self.cell(0, 10, f"Prompt {idx + 1}:", ln=1)
        self.safe_font("", 11)
        self.multi_cell(0, 8, clean(data.get("prompt")))
        self.ln(1)

        self.safe_font("I", 11)
        self.cell(0, 7, "Purpose: " + clean(data.get("purpose")), ln=1)
        self.safe_font("", 11)

        self.safe_font("B", 11)
        self.cell(0, 7, "Risk:", ln=1)
        self.safe_font_
