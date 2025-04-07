from litestar import Litestar

from registry.server.server import ServerPlugin


def create_app() -> Litestar:
    from registry.config import get_settings
    from registry.server.openapi import config as openapi_config
    from registry.server.router import get_routers

    settings = get_settings()

    return Litestar(
        debug=settings.app.DEBUG,
        openapi_config=openapi_config,
        route_handlers=get_routers(),
        on_app_init=[],
        plugins=[
            ServerPlugin(),
        ],
    )
