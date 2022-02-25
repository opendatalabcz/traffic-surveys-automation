from typing import Callable, Generic, List, TypeVar

from fastapi import Depends
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlmodel import SQLModel

from tsa.app.database import get_db_connection

T = TypeVar("T", SQLModel, SQLModel)
K = TypeVar("K", Callable, SQLModel)


class DatabaseRepository(Generic[T, K]):
    model: T
    data_class: K

    def __init__(self, connection: AsyncConnection = Depends(get_db_connection)):
        self._connection = connection

    async def create(self, instance: K, **additional_attributes) -> K:
        result = await self._execute_statement(
            insert(self.model).values(**instance.dict(exclude_none=True), **additional_attributes).returning("*"),
        )
        return self.data_class(**result.first())

    async def get_one(self, primary_key: int) -> K:
        result = await self._execute_statement(
            select(self.model).where(self.model.id == primary_key),
        )
        return self.data_class(**result.one())

    async def get_many(self, *conditions) -> List[K]:
        statement = select(self.model)

        if conditions:
            statement = statement.where(and_(*conditions))

        results = await self._execute_statement(statement)
        return [self.data_class(**result) for result in results.all()]

    async def update(self, *, conditions: List, **values):
        await self._execute_statement(
            update(self.model).values(**values).where(and_(*conditions)),
        )

    async def delete(self, primary_key: int):
        await self._execute_statement(
            delete(self.model).where(self.model.id == primary_key),
        )

    async def _execute_statement(self, statement) -> Result:
        return await self._connection.execute(statement)
