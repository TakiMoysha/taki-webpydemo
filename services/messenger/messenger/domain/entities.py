from dataclasses import dataclass
from typing import Literal


# ===================== BASE DTO
@dataclass(slots=True)
class AuditDTO:
    created_at: float
    updated_at: float


# ===================== Full DTO
@dataclass(slots=True)
class FullUserDTO(AuditDTO):
    id: int
    name: str
    email: str
    password_hash: str


@dataclass(slots=True)
class FullChatDTO(AuditDTO):
    id: int
    name: str
    kind: Literal["group", "private"]


@dataclass(slots=True)
class FullChatMemberDTO(AuditDTO):
    id: int
    chat_id: int
    user_id: int
    role: Literal["admin", "member"]


@dataclass(slots=True)
class FullGroupDTO(AuditDTO):
    id: int
    name: str
    creator_id: int


@dataclass(slots=True)
class FullMessageDTO(AuditDTO):
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
