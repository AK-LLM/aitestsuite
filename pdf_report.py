from fpdf import FPDF
import os

def generate_report(results):
    class PDF(FPDF):
        def header(self):
            self.set_font("DejaVu", style="B", size=18)
            self.cell(0, 15, "AI Prompt Security & Hallucination Assessment", ln=True, align='C')
            self.ln(5)
        def chapter_title(self, num, label):
            self.set_font("DejaVu", style="B", size=14)
            self.cell(0, 10, f"Prompt {num}: {label}", ln=True)
        def chapter_body(self, text):
            self.set_font("DejaVu", size=12)
            self.multi_cell(0, 8, text)
        def result_block(self, data):
            self.set_font("DejaVu", size=12)
            if data.get("risk_badge"):
                self.set_text_color(255,0,0) if data["risk_badge"]=="High" else self.set_text_color(255,165,0) if data["risk_badge"]=="Medium" else self.set_text_color(0,128,0)
                self.cell(0, 8, f"Risk: {data['risk_badge']} ({data.get('risk_score','N/A')})", ln=True)
                self.set_text_color(0,0,0)
            if data.get("tags"):
                self.set_font("DejaVu", style="I", size=11)
                self.cell(0,8, f"Tags: {', '.join(data['tags'])}", ln=True)
                self.set_font("DejaVu", size=12)
            if data.get("evidence"):
                self.set_font("DejaVu", style="B", size=11)
                self.cell(0,8, "Evidence:", ln=True)
                self.set_font("DejaVu", size=12)
                self.multi_cell(0,7, data["evidence"])
            if data.get("recommendations"):
                self.set_font("DejaVu", style="B", size=11)
                self.cell(0,8, "Recommendations:", ln=True)
                self.set_font("DejaVu", size=12)
                self.multi_cell(0,7, data["recommendations"])
            self.ln(3)

    pdf = PDF()
    # Assume DejaVuSans.ttf in working directory
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0,10, "Summary of Results", ln=True)

    for i, res in enumerate(results, 1):
        pdf.chapter_title(i, res.get("prompt", ""))
        pdf.chapter_body(res.get("result", ""))
        pdf.result_block(res)
        pdf.ln(3)

    return pdf.output(dest='S').encode("latin-1")
