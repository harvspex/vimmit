from pathlib import Path
import json

def load_collection(filepath: Path) -> dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}