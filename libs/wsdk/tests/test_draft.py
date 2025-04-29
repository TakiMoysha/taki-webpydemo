import pytest


class SimpleConfig:
    __match_args__ = ()  # positional match arguments

    def __init__(self, **kwargs: dict) -> None:
        self.__dict__.update(kwargs)


def test_simple_config():
    MockService = type("MockService", (object,), {})
    cfgs = [
        SimpleConfig(url="http://192.168.0.1", port=80),
        SimpleConfig(threshold=10),
        SimpleConfig(service=MockService, debug=True),
    ]

    for cfg in cfgs:
        match cfg:
            case SimpleConfig(url="http://192.168.0.1"):
                print("\tmatched url_only: ", cfg.__dict__)
            case SimpleConfig(threshlod=10):
                print("\tmatched threshold_only: ", cfg.__dict__)
            case SimpleConfig(service=MockService):
                print("\tmatched service_only: ", cfg.__dict__)
            case SimpleConfig(debug=True):
                print("\tmatched debug_only: ", cfg.__dict__)
