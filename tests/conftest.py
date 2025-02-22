import pytest
from litestar import Litestar

pytestmark = pytest.mark.anyio


@pytest.fixture(name="app")
def app(pytestconfig: pytest.Config) -> Litestar:
    from app.asgi import create_app

    return create_app()
