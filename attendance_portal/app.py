import streamlit as st
from datetime import date,time, datetime
from utils.validator import check_duplicate_attendance
from utils.data_loader import load_subjects,get_subjects_by_teacher,get_all_teachers

#loading subjects
subject_df = load_subjects()

#---teacher selection---
teacher_name = st.selectbox("Your Name : ",get_all_teachers(subject_df))

#--- subject selection---
teacher_subjects_df = get_subjects_by_teacher(subject_df,teacher_name)

#dropdown showing subject name but storing subject code
subject_option = st.selectbox(
    "Select Subject:",
    options=teacher_subjects_df["Subject"].tolist(),  # Display names
    format_func=lambda x: x  # Display the name itself
)

# Get corresponding Subject Code
subject_code = teacher_subjects_df[teacher_subjects_df["Subject"] == subject_option]["Subject Code"].values[0]

st.write(f"Selected Subject Code: {subject_code}")

#---batch selection ---
batch_options = ["D1","D2","BOTH"]
selected_batch = st.selectbox("Select Batch: ",batch_options)

#---date and time selection---
selected_date = st.date_input("Select Lecture Date: ",date.today())
selected_time = st.time_input("Select Lecture Time: ",datetime.now().time())

#---Check for duplicated lecture---
if check_duplicate_attendance(subject_code,selected_batch,selected_date,selected_time) : 
    st.warning("Attendance for this lecture already exists! You cannot generate again.")
    generate_button = st.button("Generate Table", disabled=True)
else : 
    generate_button = st.button("Generate Table")