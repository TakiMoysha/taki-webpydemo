from collections.abc import Iterable
from typing import Protocol


class ICounterMixin(Protocol):
    def __len__(self) -> int: ...


class IIntoIter(Protocol):
    def into_iter(self) -> Iterable: ...
