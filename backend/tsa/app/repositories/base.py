from typing import Callable, Generic, List, TypeVar

from databases import Database
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Table, and_, delete, insert, select, update

from tsa.app.database import get_db_connection
from tsa.app.exceptions import NotFoundError

K = TypeVar("K", Callable, BaseModel)


class DatabaseRepository(Generic[K]):
    model: Table
    data_class: K

    sort_keys: List = []

    def __init__(self, connection: Database = Depends(get_db_connection)):
        self._connection = connection

    async def create(self, instance: K, **additional_attributes) -> K:
        result = await self._connection.fetch_one(
            insert(self.model)
            .values(**instance.dict(exclude_none=True), **additional_attributes)
            .returning(self.model),
        )
        return self.data_class(**result)

    async def get_one(self, primary_key: int) -> K:
        result = await self._connection.fetch_one(
            select(self.model).where(self.model.c.id == primary_key),
        )

        if not result:
            raise NotFoundError(self.model.__name__, primary_key)

        return self.data_class(**result)

    async def get_many(self, *conditions) -> List[K]:
        statement = select(self.model)

        if conditions:
            statement = statement.where(and_(*conditions))

        statement = statement.order_by(*self.sort_keys)

        results = await self._connection.fetch_all(statement)
        return [self.data_class(**result) for result in results]

    async def update(self, *, conditions: List, **values):
        await self._connection.execute(
            update(self.model).values(**values).where(and_(*conditions)),
        )

    async def delete(self, primary_key: int):
        await self._connection.execute(
            delete(self.model).where(self.model.c.id == primary_key),
        )
