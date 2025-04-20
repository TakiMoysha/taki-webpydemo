from litestar import get
from litestar.response import File

from messenger.router import api_router, ws_router


@get("/favicon.ico", sync_to_thread=True, cache=True)
def stub_favicon() -> File:
    return File("static/favicon.ico")


def get_handlers() -> tuple:
    return (stub_favicon, api_router, ws_router)
