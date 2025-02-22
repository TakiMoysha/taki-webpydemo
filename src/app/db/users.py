from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from litestar_users.adapter.sqlalchemy.mixins import SQLAlchemyUserMixin
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["User", "UserOAuthAccount"]


class User(UUIDAuditBase, SQLAlchemyUserMixin):
    __tablename__ = "user_account"
    __table_args__ = {"comment": "User accounts for Clients"}

    avatar_url: Mapped[str | None] = mapped_column(
        String(240),
        nullable=True,
        default=None,
    )
    telegram_id: Mapped[str | None] = mapped_column(
        unique=True,
        nullable=True,
        default=None,
    )

    login_count: Mapped[int] = mapped_column(Integer(), default=0)

    oauth_accounts: Mapped[list["UserOAuthAccount"]] = relationship(
        back_populates="user",
        lazy="noload",
        cascade="all, delete",
        uselist=True,
    )


class UserOAuthAccount(UUIDAuditBase):
    __tablename__ = "user_account_oauth"
    __table_args__ = {"comment": "OAUTH2 Accounts for User"}

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
    )
    oauth_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    access_token: Mapped[str] = mapped_column(String(100), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(100), nullable=False)
    expires_at: Mapped[int | None] = mapped_column(Integer(), nullable=False)

    account_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    account_email: Mapped[str] = mapped_column(String(100), nullable=False)

    provider_id: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(100), nullable=False)

    user_name: AssociationProxy[str] = association_proxy("user", "name")
    user_email: AssociationProxy[str] = association_proxy("user", "email")
    user: Mapped[User] = relationship(
        back_populates="oauth_accounts",
        viewonly=True,
        innerjoin=True,
        lazy="joined",
    )
