from typing import List

from tsa import enums
from tsa.app.schemas.base import TaskModel
from tsa.app.schemas.task import Task

from .base import DatabaseRepository


class TaskRepository(DatabaseRepository[Task]):
    model = TaskModel
    data_class = Task
    sort_keys = [TaskModel.c.id]

    async def get_many(self, source_file_id: int) -> List[Task]:
        return await super().get_many(self.model.c.source_file_id == source_file_id)

    async def update_state(self, task_id: int, new_state: enums.TaskStatus):
        await self.update(conditions=[self.model.c.id == task_id], status=new_state.value)
