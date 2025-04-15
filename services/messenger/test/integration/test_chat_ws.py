import unittest
from turtle import setup
from typing import override
from unittest import mock

import pytest
from litestar import WebSocket, websocket, websocket_listener
from litestar.exceptions.websocket_exceptions import WebSocketDisconnect, WebSocketException
from litestar.serialization import decode_json
from litestar.testing import AsyncTestClient, TestClient, create_async_test_client, create_test_client
from msgspec import json

from messenger.router.ws import ChatConnectionWs

pytestmark = pytest.mark.asyncio


@pytest.mark.skip("issue in litetsar msgspec.decode_json")
# @mock.patch("messenger.router.ws.chat_generator") # overwrite function with custom returned data
@pytest.mark.timeout(5)
async def test_deplex_chat_connection(client: AsyncTestClient) -> None:
    test_msg = {"hello": "world"}
    ws = await client.websocket_connect("/ws/v1/chats/100")
    ws.send_json(test_msg)
    data = ws.receive_json()
    ws.close()
    assert data == {"message": test_msg}
