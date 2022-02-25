from itertools import permutations
from typing import List

from fastapi import APIRouter, Depends, status

from tsa.app.schemas import ResponseLine
from tsa.app.repositories.lines import LinesRepository
from tsa.app.repositories.task import TaskRepository
from tsa.config import config
from tsa.dataclasses.geometry import Line
from tsa.processes.count_vehicles import count_vehicles as perform_count_vehicles
from tsa.storage.file import FileStorageMethod

router = APIRouter(prefix="/lines", tags=["lines"])


@router.get(
    "/{lines_id}",
    description="Count the vehicles that cross the lines.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Lines were not found."}},
    response_model=List[ResponseLine],
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
        [Line([line.start, line.end]) for line in lines.lines],
    )
    counts = counts.tolist()

    response_counts_unknown = [
        ResponseLine(source_name=line.name, destination_name="UNDEFINED", count=counts[i][-1])
        for i, line in enumerate(lines.lines)
    ]

    response_counts_known = (
        [
            ResponseLine(source_name=lines.lines[a].name, destination_name=lines.lines[b].name, count=counts[a][b])
            for a, b in permutations(range(len(lines.lines)))
            if a != b
        ]
        if len(lines.lines) > 1
        else []
    )

    return response_counts_known + response_counts_unknown


@router.delete(
    "/{lines_id}",
    description="Delete selected lines.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Lines were not found."}},
    status_code=status.HTTP_200_OK,
)
async def delete_lines(lines_id: int, lines_repository: LinesRepository = Depends(LinesRepository)):
    await lines_repository.delete(lines_id)
