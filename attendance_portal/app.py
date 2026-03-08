import streamlit as st
from datetime import date, datetime
from utils.validator import check_duplicate_attendance
from utils.data_loader import load_subjects, get_subjects_by_teacher, get_all_teachers

# --- Load subjects ---
subjects_df = load_subjects()

# --- Title ---
st.title("Teacher Attendance Portal")
st.markdown("---")  # Horizontal line for separation

# --- Teacher selection ---
teacher_col = st.container()
with teacher_col:
    teacher_name = st.selectbox(
        "Your Name:",
        get_all_teachers(subjects_df)
    )

# --- Subject selection ---
subject_col = st.container()
with subject_col:
    teacher_subjects_df = get_subjects_by_teacher(subjects_df, teacher_name)
    
    subject_option = st.selectbox(
        "Select Subject:",
        options=teacher_subjects_df["Subject"].tolist()
    )

    # Get corresponding Subject Code
    subject_code = teacher_subjects_df[
        teacher_subjects_df["Subject"] == subject_option
    ]["Subject Code"].values[0]
    
    st.info(f"Selected Subject Code: **{subject_code}**")

# --- Batch selection ---
batch_col = st.container()
with batch_col:
    batch_options = ["D1", "D2", "BOTH"]
    selected_batch = st.selectbox("Select Batch:", batch_options)

# --- Date and Time selection in two columns ---
date_col, time_col = st.columns(2)
with date_col:
    selected_date = st.date_input("Select Lecture Date:", date.today())
with time_col:
    selected_time = st.time_input("Select Lecture Time:", datetime.now().time())

st.markdown("---")  # Another separator

# --- Check for duplicated lecture ---
if check_duplicate_attendance(subject_code, selected_batch, selected_date, selected_time):
    st.warning("Attendance for this lecture already exists! You cannot generate again.")
    generate_button = st.button("Generate Table", disabled=True)
else:
    generate_button = st.button("Generate Table")