from advanced_alchemy.base import BigIntAuditBase
from advanced_alchemy.mixins import AuditColumns
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Enum, String, Text

__all__ = [
    "Chat",
    "ChatMember",
    "Group",
    "Message",
    "User",
]


class User(BigIntAuditBase, AuditColumns):
    __tablename__ = "msg_users"

    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    chats = relationship("ChatMember", back_populates="user")


class Chat(BigIntAuditBase, AuditColumns):
    __tablename__ = "msg_chats"

    name = Column(String, nullable=False)
    kind = Column(Enum("private", "group", name="chat_kind"), nullable=False)

    members = relationship("ChatMember", back_populates="chat")


class ChatMember(BigIntAuditBase, AuditColumns):
    __tablename__ = "msg_chat_member"
    __table_args__ = (UniqueConstraint("chat_id", "user_id"),)

    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    user_id = Column(ForeignKey("msg_users.id"), nullable=False)
    role = Column(Enum("admin", "member", name="chat_member_role"), nullable=False)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chats")


class Group(BigIntAuditBase, AuditColumns):
    __tablename__ = "msg_groups"

    name = Column(String, index=True, unique=True, nullable=False)
    creator_id = Column(ForeignKey("msg_chat_member.id"), nullable=False)

    creator = relationship("ChatMember", foreign_keys=[creator_id])
    members = relationship("ChatMember", back_populates="group")


class Message(BigIntAuditBase):
    __tablename__ = "msg_messages"

    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    sender_id = Column(ForeignKey("msg_users.id"), nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_reader = Column(Boolean, nullable=False, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
