from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine

from messenger.lib.logger import get_logger

logger = get_logger("messenger")


async def inspect_database(engine: AsyncEngine):
    async with engine.connect() as conn:
        _data = []

        for schema in await conn.run_sync(lambda conn: inspect(conn).get_schema_names()):
            logger.debug(f"Schema: {schema}")
            for table in await conn.run_sync(lambda conn: inspect(conn).get_table_names(schema=schema)):
                logger.debug(f"Table: {table}")
                for column in await conn.run_sync(lambda conn: inspect(conn).get_columns(table, schema=schema)):
                    logger.debug(f"Column: {column}")
                    column_comment = column.get("comment")
                    _data.append(
                        (
                            schema,
                            table,
                            column["name"],
                            repr(column["type"]),
                            column["nullable"],
                            column_comment,
                            False,
                        )
                    )

            for view in await conn.run_sync(lambda conn: inspect(conn).get_view_names(schema=schema)):
                logger.debug(f"View: {view}")
                _data.append((schema, view, None, None, None, False, None, True))

        return _data
