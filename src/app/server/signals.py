from collections.abc import Sequence

from litestar.events.listener import EventListener


def get_signals() -> Sequence[EventListener]:
    return []
