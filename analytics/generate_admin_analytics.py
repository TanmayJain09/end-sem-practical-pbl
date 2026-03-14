from pathlib import Path
import pandas as pd

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_FILE = BASE_DIR / "data" / "processed" / "master_attendance.csv"

OUTPUT_DIR = BASE_DIR / "data" / "analytics_data" / "admin"

# create folder if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# Load Master Attendance
# ---------------------------------------------------

def load_master_attendance():
    df = pd.read_csv(MASTER_FILE)
    return df


# ---------------------------------------------------
# Generate Overall Summary
# ---------------------------------------------------

def generate_overall_summary(df):

    total_students = df["PRN"].nunique()

    total_records = len(df)

    total_present = df["Present"].sum()

    total_absent = total_records - total_present

    attendance_percent = (total_present / total_records) * 100

    summary_df = pd.DataFrame([{
        "total_students": total_students,
        "total_records": total_records,
        "total_present": int(total_present),
        "total_absent": int(total_absent),
        "attendance_percent": round(attendance_percent, 2)
    }])

    output_file = OUTPUT_DIR / "overall_summary.csv"

    summary_df.to_csv(output_file, index=False)

    print(f"Generated: {output_file}")

# ---------------------------------------------------
# Generate Subject Attendance
# ---------------------------------------------------

def generate_subject_attendance(df):

    subject_df = df.groupby("Subject Code").agg(
        total_records=("Present", "count"),
        total_present=("Present", "sum")
    ).reset_index()

    subject_df["total_absent"] = subject_df["total_records"] - subject_df["total_present"]

    subject_df["attendance_percent"] = (
        subject_df["total_present"] / subject_df["total_records"] * 100
    ).round(2)

    output_file = OUTPUT_DIR / "subject_attendance.csv"

    subject_df.to_csv(output_file, index=False)

    print(f"Generated: {output_file}")

# ---------------------------------------------------
# Generate Student Summary
# ---------------------------------------------------

def generate_student_summary(df):

    student_df = df.groupby(["PRN", "Name"]).agg(
        total_classes=("Present", "count"),
        total_present=("Present", "sum")
    ).reset_index()

    student_df["total_absent"] = student_df["total_classes"] - student_df["total_present"]

    student_df["attendance_percent"] = (
        student_df["total_present"] / student_df["total_classes"] * 100
    ).round(2)

    output_file = OUTPUT_DIR / "student_attendance_summary.csv"

    student_df.to_csv(output_file, index=False)

    print(f"Generated: {output_file}")

# ---------------------------------------------------
# Generate Daily Trend
# ---------------------------------------------------

def generate_daily_trend(df):

    daily_df = df.groupby("Date").agg(
        total_records=("Present", "count"),
        total_present=("Present", "sum")
    ).reset_index()

    daily_df["attendance_percent"] = (
        daily_df["total_present"] / daily_df["total_records"] * 100
    ).round(2)

    output_file = OUTPUT_DIR / "daily_attendance_trend.csv"

    daily_df.to_csv(output_file, index=False)

    print(f"Generated: {output_file}")

# ---------------------------------------------------
# Main Pipeline
# ---------------------------------------------------

def main():

    print("Loading master attendance...")

    df = load_master_attendance()

    print("Generating admin analytics...")

    generate_overall_summary(df)

    generate_subject_attendance(df)

    generate_student_summary(df)

    generate_daily_trend(df)

    print("Admin analytics generation complete.")

if __name__ == "__main__":
    main()