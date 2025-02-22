from typing import Protocol, runtime_checkable


@runtime_checkable
class IInteractor(Protocol):
    """Interactor implement UseCase using a business object.

    UseCase - a function, action that the user can perform
    """

    def execute(self, *args, **kwargs): ...


@runtime_checkable
class IStore[ModelDTOLike](Protocol):
    """In-moment storage for caching and storing data in memory"""

    def add(self, values: list[ModelDTOLike]): ...
    def bulk_save(self): ...


@runtime_checkable
class IParser(Protocol):
    """Parser for transforming raw data into business objects"""

    def parse(self, data) -> list: ...
