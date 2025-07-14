from fpdf import FPDF
from io import BytesIO

def generate_report(sec, hall, robust):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AI Infosec & Hallucination Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Security Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Risk: {sec['risk_level']}\nDetails: {sec['summary']}")
    pdf.ln(5)

    pdf.cell(0, 10, "Hallucination Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Truthfulness Score: {hall['score']}\nRemarks: {hall['remarks']}")
    pdf.ln(5)

    pdf.cell(0, 10, "Robustness Assessment:", ln=True)
    pdf.multi_cell(0, 10, f"Status: {robust['status']}\nRemarks: {robust['remarks']}")

    # Return PDF as bytes for Streamlit download
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Correct way for in-memory buffer
    return pdf_bytes
