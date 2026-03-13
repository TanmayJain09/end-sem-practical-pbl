import hashlib
from pathlib import Path

def compute_file_hash(file_path : Path) -> str :
    """
    Compute SHA256 hash of a file.

    Parameters
    ----------
    file_path : Path
        Path to the file whose hash should be calculated.

    Returns
    -------
    str
        Hexadecimal SHA256 hash string representing file content.
    """

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)
    
    return sha256.hexdigest()