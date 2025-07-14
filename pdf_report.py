from fpdf import FPDF

def generate_report(sec, hall, robust, bias, exec_summary, evidence, mcp):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AI Infosec & Hallucination Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    # Executive summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Executive Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, exec_summary or "No executive summary.")
    pdf.ln(4)

    # Security
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Security Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Risk: {sec.get('risk_level', 'N/A')}")
    pdf.multi_cell(0, 10, f"Details: {sec.get('summary', 'N/A')}")
    pdf.ln(2)

    # Hallucination
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Hallucination Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Truthfulness Score: {hall.get('score', 'N/A')}")
    pdf.multi_cell(0, 10, f"Remarks: {hall.get('remarks', 'N/A')}")
    pdf.ln(2)

    # Robustness
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Robustness Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Status: {robust.get('status', 'N/A')}")
    pdf.multi_cell(0, 10, f"Remarks: {robust.get('remarks', 'N/A')}")
    pdf.ln(2)

    # Bias/Toxicity
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Bias/Toxicity Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Status: {bias.get('status', 'N/A')}")
    pdf.multi_cell(0, 10, f"Remarks: {bias.get('remarks', 'N/A')}")
    pdf.ln(2)

    # MCP Context
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "MCP/Context Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Result: {mcp.get('context_result', 'N/A')}")
    pdf.multi_cell(0, 10, f"Details: {mcp.get('details', '')}")
    pdf.ln(2)

    # Evidence
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Evidence Log:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, evidence or "No evidence captured.")

    # Return as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
