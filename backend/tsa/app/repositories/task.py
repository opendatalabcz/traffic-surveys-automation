from typing import List

from tsa import enums
from tsa.app.schemas.task import Task, TaskModel

from .base import DatabaseRepository


class TaskRepository(DatabaseRepository[TaskModel, Task]):
    model = TaskModel
    data_class = Task

    async def get_many(self, source_file_id: int) -> List[Task]:
        return await super().get_many(TaskModel.source_file_id == source_file_id)

    async def update_state(self, task_id: int, new_state: enums.TaskStatus):
        await self.update(conditions=[self.model.id == task_id], status=new_state.value)
