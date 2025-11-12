import json
from pathlib import Path

def load_json(filename):
    """
    Loads and returns the contents of a JSON file from the data directory.

    Args:
        filename (str or Path): Name of the JSON file (e.g. "config.json") or a full path.

    Returns:
        dict or list: Parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contents are not valid JSON.
    """
    data_dir = Path(__file__).resolve().parents[2] / "data"
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
