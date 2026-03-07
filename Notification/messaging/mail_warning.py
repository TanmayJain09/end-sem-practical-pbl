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