from jsonschema import exceptions as jsonschema_exceptions

from docs_lib.validators import validate_graph

DEMO_RIGHT_GRAPH = {"sources": []}

DEMO_BAD_GRAPH = {"sources": {}}

DEMO_GRAPH = {
    "sources": [
        {
            "url": "https://github.com/TakiMoysha/taki-platform/README.md",
            "desc": "Private repository, protected by SSH key.",
        },
        {
            "url": "https://github.com/TakiMoysha/taki-webpydemo/README.md",
            "desc": "Used as a sandbox, to run through the functionality.",
        },
        {
            "url": "",
            "docs": "Markdown document.",
        },
    ],
}


def test_should_validate_graph() -> None:
    validate_graph(DEMO_RIGHT_GRAPH)
    assert True


def test_should_throw_error() -> None:
    try:
        validate_graph(DEMO_BAD_GRAPH)
    except jsonschema_exceptions.ValidationError:
        assert True
    except Exception as err:
        msg = "Unexpected error"
        raise AssertionError(msg) from err
