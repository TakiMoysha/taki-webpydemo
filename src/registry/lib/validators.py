from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validate

from registry.exceptions import ValidationUserInpubtError

SERVICE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255,
        },
        "semver": {
            "type": "string",
            "minLength": 5,
            "maxLength": 14,
            "pattern": "^(?:0|[1-9]\\d*)\\.(?:0|[1-9]\\d*)\\.(?:0|[1-9]\\d*)$",
        },
        "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255,
        },
    },
    "required": ["name", "semver", "description"],
}


def validate_service(graph: dict):
    try:
        validate(instance=graph, schema=SERVICE_SCHEMA)
    except jsonschema_exceptions.ValidationError as error:
        error_path = "->".join([str(x) for x in error.absolute_path])
        msg = f"{error.message}:{error_path}"
        raise ValidationUserInpubtError(msg) from None
    except jsonschema_exceptions.SchemaError as error:
        msg = "Internal docs_lib exception."
        raise ValidationUserInpubtError(msg) from None
