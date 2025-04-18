from typing import Any

from litestar.serialization import decode_json, encode_json
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine


def set_postgres_hooks(engine: AsyncEngine) -> None:
    @event.listens_for(engine.sync_engine, "connect")
    def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
        """_sqla_on_connect

        update json columns ser/des as binary (see msgspec),
        alchemy expects "str", this change behaviour of the dialect to expect a binary value from the serializer
        """

        def encoder(bin_value: bytes) -> bytes:
            return b"\x01" + encode_json(bin_value)

        def decoder(bin_value: bytes) -> Any:
            # the byte is the \x01 prefix for jsonb used by PostgreSQL.
            # asyncpg returns it when format='binary'
            return decode_json(bin_value[1:])

        dbapi_connection.await_(
            dbapi_connection.driver_connection.set_type_codec(
                "jsonb",
                encoder=encoder,
                decoder=decoder,
                schema="pg_catalog",
                format="binary",
            ),
        )
        dbapi_connection.await_(
            dbapi_connection.driver_connection.set_type_codec(
                "json",
                encoder=encoder,
                decoder=decoder,
                schema="pg_catalog",
                format="binary",
            ),
        )


def set_sqlite_hooks(engine: AsyncEngine) -> None:
    @event.listens_for(engine.sync_engine, "connect")
    def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
        """Override the default begin statement. The disables the built in begin execution."""
        dbapi_connection.isolation_level = None

    @event.listens_for(engine.sync_engine, "begin")
    def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
        """Emits a custom begin"""
        dbapi_connection.exec_driver_sql("BEGIN")
