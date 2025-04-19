import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from msgspec import Struct

Retval = TypeVar("Retval")
P = ParamSpec("P")

type FnRequest = Callable[P, Retval] | Callable[P, Coroutine[Any, Any, Retval]]


class RetryInfo(Struct, frozen=True, eq=False, gc=False):
    current_retries: int
    next_delay: float
    exception: Exception


def retry(
    *,
    retries: int = 3,
    delay: float = 0.0,
    on_exception: Callable[[RetryInfo], None] | None = None,
) -> Callable[[FnRequest], FnRequest]:
    def outer(fn: FnRequest) -> FnRequest:
        if asyncio.coroutines.iscoroutine(fn):

            @wraps(fn)
            async def inner(*args: P.args, **kwargs: P.kwargs) -> Retval:  # type: ignore
                for current_retrie in range(1, retries + 1):
                    try:
                        return await fn(*args, **kwargs)  # type: ignore
                    except Exception as e:
                        if on_exception is not None:
                            on_exception(RetryInfo(current_retries=current_retrie, next_delay=delay, exception=e))
                        await asyncio.sleep(delay)

                return await fn(*args, **kwargs)  # type: ignore
        else:

            @wraps(fn)
            def inner(*args: P.args, **kwargs: P.kwargs) -> Retval:  # type: ignore
                for current_retrie in range(1, retries + 1):
                    try:
                        return fn(*args, **kwargs)  # type: ignore
                    except Exception as e:
                        if on_exception is not None:
                            on_exception(RetryInfo(current_retries=current_retrie, next_delay=delay, exception=e))
                        asyncio.run(asyncio.sleep(delay))

                return fn(*args, **kwargs)  # type: ignore

        return inner

    return outer
