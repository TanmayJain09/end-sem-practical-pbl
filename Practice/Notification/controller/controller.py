import subprocess
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_notebook():
    """Runs the merge_contacts.ipynb to generate critical_contacts.csv"""
    notebook_path = PROJECT_ROOT / "notebooks" / "merge_contacts.ipynb"
    print(f"Running notebook : {notebook_path}")
    try :
        subprocess.run(
            [
                "jupyter", "nbconvert", "--to", "notebook", "--execute",
                str(notebook_path), "--inplace"
            ],
            check= True
        )
        print("Notebook executed successfully")
    except subprocess.CalledProcessError as e : 
        print(f"Failed to run : {e}")

def run_mail():
    """Runs the mail_warning.py script"""
    mail_path = PROJECT_ROOT / "messaging" / "mail_warning.py"
    print(f"Running mail module: {mail_path}")
    try:
        subprocess.run([sys.executable, str(mail_path)], check=True)
        print("Mail module executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run mail module: {e}")

def main():
    while True:
        print("=== Attendance Alert System Controller ===")
        print("Select an option:")
        print("1. Run merge_contacts.ipynb")
        print("2. Run mail_warning.py")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            run_notebook()
        elif choice == "2":
            run_mail()
        elif choice == "3":
            print("Exiting controller...")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()