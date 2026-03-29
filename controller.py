import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
ANALYTICS_DIR = PROJECT_ROOT / "analytics"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

PORTAL_APP = PROJECT_ROOT / "attendance_portal" / "app.py"
LOGIN_PORTAL = DASHBOARD_DIR / "login_portal.py"

BUILD_MASTER = SCRIPTS_DIR / "build_master_attendance.py"
GENERATE_NOTIFICATION = SCRIPTS_DIR / "generate_notification.py"
MAIL_WARNING = SCRIPTS_DIR / "mail_warning.py"

ADMIN_ANALYTICS = ANALYTICS_DIR / "generate_admin_analytics.py"
TEACHER_ANALYTICS = ANALYTICS_DIR / "generate_teacher_analytics.py"


def run_python_script(script_path):
    module_path = script_path.with_suffix("").relative_to(PROJECT_ROOT)
    module_name = ".".join(module_path.parts)

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)


# --------------------------------------------------
# Button Functions
# --------------------------------------------------

def open_teacher_portal():
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", str(PORTAL_APP)
    ])
    messagebox.showinfo("Portal", "Teacher Input Portal opened in browser.")


def build_master_attendance():
    try:
        run_python_script(BUILD_MASTER)
        messagebox.showinfo("Success", "Master attendance built successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def generate_notifications():
    try:
        run_python_script(GENERATE_NOTIFICATION)
        run_python_script(MAIL_WARNING)
        messagebox.showinfo("Success", "Notifications generated and emails sent.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_dashboard():
    try:
        # Run analytics first
        run_python_script(ADMIN_ANALYTICS)
        run_python_script(TEACHER_ANALYTICS)

        # Launch dashboard portal
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", str(LOGIN_PORTAL)
        ])

        messagebox.showinfo(
            "Dashboard",
            "Analytics generated.\nDashboard portal opened."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------------------------------------------
# UI
# --------------------------------------------------

root = tk.Tk()
root.title("Attendance System Controller")
root.geometry("420x320")
root.configure(bg="#f4f6f7")

title = tk.Label(
    root,
    text="Attendance System Controller",
    font=("Arial", 16, "bold"),
    bg="#f4f6f7"
)
title.pack(pady=15)

button_style = {
    "width": 32,
    "height": 2,
    "font": ("Arial", 10)
}

tk.Button(
    root,
    text="1. Open Teacher Input Portal",
    command=open_teacher_portal,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="2. Build Master Attendance",
    command=build_master_attendance,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="3. Generate Notifications (Emails)",
    command=generate_notifications,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="4. Open Analytics Dashboard",
    command=open_dashboard,
    **button_style
).pack(pady=5)

footer = tk.Label(
    root,
    text="End Semester Project",
    font=("Arial", 9),
    bg="#f4f6f7"
)
footer.pack(pady=10)

root.mainloop()