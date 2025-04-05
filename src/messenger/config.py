import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class AppSettings:
    DEBUG = field(default_factory=lambda: os.getenv("LITESTAR_DEBUG", "False") in ("True", "true"))
    NAME = field(default_factory=lambda: os.getenv("APP_NAME", "PyWeb Demo Project"))
    URL = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:9001"))

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
    BOOTSTRAP_SERVERS = field(default_factory=lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))


@dataclass
class DatabaseSettings:
    URL = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
        )
    )


@dataclass
class Settings:
    app = field(default_factory=AppSettings)
    kafka = field(default_factory=KafkaSettings)
    db = field(default_factory=DatabaseSettings)
    logging = field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()
