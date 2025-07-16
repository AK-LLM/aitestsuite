from fpdf import FPDF
import os

FONT_PATH = "DejaVuSans.ttf"

def clean(text):
    """Clean and normalize text for PDF output."""
    if not text:
        return "-"
    try:
        t = str(text)
        t = t.replace("\r", "")
        t = t.replace("\n\n", "\n")
        t = t.strip()
        # Remove characters not in BMP
        t = "".join(c for c in t if ord(c) < 0x10000)
        return t if t else "-"
    except Exception:
        return "-"

class PromptReportPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)
        self.add_unicode_font()

    def add_unicode_font(self):
        if not hasattr(self, "_dejavu_added"):
            if os.path.exists(FONT_PATH):
                self.add_font("DejaVu", "", FONT_PATH, uni=True)
                self.add_font("DejaVu", "B", FONT_PATH, uni=True)
                self.add_font("DejaVu", "I", FONT_PATH, uni=True)
                self._dejavu_added = True
            else:
                raise RuntimeError("DejaVuSans.ttf not found in project!")

    def header(self):
        self.set_font("DejaVu", "B", 16, uni=True)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-18)
        self.set_font("DejaVu", "", 9, uni=True)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_prompt_result(self, idx, prompt, result):
        page_width = self.w - 20
        self.set_font("DejaVu", "B", 12, uni=True)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=1)
        self.set_font("DejaVu", "", 11, uni=True)
        self.multi_cell(page_width, 7, clean(prompt))
        self.ln(1)
        if result:
            answer = clean(result.get("answer"))
            risk = clean(result.get("risk_level"))
            evidence = clean(result.get("evidence"))
            recommendation = clean(result.get("recommendations"))
            self.set_font("DejaVu", "I", 10, uni=True)
