from contextlib import asynccontextmanager

from databases import Database

from tsa.config import config


def create_database_dsn() -> str:
    return f"postgresql+asyncpg://{config.DB_URL}/{config.DB_NAME}"


db_engine = Database(create_database_dsn())


@asynccontextmanager
async def database_connection() -> Database:
    async with db_engine as db:
        yield db


async def get_db_connection() -> Database:
    async with db_engine.transaction():
        yield db_engine
