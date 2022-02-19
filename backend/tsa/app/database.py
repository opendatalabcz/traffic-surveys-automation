from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from tsa.config import config


def create_database_dsn() -> str:
    return f"postgresql+asyncpg://{config.DATABASE_URL}/{config.DATABASE_NAME}"


async_engine = create_async_engine(create_database_dsn(), pool_size=2, max_overflow=5)


async def get_session() -> AsyncConnection:
    async with async_engine.begin() as connection:
        yield connection
