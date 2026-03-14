import streamlit as st
import pandas as pd
from pathlib import Path

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
# Top Metrics
# --------------------------------------------------

st.subheader("Overall Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    int(overall_df["total_students"][0])
)

col2.metric(
    "Total Records",
    int(overall_df["total_records"][0])
)

col3.metric(
    "Total Present",
    int(overall_df["total_present"][0])
)

col4.metric(
    "Attendance %",
    f'{overall_df["attendance_percent"][0]} %'
)


# --------------------------------------------------
# Daily Attendance Trend
# --------------------------------------------------

st.subheader("Daily Attendance Trend")

st.line_chart(
    daily_df.set_index("Date")["attendance_percent"]
)


# --------------------------------------------------
# Subject Attendance
# --------------------------------------------------

st.subheader("Subject Attendance")

st.bar_chart(
    subject_df.set_index("Subject Code")["attendance_percent"]
)


# --------------------------------------------------
# Low Attendance Students
# --------------------------------------------------

st.subheader("Students Below 75% Attendance")

low_attendance = student_df[
    student_df["attendance_percent"] < 75
]

st.dataframe(low_attendance)


# --------------------------------------------------
# Download Student Report
# --------------------------------------------------

st.subheader("Download Student Attendance Report")

csv = student_df.to_csv(index=False)

st.download_button(
    label="Download Report",
    data=csv,
    file_name="student_attendance_summary.csv",
    mime="text/csv"
)