from litestar.connection import ASGIConnection

from messenger.auth import AuthJWTToken, UserFromToken


async def retrieve_user_handler(token: AuthJWTToken, conn: ASGIConnection) -> UserFromToken:
    return UserFromToken(id=token.sub)
