import pandas as pd
from pathlib import Path

#define paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "master_data"

STUDENTS_FILE = DATA_DIR / "students_master.csv"
SUBJECTS_FILE = DATA_DIR / "subjects_master.csv"

def load_students() : 
    """Load students_master.csv and return DataFrame"""
    df = pd.read_csv(STUDENTS_FILE)
    
    #basic data validation
    if df.duplicated(subset="PRN").any() : 
        raise ValueError("Duplicate PRN found in students_master.csv")
    if df.isnull().any().any() : 
        raise ValueError("Missing values found in students_master.csv")
    return df
    
def load_subjects() : 
    """Load subjects_master.csv and return DataFrame"""
    df = pd.read_csv(SUBJECTS_FILE)
    # Basic validation
    if df.duplicated(subset="Subject Code").any():
        raise ValueError("Duplicate Subject Code found in subjects_master.csv")
    if df.isnull().any().any():
        raise ValueError("Missing values found in subjects_master.csv")
    return df

def get_subjects_by_teacher(subjects_df, teacher_name):
    """Filter subjects assigned to a particular teacher"""
    return subjects_df[subjects_df["Teacher"] == teacher_name]

def get_students_by_batch(students_df, batch_name):
    """Filter students belonging to a batch"""
    return students_df[students_df["Batch"] == batch_name]    

def get_students_for_lecture(students_df, lecture_batch):
    """
    Returns students who should attend a lecture.
    lecture_batch: 'D1', 'D2', or 'BOTH'
    """
    if lecture_batch.upper() == "BOTH":
        return students_df
    else:
        return students_df[students_df["Batch"] == lecture_batch]