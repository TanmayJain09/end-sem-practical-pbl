import pandas as pd
import smtplib, ssl
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime
import csv

# ------------------------------
# Paths
# ------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = PROCESSED_DIR / "critical_contacts.csv"
LOG_FILE = LOG_DIR / "message_log.csv"

# ------------------------------
# Email credentials
# ------------------------------
EMAIL_ADDRESS = "purposeschool619@gmail.com"
EMAIL_PASSWORD = "nokgtfpcprbmuybe"  # Gmail App Password

SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # SSL

# ------------------------------
# Read critical contacts
# ------------------------------
df = pd.read_csv(CSV_FILE)

# ------------------------------
# Initialize log file if not exists
# ------------------------------
if not LOG_FILE.exists():
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "PRN", "Name", "Email", "Status"])

# ------------------------------
# Function to send email
# ------------------------------
def send_email(prn, to_email, name, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        status = "Sent"
        print(f"Email sent to {name} ({to_email})")
    except Exception as e:
        status = f"Failed: {e}"
        print(f"Failed to send email to {name} ({to_email}): {e}")

    # ------------------------------
    # Log the result
    # ------------------------------
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), prn, name, to_email, status])

# ------------------------------
# Loop over critical students
# ------------------------------
for idx, row in df.iterrows():
    prn = row["PRN"]
    student_name = row["Name"]
    attendance = round(row["Net_Attendance_Percentage"], 2)
    lectures_attended = row["Lectures_Attended"]
    total_lectures = row["Total_Lectures_Batch"]
    to_email = row["email"]

    subject = "Attendance Warning Notification"
    body = f"""Dear {student_name},

Your attendance is currently {attendance}%.
Lectures Attended: {lectures_attended}
Total Lectures: {total_lectures}

This is a warning. Please improve your attendance immediately.

Regards,
Attendance Monitoring System
"""
    send_email(prn, to_email, student_name, subject, body)