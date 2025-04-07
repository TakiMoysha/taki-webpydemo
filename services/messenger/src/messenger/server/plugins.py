from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.security.jwt import JWTAuth

from messenger.auth import AuthJWTToken, UserFromToken
from messenger.config import get_settings
from messenger.lib.database import BaseModel
from messenger.server.dependencies import retrieve_user_handler

settings = get_settings()

jwt_auth = JWTAuth[UserFromToken](
    token_secret=settings.app.SECRET_KEY,
    retrieve_user_handler=retrieve_user_handler,
    token_cls=AuthJWTToken,
)


alchemy_plugin = SQLAlchemyPlugin(
    config=SQLAlchemyAsyncConfig(connection_string=settings.db.URL, create_all=True, metadata=BaseModel.metadata)
)


def get_plugins() -> tuple[SQLAlchemyPlugin, ...]:
    return (alchemy_plugin,)
