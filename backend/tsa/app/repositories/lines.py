from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from tsa.app.database import DatabaseRepository
from tsa.app.schemas.line import Lines, LinesBase, LinesModel


class LinesRepository(DatabaseRepository):
    async def create(self, task_id: int, lines: Lines) -> LinesBase:
        data = lines.dict(exclude_none=True)
        statement = insert(LinesModel).values(**data, task_id=task_id).returning("*")

        raw_result = await self._connection.execute(statement)
        return LinesBase.from_db_dict(raw_result.first())

    async def get(self, lines_id: int) -> LinesBase:
        statement = select(LinesModel).where(LinesModel.id == lines_id)

        raw_result = await self._connection.execute(statement)
        return LinesBase.from_db_dict(raw_result.one())
