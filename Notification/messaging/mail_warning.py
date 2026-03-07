#importing library
import pandas as pd
import smtplib, ssl
from email.message import EmailMessage
from pathlib import Path

#path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CSV_FILE = PROCESSED_DIR / "critical_contacts.csv"

#reading csv
df = pd.read_csv(CSV_FILE)


#email credentials
EMAIL_ADDRESS = "purposeschool619@gmail.com"
EMAIL_PASSWORD = "nokgtfpcprbmuybe"  # Use Gmail App Password

#smtp settings
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # For SSL

#function to send email
def send_email(to_email, subject, body) :
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server : 
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Email sent to {to_email}")

#loop over critical students
for idx, row in df.iterrows() : 
    student_name = row["Name"]
    attendance = round(row["Net_Attendance_Percentage"],2)
    lectures_attended = row["Lectures_Attended"]
    total_lectures = row["Total_Lectures_Batch"]
    to_email = row["email"]

    #draft body
    subject = "Attendance Warning Notification"
    body = f"""Dear {student_name},

Your attendance is currently {attendance}%.
Lectures Attended: {lectures_attended}
Total Lectures: {total_lectures}

This is a warning. Please improve your attendance immediately.

Regards,
Attendance Monitoring System
"""

    #send email
    send_email(to_email,subject,body)    