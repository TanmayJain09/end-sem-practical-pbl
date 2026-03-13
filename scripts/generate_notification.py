import pandas as pd
import json
from pathlib import Path

#defining file directories

MASTER_ATT_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "master_attendance.csv"
STUDENT_MASTER_FILE = Path(__file__).resolve().parent.parent / "data" / "master_data" / "students_master.csv"
RULES_FILE = Path(__file__).resolve().parent.parent / "config" / "attendance_rules.json"

NOTIFICATION_FILE = Path(__file__).resolve().parent.parent / "data" / "derived" / "notification_status.csv"
SUBJECT_SUMMARY_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "subject_attendance_summary.csv"