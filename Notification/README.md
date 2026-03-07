# Attendance Alert — Notification Module

This module automates notifications for students with low attendance.  
Currently, it supports **email warnings** for students below defined attendance thresholds.  

---

## Folder Structure
attendance-alert-system/
│
├── notebooks/
│ ├── merge_contacts.ipynb # Merges Data for essential Work
│
├── messaging/
│ ├── mail_warning.py # Sends email warnings
│ ├── sms_warning.py # Placeholder for future SMS warnings
│ └── whatsapp_warning.py # Placeholder for future WhatsApp warnings
│
├── logs/
│ └── message_log.csv # Logs of notifications sent
│
├── data/processed/
│ └── critical_contacts.csv # Input data with students at risk
│
└── controller/
└── controller.py # Launches merge & notification scripts


---

## How It Works

1. **Creating Data**  
   - `critical_escalation_table.csv` contains students flagged for low attendance.
   - `contact_details.xlsx` contains student contact details
   - `merge_contact.ipynb` merges both the data as required and generated `critical_contact.csv` 

1. **Input Data**  
   - The generated `critical_contacts.csv` contains students flagged for low attendance.  
   - Key fields include: `PRN`, `Name`, `Email ID`, `Lectures_Attended`, `Total_Lectures_Batch`, `Net_Attendance_Percentage`.

2. **Email Notifications**  
   - `mail_warning.py` sends personalized emails with:  
     - Student name  
     - Attendance percentage  
     - Lectures attended vs total lectures  
     - Warning to improve attendance

3. **Logging**  
   - Each email is recorded in `logs/message_log.csv` with:  
     - Timestamp  
     - PRN  
     - Name  
     - Email  
     - Status (Sent / Failed)

4. **Controller Integration**  
   - `controller.py` allows running:  
     - `merge_contacts.ipynb` to generate critical contacts  
     - `mail_warning.py` to send emails  

---

## Setup & Usage

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure Email Credentials**

- Create a .env file in the project root:

```bash
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

- Add `.env` to `.gitignore` to keep credentials private.

3. **Run Email Notifications**

```bash
# Directly
python messaging/mail_warning.py

# Or via controller
python controller/controller.py
```

4. **Check Logs**

View `logs/message_log.csv` to see a record of all notifications sent.

# Notes
- Only email notifications are implemented; SMS and WhatsApp are placeholders for future updates.
- The system works with sample data for demonstration but can scale for full classroom datasets.