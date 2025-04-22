from typing import Protocol

from litestar.types import Scopes
from litestar.di import Provide
from litestar.plugins.sqlalchemy import repository


class IDAO(Protocol): ...


class Service:
    def __init__(self) -> None: ...


class ClientRepository(repository.SQLAlchemyAsyncRepository): ...


service_provider = Provide(scope=REQUEST)
