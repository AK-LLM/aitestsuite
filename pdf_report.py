from fpdf import FPDF

def clean(text):
    """Normalize text for PDF output, avoid None/empty issues."""
    if not text:
        return "-"
    try:
        t = str(text)
        t = t.replace("\r", "")
        t = t.replace("\n\n", "\n")
        t = t.strip()
        return t if t else "-"
    except Exception:
        return "-"

class PromptReportPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=1, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_prompt_result(self, idx, prompt, result):
        page_width = self.w - 20  # Avoid zero-width
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=1)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(page_width, 7, clean(prompt))
        self.ln(1)
        if result:
            answer = clean(result.get("answer"))
            risk = clean(result.get("risk_level"))
            evidence = clean(result.get("evidence"))
            recommendation = clean(result.get("recommendations"))
            self.set_font("Helvetica", "I", 10)
            self.multi_cell(page_width, 6, "AI Response: " + answer)
            self.multi_cell(page_width, 6, "Risk: " + risk)
            self.multi_cell(page_width, 6, "Evidence: " + evidence)
            self.multi_cell(page_width, 6, "Recommendations: " + recommendation)
        else:
            self.set_font("Helvetica", "I", 10)
            self.multi_cell(page_width, 6, "No result available.")
        self.ln(2)

def generate_report(results):
    pdf = PromptReportPDF()
    pdf.add_page()
    page_width = pdf.w - 20
    if not results or not isinstance(results, list):
        pdf.set_font("Helvetica", "I", 12)
        pdf.cell(0, 10, "No results found.", ln=1)
    else:
        for idx, res in enumerate(results):
            pdf.add_prompt_result(idx, res.get("prompt", "-"), res)
    return pdf.output(dest='S').encode('latin-1')
