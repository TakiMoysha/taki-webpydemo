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


@websocket(path="/v1/chats/{chat_id:str}")
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


# connection & disconnection processing
# write and read messages
# msg status processing
class ChatService:
    def __init__(self) -> None:
        pass

    def new_member(self, socket: WebSocket) -> None:
        pass

    def leave_member(self, socket: WebSocket) -> None:
        pass

    def receive_msg(self, msg: Message) -> None:
        pass

    def new_msg(self, msg: Message) -> None:
        pass
