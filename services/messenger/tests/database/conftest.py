import os
from typing import Generator, Literal

import pytest
from sqlalchemy import StaticPool
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session

from messenger.lib.database import BaseModel


# @pytest.fixture(scope="session")
# def sqlalchemy_connect_url() -> str:
#     return os.getenv("SQLALCHEMY_CONNECT_URL", "sqlite:///:memory:")


# @pytest.fixture(scope="session")
# def sqlalchemy_connect_url(request: pytest.FixtureRequest) -> str | Literal["sqlite:///:memory:"]:
#     url = request.config.getoption("--sqlalchemy-connect-url")
#     return url


# @pytest.fixture(scope="session")
# def database_engine(database_url: str) -> Engine:
#     return create_engine(database_url, echo=True)
#
#
# @pytest.fixture(scope="session")
# def tables(engine: Engine) -> Generator[None, Engine, None]:
#     BaseModel.metadata.create_all(engine)
#     yield
#     BaseModel.metadata.drop_all(engine)
#
#
# @pytest.fixture(scope="function")
# async def dbsession(engine: Engine, tables: Generator[None, Engine, None]):
#     connection = engine.connect()
#     session = Session(bind=connection, autoflush=False, autocommit=False)
#
#     yield session
#
#     session.rollback()
#     connection.close()


# def pytest_addoption(parser: pytest.Parser) -> None:
#     parser.addoption(
#         "--sqlalchemy-connect-url",
#         action="store",
#         default="sqlite:///:memory:",
#         help="Database url for SQLAlchemy",
#     )
