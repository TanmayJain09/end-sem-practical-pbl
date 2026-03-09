from pathlib import Path
import pandas as pd

ATTENDANCE_DIR = Path(__file__).resolve().parent.parent / "data" / "raw_attendance"

def save_attendance_csv(df, lecture_meta):

    # Ensure dataframe type
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    lecture_date_str = lecture_meta["date"].strftime("%Y-%m-%d")
    lecture_time_str = lecture_meta["time"].strftime("%H-%M")

    subject = lecture_meta["subject_code"]
    batch = lecture_meta["batch"]

    filename = f"{lecture_date_str}_{subject}_{batch}_{lecture_time_str}.csv"

    # create directory if it doesn't exist
    ATTENDANCE_DIR.mkdir(parents=True, exist_ok=True)

    filepath = ATTENDANCE_DIR / filename

    df.to_csv(filepath, index=False)

    return filepath