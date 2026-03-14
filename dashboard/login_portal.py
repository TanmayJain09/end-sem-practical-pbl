import streamlit as st
import subprocess
import sys

st.set_page_config(
    page_title="Attendance System Login",
    layout="centered"
)

st.title("Attendance Management System")

st.subheader("Login")

# -----------------------------
# Role Selection
# -----------------------------

role = st.selectbox(
    "Select Role",
    ["Admin", "Teacher", "Student"]
)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# -----------------------------
# Login Button
# -----------------------------

if st.button("Login"):

    if role == "Admin":
        st.success("Opening Admin Dashboard...")

        subprocess.Popen(
            ["streamlit", "run", "dashboards/admin_dashboard.py"]
        )

    elif role == "Teacher":
        st.success("Opening Teacher Dashboard...")

        subprocess.Popen(
            ["streamlit", "run", "dashboards/teacher_dashboard.py"]
        )

    elif role == "Student":
        st.success("Opening Student Dashboard...")

        subprocess.Popen(
            ["streamlit", "run", "dashboards/student_dashboard.py"]
        )