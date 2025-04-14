import os

from wsdk.random import get_random_string


def get_os_secret_key(length: int = 32) -> str:
    return os.getenv("SECRET_KEY", get_random_string(length))
