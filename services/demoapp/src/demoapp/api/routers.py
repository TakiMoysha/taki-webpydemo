from litestar.router import Router

from .health.routers import router as health_handler

api_router = Router(path="/api", route_handlers=[health_handler])
