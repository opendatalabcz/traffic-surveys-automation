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
    sbatch_file_name = _generate_sbatch_file(source_file, task, config_file_name)

    subprocess.run(["sbatch", sbatch_file_name])


def _generate_config_file(task: Task):
    config_file_name = f"task_configs/config_{task.id}.json"

    with open(config_file_name, "w", encoding="utf-8") as config_file:
        simplejson.dump(task.parameters, config_file)

    return config_file_name


def _generate_sbatch_file(source_file, task: Task, config_file_name: str):
    sbatch_file_name = f"sbatch_configs/sbatch_{task.id}"

    with open(sbatch_file_name, "w", encoding="utf-8") as sbatch_file:
        sbatch_file.writelines(
            [
                "#!/bin/bash\n",
                "#SBATCH -N 1\n",
                "#SBATCH -c 1\n",
                "#SBATCH -p gpu\n",
                "#SBATCH -G 1\n",
                f"#SBATCH -J tsa_{task.id}\n",
                f"#SBATCH -e logs/tsa_{task.id}.err\n",
                f"#SBATCH -o logs/tsa_{task.id}.out\n",
            ]
        )
        sbatch_file.write(
            (
                "singularity exec --bind ~/models:/app/models --nv"
                f" --env MODELS_PATH=/app/models,DATABASE_NAME='{config.DB_NAME}',DATABASE_URL='{config.DB_URL}',"
                f"NEPTUNE_PROJECT='ondrejpudis/diploma-thesis',NEPTUNE_API_KEY='{config.NEPTUNE_API_KEY}'"
                " traffic-surveys-automation_master.sif"
                f" python /app/cli/analyse.py"
                f" -f {config.SOURCE_FILES_PATH}/{source_file.path}"
                f" -o {config.OUTPUT_FILES_PATH}/{task.output_path}"
                f" -d {task.models[0]} -t {task.models[1]} -i {source_file.id} {task.id} -c {config_file_name}\n"
            )
        )

    return sbatch_file_name
