from tsa.app.schemas.line import Lines, LinesBase, LinesModel

from .base import DatabaseRepository


class LinesRepository(DatabaseRepository[LinesModel, LinesBase]):
    model = LinesModel
    data_class = LinesBase

    async def create(self, lines: Lines, *, task_id: int) -> LinesBase:
        return await super().create(lines, task_id=task_id)
