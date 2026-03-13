from pathlib import Path
import pandas as pd

from scripts.hash_utils import compute_file_hash
from scripts.registry_manager import (
    load_registry,
    save_registry,
    get_file_hash
)
from scripts.file_parser import parse_attendance_filename

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_ATTENDANCE_DIR = DATA_DIR / "raw_attendance"
PROCESSED_DIR = DATA_DIR / "processed"
MASTER_FILE = PROCESSED_DIR / "master_attendance.csv"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def get_attendance_files() :
    """
    Return list of all attendance CSV files.
    """

    return list(RAW_ATTENDANCE_DIR.glob("*.csv")) 

def detect_changed_files(files,registry) : 
    """
    Detect new or modified attendance files.
    """

    changed_files=[]

    for file in files : 
        
        current_hash = compute_file_hash(file)
        stored_hash = get_file_hash(registry,file)

        if stored_hash is None : 
            print(f"NEW FILE : {file.name}")
            changed_files.append((file,current_hash))
        
        elif stored_hash != current_hash : 
            print(f"MODIFIED : {file.name}")
            changed_files.append((file,current_hash))
        
    return changed_files

def load_master():
    """
    Load master attendance file if it exists.
    """

    if MASTER_FILE.exists():
        return pd.read_csv(MASTER_FILE)

    return pd.DataFrame()