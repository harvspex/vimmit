from pathlib import Path

from common.exceptions import ImportExportError


DEFAULT_FILENAME = 'vimmit'
VMT_SUFFIX = '.vmt'


def _validate_path(
    filepath: str | None,
    default_name: str=DEFAULT_FILENAME,
    suffix: str=VMT_SUFFIX
) -> Path:
    if filepath is None:
        filepath = Path.cwd()

    path = Path(filepath).expanduser()

    if not path.parent.exists():
        raise ImportExportError('Parent directory does not exist.')

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
        raise ImportExportError(f'Cannot overwrite file that already exists: {path}')
    return path


def validate_import_path(filepath: str | None) -> Path:
    path = _validate_path(filepath)
    if not path.is_file():
        raise ImportExportError(f'Cannot import from file that does not exist: {path}')
    return path