import os
from typing import Literal

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def database_url() -> str | Literal["sqlite+aiosqlite:///:memory:"]:
    return os.getenv("DB_URL", "sqlite+aiosqlite:///:memory:")


@pytest.fixture
async def database_engine(database_url: str | Literal["sqlite+aiosqlite:///:memory:"]):
    engine = await create_engine(database_url)
