from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Protocol, runtime_checkable

from wsdk.exceptions import BaseServiceDevKitError
from wsdk.singleton import SingletonMixin


class NoHandlerRegisteredError(BaseServiceDevKitError):
    pass


type TCommand = type
type TQuery = type


@runtime_checkable
class ICommandHandler(Protocol):
    async def handle(self, command: Any) -> Any: ...


@runtime_checkable
class IQueryHandler(Protocol):
    async def handle(self, query: Any) -> Any: ...


@dataclass(eq=False, init=False)
class Mediator(SingletonMixin):
    def __init__(self) -> None:
        if not self._inicialized:
            self._commands_map: defaultdict[TCommand, list[ICommandHandler]] = defaultdict(list)
            self._query_map: defaultdict[TQuery, list[IQueryHandler]] = defaultdict(list)
            self._inicialized = True

    def _reset(self) -> None:
        self._commands_map: defaultdict[TCommand, list[ICommandHandler]] = defaultdict(list)
        self._query_map: defaultdict[TQuery, list[IQueryHandler]] = defaultdict(list)

    def register_command(self, command: TCommand, handlers: Iterable[ICommandHandler]) -> None:
        self._commands_map[command].extend(handlers)

    def register_query(self, query: TCommand, handlers: Iterable[IQueryHandler]) -> None:
        self._query_map[query].extend(handlers)

    async def handle_command(self, command: TCommand) -> Iterable[CR]:
        handlers: list[ICommandHandler] = self._commands_map[command.__class__]

        if not handlers:
            msg = f"No handler registered for {command.__class__}"
            raise NoHandlerRegisteredError(msg)
        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: TCommand) -> Iterable[QR]:
        handlers: list[IQueryHandler] = self._query_map[query.__class__]

        if not handlers:
            msg = f"No handler registered for {query.__class__}"
            raise NoHandlerRegisteredError(msg)
        return [await handler.handle(query) for handler in handlers]
