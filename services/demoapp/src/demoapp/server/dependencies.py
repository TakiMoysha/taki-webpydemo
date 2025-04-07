from litestar.di import Provide

from demoapp.config import consts


async def provide_stub_user() -> None:
    return None


def get_dependencies() -> dict[str, Provide]:
    return {consts.USER_DEPENDENCY_KEY: Provide(provide_stub_user)}
