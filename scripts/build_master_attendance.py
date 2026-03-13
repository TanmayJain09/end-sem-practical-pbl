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

print(RAW_ATTENDANCE_DIR)