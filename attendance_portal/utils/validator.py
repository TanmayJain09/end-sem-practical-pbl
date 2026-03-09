from pathlib import Path

ATTENDANCE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw_attendance"

def check_duplicate_attendance(subject, batch, lecture_date, lecture_time):
    """
    Returns True if an attendance file already exists for the same lecture
    """
    lecture_date_str = lecture_date.strftime("%Y-%m-%d")
    lecture_time_str = lecture_time.strftime("%H-%M")  # replace colon to avoid filename issues

    # Pattern: YYYY-MM-DD_Subject_Batch_HH-MM.csv
    file_path = ATTENDANCE_DIR / f"{lecture_date_str}_{subject}_{batch}_{lecture_time_str}.csv"
    return file_path.exists()