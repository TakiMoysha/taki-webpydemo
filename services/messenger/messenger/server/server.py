from typing import override

from click import Group
from litestar.config.app import AppConfig
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol
from slugify import slugify


class ServerPlugin(InitPluginProtocol, CLIPluginProtocol):
    __slots__ = ("app_slug", "kafka")

    app_slug: str
    kafka: None  # !TODO:

    @override
    def on_cli_init(self, cli: Group) -> None:
        from messenger.config import get_settings

        settings = get_settings()
        self.version = settings.app.version
        self.app_slug = slugify(settings.app.NAME.lower())

    @override
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        return super().on_app_init(app_config)
