# ruff: noqa: F403,F405
from .prelude import *


class Chat(BigIntAuditBase):
    __tablename__ = "msg_chats"

    name = Column(String, nullable=False)
    kind = Column(Enum("private", "group", name="chat_kind"), nullable=False)

    members = relationship("ChatMember", back_populates="chat")


class ChatMember(BigIntAuditBase):
    __tablename__ = "msg_chat_member"
    __table_args__ = (UniqueConstraint("chat_id", "user_id"),)

    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    user_id = Column(ForeignKey("msg_users.id"), nullable=False)
    role = Column(Enum("admin", "member", name="chat_member_role"), nullable=False)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chats")


class ChatGroup(BigIntAuditBase):
    __tablename__ = "msg_groups"
    __pii_columns__ = {"name", "description"}

    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String(length=1024), nullable=True, default=None)
    creator_id = Column(ForeignKey("msg_chat_member.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # TODO: setup relationship
    # creator = relationship("ChatMember", foreign_keys=[creator_id])
    # members = relationship("ChatMember", back_populates="group")
    # invitations = relationship("ChatMember", back_populates="group_invitations")


class Message(BigIntAuditBase):
    __tablename__ = "msg_messages"

    chat_id = Column(ForeignKey("msg_chats.id"), nullable=False)
    sender_id = Column(ForeignKey("msg_users.id"), nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_reader = Column(Boolean, nullable=False, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
