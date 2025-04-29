import threading
from functools import wraps
from collections.abc import Callable


def thread_safe_cached(fn: Callable) -> Callable:
    cache = {}
    in_progress = {}
    lock = threading.Lock()

    @wraps(fn)
    def wrapper(*args: list, **kwargs: dict) -> Callable:
        key = (args, frozenset(kwargs.items()))
        print("WSDK_DEBUG: key", key)
        with lock:
            if key in cache:
                return cache[key]
            if key in in_progress:
                in_progress[key] = threading.Event()
                in_progress[key].clear()
                creator = True
            else:
                creator = False

        if creator:
            try:
                result = fn(*args, **kwargs)
                with lock:
                    cache[key] = result
            finally:
                in_progress[key].set()
                with lock:
                    del in_progress[key]
            return result

        in_progress[key].wait()
        with lock:
            return cache[key]

    return wrapper
