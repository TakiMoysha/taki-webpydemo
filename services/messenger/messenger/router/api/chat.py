from typing import Annotated

from litestar import get, post
from litestar.controller import Controller
from litestar.openapi.spec import Example
from litestar.params import Body

from messenger.database.models import Message
from messenger.lib.logger import get_logger

NewChatRequestExample = Example(
    summary="Create new chat",
    value='{"name": "Example Chat", "members": ["user@example.com", "user@example.com"]}',
)

logger = get_logger()


class ChatController(Controller):
    path = "/chats/"

    # guards = [JWTAuth, OAuth2Auth]

    @get("/")
    async def available_chats(self) -> None:
        return None

    @post("/")
    async def create_chat(
        self,
        data: Annotated[
            dict,
            Body(
                title="New chat data",
                description="json with chat.name and invited member by email",
                examples=[NewChatRequestExample],
            ),
        ],
    ) -> None:
        return None

    @get("/{chat_id:int}/history")
    async def get_history(self, chat_id: int) -> None:
        # db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).limit(40)
        return None
