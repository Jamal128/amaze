"""Configuration file reader for the maze generator."""

from pathlib import Path

from parser.pydantic_model import MazeConfig
from pydantic import ValidationError

MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def parse_config(config_path: str) -> MazeConfig:
    """Parse a KEY=VALUE config file and return a validated MazeConfig.

    Args:
        config_path: Path to the configuration file.

    Returns:
        A MazeConfig instance with validated values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is malformed, missing keys, or fails validation.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path!r}")
    if not path.is_file():
        raise ValueError(f"Not a regular file: {config_path!r}")

    pairs = _read_pairs(path)
    _check_mandatory(pairs)

    try:
        return MazeConfig.model_validate(pairs)
    except ValidationError as exc:
        raise ValueError(f"Config validation error: {exc}") from exc


def _read_pairs(path: Path) -> dict[str, str]:
    """Read KEY=VALUE pairs from a config file, skipping comments and blanks.

    Args:
        path: Path object pointing to the config file.

    Returns:
        Dict of uppercase keys to raw string values.

    Raises:
        ValueError: On malformed lines or duplicate keys.
    """
    pairs: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Invalid line {line!r}: expected KEY=VALUE.")
            key, _, value = line.partition("=")
            key = key.strip().upper()
            value = value.strip()
            if not key:
                raise ValueError(f"Invalid line {line!r}: missing key.")
            if not value:
                raise ValueError(f"Invalid line {line!r}: missing value.")
            if key in pairs:
                raise ValueError(f"Duplicate key: {key!r}.")
            pairs[key] = value
    return pairs


def _check_mandatory(pairs: dict[str, str]) -> None:
    """Raise ValueError if any mandatory key is absent.

    Args:
        pairs: Parsed key-value pairs.

    Raises:
        ValueError: Listing the missing keys.
    """
    missing = MANDATORY_KEYS - pairs.keys()
    if missing:
        raise ValueError(f"Missing mandatory keys: {', '.join(sorted(missing))}.")
