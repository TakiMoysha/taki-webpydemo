from litestar.events import listener
from messenger.lib.logger import get_logger

from .dependencies import provide_users_service

logger = get_logger(__name__)


@listener("user_created")
async def user_created_event_handler(user_id) -> None:
    await logger.ainfo("User created", user_id=user_id)

    async with get_session() as db_session:
        service = await anext(provide_users_service(db_session))
        obj = await service.find(id=user_id)

        if obj is None:
            await logger.aerror("User not found", user_id=user_id)
        else:
            await logger.ainfo("User found", user_id=user_id)
