from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.testing import AsyncTestClient, TestClient, create_async_test_client

from messenger.asgi import create_app
from messenger.router.ws import ChatConnectionWs


@pytest_asyncio.fixture
async def client():
    async with AsyncTestClient(app=create_app(), session_config=ServerSideSessionConfig()) as client:
        await client.set_session_data({"user_id": 1})
        res = await client.get("/api/health")
        assert res.status_code == 200
        return client


# Tests:
# - auth token
# - jwt
# - sso
# - 2fa
# - history msg
# - msg statuses
# - dublication prevent
# - sorting
