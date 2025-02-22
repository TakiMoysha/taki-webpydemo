import os
import subprocess

ENVS = ["dev", "development", "stage", "staging", "prod", "production"]

DOCKER_ENV = """
# App
SECRET_KEY='secret-key'
LITESTAR_DEBUG=true
LITESTAR_HOST=0.0.0.0
LITESTAR_PORT=8000
APP_URL=http://localhost:${LITESTAR_PORT}

LOG_LEVEL=10
# Database
DATABASE_ECHO=true
DATABASE_ECHO_POOL=true
DATABASE_POOL_DISABLE=false
DATABASE_POOL_MAX_OVERFLOW=5
DATABASE_POOL_SIZE=5
DATABASE_POOL_TIMEOUT=30
DATABASE_URL=postgresql+asyncpg://app:app@db:5432/app

# Cache
REDIS_URL=redis://cache:6379/0

# Async Queue
SAQ_USE_SERVER_LIFESPAN=False # don't use with docker.
SAQ_WEB_ENABLED=True
SAQ_BACKGROUND_WORKERS=1
SAQ_CONCURRENCY=1

# VITE Pipeline
VITE_HOST=localhost
VITE_PORT=3006
VITE_HOT_RELOAD=True
VITE_DEV_MODE=True
ALLOWED_CORS_ORIGINS=["localhost:3006","localhost:8000"]
"""


TESTING_ENV = """
# App
SECRET_KEY='secret-key'

# Cache
VALKEY_PORT=6308
REDIS_URL=redis://localhost:${VALKEY_PORT}/0

SAQ_USE_SERVER_LIFESPAN=False # don't use with docker.
SAQ_WEB_ENABLED=True
SAQ_BACKGROUND_WORKERS=1
SAQ_CONCURRENCY=1

VITE_HOST=localhost
VITE_PORT=3006
VITE_HOT_RELOAD=True
VITE_DEV_MODE=True
VITE_USE_SERVER_LIFESPAN=False
"""

LOCAL_ENV = """
# App
SECRET_KEY='secret-key'
LITESTAR_DEBUG=true
LITESTAR_HOST=0.0.0.0
LITESTAR_PORT=8089
APP_URL=http://localhost:${LITESTAR_PORT}

LOG_LEVEL=10
# Database
DATABASE_ECHO=true
DATABASE_ECHO_POOL=true
DATABASE_POOL_DISABLE=false
DATABASE_POOL_MAX_OVERFLOW=5
DATABASE_POOL_SIZE=5
DATABASE_POOL_TIMEOUT=30
DATABASE_URL=postgresql+asyncpg://app:app@localhost:15432/app

REDIS_URL=redis://localhost:16379/0

# Worker
SAQ_USE_SERVER_LIFESPAN=True
SAQ_WEB_ENABLED=True
SAQ_BACKGROUND_WORKERS=1
SAQ_CONCURRENCY=1

VITE_HOST=localhost
VITE_PORT=5174
VITE_HOT_RELOAD=True
VITE_DEV_MODE=True
"""


def generate_secret_key(length: str) -> str:
    """call system openssl rand -base64 32"""

    return subprocess.run(
        ["openssl", "rand", "--base64", length],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def get_environment_config():
    """build environment config by env variable X_ENV"""
    _environment = os.getenv("X_ENV", "development").lower()
    if _environment not in ENVS:
        raise Exception(f"Bad environment type, available: {ENVS}")

    _secret_key_len = os.getenv("X_SECRET_LEN", 32)

    try:
        env_config = {
            "debug": True if _environment in ["dev", "development"] else False,
            "secret_key_length": int(_secret_key_len),
        }

        return env_config
    except Exception as err:
        err.add_note(
            f"get_settings_by_env: CHECK type of env generation setting: {_environment}; {_secret_key_len}",
        )
        raise


if __name__ == "__main__":
    gen_settings = get_environment_config()
    print("generation .env file with settings: ", gen_settings)

    filename_postfix = ".env" if not os.path.exists(".env") else ".tmp.env"

    with open(filename_postfix, "w") as env_file:
        for key, value in gen_settings.items():
            env_file.write(f"{key.upper()}={value}\n")
            # print(f"{key}={value}")
