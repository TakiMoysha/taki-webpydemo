from typing import Any

from orjson import loads

from docs_lib.consts import DATA_DIR
from docs_lib.validators import validate_graph


def load_graph_file() -> dict[str, Any]:
    path = DATA_DIR / "graph.json"

    if not path.exists():
        msg = f"graphfile not found at {path}"
        raise FileNotFoundError(msg)

    _graph = loads(path.read_text())
    validate_graph(_graph)
    return _graph
