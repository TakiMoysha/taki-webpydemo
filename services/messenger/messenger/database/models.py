from advanced_alchemy.mixins import AuditColumns
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, DateTime, Enum, Integer, String, Text

from messenger.lib.database import BaseModel

__all__ = [
    "Chat",
    "ChatMember",
    "Group",
    "Message",
    "User",
]


class User(BaseModel, AuditColumns):
    __tablename__ = "msg_users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    chats = relationship("ChatMember", back_populates="user")


class Chat(BaseModel, AuditColumns):
    __tablename__ = "msg_chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    kind = Column(Enum("private", "group", name="chat_kind"), nullable=False)

    members = relationship("ChatMember", back_populates="chat")


class ChatMember(BaseModel, AuditColumns):
    __tablename__ = "msg_chat_member"
    __table_args__ = (UniqueConstraint("chat_id", "user_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    user_id = Column(ForeignKey("msg_users.id"), nullable=False)
    role = Column(Enum("admin", "member", name="chat_member_role"), nullable=False)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chats")


class Group(BaseModel, AuditColumns):
    __tablename__ = "msg_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    creator_id = Column(ForeignKey("msg_chat_member.id"), nullable=False)

    creator = relationship("ChatMember", foreign_keys=[creator_id])
    members = relationship("ChatMember", back_populates="group")


class Message(BaseModel):
    __tablename__ = "msg_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    sender_id = Column(ForeignKey("msg_users.id"), nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_reader = Column(Boolean, nullable=False, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
