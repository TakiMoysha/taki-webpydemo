import os
from dataclasses import dataclass, field
from functools import lru_cache

TRUE_VALUES = ["True", "true", "1", "yes", "y"]


@dataclass(frozen=True, slots=True)
class AppSettings:
    DEBUG: bool = field(default_factory=lambda: os.getenv("DEBUG", "False") in TRUE_VALUES)
    NAME: str = field(default_factory=lambda: os.getenv("APP_NAME", "Demo - Registry"))
    URL: str = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:10001"))
    SECRET_KEY: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "dont_expose_me"), repr=False)

    @property
    def version(self) -> str:
        from registry.__about__ import __version__

        return __version__


@dataclass(frozen=True, slots=True)
class LoggingSettings:
    APP_LOG_LEVEL: str = field(default_factory=lambda: os.getenv("APP_LOG_LEVEL", "INFO"))


@dataclass(frozen=True, slots=True)
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    log: LoggingSettings = field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    print(Settings())
    return Settings()
