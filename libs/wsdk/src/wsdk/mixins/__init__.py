from collections.abc import Iterable
from typing import Protocol, Self


class ICounterMixin(Protocol):
    def __len__(self) -> int: ...


class IIntoIter(Protocol):
    def into_iter(self) -> Iterable: ...


class SingletonMixin:
    def __new__(cls, *args: list, **kwargs: dict) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._inicialized = False

        return cls._instance
