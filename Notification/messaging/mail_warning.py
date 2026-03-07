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