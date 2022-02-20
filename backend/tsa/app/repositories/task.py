from typing import List

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from tsa.app.database import DatabaseRepository
from tsa.app.schemas.task import Task, TaskModel


class TaskRepository(DatabaseRepository):
    async def create(self, task: Task) -> Task:
        data = task.dict(exclude_none=True)
        statement = insert(TaskModel).values(**data).returning("*")

        raw_result = await self._connection.execute(statement)
        return Task(**raw_result.first())

    async def list(self, source_file_id: int) -> List[Task]:
        statement = select(TaskModel).where(TaskModel.source_file_id == source_file_id)

        raw_results = await self._connection.execute(statement)
        return [Task(**raw_result) for raw_result in raw_results.all()]

    async def get(self, task_id: int) -> Task:
        statement = select(TaskModel).where(TaskModel.id == task_id)

        raw_result = await self._connection.execute(statement)
        return TaskModel(**raw_result.one())
