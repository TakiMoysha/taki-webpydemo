from dataclasses import dataclass
from typing import Literal


# ===================== Full DTO
@dataclass(slots=True)
class FullUserDTO:
    id: int
    name: str
    email: str
    password_hash: str


@dataclass(slots=True)
class FullChatDTO:
    id: int
    name: str
    kind: Literal["group", "private"]


@dataclass(slots=True)
class FullChatMemberDTO:
    id: int
    chat_id: int
    user_id: int
    role: Literal["admin", "member"]


@dataclass(slots=True)
class FullGroupDTO:
    id: int
    name: str
    creator_id: int


@dataclass(slots=True)
class FullMessageDTO:
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: float
    is_reader: bool


# ===================== ReadOnly DTO
@dataclass(slots=True, frozen=True)
class ReadOnlyUserDTO:
    id: int
    name: str
    email: str
