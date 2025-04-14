from contextlib import contextmanager

from wsdk.exceptions import BaseDevKitError


@contextmanager
def map_errors(map: dict[Exception, BaseDevKitError], *args, **kwrags):
    try:
        yield None
    except Exception as e:
        raise map.get(e, BaseDevKitError)(*args, **kwrags)
