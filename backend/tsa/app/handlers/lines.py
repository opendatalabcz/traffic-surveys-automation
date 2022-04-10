from fastapi import APIRouter, Depends, status

from tsa.app.repositories.lines import LinesRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import LinesResponse
from tsa.config import config
from tsa.dataclasses.geometry import Line
from tsa.processes.count_vehicles import count_vehicles as perform_count_vehicles
from tsa.storage.file import FileStorageMethod

router = APIRouter(prefix="/lines", tags=["lines"])


@router.get(
    "/{lines_id}",
    description="Count the vehicles that cross the lines.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Lines were not found."}},
    response_model=LinesResponse,
    status_code=status.HTTP_200_OK,
)
async def count_vehicles(
    lines_id: int,
    lines_repository: LinesRepository = Depends(LinesRepository),
    task_repository: TaskRepository = Depends(TaskRepository),
):
    lines = await lines_repository.get_one(lines_id)
    task = await task_repository.get_one(lines.task_id)

    counts = perform_count_vehicles(
        FileStorageMethod(config.OUTPUT_FILES_PATH / task.output_path),
        [Line([line.start.as_tuple(), line.end.as_tuple()]) for line in lines.lines],
    )
    counts = counts.tolist()

    return LinesResponse(names=[line.name for line in lines.lines] + ["Other direction"], counts=counts)


@router.delete(
    "/{lines_id}",
    description="Delete selected lines.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Lines were not found."}},
    status_code=status.HTTP_200_OK,
)
async def delete_lines(lines_id: int, lines_repository: LinesRepository = Depends(LinesRepository)):
    await lines_repository.delete(lines_id)
