from collections.abc import Sequence

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.plugins import PluginProtocol
from litestar.plugins.structlog import StructlogPlugin
from litestar_granian import GranianPlugin
from litestar_saq import SAQPlugin
from litestar_users import LitestarUsersPlugin
from litestar_vite import VitePlugin

from app.config import app as config
from app.server.server import ServerPlugin

from .users import litestar_users_config

__all__ = [
    "alchemy",
    "app_config",
    "get_plugins",
    "granian",
    "saq",
    "structlog",
    "users_plugin",
]

saq = SAQPlugin(config=config.saq_config)
structlog = StructlogPlugin(config=config.log_config)
alchemy = SQLAlchemyPlugin(config=config.alchemy_config)
granian = GranianPlugin()
app_config = ServerPlugin()
channels_plugin = ChannelsPlugin(
    backend=MemoryChannelsBackend(history=20),
    channels=["general", "loopback"],
    arbitrary_channels_allowed=True,
)
users_plugin = LitestarUsersPlugin(config=litestar_users_config)


def get_plugins() -> Sequence[PluginProtocol]:
    """Exclude optional plugins if not enabled."""
    plugins = {
        structlog,
        saq,
        alchemy,
        granian,
        users_plugin,
    }
    return [plugin for plugin in plugins if plugin is not None]
