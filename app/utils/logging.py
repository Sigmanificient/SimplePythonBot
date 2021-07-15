from datetime import datetime
from typing import Any, Tuple, Union

LOG_FORMAT: str = '%d/%b/%Y:%H:%M:%S'


def log(*args: Union[Any, Tuple[Any]]) -> None:
    """prints a formatted log message."""
    print(f"[{datetime.now():{LOG_FORMAT}}]", *args)


def warn(*args: Union[Any, Tuple[Any]]) -> None:
    """prints a warning message."""
    print("[Warning]", *args)
