from typing import Protocol

# !TODO: replace with proper types
type URL = str
type FSPath = str

type FilePath = URL | FSPath


class IDocsFilesRepository(Protocol):
    def load_content(self, path: FilePath) -> str: ...
