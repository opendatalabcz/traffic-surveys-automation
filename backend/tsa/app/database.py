from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from tsa.config import config


def create_database_dsn() -> str:
    return f"postgresql+asyncpg://{config.DATABASE_URL}/{config.DATABASE_NAME}"


async_engine = create_async_engine(create_database_dsn(), pool_size=2, max_overflow=5)


async def get_db_connection() -> AsyncConnection:
    async with async_engine.begin() as connection:
        yield connection


class DatabaseRepository:
    def __init__(self, db_connection: AsyncConnection = Depends(get_db_connection)):
        self._connection = db_connection
