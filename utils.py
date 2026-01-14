from pathlib import Path
import pickle


def load_collection(filepath: Path) -> dict:
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def _init_config(filepath: Path) -> dict:
    ...


def load_config(filepath: Path) -> dict:
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return _init_config(filepath)


def load_blacklist(filepath: Path) -> set:
    with open(filepath, 'r') as f:
        return set([_.lower().strip() for _ in f.readlines() if _])
