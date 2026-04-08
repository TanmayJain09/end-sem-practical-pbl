from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Image, Table, TableStyle, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

from scripts.graph_generator import (
    generate_daily_trend_graph,
    generate_subject_graph
)

def generate_admin_pdf(overall_df, subject_df, student_df, daily_df):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # =========================================
    # PAGE 1 → KPI SUMMARY
    # =========================================
    elements.append(Paragraph("Admin Attendance Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    kpi_data = [
        ["Metric", "Value"],
        ["Total Students", int(overall_df["total_students"][0])],
        ["Total Records", int(overall_df["total_records"][0])],
        ["Total Present", int(overall_df["total_present"][0])],
        ["Attendance %", f'{overall_df["attendance_percent"][0]} %'],
    ]

    table = Table(kpi_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # =========================================
    # PAGE 2 → SUBJECT DATA
    # =========================================
    elements.append(Paragraph("Subject Attendance", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    subject_data = [list(subject_df.columns)] + subject_df.values.tolist()

    table = Table(subject_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # =========================================
    # PAGE 3 → STUDENT DATA + DEFAULTERS
    # =========================================
    elements.append(Paragraph("Student Attendance", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    student_data = [list(student_df.columns)] + student_df.values.tolist()

    table = Table(student_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
    ]))

    elements.append(table)

    # Defaulters
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Defaulters (<75%)", styles["Heading3"]))

    defaulters = student_df[student_df["attendance_percent"] < 75]

    if not defaulters.empty:
        def_data = [list(defaulters.columns)] + defaulters.values.tolist()
        table = Table(def_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.red),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(table)

    elements.append(PageBreak())

    # =========================================
    # PAGE 4 → GRAPHS
    # =========================================
    elements.append(Paragraph("Attendance Visualizations", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    graph1 = generate_daily_trend_graph(daily_df)
    graph2 = generate_subject_graph(subject_df)

    elements.append(Image(graph1, width=450, height=250))
    elements.append(Spacer(1, 20))
    elements.append(Image(graph2, width=450, height=250))

    doc.build(elements)

    buffer.seek(0)
    return buffer