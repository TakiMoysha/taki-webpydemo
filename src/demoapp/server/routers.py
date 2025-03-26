from litestar.types import ControllerRouterHandler

from demoapp.api.routers import api_router

route_handlers: list[ControllerRouterHandler] = [api_router]
