from pathlib import Path
from typing import Any, Callable
import pickle

CONFIG = {
    'base_url': None,
    'bl_hash': None,
    'systems': {},
}

def dump_pickle(obj: Any, filepath: Path):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def _load_pickle(filepath: Path, default: Callable, *args, **kwargs) -> dict:
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default(*args, **kwargs)


def load_collection(filepath: Path) -> dict:
    return _load_pickle(filepath, lambda: {})


def _init_config(filepath: Path) -> dict:
    dump_pickle(CONFIG, filepath)
    return CONFIG


def load_config(filepath: Path) -> dict:
    return _load_pickle(filepath, _init_config, filepath)


def load_blacklist(filepath: Path) -> set:
    with open(filepath, 'r') as f:
        return set([_.lower().strip() for _ in f.readlines() if _])
