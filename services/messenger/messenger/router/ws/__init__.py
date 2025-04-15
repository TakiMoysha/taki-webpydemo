import asyncio
import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import override

from litestar import Litestar, WebSocket, websocket, websocket_listener
from litestar.handlers import WebsocketListener, send_websocket_stream

# @dataclass
# class Message:
#     content: str
#     timestamp: float
#     sender: str


@websocket(path="/v1/chat/{chat_id:str}")
async def chat_handler(socket: WebSocket) -> None:
    await socket.accept()
    is_working = True

    async def handle_stream() -> AsyncGenerator[dict[str, str], None]:  # open issue, dict annotated not working
        while is_working:
            yield {"message": "hello"}
            await asyncio.sleep(0.5)
            # await asyncio.sleep(0.5)

        await socket.close()

    async def handle_receive() -> None:
        async for event in socket.iter_json():
            print(f"{socket.client}: {event}")
        print("receive ended")

    async with asyncio.TaskGroup() as tg:
        # tg.create_task(send_websocket_stream(socket, stream=handle_stream())) # https://github.com/litestar-org/litestar/issues/4106
        tg.create_task(handle_receive())


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
