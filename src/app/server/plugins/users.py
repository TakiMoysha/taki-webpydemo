from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.security.session_auth import SessionAuth
from litestar_users import LitestarUsersConfig
from litestar_users.config import (
    AuthHandlerConfig,
    CurrentUserHandlerConfig,
    PasswordResetHandlerConfig,
    RegisterHandlerConfig,
    UserManagementHandlerConfig,
    VerificationHandlerConfig,
)

from app.config.base import get_settings
from app.db.models.users import User
from app.domain.dto import UserReadDTO, UserRegistrationDTO, UserUpdateDTO
from app.domain.services.users import UserService

settings = get_settings()

litestar_users_config = LitestarUsersConfig(
    auth_backend_class=SessionAuth,
    session_backend_config=ServerSideSessionConfig(),
    secret=settings.app.SECRET_KEY,
    user_model=User,  # pyright: ignore
    user_read_dto=UserReadDTO,
    user_registration_dto=UserRegistrationDTO,
    user_update_dto=UserUpdateDTO,
    user_service_class=UserService,
    auth_handler_config=AuthHandlerConfig(),
    current_user_handler_config=CurrentUserHandlerConfig(),
    password_reset_handler_config=PasswordResetHandlerConfig(),
    register_handler_config=RegisterHandlerConfig(),
    user_management_handler_config=UserManagementHandlerConfig(),
    verification_handler_config=VerificationHandlerConfig(),
)
