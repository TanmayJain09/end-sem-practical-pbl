import json
from pathlib import Path

#Path to the registry file
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "registry" / "file_hash_registry.json"

def load_registry() -> dict :
    """
    Load the hash registry from JSON file.

    Returns
    -------
    dict
        Dictionary mapping filename → stored hash.
    """

    if not REGISTRY_PATH.exists() : 
        return { }
    
    with open(REGISTRY_PATH,"r",encoding="utf-8") as f :
        return json.load(f)

def save_registry(registry: dict) -> None:
    """
    Save the updated registry to JSON file.

    Parameters
    ----------
    registry : dict
        Dictionary containing filename → hash mapping.
    """

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
    
def get_file_hash(registry: dict, filename: str) -> str | None:
    """
    Get stored hash for a file from registry.

    Parameters
    ----------
    registry : dict
        Current registry dictionary.
    filename : str
        CSV filename.

    Returns
    -------
    str | None
        Stored hash if file exists in registry, else None.
    """

    return registry.get(filename)