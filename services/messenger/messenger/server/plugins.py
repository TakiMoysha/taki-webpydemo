from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar.plugins.structlog import StructlogPlugin
from litestar.security.jwt import JWTAuth

from messenger.auth import AuthJWTToken, UserFromToken
from messenger.config import get_settings
from messenger.config.plugins import alchemy_config, structlog_config
from messenger.server.dependencies import retrieve_user_handler
from messenger.server.server import ServerPlugin

settings = get_settings()

jwt_auth = JWTAuth[UserFromToken](
    token_secret=settings.app.SECRET_KEY,
    retrieve_user_handler=retrieve_user_handler,
    token_cls=AuthJWTToken,
)

structlog_plugin = StructlogPlugin(config=structlog_config)

alchemy_plugin = SQLAlchemyPlugin(config=alchemy_config)


def get_plugins() -> tuple:
    return (structlog_plugin, alchemy_plugin, ServerPlugin())
