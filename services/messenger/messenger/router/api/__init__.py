from typing import Annotated

from litestar import get, post
from litestar.controller import Controller
from litestar.openapi.spec import Example
from litestar.params import Body

from messenger.database.models import Message

NewChatRequestExample = Example(
    summary="Create new chat",
    value='{"name": "Example Chat", "members": ["user@example.com", "user@example.com"]}',
)


@get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


class ChatController(Controller):
    path = "/v1/chats/"

    # guards = [JWTAuth, OAuth2Auth]

    @get("/")
    def available_chats(self) -> None:
        return None

    @post("/")
    def create_chat(
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
    def get_history(self, chat_id: int) -> None:
        # db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).limit(40)
        return None
