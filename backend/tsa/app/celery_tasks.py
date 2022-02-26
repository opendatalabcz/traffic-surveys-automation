from tsa import enums
from tsa.config import config
from tsa.datasets import VideoFramesDataset
from tsa.models import abstract, detection, tracking
from tsa.processes import run_detection_and_tracking, store_tracks
from tsa.storage import VideoStorageMethod
from tsa.app.celery import async_task
from tsa.app.database import db_connection
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import SourceFileBase, Task

DETECTION_MODEL_MAPPING = {
    enums.DetectionModels.efficientdet_d5_adv_prop: detection.EfficientDetD5AdvPropAA,
    enums.DetectionModels.efficientdet_d6: detection.EfficientDetD6,
}

TRACKING_MODEL_MAPPING = {
    enums.TrackingModel.simple_sort: tracking.SimpleSORT,
    enums.TrackingModel.deep_sort: tracking.DeepSORT,
}


def _init_detection_model(model_name: enums.DetectionModels) -> abstract.PredictableModel:
    model = DETECTION_MODEL_MAPPING[model_name]
    return model(
        config.ED_MAX_OUTPUTS,
        config.ED_IOU_THRESHOLD,
        config.ED_SCORE_THRESHOLD,
        config.ED_NSM_SIGMA,
        config.ED_BATCH_SIZE,
    )


def _init_tracking_model(model_name: enums.TrackingModel) -> abstract.TrackableModel:
    if model_name == enums.TrackingModel.deep_sort:
        return tracking.DeepSORT(
            config.DEEP_SORT_MIN_UPDATES,
            config.DEEP_SORT_MAX_AGE,
            config.DEEP_SORT_IOU_THRESHOLD,
            config.DEEP_SORT_MAX_COSINE_DISTANCE,
            config.DEEP_SORT_MAX_MEMORY_SIZE,
        )
    return tracking.SimpleSORT(
        config.SORT_MIN_UPDATES,
        config.SORT_MAX_AGE,
        config.SORT_IOU_THRESHOLD,
    )


async def _change_db_statuses(
    source_file_id: int, task_id: int, source_file_status: enums.SourceFileStatus, task_status: enums.TaskStatus
):
    async with db_connection() as connection:
        await SourceFileRepository(connection).update_state(source_file_id, source_file_status)
        await TaskRepository(connection).update_state(task_id, task_status)


@async_task()
async def run_task(task_id: int):
    async with db_connection() as connection:
        task = await TaskRepository(connection).get_one(task_id)
        source_file = await SourceFileRepository(connection).get_one(task.source_file_id)

    try:
        with config.override(**task.parameters):
            await _run_task(task, source_file)
    except Exception as exc:
        await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.failed)
        raise exc


async def _run_task(task: Task, source_file: SourceFileBase):
    await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processing, enums.TaskStatus.processing)

    video_dataset = VideoFramesDataset(
        str(config.SOURCE_FILES_PATH / source_file.path), config.VIDEO_FRAME_RATE, config.VIDEO_MAX_FRAMES
    )
    video_statistics = video_dataset.video_statistics

    prediction_model = _init_detection_model(enums.DetectionModels(task.models[0]))
    tracking_model = _init_tracking_model(enums.TrackingModel(task.models[1]))

    tracking_generator = run_detection_and_tracking(video_dataset, prediction_model, tracking_model)

    store_tracks(
        tracking_generator,
        VideoStorageMethod(
            str(config.OUTPUT_FILES_PATH / task.output_path),
            float(video_statistics.frame_rate),
            video_statistics.resolution,
        ),
    )

    await _change_db_statuses(source_file.id, task.id, enums.SourceFileStatus.processed, enums.TaskStatus.completed)
