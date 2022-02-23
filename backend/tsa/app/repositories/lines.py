from typing import List

from tsa.app.schemas.line import Lines, LinesBase, LinesModel

from .base import DatabaseRepository


class LinesRepository(DatabaseRepository[LinesModel, LinesBase]):
    model = LinesModel
    data_class = LinesBase

    async def create(self, lines: Lines, *, task_id: int) -> LinesBase:
        return await super().create(lines, task_id=task_id)

    async def get_many(self, task_id: int) -> List[LinesBase]:
        return await super().get_many(LinesModel.task_id == task_id)
