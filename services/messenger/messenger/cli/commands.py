import asyncio

import click
from litestar import Litestar
from sqlalchemy import MetaData, inspect
from tabulate import tabulate

from messenger.config.app import Settings
from messenger.lib.logger import get_logger

logger = get_logger(__name__)


def show_database_schema(settings: Settings) -> click.Command:
    async def _inspect_db():
        meta = MetaData()
        engine = settings.db.get_engine()
        async with engine.sync_engine.connect() as conn:
            values = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names(),
            )

        return values

    @click.command(name="show-database-schema")
    def _show_db_schema(app: Litestar) -> None:
        values = asyncio.run(_inspect_db())
        click.echo(f"values: {values}")

        # table_format = tabulate(
        #     [(table.name, [c.name for c in table.columns]) for table in values],
        #     headers=["Table", "Columns"],
        # )
        # click.echo(f"Database schema:\n {table_format}")

    return _show_db_schema
