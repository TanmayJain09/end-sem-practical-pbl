from pathlib import Path

def parse_attendance_filename(file_path: Path) -> dict:
    """
    Parse attendance CSV filename and extract metadata.

    Expected format:
    YYYY-MM-DD_SUBJECTCODE_BATCH_HH-MM.csv

    Example:
    2026-03-10_AI0201_D1_23-50.csv

    Returns
    -------
    dict
        Dictionary containing parsed metadata.
    """

    filename = file_path.stem #remove.csv
    parts = filename.split("_")

    if len(parts) != 4 : 
        raise ValueError(f"Invalid filename format: {file_path.name}")

    date = parts[0]
    subject_code = parts[1]
    batch = parts[2]
    time = parts[3].replace("-",":")

    return{
        "Date" : date,
        "Time" : time,
        "Subject Code" : subject_code,
        "Batch" : batch,
        "Source File" : file_path.name
    }