from dataclasses import dataclass

from litestar.security.jwt.token import Token


@dataclass
class AuthJWTToken(Token):
    flag: bool = False


@dataclass
class UserFromToken:
    id: str
