from tsa import enums
from tsa.app.database import database_connection
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository


async def get_db_objects(task_id: int):
    async with database_connection() as db:
        task = await TaskRepository(db).get_one(task_id)
        source_file = await SourceFileRepository(db).get_one(task.source_file_id)

    return task, source_file


async def change_db_statuses(
    source_file_id: int, task_id: int, source_file_status: enums.SourceFileStatus, task_status: enums.TaskStatus
):
    async with database_connection() as db:
        await SourceFileRepository(db).update_state(source_file_id, source_file_status)
        await TaskRepository(db).update_state(task_id, task_status)
