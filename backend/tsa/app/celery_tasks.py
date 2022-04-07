from tsa import enums
from tsa.config import config
from tsa.dataclasses.frames import VideoFramesDataset
from tsa.models import init_detection_model, init_tracking_model
from tsa.processes import run_detection_and_tracking, store_tracks
from tsa.storage import FileStorageMethod
from tsa.app.celery import async_task
from tsa.app.database import database_connection
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import SourceFileBase, Task


async def _change_db_statuses(
    source_file_id: int, task_id: int, source_file_status: enums.SourceFileStatus, task_status: enums.TaskStatus
):
    async with database_connection() as db:
        await SourceFileRepository(db).update_state(source_file_id, source_file_status)
        await TaskRepository(db).update_state(task_id, task_status)


@async_task()
async def run_task(task_id: int):
    async with database_connection() as db:
        task = await TaskRepository(db).get_one(task_id)
        source_file = await SourceFileRepository(db).get_one(task.source_file_id)

    try:
        with config.override(**task.parameters):
            await _run_task(task, source_file)
    except Exception as exc:
        await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.failed)
        raise exc


async def _run_task(task: Task, source_file: SourceFileBase):
    await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processing, enums.TaskStatus.processing)

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

    await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.completed)
