from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


type AppClient = AsyncIterator[AsyncClient]


@pytest.fixture(name="demoapp_client")
async def demoapp_client(app: Litestar) -> AppClient:
    async with AsyncTestClient(app, base_url="http://localhost:8000") as client:
        yield client
