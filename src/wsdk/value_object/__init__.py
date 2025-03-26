from abc import ABC
from dataclasses import dataclass
from typing import TypeVar

from wsdk.validators import IValidator


@dataclass(frozen=True, slots=True)
class BaseValueObject[T](ABC):
    value: T
    validators: tuple[IValidator] | None

    def __post_init__(self) -> None:
        if self.validators is not None:
            tuple(v(self.value) for v in self.validators)
