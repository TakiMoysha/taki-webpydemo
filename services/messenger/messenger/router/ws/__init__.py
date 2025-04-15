import asyncio
import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import override

import anyio
from litestar import Litestar, WebSocket, websocket, websocket_listener
from litestar.handlers import WebsocketListener, send_websocket_stream
from litestar.serialization.msgspec_hooks import decode_json

from messenger.lib.logger import get_logger

L = get_logger()


@dataclass
class Message:
    content: str
    timestamp: float
    sender: str


@websocket(path="/v1/chat/{chat_id:str}")
async def chat_handler(socket: WebSocket) -> None:
    await socket.accept()

    is_streaming = anyio.Event()
    await is_streaming.set()

    async def handle_stream() -> None:
        while is_streaming.is_set():
            msg = Message(content=str(is_streaming.statistics()), timestamp=time.time(), sender="takimoysha")
            await socket.send_json(msg)

        await socket.close()

    async def handle_receive() -> None:
        async for event in socket.iter_json():
            L.info(f"{socket.client}: {event}")

        L.info("receive ended")
        await is_streaming.set()

    async with asyncio.TaskGroup() as tg:
        # tg.create_task(send_websocket_stream(socket, stream=handle_stream())) # https://github.com/litestar-org/litestar/issues/4106
        # tg.create_task(handle_stream())
        # tg.create_task(handle_receive())
        await is_streaming.set()


class ChatConnectionWs(WebsocketListener):
    path = "/v2/chat/{chat_id:int}"

    # @override
    # async def on_accept(self, chat_id: int, socket: WebSocket) -> None:
    #     await socket.accept(headers={"X-Chat-Header": str(chat_id)})

    @override
    # async def on_receive(self, data: str) -> AsyncGenerator[Message, None]:
    async def on_receive(self, data: str) -> str:
        print("conn: ", self._owner, data)
        return data
