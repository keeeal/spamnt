import logging
from yaml import safe_dump, safe_load
from pathlib import Path
from typing import Any, Optional, Union


def read_config(
    file: Union[Path, str],
    default: Optional[Any] = None,
) -> Optional[Any]:
    if Path(file).is_file():
        logging.info(f"Reading: {file}")
        with open(file) as f:
            return safe_load(f)
    elif default:
        logging.info(f"Creating: {file}")
        with open(file, "w+") as f:
            safe_dump(default, f, indent=2, sort_keys=False)
        return default
    else:
        logging.warning(f"Not found: {file}")
