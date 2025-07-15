# pdf_report.py (Unicode-safe, for fpdf2)

from fpdf import FPDF
from io import BytesIO

def generate_report(results):
    pdf = FPDF()
    pdf.add_page()
    # Use a font that supports Unicode. 'Arial Unicode MS' is universal if available,
    # or fallback to DejaVu. fpdf2 supports custom TTF fonts if needed.
    # For simplicity, we'll use the default and let fpdf2 handle Unicode.
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "AI Prompt Assessment Report", ln=True, align="C")
    pdf.ln(10)
    for i, r in enumerate(results, 1):
        pdf.multi_cell(0, 10, f"{i}. Prompt: {r['prompt']}")
        pdf.multi_cell(0, 8, f"Risk: {r.get('risk_badge','N/A')} - {r.get('risk_score','N/A')}")
        for k in ["security", "hallucination", "robustness", "bias", "mcp"]:
            if k in r and isinstance(r[k], dict):
                pdf.multi_cell(0, 8, f"{k.capitalize()}: {r[k]}")
        if r.get("evidence"):
            pdf.multi_cell(0, 8, "Evidence: " + "; ".join([str(e) for e in r["evidence"]]))
        if r.get("recommendations"):
            pdf.multi_cell(0, 8, "Recommendations: " + "; ".join([str(e) for e in r["recommendations"]]))
        pdf.ln(4)

    # Output PDF to bytes (fpdf2 handles Unicode with utf-8)
    pdf_bytes = pdf.output(dest="S").encode("utf-8")
    return pdf_bytes
