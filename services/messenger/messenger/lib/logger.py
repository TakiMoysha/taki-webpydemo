from functools import lru_cache
from typing import Any

import structlog


@lru_cache
def get_logger(*args: Any, **initial_values: Any) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(*args, **initial_values)
