from typing import override

from click import Group
from litestar import Request
from litestar.config.app import AppConfig
from litestar.config.response_cache import (
    ResponseCacheConfig,
    default_cache_key_builder,
)
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol
from litestar.stores.redis import RedisStore
from litestar.stores.registry import StoreRegistry
from redis.asyncio import Redis


class ServerPlugin(InitPluginProtocol, CLIPluginProtocol):
    __slots__ = ("app_slug", "redis")

    redis: Redis
    app_slug: str

    @override
    def on_cli_init(self, cli: Group) -> None:
        from demoapp.cli.commands import (
            show_database_schema,
        )
        from demoapp.config import get_settings

        settings = get_settings()
        self.app_slug = settings.app.slug
        self.version = settings.app.version
        self.redis = settings.cache.get_client()

    @override
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        return super().on_app_init(app_config)
