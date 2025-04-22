import os
from pathlib import Path
from wsdk.config import get_upcast_env


def test_wsdk_upcast_config() -> None:
    version_env = "TEST_VERSION"
    debug_env = "TEST_DEBUG"
    path_env = "TEST_PATH"

    os.environ[version_env] = "0.0.0"
    os.environ[debug_env] = "yes"
    os.environ[path_env] = str(Path.cwd())

    a = get_upcast_env(version_env, "0.0.0")
    assert isinstance(a, str)
    assert a == "0.0.0"

    b = get_upcast_env(debug_env, True)
    assert isinstance(b, bool)
    assert b is True

    c = get_upcast_env(path_env, Path.cwd())
    assert isinstance(c, Path)
    assert c == Path.cwd()
