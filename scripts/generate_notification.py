import pandas as pd
import json
from pathlib import Path

#defining file directories

MASTER_ATT_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "master_attendance.csv"
STUDENT_MASTER_FILE = Path(__file__).resolve().parent.parent / "data" / "master_data" / "students_master.csv"
RULES_FILE = Path(__file__).resolve().parent.parent / "config" / "attendance_rules.json"

NOTIFICATION_FILE = Path(__file__).resolve().parent.parent / "data" / "derived" / "notification_status.csv"
SUBJECT_SUMMARY_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "subject_attendance_summary.csv"

#loading data
master_df = pd.read_csv(MASTER_ATT_FILE)
students_df = pd.read_csv(STUDENT_MASTER_FILE)
with open(RULES_FILE) as f : 
    rules = json.load(f)

# Ensure Present column is boolean
master_df['Present'] = master_df['Present'].astype(bool)

# ------------------------
# Helper function to classify attendance
# ------------------------
def classify_attendance(percentage, rules):
    if percentage >= rules["safe"]:
        return "Safe"
    elif percentage >= rules["warning"]:
        return "Warning"
    elif percentage >= rules["alert"]:
        return "Alert"
    else:
        return "Critical"
    
# ------------------------
# Step 1: Subject-wise attendance (batch-aware)
# ------------------------
subject_rows = []

for _, student in students_df.iterrows():
    prn = student['PRN']
    name = student['Name']
    student_batch = student['Batch']
    
    student_attendance = master_df[(master_df['PRN'] == prn) & 
                                   ((master_df['Batch'] == student_batch) | (master_df['Batch'] == "BOTH"))]
    
    for subject, group in student_attendance.groupby('Subject Code'):
        total_classes = len(group)
        classes_present = group['Present'].sum()
        attendance_pct = round((classes_present / total_classes) * 100, 2) if total_classes > 0 else 0.0
        
        subject_rows.append({
            "PRN": prn,
            "Name": name,
            "Subject Code": subject,
            "Total Classes": total_classes,
            "Classes Present": classes_present,
            "Attendance %": attendance_pct
        })

subject_summary_df = pd.DataFrame(subject_rows)
subject_summary_df.to_csv(SUBJECT_SUMMARY_FILE, index=False)

# ------------------------
# Step 2: Overall attendance (sum over all subjects)
# ------------------------
overall_rows = []

for prn, group in subject_summary_df.groupby('PRN'):
    name = group['Name'].iloc[0]
    total_classes = group['Total Classes'].sum()
    classes_present = group['Classes Present'].sum()
    overall_pct = round((classes_present / total_classes) * 100, 2) if total_classes > 0 else 0.0
    status = classify_attendance(overall_pct, rules)
    
    overall_rows.append({
        "PRN": prn,
        "Name": name,
        "Total Classes": total_classes,
        "Classes Present": classes_present,
        "Attendance %": overall_pct,
        "Status": status
    })

notification_df = pd.DataFrame(overall_rows)

# ------------------------
# Step 3: Merge emails
# ------------------------
notification_df = notification_df.merge(students_df[['PRN', 'Email']], on='PRN', how='left')

# ------------------------
# Step 4: Keep only Warning / Alert / Critical
# ------------------------
notification_df = notification_df[notification_df['Status'] != "Safe"]

# ------------------------
# Step 5: Save notification CSV
# ------------------------
notification_df.to_csv(NOTIFICATION_FILE, index=False)

print(f"Notification CSV saved: {NOTIFICATION_FILE}")
print(f"Subject-wise summary CSV saved: {SUBJECT_SUMMARY_FILE}")