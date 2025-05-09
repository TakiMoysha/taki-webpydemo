from collections.abc import Sequence

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.plugins import PluginProtocol
from litestar.plugins.structlog import StructlogPlugin
from litestar_saq import SAQPlugin
from litestar_users import LitestarUsersPlugin
from litestar_vite import VitePlugin

from demoapp.config import app as config
from demoapp.server.server import ServerPlugin

from .users import litestar_users_config

__all__ = [
    "alchemy",
    "app_config",
    "get_plugins",
    "saq",
    "structlog",
    "users_plugin",
]

saq = SAQPlugin(config=config.saq_config)
structlog = StructlogPlugin(config=config.log_config)
alchemy = SQLAlchemyPlugin(config=config.alchemy_config)
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
        users_plugin,
    }
    return [plugin for plugin in plugins if plugin is not None]
