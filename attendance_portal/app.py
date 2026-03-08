from utils.data_loader import load_students,load_subjects,get_subjects_by_teacher,get_students_by_batch
 
#load master data
students_df = load_students()
subjects_df = load_subjects()

print("All Students:")
print(students_df.head())

print("\nAll Subjects")
print(subjects_df)

# Example: Subjects for Teacher 1
teacher_subjects = get_subjects_by_teacher(subjects_df, "Teacher 1")
print("\nTeacher 1 Subjects:")
print(teacher_subjects)

# Example: Students in batch D1
batch_students = get_students_by_batch(students_df, "D1")
print("\nBatch D1 Students:")
print(batch_students)