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
# Main Pipeline
# ---------------------------------------------------

def main():

    print("Loading master attendance...")

    df = load_master_attendance()

    print("Generating admin analytics...")

    generate_overall_summary(df)

    print("Admin analytics generation complete.")


if __name__ == "__main__":
    main()