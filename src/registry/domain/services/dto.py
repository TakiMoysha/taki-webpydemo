from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from registry.domain.exceptions import DomainError
from registry.domain.services.exceptions import ServiceAlreadyExistsError, ServiceCreationError
from registry.domain.services.value_objects import ServiceAddress, ServiceId, ServiceName
from registry.GLOBSCOPE import ServiceMetadata
from wsdk.events import BaseEvent


@dataclass
class BaseDTO(ABC):
    _events: list[BaseEvent] = field(init=False, default_factory=list, repr=False, hash=False, compare=False)

    def record_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def init_events(self, events: list[BaseEvent]) -> None:
        # validate events
        self._events = events

    def get_events(self) -> list[BaseEvent]:
        return self._events


@dataclass
class ServiceDTO(BaseDTO):
    id: ServiceId
    servicename: ServiceName
    address: str
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None

    @property
    def metadata(self) -> ServiceMetadata:
        return ServiceMetadata(str(self.id.value), self.servicename.value, self.address)

    @classmethod
    def register(cls, service_id: UUID, servicename: str, address: str, exising_services: set[ServiceMetadata]) -> Self:
        # validation row values
        _service_id = ServiceId(service_id)
        _servicename = ServiceName(servicename)
        _service_address = ServiceAddress(address)
        _service_metadata = ServiceMetadata(str(service_id), servicename, address)

        # validation
        if _service_metadata in exising_services:
            raise ServiceAlreadyExistsError(servicename)

        try:
            service = cls(_service_id, _servicename, address)
            exising_services.add(_service_metadata)
            # service.publish_event(ServiceRegistration()) # !TODO: implement event bus (?)
        except Exception as err:
            # rollback
            raise ServiceCreationError(servicename) from err

        return service

    def unregister(self, existing_username: set[ServiceMetadata], histdb: list[Self]) -> None:
        if self.deleted_at is None:
            return

        histdb.append(self)

        existing_username.remove(self.metadata)
