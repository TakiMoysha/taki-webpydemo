from litestar import get
from litestar.response import File
from litestar.types import ControllerRouterHandler

from messenger.router import api_router, ws_router


@get("/favicon.ico", sync_to_thread=True, cache=True)
def stub_favicon() -> File:
    return File("static/favicon.ico")


root_router: tuple[ControllerRouterHandler, ...] = (stub_favicon, api_router, ws_router)
