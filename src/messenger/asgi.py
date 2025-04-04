from litestar import Litestar


def create_messenger() -> Litestar:
    from messenger.config.app import get_settings
    from messenger.server.openapi import config as openapi_config
    from messenger.server.routers import route_handlers

    settings = get_settings()

    return Litestar(
        debug=settings.app.DEBUG,
        openapi_config=openapi_config,
        route_handlers=route_handlers,
        on_app_init=[],
    )
