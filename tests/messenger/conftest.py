from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def messenger_client() -> AsyncGenerator[AsyncClient, None]: ...


@pytest.mark.asyncio
async def messenger_server() -> AsyncGenerator[AsyncClient, None]: ...


# Tests:
# - auth token
# - history msg
# - msg statuses
# - dublication prevent
# - sorting
