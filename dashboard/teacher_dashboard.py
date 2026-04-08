import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from scripts.pdf_generator import generate_teacher_pdf

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ANALYTICS_DIR = BASE_DIR / "data" / "analytics_data" / "teacher"
MASTER_DATA_DIR = BASE_DIR / "data" / "master_data"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

SUBJECT_MASTER = MASTER_DATA_DIR / "subjects_master.csv"
MASTER_ATTENDANCE = PROCESSED_DIR / "master_attendance.csv"

SUBJECT_FILE = ANALYTICS_DIR / "teacher_subject_summary.csv"
STUDENT_FILE = ANALYTICS_DIR / "teacher_student_summary.csv"
DAILY_FILE = ANALYTICS_DIR / "teacher_daily_trend.csv"

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Teacher Attendance Dashboard",
    layout="wide"
)

st.title("Teacher Attendance Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

subject_df = pd.read_csv(SUBJECT_FILE)
student_df = pd.read_csv(STUDENT_FILE)
daily_df = pd.read_csv(DAILY_FILE)

subjects_master = pd.read_csv(SUBJECT_MASTER)
master_attendance = pd.read_csv(MASTER_ATTENDANCE)

teachers = subjects_master["Teacher"].unique()

# --------------------------------------------------
# Teacher Selector
# --------------------------------------------------

selected_teacher = st.selectbox(
    "Select Teacher",
    teachers
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------

subject_df = subject_df[subject_df["Teacher"] == selected_teacher]
student_df = student_df[student_df["Teacher"] == selected_teacher]
daily_df = daily_df[daily_df["Teacher"] == selected_teacher]

# --------------------------------------------------
# Get subject code for that teacher
# --------------------------------------------------

teacher_subjects = subjects_master[
    subjects_master["Teacher"] == selected_teacher
]["Subject Code"].values

attendance_teacher = master_attendance[
    master_attendance["Subject Code"].isin(teacher_subjects)
]

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

total_students = student_df["PRN"].nunique()
total_classes = student_df["total_classes"].sum()
total_present = student_df["total_present"].sum()

attendance_percent = round(
    (total_present / total_classes) * 100, 2
) if total_classes > 0 else 0

st.subheader("Overall Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Total Classes", total_classes)
col3.metric("Total Present", total_present)
col4.metric("Attendance %", f"{attendance_percent} %")

st.divider()

# --------------------------------------------------
# Charts Layout
# --------------------------------------------------

left, right = st.columns(2)

# --------------------------------------------------
# Daily Attendance Trend
# --------------------------------------------------

with left:

    st.subheader("Daily Attendance Trend")

    fig = px.line(
        daily_df,
        x="Date",
        y="attendance_percent",
        markers=True,
        title="Attendance % Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Batch Distribution (Pie Chart)
# --------------------------------------------------

with right:

    st.subheader("Batch Distribution")

    batch_counts = (
        attendance_teacher[["PRN", "Batch"]]
        .drop_duplicates()
        .groupby("Batch")
        .count()
        .reset_index()
    )

    batch_counts.columns = ["Batch", "Students"]

    fig = px.pie(
        batch_counts,
        values="Students",
        names="Batch",
        title="Student Distribution by Batch"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Low Attendance Students
# --------------------------------------------------

st.subheader("Students Below 75% Attendance")

# Add student names
student_names = master_attendance[["PRN", "Name"]].drop_duplicates()

student_df = student_df.merge(student_names, on="PRN", how="left")

low_attendance = student_df[
    student_df["attendance_percent"] < 75
][["PRN", "Name", "attendance_percent"]]

st.dataframe(low_attendance, use_container_width=True)

st.divider()

# --------------------------------------------------
# Download Report
# --------------------------------------------------

st.subheader("Download Student Attendance Report")

report = student_df[["PRN", "Name", "total_classes", "total_present", "attendance_percent"]]

csv = report.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{selected_teacher}_student_attendance.csv",
    mime="text/csv"
)

# ---------------- PDF ----------------

pdf_buffer = generate_teacher_pdf(
    selected_teacher,
    student_df,
    daily_df,
    batch_counts
)

st.download_button(
    label="Download PDF Report",
    data=pdf_buffer,
    file_name=f"{selected_teacher}_attendance_report.pdf",
    mime="application/pdf"
)