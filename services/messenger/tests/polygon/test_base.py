import pytest

from collections.abc import Iterable
import sqlite3
from typing import Protocol, runtime_checkable
from dishka import Provider, make_container, provide, Scope


## ============================================================================ SCOPE
# [RUNTIME] → APP → [SESSION] → REQUEST → ACTION → STEP


## ============================================================================ Services
@runtime_checkable
class IRepository(Protocol): ...


class RepositoryImpl: ...


class Service:
    def __init__(self, repo: IRepository) -> None: ...


class NetworkMesh: ...


service_provider = Provider(scope=Scope.SESSION)
service_provider.provide(Service)
service_provider.provide(RepositoryImpl, provides=IRepository)
service_provider.provide(NetworkMesh, scope=Scope.APP)


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    def new_conn(self) -> Iterable[sqlite3.Connection]:
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()


## ============================================================================ Containers

container = make_container(service_provider, ConnectionProvider())


@pytest.mark.polygon
@pytest.mark.asyncio
async def test_base():
    client = container.get("NetworkMesh")


## ============================================================================ ...
# https://dishka.readthedocs.io/en/stable/di_intro.html
