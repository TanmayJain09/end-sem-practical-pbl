import streamlit as st
from utils.data_loader import load_subjects,get_subjects_by_teacher,get_all_teachers

#loading subjects
subject_df = load_subjects()

#---teacher selection---
st.title("Teacher Attendance Portal")
teacher_name = st.selectbox("Your Name : ",get_all_teachers(subject_df))

#show subject for the selected teacher
teacher_subjects_df = get_subjects_by_teacher(subject_df,teacher_name)
subject_options = teacher_subjects_df["Subject"].tolist()

st.write(f"You are teaching: {', '.join(subject_options)}")