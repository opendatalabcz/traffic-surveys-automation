from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import StreamingResponse

from tsa import enums
from tsa.app.internal.task_visualization import create_task_visualization
from tsa.app.repositories.lines import LinesRepository
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import Lines, LinesBase
from tsa.config import config

router = APIRouter(prefix="/task", tags=["tasks"])


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
):
    task = await task_repository.get_one(task_id)
    source_file = await source_file_repository.get_one(task.source_file_id)

    if task.output_method != enums.TaskOutputMethod.file:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"Task is of type {task.output_method.value}. File is expected."
        )

    if task.status != enums.TaskStatus.completed:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Task is not completed yet. Status is {task.status.value}.")

    return create_task_visualization(source_file.path, task.output_path, minimum_path_length, clusters)


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
