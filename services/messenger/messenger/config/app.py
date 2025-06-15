import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Final

from litestar.serialization import decode_json, encode_json
from litestar.utils.module_loader import module_to_os_path
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from messenger.lib.database.hooks import set_postgres_hooks, set_sqlite_hooks

from wsdk.config import get_upcast_env

PROJECT_HOME: Final[Path] = module_to_os_path(get_upcast_env("PROJECT_HOME", "messenger"))


@dataclass
class AppSettings:
    DEBUG: bool = field(default_factory=lambda: get_upcast_env("LITESTAR_DEBUG", False))
    NAME: str = field(default_factory=lambda: get_upcast_env("APP_NAME", "Demo - Messenger"))
    URL: str = field(default_factory=lambda: get_upcast_env("APP_URL", "http://localhost:9001"))
    SECRET_KEY: str = field(default_factory=lambda: get_upcast_env("SECRET_KEY", "_dont_expose_me_"))

    @property
    def version(self) -> str:
        from messenger.__about__ import __version__

        return __version__


@dataclass
class LoggingSettings:
    LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    SAQ_LEVEL: str = logging._levelToName[logging.WARNING]
    SQLALCHEMY_LEVEL: str = logging._levelToName[logging.WARNING]
    UVICORN_ACCESS_LEVEL: str = logging._levelToName[logging.ERROR]
    UVICORN_ERROR_LEVEL: str = logging._levelToName[logging.WARNING]


@dataclass
class KafkaSettings:
    BOOTSTRAP_SERVERS: str = field(default_factory=lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))

    NEW_MESSAGE_TOPIK: str = field(default_factory=lambda: os.getenv("KAFKA_NEW_MESSAGE_TOPIC", "new-message-topic"))
    NEW_CHAT_TOPIC: str = field(default_factory=lambda: os.getenv("KAFKA_NEW_CHAT_TOPIC", "new-chat-topic"))
    CHAT_DELETED_TOPIC: str = field(default_factory=lambda: os.getenv("KAFKA_CHAT_DELETED_TOPIC", "chat-deleted-topic"))
    NEW_LISTENER_ADDED_TOPIC: str = field(
        default_factory=lambda: os.getenv("KAFKA_NEW_LISTENER_ADDED_TOPIC", "listener-added-topic")
    )


@dataclass
class DatabaseSettings:
    URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///tmp/messenger.sqlite3"))

    ECHO: bool = field(default_factory=lambda: get_upcast_env("DATABASE_ECHO", False))
    ECHO_POOL: bool = field(default_factory=lambda: get_upcast_env("DATABASE_ECHO_POOL", False))

    # POOLING: bool = field(default_factory=lambda: get_upcast_env("DATABASE_POOLING", False))
    # POOL_DISABLED: bool = field(default_factory=lambda: get_upcast_env("DATABASE_POOL_DISABLED", False))
    # POOL_MAX_OVERFLOW: int = field(default_factory=lambda: get_upcast_env("DATABASE_MAX_POOL_OVERFLOW", 10))
    POOL_SIZE: int = field(default_factory=lambda: get_upcast_env("DATABASE_POOL_SIZE", 5))
    POOL_TIMEOUT: int = field(default_factory=lambda: get_upcast_env("DATABASE_POOL_TIMEOUT", 30))
    POOL_RECYCLE: int = field(default_factory=lambda: get_upcast_env("DATABASE_POOL_RECYCLE", 300))
    POOL_PRE_PING: bool = field(default_factory=lambda: get_upcast_env("DATABASE_PRE_POOL_PING", False))

    MIGRATION_VERSION_TABLE: str = "alembic_version"
    MIGRATION_PATH: str = f"{PROJECT_HOME}/database/migrations"
    MIGRATION_CONFIG: str = f"{PROJECT_HOME}/database/migrations/alembic.ini"
    FIXTURE_PATH: str = f"{PROJECT_HOME}/database/fixtures"

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
                pool_use_lifo=True,
            )
            set_postgres_hooks(engine)
        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
            )
            set_sqlite_hooks(engine)
        else:
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
            )

        self._engine_instance = engine
        return self._engine_instance


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    kafka: KafkaSettings = field(default_factory=KafkaSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()
