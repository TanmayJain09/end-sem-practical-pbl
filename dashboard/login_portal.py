import streamlit as st
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Attendance System Login",
    layout="centered"
)

st.title("Attendance Monitoring System")

st.write("Select Login Type")

# --------------------------------------------------
# Login Selection
# --------------------------------------------------

login_type = st.selectbox(
    "Login As",
    ["Admin", "Teacher", "Student"]
)

# --------------------------------------------------
# Login Button
# --------------------------------------------------

if st.button("Enter Dashboard"):

    base_dir = Path(__file__).resolve().parent

    if login_type == "Admin":

        dashboard_path = base_dir / "admin_dashboard.py"

        subprocess.Popen(
            ["streamlit", "run", str(dashboard_path)]
        )

        st.success("Opening Admin Dashboard...")

    elif login_type == "Teacher":

        st.warning("Teacher dashboard not implemented yet.")

    elif login_type == "Student":

        st.warning("Student dashboard not implemented yet.")