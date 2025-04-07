import os
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass
class AppSettings:
    NAME = field(default_factory=lambda: os.getenv("APP_NAME", "Registry"))
    URL = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:10000"))

    @property
    def version(self) -> str:
        from registry.__about__ import __version__

        return __version__


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)


@lru_cache
def get_settings() -> dict:
    return {}
