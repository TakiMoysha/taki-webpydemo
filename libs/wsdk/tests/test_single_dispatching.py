from dataclasses import dataclass
from functools import singledispatch
from typing import Callable, overload, override
from unittest import TestCase


@dataclass(frozen=True, slots=True)
class BusRecord: ...


@dataclass(frozen=True, slots=True)
class EventRecord(BusRecord):
    name: str
    callback: Callable


@dataclass(frozen=True, slots=True)
class CommandRecord(BusRecord):
    name: str
    callback: Callable
    arguments: list


@dataclass(frozen=True, slots=True)
class QueryRecord(BusRecord):
    name: str
    callback: Callable
    params: list


class ABus:
    def __init__(self) -> None:
        self._events = []
        self._commands = []
        self._queries = []


_bus = ABus()


@singledispatch
def registry(bus_record: BusRecord) -> None:
    raise NotImplementedError(f"Unsupported type: {type(bus_record)}")


@registry.register
def _(bus_record: EventRecord) -> None:
    _bus._events.append(bus_record)


@registry.register
def _(bus_record: CommandRecord) -> None:
    _bus._commands.append(bus_record)


@registry.register
def _(bus_record: QueryRecord) -> None:
    _bus._queries.append(bus_record)


class TestABusDispatchMethod(TestCase):
    @override
    def setUp(self) -> None:
        self.abus = ABus()

    def test_should_call_event_handler(self) -> None:
        registry(EventRecord("event", lambda: None))

    def test_should_call_command_handler(self) -> None:
        registry(CommandRecord("command", lambda: None, []))
        try:
            registry(123)
        except Exception as e:
            assert True
            return

        raise AssertionError("Should raise exception")

    def test_should_call_query_handler(self) -> None:
        registry(QueryRecord("query", lambda: None, []))
