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
        # Remove emoji and 4-byte unicode (non-BMP)
        t = ''.join(c for c in t if ord(c) <= 0xFFFF)
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
                # fallback to Helvetica
                self._dejavu_added = False
                print("WARNING: DejaVuSans.ttf not found. Falling back to Helvetica (ASCII only).")

    def safe_font(self, style="", size=12):
        if hasattr(self, "_dejavu_added") and self._dejavu_added:
            self.set_font("DejaVu", style, size)
        else:
            self.set_font("Helvetica", style, size)

    def header(self):
        self.safe_font("B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.safe_font("", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_prompt_result(self, idx, prompt, result):
        page_width = self.w - 20
        self.safe_font("B", 12)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=1)
        self.safe_font("", 11)
        self.multi_cell(page_width, 7, clean(prompt))
        self.ln(1)
        if result:
            answer = clean(result.get("answer"))
            risk = clean(result.get("risk_level"))
            evidence = clean(result.get("evidence"))
            recommendation = clean(result.get("recommendations"))
            self.safe_font("I", 10)
            self.multi_cell(page_width, 6, "AI Response: " + answer)
            self.multi_cell(page_width, 6, "Risk: " + risk)
            self.multi_cell(page_width, 6, "Evidence: " + evidence)
            self.multi_cell(page_width, 6, "Recommendations: " + recommendation)
        else:
            self.safe_font("I", 10)
            self.multi_cell(page_width, 6, "No result available.")
        self.ln(2)

def generate_report(results):
    pdf = PromptReportPDF()
    pdf.add_page()
    if not results or not isinstance(results, list):
        pdf.safe_font("I", 12)
        pdf.cell(0, 10, "No results found.", ln=1)
    else:
        for idx, res in enumerate(results):
            pdf.add_prompt_result(idx, res.get("prompt", "-"), res)
    return pdf.output(dest='S').encode('latin-1')  # Should be fine now, only BMP chars
