from pathlib import Path
import pandas as pd

ATTENDANCE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw_attendance"
print(ATTENDANCE_DIR)
def get_attendance_filepath(meta):

    lecture_date_str = meta["date"].strftime("%Y-%m-%d")
    lecture_time_str = meta["time"].strftime("%H-%M")

    subject = meta["subject_code"]
    batch = meta["batch"]

    filename = f"{lecture_date_str}_{subject}_{batch}_{lecture_time_str}.csv"

    return ATTENDANCE_DIR / filename


def load_existing_attendance(meta):

    filepath = get_attendance_filepath(meta)

    if filepath.exists():
        return pd.read_csv(filepath)

    return None