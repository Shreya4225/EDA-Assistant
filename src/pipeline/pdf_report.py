# src/pipeline/pdf_report.py

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

from src.pipeline.report_builder import generate_report_charts


def generate_pdf_report(df, ai_insight, output_path="EDA_Report.pdf"):
    """Builds a complete EDA report PDF."""

    chart_paths, captions = generate_report_charts(df)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # --- Title Page ---
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 100, "📊 EDA Auto Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, f"Dataset Rows: {df.shape[0]}")
    c.drawString(50, height - 160, f"Dataset Columns: {df.shape[1]}")
    c.drawString(50, height - 200, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.showPage()

    # --- AI Insights Page ---
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "🧠 AI Insights & Summary")

    c.setFont("Helvetica", 11)

    text_obj = c.beginText(50, height - 80)
    for line in ai_insight.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    c.showPage()

    # --- Charts Pages ---
    for i, img_path in enumerate(chart_paths):
        c.setFont("Helvetica-Bold", 15)
        c.drawString(50, height - 50, f"Figure {i + 1}")

        if os.path.exists(img_path):
            c.drawImage(img_path, 50, 200, width - 100, height - 300)

        c.setFont("Helvetica", 11)
        c.drawString(50, 180, captions[i])

        c.showPage()

    c.save()
    return output_path
