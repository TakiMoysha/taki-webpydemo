from dataclasses import dataclass
from typing import ClassVar, Self


@dataclass(eq=False)
class BaseDevKitError(Exception):
    status: ClassVar[int] = 500
    subject = Self.__name__
    description = "base devkit error"
