from typing import Any, Protocol, TypeVar, runtime_checkable

ModelType = TypeVar("ModelType")


@runtime_checkable
class IAsyncDAOModel(Protocol[ModelType]):
    """Data Access Object implementation protocol oriented on SQLAlchemy model."""

    model: ModelType
    session: Any

    def __init__(self, model: ModelType, session: Any) -> None: ...

    async def get(self, obj_id: Any, **kwargs: Any) -> ModelType | None: ...

    async def find(self, **kwargs: Any) -> list[ModelType]: ...

    async def update(self, obj_id: Any, **kwargs: Any) -> ModelType: ...

    async def delete(self, obj_id: Any, **kwargs: Any) -> ModelType: ...

    async def create(self, **kwargs: Any) -> ModelType: ...
