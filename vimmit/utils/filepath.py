from pathlib import Path
from typing import Callable


DEFAULT_FILENAME = 'vimmit'
VMT_SUFFIX = '.vmt'


def validate_path(func: Callable, filepath: str | None):
    def wrapper() -> Path:
        if filepath is None:
            filepath = Path.cwd() / DEFAULT_FILENAME

        path = Path(filepath).expanduser()

        if not path.parent.exists():
            raise NotADirectoryError('Parent directory does not exist.')

        if path.is_dir():
            path /= DEFAULT_FILENAME

        path = path.with_suffix(VMT_SUFFIX)

        return func(path)
    return wrapper


@validate_path
def validate_export_path(filepath: str | None) -> Path:
    if filepath.is_file() and filepath.suffix == VMT_SUFFIX:
        raise FileExistsError(f'{filepath} that already exists.')
    return filepath


@validate_path
def validate_import_path(filepath: str | None) -> Path:
    if not filepath.is_file():
        raise FileNotFoundError(f'{filepath} does not exist.')
    return filepath