from dataclasses import dataclass
from typing import Any, Protocol

type Event = Any
type OutboxMessage = Any


class IMessageOutbox(Protocol):
    def save(self, event: Event) -> None: ...
    def mark_as_published(self, message: OutboxMessage) -> None: ...
    def to_publish(self) -> tuple[OutboxMessage]: ...


class IEventBus(Protocol):
    def publish(self, event: Event) -> None: ...


class StoreAndForwardEventBus(IEventBus):
    def __init__(self, message: IMessageOutbox) -> None:
        self._message_outbox = message

    def publish(self, event: Event) -> None:
        self._message_outbox.save(event)
