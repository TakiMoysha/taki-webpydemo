from typing import Any

from jsonschema import exceptions, validate
from jsonschema import exceptions as jsonschema_exceptions

from docs_lib.exceptions import DocsLibBaseException

GRAPH_SOURCES_SCHEMA = {
    "type": "array",
    "properties": {
        "url": {"type": "string", "format": "uri"},
        "tags": {"enum": ["test_enum"]},
        "desc": {"type": "string", "maxLength": 64},
    },
    "required": ["url"],
}


GRAPH_SCHEMA = {
    "title": "Graph",
    "type": "object",
    "properties": {
        "sources": GRAPH_SOURCES_SCHEMA,
    },
}


class DocsValidationError(DocsLibBaseException): ...


def validate_graph(graph: dict[str, Any]) -> None:
    try:
        validate(instance=graph, schema=GRAPH_SCHEMA)
    except jsonschema_exceptions.ValidationError as error:
        error_path = "->".join([str(x) for x in error.absolute_path])
        msg = f"{error.message}:{error_path}"
        raise exceptions.ValidationError(msg) from None
    except jsonschema_exceptions.SchemaError as error:
        msg = "Internal docs_lib exception."
        raise exceptions.ValidationError(msg) from None
