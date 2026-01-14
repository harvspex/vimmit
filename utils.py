from pathlib import Path
from typing import Any
import pickle


def dump_pickle(obj: Any, filepath: Path):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


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
