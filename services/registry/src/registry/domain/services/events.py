from dataclasses import dataclass
from uuid import UUID

from wsdk.events import BaseEvent


@dataclass(frozen=True)
class ServiceNameUpdated(BaseEvent):
    service_id: UUID
    old_servicename: str
    new_servicename: str


@dataclass(frozen=True)
class ServiceUnregistered(BaseEvent):
    service_id: UUID


@dataclass(frozen=True)
class ServiceRegistered(BaseEvent):
    service_id: UUID
