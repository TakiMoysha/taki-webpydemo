from typing import Self


class SingletonMixin:
    def __new__(cls, *args: list, **kwargs: dict) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._inicialized = False

        return cls._instance
