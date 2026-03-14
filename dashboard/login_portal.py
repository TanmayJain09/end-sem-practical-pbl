import streamlit as st
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Attendance System", layout="centered")

st.title("Attendance Analytics Portal")
st.write("Select a role to open the dashboard")

role = st.selectbox(
    "Choose Role",
    ["Admin", "Teacher", "Student"]
)

if st.button("Open Dashboard"):

    if role == "Admin":
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            str(BASE_DIR / "admin_dashboard.py")
        ])

    elif role == "Teacher":
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            str(BASE_DIR / "teacher_dashboard.py")
        ])

    elif role == "Student":
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            str(BASE_DIR / "student_dashboard.py")
        ])

    st.success("Dashboard launched in a new tab.")