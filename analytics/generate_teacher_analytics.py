from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_ATTENDANCE = BASE_DIR / "data" / "processed" / "master_attendance.csv"
SUBJECT_MASTER = BASE_DIR / "data" / "master_data" / "subjects_master.csv"

OUTPUT_DIR = BASE_DIR / "data" / "analytics_data" / "teacher"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

attendance_df = pd.read_csv(MASTER_ATTENDANCE)
subject_df = pd.read_csv(SUBJECT_MASTER)

# --------------------------------------------------
# Merge Teacher Info
# --------------------------------------------------

df = attendance_df.merge(
    subject_df,
    on="Subject Code",
    how="left"
)

# Convert Present column to numeric
df["Present"] = df["Present"].astype(int)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# Teacher Subject Summary
# --------------------------------------------------

teacher_subject = (
    df.groupby(["Teacher", "Subject Code"])
    .agg(
        total_classes=("Present", "count"),
        total_present=("Present", "sum")
    )
    .reset_index()
)

teacher_subject["attendance_percent"] = (
    teacher_subject["total_present"]
    / teacher_subject["total_classes"]
    * 100
).round(2)

teacher_subject.to_csv(
    OUTPUT_DIR / "teacher_subject_summary.csv",
    index=False
)

# --------------------------------------------------
# Teacher Student Summary
# --------------------------------------------------

teacher_student = (
    df.groupby(["Teacher", "PRN"])
    .agg(
        total_classes=("Present", "count"),
        total_present=("Present", "sum")
    )
    .reset_index()
)

teacher_student["attendance_percent"] = (
    teacher_student["total_present"]
    / teacher_student["total_classes"]
    * 100
).round(2)

teacher_student.to_csv(
    OUTPUT_DIR / "teacher_student_summary.csv",
    index=False
)

# --------------------------------------------------
# Teacher Daily Trend
# --------------------------------------------------

teacher_daily = (
    df.groupby(["Teacher", "Date"])
    .agg(
        total_classes=("Present", "count"),
        total_present=("Present", "sum")
    )
    .reset_index()
)

teacher_daily["attendance_percent"] = (
    teacher_daily["total_present"]
    / teacher_daily["total_classes"]
    * 100
).round(2)

teacher_daily.to_csv(
    OUTPUT_DIR / "teacher_daily_trend.csv",
    index=False
)

print("Teacher analytics generated successfully.")