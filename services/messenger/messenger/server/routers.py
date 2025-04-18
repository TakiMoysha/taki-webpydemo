from litestar.types import ControllerRouterHandler

from messenger.router import api_router, ws_router

route_handlers: tuple[ControllerRouterHandler, ...] = (api_router, ws_router)
