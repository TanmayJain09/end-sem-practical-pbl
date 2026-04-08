import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from scripts.pdf_generator import generate_admin_pdf
from scripts.graph_generator import (
    generate_daily_trend_graph,
    generate_subject_graph
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "analytics_data" / "admin"

OVERALL_FILE = DATA_DIR / "overall_summary.csv"
SUBJECT_FILE = DATA_DIR / "subject_attendance.csv"
STUDENT_FILE = DATA_DIR / "student_attendance_summary.csv"
DAILY_FILE = DATA_DIR / "daily_attendance_trend.csv"

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Admin Attendance Dashboard",
    layout="wide"
)

st.title("Admin Attendance Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

overall_df = pd.read_csv(OVERALL_FILE)
subject_df = pd.read_csv(SUBJECT_FILE)
student_df = pd.read_csv(STUDENT_FILE)
daily_df = pd.read_csv(DAILY_FILE)

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

st.subheader("Overall Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", int(overall_df["total_students"][0]))
col2.metric("Total Records", int(overall_df["total_records"][0]))
col3.metric("Total Present", int(overall_df["total_present"][0]))
col4.metric("Attendance %", f'{overall_df["attendance_percent"][0]} %')

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

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# Subject Attendance
# --------------------------------------------------

with right:

    st.subheader("Subject Attendance")

    fig = px.bar(
        subject_df,
        x="Subject Code",
        y="attendance_percent",
        color="attendance_percent",
        title="Attendance % by Subject"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()
    
# --------------------------------------------------
# Low Attendance Students
# --------------------------------------------------

st.subheader("Students Below 75% Attendance")

low_attendance = student_df[
    student_df["attendance_percent"] < 75
]

st.dataframe(low_attendance, use_container_width=True)

st.divider()

# --------------------------------------------------
# Download Report
# --------------------------------------------------

st.subheader("Download Student Attendance Report")

# CSV (existing)
csv = student_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="student_attendance_summary.csv",
    mime="text/csv"
)

pdf_buffer = generate_admin_pdf(
    overall_df,
    subject_df,
    student_df,
    daily_df
)

st.download_button(
    label="Download PDF Report",
    data=pdf_buffer,
    file_name="admin_attendance_report.pdf",
    mime="application/pdf"
)