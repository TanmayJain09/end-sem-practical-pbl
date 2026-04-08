import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from scripts.pdf_generator import generate_student_pdf

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MASTER_DATA_DIR = BASE_DIR / "data" / "master_data"

MASTER_ATTENDANCE = PROCESSED_DIR / "master_attendance.csv"
SUBJECT_MASTER = MASTER_DATA_DIR / "subjects_master.csv"

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Student Attendance Dashboard",
    layout="wide"
)

st.title("Student Attendance Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

attendance_df = pd.read_csv(MASTER_ATTENDANCE)
subject_df = pd.read_csv(SUBJECT_MASTER)

# Merge subject names
attendance_df = attendance_df.merge(
    subject_df,
    on="Subject Code",
    how="left"
)

attendance_df["Present"] = attendance_df["Present"].astype(int)
attendance_df["Date"] = pd.to_datetime(attendance_df["Date"])

# --------------------------------------------------
# Student Selector
# --------------------------------------------------

students = attendance_df[["PRN", "Name"]].drop_duplicates()

student_display = students.apply(
    lambda x: f"{x['PRN']} - {x['Name']}",
    axis=1
)

selected_student_display = st.selectbox(
    "Select Student",
    student_display
)

selected_prn = selected_student_display.split(" - ")[0]

student_data = attendance_df[
    attendance_df["PRN"] == int(selected_prn)
]

student_name = student_data["Name"].iloc[0]

st.subheader(f"Student: {student_name}")

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

total_classes = len(student_data)
total_present = student_data["Present"].sum()
total_absent = total_classes - total_present

attendance_percent = round(
    (total_present / total_classes) * 100, 2
) if total_classes > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Classes", total_classes)
col2.metric("Present", total_present)
col3.metric("Absent", total_absent)
col4.metric("Attendance %", f"{attendance_percent} %")

st.divider()

# --------------------------------------------------
# Charts Layout
# --------------------------------------------------

left, right = st.columns(2)

# --------------------------------------------------
# Attendance Trend
# --------------------------------------------------

with left:

    st.subheader("Attendance Trend")

    daily = (
        student_data
        .groupby("Date")
        .agg(
            total=("Present", "count"),
            present=("Present", "sum")
        )
        .reset_index()
    )

    daily["attendance_percent"] = (
        daily["present"] / daily["total"] * 100
    )

    fig = px.line(
        daily,
        x="Date",
        y="attendance_percent",
        markers=True,
        title="Attendance % Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Subject Attendance
# --------------------------------------------------

with right:

    st.subheader("Subject Attendance")

    subject_summary = (
        student_data
        .groupby("Subject")
        .agg(
            total=("Present", "count"),
            present=("Present", "sum")
        )
        .reset_index()
    )

    subject_summary["attendance_percent"] = (
        subject_summary["present"]
        / subject_summary["total"]
        * 100
    )

    fig = px.bar(
        subject_summary,
        x="Subject",
        y="attendance_percent",
        color="attendance_percent",
        title="Attendance % by Subject"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Download Report
# --------------------------------------------------

st.subheader("Download My Attendance Report")

report = student_data[
    ["Date", "Subject", "Present", "Batch"]
]

csv = report.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{selected_prn}_attendance.csv",
    mime="text/csv"
)

# ---------------- PDF ----------------

pdf_buffer = generate_student_pdf(
    student_name,
    student_data,
    daily,
    subject_summary
)

st.download_button(
    label="Download PDF Report",
    data=pdf_buffer,
    file_name=f"{selected_prn}_attendance_report.pdf",
    mime="application/pdf"
)