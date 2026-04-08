from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Image, Table, TableStyle, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf(title, df, graph_buffer=None):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # =========================================
    # PAGE 1 → SUMMARY + INSIGHTS
    # =========================================
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 20))

    total_students = len(df)

    if "attendance_percent" in df.columns:
        avg_attendance = round(df["attendance_percent"].mean(), 2)
        defaulters = df[df["attendance_percent"] < 75].shape[0]
    else:
        avg_attendance = "N/A"
        defaulters = "N/A"

    total_classes = (
        df["total_classes"].sum()
        if "total_classes" in df.columns
        else "N/A"
    )

    elements.append(Paragraph("Summary Insights", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    insights_data = [
        ["Metric", "Value"],
        ["Total Students", total_students],
        ["Average Attendance (%)", avg_attendance],
        ["Defaulters (<75%)", defaulters],
        ["Total Classes Conducted", total_classes],
    ]

    insights_table = Table(insights_data)

    insights_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(insights_table)

    elements.append(PageBreak())

    # =========================================
    # PAGE 2 → FULL TABLE
    # =========================================
    elements.append(Paragraph("Detailed Attendance Data", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    data = [list(df.columns)] + df.values.tolist()

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)

    elements.append(PageBreak())

    # =========================================
    # PAGE 3 → GRAPH
    # =========================================
    if graph_buffer:
        elements.append(Paragraph("Attendance Visualization", styles["Heading2"]))
        elements.append(Spacer(1, 20))

        img = Image(graph_buffer, width=450, height=250)
        elements.append(img)

    doc.build(elements)

    buffer.seek(0)
    return buffer