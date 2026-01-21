from pathlib import Path

from common.exceptions import ImportExportError


DEFAULT_FILENAME = 'vimmit'
VMT_SUFFIX = '.vmt'


def _validate_path(filepath: str | None):
    if filepath is None:
        filepath = Path.cwd()

    path = Path(filepath).expanduser()

    if not path.parent.exists():
        raise ImportExportError('Parent directory does not exist.')

    if path.is_dir():
        path /= DEFAULT_FILENAME

    return path.with_suffix(VMT_SUFFIX)


def validate_export_path(filepath: str | None) -> Path:
    path = _validate_path(filepath)
    if path.is_file() and path.suffix == VMT_SUFFIX:
        raise ImportExportError(f'{path} that already exists.')
    return path


def validate_import_path(filepath: str | None) -> Path:
    path = _validate_path(filepath)
    if not path.is_file():
        raise ImportExportError(f'{path} does not exist.')
    return path