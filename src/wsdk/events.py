from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from uuid6 import uuid7


@dataclass(frozen=True)
class BaseEvent:
    id: UUID = field(init=False, kw_only=True, default_factory=uuid7)
    occurred_at: datetime = field(init=False, kw_only=True, default_factory=lambda: datetime.now(UTC))
