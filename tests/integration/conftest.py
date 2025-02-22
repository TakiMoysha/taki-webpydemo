from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


type AppClient = AsyncIterator[AsyncClient]
type JsonerClient = AsyncIterator[AsyncClient]


@pytest.fixture(name="app_client")
async def app_client(app: Litestar) -> AppClient:
    async with AsyncTestClient(app, base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture(name="jsoner_client")
async def jsoner_client(app: Litestar) -> JsonerClient:
    async with AsyncTestClient(app, base_url="http://localhost:8000") as client:
        yield client
