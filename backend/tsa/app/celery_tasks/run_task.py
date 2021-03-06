from tsa import enums
from tsa.app.celery import async_task
from tsa.app.schemas import SourceFileBase, Task
from tsa.config import config
from tsa.dataclasses.frames import VideoFramesDataset
from tsa.models import init_detection_model, init_tracking_model
from tsa.monitoring import Monitor
from tsa.processes import run_detection_and_tracking, store_tracks
from tsa.storage import FileStorageMethod

from .common import change_db_statuses, get_db_objects


@async_task()
async def run_task(task_id: int):
    task, source_file = await get_db_objects(task_id)

    try:
        with config.override(**task.parameters):
            await _run_task(task, source_file)
    except Exception as exc:
        await change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.failed)
        raise exc


async def _run_task(task: Task, source_file: SourceFileBase):
    await change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processing, enums.TaskStatus.processing)

    with Monitor.neptune_monitor(
        "tsa-analysis", [task.models[0], task.models[1], str(source_file.path), str(task.output_path)]
    ):
        video_dataset = VideoFramesDataset(
            config.SOURCE_FILES_PATH / source_file.path, config.VIDEO_FRAME_RATE, config.VIDEO_MAX_FRAMES
        )

        prediction_model = init_detection_model(enums.DetectionModels(task.models[0]))
        tracking_model = init_tracking_model(enums.TrackingModel(task.models[1]))

        tracking_generator = run_detection_and_tracking(video_dataset, prediction_model, tracking_model)

        store_tracks(
            tracking_generator,
            FileStorageMethod(config.OUTPUT_FILES_PATH / task.output_path),
        )

    await change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.completed)
