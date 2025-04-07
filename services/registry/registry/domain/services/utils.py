from dataclasses import dataclass
from typing import override


@dataclass
class ServiceMetadata:
    id: str
    name: str
    address: str

    @override
    def __hash__(self) -> int:
        return hash(f"{self.id}:{self.name}")
