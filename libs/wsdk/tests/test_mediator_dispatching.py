import pytest
from typing import override
from unittest import TestCase

from wsdk.mediator.dispatch_based import BaseCommand, BaseQuery, ICommandHandler, IQueryHandler, Mediator


class TestCommand(BaseCommand):
    pass


class TestCommandHandler(ICommandHandler):
    @override
    async def handle(self, command: BaseCommand) -> None:
        pass


class TestQueryHandler(IQueryHandler):
    @override
    async def handle(self, query: BaseQuery) -> None:
        pass


@pytest.mark.skip("Not implemented")
class TestMediator(TestCase):
    mediator: Mediator

    @override
    def setUp(self) -> None:
        self.mediator = Mediator()
        return super().setUp()

    @pytest.mark.skip("Not implemented")
    def test_should_mediator(self) -> None:
        a_command: BaseCommand = TestCommand()
        a_command_handlers: list[ICommandHandler] = [TestCommandHandler()]

        b_query: BaseQuery = BaseQuery()
        b_query_handlers: list[IQueryHandler] = [TestQueryHandler()]

        ## SHOULD BE OK
        self.mediator.register(
            a_command,
            b_query_handlers,
        )

        self.mediator.register(
            a_command,
            a_command_handlers,
        )

        ## SHOULD BE OK
        self.mediator.register(
            b_query,
            a_command_handlers,
        )
