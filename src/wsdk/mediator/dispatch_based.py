from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Any, Protocol, overload, runtime_checkable

from wsdk.exceptions import BaseDevKitError
from wsdk.singleton import SingletonMixin


class NoHandlerRegisteredError(BaseDevKitError):
    pass


class BaseCommand: ...


class BaseQuery: ...


class BaseEvent: ...


@runtime_checkable
class ICommandHandler(Protocol):
    object_type = BaseCommand

    async def handle(self, command: Any) -> Any: ...


@runtime_checkable
class IQueryHandler(Protocol):
    object_type = BaseQuery

    async def handle(self, query: Any) -> Any: ...


@runtime_checkable
class IEventHandler(Protocol):
    object_type = BaseEvent

    async def handle(self, query: Any) -> Any: ...


@dataclass(eq=False, init=False)
class Mediator(SingletonMixin):
    def __init__(self) -> None:
        if not self._inicialized:
            self._reinit_maps()
            self._inicialized = True

    def _reinit_maps(self) -> None:
        self.commands_map: defaultdict[BaseCommand, list[ICommandHandler]] = defaultdict(list)
        self.query_map: defaultdict[BaseQuery, list[IQueryHandler]] = defaultdict(list)
        self.events_map: defaultdict[BaseEvent, list[IEventHandler]] = defaultdict(list)

    @singledispatchmethod
    def register(
        self,
        command: BaseCommand | BaseQuery | BaseEvent,
        handlers: Iterable[ICommandHandler] | Iterable[IQueryHandler] | Iterable[IEventHandler],
    ) -> None:
        debug_msg = f"Unsupported type: {type(command)}, {tuple(map(type, handlers))}"
        raise NotImplementedError(debug_msg)

    @overload
    @register.register
    # @register.register(BaseCommand)
    # @register.register(Iterable[ICommandHandler])
    def _(self, command: BaseCommand, handlers: Iterable[ICommandHandler]) -> None:
        print(command, handlers)
        self.commands_map[command].extend(handlers)

    @overload
    @register.register
    # @register.register(BaseQuery)
    # @register.register(Iterable[IQueryHandler])
    def _(self, query: BaseQuery, handlers: Iterable[IQueryHandler]) -> None:
        print(query, handlers)
        self.query_map[query].extend(handlers)

    @overload
    @register.register
    # @register.register(BaseEvent)
    # @register.register(Iterable[IEventHandler])
    def _(self, event: BaseEvent, handlers: Iterable[IEventHandler]) -> None:
        print(event, handlers)
        self.events_map[event].extend(handlers)

    # async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
    #     handlers: list[ICommandHandler] = self.commands_map[command.__class__]
    #
    #     if not handlers:
    #         msg = f"No handler registered for {command.__class__}"
    #         raise NoHandlerRegisteredError(msg)
    #
    #     return [await handler.handle(command) for handler in handlers]
    #
    # async def handle_query(self, query: BaseCommand) -> Iterable[QR]:
    #     handlers: list[IQueryHandler] = self.query_map[query.__class__]
    #
    #     if not handlers:
    #         msg = f"No handler registered for {query.__class__}"
    #         raise NoHandlerRegisteredError(msg)
    #
    #     return [await handler.handle(query) for handler in handlers]
