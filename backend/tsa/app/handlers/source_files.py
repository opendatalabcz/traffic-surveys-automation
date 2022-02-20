from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from tsa import enums
from tsa.app.disk_manager import DiskManager
from tsa.app.internal.create_task import create_task as perform_create_task
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.repositories.task import TaskRepository
from tsa.app.schemas import SourceFile, SourceFileBase, SourceFileWithTasks
from tsa.app.schemas.task import NewTask, Task

router = APIRouter(prefix="/source_file", tags=["source_files"])


def check_source_files_exist(source_files: List[SourceFileBase], location: DiskManager) -> List[bool]:
    files_on_disk = {str(path) for path in location.read_source_files_folder()}
    return [source_file.path in files_on_disk for source_file in source_files]


@router.get(
    "",
    description="List all source files stored in the database.",
    response_model=List[SourceFile],
    status_code=status.HTTP_200_OK,
)
async def list_source_files(
    disk_manager: DiskManager = Depends(DiskManager),
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
) -> List[SourceFile]:
    source_files = await source_file_repository.get_many()
    source_files_existence = check_source_files_exist(source_files, disk_manager)

    return [
        SourceFile(**source_file.dict(), file_exists=exists)
        for source_file, exists in zip(source_files, source_files_existence)
    ]


@router.post(
    "/discover",
    description="Run discovery of new files in the source files folder.",
    response_model=List[SourceFile],
    response_description="Newly discovered source files. Already existing source files are not counted.",
    status_code=status.HTTP_200_OK,
)
async def discover(
    disk_manager: DiskManager = Depends(DiskManager),
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
) -> List[SourceFile]:
    discovered_files = []

    for file in disk_manager.read_source_files_folder():
        source_file = SourceFileBase(path=str(file))
        new_object = await source_file_repository.create(source_file)

        if new_object is not None:
            discovered_files.append(SourceFile(**new_object.dict(), file_exists=True))

    return discovered_files


@router.get(
    "/{source_file_id}",
    description="Get details of a source file with all the tasks connected to the source file.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "The source file does not exist."}},
    response_model=SourceFileWithTasks,
    status_code=status.HTTP_200_OK,
)
async def get_source_file(
    source_file_id: int,
    disk_manager: DiskManager = Depends(DiskManager),
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
    task_repository: TaskRepository = Depends(TaskRepository),
) -> SourceFileWithTasks:
    source_file = await source_file_repository.get_one(source_file_id)
    source_file_tasks = await task_repository.get_many(source_file_id)

    return SourceFileWithTasks(
        **source_file.dict(),
        file_exists=disk_manager.exists_in_source_files_folder(source_file.path),
        tasks=source_file_tasks,
    )


@router.post(
    "/{source_file_id}",
    description="Create a new task to be performed asynchronously in near future.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "The source file is invalid for task creation."},
        status.HTTP_404_NOT_FOUND: {"description": "The source file does not exist."},
    },
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    source_file_id: int,
    task_data: NewTask,
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
    task_repository: TaskRepository = Depends(TaskRepository),
) -> Task:
    source_file = await source_file_repository.get_one(source_file_id)

    if source_file.status == enums.SourceFileStatus.deleted:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Can't create a task for deleted source file.")

    await source_file_repository.update_state(source_file_id, enums.SourceFileStatus.processing)

    return await perform_create_task(task_repository, task_data, source_file_id, source_file.path)
