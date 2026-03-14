from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_FILE = BASE_DIR / "data" / "processed" / "master_attendance.csv"

OUTPUT_DIR = BASE_DIR / "data" / "analytics_data" / "teacher"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Master Attendance
# --------------------------------------------------

df = pd.read_csv(MASTER_FILE)

# Ensure Date column is datetime
df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# Teacher Subject Summary
# --------------------------------------------------

teacher_subject = (
    df.groupby(["Teacher", "Subject Code"])
    .agg(
        total_classes=("Attendance", "count"),
        total_present=("Attendance", "sum")
    )
    .reset_index()
)

teacher_subject["attendance_percent"] = (
    teacher_subject["total_present"] /
    teacher_subject["total_classes"] * 100
).round(2)

teacher_subject.to_csv(
    OUTPUT_DIR / "teacher_subject_summary.csv",
    index=False
)

# --------------------------------------------------
# Teacher Student Summary
# --------------------------------------------------

teacher_student = (
    df.groupby(["Teacher", "Student ID"])
    .agg(
        total_classes=("Attendance", "count"),
        total_present=("Attendance", "sum")
    )
    .reset_index()
)

teacher_student["attendance_percent"] = (
    teacher_student["total_present"] /
    teacher_student["total_classes"] * 100
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
        total_classes=("Attendance", "count"),
        total_present=("Attendance", "sum")
    )
    .reset_index()
)

teacher_daily["attendance_percent"] = (
    teacher_daily["total_present"] /
    teacher_daily["total_classes"] * 100
).round(2)

teacher_daily.to_csv(
    OUTPUT_DIR / "teacher_daily_trend.csv",
    index=False
)

print("Teacher analytics generated successfully.")