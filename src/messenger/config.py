import logging
import os
import secrets
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class AppSettings:
    DEBUG: bool = field(default_factory=lambda: os.getenv("LITESTAR_DEBUG", "False") in ("True", "true"))
    NAME: str = field(default_factory=lambda: os.getenv("APP_NAME", "Demo - Messenger"))
    URL: str = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:9001"))
    SECRET_KEY: str = field(default_factory=lambda: os.getenv("APP_SECRET_KEY", secrets.token_hex()))

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
    GRANIAN_ACCESS_LEVEL: str = logging._levelToName[logging.ERROR]
    GRANIAN_ERROR_LEVEL: str = logging._levelToName[logging.WARNING]


@dataclass
class KafkaSettings:
    BOOTSTRAP_SERVERS: str = field(default_factory=lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))


@dataclass
class DatabaseSettings:
    URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:"))


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    kafka: KafkaSettings = field(default_factory=KafkaSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()
