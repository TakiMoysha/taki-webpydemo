from asyncio import sleep
from collections.abc import Callable
from functools import wraps
from time import time
from typing import Any

from wsdk.exceptions import BaseDevKitError

FnRequest = Callable[..., Any]


def aretry_on_exception(attempts: int = 3, delay: int = 1) -> FnRequest:
    def wrapper(fn: FnRequest) -> FnRequest:
        @wraps(fn)
        async def _retry_on_exception(*args: list, **kwargs: dict) -> Any:
            for _ in range(attempts):
                try:
                    result = await fn(*args, **kwargs)
                except BaseDevKitError as err:
                    result = err
                    await sleep(delay)

            if isinstance(result, BaseDevKitError):
                raise result

            return result

        return _retry_on_exception

    return wrapper


def atimer(fn: FnRequest) -> FnRequest:
    @wraps(fn)
    async def _timer(*args: list, **kwargs: dict) -> Any:
        start = time.perf_counter()
        result = await fn(*args, **kwargs)
        end = time.perf_counter()
        print(f"{fn.__name__} took {end - start} seconds")
        return result

    return _timer
