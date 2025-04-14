from turtle import setup
from typing import override
from unittest import mock
import unittest

from msgspec import json
import pytest
from litestar import WebSocket, websocket, websocket_listener
from litestar.testing import AsyncTestClient, TestClient, create_async_test_client, create_test_client

from messenger.router.ws import ChatConnectionWs

pytestmark = pytest.mark.asyncio


async def test_websocket(client: AsyncTestClient) -> None:
    ws = await client.websocket_connect("/ws/v1/chat/100")
    _ = ws.send_json({"hello": "world"})
    r = ws.receive()
    print(r)
    # data = ws.receive_json()
    # ws.close()
    # print(data)
    # assert data == {"message": {"hello": "world"}}


# @mock.patch("messenger.router.ws.chat_generator") # overwrite function with custom returned data
# async def test_ws_duplex_connection(client: AsyncTestClient) -> None:
#     async def _test_by_version(path: str) -> None:
#         ws = await client.websocket_connect(path)
#         ws.send("hello, world")
#         response = await ws.receive()
#         print(response)
#
#
#     print("---")
#     await _test_by_version("/chat/v1/1")
#     print("---")
#     await _test_by_version("/chat/v2/1")


class TestChatByWebSocket(unittest.TestCase):
    @classmethod
    @override
    def setUpClass(cls) -> None:
        # create models
        cls.access_token = None
        cls.user_settings = None
        cls.account = None

    @override
    def tearDown(self) -> None:
        # drop models
        # close connections (dispose)
        pass

    @override
    def setUp(self) -> None:
        self.client = create_async_test_client(ChatConnectionWs)

    # @pytest.mark.order(1)
    # # @mock.patch("messenger.router.ws.chat_generator") # overwrite function with custom returned data
    # async def test_ws_duplex_connection(self) -> None:
    #     ws = await self.client.websocket_connect("/chat/v2/1")
    #     ws.send("hello, world")
    #     response = ws.receive_json()
    #     print("RESPONSE", response)
