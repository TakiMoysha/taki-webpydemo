from uuid import UUID
from advanced_alchemy.repository import SQLAlchemyAsyncRepository, SQLAlchemyAsyncSlugRepository
from advanced_alchemy.service import (
    ModelDictT,
    SQLAlchemyAsyncRepositoryService,
    is_dict,
    is_dict_with_field,
    is_dict_without_field,
    schema_dump,
)


class UserService(SQLAlchemyAsyncRepostioryService[m.User]):
    class UserRepository(SQLalchemyAsyncRepository[m.User]):
        model_type = m.User
