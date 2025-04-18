from typing import override

from click import Group
from litestar.config.app import AppConfig
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol

from wsdk.slugify import slugify


class ServerPlugin(InitPluginProtocol, CLIPluginProtocol):
    app_slug: str
    server: str

    @override
    def on_cli_init(self, cli: Group) -> None:
        from messenger.cli.commands import (
            show_database_schema,
        )
        from messenger.config import get_settings

        settings = get_settings()
        self.settings = settings
        self.version = settings.app.version
        self.app_slug = slugify(settings.app.NAME.lower())

        cli.add_command(show_database_schema(self.settings))

    @override
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        return super().on_app_init(app_config)
