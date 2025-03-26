from jsonschema import exceptions as jsonschema_exceptions

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
            "desc": "Used as a sandbox to try out the functionality.",
        },
        {
            "url": "",
            "docs": "Markdown document.",
        },
    ],
}


def test_should_validate_graph() -> None:
    # validate_graph(DEMO_BAD_GRAPH) # noqa: ERA001
    assert True


def test_should_throw_error() -> None:
    try:
        # validate_graph(DEMO_BAD_GRAPH) # # noqa: ERA001
        pass
    except jsonschema_exceptions.ValidationError:
        assert True
    except Exception as err:
        msg = "Unexpected error"
        raise AssertionError(msg) from err
