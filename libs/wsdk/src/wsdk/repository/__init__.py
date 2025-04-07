from typing import Protocol


class BaseRepository[Tid](Protocol):
    async def add(self, obj: object) -> None: ...

    async def update(self, obj: object) -> None: ...
