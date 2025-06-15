from typing import Any

from litestar import Request
from litestar_users.service import BaseUserService

from demoapp.db.models.users import User
from demoapp.lib.logger import Logger


class UserService(BaseUserService[User, Any, Any]):  # type: ignore[type-var]
    async def post_login_hook(self, user: User, request: Request | None = None) -> None:
        Logger.warning("post_login_hook +1")
        user.login_count += 1
