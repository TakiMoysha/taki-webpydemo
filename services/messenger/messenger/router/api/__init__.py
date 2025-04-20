from typing import Literal

from litestar import Router
from litestar.params import Parameter

from messenger.router.api.chat import ChatController
from messenger.router.api.healthcheck import health_check

from .annotates import TEnvironment

v1_router = Router(
    path="/v1",
    route_handlers=[
        ChatController,
    ],
)

api_router = Router(
    path="/api",
    route_handlers=[
        health_check,
        v1_router,
    ],
    parameters={
        "from": Parameter(TEnvironment, description="Environment", default="docker"),
    },
)
