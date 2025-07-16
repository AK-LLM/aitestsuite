from fpdf import FPDF
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "AI Prompt Security & Hallucination Assessment", 0, 1, "C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, title, 0, 1)
        self.ln(1)

    def section_body(self, body):
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 8, body)
        self.ln()

    def result_block(self, data, prompt_idx):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 8, f"Prompt {prompt_idx + 1}:", ln=True)
        self.set_font("DejaVu", "", 12)
        prompt = data.get("prompt", "")
        self.multi_cell(0, 7, str(prompt))
        self.ln(1)
        
        # Risk badge
        risk_badge = data.get("risk_badge", "")
        risk_score = data.get("risk_score", "")
        if risk_badge:
            if risk_badge == "High":
                self.set_text_color(255, 0, 0)
            elif risk_badge == "Medium":
                self.set_text_color(255, 165, 0)
            else:
                self.set_text_color(0, 128, 0)
            self.set_font("DejaVu", "B", 11)
            self.cell(0, 8, f"Risk: {risk_badge} ({risk_score})", ln=True)
            self.set_text_color(0, 0, 0)
        
        # Tags
        tags = data.get("tags")
        if tags:
            self.set_font("DejaVu", "I", 11)
            self.cell(0, 8, "Tags: " + ", ".join(str(t) for t in tags), ln=True)
        
        # Evidence
        evidence = str(data.get("evidence", "") or "")
        if evidence.strip():
            self.set_font("DejaVu", "B", 11)
            self.cell(0, 8, "Evidence:", ln=True)
            self.set_font("DejaVu", "", 12)
            self.multi_cell(0, 7, evidence)
        
        # Recommendations
        recommendations = str(data.get("recommendations", "") or "")
        if recommendations.strip():
            self.set_font("DejaVu", "B", 11)
            self.cell(0, 8, "Recommendations:", ln=True)
            self.set_font("DejaVu", "", 12)
            self.multi_cell(0, 7, recommendations)
        
        self.ln(3)

def ensure_font():
    # Check if font exists locally, otherwise throw error.
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError("DejaVuSans.ttf not found in project folder.")
    return FONT_PATH

def generate_report(results):
    font_path = ensure_font()
    pdf = PDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)
    
    pdf.section_title("Summary of Results")
    pdf.ln(1)
    
    for idx, res in enumerate(results):
        pdf.result_block(res, idx)
    
    return pdf.output(dest="S").encode("latin-1")
