from datetime import datetime

from tsa import enums
from tsa.app.celery_tasks import run_task
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas.task import NewTask, Task


def _generate_output_path(source_path: str) -> str:
    source_path_parts = source_path.rsplit(".", 1)
    return f"{source_path_parts[0]}_{datetime.now().isoformat()}.json"


async def create_task(task_repository: TaskRepository, new_task: NewTask, source_id: int, source_path: str) -> Task:
    task = Task(
        name=new_task.name,
        models=[new_task.detection_model.value, new_task.tracking_model.value],
        output_path=_generate_output_path(source_path),
        parameters=new_task.parameters,
        status=enums.TaskStatus.created,
        source_file_id=source_id,
    )
    saved_task = await task_repository.create(task)

    run_task.s(task_id=saved_task.id).apply_async()

    return saved_task
