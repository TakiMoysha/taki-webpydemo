from typing import Protocol, override
from uuid import UUID


class IValidator[T](Protocol):
    __slots__ = "_validators", "value"

    def __call__(self, value: T) -> None: ...


class UUIDValidator(IValidator[str]):
    @override
    def __call__(self, value: str) -> None:
        UUID(value)
