import pandas as pd
from email.message import EmailMessage
import smtplib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

# ------------------------
# Load environment variables (email credentials)
# ------------------------
load_dotenv(Path(__file__).resolve().parent.parent / "config" / ".env")

SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ------------------------
# File paths
# ------------------------
NOTIFICATION_FILE = Path(__file__).resolve().parent.parent / "data/derived/notification_status.csv"
SUBJECT_SUMMARY_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "subject_attendance_summary.csv"
LOG_FILE = Path(__file__).resolve().parent.parent / "logs/email_log.csv"

# Ensure logs folder exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# ------------------------
# Load data
# ------------------------
notification_df = pd.read_csv(NOTIFICATION_FILE)
subject_summary_df = pd.read_csv(SUBJECT_SUMMARY_FILE)

# ------------------------
# Gravity message mapping
# ------------------------
gravity_messages = {
    "Warning": "Your attendance is low. Please take care.",
    "Alert": "Your attendance is below acceptable limits. Immediate action needed.",
    "Critical": "Your attendance is critically low! Immediate improvement required."
}

# ------------------------
# Loop over each student and send email
# ------------------------
for _, student in notification_df.iterrows():
    prn = student['PRN']
    name = student['Name']
    overall = student['Attendance %']
    status = student['Status']
    student_email = student['Email']

    # Prepare subject-wise attendance table
    subjects = subject_summary_df[subject_summary_df['PRN'] == prn][['Subject Code', 'Attendance %']]
    subject_table = "\n".join([f"{row['Subject Code']}: {row['Attendance %']}%" for _, row in subjects.iterrows()])

    # Prepare notice based on status
    notice = gravity_messages.get(status, "")

    # Email body
    email_body = f"""Dear {name},

Your current overall attendance is {overall}% ({status}).

{notice}

Here is your subject-wise attendance:
{subject_table}

Best regards,
Attendance Portal
"""

    # Prepare log row
    log_row = {
        "PRN": prn,
        "Name": name,
        "Email": student_email,
        "Status": "",
        "Timestamp": datetime.now(),
        "Error_Message": ""
    }

    # Send email
    try:
        msg = EmailMessage()
        msg['From'] = SENDER_EMAIL
        msg['To'] = student_email
        msg['Subject'] = "Attendance Alert"
        msg.set_content(email_body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        log_row['Status'] = "Success"

    except Exception as e:
        log_row['Status'] = "Failed"
        log_row['Error_Message'] = str(e)

    # Append to log CSV
    log_df = pd.DataFrame([log_row])
    if LOG_FILE.exists():
        log_df.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        log_df.to_csv(LOG_FILE, index=False)

print(f"Emails processed. Check log at: {LOG_FILE}")