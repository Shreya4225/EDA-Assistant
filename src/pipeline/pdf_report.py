# src/pipeline/pdf_report.py

import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from src.pipeline.report_builder import generate_report_charts


def generate_pdf_report(df, ai_insights, output_path="EDA_Report.pdf"):
    """
    Generates a clean multi-page EDA report with charts and AI text insights.
    Automatically wraps text properly to prevent overflow.
    """

    chart_paths, captions = generate_report_charts(df)

    pdf = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50,
    )

    width, height = A4
    styles = getSampleStyleSheet()

    # Custom bullet style
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6,
    )

    content = []

    # Title Page
    content.append(Paragraph("<b>📊 EDA Auto Report</b>", styles['Heading1']))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Dataset Rows: {df.shape[0]}", styles['Normal']))
    content.append(Paragraph(f"Dataset Columns: {df.shape[1]}", styles['Normal']))
    content.append(Paragraph(
        f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    ))
    content.append(PageBreak())

    # Insights Page
    content.append(Paragraph("🧠 AI Insights & Summary", styles['Heading2']))
    content.append(Spacer(1, 8))
    content.append(Paragraph("Here are insights based on the dataset:", styles['Normal']))
    content.append(Spacer(1, 12))

    # Split text into bullet list items
    if isinstance(ai_insights, str):
        insights_list = ai_insights.split("\n")
    else:
        insights_list = ai_insights

    for point in insights_list:
        if point.strip():
            content.append(Paragraph(f"• {point}", bullet_style))

    content.append(PageBreak())

    # Chart Pages
    content.append(Paragraph("📈 Visual Analysis", styles['Heading2']))
    content.append(Spacer(1, 15))

    for i, img_path in enumerate(chart_paths):
        if os.path.exists(img_path):
            content.append(Image(img_path, width=450, height=250))

        content.append(Spacer(1, 10))
        content.append(Paragraph(captions[i], styles['Normal']))
        content.append(PageBreak())

    pdf.build(content)
    return output_path



# # src/pipeline/pdf_report.py

# import os
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from datetime import datetime

# from src.pipeline.report_builder import generate_report_charts


# def generate_pdf_report(df, ai_insight, output_path="EDA_Report.pdf"):
#     """Builds a complete EDA report PDF."""

#     chart_paths, captions = generate_report_charts(df)

#     c = canvas.Canvas(output_path, pagesize=A4)
#     width, height = A4

#     # --- Title Page ---
#     c.setFont("Helvetica-Bold", 22)
#     c.drawString(50, height - 100, "📊 EDA Auto Report")

#     c.setFont("Helvetica", 12)
#     c.drawString(50, height - 140, f"Dataset Rows: {df.shape[0]}")
#     c.drawString(50, height - 160, f"Dataset Columns: {df.shape[1]}")
#     c.drawString(50, height - 200, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     c.showPage()

#     # --- AI Insights Page ---
#     c.setFont("Helvetica-Bold", 18)
#     c.drawString(50, height - 50, "🧠 AI Insights & Summary")

#     c.setFont("Helvetica", 11)

#     text_obj = c.beginText(50, height - 80)
#     for line in ai_insight.split("\n"):
#         text_obj.textLine(line)
#     c.drawText(text_obj)
#     c.showPage()

#     # --- Charts Pages ---
#     for i, img_path in enumerate(chart_paths):
#         c.setFont("Helvetica-Bold", 15)
#         c.drawString(50, height - 50, f"Figure {i + 1}")

#         if os.path.exists(img_path):
#             c.drawImage(img_path, 50, 200, width - 100, height - 300)

#         c.setFont("Helvetica", 11)
#         c.drawString(50, 180, captions[i])

#         c.showPage()

#     c.save()
#     return output_path
