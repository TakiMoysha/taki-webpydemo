from advanced_alchemy.mixins import AuditColumns
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Boolean, DateTime, Enum, Integer, String, Text

from messenger.lib.database import BaseModel

# =========================== Users ===========================


class User(BaseModel, AuditColumns):
    __tablename__ = "msg_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)


class Chat(BaseModel, AuditColumns):
    __tablename__ = "msg_chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    kind = Column(Enum("private", "group", name="chat_kind"), nullable=False)


class Group(BaseModel, AuditColumns):
    __tablename__ = "msg_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    creator = Column(ForeignKey("msg_users.id"), nullable=False)
    members = mapped_column("msg_users.id", ForeignKey("msg_users.id"))


class Message(BaseModel):
    __tablename__ = "msg_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    sender_id = Column(ForeignKey("msg_users.id"), nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_reader = Column(Boolean, nullable=False)
