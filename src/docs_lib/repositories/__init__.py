from docs_lib.repositories.types import IDocsFilesRepository


class LocalRepository(IDocsFilesRepository): ...


class GithubRepository(IDocsFilesRepository): ...


class MegaRepository(IDocsFilesRepository): ...
