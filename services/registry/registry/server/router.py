from litestar.router import Router

from registry.api.router import root_api_router


def get_routers() -> tuple[Router]:
    return (root_api_router,)
