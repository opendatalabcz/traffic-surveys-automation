import subprocess

import simplejson

from tsa.app.celery import async_task
from tsa.app.schemas import Task
from tsa.config import config

from .common import get_db_objects


@async_task()
async def schedule_task(task_id: int):
    task, source_file = await get_db_objects(task_id)

    config_file_name = _generate_config_file(task)

    subprocess.run(
        [
            "sbatch",
            "-N 1",
            "-c 1",
            "-p gpu",
            "-G 1",
            f"-J tsa_{task.id}",
            f"-e logs/tsa_{task.id}.err",
            f"-o logs/tsa_{task.id}.out",
            (
                "singularity exec --bind ~/models:/app/models --nv"
                f"--env='MODELS_PATH=/app/models,DATABASE_NAME={config.DB_NAME},DATABASE_URL={config.DB_URL}'"
                "traffic-surveys-automation_master.sif"
                f"python /app/cli/analyse.py -f ~/input/{source_file.path} -o ~/output/{task.output_path}"
                f"-d {task.models[0]} -t {task.models[1]} -i {source_file.id} {task.id} -c {config_file_name}"
            ),
        ]
    )


def _generate_config_file(task: Task):
    config_file_name = f"task_configs/config_{task.id}.json"

    with open(config_file_name, "w", encoding="utf-8") as config_file:
        simplejson.dump(task.parameters, config_file)

    return config_file_name
