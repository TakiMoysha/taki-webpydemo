from litestar.router import Router

from .api import ChatController, health_check
from .ws import chat_handler

api_router = Router(
    "/api",
    route_handlers=(health_check, ChatController),
)
ws_router = Router(
    "/ws",
    route_handlers=(chat_handler,),
)

__all__ = [
    "api_router",
    "ws_router",
]
