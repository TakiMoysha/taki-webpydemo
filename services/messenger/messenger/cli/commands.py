import asyncio

import click
from litestar import Litestar
from sqlalchemy import MetaData, inspect
from tabulate import tabulate

from messenger.config.app import Settings
from messenger.lib.database.metadata import inspect_database
from messenger.lib.logger import get_logger

logger = get_logger(__name__)


def show_database_schema(settings: Settings) -> click.Command:
    @click.command(name="show-database-schema")
    def _show_db_schema(app: Litestar) -> None:
        engine = settings.db.get_engine()
        values = asyncio.run(inspect_database(engine))
        table_format = tabulate(
            values,
            headers=["Schema", "Table", "Column", "Type", "Nullable", "Comment", "PK", "View"],
        )
        click.echo(table_format)

    return _show_db_schema
