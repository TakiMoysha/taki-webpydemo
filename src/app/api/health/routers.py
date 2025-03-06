from litestar.router import Router

from .handlers import demo_validation

router = Router(path="/health", route_handlers=[demo_validation])
