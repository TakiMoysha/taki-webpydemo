from typing import Protocol, runtime_checkable


@runtime_checkable
class IInteractor(Protocol):
    def execute(self, *args, **kwargs): ...


@runtime_checkable
class IStore[ModelDTOLike](Protocol):
    def add(self, values: list[ModelDTOLike]): ...
    def bulk_save(self): ...
