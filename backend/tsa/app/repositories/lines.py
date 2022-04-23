from typing import List

from tsa.app.schemas.base import LineModel
from tsa.app.schemas.line import Lines, LinesBase

from .base import DatabaseRepository


class LinesRepository(DatabaseRepository):
    model = LineModel
    data_class = LinesBase
    sort_keys = [LineModel.c.id]

    async def create(self, lines: Lines, *, task_id: int) -> LinesBase:
        return await super().create(lines, task_id=task_id)

    async def get_many(self, task_id: int) -> List[LinesBase]:
        return await super().get_many(LineModel.c.task_id == task_id)
