# controller.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
PORTAL_APP = PROJECT_ROOT / "attendance_portal" / "app.py"

# Map buttons to scripts
SCRIPT_MAP = {
    "Open Teacher Input Portal": "streamlit",  # special handling
    "Build Master Attendance": SCRIPTS_DIR / "build_master_attendance.py",
    "Generate Notifications": SCRIPTS_DIR / "generate_notification.py",
    "Send Emails": SCRIPTS_DIR / "mail_warning.py",
}

def run_script(key):
    """Run a script or streamlit app."""
    try:
        if key == "Open Teacher Input Portal":
            # Run streamlit app
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(PORTAL_APP)])
            messagebox.showinfo("Info", "Teacher Input Portal launched in your browser!")
        else:
            script_path = SCRIPT_MAP[key]
            result = subprocess.run([sys.executable, str(script_path)],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"{script_path.name} ran successfully!")
            else:
                messagebox.showerror("Error", f"Error in {script_path.name}:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Exception", str(e))

# Create main window
root = tk.Tk()
root.title("Attendance System Controller")
root.geometry("450x250")

tk.Label(root, text="Attendance System Controller", font=("Arial", 16)).pack(pady=10)

# Buttons
for label in SCRIPT_MAP.keys():
    tk.Button(root, text=label, width=35, height=2, command=lambda l=label: run_script(l)).pack(pady=5)

root.mainloop()