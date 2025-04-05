from litestar.types import ControllerRouterHandler

from messenger.api.routers import api_router

route_handlers: tuple[ControllerRouterHandler] = (api_router,)
