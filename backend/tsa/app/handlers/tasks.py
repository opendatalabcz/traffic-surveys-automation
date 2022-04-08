from typing import Dict, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import StreamingResponse

from tsa import enums
from tsa.app.disk_manager import DiskManager
from tsa.app.internal.task_video import create_video
from tsa.app.internal.task_visualization import create_task_visualization
from tsa.app.repositories.lines import LinesRepository
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import Lines, LinesBase, TaskWithLines
from tsa.config import config, config_to_dict

router = APIRouter(prefix="/task", tags=["tasks"])


@router.get(
    "/configuration",
    description="Get the keys and default values of the default configuration.",
    response_model=Dict[str, Union[Optional[float], Optional[int]]],
    status_code=status.HTTP_200_OK,
)
async def default_configuration():
    return config_to_dict()


@router.get(
    "/{task_id}",
    description="Get details of a task.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "The task does not exist."}},
    response_model=TaskWithLines,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: int,
    task_repository: TaskRepository = Depends(TaskRepository),
    lines_repository: LinesRepository = Depends(LinesRepository),
) -> TaskWithLines:
    task = await task_repository.get_one(task_id)
    all_lines = await lines_repository.get_many(task_id)

    return TaskWithLines(**task.dict(), lines=all_lines)


@router.get(
    "/{task_id}/visualization",
    description="Generate a visualization of the processed task.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "The task is invalid for visualization."},
        status.HTTP_404_NOT_FOUND: {"description": "The task does not exist."},
    },
    response_class=StreamingResponse,
    response_description="Streaming response of the PNG data of a visualization image.",
    status_code=status.HTTP_200_OK,
)
async def visualization(
    task_id: int,
    minimum_path_length: int = config.VISUALIZATION_MIN_PATH_LENGTH,
    clusters: int = config.VISUALIZATION_N_CLUSTERS,
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
    task_repository: TaskRepository = Depends(TaskRepository),
    disk_manager: DiskManager = Depends(DiskManager),
):
    task = await task_repository.get_one(task_id)
    source_file = await source_file_repository.get_one(task.source_file_id)

    if task.status != enums.TaskStatus.completed:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Task is not completed yet. Status is {task.status.value}.")

    return create_task_visualization(
        task.output_path,
        source_file.path if disk_manager.exists_in_source_files_folder(source_file.path) else None,
        minimum_path_length,
        clusters,
    )


@router.get(
    "/{task_id}/video",
    description="Generate a video export of the processed task.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "The task is invalid for visualization."},
        status.HTTP_404_NOT_FOUND: {"description": "The task does not exist."},
    },
    response_class=StreamingResponse,
    response_description="Streaming response of the MP4 data.",
    status_code=status.HTTP_200_OK,
)
async def video(
    task_id: int,
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
    task_repository: TaskRepository = Depends(TaskRepository),
    disk_manager: DiskManager = Depends(DiskManager),
):
    task = await task_repository.get_one(task_id)
    source_file = await source_file_repository.get_one(task.source_file_id)

    if task.status != enums.TaskStatus.completed:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Task is not completed yet. Status is {task.status.value}.")

    if not disk_manager.exists_in_source_files_folder(source_file.path):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Original video file does not exist.")

    return create_video(
        source_file.path,
        task.output_path,
        task.parameters.get("VIDEO_FRAME_RATE", config.VIDEO_FRAME_RATE),
        task.parameters.get("VIDEO_SHOW_CLASS", config.VIDEO_SHOW_CLASS),
    )


@router.post(
    "/{task_id}/lines",
    description="Create lines for a given task. These lines can be used for counting.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "The task does not exist."}},
    response_model=LinesBase,
    status_code=status.HTTP_201_CREATED,
)
async def store_lines(
    task_id: int,
    lines: Lines,
    lines_repository: LinesRepository = Depends(LinesRepository),
) -> LinesBase:
    return await lines_repository.create(lines, task_id=task_id)
