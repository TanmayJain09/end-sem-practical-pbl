import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils.validator import check_duplicate_attendance
from utils.csv_writer import save_attendance_csv
from utils.data_loader import (
    load_students,
    load_subjects,
    get_subjects_by_teacher,
    get_all_teachers,
    get_students_for_lecture
)

# --- Load data ---
subjects_df = load_subjects()
students_df = load_students()

# --- Session state initialization ---
if "attendance_table" not in st.session_state:
    st.session_state.attendance_table = None

if "lecture_meta" not in st.session_state:
    st.session_state.lecture_meta = None


# --- Title ---
st.title("Teacher Attendance Portal")
st.markdown("---")


# -----------------------------------
# Lecture configuration FORM
# -----------------------------------
# Teacher selector OUTSIDE form
teacher_name = st.selectbox(
    "Your Name:",
    get_all_teachers(subjects_df)
)

teacher_subjects_df = get_subjects_by_teacher(subjects_df, teacher_name)

# Form starts here
with st.form("lecture_form"):

    subject_option = st.selectbox(
        "Select Subject:",
        teacher_subjects_df["Subject"].tolist()
    )

    subject_code = teacher_subjects_df[
        teacher_subjects_df["Subject"] == subject_option
    ]["Subject Code"].values[0]

    st.info(f"Selected Subject Code: **{subject_code}**")

    batch_options = ["D1", "D2", "BOTH"]
    selected_batch = st.selectbox("Select Batch:", batch_options)

    date_col, time_col = st.columns(2)

    with date_col:
        selected_date = st.date_input("Select Lecture Date:", date.today())

    with time_col:
        selected_time = st.time_input("Select Lecture Time:", datetime.now().time())

    # Duplicate check
    if check_duplicate_attendance(subject_code, selected_batch, selected_date, selected_time):
        st.warning("Attendance for this lecture already exists!")
        generate_button = st.form_submit_button("Generate Table", disabled=True)
    else:
        generate_button = st.form_submit_button("Generate Table")


# -----------------------------------
# Generate attendance table
# -----------------------------------
if generate_button:

    lecture_students = get_students_for_lecture(students_df, selected_batch)

    table = lecture_students[["PRN", "Name"]].copy()
    table["Present"] = True

    st.session_state.attendance_table = table

    st.session_state.lecture_meta = {
        "teacher": teacher_name,
        "subject_code": subject_code,
        "batch": selected_batch,
        "date": selected_date,
        "time": selected_time
    }


# -----------------------------------
# Display attendance table
# -----------------------------------
if st.session_state.attendance_table is not None:

    meta = st.session_state.lecture_meta

    st.subheader("Mark Attendance")

    st.markdown(f"""
    **Teacher:** {meta['teacher']}  
    **Subject Code:** {meta['subject_code']}  
    **Batch:** {meta['batch']}  
    **Date:** {meta['date']}  
    **Time:** {meta['time'].strftime('%H:%M')}
    """)

    col1, col2 = st.columns(2)

    # Mark all present
    with col1:
        if st.button("Mark All Present"):
            st.session_state.attendance_table["Present"] = True

    # Mark all absent
    with col2:
        if st.button("Mark All Absent"):
            st.session_state.attendance_table["Present"] = False

    # Attendance editor (IMPORTANT: widget manages its own state)
    st.data_editor(
        st.session_state.attendance_table,
        use_container_width=True,
        num_rows="fixed",
        key="attendance_editor"
    )

    st.markdown("---")

    # -----------------------------------
    # Upload attendance
    # -----------------------------------
    if st.button("Upload Attendance"):

        attendance_df = st.session_state.attendance_table
        meta = st.session_state.lecture_meta

        filepath = save_attendance_csv(attendance_df, meta)

        st.success(f"Attendance saved successfully: {filepath}")