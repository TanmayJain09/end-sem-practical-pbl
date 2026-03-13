from pathlib import Path
import pandas as pd

from scripts.hash_utils import compute_file_hash
from scripts.registry_manager import (
    load_registry,
    save_registry,
    get_stored_hash
)
from scripts.file_parser import parse_attendance_filename

RAW_ATTENDANCE_DIR = Path("data/raw_attendance")
print(RAW_ATTENDANCE_DIR)