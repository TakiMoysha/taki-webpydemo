from dataclasses import dataclass

from wsdk.exceptions import BaseDevKitError


@dataclass(eq=False)
class DomainError(BaseDevKitError):
    description = "A domain error has occurred"
