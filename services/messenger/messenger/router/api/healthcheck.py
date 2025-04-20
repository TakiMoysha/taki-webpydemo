from typing import Annotated, Literal
from litestar import get, post
from litestar.controller import Controller
from litestar.openapi.spec import Example
from litestar.params import Body, Parameter

from messenger.database.models import Message
from messenger.lib.logger import get_logger
from messenger.router.api.annotates import TEnvironment

from messenger.config import get_settings

logger = get_logger()


@get("/healthcheck")
async def health_check() -> dict:
    logger.warning("test msg", obj={"status": "ok"})

    return {"status": "ok", "version": get_settings().app.version}
