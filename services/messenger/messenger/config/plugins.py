import sys
from litestar.logging.config import (
    LoggingConfig,
    StructLoggingConfig,
    default_structlog_processors,
    default_structlog_standard_lib_processors,
)
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.plugins.sqlalchemy import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from litestar.plugins.structlog import StructlogConfig
import structlog

from .app import get_settings

settings = get_settings()


alchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=settings.db.get_engine(),
    create_all=True,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False),
    alembic_config=AlembicAsyncConfig(
        version_table_name=settings.db.MIGRATION_VERSION_TABLE,
        script_config=settings.db.MIGRATION_CONFIG,
        script_location=settings.db.MIGRATION_PATH,
    ),
)


structlog_config = StructlogConfig(
    enable_middleware_logging=True,
    structlog_logging_config=StructLoggingConfig(
        log_exceptions="always",
        wrapper_class=structlog.make_filtering_bound_logger(settings.logging.LEVEL),
        standard_lib_logging_config=LoggingConfig(
            root={
                "level": settings.logging.LEVEL,
                "handlers": ["queue_listener"],
            },
            formatters={
                "standard": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.processors.add_log_level,
                        structlog.processors.JSONRenderer(),
                        structlog.processors.dict_tracebacks,
                        # structlog.processors.StackInfoRenderer(),
                        # structlog.dev.set_exc_info,
                        # structlog.processors.format_exc_info,
                        # structlog.processors.MaybeTimeStamper(fmt="%Y-%m-%d %H:%M"),
                        # structlog.processors.ExceptionPrettyPrinter(),
                        # structlog.dev.ConsoleRenderer(),
                        # structlog.processors.TimeStamper(fmt="unix"),
                        # default_structlog_processors(),
                    ],
                }
            },
            loggers={
                "uvicorn.access": {
                    "propagate": False,
                    # "level": settings.logging.UVICORN_ACCESS_LEVEL,
                    "level": "ERROR",
                    "handlers": ["queue_listener"],
                },
                "uvicorn.error": {
                    "propagate": False,
                    # "level": settings.logging.UVICORN_ERROR_LEVEL,
                    "level": "ERROR",
                    "handlers": ["queue_listener"],
                },
                # },
                "sqlalchemy.engine": {
                    "propagate": False,
                    # "level": settings.logging.SQLALCHEMY_LEVEL,
                    "level": "ERROR",
                    "handlers": ["queue_listener"],
                },
                "sqlalchemy.pool": {
                    "propagate": False,
                    # "level": settings.logging.SQLALCHEMY_LEVEL,
                    "level": "ERROR",
                    "handlers": ["queue_listener"],
                },
            },
        ),
    ),
    middleware_logging_config=LoggingMiddlewareConfig(
        request_log_fields=["method", "path", "path_params", "query"],
        response_log_fields=["status_code"],
    ),
)
