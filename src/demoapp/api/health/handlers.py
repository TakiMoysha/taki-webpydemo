from typing import Annotated

from litestar import get, post
from pydantic import BaseModel


class HealthValidationSchema(BaseModel):
    user_id: str
    action: str
    is_bot: bool = False


@get(path="/validation", guards=[])
async def demo_validation(
    param: Annotated[HealthValidationSchema, ""],
) -> dict[str, str]:
    return {"params": str(param)}
