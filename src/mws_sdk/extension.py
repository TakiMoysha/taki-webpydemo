from typing import Any, Protocol


class IExtension(Protocol):
    def extend(self) -> None: ...


class BaseExtensionMixin(Protocol):
    """Can be used to expand global objects (rust-based objects, asgi, runtime, etc.)"""

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        self._extensions = {}

    def add_extension(self, name: str, extension: IExtension) -> None:
        self._extensions[name] = extension

    def get_extension(self, name: str) -> IExtension | None:
        return self._extensions.get(name, None)

    def __getattr__(self, name: str) -> IExtension:
        extension = self.get_extension(name)
        if extension is None:
            msg = f"'{self.__class__.__name__}' object has no attribute '{name}'"
            raise AttributeError(msg)

        return extension
