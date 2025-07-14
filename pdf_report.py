from fpdf import FPDF

def generate_report(sec, hall, robust, bias, exec_summary, evidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AI Infosec & Hallucination Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Executive Summary:\n{exec_summary}\n")
    pdf.cell(0, 10, "Security Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Risk: {sec['risk_level']}\nDetails: {sec['summary']}")
    pdf.cell(0, 10, "Hallucination Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Truthfulness Score: {hall['score']}\nRemarks: {hall['remarks']}")
    pdf.cell(0, 10, "Robustness Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Status: {robust['status']}\nRemarks: {robust['remarks']}")
    pdf.cell(0, 10, "Bias/Toxicity Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Status: {bias['status']}\nRemarks: {bias['remarks']}")
    pdf.multi_cell(0, 10, f"Sample Evidence: {evidence}")
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
