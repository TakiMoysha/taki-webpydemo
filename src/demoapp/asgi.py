from litestar import Litestar

from demoapp.server.signals import get_signals


def create_app() -> Litestar:
    from demoapp.config.app import cors_config
    from demoapp.config.base import get_settings
    from demoapp.server.dependencies import get_dependencies
    from demoapp.server.openapi import config as openapi_config
    from demoapp.server.plugins import get_plugins
    from demoapp.server.routers import route_handlers

    settings = get_settings()

    return Litestar(
        debug=settings.app.DEBUG,
        cors_config=cors_config,
        dependencies=get_dependencies(),
        openapi_config=openapi_config,
        route_handlers=route_handlers,
        plugins=get_plugins(),
        listeners=get_signals(),
        on_app_init=[],
    )
