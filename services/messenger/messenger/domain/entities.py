from dataclasses import dataclass
from typing import Literal


# ===================== BASE DTO
@dataclass
class AuditDTO:
    created_at: float
    updated_at: float


# ===================== Full DTO
@dataclass
class FullUserDTO(AuditDTO):
    id: int
    name: str
    email: str
    password_hash: str


@dataclass
class FullChatDTO(AuditDTO):
    id: int
    name: str
    kind: Literal["group", "private"]


@dataclass
class FullChatMemberDTO(AuditDTO):
    id: int
    chat_id: int
    user_id: int
    role: Literal["admin", "member"]


@dataclass
class FullGroupDTO(AuditDTO):
    id: int
    name: str
    creator_id: int


@dataclass
class FullMessageDTO(AuditDTO):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: float
    is_reader: bool


# ===================== ReadOnly DTO
@dataclass(frozen=True)
class ReadOnlyUserDTO:
    id: int
    name: str
    email: str
