from litestar.router import Router

from .api import health_check
from .ws import chat_handler, ChatConnectionWs

api_router = Router("/api", route_handlers=(health_check,))
ws_router = Router(
    "/ws",
    route_handlers=(
        chat_handler,
        ChatConnectionWs,
    ),
)

__all__ = [
    "api_router",
    "ws_router",
]
