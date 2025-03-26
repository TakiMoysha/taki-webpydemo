import json
import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Final, Self

from litestar.serialization import decode_json, encode_json
from litestar.utils.module_loader import module_to_os_path
from redis.asyncio import Redis
from slugify import slugify
from sqlalchemy import NullPool, event
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

from demoapp.config.consts import BAD_VALUE
from demoapp.lib.utils import get_random_string

APP_DIR: Final[Path] = module_to_os_path("app")
TRUE_VALUES = ("1", "true", "True", "T")


@dataclass
class AppSettings:
    URL: str = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:8000"))
    DEBUG: bool = field(default_factory=lambda: os.getenv("LITESTAR_DEBUG", "False") in TRUE_VALUES)
    SECRET_KEY: str = field(default_factory=lambda: os.getenv("SECRET_KEY", get_random_string(32)))
    NAME: str = field(default_factory=lambda: "PyWeb Demo Project")
    ALLOWED_CORS_ORIGINS: list[str] | str = field(default_factory=lambda: os.getenv("ALLOWED_CORS_ORIGINS", '["*"]'))
    CSRF_COOKIE_NAME: str = field(default_factory=lambda: "csrftoken")
    CSRF_COOKIE_SECURE: bool = field(default_factory=lambda: False)
    JWT_ENCRYPTION_ALGORITHM: str = field(default_factory=lambda: "HS256")

    @property
    def slug(self) -> str:
        return slugify(self.NAME.lower())

    @property
    def version(self) -> str:
        from demoapp.__about__ import __version__

        return __version__

    def __post_init__(self) -> None:
        if self.SECRET_KEY is BAD_VALUE or len(self.SECRET_KEY) not in (16, 24, 32):
            msg = "BAD SECRET_KEY. SECRET_KEY should be set in .env file and be 16, 24 or 32 characters long."
            raise ValueError(msg, self.SECRET_KEY)

        if not isinstance(self.ALLOWED_CORS_ORIGINS, str):
            return

        if self.ALLOWED_CORS_ORIGINS.startswith("[") and self.ALLOWED_CORS_ORIGINS.endswith("]"):
            try:
                self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
            except (SyntaxError, ValueError):
                msg = "ALLOWED_CORS_ORIGINS is not a valid list representation."
                raise ValueError(msg) from None
        else:
            self.ALLOWED_CORS_ORIGINS = [host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")]


@dataclass
class DatabaseSettings:
    ECHO: bool = field(default_factory=lambda: os.getenv("DATABASE_ECHO", "False") in TRUE_VALUES)
    ECHO_POOL: bool = field(default_factory=lambda: os.getenv("DATABASE_ECHO_POOL", "False") in TRUE_VALUES)
    POOL_DISABLED: bool = field(default_factory=lambda: os.getenv("DATABASE_POOL_DISABLED", "False") in TRUE_VALUES)
    POOL_MAX_OVERFLOW: int = field(default_factory=lambda: int(os.getenv("DATABASE_MAX_POOL_OVERFLOW", "10")))
    POOL_SIZE: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_SIZE", "5")))
    POOL_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_TIMEOUT", "30")))
    POOL_RECYCLE: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_RECYCLE", "300")))
    POOL_PRE_PING: bool = field(default_factory=lambda: os.getenv("DATABASE_PRE_POOL_PING", "False") in TRUE_VALUES)
    URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///tmp/db.sqlite3"))

    MIGRATION_VERSION_TABLE: str = "alembic_version"
    MIGRATION_PATH: str = f"{APP_DIR}/db/migrations"
    MIGRATION_CONFIG: str = f"{APP_DIR}/db/migrations/alembic.ini"
    FIXTURE_PATH: str = f"{APP_DIR}/db/fixtures"

    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance

        if self.URL.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                pool_use_lifo=True,  # use lifo to reduce the number of idle connections
                poolclass=NullPool if self.POOL_DISABLED else None,
            )  # See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
                """Using msgspec for serialization of the json column values means that the
                output is binary, not `str` like `json.dumps` would output.
                SQLAlchemy expects that the json serializer returns `str` and calls `.encode()` on the value to
                turn it to bytes before writing to the JSONB column. I'd need to either wrap `serialization.to_json` to
                return a `str` so that SQLAlchemy could then convert it to binary, or do the following, which
                changes the behaviour of the dialect to expect a binary value from the serializer.
                See Also https://github.com/sqlalchemy/sqlalchemy/blob/14bfbadfdf9260a1c40f63b31641b27fe9de12a0/lib/sqlalchemy/dialects/postgresql/asyncpg.py#L934  pylint: disable=line-too-long
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

        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )  # [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker]

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
                """Override the default begin statement.  The disables the built in begin execution."""
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
                """Emits a custom begin"""
                dbapi_connection.exec_driver_sql("BEGIN")

        else:
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
        self._engine_instance = engine
        return self._engine_instance


@dataclass
class ServerSettings:
    HOST: str = field(default_factory=lambda: os.getenv("SERVER_HOST", "localhost"))
    PORT: int = field(default_factory=lambda: int(os.getenv("SERVER_PORT", "8000")))
    RELOAD: bool = field(default_factory=lambda: os.getenv("SERVER_RELOAD", "False") in TRUE_VALUES)
    KEEP_ALIVE: int = field(default_factory=lambda: int(os.getenv("SERVER_KEEP_ALIVE", "60")))
    WATCH_DIRS: list[str] = field(default_factory=lambda: os.getenv("SERVER_WATCH_DIRS", f"{APP_DIR}").split(","))


@dataclass
class CacheSettings:
    URL: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    SOCKET_CONNECT_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("REDIS_CONNECT_TIMEOUT", "5")))
    HEALTH_CHECK_INTERVAL: int = field(default_factory=lambda: int(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", "5")))
    SOCKET_KEEPALIVE: bool = field(default_factory=lambda: os.getenv("REDIS_SOCKET_KEEPALIVE", "True") in TRUE_VALUES)

    _redis_instance: Redis | None = None

    @property
    def client(self) -> Redis:
        return self.get_client()

    def get_client(self) -> Redis:
        if self._redis_instance is not None:
            return self._redis_instance

        self._redis_instance = Redis.from_url(
            url=self.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=self.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=self.SOCKET_KEEPALIVE,
            health_check_interval=self.HEALTH_CHECK_INTERVAL,
        )
        return self._redis_instance


@dataclass
class LogSettings:
    LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    SAQ_LEVEL: str = logging._levelToName[logging.WARNING]
    SQLALCHEMY_LEVEL: str = logging._levelToName[logging.WARNING]
    UVICORN_ACCESS_LEVEL: str = logging._levelToName[logging.ERROR]
    UVICORN_ERROR_LEVEL: str = logging._levelToName[logging.WARNING]
    GRANIAN_ACCESS_LEVEL: str = logging._levelToName[logging.ERROR]
    GRANIAN_ERROR_LEVEL: str = logging._levelToName[logging.WARNING]


@dataclass
class SaqSettings:
    PROCESSES: int = field(default_factory=lambda: int(os.getenv("SAQ_PROCESSES", "1")))
    CUNCURRENCY: int = field(default_factory=lambda: int(os.getenv("SAQ_CONCURRENCY", "10")))
    USE_SERVER_LIFESPAN: bool = True


@dataclass
class AppConfig:
    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    cache: CacheSettings = field(default_factory=CacheSettings)
    log: LogSettings = field(default_factory=LogSettings)
    saq: SaqSettings = field(default_factory=SaqSettings)

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> Self:
        from litestar.cli._utils import console

        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if env_file.is_file():
            from dotenv import load_dotenv

            console.print(f"[yellow] Using {dotenv_filename}[/]")
            load_dotenv(env_file, override=True)

        return cls()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> AppConfig:
    return AppConfig.from_env()
