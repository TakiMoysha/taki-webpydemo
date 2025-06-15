from dataclasses import dataclass
from typing import Annotated

from litestar import get, post


@dataclass
class HealthValidationSchema:
    user_id: str
    action: str
    is_bot: bool = False


@get(path="/validation", guards=[])
async def demo_validation(
    param: Annotated[HealthValidationSchema, ""],
) -> dict[str, str]:
    return {"params": str(param)}
