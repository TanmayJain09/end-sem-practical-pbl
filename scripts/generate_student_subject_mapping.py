#import libraries
import pandas as pd
from pathlib import Path

#Base Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

MASTER_DIR = DATA_DIR / "master_data"
PROCESSED_DIR = DATA_DIR / "processed"

students_file = MASTER_DIR / "students_master.csv"
subjects_file = MASTER_DIR / "subjects_master.csv"
output_file = PROCESSED_DIR / "student_subject_mapping.csv"

#Load Master Data
students = pd.read_csv(students_file)
subjects = pd.read_csv(subjects_file)

#Cross join(student * subject)
students["key"] = 1
subjects["key"] = 1

mapping = pd.merge(students,subjects,on="key").drop("key",axis=1)

#Saving csv
mapping.to_csv(output_file,index=False)

print("student_subject_mapping.csv generated")