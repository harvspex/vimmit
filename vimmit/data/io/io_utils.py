from enum import Enum
from pathlib import Path

from common.console import console
from common.exceptions import ImportExportError


DEFAULT_FILENAME = 'vimmit'
VMT_SUFFIX = '.vmt'


class DataKeys(Enum):
    CONFIG = 'config'
    GAMES = 'games'
    BLACKLIST = 'blacklist'


class ImportModes(Enum):
    GAMES = 'games'
    SEEN = 'seen'
    BLACKLIST = 'blacklist'
    ALL = 'all'


class ExportModes(Enum):
    DATA = 'data'
    HISTORY = 'history'


def _validate_path(
    filepath: str | None,
    default_name: str=DEFAULT_FILENAME,
    suffix: str=VMT_SUFFIX
) -> Path:
    if filepath is None:
        filepath = Path.cwd()

    path = Path(filepath).expanduser()

    if not path.parent.exists():
        raise ImportExportError(
            format_filepath_message('Folder does not exist', 'orange1', path.parent)
        )

    if path.is_dir():
        path /= default_name

    return path.with_suffix(suffix)


def validate_export_path(
    filepath: str | None,
    default_name: str=DEFAULT_FILENAME,
    suffix: str=VMT_SUFFIX
) -> Path:
    path = _validate_path(filepath, default_name, suffix)
    if path.is_file():
        raise ImportExportError(
            format_filepath_message('Cannot overwrite file that already exists', 'orange1', path)
        )
    return path


def validate_import_path(filepath: str | None) -> Path:
    path = _validate_path(filepath)
    if not path.is_file():
        raise ImportExportError(
            format_filepath_message('Cannot import from file that does not exist', 'orange1', path)
        )
    return path


def format_filepath_message(message: str, colour: str, filepath: Path) -> str:
    return f'[{colour}]{message}: [/{colour}]{filepath}'