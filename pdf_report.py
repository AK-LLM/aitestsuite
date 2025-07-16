from fpdf import FPDF
import os

FONT_PATH = "DejaVuSans.ttf"

def ensure_font():
    if not os.path.exists(FONT_PATH):
        # Attempt download (should not happen on Streamlit Cloud if file uploaded)
        import urllib.request
        url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
        urllib.request.urlretrieve(url, FONT_PATH)
    return FONT_PATH

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 12, "AI Prompt Security & Hallucination Assessment", ln=True, align="C")
        self.ln(6)

    def section_title(self, title):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def result_block(self, data, idx):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 8, f"Prompt {idx+1}:", ln=True)
        self.set_font("DejaVu", "", 11)
        self.multi_cell(0, 7, data.get("prompt", ""))
        self.ln(1)

        # Show the AI's response/result
        if "result" in data:
            self.set_font("DejaVu", "I", 10)
            self.multi_cell(0, 6, f"AI Response:\n{data['result']}")
            self.ln(1)
        # Add risk/evidence/recommendations if present
        if "risk_score" in data or "risk_badge" in data:
            self.set_font("DejaVu", "B", 10)
            badge = data.get("risk_badge", "N/A")
            score = data.get("risk_score", "N/A")
            self.cell(0, 7, f"Risk: {badge} - {score}", ln=True)
        if "evidence" in data:
            self.set_font("DejaVu", "", 10)
            self.multi_cell(0, 6, f"Evidence: {data['evidence']}")
        if "recommendations" in data:
            self.set_font("DejaVu", "", 10)
            self.multi_cell(0, 6, f"Recommendations: {data['recommendations']}")
        self.ln(2)

def generate_report(results):
    ensure_font()
    pdf = PDF()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "I", FONT_PATH, uni=True)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.section_title("Summary of Results")
    pdf.ln(1)
    for idx, res in enumerate(results):
        pdf.result_block(res, idx)
    # Output with UTF-8 encoding for full Unicode compatibility
    return pdf.output(dest="S").encode("utf-8")
