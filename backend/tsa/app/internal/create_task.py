import hashlib
from typing import Dict

import simplejson

from tsa import enums
from tsa.app.celery_tasks import run_task, schedule_task
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas.task import NewTask, Task
from tsa.config import config

CELERY_TASK_MAPPING = {
    enums.CeleryTask.run.name: run_task,
    enums.CeleryTask.schedule.name: schedule_task,
}


def _generate_output_path(source_path: str, detection_model: str, tracking_model: str, parameters: Dict) -> str:
    source_path_parts = source_path.rsplit(".", 1)
    parameters_json = simplejson.dumps(parameters)
    parameters_hash = hashlib.md5(parameters_json.encode())
    return f"{source_path_parts[0]}_{detection_model}_{tracking_model}_{parameters_hash.hexdigest()[:7]}.json"


async def create_task(task_repository: TaskRepository, new_task: NewTask, source_id: int, source_path: str) -> Task:
    task = Task(
        name=new_task.name,
        models=[new_task.detection_model.value, new_task.tracking_model.value],
        output_path=_generate_output_path(
            source_path, new_task.detection_model.value, new_task.tracking_model.value, new_task.parameters
        ),
        parameters=new_task.parameters,
        status=enums.TaskStatus.created,
        source_file_id=source_id,
    )
    saved_task = await task_repository.create(task)

    celery_task = CELERY_TASK_MAPPING[config.CELERY_TASK_TYPE]
    celery_task.s(task_id=saved_task.id).apply_async()

    return saved_task
