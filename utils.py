from pathlib import Path
import pickle

def load_collection(filepath: Path) -> dict:
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}