# ruff: noqa: F403,F405
from advanced_alchemy.base import UUIDAuditBase
from .prelude import *
from sqlalchemy.ext.associationproxy import association_proxy


class User(BigIntAuditBase):
    __tablename__ = "msg_users"
    __pii_columns__ = {"name", "email"}

    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    chats = relationship("ChatMember", back_populates="user")


class UserOAuthAccount(BigIntAuditBase):
    __tablename__ = "msg_user_oauth_accounts"
    __table_args__ = {"comment": "Registered OAUTH2 accounts for users"}
    __pii_columns__ = {"oauth_name", "account_email", "account_id"}

    user_id = Column(ForeignKey("msg_users.id", ondelete="CASCADE"), nullable=False)
    oauth_name = Column(String(length=1024), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    refresh_token = Column(String(length=1024), nullable=False)
    account_id = Column(String(length=128), index=True, nullable=False)
    account_email = Column(String(length=128), nullable=False)

    # user = relationship("User", back_populates="oauth_accounts")
    user = relationship("User", back_populates="oauth_accounts", viewonly=True, innerjoin=True, lazy="joined")
    user_name = association_proxy("user", "name")
    user_email = association_proxy("user", "email")
