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
    generate_subject_graph,
    generate_teacher_daily_graph,
    generate_batch_graph,
    generate_student_daily_graph,
    generate_student_subject_graph
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

def generate_teacher_pdf(selected_teacher, student_df, daily_df, batch_df):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # ------------------------------------------
    # Page 1 — Summary
    # ------------------------------------------

    elements.append(Paragraph(f"{selected_teacher} - Attendance Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    total_students = student_df["PRN"].nunique()
    total_classes = student_df["total_classes"].sum()
    total_present = student_df["total_present"].sum()

    attendance_percent = round(
        (total_present / total_classes) * 100, 2
    ) if total_classes > 0 else 0

    defaulters = len(student_df[student_df["attendance_percent"] < 75])

    summary_data = [
        ["Metric", "Value"],
        ["Total Students", total_students],
        ["Total Classes", total_classes],
        ["Total Present", total_present],
        ["Attendance %", f"{attendance_percent}%"],
        ["Defaulters (<75%)", defaulters],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # ------------------------------------------
    # Page 2 — Student Table
    # ------------------------------------------

    elements.append(Paragraph("Student Attendance", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    table_data = [["PRN", "Name", "Classes", "Present", "%"]]

    for _, row in student_df.iterrows():
        table_data.append([
            row["PRN"],
            row.get("Name", ""),
            row["total_classes"],
            row["total_present"],
            f'{row["attendance_percent"]}%'
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # ------------------------------------------
    # Page 3 — Graphs
    # ------------------------------------------

    elements.append(Paragraph("Graphs", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    daily_graph = generate_teacher_daily_graph(daily_df)
    batch_graph = generate_batch_graph(batch_df)

    elements.append(Image(daily_graph, width=400, height=200))
    elements.append(Spacer(1, 20))
    elements.append(Image(batch_graph, width=400, height=200))

    doc.build(elements)

    buffer.seek(0)
    return buffer

def generate_student_pdf(student_name, student_df, daily_df, subject_df):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # ------------------------------------------
    # Page 1 — Summary
    # ------------------------------------------

    elements.append(Paragraph(f"{student_name} - Attendance Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    total_classes = len(student_df)
    total_present = student_df["Present"].sum()
    total_absent = total_classes - total_present

    attendance_percent = round(
        (total_present / total_classes) * 100, 2
    ) if total_classes > 0 else 0

    summary_data = [
        ["Metric", "Value"],
        ["Total Classes", total_classes],
        ["Present", total_present],
        ["Absent", total_absent],
        ["Attendance %", f"{attendance_percent}%"],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # ------------------------------------------
    # Page 2 — Full Attendance Table
    # ------------------------------------------

    elements.append(Paragraph("Attendance Records", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    table_data = [["Date", "Subject", "Present", "Batch"]]

    for _, row in student_df.iterrows():
        table_data.append([
            str(row["Date"]),
            row["Subject"],
            row["Present"],
            row["Batch"]
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # ------------------------------------------
    # Page 3 — Graphs
    # ------------------------------------------

    elements.append(Paragraph("Graphs", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    daily_graph = generate_student_daily_graph(daily_df)
    subject_graph = generate_student_subject_graph(subject_df)

    elements.append(Image(daily_graph, width=400, height=200))
    elements.append(Spacer(1, 20))
    elements.append(Image(subject_graph, width=400, height=200))

    doc.build(elements)

    buffer.seek(0)
    return buffer