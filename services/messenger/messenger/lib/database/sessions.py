from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def get_session(engine: AsyncEngine, *args, **kwargs) -> AsyncSession:
    return async_sessionmaker(bind=engine)(*args, **kwargs)
